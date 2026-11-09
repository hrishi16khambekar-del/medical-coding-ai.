# ============================================================
# gemini_helper.py
# Using GROQ API
# Model: GPT-OSS 120B via Groq Cloud
# ============================================================

import os
import re
from groq import Groq

# Automatically load environment variables from .env if present
def _load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

_load_env()

# Groq API key (loaded securely from environment or .env)
API_KEY = os.environ.get("GROQ_API_KEY", "")


def get_icd_suggestion(clinical_text, relevant_codes):
    """
    Sends clinical text + relevant ICD-10 codes to Groq AI.
    Returns the AI's suggested code and reasoning.
    """

    # Create Groq client
    client = Groq(api_key=API_KEY)

    # Build the prompt
    prompt = f"""
You are an expert AI assistant helping with medical coding support.

A healthcare professional has provided the following clinical notes:
"{clinical_text}"

Here are potentially relevant ICD-10 codes from our database:
{relevant_codes}

Your task:
1. Suggest the SINGLE most appropriate and clinically specific ICD-10 code from the list above.
2. Explain your reasoning in 2-3 simple sentences.
3. Mention any important caveats.

CLINICAL & CODING GUIDELINES:
- Prioritize Highest Specificity: Always select the most specific code that is documented (e.g., exact subtype, anatomical site, or acuity: acute vs. chronic vs. acute-on-chronic) over generic or "unspecified" (.9) codes.
- Acuity Mapping: Under ICD-10-CM guidelines and AHA Coding Clinic conventions, "acute decompensated" heart failure maps to acute heart failure (e.g., acute decompensated systolic heart failure -> I50.21).
- Selection Rule: Prefer the best matching code from the provided list. If an exact, highly specific ICD-10 code is required but not in the list, state it in the CAVEAT.
- Quality Assurance: A qualified medical coder must verify all suggestions.

Respond in this EXACT format:
SUGGESTED CODE: [code here]
DESCRIPTION: [description here]
REASONING: [your reasoning here]
CAVEAT: [any important note here]
"""

    # Call Groq API
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="openai/gpt-oss-120b",
    )

    return response.choices[0].message.content


def parse_gemini_response(response_text):
    """
    Parses the AI response to extract the code, description, reasoning, and caveat.
    Handles markdown bold (**SUGGESTED CODE:**), list prefixes (1., -), case variations,
    and multi-line reasoning.
    """
    result = {
        "code": "UNKNOWN",
        "description": "UNKNOWN",
        "reasoning": "No reasoning provided",
        "caveat": ""
    }

    current_field = None
    lines = response_text.strip().split("\n")

    for line in lines:
        raw_line = line.strip()
        cleaned_line = re.sub(r"^(?:[-*]|\d+\.)\s+", "", raw_line)

        code_match = re.match(r"^\*?\*?SUGGESTED\s+CODE\*?\*?\s*:\s*\*?\*?(.*)", cleaned_line, re.IGNORECASE)
        desc_match = re.match(r"^\*?\*?DESCRIPTION\*?\*?\s*:\s*\*?\*?(.*)", cleaned_line, re.IGNORECASE)
        reason_match = re.match(r"^\*?\*?REASONING\*?\*?\s*:\s*\*?\*?(.*)", cleaned_line, re.IGNORECASE)
        caveat_match = re.match(r"^\*?\*?CAVEAT\*?\*?\s*:\s*\*?\*?(.*)", cleaned_line, re.IGNORECASE)

        if code_match:
            current_field = "code"
            val = code_match.group(1).strip().strip("*_`")
            if val:
                result["code"] = val
        elif desc_match:
            current_field = "description"
            val = desc_match.group(1).strip().strip("*_`")
            if val:
                result["description"] = val
        elif reason_match:
            current_field = "reasoning"
            val = reason_match.group(1).strip().strip("*_`")
            if val:
                result["reasoning"] = val
        elif caveat_match:
            current_field = "caveat"
            val = caveat_match.group(1).strip().strip("*_`")
            if val:
                result["caveat"] = val
        elif current_field in ("reasoning", "caveat") and raw_line:
            # Multi-line continuation for reasoning or caveat
            if result[current_field] == "No reasoning provided":
                result[current_field] = raw_line.strip("*_`")
            else:
                result[current_field] += " " + raw_line.strip("*_`")

    return result
