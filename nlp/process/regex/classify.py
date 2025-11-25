import pandas as pd
from .utils import (
    populate_nicotine_and_eliquid,
    populate_nic_free,
)

# Main function to run regex classification pipeline 
def classify_regex_df(df: pd.DataFrame) -> pd.DataFrame:
    # Extract nicotine and e-liquid levels
    df = populate_nicotine_and_eliquid(df)

    # Determine nicotine-free status
    df = populate_nic_free(df)

    return df


def main(
    input_path,
    output_path
):
    df = pd.read_csv(input_path)
    df = classify_regex_df(df)
    df.to_csv(output_path, index=False)
    print(f"Saved regex classification to {output_path}")


if __name__ == "__main__":
    main("input.csv", "regex_output.csv")
