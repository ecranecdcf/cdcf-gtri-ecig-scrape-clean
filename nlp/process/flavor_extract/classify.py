import pandas as pd
from tqdm import tqdm
from utils import extract_flavors
import json

### CHANGE THESE PATHS AS NEEDED ###
FLAVOR_EXTRACT_INPUT = "azure_product_data.csv"
FLAVOR_EXTRACT_OUTPUT = "azure_flavor_extract_llm.csv"

SAMPLE = True  # If True, will sample 300 products for quick testing.
                # If False, will process the full dataset.
SAMPLE_SIZE = 10
SAMPLE_OUTPUT = f"flavor_categorization_sample_{SAMPLE_SIZE}_extracted_GPT_v1.csv"

def main():
    
    global FLAVOR_EXTRACT_INPUT, FLAVOR_EXTRACT_OUTPUT

    df = pd.read_csv(FLAVOR_EXTRACT_INPUT)
    df = df[['id', 'product_name', 'site_name', 'url', 'site_category', 'site_tag', 'description', 'flavor_text']]

    if SAMPLE:
        if len(df) > SAMPLE_SIZE:
            df = df.sample(n=SAMPLE_SIZE, random_state=42).copy()
        FLAVOR_EXTRACT_OUTPUT = SAMPLE_OUTPUT
        print(f"Running in SAMPLE mode. Processing {len(df)} random rows.")

    # We will process the entire DataFrame (or the sample)
    # The original script's subsetting for "other flavors" is removed.
    
    results = []
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Extracting flavors"):
        product_name = row.get("product_name", "")
        description = row.get("description", "")
        flavor_text = row.get("flavor_text", "")

        flavor_list = extract_flavors(
            product_name=product_name,
            description=description,
            flavor_text=flavor_text
        )

        # Ensure we always have a list
        if not isinstance(flavor_list, list):
            flavor_list = []

        # JSON-encode the full list for storage
        flavors_json = json.dumps(flavor_list, ensure_ascii=False)

        results.append(
            {
                "llm_flavors": flavors_json,
            }
        )
    results_df = pd.DataFrame(results)
    # Combine the original data with the new classification results
    final_df = pd.concat([df.reset_index(drop=True), results_df], axis=1)
    
    final_df.to_csv(FLAVOR_EXTRACT_OUTPUT, index=False)
    print(f"Saved results to {FLAVOR_EXTRACT_OUTPUT}.")

if __name__ == "__main__":
    main()