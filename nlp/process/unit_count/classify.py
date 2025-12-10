import pandas as pd
from tqdm import tqdm
from .utils import classify_unit_count 

# Classifies the unit count for each row in the DataFrame using the LLM classifier.
def classify_unit_count_df(df: pd.DataFrame) -> pd.DataFrame:
    results = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Extracting unit counts"):
        
        result = classify_unit_count(
            product_name=row.get("product_name", "") or "",
            description=row.get("description", "") or "",
            package_contents=row.get("package_contents", "") or ""
        )

        # Safety check: ensure LLM returned a dict
        if not isinstance(result, dict):
            result = {
                "unit_count": 1,
                "confidence": "low",
                "rationale": "Non-dict result from classifier."
            }

        results.append(
            {
                "llm_unit_count": result.get("unit_count", 1),
                "llm_unit_count_confidence": result.get("confidence", "low"),
                "llm_unit_count_rationale": result.get("rationale", "")
            }
        )

    results_df = pd.DataFrame(results)
    return pd.concat([df.reset_index(drop=True), results_df], axis=1)

# Main function to run the unit count extraction pipeline WITH sampling option
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

    final_df = classify_unit_count_df(df)
    final_df.to_csv(output_path, index=False)
    print(f"Saved results to {output_path}.")


if __name__ == "__main__":
    main("input.csv", "unit_count_output.csv")