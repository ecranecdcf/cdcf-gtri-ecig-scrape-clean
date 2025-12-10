import pandas as pd
from tqdm import tqdm
from .utils import extract_flavors
import json

# Function to extract flavors for each row in the DataFrame using the LLM extractor.
def extract_flavors_df(df: pd.DataFrame) -> pd.DataFrame:
    results = []

    # Use a subset of columns for the extraction logic
    df_process = df[['id', 'product_name', 'description', 'flavor_text']]

    for _, row in tqdm(df_process.iterrows(), total=len(df_process), desc="Extracting flavors"):
        product_name = row.get("product_name", "") or ""
        description = row.get("description", "") or ""
        flavor_text = row.get("flavor_text", "") or ""

        flavor_list = extract_flavors(
            product_name=product_name,
            description=description,
            flavor_text=flavor_text
        )

        # Ensure result is a list and JSON-encode it
        if not isinstance(flavor_list, list):
            flavor_list = []
        
        flavors_json = json.dumps(flavor_list, ensure_ascii=False)

        results.append(
            {
                "llm_flavors": flavors_json,
            }
        )

    results_df = pd.DataFrame(results)
    # Combine the original data with the new extraction results
    return pd.concat([df.reset_index(drop=True), results_df], axis=1)


# Main function to run the flavor extraction pipeline with sampling option
def main(
    input_path: str,
    output_path: str,
    sample: bool = False,
    sample_size: int = 10
):
    df = pd.read_csv(input_path)

    current_output_path = output_path

    if sample:
        n_sample = min(len(df), sample_size)
        df = df.sample(n=n_sample, random_state=42).copy()
        
        # Modify output path for sample run, similar to the second block's pattern
        current_output_path = output_path.replace(".csv", f"_sample_{n_sample}.csv")
        print(f"Running SAMPLE mode with {len(df)} rows.")

    # The column subsetting happens inside extract_flavors_df
    final_df = extract_flavors_df(df) 
    final_df.to_csv(current_output_path, index=False)

    print(f"Saved results to {current_output_path}.")


if __name__ == "__main__":
    # Define default paths/settings here or pass them as arguments
    FLAVOR_EXTRACT_INPUT = "azure_product_data.csv"
    FLAVOR_EXTRACT_OUTPUT = "azure_flavor_extract_llm.csv"
    
    # Example usage: Run without sampling
    # main(FLAVOR_EXTRACT_INPUT, FLAVOR_EXTRACT_OUTPUT) 

    main(
        input_path=FLAVOR_EXTRACT_INPUT, 
        output_path=FLAVOR_EXTRACT_OUTPUT, 
        sample=True, 
        sample_size=10
    )