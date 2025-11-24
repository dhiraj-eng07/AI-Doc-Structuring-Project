import json
import re
import google.generativeai as genai
from src.fields import EXPECTED_FIELDS

# -------------------
# API KEY + MODEL
# -------------------
API_KEY = "AIzaSyBSejyBuc5a-4QaoAu74k_CNNbzm3L9rJE"
MODEL_NAME = "models/gemini-2.5-flash"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# -------------------
# PROMPT
# -------------------
def build_prompt(full_text: str):
    return f"""
You are a professional document → structured data extraction system.

You MUST convert the following biography/work/education text into a PREDEFINED structured dataset with EXACT fields:

{EXPECTED_FIELDS}

RULES:
- ALWAYS return ALL fields.
- If a field is missing in the text, keep "value": "".
- Extract values even when hidden inside long sentences.
- Comments MUST include at least one sentence from context.
- raw_context MUST be the exact paragraph text where info came from.
- NEVER invent new values.
- NEVER change wording.

OUTPUT FORMAT (STRICT JSON):
{{
  "First Name": {{"value": "...", "comments": "...", "raw_context": "..."}},
  "Last Name": {{"value": "...", "comments": "...", "raw_context": "..."}},
  ...
}}

Now extract from this text:
\"\"\"{full_text}\"\"\"
    """


# -------------------
# JSON CLEANING
# -------------------
def extract_clean_json(text: str):
    """
    Extract JSON from LLM output safely.
    Handles:
    - Markdown ```json blocks
    - Extra messages
    - Partial JSON extraction
    """
    text = text.replace("```json", "").replace("```", "")

    # Try direct parse
    try:
        return json.loads(text)
    except:
        pass

    # Try object-based JSON
    obj_match = re.search(r"\{.*\}", text, re.S)
    if obj_match:
        try:
            return json.loads(obj_match.group(0))
        except:
            pass

    # Try list JSON
    list_match = re.search(r"\[.*\]", text, re.S)
    if list_match:
        try:
            return json.loads(list_match.group(0))
        except:
            pass

    return None


# -------------------
# MAIN EXTRACTION
# -------------------
def extract_kv_pairs_from_text(full_text: str):
    prompt = build_prompt(full_text)
    response = model.generate_content(prompt).text

    parsed = extract_clean_json(response)

    if parsed is None:
        print("❌ Could not decode JSON. Model output was:")
        print(response[:2000])
        return []

    # Convert dict → list in fixed order
    items = []
    for key in EXPECTED_FIELDS:
        data = parsed.get(key, {})
        items.append({
            "key": key,
            "value": data.get("value", ""),
            "comments": data.get("comments", ""),
            "raw_context": data.get("raw_context", "")
        })

    return items
