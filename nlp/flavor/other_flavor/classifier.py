import pandas as pd
from tqdm import tqdm
from utils import classify_other_flavor, sample_other_flavors

### CHANGE THESE PATHS AS NEEDED ###
FLAVOR_INPUT = "flavor_categorization_full_results.csv"
FLAVOR_OUTPUT = "flavor_categorization_with_subcategories.csv"

SAMPLE = True  # If True, will sample 300 "Other" flavors for quick testing.
               # If False, will process the full dataset.
SAMPLE_OUTPUT = "flavor_categorization_sample_300.csv"

def main():
    
    global FLAVOR_INPUT, FLAVOR_OUTPUT

    if SAMPLE:
        sample_other_flavors(FLAVOR_INPUT, SAMPLE_OUTPUT, n=300, seed=42)
        FLAVOR_INPUT = SAMPLE_OUTPUT
        FLAVOR_OUTPUT = "flavor_categorization_with_subcategories_SAMPLE.csv"

    df = pd.read_csv(FLAVOR_INPUT)
    subset = df[df["predicted_category"].str.lower() == "other flavors"].copy()

    results = []
    for i, row in tqdm(subset.iterrows(), total=len(subset), desc="Classifying flavors"):
        res = classify_other_flavor(row["flavor_name"], row.get("description", ""))
        results.append(res)
       
    final = pd.concat([subset.reset_index(drop=True), pd.DataFrame(results)], axis=1)
    final.to_csv(FLAVOR_OUTPUT, index=False)
    print(f"Saved results to {FLAVOR_OUTPUT}.")

if __name__ == "__main__":
    main()
