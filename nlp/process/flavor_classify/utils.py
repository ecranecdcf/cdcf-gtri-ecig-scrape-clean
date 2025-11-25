import json
import logging

import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

MODEL = "llama3.1:8b"
API_URL = "http://localhost:11434/api/generate"

def create_flavor_category_prompt(flavor_name: str, flavor_description: str = "") -> str:
    prompt = f"""
You are an expert e-cigarette flavor classifier. Assign exactly ONE flavor category to each product using the rules below.

### PRIORITY RULE
If a flavor description is provided, weight it more heavily than the flavor name.  
- Example: Flavor name “Sunny Day” with description “blueberry and mint blend” should be classified as Other Flavors, not Unknown.

### FLAVOR CATEGORIES (Choose ONE)
1. **Tobacco**  
   - Tobacco-only flavors. May include sweet, caramel-like, or robust earthy tobacco notes. Examples: "Smooth Tobacco", "Cuban Cigar", "Red", "Regular", "American", "American Patriots".
2. **Mint**  
   - Mint-only flavors. Examples: "Spearmint", "Mint", "Cool Mint", "Mighty Mint".
3. **Menthol**  
   - Menthol-only flavors with a primary icy/menthol taste or experience. Examples: "Menthol", "Blue Menthol", "Cool Ice", "Goodport", "Arctic Ice".
4. **Unflavoured**  
   - Truly no flavor AND no cooling terms (names like "Unflavored", "Naked", "No Flavor") with no mention of ice/cool/menthol/chill or other flavor notes in profile. Examples: "Unflavored" with no cooling/menthol/coolant terms anywhere.
5. **Clear/Other Cooling**  
   Marketed as unflavored but has cooling sensations (clear, clear ice, naked ice) OR description mentions cool/chill/cold/ice/chill/menthol. Examples: "Clear", "Clear Ice", "Naked Ice" when paired with cooling / icy / menthol descriptors.
6. **Wellness/Health**  
   Vitamin vapes or health vapes, where the "flavor" is a functional ingredient (B12, melatonin, sleep blend, vitamin). Examples: "B12", "Vitamin B12", "Melatonin", "Sleep Blend", "Energy B12".
7. **Other Flavors**  
   Any identifiable flavor profile not covered above: fruit, dessert, candy, beverages, spices, mixed flavors, “X Ice” when the base is a flavor (e.g., Mango Ice, Blue Razz Ice).Examples: "Clove", "Raspberry", "Blueberry Freeze", "Bubblegum", "Cake", "Ice Cream", "Grape Energy", "Mango Ice", "Strawberry Banana".
8. **Unknown**  
   Only use if BOTH the flavor name provides no interpretable flavor clues AND no description is available. Examples: “Jazz”, “Midnight”, “Eclipse” with no description.

### DECISION RULES
- If description clearly identifies fruit/mint/menthol/tobacco/etc., use that category even if the name is abstract.  
- If a name appears unflavored but description mentions cooling, label as Clear/Other Cooling.  
- If a flavor contains cooling but its main taste is a fruit/dessert, label as Other Flavors.  
- If health/wellness ingredient is the main focus, label as Wellness/Health.  
- If still unclear after using both name and description, label as Unknown.

### OUTPUT FORMAT
Return ONLY a single valid JSON object with the following fields:
{{
  "flavor_category": "Tobacco" | "Mint" | "Menthol" | "Unflavoured" | "Clear/Other Cooling" | "Wellness/Health" |  "Other Flavors" | "Unknown",
  "confidence": "high" | "low",
  "rationale": "short explanation referencing the key words or phrases you used"
}}

### TASK
Classify this product:
- Flavor Name: "{flavor_name}"
- Flavor Description: "{flavor_description}"

JSON output:
"""
    return prompt

def classify_flavor_category(flavor_name: str, flavor_description: str = "") -> dict:
    prompt = create_flavor_category_prompt(flavor_name, flavor_description)

    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
    }

    try:
        response = requests.post(API_URL, json=data, timeout=60)
        response.raise_for_status()
        response_json = response.json()
        raw = response_json.get("response", "{}")

        if isinstance(raw, dict):
            return raw

        result_str = str(raw).strip()
        if result_str.startswith("```json"):
            result_str = result_str[7:]
        if result_str.endswith("```"):
            result_str = result_str[:-3]

        parsed = json.loads(result_str)

        if isinstance(parsed, dict):
            return parsed

        logging.warning("Model returned non-dict JSON; falling back to Unknown.")
        return {
            "flavor_category": "Unknown",
            "confidence": "low",
            "rationale": "Model output was not a JSON object."
        }

    except Exception as e:
        logging.error(f"Error classifying flavor for '{product_name}': {e}")
        return {
            "flavor_category": "Unknown",
            "confidence": "low",
            "rationale": f"Error during classification: {e}"
        }
