import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import os
import re
from tqdm import tqdm

# Initialize the LLaMA model using pretrained parameters from the transformers library of HuggingFace
def init_llama_model(model_dir):
    # Directory error checking
    if not os.path.exists(model_dir):
        raise FileNotFoundError(f"The model directory at {model_dir} does not exist.")
        
    try:
        # Load the model and tokenizer from the specified directory
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        model = AutoModelForCausalLM.from_pretrained(model_dir, torch_dtype=torch.bfloat16)
        
        # Avoid warning msg about pad token id
        tokenizer.pad_token_id = tokenizer.eos_token_id
        model.config.pad_token_id = model.config.eos_token_id
        model.generation_config.temperature=None
        model.generation_config.top_p=None
        
        # Create the pipeline for text generation
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=0,  # Assuming a GPU environment -- change if needed
            do_sample=False # For deterministic generation
        )
        
        print("Custom LLM initialized successfully.")
        return pipe
    except Exception as e:
        print("Error initializing LLM:", e)
        return None

# Load scraped data from csv
def load_csv_data(file_path):
    # Directory error checking
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    # Load CSV data
    data = pd.read_csv(file_path, usecols=lambda column: 'Unnamed' not in column)
    return data

# Preprocessing steps
### JPJ: We may not need this if preprocessing is performed prior to data ingestion
def preprocess_data(data):
    # Replace NaN for object columns
    data.loc[:, data.select_dtypes(include=["object"]).columns] = data.select_dtypes(include=["object"]).fillna("")
    # Replace NaN for numeric columns with 0 or another default
    data.loc[:, data.select_dtypes(include=["float64"]).columns] = data.select_dtypes(include=["float64"]).fillna(0)
    return data    

# Classify scraped data for the TFN variable
def classify_tfn(pipe, text):
    try:
        # Prompt contains few shot learning to prime LLM with edge cases it may struggle with
        prompt = f"""
            [INST] <<SYS>>
            You are an analyst that determines if a product is tobacco-free or synthetic nicotine. You will receive a product description. If it is a CBD/THC product, return N/A. If it is tobacco-free or uses synthetic nicotine, output true with the phrase or word that indicates this. If it is not, return False. 
            <</SYS>> [/INST]
            
            [INST]
            Synthetic Nicotine
            [/INST]
            True - trigger term: "Synthetic Nicotine"
            
            [INST]
            synthetic nicotine
            [/INST]
            True - trigger term: "synthetic nicotine"
            
            [INST]
            TF, abbreviated for Tobacco Free.
            [/INST]
            True - trigger term: "TF"
            
            [INST]
            TFN, abbreviated for Tobacco Free Nicotine.
            [/INST]
            True - trigger term: "TFN"
            
            [INST]
            0% (0mg) of nicotine.
            [/INST]
            False - no trigger terms
            
            [INST]
            {text}
            [/INST]
            """
        # Set 256 max tokens due to length of some of the scraped product descriptions
        outputs = pipe(prompt, max_new_tokens=128, do_sample=False)
        response = outputs[0]["generated_text"].strip()
        return response

    except Exception as e:
        return f"Error during classification: {e}"
    
def classify_cbd(pipe, text):
    try:
        prompt = f"""
            [INST] <<SYS>> 
            You analyze text to determine if the product contains CBD/THC. You will receive text of a product's description. If it contains CBD/THC without nicotine, return True. If it does not contain CBD/THC, return False. If it contains both CBD/THC and nicotine, return "REVIEW".
            <</SYS>> [/INST]
            
            [INST]
            CBD
            [/INST]
            True - trigger terms: "CBD"
            
            [INST]
            {text}
            [/INST]
        """

        outputs = pipe(prompt, max_new_tokens=32, do_sample=False)
        response = outputs[0]["generated_text"].strip()
        return response

    except Exception as e:
        return f"Error during classification: {e}"
    
def classify_flavor(pipe, text):
    # Flavors can be very long--
    max_tokens = len(text.split()) * 2

    try:
        prompt = f"""
            [INST] <<SYS>> 
            You are an expert in parsing vape product descriptions. Extract flavors, their descriptions, and whether they include menthol or cooling indicators in a structured JSON format.
            <</SYS>> [/INST]
            Extract flavors from the following text and format the output as a JSON array with "flavor", "description", and "ice" (true/false based on cooling indicators). 
            
            [INST]
            "{text}"
            [/INST]
        """

        outputs = pipe(prompt, max_new_tokens=max_tokens, do_sample=False)
        response = outputs[0]["generated_text"].strip()
        return response

    except Exception as e:
        return f"Error during classification: {e}"
    
def classify_product(pipe, text):
    # Closed cartridges should mention pods while disposables will not mention pods at all
    # 
    try:
        prompt = f"""
            [INST] <<SYS>> 
            Classify the product using the description into one of the following categories:
            
            - **CLOSED REFILL**: Prefilled cartridges or pods that are not refillable after use with volume less than 5 mL.
            - **CLOSED SYSTEM**: A vape device or starter kit that uses replaceable, prefilled pods or cartridges.
            - **OPEN SYSTEM**: A refillable vape product or starter kit with a tank or cartridge that allows users to manually add their choice of e-liquid. Description may include an e-liquid capacity, battery capacity, and a refillable pod or tank.
            - **E-LIQUID**: Bottles of liquid used to refill tanks or pods with volume greater than 10 mL.
            - **DISPOSABLE**: Single-use vaping device that is disposable and non-reusable after e-liquid is depleted. These are advertised with an associated puff count or puffs per device.
            - **ACCESSORY**: Components like chargers, mesh coils, batteries, and REPLACEMENT pods or tanks (may have a coil or sub-ohm capacity). 

            Return the product classification.
            <</SYS>> [/INST]

            [INST]
            Replacement pod, replacement tank, empty pod, or empty tank
            [/INST]
            ACCESSORY

            [INST]
            Disposable vape, single-use vape, puff count, puffs per device
            [/INST]
            DISPOSABLE

            [INST]
            Refillable vape kit, starter kit with refillable pods or tank  
            [/INST]
            OPEN SYSTEM

            [INST]
            {text}
            [/INST]
             
        """
        outputs = pipe(prompt, max_new_tokens=64, do_sample=False)
        response = outputs[0]["generated_text"].strip()
        return response

    except Exception as e:
        return f"Error during classification: {e}"

def classify_dataset(pipe, data, flag=False):
    # Initialize 'classified' as a DataFrame with the 'all_text' column from 'data'
    classified = pd.DataFrame(data['all_text'])
    
    raw_llm = '_raw_llm'

    # Determine the classification function and column name based on flag
    if flag == 'tfn':
        classified[flag + raw_llm] = [
            classify_tfn(pipe, x) for x in tqdm(data['all_text'], desc=f"Classifying {flag.upper()}")
        ]
    elif flag == 'cbd':
        classified[flag + raw_llm] = [
            classify_cbd(pipe, x) for x in tqdm(data['all_text'], desc=f"Classifying {flag.upper()}")
        ]
    elif flag == 'product_type':
        classified[flag + raw_llm] = [
            classify_product(pipe, f"{row['title']}\n{row['description']}")
            for _, row in tqdm(data.iterrows(), desc="Classifying Product Type", total=len(data))
        ]
    elif flag == 'flavor':
        classified[flag + raw_llm] = [
            classify_flavor(pipe, row['all_text']) if not row['flavor_extracted'] else None
            for _, row in tqdm(data.iterrows(), desc="Classifying Flavor", total=len(data))
        ]
    else:
        raise ValueError("Invalid flag specified. Use 'tfn', 'cbd', 'product_type', or 'flavor'.")
    
    return classified

def save_classified_data(data, output_path):
    data.to_csv(output_path, index=False)
    print(f"Classified data saved to {output_path}.")

### Extracting LLM response
def extract_llm(row, llm_flag):
    first_line = row['all_text'].splitlines()[0]  
    text = row[llm_flag + "_raw_llm"]

    if first_line not in text:
        return None 
    
    if llm_flag in {'tfn', 'cbd', 'product_type'}:
        pattern = re.compile(rf'{re.escape(first_line)}.*?\[/INST\]\s*(.*?)(?:\n|$)', re.DOTALL)
    else:
        return None  # Return None for unsupported flags

    match = pattern.search(text)
    if not match:
        return None  # Return None if no match is found

    # Process the match based on llm_flag
    if llm_flag in {'tfn', 'cbd', 'product_type'}:
        return match.group(1).strip()
    return None

# Usage Example
if __name__ == "__main__":
    model_dir = "/home/jjun44/CDCF_vape/Llama-3.1-8B-Instruct"
    file_path = '/home/jjun44/CDCF_vape/datasets/input/input_file.csv'
    output_path = '/home/jjun44/CDCF_vape/datasets/output/output_file.csv'
    flags = ['tfn', 'cbd']
    pipe = init_llama_model(model_dir)
    if pipe is not None:
        try:
            data = load_csv_data(file_path)
            data = preprocess_data(data)
            data = classify_dataset(pipe, data, flags)
            save_classified_data(data, output_path)
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print("An error occurred:", e)
