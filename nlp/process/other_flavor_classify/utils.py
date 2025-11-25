import json
import logging

import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

### These categories were refined from manual review and inspired from survey questions.
### Subcategories refined from manual review & survey alignment
MODEL = "llama3.1:8b"
API_URL = "http://localhost:11434/api/generate"

OTHER_FLAVOR_SUBCATEGORIES = {
    "Spice": "Spice-forward flavors such as cinnamon, clove, vanilla, nutmeg, anise, chai.",
    "Fruit": "Fruit or fruity blends such as mango, berry mixes, citrus, tropical fruit, apple, grape.",
    "Chocolate": "Chocolate or cocoa-based flavors (e.g., chocolate, cocoa, brownie, fudge).",
    "Alcoholic Drinks": "Modeled after alcoholic beverages (e.g., wine, whiskey, rum, cocktail, margarita, pina colada).",
    "Non-alcoholic Drinks": "Modeled after non-alcoholic drinks (e.g., soda, lemonade, coffee, tea, energy drinks, milkshakes, smoothies).",
    "Sweets": "Candy, dessert, bakery, and sweet treat flavors (e.g., custard, cake, donut, ice cream, gummy, pastry, cookie).",
    "Concept": "Unclear, abstract, brand-based, or non-literal flavor names that do not match food/drink/spice categories.",
}   

def create_prompt(flavor_name: str, flavor_description: str = "") -> str:
    cats = "\n".join([f"- **{cat}**: {desc}" for cat, desc in OTHER_FLAVOR_SUBCATEGORIES.items()])
    prompt = f"""
You are an expert at categorizing e-cigarette flavors into standardized subcategories.

A single flavor may belong to MULTIPLE subcategories, or just one.

### Allowed Subcategories
{cats}

### Important Rules
- Only use subcategory names from the list above.
- Assign ALL subcategories that reasonably apply (multi-label allowed).
- If the flavor clearly does not match a specific subcategory and is mainly abstract or branded, use "Concept".
- If NO flavor profile can be inferred from name **or** description, use "Concept".
- If the flavor name or description strongly indicates a category, prioritize that category.
- Provide a confidence level: "high" or "low".
    - Use "high" if the flavor name or description clearly matches one or more specific subcategories (e.g., contains explicit flavor words such as “mango”, “cinnamon”, “chocolate”, “lemonade”, “cake”).
    - Use "low" if the classification relies on indirect associations, vague branding, or otherwise ambiguous text.

### Examples
Flavor: "Mango Ice"
Output:
{{
  "other_flavor_category": ["Fruit"],
  "confidence": "high",
  "rationale": "Contains 'mango', which is a fruit."
}}

Flavor: "Cinnamon Fireball"
Output:
{{
  "other_flavor_category": ["Spice", "Alcoholic Drinks"],
  "confidence": "high",
  "rationale": "Contains cinnamon (spice) and Fireball references cinnamon whiskey."
}}

Flavor: "Birthday Cake"
Output:
{{
  "other_flavor_category": ["Sweets"],
  "confidence": "high",
  "rationale": "Birthday cake is a dessert flavor."
}}

Flavor: "Galaxy Blast"
Output:
{{
  "other_flavor_category": ["Concept"],
  "confidence": "low",
  "rationale": "Abstract/branded name with no clear flavor type."
}}

### Task
Classify the following flavor into one or more subcategories.

- Flavor Name: "{flavor_name}"
- Description (optional): "{flavor_description}"

Return ONLY a single valid JSON object with the structure:

{{
  "other_flavor_category": ["one or more of: Spice, Fruit, Chocolate, Alcoholic Drinks, Non-alcoholic Drinks, Sweets, Concept, Unknown"],
  "confidence": "low" | "high",
  "rationale": "brief explanation of the words or associations that led to this classification"
}}

No markdown, no backticks, no additional text.

JSON output:
"""
    return prompt



def classify_other_flavor(flavor_name: str, flavor_description: str = "") -> dict:
    prompt = create_prompt(flavor_name, flavor_description)

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",  # ask Ollama to enforce JSON
        "options": {
            "temperature": 0.1,
            "top_p": 0.9,
            "num_predict": 256,  # Ollama-style max tokens
        },
    }

    try:
        resp = requests.post(API_URL, json=payload, timeout=90)
        resp.raise_for_status()
        data = resp.json()
        raw = data.get("response", "")

        # In rare cases, Ollama might already return a dict
        if isinstance(raw, dict):
            parsed = raw
        else:
            result_str = str(raw).strip()
            # Clean markdown fences if they sneak in
            if result_str.startswith("```json"):
                result_str = result_str[7:]
            if result_str.endswith("```"):
                result_str = result_str[:-3]
            try:
                parsed = json.loads(result_str)
            except json.JSONDecodeError:
                logging.warning(f"JSON decode failed for flavor '{flavor_name}'. Raw: {result_str!r}")
                return {
                    "categories": ["Other"],
                    "confidence": "low",
                    "rationale": "Model response was not valid JSON; defaulted to 'Other'.",
                }

        categories = parsed.get("categories", ["Other"])
        if isinstance(categories, str):
            categories = [categories]

        # Filter to allowed subcategories, default to ["Other"] if nothing valid
        categories = [c for c in categories if c in OTHER_FLAVOR_SUBCATEGORIES] or ["Other"]

        confidence = parsed.get("confidence", "low")
        rationale = parsed.get("rationale", "")

        return {
            "categories": categories,
            "confidence": confidence,
            "rationale": rationale,
        }

    except Exception as e:
        logging.error(f"Error classifying flavor '{flavor_name}': {e}")
        return {
            "categories": ["Other"],
            "confidence": "low",
            "rationale": f"ERROR during classification: {e}",
        }