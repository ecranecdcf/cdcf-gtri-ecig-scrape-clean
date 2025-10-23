import json, requests, pandas as pd

### These categories were refined from manual review and inspired from survey questions.
SUBCATEGORIES = {
    "Spice": "Spices (e.g., cinnamon, clove, vanilla, nutmeg, anise)",
    "Fruit": "Fruit or fruity flavors (e.g., strawberry, mango, blueberry, citrus blends)",
    "Chocolate": "Chocolate or cocoa-based flavors",
    "Alcoholic Drinks": "Alcoholic drinks (e.g., wine, whiskey, margarita, rum, cocktails, pina colada)",
    "Non-alcoholic Drinks": "Non-alcoholic drinks (e.g., lemonade, coffee, soda, energy drinks, tea, milkshakes, smoothie)",
    "Sweets": "Candy, desserts, or other sweet flavors (e.g., custard, cake, donut, gummy, pastry)",
    "Cooling": "Cooling agents (e.g., ice, chill, frost, cool, menthol when mixed with other flavors)",
    "Other": "Other (for unclear, brand-based, or unidentifiable flavor types)",
}

MODEL = "llama3.1:8b"
API_URL = "http://localhost:11434/api/generate"

def create_prompt(flavor_name, description=""):
    cats = "\n".join([f"- {cat}: {desc}" for cat, desc in SUBCATEGORIES.items()])
    prompt = f"""
        You are an expert at categorizing e-cigarette flavors. 
        Each flavor can belong to multiple subcategories from the list below:

        {cats}

        Return your answer in JSON format with the following keys:
        {{
          "categories": ["List of one or more subcategories"],
          "confidence": "low | medium | high",
          "rationale": "Explain briefly what words or associations led to this classification."
        }}

        Examples:
        Flavor: "Mango Ice"
        Output: {{"categories": ["Fruit", "Cooling"], "confidence": "high", "rationale": "Contains 'mango', which is a fruit; 'ice' may refer to cooling."}}

        Flavor: "Cinnamon Fireball"
        Output: {{"categories": ["Spice", "Alcoholic Drinks"], "confidence": "medium", "rationale": "'Cinnamon' is a spice and 'Fireball' references a whiskey brand."}}

        Flavor Name: "{flavor_name}"
        Description: "{description}"

        Output:
    """
    return prompt


def classify_other_flavor(flavor_name, description=""):
    global SUBCATEGORIES, MODEL, API_URL

    prompt = create_prompt(flavor_name, description)
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1, 
            "top_p": 0.9, 
            "max_tokens": 150
        },
    }
    try:
        r = requests.post(API_URL, json=payload, timeout=90)
        r.raise_for_status()
        raw_text = r.json().get("response", "").strip()
        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError:
            parsed = {"categories": ["Other"], "confidence": "low", "rationale": raw_text}
        
        categories = parsed.get("categories", ["Other"])
        categories = [c for c in categories if c in SUBCATEGORIES.keys()] or ["Other"]

        confidence = parsed.get("confidence", "low")
        rationale = parsed.get("rationale", "")

        return {"categories": categories, "confidence": confidence, "rationale": rationale}
    
    except Exception as e:
        return {"categories": ["Other"], "confidence": "low", "rationale": f"ERROR: {e}"}


def sample_other_flavors(input_csv: str, output_csv: str, n: int = 300, seed: int = 42):
    df = pd.read_csv(input_csv)
    other = df[df["predicted_category"].str.lower() == "other flavors"].copy()
    sample = other.sample(n=n, random_state=seed)
    sample.to_csv(output_csv, index=False)
    print(f"Saved a sample of ({n} flavors) to {output_csv}")