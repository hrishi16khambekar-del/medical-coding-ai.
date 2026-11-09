"""
generate_tableau_dataset.py
Generates an enriched, highly realistic dataset of 50 clinical coding cases
specifically structured for Tableau visualization and auditing.
"""

import os
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_cases():
    cases = [
        # --- ENDOCRINOLOGY ---
        {
            "department": "Endocrinology",
            "clinical_note": "Patient with poorly controlled type 2 diabetes mellitus, presenting with bilateral lower extremity diabetic peripheral neuropathy.",
            "suggested_code": "E11.40",
            "suggested_description": "Type 2 diabetes mellitus with diabetic neuropathy, unspecified",
            "confidence_score": 0.94,
            "is_correct": "YES",
            "verified_code": "E11.40",
            "verified_description": "Type 2 diabetes mellitus with diabetic neuropathy, unspecified",
            "error_category": "None",
            "coder_id": "Coder_A"
        },
        {
            "department": "Endocrinology",
            "clinical_note": "Routine follow-up for type 1 diabetes mellitus. Patient reports no diabetic neuropathy or nephropathy at this time.",
            "suggested_code": "E10.40",
            "suggested_description": "Type 1 diabetes mellitus with diabetic neuropathy, unspecified",
            "confidence_score": 0.81,
            "is_correct": "NO",
            "verified_code": "E10.9",
            "verified_description": "Type 1 diabetes mellitus without complications",
            "error_category": "Negation Missed",
            "coder_id": "Coder_B"
        },
        {
            "department": "Endocrinology",
            "clinical_note": "Patient with established type 2 diabetes mellitus and chronic kidney disease stage 3.",
            "suggested_code": "E11.22",
            "suggested_description": "Type 2 diabetes mellitus with diabetic chronic kidney disease",
            "confidence_score": 0.96,
            "is_correct": "YES",
            "verified_code": "E11.22",
            "verified_description": "Type 2 diabetes mellitus with diabetic chronic kidney disease",
            "error_category": "None",
            "coder_id": "Coder_A"
        },
        {
            "department": "Endocrinology",
            "clinical_note": "Uncontrolled hyperglycemia in patient with history of gestational diabetes, now 6 months postpartum.",
            "suggested_code": "O24.419",
            "suggested_description": "Gestational diabetes mellitus in pregnancy, unspecified control",
            "confidence_score": 0.68,
            "is_correct": "NO",
            "verified_code": "R73.09",
            "verified_description": "Other abnormal glucose (postpartum follow-up)",
            "error_category": "Subtype Confusion",
            "coder_id": "Coder_C"
        },
        {
            "department": "Endocrinology",
            "clinical_note": "Patient with primary hypothyroidism on stable levothyroxine replacement therapy.",
            "suggested_code": "E03.9",
            "suggested_description": "Hypothyroidism, unspecified",
            "confidence_score": 0.95,
            "is_correct": "YES",
            "verified_code": "E03.9",
            "verified_description": "Hypothyroidism, unspecified",
            "error_category": "None",
            "coder_id": "Coder_A"
        },
        {
            "department": "Endocrinology",
            "clinical_note": "Follow-up for type 2 diabetes mellitus. Blood glucose well regulated on metformin, no retinopathy noted.",
            "suggested_code": "E11.9",
            "suggested_description": "Type 2 diabetes mellitus without complications",
            "confidence_score": 0.92,
            "is_correct": "YES",
            "verified_code": "E11.9",
            "verified_description": "Type 2 diabetes mellitus without complications",
            "error_category": "None",
            "coder_id": "Coder_B"
        },

        # --- CARDIOLOGY ---
        {
            "department": "Cardiology",
            "clinical_note": "Patient admitted with acute subendocardial non-ST elevation myocardial infarction (NSTEMI). Cardiac troponins elevated.",
            "suggested_code": "I21.4",
            "suggested_description": "Non-ST elevation (NSTEMI) myocardial infarction",
            "confidence_score": 0.97,
            "is_correct": "YES",
            "verified_code": "I21.4",
            "verified_description": "Non-ST elevation (NSTEMI) myocardial infarction",
            "error_category": "None",
            "coder_id": "Coder_B"
        },
        {
            "department": "Cardiology",
            "clinical_note": "Elderly patient with chronic essential hypertension, blood pressure reading 152/94 mmHg.",
            "suggested_code": "I10",
            "suggested_description": "Essential (primary) hypertension",
            "confidence_score": 0.98,
            "is_correct": "YES",
            "verified_code": "I10",
            "verified_description": "Essential (primary) hypertension",
            "error_category": "None",
            "coder_id": "Coder_A"
        },
        {
            "department": "Cardiology",
            "clinical_note": "Patient presents with paroxysmal atrial fibrillation; successfully rate controlled with beta blockers.",
            "suggested_code": "I48.0",
            "suggested_description": "Paroxysmal atrial fibrillation",
            "confidence_score": 0.93,
            "is_correct": "YES",
            "verified_code": "I48.0",
            "verified_description": "Paroxysmal atrial fibrillation",
            "error_category": "None",
            "coder_id": "Coder_C"
        },
        {
            "department": "Cardiology",
            "clinical_note": "Patient with acute decompensated systolic heart failure with severe dyspnea on exertion.",
            "suggested_code": "I50.9",
            "suggested_description": "Heart failure, unspecified",
            "confidence_score": 0.74,
            "is_correct": "NO",
            "verified_code": "I50.21",
            "verified_description": "Acute systolic (congestive) heart failure",
            "error_category": "Specificity Mismatch",
            "coder_id": "Coder_A"
        },
        {
            "department": "Cardiology",
            "clinical_note": "Patient evaluated for recurrent chest pain on exertion. Diagnosed with atherosclerotic heart disease with stable angina pectoris.",
            "suggested_code": "I25.110",
            "suggested_description": "Atherosclerotic heart disease of native coronary artery with unstable angina pectoris",
            "confidence_score": 0.79,
            "is_correct": "NO",
            "verified_code": "I25.119",
            "verified_description": "Atherosclerotic heart disease with angina pectoris, other",
            "error_category": "Subtype Confusion",
            "coder_id": "Coder_B"
        },
        {
            "department": "Cardiology",
            "clinical_note": "Chronic combined systolic and diastolic congestive heart failure, stable on current outpatient regimen.",
            "suggested_code": "I50.42",
            "suggested_description": "Chronic combined systolic and diastolic (congestive) heart failure",
            "confidence_score": 0.95,
            "is_correct": "YES",
            "verified_code": "I50.42",
            "verified_description": "Chronic combined systolic and diastolic (congestive) heart failure",
            "error_category": "None",
            "coder_id": "Coder_C"
        },
        {
            "department": "Cardiology",
            "clinical_note": "Hypertensive emergency with blood pressure 210/115 mmHg without acute target organ damage.",
            "suggested_code": "I16.0",
            "suggested_description": "Hypertensive urgency",
            "confidence_score": 0.88,
            "is_correct": "YES",
            "verified_code": "I16.0",
            "verified_description": "Hypertensive urgency",
            "error_category": "None",
            "coder_id": "Coder_A"
        },

        # --- PULMONOLOGY / RESPIRATORY ---
        {
            "department": "Pulmonology",
            "clinical_note": "Patient with chronic obstructive pulmonary disease (COPD) presenting with acute exacerbation and productive cough.",
            "suggested_code": "J44.1",
            "suggested_description": "Chronic obstructive pulmonary disease with (acute) exacerbation",
            "confidence_score": 0.96,
            "is_correct": "YES",
            "verified_code": "J44.1",
            "verified_description": "Chronic obstructive pulmonary disease with (acute) exacerbation",
            "error_category": "None",
            "coder_id": "Coder_B"
        },
        {
            "department": "Pulmonology",
            "clinical_note": "Young adult with mild intermittent asthma, currently asymptomatic without status asthmaticus.",
            "suggested_code": "J45.20",
            "suggested_description": "Mild intermittent asthma, uncomplicated",
            "confidence_score": 0.91,
            "is_correct": "YES",
            "verified_code": "J45.20",
            "verified_description": "Mild intermittent asthma, uncomplicated",
            "error_category": "None",
            "coder_id": "Coder_A"
        },
        {
            "department": "Pulmonology",
            "clinical_note": "Community acquired acute pneumonia of the right lower lobe, organism unspecified.",
            "suggested_code": "J18.9",
            "suggested_description": "Pneumonia, unspecified organism",
            "confidence_score": 0.94,
            "is_correct": "YES",
            "verified_code": "J18.9",
            "verified_description": "Pneumonia, unspecified organism",
            "error_category": "None",
            "coder_id": "Coder_C"
        },
        {
            "department": "Pulmonology",
            "clinical_note": "Patient with severe persistent asthma with acute exacerbation triggered by viral infection.",
            "suggested_code": "J45.901",
            "suggested_description": "Unspecified asthma with (acute) exacerbation",
            "confidence_score": 0.72,
            "is_correct": "NO",
            "verified_code": "J45.51",
            "verified_description": "Severe persistent asthma with (acute) exacerbation",
            "error_category": "Specificity Mismatch",
            "coder_id": "Coder_B"
        },
        {
            "department": "Pulmonology",
            "clinical_note": "Acute bronchitis due to viral infection, chest X-ray confirms no focal consolidation or pneumonia.",
            "suggested_code": "J18.9",
            "suggested_description": "Pneumonia, unspecified organism",
            "confidence_score": 0.65,
            "is_correct": "NO",
            "verified_code": "J20.9",
            "verified_description": "Acute bronchitis, unspecified",
            "error_category": "Negation Missed",
            "coder_id": "Coder_A"
        },
        {
            "department": "Pulmonology",
            "clinical_note": "Chronic respiratory failure with hypoxia requiring nocturnal supplemental oxygen therapy.",
            "suggested_code": "J96.11",
            "suggested_description": "Chronic respiratory failure with hypoxia",
            "confidence_score": 0.95,
            "is_correct": "YES",
            "verified_code": "J96.11",
            "verified_description": "Chronic respiratory failure with hypoxia",
            "error_category": "None",
            "coder_id": "Coder_C"
        },

        # --- NEUROLOGY ---
        {
            "department": "Neurology",
            "clinical_note": "Acute ischemic cerebral infarction of the middle cerebral artery territory with left hemiparesis.",
            "suggested_code": "I63.512",
            "suggested_description": "Cerebral infarction due to unspecified occlusion or stenosis of left middle cerebral artery",
            "confidence_score": 0.93,
            "is_correct": "YES",
            "verified_code": "I63.512",
            "verified_description": "Cerebral infarction due to unspecified occlusion or stenosis of left middle cerebral artery",
            "error_category": "None",
            "coder_id": "Coder_B"
        },
        {
            "department": "Neurology",
            "clinical_note": "Patient presents with frequent intractable migraine with aura, accompanied by photophobia and nausea.",
            "suggested_code": "G43.119",
            "suggested_description": "Migraine with aura, intractable, without status migrainosus",
            "confidence_score": 0.90,
            "is_correct": "YES",
            "verified_code": "G43.119",
            "verified_description": "Migraine with aura, intractable, without status migrainosus",
            "error_category": "None",
            "coder_id": "Coder_A"
        },
        {
            "department": "Neurology",
            "clinical_note": "Evaluation for focal epilepsy with impairment of consciousness, not intractable.",
            "suggested_code": "G40.209",
            "suggested_description": "Localization-related (focal) symptomatic epilepsy and epileptic syndromes with complex partial seizures, not intractable",
            "confidence_score": 0.89,
            "is_correct": "YES",
            "verified_code": "G40.209",
            "verified_description": "Localization-related symptomatic epilepsy, not intractable",
            "error_category": "None",
            "coder_id": "Coder_C"
        },
        {
            "department": "Neurology",
            "clinical_note": "Patient presenting with resting tremor, rigidity, and bradykinesia consistent with Parkinson's disease.",
            "suggested_code": "G20",
            "suggested_description": "Parkinson's disease",
            "confidence_score": 0.96,
            "is_correct": "YES",
            "verified_code": "G20",
            "verified_description": "Parkinson's disease",
            "error_category": "None",
            "coder_id": "Coder_B"
        },
        {
            "department": "Neurology",
            "clinical_note": "Transient ischemic attack (TIA) with complete resolution of speech slurring within 45 minutes, no persistent stroke.",
            "suggested_code": "I63.9",
            "suggested_description": "Cerebral infarction, unspecified",
            "confidence_score": 0.69,
            "is_correct": "NO",
            "verified_code": "G45.9",
            "verified_description": "Transient cerebral ischemic attack, unspecified",
            "error_category": "Negation Missed",
            "coder_id": "Coder_A"
        },

        # --- ORTHOPEDICS ---
        {
            "department": "Orthopedics",
            "clinical_note": "Patient with chronic lower back pain localized to lumbosacral region without sciatica or radiculopathy.",
            "suggested_code": "M54.50",
            "suggested_description": "Low back pain, unspecified",
            "confidence_score": 0.92,
            "is_correct": "YES",
            "verified_code": "M54.50",
            "verified_description": "Low back pain, unspecified",
            "error_category": "None",
            "coder_id": "Coder_A"
        },
        {
            "department": "Orthopedics",
            "clinical_note": "Severe bilateral primary osteoarthritis of the knee joints.",
            "suggested_code": "M17.0",
            "suggested_description": "Bilateral primary osteoarthritis of knee",
            "confidence_score": 0.96,
            "is_correct": "YES",
            "verified_code": "M17.0",
            "verified_description": "Bilateral primary osteoarthritis of knee",
            "error_category": "None",
            "coder_id": "Coder_B"
        },
        {
            "department": "Orthopedics",
            "clinical_note": "Patient with lumbar disc displacement at L4-L5 presenting with documented lumbar radiculopathy.",
            "suggested_code": "M54.50",
            "suggested_description": "Low back pain, unspecified",
            "confidence_score": 0.63,
            "is_correct": "NO",
            "verified_code": "M51.16",
            "verified_description": "Intervertebral disc disorders with radiculopathy, lumbar region",
            "error_category": "Specificity Mismatch",
            "coder_id": "Coder_C"
        },
        {
            "department": "Orthopedics",
            "clinical_note": "Closed non-displaced fracture of the shaft of the right radius, initial encounter for closed fracture.",
            "suggested_code": "S52.301A",
            "suggested_description": "Unspecified fracture of shaft of right radius, initial encounter",
            "confidence_score": 0.88,
            "is_correct": "YES",
            "verified_code": "S52.301A",
            "verified_description": "Unspecified fracture of shaft of right radius, initial encounter",
            "error_category": "None",
            "coder_id": "Coder_B"
        },
        {
            "department": "Orthopedics",
            "clinical_note": "Rotator cuff tear of the right shoulder, non-traumatic, complete tear of supraspinatus tendon.",
            "suggested_code": "M75.121",
            "suggested_description": "Complete rotator cuff tear or rupture of right shoulder, not specified as traumatic",
            "confidence_score": 0.91,
            "is_correct": "YES",
            "verified_code": "M75.121",
            "verified_description": "Complete rotator cuff tear of right shoulder, non-traumatic",
            "error_category": "None",
            "coder_id": "Coder_A"
        },
        {
            "department": "Orthopedics",
            "clinical_note": "Carpal tunnel syndrome affecting the dominant right hand and wrist.",
            "suggested_code": "G56.01",
            "suggested_description": "Carpal tunnel syndrome, right upper limb",
            "confidence_score": 0.95,
            "is_correct": "YES",
            "verified_code": "G56.01",
            "verified_description": "Carpal tunnel syndrome, right upper limb",
            "error_category": "None",
            "coder_id": "Coder_C"
        },

        # --- GASTROENTEROLOGY ---
        {
            "department": "Gastroenterology",
            "clinical_note": "Patient with gastroesophageal reflux disease (GERD) with documented reflux esophagitis on endoscopy.",
            "suggested_code": "K21.0",
            "suggested_description": "Gastro-esophageal reflux disease with esophagitis",
            "confidence_score": 0.94,
            "is_correct": "YES",
            "verified_code": "K21.0",
            "verified_description": "Gastro-esophageal reflux disease with esophagitis",
            "error_category": "None",
            "coder_id": "Coder_A"
        },
        {
            "department": "Gastroenterology",
            "clinical_note": "Acute calculus cholecystitis with gallstones identified on ultrasound examination.",
            "suggested_code": "K80.00",
            "suggested_description": "Calculus of gallbladder with acute cholecystitis without obstruction",
            "confidence_score": 0.91,
            "is_correct": "YES",
            "verified_code": "K80.00",
            "verified_description": "Calculus of gallbladder with acute cholecystitis without obstruction",
            "error_category": "None",
            "coder_id": "Coder_B"
        },
        {
            "department": "Gastroenterology",
            "clinical_note": "Patient with Crohn's disease of the small intestine with intestinal obstruction.",
            "suggested_code": "K50.90",
            "suggested_description": "Crohn's disease, unspecified, without complications",
            "confidence_score": 0.73,
            "is_correct": "NO",
            "verified_code": "K50.012",
            "verified_description": "Crohn's disease of small intestine with intestinal obstruction",
            "error_category": "Specificity Mismatch",
            "coder_id": "Coder_C"
        },
        {
            "department": "Gastroenterology",
            "clinical_note": "Ulcerative colitis, unspecified, currently in endoscopic remission without complications.",
            "suggested_code": "K51.90",
            "suggested_description": "Ulcerative colitis, unspecified, without complications",
            "confidence_score": 0.93,
            "is_correct": "YES",
            "verified_code": "K51.90",
            "verified_description": "Ulcerative colitis, unspecified, without complications",
            "error_category": "None",
            "coder_id": "Coder_A"
        },
        {
            "department": "Gastroenterology",
            "clinical_note": "Acute diverticulitis of the sigmoid colon without perforation or abscess.",
            "suggested_code": "K57.32",
            "suggested_description": "Diverticulitis of large intestine without perforation or abscess without bleeding",
            "confidence_score": 0.92,
            "is_correct": "YES",
            "verified_code": "K57.32",
            "verified_description": "Diverticulitis of large intestine without perforation or abscess without bleeding",
            "error_category": "None",
            "coder_id": "Coder_B"
        },

        # --- NEPHROLOGY / UROLOGY ---
        {
            "department": "Nephrology",
            "clinical_note": "Patient with chronic kidney disease stage 4 (severe decrease in GFR, 22 mL/min).",
            "suggested_code": "N18.4",
            "suggested_description": "Chronic kidney disease, stage 4 (severe)",
            "confidence_score": 0.97,
            "is_correct": "YES",
            "verified_code": "N18.4",
            "verified_description": "Chronic kidney disease, stage 4 (severe)",
            "error_category": "None",
            "coder_id": "Coder_A"
        },
        {
            "department": "Nephrology",
            "clinical_note": "Calculus of the right kidney (nephrolithiasis) causing flank pain, no hydronephrosis.",
            "suggested_code": "N20.0",
            "suggested_description": "Calculus of kidney",
            "confidence_score": 0.94,
            "is_correct": "YES",
            "verified_code": "N20.0",
            "verified_description": "Calculus of kidney",
            "error_category": "None",
            "coder_id": "Coder_B"
        },
        {
            "department": "Nephrology",
            "clinical_note": "Female patient presenting with acute cystitis with dysuria, confirmed urinary tract infection.",
            "suggested_code": "N39.0",
            "suggested_description": "Urinary tract infection, site not specified",
            "confidence_score": 0.90,
            "is_correct": "YES",
            "verified_code": "N39.0",
            "verified_description": "Urinary tract infection, site not specified",
            "error_category": "None",
            "coder_id": "Coder_C"
        },
        {
            "department": "Nephrology",
            "clinical_note": "End stage renal disease (ESRD) on chronic hemodialysis maintenance.",
            "suggested_code": "N18.6",
            "suggested_description": "End stage renal disease",
            "confidence_score": 0.96,
            "is_correct": "YES",
            "verified_code": "N18.6",
            "verified_description": "End stage renal disease",
            "error_category": "None",
            "coder_id": "Coder_A"
        },

        # --- PSYCHIATRY / MENTAL HEALTH ---
        {
            "department": "Psychiatry",
            "clinical_note": "Major depressive disorder, recurrent episode, moderate severity, without psychotic features.",
            "suggested_code": "F33.1",
            "suggested_description": "Major depressive disorder, recurrent, moderate",
            "confidence_score": 0.93,
            "is_correct": "YES",
            "verified_code": "F33.1",
            "verified_description": "Major depressive disorder, recurrent, moderate",
            "error_category": "None",
            "coder_id": "Coder_B"
        },
        {
            "department": "Psychiatry",
            "clinical_note": "Patient presents with persistent severe generalized anxiety disorder and panic attacks.",
            "suggested_code": "F41.1",
            "suggested_description": "Generalized anxiety disorder",
            "confidence_score": 0.92,
            "is_correct": "YES",
            "verified_code": "F41.1",
            "verified_description": "Generalized anxiety disorder",
            "error_category": "None",
            "coder_id": "Coder_C"
        },
        {
            "department": "Psychiatry",
            "clinical_note": "Bipolar I disorder, most recent episode manic, severe with psychotic features.",
            "suggested_code": "F31.9",
            "suggested_description": "Bipolar disorder, unspecified",
            "confidence_score": 0.70,
            "is_correct": "NO",
            "verified_code": "F31.2",
            "verified_description": "Bipolar disorder, current episode manic severe with psychotic features",
            "error_category": "Specificity Mismatch",
            "coder_id": "Coder_A"
        },
        {
            "department": "Psychiatry",
            "clinical_note": "Patient suffering from chronic post-traumatic stress disorder (PTSD) secondary to military combat.",
            "suggested_code": "F43.12",
            "suggested_description": "Post-traumatic stress disorder, chronic",
            "confidence_score": 0.94,
            "is_correct": "YES",
            "verified_code": "F43.12",
            "verified_description": "Post-traumatic stress disorder, chronic",
            "error_category": "None",
            "coder_id": "Coder_B"
        },

        # --- INFECTIOUS DISEASE / ONCOLOGY / GENERAL ---
        {
            "department": "Infectious Disease",
            "clinical_note": "Confirmed COVID-19 infection with acute upper respiratory symptoms and fever.",
            "suggested_code": "U07.1",
            "suggested_description": "COVID-19",
            "confidence_score": 0.98,
            "is_correct": "YES",
            "verified_code": "U07.1",
            "verified_description": "COVID-19",
            "error_category": "None",
            "coder_id": "Coder_C"
        },
        {
            "department": "Infectious Disease",
            "clinical_note": "Patient with cellulitis of the left lower limb involving erythema, edema, and warmth.",
            "suggested_code": "L03.116",
            "suggested_description": "Cellulitis of left lower limb",
            "confidence_score": 0.93,
            "is_correct": "YES",
            "verified_code": "L03.116",
            "verified_description": "Cellulitis of left lower limb",
            "error_category": "None",
            "coder_id": "Coder_A"
        },
        {
            "department": "Infectious Disease",
            "clinical_note": "Severe sepsis secondary to community acquired pneumonia, with acute organ dysfunction.",
            "suggested_code": "A41.9",
            "suggested_description": "Sepsis, unspecified organism",
            "confidence_score": 0.78,
            "is_correct": "NO",
            "verified_code": "R65.20",
            "verified_description": "Severe sepsis without septic shock",
            "error_category": "Subtype Confusion",
            "coder_id": "Coder_B"
        },
        {
            "department": "Oncology",
            "clinical_note": "Malignant neoplasm of upper-outer quadrant of right female breast.",
            "suggested_code": "C50.411",
            "suggested_description": "Malignant neoplasm of upper-outer quadrant of right female breast",
            "confidence_score": 0.95,
            "is_correct": "YES",
            "verified_code": "C50.411",
            "verified_description": "Malignant neoplasm of upper-outer quadrant of right female breast",
            "error_category": "None",
            "coder_id": "Coder_C"
        },
        {
            "department": "Oncology",
            "clinical_note": "Patient with secondary malignant neoplasm of the lung metastatic from primary colon adenocarcinoma.",
            "suggested_code": "C34.90",
            "suggested_description": "Malignant neoplasm of unspecified part of bronchus or lung",
            "confidence_score": 0.71,
            "is_correct": "NO",
            "verified_code": "C78.00",
            "verified_description": "Secondary malignant neoplasm of unspecified lung",
            "error_category": "Subtype Confusion",
            "coder_id": "Coder_A"
        },
        {
            "department": "General Medicine",
            "clinical_note": "Patient presenting with acute dehydration and electrolyte imbalance due to gastroenteritis.",
            "suggested_code": "E86.0",
            "suggested_description": "Dehydration",
            "confidence_score": 0.92,
            "is_correct": "YES",
            "verified_code": "E86.0",
            "verified_description": "Dehydration",
            "error_category": "None",
            "coder_id": "Coder_B"
        }
    ]

    # Generate dates across past 3 weeks
    start_date = datetime(2026, 9, 12, 9, 0)
    records = []

    for i, case in enumerate(cases, 1):
        # Spacing dates
        day_offset = (i * 15) // 50
        hour_offset = (i * 7) % 8
        minute_offset = (i * 13) % 60
        created_at = start_date + timedelta(days=day_offset, hours=hour_offset, minutes=minute_offset)
        
        # Audit recommendation
        audit_flag = "Low Risk (Auto-Approved)" if case["is_correct"] == "YES" and case["confidence_score"] >= 0.90 else (
            "Medium Review" if case["is_correct"] == "YES" else "High Priority Override"
        )

        records.append({
            "case_id": i,
            "created_date": created_at.strftime("%Y-%m-%d"),
            "created_timestamp": created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "department": case["department"],
            "clinical_note": case["clinical_note"],
            "suggested_code": case["suggested_code"],
            "suggested_description": case["suggested_description"],
            "confidence_score": case["confidence_score"],
            "human_verified": "ACCEPTED" if case["is_correct"] == "YES" else "OVERRIDDEN",
            "is_correct": case["is_correct"],
            "verified_code": case["verified_code"],
            "verified_description": case["verified_description"],
            "error_category": case["error_category"],
            "coder_id": case["coder_id"],
            "audit_risk_level": audit_flag,
            "processing_seconds": round(random.uniform(1.2, 3.4), 2)
        })

    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    df = generate_cases()
    
    # 1. Save in medical_coding_ai/database
    os.makedirs("database", exist_ok=True)
    out_path1 = os.path.join("database", "tableau_coding_cases.csv")
    df.to_csv(out_path1, index=False)
    print(f"Generated {len(df)} records -> {out_path1}")

    # 2. Also save in Desktop DA Project/medical_AI if it exists
    desktop_target = r"C:\Users\hrish\OneDrive\Desktop\DA Project\medical_AI"
    if os.path.exists(desktop_target):
        out_path2 = os.path.join(desktop_target, "tableau_coding_cases.csv")
        df.to_csv(out_path2, index=False)
        print(f"Copied {len(df)} records -> {out_path2}")
    
    # Summary statistics
    total = len(df)
    correct = (df["is_correct"] == "YES").sum()
    accuracy = round((correct / total) * 100, 2)
    print("\n--- DATASET SUMMARY ---")
    print(f"Total Cases: {total}")
    print(f"Accuracy Rate: {accuracy}% ({correct}/{total})")
    print(f"Human Override Rate: {round(100 - accuracy, 2)}%")
    print("\nOverrides by Error Category:")
    print(df[df["is_correct"] == "NO"]["error_category"].value_counts())
    print("\nDepartment Breakdown:")
    print(df["department"].value_counts())
