### NOTE: THIS FILE IS STILL IN PROGRESS AND MAY BE MODIFIED FURTHER ###

import json
import logging

import pandas as pd
import requests

# Set up basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

MODEL = "gpt-oss:20b"                     # Your specified model
API_URL = "http://localhost:11434/api/generate"  # Your local Ollama API endpoint


def create_prompt(product_name: str, description: str = "", flavor_text: str = "") -> str:
    """Build the flavor-extraction prompt."""
#     prompt = f"""
# You are a Data Extraction Specialist for the vaping industry. Your task is to extract a structured list of flavors from unstructured vape product text.

# ### GOAL
# Return a JSON array of objects. Each object must have:
# - "flavor": the full flavor name, exactly as it would appear on packaging
# - "description": a short descriptive phrase about that flavor, or null if none is given

# ### WHAT COUNTS AS A FLAVOR ("flavor" field)
# Extract the **complete flavor name**, not split into pieces. A flavor may be:
# - Standard flavors: "Blue Raspberry", "Watermelon", "Mint", "Menthol"
# - Compound flavors: "Strawberry Banana Ice", "Red Apple Ice", "Blue Razz Lemonade"
# - Creative/marketing names: "Killer Kustard", "Unicorn Milk", ”Milano Adore"
# - Dessert/drink flavors: "Vanilla Custard", "Peach Lemonade", "Caramel Macchiato"
# - Color and flavor combos: "Pink Lemonade", "Red Apple"
# - Ice/menthol variants: "Blue Razz Ice", "Cool Mint", "Icy Grape", "Cool Ice"
# - Tobacco-style flavors: "Smooth Tobacco", "Cuban Cigar", "Red", "Regular", "American", "American Patriots"
# - Unflavoured-style names that are still labeled options:
#   - "Unflavored", "Unflavoured", "Naked", "No Flavor"
# - Clear/other cooling names marketed as almost-unflavored:
#   - "Clear", "Clear Ice", "Naked" when paired with cooling/ice/menthol language
# - Wellness/health vapes where the active ingredient functions as the “flavor”:
#   - "B12", "Melatonin", "Vitamin B12"

# Do **not** split a multi-word flavor:
# - "Strawberry Banana Ice” labeled as "flavor": "Strawberry Banana Ice"

# ### DESCRIPTION RULES ("description" field)
# The "description" gives extra taste or profile information for a flavor.

# Use "description" when there is an additional descriptive phrase relevant to the flavor name. Examples of descriptions:
# - “Killer Kustard... Flavor \n custard flavor with hints of vanilla”
#  - flavor: “Killer Kustard”
#  - description: “Vanilla Custard”
# - “Royalty II: Custard, Nuts, Vanilla”
#  - flavor: “Royalty II”
#  - description: “Custard, Nuts, Vanilla”
# - “Clear Ice - unflavored with a light cooling sensation”
#  - flavor: “Clear Ice”
#  - description: “unflavored with a light cooling sensation”
# - “Blue Razz Ice... delivers a bold blue raspberry taste with a refreshing icy finish.”
#  - flavor: “Blue Razz Ice”
#  - description: “bold blue raspberry taste with a refreshing icy finish”

# ### WHAT TO IGNORE
# Do **NOT** extract as flavors:
# - Brand names: Elf Bar, Lost Mary, Juul, Vaporesso, Monster Bar, SMOK, etc.
# - Series/model names: BC5000, Max Air, GRIP, XROS 3, Thelema, etc.
# - Hardware terms: pod, kit, device, coil, battery, mod, tank
# - Pure nicotine information: 50mg, 5%, 0mg, "salt nic", "nicotine salt" (except when used only inside the description string)
# - Generic words: vape, disposable, e-liquid, juice, puff, cartridge
# - Colors with no flavor meaning by themselves: "Red", "Blue", "Black" (unless clearly part of a named flavor like "Red Apple")

# ### MULTIPLE FLAVOR RULE
# If the text clearly lists multiple distinct flavor options, return one object per flavor:

# - "Available in Banana, Grape, Killer Kustard"
#   [
#     {{ "flavor": "Banana", "description": null }},
#     {{ "flavor": "Grape", "description": null }},
#     {{ "flavor": "Killer Kustard", "description": null }}
#   ]
# - ”Flavors Black CherryBlow PopBlue Razz IceBlueberry WatermelonTropical Rainbow Blast”
#   [
#     {{ "flavor": ”Black Cherry", "description": null }},
#     {{ "flavor": ”Blow Pop", "description": null }},
#     {{ "flavor": ”Blue Razz Ice", "description": null }}
#     {{ "flavor": ”Blueberry Watermelon", "description": null }},
#     {{ "flavor": ”Tropical Rainbow Blast", "description": null }}
#   ]

# ### OUTPUT FORMAT
# Return ONLY a valid JSON array of objects. No markdown, no backticks, no extra commentary.

# Each element must be:
# {{
#   "flavor": "string",
#   "description": "string or null"
# }}

# If no flavors are found, return: []

# ### TASK
# Extract all full flavor names and their linked descriptions (if any) from the following text:
# - Product Name: "{product_name}"
# - Description: "{description}"
# - Flavor Text: "{flavor_text}"

# JSON output:
# """
#     return prompt
    prompt = f"""
You are a Data Extraction Specialist for the vaping industry. Extract a structured list of FLAVOR OPTIONS from the text.

## GOAL
Return a JSON array of objects. Each object must have:
- "flavor": the full flavor name, exactly as it would appear on packaging
- "description": a short taste/profile phrase about that flavor, or null if none is clearly given

If you cannot find any valid flavor names, you MUST return: [].

## WHAT COUNTS AS A FLAVOR ("flavor")
Extract the COMPLETE flavor name (do not split multi-word names). A flavor can be:
- Standard flavors: "Blue Raspberry", "Watermelon", "Mint"
- Compound flavors: "Strawberry Banana Ice", "Blue Razz Lemonade", "Red Apple Ice"
- Creative names: "Killer Kustard", "Unicorn Milk", "Milano Adore"
- Dessert/drink flavors: "Vanilla Custard", "Peach Lemonade", "Caramel Macchiato"
- Color+flavor: "Pink Lemonade", "Red Apple"
- Tobacco-style names: "Smooth Tobacco", "Cuban Cigar", "American Patriots"
- Unflavoured-style flavor options: "Unflavored", "Unflavoured", "Naked", "No Flavor", "Clear", "Clear Ice"
- Wellness/health: "B12", "Melatonin", "Vitamin B12"

You may ONLY output a flavor if its name (or very close variation) actually appears in the input text.
Never invent flavors or reuse example flavors that do not appear.

## DESCRIPTION ("description")
For each flavor you find, look in nearby text for a short phrase that describes how it tastes:
- Often after "-", ":" or phrases like "flavor", "tastes like", "blend of", "notes of".
- Example: "Royalty II: Custard, Nuts, Vanilla" ->
  {{ "flavor": "Royalty II", "description": "custard, nuts, vanilla" }}

If you cannot clearly find a taste description linked to that flavor, set:
- "description": null

## WHAT TO IGNORE
Do NOT extract these as flavors:
- Brand names: Elf Bar, Lost Mary, Juul, Vaporesso, SMOK, Wulf Mods, Empire Glassworks, etc.
- Series/model names: BC5000, Max Air, GRIP, XROS 3, Thelema, etc.
- Hardware-only products: kits, batteries, mods, coils, tanks, pods, torches, honey straws, devices
  (if the product is ONLY hardware/accessory with no flavor names, return []).
- Pure nicotine info: 50mg, 5%, 0mg, "salt nic", "nicotine salt"
- Generic words: vape, disposable, e-liquid, juice, puff, cartridge
- Colors with no flavor meaning by themselves: "Red", "Blue", "Black"

## MULTIPLE FLAVORS
If the text clearly lists multiple distinct flavor options, return one object per flavor:
- "Available in Banana, Grape, Killer Kustard" ->
  [
    {{ "flavor": "Banana", "description": null }},
    {{ "flavor": "Grape", "description": null }},
    {{ "flavor": "Killer Kustard", "description": null }}
  ]

## NEGATIVE EXAMPLE (IMPORTANT)
Input text describes only hardware/accessories, such as:
"Wulf Mods X Empire Glassworks Honey Straw Kit ... honey straw kit, torches, pen torch, stable and powerful torch pen..."
This product has NO flavor names.
Output MUST be:
[]

## OUTPUT FORMAT
Return ONLY a valid JSON array of objects. No markdown, no backticks, no extra text.

Each element must be:
{{
  "flavor": "string",
  "description": "string or null"
}}

If no flavors are found, return: [].

## TASK
Use ALL fields below as a single combined text source.

- Product Name: "{product_name}"
- Description: "{description}"
- Flavor Text: "{flavor_text}"

JSON output:
"""
    return prompt


def extract_flavors(product_name: str, description: str = "", flavor_text: str = ""):
    """
    Call Llama via Ollama to extract flavors.
    Returns a Python list of flavor objects (each with "flavor" and "description"),
    or [] on error.
    """
    prompt = create_prompt(product_name, description, flavor_text)

    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",  # ask Ollama to enforce JSON
    }

    try:
        response = requests.post(API_URL, json=data, timeout=60)
        response.raise_for_status()

        response_json = response.json()
        raw = response_json.get("response", "[]")

        # Case 1: Ollama already gave us a Python list/dict (rare, but be safe)
        if isinstance(raw, list):
            return raw
        if isinstance(raw, dict):
            # Single object – wrap in a list
            return [raw]

        # Case 2: raw is a string containing JSON
        result_str = str(raw).strip()

        # Clean up potential markdown fences just in case
        if result_str.startswith("```json"):
            result_str = result_str[7:]
        if result_str.endswith("```"):
            result_str = result_str[:-3]

        parsed = json.loads(result_str)

        # Accept both list and single-object JSON
        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict):
            return [parsed]

        logging.warning("Model returned JSON that is neither list nor dict; returning empty list.")
        logging.debug(f"Parsed JSON type: {type(parsed)}, value: {parsed!r}")
        return []

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed for '{product_name}': {e}")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response for '{product_name}': {e}")
        logging.debug(f"Raw response text: {raw!r}")
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred for '{product_name}': {e}")
        return []

