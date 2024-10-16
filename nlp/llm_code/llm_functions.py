import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import os

### Initializing the local model (downloaded via HuggingFace)
def init_llama_model():
    try:
        model_id = "/home/jjun44/CDCF_vape/Llama-3.1-8B-Instruct"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16)

        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=0 
        )

        print("LLM initialized successfully.")
        return pipe
    except Exception as e:
        print("Error initializing LLM:", e)
        return None

### Loading the vape dataset to classify
def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    data = pd.read_csv(file_path)
    return data

### Preprocessing data steps
def preprocess_data(data):
    data.fillna("", inplace=True)  # add more preprocessing steps as needed
    return data

### Custom prompt with few shot learning to mediate false negatives for TFN
def classify_with_custom_prompt(pipe, text):
    try:
        prompt = f"""
            <s>
            [INST]
            <<SYS>>
            You analyze text to determine if the product is tobacco-free. You will receive text of a product's description. If it is tobacco-free, output the phrase or word that indicates this. If it is not tobacco-free, return False.
            <</SYS>>
            
            The Hotbox Disposable Vape is a 7500 puff disposable vape featuring a mesh coil system and paired with 5% synthetic nicotine. This all new propriety mesh coil design allows for the purest and strongest flavor production out of any other disposable currently on the market.
            [/INST]
            synthetic nicotine - trigger term: "synthetic nicotine"
            </s>
            
            <s>
            [INST]
            Pod Juice, Pod FLO 3500 5.5% TF Disposable Device has a 10ml juice capacity and 3500 puff count with a 600mah battery, and comes in a variety of delightful flavors!
            [/INST]
            TF (abbreviated for Tobacco Free) - trigger term: "TF"
            </s>
            
            <s>
            [INST]
            Experience the pinnacle of vaping technology with the Lost Mary MO20000 Pro Disposable Vape. This cutting-edge device boasts an impressive 18mL prefilled capacity with premium nic salts, delivering a satisfying 5% (50mg) nicotine strength. Equipped with dual 0.9ohm mesh coils, it ensures consistent and flavorful vapor production with every puff.
            [/INST]
            FALSE - no trigger terms
            </s>
            
            <s>
            [INST]
            {text}
            [/INST]
            """

        outputs = pipe(prompt, max_new_tokens=256, do_sample=False)
        response = outputs[0]["generated_text"].strip()
        return response

    except Exception as e:
        return f"Error during classification: {e}"

def classify_dataset(pipe, data):
    data['classification'] = data['all_text'].apply(lambda x: classify_with_custom_prompt(pipe, x))
    return data

def save_classified_data(data, output_path):
    data.to_csv(output_path, index=False)
    print(f"Classified data saved to {output_path}.")


if __name__ == "__main__":
    file_path = 'data/vape_products.csv'
    output_path = 'data/classified_vape_products.csv'
    
    pipe = init_llama_model()
    if pipe is not None:
        try:
            data = load_data(file_path)
            data = preprocess_data(data)
            data = classify_dataset(pipe, data)
            save_classified_data(data, output_path)
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print("An error occurred:", e)