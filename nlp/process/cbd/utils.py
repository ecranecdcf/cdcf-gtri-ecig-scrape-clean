import json, requests, pandas as pd
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MODEL = "llama3.1:8b"  
API_URL = "http://localhost:11434/api/generate"

# Create prompt for CBD/THC classification
def create_prompt(product_name, description=""):    
    prompt = f"""
You are an expert in vape and cannabinoid product classification. Your task is to determine 
whether a product contains **CBD or THC** or is related to these substances.

### CLASSIFICATION RULES (IMPORTANT)
1. CBD_category = 1 if the product contains or is used with **CBD or THC**. 
2. CBD_category = 0 if the product does NOT contain or is NOT used with **CBD or THC**.

#### EXAMPLE SIGNALS

CBD:
- "CBD", "cannabidiol", "hemp extract", "isolate", "broad spectrum", "full spectrum"

THC:
- “THC”, “Delta 8”, “Delta-9”, “Delta 10”, “HHC”, “live resin”, “distillate”

### REQUIRED OUTPUT FORMAT
Return ONLY a valid JSON object:

{{
  "cbd_category": 1 | 0,
  "confidence": "high" | "low",
  "rationale": "short explanation referencing key words"
}}

### PRODUCT INFORMATION
Product Name: "{product_name}"
Description: "{description}"

JSON Output:
"""
    return prompt

# Function to classify CBD/THC category using LLM
def classify_cbd_category(product_name, description=""):
    prompt = create_prompt(product_name, description)
    
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
            "cbd_category": result_data.get("cbd_category", "Error"),
            "confidence": result_data.get("confidence", "low"),
            "rationale": result_data.get("rationale", "No rationale provided by model.")
        }

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed for '{product_name}': {e}")
        return {"cbd_category": "Error", "confidence": "low", "rationale": str(e)}
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response for '{product_name}': {e}")
        logging.debug(f"Raw response: {result_str}")
        return {"cbd_category": "Error", "confidence": "low", "rationale": "Failed to parse model's JSON output."}
    except Exception as e:
        logging.error(f"An unexpected error occurred for '{product_name}': {e}")
        return {"cbd_category": "Error", "confidence": "low", "rationale": str(e)}