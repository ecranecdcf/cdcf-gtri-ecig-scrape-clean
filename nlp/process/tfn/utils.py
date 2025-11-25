import json, requests, pandas as pd
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MODEL = "llama3.1:8b"  
API_URL = "http://localhost:11434/api/generate"

# Create prompt for CBD/THC classification
def create_prompt(product_name, description=""):    
    prompt = f"""
You are an expert in nicotine and TFN (tobacco-free nicotine) classification. 
Your job is to determine whether a product contains **synthetic nicotine or tobacco-free nicotine**.

### CLASSIFICATION RULES (IMPORTANT)
1. tfn_category = 1 if the product contains **synthetic nicotine** or **tobacco-free nicotine**. 
2. tfn_category = 0 if the product does NOT contain **synthetic nicotine** or **tobacco-free nicotine**.

### EXAMPLE SIGNALS
TFN:
- "TFN", "tobacco-free nicotine", "synthetic nicotine", "non-tobacco nicotine"
Metatine:
- "Metatine", "metatin"

### REQUIRED OUTPUT FORMAT
Return ONLY a valid JSON:

{{
  "tfn_category": 1 | 0,
  "confidence": "high" | "low",
  "rationale": "short explanation referencing key words"
}}

### PRODUCT INFO
Product Name: "{product_name}"
Description: "{description}"

JSON Output:
"""
    return prompt

# Function to classify CBD/THC category using LLM
def classify_tfn_category(product_name, description=""):
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
            "tfn_category": result_data.get("tfn_category", "Error"),
            "confidence": result_data.get("confidence", "low"),
            "rationale": result_data.get("rationale", "No rationale provided by model.")
        }

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed for '{product_name}': {e}")
        return {"tfn_category": "Error", "confidence": "low", "rationale": str(e)}
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response for '{product_name}': {e}")
        logging.debug(f"Raw response: {result_str}")
        return {"tfn_category": "Error", "confidence": "low", "rationale": "Failed to parse model's JSON output."}
    except Exception as e:
        logging.error(f"An unexpected error occurred for '{product_name}': {e}")
        return {"tfn_category": "Error", "confidence": "low", "rationale": str(e)}