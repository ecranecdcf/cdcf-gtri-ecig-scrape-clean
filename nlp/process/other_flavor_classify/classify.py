import pandas as pd
from tqdm import tqdm
from .utils import classify_other_flavor

# Applies the LLM sub-flavor classifier to rows with 'Other Flavors'
def classify_other_flavor_df(df: pd.DataFrame) -> pd.DataFrame:
    subset = df[df["llm_flavor_category"].str.lower() == "other flavors"].copy()
    results = []

    for _, row in tqdm(subset.iterrows(), total=len(subset), desc="Classifying sub-flavors"):

        result = classify_other_flavor(
            flavor_name=row.get("flavor_name", "") or "",
            flavor_description=row.get("description", "") or ""
        )

        # Ensure dict output
        if not isinstance(result, dict):
            result = {
                "other_flavor_category": "Unknown",
                "confidence": "low",
                "rationale": "Non-dict output from classifier."
            }

        results.append(
            {
                "llm_other_flavor_category": result.get("other_flavor_category", "Unknown"),
                "llm_other_flavor_confidence": result.get("confidence", "low"),
                "llm_other_flavor_rationale": result.get("rationale", "")
            }
        )

    # Attach results to original dataframe
    results_df = pd.DataFrame(results)
    output_df = pd.concat([df.reset_index(drop=True), results_df], axis=1)

    return output_df

# Main function to run the other-flavor classification pipeline WITH sampling option
def main(
    input_path: str = "flavor_categorization_full_results.csv",
    output_path: str = "flavor_categorization_with_subcategories.csv",
    sample: bool = False,
    sample_size: int = 300,
    seed: int = 42
):
    df = pd.read_csv(input_path)

    if sample:
        df = df.sample(n=min(len(df), sample_size), random_state=42).copy()
        output_path = output_path.replace(".csv", "_sample.csv")
        print(f"Running SAMPLE mode with {len(df)} rows.")

    # Run classifier
    final_df = classify_other_flavor_df(df)
    final_df.to_csv(output_path, index=False)

    print(f"Saved other-flavor classification to {output_path}.")


if __name__ == "__main__":
    main("input.csv", "other_flavor_output.csv")
