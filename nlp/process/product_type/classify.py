import pandas as pd
from tqdm import tqdm
from .utils import classify_product_category

# Classifies the product type for each row in the DataFrame using the LLM classifier.
def classify_product_category_df(df: pd.DataFrame) -> pd.DataFrame:
    results = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Classifying product categories"):

        # Relevant fields for classification
        result = classify_product_category(
            product_name=row.get("product_name", "") or "",
            site_category=row.get("site_category", "") or "",
            site_tag=row.get("site_tag", "") or "",
            description=row.get("description", "") or "",
            package_contents=row.get("package_contents", "") or ""
        )

        # ensure dict format
        if not isinstance(result, dict):
            result = {
                "categories": "Unknown",
                "confidence": "low",
                "rationale": "Non-dict result from classifier."
            }

        results.append(
            {
                "llm_product_type": result.get("categories", "Unknown"),
                "llm_product_type_confidence": result.get("confidence", "low"),
                "llm_product_type_rationale": result.get("rationale", "")
            }
        )

    results_df = pd.DataFrame(results)
    return pd.concat([df.reset_index(drop=True), results_df], axis=1)

# Main function to run the product type classification pipeline alone WITH sampling option
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

    final_df = classify_product_category_df(df)
    final_df.to_csv(output_path, index=False)

    print(f"Saved results to {output_path}.")

if __name__ == "__main__":
    main("input.csv", "product_type_output.csv")
