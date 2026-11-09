# ============================================================
# icd_lookup.py
# This file searches for relevant ICD-10 codes
# based on keywords in the clinical text
# ============================================================

import os
import re
import pandas as pd

# Path to the ICD-10 CSV file (resolved relative to this file's directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICD_PATH = os.path.join(BASE_DIR, "data", "icd10_codes.csv")

# -------------------------------------------------------
# Synonym dictionary — maps common patient language
# to the medical terms used in ICD-10 descriptions
# -------------------------------------------------------
SYNONYMS = {
    "blood pressure"       : "hypertension",
    "high bp"              : "hypertension",
    "hypertensive"         : "hypertension",
    "heart attack"         : "myocardial infarction",
    "stroke"               : "cerebral infarction",
    "sugar"                : "diabetes",
    "diabetic"             : "diabetes",
    "kidney"               : "renal",
    "lungs"                : "respiratory",
    "breathing"            : "respiratory",
    "back pain"            : "low back pain",
    "backache"             : "low back pain",
    "depression"           : "depressive",
    "cancer"               : "malignant neoplasm",
    "tumor"                : "malignant neoplasm",
    "uti"                  : "urinary tract infection",
    "chest pain"           : "angina",
    "gallstone"            : "calculus of gallbladder",
    "kidney stone"         : "calculus of kidney",
    "copd"                 : "chronic obstructive",
    "nerve damage"         : "neuropathy",
    "afib"                 : "atrial fibrillation",
    "seizure"              : "epilepsy",
    "parkinson"            : "parkinson",
    # Heart Failure & Cardiology specifics
    "chf"                  : "congestive heart failure",
    "adhf"                 : "acute systolic heart failure",
    "decompensated"        : "acute",
    "decompensated heart failure": "acute systolic heart failure",
    "systolic heart failure": "systolic heart failure",
    "diastolic heart failure": "diastolic heart failure",
    "hfref"                : "systolic heart failure",
    "hfpef"                : "diastolic heart failure",
    "nstemi"               : "non-st elevation myocardial infarction",
    "stemi"                : "myocardial infarction",
    "shortness of breath"  : "dyspnea respiratory",
    "sob"                  : "dyspnea",
    "dyspnea"              : "dyspnea respiratory",
    "covid"                : "covid-19",
}


def load_icd_codes():
    """Loads the ICD-10 CSV file into a pandas DataFrame."""
    df = pd.read_csv(ICD_PATH)
    return df


def apply_synonyms(text):
    """
    Replaces common patient terms with medical terms
    so ICD-10 matching works better.
    """
    text_lower = text.lower()
    for common_term, medical_term in SYNONYMS.items():
        if common_term in text_lower:
            text_lower = text_lower + " " + medical_term
    return text_lower


def search_icd_codes(clinical_text):
    """
    Searches the ICD-10 list for codes matching the clinical text.
    Uses synonym expansion and relevance scoring so the most
    specific diagnostic candidates rank first.
    """
    df = load_icd_codes()

    # Expand clinical text with medical synonyms
    expanded_text = apply_synonyms(clinical_text)

    # Generic words that shouldn't independently trigger a match
    skip_words = {"with", "without", "unspecified", "type", "stage",
                  "acute", "chronic", "other", "primary", "secondary",
                  "complications", "noted", "patient", "presents"}

    expanded_words = set(re.findall(r"\b[a-zA-Z0-9_-]+\b", expanded_text))
    scored_matches = []

    for _, row in df.iterrows():
        desc = str(row["description"]).lower()
        desc_words = re.findall(r"\b[a-zA-Z0-9_-]+\b", desc)

        score = 0
        has_primary_match = False

        for w in desc_words:
            if w in expanded_words:
                if len(w) > 3 and w not in skip_words:
                    score += 3
                    has_primary_match = True
                elif w in ("acute", "chronic", "systolic", "diastolic", "primary", "secondary"):
                    score += 2  # Acuity/subtype boosts rank when primary disease matches
                else:
                    score += 1

        if has_primary_match:
            scored_matches.append((score, row))

    if not scored_matches:
        # No keyword match — provide full reference table
        return df[["code", "description", "category"]].to_string(index=False)

    # Sort descending by relevance score
    scored_matches.sort(key=lambda x: x[0], reverse=True)
    matched_df = pd.DataFrame([item[1] for item in scored_matches])

    # Pass the top 20 most relevant candidates to the AI
    top_matches = matched_df.head(20)
    return top_matches[["code", "description", "category"]].to_string(index=False)


DEPARTMENT_MAP = {
    "Diabetes": "Endocrinology",
    "Endocrinology": "Endocrinology",
    "Cardiovascular": "Cardiology",
    "Cardiology": "Cardiology",
    "Respiratory": "Pulmonology",
    "Pulmonology": "Pulmonology",
    "Gastrointestinal": "Gastroenterology",
    "Gastroenterology": "Gastroenterology",
    "Musculoskeletal": "Orthopedics",
    "Orthopedics": "Orthopedics",
    "Renal": "Nephrology",
    "Nephrology": "Nephrology",
    "Mental Health": "Psychiatry",
    "Psychiatry": "Psychiatry",
    "Neurological": "Neurology",
    "Neurology": "Neurology",
    "Oncology": "Oncology",
    "Infectious Disease": "Infectious Disease",
    "History": "General Medicine",
    "Preventive": "Preventive Medicine",
    "General Medicine": "General Medicine",
}


def get_category_for_code(code):
    """
    Looks up the hospital department for a given ICD-10 code.
    Maps categories to proper clinical departments (e.g. Diabetes -> Endocrinology).
    Defaults to 'General Medicine' if code not found in reference table.
    """
    try:
        df = load_icd_codes()
        clean_code = str(code).strip().upper()
        match = df[df["code"].astype(str).str.upper() == clean_code]
        if not match.empty:
            raw_category = match.iloc[0]["category"]
            return DEPARTMENT_MAP.get(raw_category, raw_category)
    except Exception:
        pass
    return "General Medicine"

