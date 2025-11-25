import json, requests, pandas as pd
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

### These categories are taken directly from your 'E-Cigarette Coding Convention' document. 
PRODUCT_CATEGORIES = {
    "Closed Refills": "Prefilled cartridges, tanks, or pods used in rechargeable devices. These come with e-liquid inside and are NOT refillable. (e.g., JUUL pods, Logic Pro Tanks)",
    "Closed System": "Rechargeable devices/kits intended for use with prefilled cartridges. (e.g., JUUL system, VUSE Solo system)",
    "Disposable System": "Non-rechargeable and non-reusable devices, disposed of after e-liquid is depleted. (e.g., Puff Bar, Elfbar)",
    "E-Liquid": "Bottles or containers of liquid used used for refilling e-cigarette devices or pods. (e.g., Vape Craft 120ML bottles)",
    "Accessories": "Parts or components sold WITHOUT e-liquid, including batteries, chargers, coils, replacement/refillable pods/cartridges. (e.g., Ooze Slim Pen)",
    "Heated Tobacco Products": "Devices that heat tobacco rather than burn it, usually paired with a tobacco stick. (e.g., HEETS, IQOS)",
    "Open System": "Rechargeable devices/kits with a built-in refillable tank intended to be manually filled with e-liquid. Compatible with liquid bottles, not cartridges. (e.g., Vaporesso XROS 4)"
}

MODEL = "llama3.1:8b"  
API_URL = "http://localhost:11434/api/generate"

def create_prompt(product_name, site_category="", site_tag="", description="", package_contents=""):
    # Format the categories for the prompt
    cats = "\n".join([f"- **{cat}**: {desc}" for cat, desc in PRODUCT_CATEGORIES.items()])
    
    prompt = f"""
        You are an expert e-cigarette product classifier. Your sole task is to
        analyze the product information and return a single, valid JSON object
        with the product's category.

        ## Categories
        {cats}

        ## Instructions
        1.  Analyze the provided fields: Product Name, Site Category, Site Tags, Description, and Package Contents.
        2.  Select **exactly ONE** category from the list above that best fits the product. Do not return more than one category.
        3.  Provide a confidence level: "high" or "low".
            - Use "high" if keywords (e.g., "Disposable", "Battery", "Refillable", "E-Liquid Bottle", "Pods") are present.
            - Use "low" if the classification is an inference based on ambiguous text.
        4.  Provide a brief "rationale" explaining your choices, referencing the most useful fields.
        5.  **CRITICAL:** Your entire response MUST be a single, valid JSON object, and nothing else.
            Do not add any text before or after the JSON, such as "Here is the JSON:".

        ## Examples

        **Example 1:**
        Product Name: "Elfbar BC5000"
        Site Category: "disposables/elfbar"
        Site Tags: "elfbar-bc5000-disposable"
        Description: "A compact, single-use vape device, pre-filled with 13mL of e-liquid."
        Package Contents: "1 x Elfbar BC5000 Device"
        Output:
        ```json
        {{
          "categories": "Disposable System",
          "confidence": "high",
          "rationale": "The 'Description', 'Site Category', and 'Site Tags' all explicitly use the word 'disposable' or 'single-use'."
        }}
        ```

        **Example 2:**
        Product Name: "JUUL Device Kit"
        Site Category: "vape-kits"
        Site Tags: "juul-device-kit"
        Description: "Includes one rechargeable JUUL device and a USB charging dock. Pods sold separately."
        Package Contents: "1 x JUUL Device, 1 x USB Charger"
        Output:
        ```json
        {{
          "categories": "Closed System",
          "confidence": "high",
          "rationale": "The 'Description' specifies a 'rechargeable JUUL device' and notes 'Pods sold separately,' which defines a 'Closed System' without 'Closed Refills'."
        }}
        ```

        **Example 3:**
        Product Name: "Ooze Slim Pen Battery"
        Site Category: "battery-device"
        Site Tags: "ooze-slim-pen-battery-mod"
        Description: "510 thread battery for your favorite cartridges. Charger included."
        Package Contents: "1 x Ooze Slim Pen, 1 x USB Charger"
        Output:
        ```json
        {{
          "categories": "Accessories",
          "confidence": "high",
          "rationale": "The 'Product Name' ('Battery') and 'Site Category' ('battery-device') clearly indicate it's an accessory. The 'Description' confirms it's for cartridges, not with them."
        }}
        ```

        ## Task
        Classify the following product.

        - Product Name: "{product_name}"
        - Site Category: "{site_category}"
        - Site Tags: "{site_tag}"
        - Description: "{description}"
        - Package Contents: "{package_contents}"

        JSON Output (must be the only text you return):
        """
    return prompt

def classify_product_category(product_name, site_category="", site_tag="", description="", package_contents=""):
    prompt = create_prompt(product_name, site_category, site_tag, package_contents, description)
    
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
        
        return {
            "categories": result_data.get("categories", "Error"),
            "confidence": result_data.get("confidence", "low"),
            "rationale": result_data.get("rationale", "No rationale provided by model.")
        }

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed for '{product_name}': {e}")
        return {"categories": ["Error"], "confidence": "low", "rationale": str(e)}
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response for '{product_name}': {e}")
        logging.debug(f"Raw response: {result_str}")
        return {"categories": ["Error"], "confidence": "low", "rationale": "Failed to parse model's JSON output."}
    except Exception as e:
        logging.error(f"An unexpected error occurred for '{product_name}': {e}")
        return {"categories": ["Error"], "confidence": "low", "rationale": str(e)}
