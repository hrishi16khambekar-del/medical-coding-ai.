# ============================================================
# database_helper.py
# This file handles all SQLite database operations
# It saves and reads coding results from the database
# ============================================================

import sqlite3  # Built-in Python library for SQLite
import os
import sys

# Ensure Windows terminal handles emojis/UTF-8 cleanly
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Ensure database directory exists before connection
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "results.db")


def create_database():
    """
    Creates the database and the results table if they don't exist.
    Call this once at the start of the program.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table to store coding results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coding_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clinical_text TEXT NOT NULL,
            department TEXT DEFAULT 'General',
            suggested_code TEXT,
            suggested_description TEXT,
            gemini_reasoning TEXT,
            verified_by_human TEXT,
            is_correct TEXT,
            error_category TEXT DEFAULT 'None',
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Auto-migrate existing database if columns are missing
    cursor.execute("PRAGMA table_info(coding_results)")
    existing_columns = [row[1] for row in cursor.fetchall()]
    if "department" not in existing_columns:
        cursor.execute("ALTER TABLE coding_results ADD COLUMN department TEXT DEFAULT 'General'")
    if "error_category" not in existing_columns:
        cursor.execute("ALTER TABLE coding_results ADD COLUMN error_category TEXT DEFAULT 'None'")

    conn.commit()
    conn.close()

    # Backfill proper hospital departments for any historical cases
    backfill_departments()
    print("✅ Database ready.")


def backfill_departments():
    """
    Backfills historical database records with proper hospital departments
    based on their ICD-10 codes.
    """
    try:
        from icd_lookup import get_category_for_code
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, suggested_code, verified_by_human FROM coding_results")
        rows = cursor.fetchall()
        for row_id, suggested_code, verified_code in rows:
            code = verified_code if (verified_code and verified_code != "UNKNOWN") else suggested_code
            dept = get_category_for_code(code)
            cursor.execute("UPDATE coding_results SET department = ? WHERE id = ?", (dept, row_id))
        conn.commit()
        conn.close()
    except Exception:
        pass


def save_result(clinical_text, suggested_code, suggested_description, gemini_reasoning, verified_code, is_correct, department="General", error_category="None"):
    """
    Saves one coding result to the database, including department and error category.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO coding_results 
        (clinical_text, department, suggested_code, suggested_description, gemini_reasoning, verified_by_human, is_correct, error_category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (clinical_text, department, suggested_code, suggested_description, gemini_reasoning, verified_code, is_correct, error_category))

    conn.commit()
    conn.close()
    print("✅ Result saved to database.")


def get_accuracy_stats():
    """
    Reads the database and calculates accuracy statistics.
    Returns a dictionary with stats.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Total cases
    cursor.execute("SELECT COUNT(*) FROM coding_results")
    total = cursor.fetchone()[0]

    # Correct cases
    cursor.execute("SELECT COUNT(*) FROM coding_results WHERE is_correct = 'YES'")
    correct = cursor.fetchone()[0]

    conn.close()

    # Calculate accuracy
    accuracy = (correct / total * 100) if total > 0 else 0

    return {
        "total_cases": total,
        "correct": correct,
        "incorrect": total - correct,
        "accuracy_percent": round(accuracy, 2)
    }


def export_to_csv():
    """
    Exports all results to a CSV file for Tableau / Power BI.
    """
    import pandas as pd
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM coding_results", conn)
    conn.close()

    export_path = os.path.join(DB_DIR, "results_export.csv")
    df.to_csv(export_path, index=False)
    print(f"✅ Data exported to: {export_path}")

    # Also sync to Desktop folder if present
    desktop_dir = r"C:\Users\hrish\OneDrive\Desktop\DA Project\medical_AI"
    if os.path.exists(desktop_dir):
        desktop_path = os.path.join(desktop_dir, "results_export.csv")
        try:
            df.to_csv(desktop_path, index=False)
            print(f"✅ Synced export to Desktop: {desktop_path}")
        except PermissionError:
            print("⚠️ Note: Desktop export file is currently open in Excel or another program. Close it to update Desktop copy.")

    return export_path
