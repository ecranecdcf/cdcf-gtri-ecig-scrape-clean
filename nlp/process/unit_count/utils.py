import json, requests, pandas as pd
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MODEL = "llama3.1:8b"  
API_URL = "http://localhost:11434/api/generate"

# Create prompt for unit count extraction
def create_prompt(product_name, description="", package_contents=""):    
    prompt = f"""
You are an expert at counting vape products and e-liquid containers in product packages.

### CRITICAL RULE
Count ONLY these items:
1. **Vape devices**: Disposable vapes, rechargeable devices, pod systems, vape pens, mods
2. **E-liquid containers**: Bottles of e-liquid, e-juice containers, vape juice

### DO NOT COUNT
- Batteries, chargers, cables, USB cords
- Replacement coils, atomizers, nozzles, tips
- Empty pods or cartridges (unless they are pre-filled)
- Accessories like cases, lanyards, cleaning tools
- Spare parts or components

### EXAMPLES

Example 1:
Product Name: "Elf Bar BC5000 10-Pack"
Description: "Box of 10 disposable vapes"
→ unit_count: 10
→ rationale: "10-Pack explicitly indicates 10 disposable vape devices"

Example 2:
Product Name: "JUUL Device Starter Kit"
Description: "Includes 1 JUUL device, USB charger, and 4 flavor pods"
Package Contents: "1 x JUUL Device, 1 x USB Charger, 4 x Flavor Pods"
→ unit_count: 1
→ rationale: "Only counting the 1 vape device (JUUL), not the charger or accessories"

Example 3:
Product Name: "Premium E-Liquid 3-Pack Bundle"
Description: "Three 60mL bottles of premium vape juice"
→ unit_count: 3
→ rationale: "3 bottles of e-liquid"

Example 4:
Product Name: "Vaporesso XROS 3 Kit"
Description: "Rechargeable pod system with 2 refillable pods and USB-C cable"
Package Contents: "1 x XROS 3 Device, 2 x Refillable Pods, 1 x USB-C Cable"
→ unit_count: 1
→ rationale: "Only 1 vape device, ignoring empty pods and cable"

Example 5:
Product Name: "Geek Bar Pulse Disposable Vape"
Description: "Single use disposable vaping device, 15000 puffs"
→ unit_count: 1
→ rationale: "Single disposable vape"

Example 6:
Product Name: "Lost Mary OS5000 5-Count"
Description: "5 disposable vapes in assorted flavors"
→ unit_count: 5
→ rationale: "5-Count indicates 5 disposable devices"

Example 7:
Product Name: "Replacement Coil Pack (5-Pack)"
Description: "Pack of 5 replacement coils for sub-ohm tanks"
→ unit_count: 1
→ rationale: "Coils are accessories, not vape devices or e-liquid, defaulting to 1"

Example 8:
Product Name: "Naked 100 E-Liquid"
Description: "Single 100mL bottle of nicotine salt e-juice"
→ unit_count: 1
→ rationale: "1 bottle of e-liquid"

### CLASSIFICATION RULES
1. Look for explicit pack quantities: "10-pack", "5 pack", "box of 12", "3-count"
2. Check package contents for device/liquid counts: "5 x Disposable", "3 x Bottles"
3. **Ignore** accessories, chargers, cables, coils, empty pods in the count
4. If the product is ONLY accessories (no vape device or e-liquid), return unit_count: 1
5. If no quantity specified for a vape/e-liquid product, assume unit_count = 1
6. confidence = "high" if quantity is explicitly stated
7. confidence = "low" if inferred or assumed

### REQUIRED OUTPUT FORMAT
Return ONLY valid JSON:

{{
  "unit_count": <integer>,
  "confidence": "high" | "low",
  "rationale": "short explanation of how you counted only vape devices or e-liquid containers"
}}

### PRODUCT INFORMATION
Product Name: "{product_name}"
Description: "{description}"
Package Contents: "{package_contents}"

JSON Output:
"""
    return prompt

# Function to extract unit count using LLM
def classify_unit_count(product_name, description="", package_contents=""):
    prompt = create_prompt(product_name, description, package_contents)
    
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"  # Request JSON format directly
    }
    
    try:
        response = requests.post(API_URL, json=data, timeout=60)
        response.raise_for_status()
        
        response_json = response.json()
        result_str = response_json.get('response', '{}')
        
        # Clean up potential markdown code fences
        if result_str.startswith("```json"):
            result_str = result_str[7:]
        if result_str.endswith("```"):
            result_str = result_str[:-3]
        
        result_data = json.loads(result_str.strip())
        
        # Validate unit_count is an integer
        unit_count = result_data.get("unit_count", 1)
        try:
            unit_count = int(unit_count)
            # Ensure positive (at least 1)
            if unit_count < 1:
                unit_count = 1
        except (ValueError, TypeError):
            logging.warning(f"Invalid unit_count '{unit_count}' for '{product_name}', defaulting to 1")
            unit_count = 1
        
        return {
            "unit_count": unit_count,
            "confidence": result_data.get("confidence", "low"),
            "rationale": result_data.get("rationale", "No rationale provided by model.")
        }

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed for '{product_name}': {e}")
        return {"unit_count": 1, "confidence": "low", "rationale": str(e)}
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response for '{product_name}': {e}")
        logging.debug(f"Raw response: {result_str}")
        return {"unit_count": 1, "confidence": "low", "rationale": "Failed to parse model's JSON output."}
    except Exception as e:
        logging.error(f"An unexpected error occurred for '{product_name}': {e}")
        return {"unit_count": 1, "confidence": "low", "rationale": str(e)}