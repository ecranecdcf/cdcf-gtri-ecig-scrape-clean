import time
from langfuse.openai import openai
import os
import traceback
import threading
import tiktoken  # For accurate token counting
import torch
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import dotenv
from langfuse import Langfuse


dotenv.load_dotenv()

# api_key = os.getenv("GLADOS_KEY")

# gets API Key from environment variable OPENAI_API_KEY
model_name = os.getenv("GLADOS_MODEL")
alt_model_name = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
# local_model_name = "meta-llama/Llama-3.2-3B-Instruct"
base_url = os.getenv('GLADOS_HOST')
api_key = os.getenv('GLADOS_KEY')
alt_api_key = os.getenv('OPENAI_API_KEY')
glados_client = openai.OpenAI(api_key=api_key, base_url=base_url)
openai_client = openai.OpenAI(api_key=alt_api_key)

langfuse = Langfuse(
  secret_key=os.getenv("LANGFUSE_SECRET"),
  public_key=os.getenv("LANGFUSE_PUBLIC"),
  host=os.getenv("LANGFUST_HOST")
)

def init_llm():
    """
    Initializes the LLM pipeline with the specified model.
    This function is called at the start of the script to set up the model.
    """
    print('Initializing LLM...')
    global local_pipeline, model, tokenizer
    # Load the model and tokenizer
    model_id = "meta-llama/Llama-3.2-3B-Instruct"
    print('init llama local')
    local_pipeline = pipeline(
        "text-generation",
        model=model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )

    # Access the model and tokenizer
    model = local_pipeline.model
    tokenizer = local_pipeline.tokenizer


    # Ensure the tokenizer has a pad token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        model.config.pad_token_id = tokenizer.pad_token_id

    # Configuration
    PROVIDER_RATE_LIMITS = {
        "your_provider": {  # Replace "your_provider" with the actual provider name
            "tokens": 3000,
            "requests": 10,
            "seconds": 60,  # 1 minute
        },
        # ... other providers
    }

    return model, tokenizer, local_pipeline



def cut_off_strings(strings, max_tokens, model_name="gpt-3.5-turbo"):
    """
    Cuts off strings in an array to ensure they don't exceed the maximum token limit.

    Args:
      strings: A list of strings.
      max_tokens: The maximum number of tokens allowed.
      model_name: The name of the OpenAI model to use for tokenization (default: gpt-3.5-turbo).

    Returns:
      A list of strings, where each string is truncated to fit within the token limit.
    """

    encoding = tiktoken.encoding_for_model(model_name)
    truncated_strings = []
    total_tokens = 0

    for string in strings:
        encoded = encoding.encode(string)
        num_tokens = len(encoded)

        if total_tokens + num_tokens > max_tokens:
            remaining_tokens = max_tokens - total_tokens
            if remaining_tokens > 0:  # Truncate if there are remaining tokens
                truncated_encoded = encoded[:remaining_tokens]
                truncated_string = encoding.decode(truncated_encoded)
                truncated_strings.append(truncated_string)
            break  # Stop adding more strings
        else:
            truncated_strings.append(string)
            total_tokens += num_tokens

    print('total_tokens', total_tokens)
    return truncated_strings

def extract_text_from_llm(d):
    """
    Extracts text from a list of dictionaries where each dictionary has a 'type' and 'text' key,
    specifically targeting dictionaries where 'type' is 'text'.
    """
    try:
        if isinstance(d, str):
            data = json.loads(d)
        else:
            data = d
        extracted_texts = []
        for item in data:
            if item.get('type') == 'text':
                extracted_texts.append(item.get('text'))
        return ('\n'.join(extracted_texts)).strip()
    except Exception as ex:
        print(ex)
        return d.strip()


def llm_query(prompt, question, limit=-1, tags=None, name='cdcf-vape-query', session_id=None, use_glados=True):
    chats = []
    if not tags:
        tags = []

    if use_glados:
        client = glados_client
        model = model_name
    else:
        client = openai_client
        model = alt_model_name

    metadata = {
        'langfuse_tags': tags,
        'langfuse_session_id': session_id
    }
    # truncated_strings = cut_off_strings(messages, 16000, model_name=alt_model_name)
    messages=[
            {"role": "system", "content": prompt}, # Reference the prompt by its Langfuse ID
            {"role": "user", "content": question}
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            name=name,
            metadata=metadata,
        )
    except openai.APIError as e:
        if "limit" in e.message.lower():  # Check for "Rate limit" in the error message
            print(f"Rate limit error: {e}")
            wait_time = 30
            max_retries = 3
            for attempt in range(max_retries):
                wait_time *= 2
                print(f"Retrying in {wait_time} seconds (attempt {attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=chats,
                        name=name,
                        metadata=metadata,
                    )
                except openai.APIError as e_retry:
                    if "limit" in e_retry.message.lower(): # Check again for Rate limit in message
                        print(f"Rate limit error (retry {attempt + 1}): {e_retry}")
                        continue  # Continue to the next retry
                    else:
                        print(f"Other API Error (retry {attempt + 1}): {e_retry}")
                        return None # Or raise
                except Exception as e:
                    print(f"An unexpected error occurred during retry: {e}")
                    return None
            else:
                print("Maximum retries exceeded. Giving up.")
                return None
        else:
            print(f"Other API Error: {e}") # Handle other API errors (not rate limit)
            return None # Or raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    features = response.choices[0].message.content
    print('SLEEPING....1')
    time.sleep(1)
    
    return features

def llm_query_local(messages, limit=-1):
    chats = [    
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are an assistant that must respond to the user question in a concise and accurate manner."
                }
            ]
        }
    ]

    truncated_strings = cut_off_strings(messages, 3000, model_name=alt_model_name)
    
    for m in truncated_strings:
        chats.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": m
                    },

                ],
            })
        
    if len(chats) == 0:
        return None
    
    outputs = local_pipeline(
        chats,
        max_new_tokens=1024,
    )
    
    print()
    print()
    output =  outputs[0]["generated_text"][-1].get('content')
    final_val = extract_text_from_llm(output)
    print(output)
    print(final_val)
    return final_val
