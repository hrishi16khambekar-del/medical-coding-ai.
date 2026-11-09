# ============================================================
# main.py
# This is the MAIN file — run this to start the program
# 
# How to run: python main.py
# ============================================================

import sys

# Ensure Windows terminal handles emojis/UTF-8 cleanly
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from database_helper import create_database, save_result, get_accuracy_stats, export_to_csv
from icd_lookup import search_icd_codes, get_category_for_code
from gemini_helper import get_icd_suggestion, parse_gemini_response


def print_banner():
    """Prints a welcome banner."""
    print("\n" + "=" * 60)
    print("   🏥 AI-ASSISTED MEDICAL CODING SUPPORT SYSTEM")
    print("   ⚠️  For support use only — Human verification required")
    print("=" * 60 + "\n")


def print_stats():
    """Prints current accuracy statistics."""
    stats = get_accuracy_stats()
    print("\n📊 SESSION STATISTICS:")
    print(f"   Total Cases : {stats['total_cases']}")
    print(f"   Correct     : {stats['correct']}")
    print(f"   Incorrect   : {stats['incorrect']}")
    print(f"   Accuracy    : {stats['accuracy_percent']}%")
    print("-" * 60)


def run_coding_session():
    """Runs one coding session for a clinical case."""

    print("\n📝 Enter the clinical notes below.")
    print("   (Example: 'Patient has type 2 diabetes with neuropathy')")
    print("   Type 'quit' to exit.\n")

    clinical_text = input("Clinical Notes: ").strip()

    if clinical_text.lower() == "quit":
        return False  # Signal to stop the loop

    if not clinical_text:
        print("⚠️  Please enter some clinical notes.")
        return True

    print("\n🔍 Searching ICD-10 database...")
    relevant_codes = search_icd_codes(clinical_text)

    print("🤖 Asking Gemini AI for code suggestion...")
    try:
        raw_response = get_icd_suggestion(clinical_text, relevant_codes)
        parsed = parse_gemini_response(raw_response)
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        print("   Please check your API key in gemini_helper.py")
        return True

    # Detect medical department/category from the suggested code
    department = get_category_for_code(parsed["code"])

    # Display the AI suggestion
    print("\n" + "=" * 60)
    print("🎯 AI SUGGESTION (Needs Human Verification)")
    print("=" * 60)
    print(f"   Department     : {department}")
    print(f"   Suggested Code : {parsed['code']}")
    print(f"   Description    : {parsed['description']}")
    print(f"   Reasoning      : {parsed['reasoning']}")
    print(f"   Caveat         : {parsed['caveat']}")
    print("=" * 60)

    # Human verification step
    print("\n✅ HUMAN VERIFICATION REQUIRED")
    is_correct = input("   Is this suggestion CORRECT? (yes/no): ").strip().upper()

    error_category = "None"
    if is_correct == "YES":
        verified_code = parsed["code"]
        correct_flag = "YES"
        print("✅ Marked as CORRECT — saved.")
    else:
        print("\n   What is the correct ICD-10 code?")
        verified_code = input("   Enter correct code (e.g. E11.40): ").strip()
        correct_flag = "NO"
        
        # If the verified code belongs to a known category, use it
        verified_dept = get_category_for_code(verified_code)
        if verified_dept != "General Medicine":
            department = verified_dept

        print("\n   ⚠️  HUMAN OVERRIDE — Why was the AI suggestion incorrect?")
        print("   1. Subtype Confusion (e.g., Type 1 vs Type 2 diabetes)")
        print("   2. Negation Missed (e.g., patient does NOT have condition)")
        print("   3. Specificity Mismatch (e.g., unspecified instead of acute)")
        print("   4. False Keyword Match (e.g., irrelevant symptom matched)")
        print("   5. Other / Unlisted Code")
        reason_choice = input("   Select reason (1-5 or type custom text): ").strip()
        
        reasons_map = {
            "1": "Subtype Confusion",
            "2": "Negation Missed",
            "3": "Specificity Mismatch",
            "4": "False Keyword Match",
            "5": "Other / Unlisted Code"
        }
        error_category = reasons_map.get(reason_choice, reason_choice if reason_choice else "Other")
        print(f"✅ Marked as INCORRECT — Reason '{error_category}' recorded.")

    # Save to database
    save_result(
        clinical_text=clinical_text,
        suggested_code=parsed["code"],
        suggested_description=parsed["description"],
        gemini_reasoning=parsed["reasoning"],
        verified_code=verified_code,
        is_correct=correct_flag,
        department=department,
        error_category=error_category
    )

    # Show updated stats
    print_stats()

    return True  # Continue the loop


def main():
    """Main function — runs the full program."""

    print_banner()

    # Set up the database
    create_database()

    print("\n📋 MENU:")
    print("   1. Start Coding Session")
    print("   2. View Statistics")
    print("   3. Export Data to CSV (for Power BI)")
    print("   4. Quit")

    while True:
        print("\n" + "-" * 60)
        choice = input("Enter choice (1/2/3/4): ").strip()

        if choice == "1":
            # Run coding sessions until user types 'quit'
            keep_going = True
            while keep_going:
                keep_going = run_coding_session()

        elif choice == "2":
            print_stats()

        elif choice == "3":
            path = export_to_csv()
            print(f"   Open this file in Power BI: {path}")

        elif choice == "4":
            print("\n👋 Goodbye! Your data is saved in the database folder.")
            break

        else:
            print("⚠️  Please enter 1, 2, 3, or 4.")


# Run the program
if __name__ == "__main__":
    main()
