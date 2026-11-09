# 🏥 AI-Assisted Medical Coding Support System

An AI-driven decision-support tool that assists clinical documentation specialists and medical coders in identifying, verifying, and assigning the most clinically specific ICD-10 diagnosis codes from clinical notes.

> **⚠️ Disclaimer**: For support and educational use only. Human verification by certified medical coding professionals is required.

---

## 🚀 Features

- **Clinical Text Processing**: Parses unstructured physician notes and clinical summaries.
- **ICD-10 Code Lookup**: Searches and ranks relevant ICD-10 candidate codes.
- **LLM-Powered Decision Support**: Uses Groq-hosted models to evaluate clinical acuity, specificity, and coding guidelines.
- **Audit & Human Verification**: Tracks verification status, coder corrections, and accuracy metrics in a SQLite database.
- **Tableau Analytics Export**: Generates enriched reporting datasets for visual auditing and compliance analytics.

---

## 📁 Project Structure

```text
medical_coding_ai/
├── data/
│   └── icd10_codes.csv           # ICD-10 reference dataset
├── database/
│   ├── results.db                # SQLite audit database
│   ├── results_export.csv        # Exported session data
│   └── tableau_coding_cases.csv  # Tableau-ready dataset
├── database_helper.py            # SQLite operations & accuracy tracking
├── app.py                        # Streamlit web application
├── gemini_helper.py              # LLM integration & prompt engineering
├── generate_tableau_dataset.py   # Synthetic cohort generator for analytics
├── icd_lookup.py                 # Keyword search & category mapping
├── main.py                       # CLI application entry point
├── requirements.txt              # Python dependencies
└── README.md
```

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/<your-username>/medical-coding-ai.git
   cd medical-coding-ai
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Groq API Key**:
   Create a `.env` file or set the environment variable:
   ```bash
   # Create a .env file:
   cp .env.example .env
   # Then edit .env with your GROQ_API_KEY
   ```

4. **Run the Application**:
   - **Interactive Web App (Streamlit)**:
     ```bash
     streamlit run app.py
     ```
   - **Terminal CLI**:
     ```bash
     python main.py
     ```

---

## 🌐 Deploy Free on Streamlit Cloud (1-Click Public Demo)

1. Push this repository to GitHub.
2. Sign in at [share.streamlit.io](https://share.streamlit.io/) with your GitHub account.
3. Select this repository and set main file to `app.py`.
4. Under **Advanced settings > Secrets**, add your key:
   ```toml
   GROQ_API_KEY = "your-groq-api-key"
   ```
5. Click **Deploy!** Anyone with your link can now test your AI live in their web browser without installing anything.
