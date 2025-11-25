import pandas as pd
from tqdm import tqdm
from .utils import classify_tfn_category 

# Classifies the TFN category for each row in the DataFrame using the LLM classifier.
def classify_tfn_df(df: pd.DataFrame) -> pd.DataFrame:
    results = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Classifying TFN"):
        
        result = classify_tfn_category(
            product_name=row.get("product_name", "") or "",
            description=row.get("description", "") or ""
        )

        # Safety check: ensure LLM returned a dict
        if not isinstance(result, dict):
            result = {
                "tfn_category": "Unknown",
                "confidence": "low",
                "rationale": "Non-dict result from classifier."
            }

        results.append(
            {
                "llm_tfn_category": result.get("tfn_category", "Unknown"),
                "llm_tfn_confidence": result.get("confidence", "low"),
                "llm_tfn_rationale": result.get("rationale", "")
            }
        )

    results_df = pd.DataFrame(results)
    return pd.concat([df.reset_index(drop=True), results_df], axis=1)

# Main function to run the TFN classification pipeline alone WITH sampling option
def main(
    input_path,
    output_path,
    sample: bool = False,
    sample_size: int = 30
):
    df = pd.read_csv(input_path)

    if sample:
        df = df.sample(n=min(len(df), sample_size), random_state=42).copy()
        output_path = output_path.replace(".csv", "_sample.csv")
        print(f"Running SAMPLE mode with {len(df)} rows.")

    final_df = classify_tfn_df(df)
    final_df.to_csv(output_path, index=False)
    print(f"Saved results to {output_path}.")


if __name__ == "__main__":
    main("input.csv", "tfn_output.csv")
