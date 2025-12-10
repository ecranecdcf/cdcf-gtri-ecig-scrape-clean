### NOTE: THIS FILE IS STILL IN PROGRESS AND MAY BE MODIFIED FURTHER ###

import json
import logging
import re

import pandas as pd
import requests

# Set up basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

MODEL = "llama3.1:8b"                    
API_URL = "http://localhost:11434/api/generate"

def extract_json_from_text(text: str) -> str:
    """Extract JSON array or object from text that might contain reasoning or other content."""
    # First try to find a JSON array (greedy to get the whole array)
    array_match = re.search(r'\[.*\]', text, re.DOTALL)
    if array_match:
        return array_match.group(0)
    
    # If no array found, try to find a JSON object and convert it to array
    object_match = re.search(r'\{.*\}', text, re.DOTALL)
    if object_match:
        # Return the object wrapped in an array
        return f"[{object_match.group(0)}]"
    
    return "[]"

def create_prompt(product_name: str, description: str = "", flavor_text: str = "") -> str:
    # Simpler, more direct prompt
    prompt = f"""Extract all flavor names from this vape product information.

Product Name: {product_name}
Description: {description}
Flavor Text: {flavor_text}

Return a JSON array where each element is an object with "flavor" (the flavor name) and "description" (taste description or null).

Rules:
- Return format: [{{ "flavor": "name", "description": "desc or null" }}, ...]
- Extract ONLY flavors that actually appear in the text
- DO NOT extract: brand names (Elf Bar, Geek Bar, FLUM, etc.), model numbers (BC5000, Pulse, etc.), or generic words (vape, disposable, puff)
- If multiple flavors listed, return array with all of them
- If no flavors found, return []

Examples:
Input: "Elf Bar BC5000 Blue Razz Ice"
Output: [{{"flavor": "Blue Razz Ice", "description": null}}]

Input: "Available in: Strawberry, Watermelon, Grape"
Output: [{{"flavor": "Strawberry", "description": null}}, {{"flavor": "Watermelon", "description": null}}, {{"flavor": "Grape", "description": null}}]

Input: "Vaporesso XROS 3 Kit"
Output: []

Return ONLY the JSON array, nothing else:"""
    return prompt


def extract_flavors(product_name, description, flavor_text):
    prompt = create_prompt(product_name, description, flavor_text)
    
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(API_URL, json=data, timeout=60)
        response.raise_for_status()
        
        response_json = response.json()
        raw_response_text = response_json.get("response", "[]")
        
        # Check if empty
        if not raw_response_text or not raw_response_text.strip():
            return []
        
        # Clean markdown fences if present
        if raw_response_text.startswith("```json"):
            raw_response_text = raw_response_text[7:]
        if raw_response_text.endswith("```"):
            raw_response_text = raw_response_text[:-3]
        
        raw_response_text = raw_response_text.strip()
        
        # Try to parse directly first
        try:
            parsed = json.loads(raw_response_text)
            
            # If it's a dict, wrap it in a list (SILENT - this is expected fallback)
            if isinstance(parsed, dict):
                return [parsed]
            # If it's already a list, return it
            elif isinstance(parsed, list):
                return parsed
            else:
                return []
                
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON from text
            raw_response_text = extract_json_from_text(raw_response_text)
            
            try:
                parsed = json.loads(raw_response_text)
                if isinstance(parsed, dict):
                    return [parsed]
                elif isinstance(parsed, list):
                    return parsed
                else:
                    return []
            except json.JSONDecodeError as e:
                print(f"ERROR: Failed to decode extracted JSON for '{product_name}'. Error: {e}")
                return []
            
    except requests.exceptions.RequestException as e:
        print(f"ERROR: API request failed for '{product_name}': {e}")
        return []
        
    except Exception as e:
        print(f"An unexpected error occurred for '{product_name}': {e}")
        return []