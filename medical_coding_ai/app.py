"""
app.py - Streamlit Web Application
AI-Assisted Medical Coding Support System
"""

import os
import streamlit as st
import pandas as pd

from database_helper import create_database, save_result, get_accuracy_stats, DB_PATH
from icd_lookup import search_icd_codes, get_category_for_code
from gemini_helper import get_icd_suggestion, parse_gemini_response

# Ensure database table exists
create_database()

st.set_page_config(
    page_title="AI Medical Coding Support",
    page_icon="🏥",
    layout="wide"
)

# Custom header styling
st.title("🏥 AI-Assisted Medical Coding Support System")
st.caption("Clinical decision-support tool for ICD-10 coding. Human verification required.")

# --- SIDEBAR: Configuration & Statistics ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check for API key in Streamlit secrets, environment, or user input
    default_key = ""
    if "GROQ_API_KEY" in st.secrets:
        default_key = st.secrets["GROQ_API_KEY"]
    elif os.environ.get("GROQ_API_KEY"):
        default_key = os.environ.get("GROQ_API_KEY")

    api_key_input = st.text_input(
        "Groq API Key (Optional override)",
        value=default_key,
        type="password",
        help="Leave default if already set via .env or Streamlit Secrets."
    )
    if api_key_input:
        os.environ["GROQ_API_KEY"] = api_key_input

    st.markdown("---")
    st.header("📊 Session Statistics")
    stats = get_accuracy_stats()
    col_s1, col_s2 = st.columns(2)
    col_s1.metric("Total Cases", stats["total_cases"])
    col_s2.metric("Accuracy", f"{stats['accuracy_percent']}%")
    
    col_s3, col_s4 = st.columns(2)
    col_s3.metric("Correct", stats["correct"])
    col_s4.metric("Incorrect", stats["incorrect"])

    st.markdown("---")
    st.info("💡 **Tip**: Certified coders must verify all AI-generated suggestions before submission to billing.")

# --- MAIN CONTENT ---
st.subheader("📝 Enter Clinical Notes")

# Quick example loader
examples = {
    "Select an example...": "",
    "Endocrinology (Diabetes w/ Neuropathy)": "Patient with poorly controlled type 2 diabetes mellitus, presenting with bilateral lower extremity diabetic peripheral neuropathy.",
    "Cardiology (Acute Heart Failure)": "68-year-old male admitted with acute decompensated systolic heart failure, severe dyspnea on exertion, and bilateral lower extremity pitting edema.",
    "Negation Test (No complications)": "Routine follow-up for type 1 diabetes mellitus. Patient reports no diabetic neuropathy or nephropathy at this time.",
    "Pulmonology (COPD with Exacerbation)": "Patient with severe chronic obstructive pulmonary disease presenting with acute exacerbation and worsening shortness of breath."
}

selected_example = st.selectbox("Load Sample Case (Optional):", list(examples.keys()))
initial_text = examples[selected_example] if selected_example != "Select an example..." else ""

clinical_notes = st.text_area(
    "Clinical Notes / Discharge Summary:",
    value=initial_text,
    height=120,
    placeholder="e.g., Patient with poorly controlled type 2 diabetes mellitus presenting with bilateral lower extremity diabetic neuropathy..."
)

analyze_btn = st.button("🔍 Analyze & Suggest ICD-10 Code", type="primary", use_container_width=True)

# Session state initialization for holding analysis results
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if analyze_btn:
    if not clinical_notes.strip():
        st.warning("⚠️ Please enter clinical notes before analyzing.")
    else:
        with st.spinner("Searching ICD-10 reference and consulting AI model..."):
            try:
                # 1. Search candidate ICD-10 codes
                relevant_codes = search_icd_codes(clinical_notes)

                # 2. Query LLM
                raw_response = get_icd_suggestion(clinical_notes, relevant_codes)
                parsed = parse_gemini_response(raw_response)
                department = get_category_for_code(parsed["code"])

                st.session_state.analysis_result = {
                    "clinical_text": clinical_notes,
                    "parsed": parsed,
                    "department": department,
                    "verified": False
                }
            except Exception as e:
                st.error(f"❌ Analysis Error: {str(e)}")
                st.info("Please verify that a valid Groq API key is configured in the sidebar or `.env`.")

# --- DISPLAY AI SUGGESTION & VERIFICATION ---
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    parsed = result["parsed"]
    dept = result["department"]

    st.markdown("---")
    st.subheader("🎯 AI Suggestion")

    col_code, col_dept = st.columns([1, 2])
    with col_code:
        st.success(f"### Code: `{parsed['code']}`")
    with col_dept:
        st.info(f"**Department:** {dept}  \n**Description:** {parsed['description']}")

    st.markdown(f"**🧠 Clinical Reasoning:** {parsed['reasoning']}")
    if parsed.get("caveat"):
        st.warning(f"**⚠️ Caveat / Consideration:** {parsed['caveat']}")

    # --- HUMAN VERIFICATION SECTION ---
    st.markdown("---")
    st.subheader("✅ Human Verification & Audit")
    
    with st.form("verification_form"):
        is_correct = st.radio(
            "Is the AI-suggested code clinically accurate?",
            options=["YES", "NO"],
            horizontal=True
        )

        col_v1, col_v2 = st.columns(2)
        with col_v1:
            corrected_code = st.text_input(
                "Verified / Corrected Code (if NO):",
                value=parsed["code"] if is_correct == "YES" else "",
                placeholder="e.g. E10.9"
            )
        with col_v2:
            error_reason = st.selectbox(
                "Error Category (if NO):",
                options=[
                    "None",
                    "Subtype Confusion",
                    "Negation Missed",
                    "Specificity Mismatch",
                    "False Keyword Match",
                    "Other / Unlisted Code"
                ],
                disabled=(is_correct == "YES")
            )

        submit_verification = st.form_submit_button("💾 Save Verification to Audit Log")

        if submit_verification:
            final_code = parsed["code"] if is_correct == "YES" else (corrected_code.strip() or parsed["code"])
            final_error = "None" if is_correct == "YES" else error_reason
            
            # Update department if corrected code matches a known category
            final_dept = dept
            if is_correct == "NO" and final_code:
                detected_dept = get_category_for_code(final_code)
                if detected_dept != "General Medicine":
                    final_dept = detected_dept

            save_result(
                clinical_text=result["clinical_text"],
                suggested_code=parsed["code"],
                suggested_description=parsed["description"],
                gemini_reasoning=parsed["reasoning"],
                verified_code=final_code,
                is_correct=is_correct,
                department=final_dept,
                error_category=final_error
            )
            st.success("✅ Case successfully verified and logged to database!")
            st.session_state.analysis_result = None
            st.rerun()

# --- RECENT AUDIT LOG TABLE ---
st.markdown("---")
st.subheader("📋 Recent Verification Log")
try:
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    recent_df = pd.read_sql_query(
        "SELECT id, clinical_text, suggested_code, verified_code, is_correct, department, error_category, timestamp FROM coding_results ORDER BY id DESC LIMIT 10",
        conn
    )
    conn.close()
    if not recent_df.empty:
        st.dataframe(recent_df, use_container_width=True)
    else:
        st.caption("No cases verified yet in the database.")
except Exception:
    st.caption("Audit log will appear once cases are saved.")
