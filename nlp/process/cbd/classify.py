import pandas as pd
from tqdm import tqdm
from .utils import classify_cbd_category 

# Classifies the CBD/THC category for each row in the DataFrame using the LLM classifier.
def classify_cbd_df(df: pd.DataFrame) -> pd.DataFrame:
    results = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Classifying CBD/THC"):
        
        result = classify_cbd_category(
            product_name=row.get("product_name", "") or "",
            description=row.get("description", "") or ""
        )

        # Safety check: ensure LLM returned a dict
        if not isinstance(result, dict):
            result = {
                "cbd_thc_class": "Unknown",
                "confidence": "low",
                "rationale": "Non-dict result from classifier."
            }

        results.append(
            {
                "llm_cbd_thc_category": result.get("cbd_category", "Unknown"),
                "llm_cbd_thc_confidence": result.get("confidence", "low"),
                "llm_cbd_thc_rationale": result.get("rationale", "")
            }
        )

    results_df = pd.DataFrame(results)
    return pd.concat([df.reset_index(drop=True), results_df], axis=1)

# Main function to run the CBD classification pipeline alone WITH sampling option
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

    final_df = classify_cbd_df(df)
    final_df.to_csv(output_path, index=False)
    print(f"Saved results to {output_path}.")


if __name__ == "__main__":
    main("input.csv", "cbd_output.csv")
