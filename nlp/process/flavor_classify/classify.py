import pandas as pd
from tqdm import tqdm
from .utils import classify_flavor_category

# Classifies the flavor category for each row in the DataFrame using the LLM classifier.
def classify_flavor_df(df: pd.DataFrame) -> pd.DataFrame:
    results = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Classifying flavor category"):

        result = classify_flavor_category(
            flavor_name=row.get("flavor_name", "") or "",
            flavor_description=row.get("flavor_description", "") or ""
        )

        # ensure dict format
        if not isinstance(result, dict):
            result = {
                "flavor_category": "Unknown",
                "confidence": "low",
                "rationale": "Non-dict result from classifier."
            }

        results.append(
            {
                "llm_flavor_category": result.get("flavor_category", "Unknown"),
                "llm_flavor_confidence": result.get("confidence", "low"),
                "llm_flavor_rationale": result.get("rationale", "")
            }
        )

    results_df = pd.DataFrame(results)
    return pd.concat([df.reset_index(drop=True), results_df], axis=1)


# Main function to run the flavor classification pipeline alone WITH sampling option
def main(
    input_path: str,
    output_path: str,
    sample: bool = False,
    sample_size: int = 30
):
    df = pd.read_csv(input_path)

    if sample:
        df = df.sample(n=min(len(df), sample_size), random_state=42).copy()
        output_path = output_path.replace(".csv", "_sample.csv")
        print(f"Running SAMPLE mode with {len(df)} rows.")

    final_df = classify_flavor_df(df)
    final_df.to_csv(output_path, index=False)

    print(f"Saved results to {output_path}.")


if __name__ == "__main__":
    main("input.csv", "flavor_output.csv")
