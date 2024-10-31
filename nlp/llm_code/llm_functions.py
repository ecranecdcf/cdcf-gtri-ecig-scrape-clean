import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import os
import re

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
        model.config.pad_token_id = model.config.eos_token_id
        
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

# Preprocessing steps as needed
def preprocess_data(data):
    data.fillna("", inplace=True)  # add more preprocessing steps as needed
    return data

# Classify scraped data for the TFN variable
def classify_tfn(pipe, text):
    try:
        # Prompt contains few shot learning to prime LLM with edge cases it may struggle with
        prompt = f"""
            [INST]
            <<SYS>>
            You are an analyst that determines if a product is tobacco-free or synthetic nicotine. You will receive a product description. If it is a CBD/THC product, return N/A. If it is tobacco-free or uses synthetic nicotine, output true with the phrase or word that indicates this. If it is not, return False. 
            <</SYS>>
            [/INST]
            
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
            Experience the pinnacle of vaping technology with the Lost Mary MO20000 Pro Disposable Vape. This cutting-edge device boasts an impressive 18mL prefilled capacity with premium nic salts, delivering a satisfying 0% (0mg) or 5% (50mg) nicotine strength. Equipped with dual 0.9ohm mesh coils, it ensures consistent and flavorful vapor production with every puff. 
            [/INST]
            False - no trigger terms
            
            [INST]
            {text}
            [/INST]
            """
        # Set 256 max tokens due to length of some of the scraped product descriptions
        outputs = pipe(prompt, max_new_tokens=256, do_sample=False)
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

        outputs = pipe(prompt, max_new_tokens=64, do_sample=False)
        response = outputs[0]["generated_text"].strip()
        return response

    except Exception as e:
        return f"Error during classification: {e}"
    
def classify_iced(pipe, text):
    try:
#         prompt = f"""
#             [INST] <<SYS>> 
#             You analyze text to determine if the product's description terms related to "icy". You will receive text of a product's description. If it contains synonyms, return True. If it does not contain any synonyms, return False.
#             <</SYS>> [/INST]
            
#             [INST]
#             Frozen, freeze
#             [/INST]
#             True - trigger terms: "frozen", "freeze"
            
#             [INST]
#             Mint, Spearmint, Peppermint
#             [/INST]
#             True - trigger terms: "Mint", "Spearmint", "Peppermint"
            
#             [INST]
#             Cool, cooling, chill, chilling
#             [/INST]
#             True - trigger terms: "cool", "cooling", "chill", "chilling"
            
#             [INST]
#             Menthol
#             [/INST]
#             True - trigger terms: "menthol"
                    
#             [INST]
#             {text}
#             [/INST]
#         """
        prompt = f"""
        The following text consists of the name and a description for an e-cigarette product. Based on the text, does this e-cigarette produce a cooling sensation when used? Look for key words like 'mint,' 'icy,' 'menthol,' or similar words in the text. If these features are present in  the text, answer with yes. If not, answer with no. If the text doesn't describe an e-cigarette, answer with no.
        
        [INST]
        {text}
        [/INST]
        """
        outputs = pipe(prompt, max_new_tokens=64, do_sample=False)
        response = outputs[0]["generated_text"].strip()
        return response

    except Exception as e:
        return f"Error during classification: {e}"

def classify_product(pipe, text):
    try:
        prompt = f"""
            [INST] <<SYS>> 
            You analyze text to determine the product type based on categories below. You will receive text of a product's name and description.  
            
            If it is a prefilled cartridge (including tanks, cartridges, pods for e-cigarette devices, JUUL pods, Logic Pro Tanks) that is not intended to be refilled after liquid depleted, return: 
                {{"product_class": "Closed Refills"}}
            If it is a closed system (including rechargeable devices/kits intended to be used with prefilled cartridges, JUUL system, VUSE Solo system) that is sold by itself without additional cartridges, return:
                {{"product_class": "Closed System"}}
            If it is a disposable device (including Puff Bar, VGOD STIG, Elfbar) that is non-reusable e-cigarette device and is not intended to be refilled with e-liquid after depletion (once e-liquid has been consumed), return:
                {{"product_class": "Disposable System"}}
            If it is an e-liquid container used in e-cigarette devices (typically conaining humectant such as propylene glycol, nicotine ,and flavoring Vape Craft 120ML bottles), return:
                {{"product_class": "E-liquid"}}
            If it is an accessory or part (including battery, charger, device sold without e-liquids such as Ooze Slim Pen), return:
                {{"product_class": "Accessories"}}
            <</SYS>> [/INST]
            
            [INST]
            {text}
            [/INST]
        """
        outputs = pipe(prompt, max_new_tokens=128, do_sample=False)
        response = outputs[0]["generated_text"].strip()
        return response

    except Exception as e:
        return f"Error during classification: {e}"
    

def classify_dataset(pipe, data, flag=False):
    # Initialize 'classified' as a DataFrame with the 'all_text' column from 'data'
    classified = pd.DataFrame(data['all_text'])
    
    raw_llm = '_raw_llm'

    # Determine the classification function and column name based on flag
    if flag == 'iced':
        classified[flag + raw_llm] = data['all_text'].apply(lambda x: classify_iced(pipe, x))
    elif flag == 'tfn':
        classified[flag + raw_llm] = data['all_text'].apply(lambda x: classify_tfn(pipe, x))
    elif flag == 'cbd':
        classified[flag + raw_llm] = data['all_text'].apply(lambda x: classify_cbd(pipe, x))
    elif flag == 'product_type':
        classified[flag + raw_llm] = data['all_text'].apply(lambda x: classify_product(pipe, x))
    else:
        raise ValueError("Invalid flag specified. Use 'iced', 'tfn', 'cbd', or 'product_type'.")

    return classified

def save_classified_data(data, output_path):
    data.to_csv(output_path, index=False)
    print(f"Classified data saved to {output_path}.")

### Extracting LLM response
def extract_llm(row, llm_flag):
        first_line = row['all_text'].splitlines()[0]  # Extract the first line from 'description' column
        text = row[llm_flag + "_raw_llm"]
        if llm_flag == 'tfn' or llm_flag == 'cbd' or llm_flag == 'iced':
            # Check if the first line appears in the text
            if first_line in text:
                # Create a regex pattern to match [/INST] followed by specific content and capture it
                pattern = re.compile(rf'{re.escape(first_line)}.*?\[/INST\]\s*(.*?)(?:\n|$)', re.DOTALL)
                match = pattern.search(text)

                if match:
                    return match.group(1).strip()
        elif llm_flag == "product_type":
            # Pattern to find product_class within <<ANS>> ... [ANS] section if it exists
            ans_pattern = re.compile(
                r"<<ANS>>.*?[\'\"]product_class[\'\"]\s*:\s*\"(Closed Refills|Closed System|Disposable System|E-liquid|Accessories)\".*?\[ANS\]", 
                re.DOTALL
            )

            # First, attempt to find product_class within the <<ANS>> ... [ANS] section
            ans_match = ans_pattern.search(text)
            if ans_match:
                return f'{{"product_class": "{ans_match.group(1)}"}}'

            # If no match within <<ANS>> ... [ANS], search for the first occurrence after the first_line
            if first_line in text:
                general_pattern = re.compile(
                    rf'{re.escape(first_line)}.*?[\'\"]product_class[\'\"]\s*:\s*\"(Closed Refills|Closed System|Disposable System|E-liquid|Accessories)\"', 
                    re.DOTALL
                )
                match = general_pattern.search(text)
                return f'{{"product_class": "{match.group(1)}"}}' if match else None
        
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