import pandas as pd
from datetime import datetime
import os
import sys
from pathlib import Path

# Import data ingestion
from ingest.ingest import load_input_or_query, read_sql_file

# Import LLM modules
from process.regex.classify import classify_regex_df
from process.product_type.classify import classify_product_category_df
from process.cbd.classify import classify_cbd_df
from process.tfn.classify import classify_tfn_df
# from process.flavor_extract.classify import classify_flavor_extract_df

# PATH FUNCTIONS
NLP_ROOT = Path(__file__).resolve().parent
INGEST_DATA_DIR = NLP_ROOT / "ingest"

def run_product_pipeline(input_path: str, output_path: str):
    print(f"Loading dataset: {input_path}")
    df = load_input_or_query(input_path, read_sql_file("sql/product.sql"))

    # ---- REGEX ---- (Nicotine Level, E-liquid Content, TFN)
    print("\nRunning regex functions (nicotine level, e-liquid content, TFN)...")
    df = classify_regex_df(df)

    # ---- PRODUCT TYPE ----
    print("\nRunning Product Type Classification...")
    df = classify_product_category_df(df)

    # ---- CBD ----
    print("\nRunning CBD Classification...")
    df = classify_cbd_df(df)

    # ---- TFN ----
    print("\nRunning TFN Classification...")
    df = classify_tfn_df(df)

    ### STILL IN PROGRESS ###
    # # ---- FLAVOR EXTRACTION ----
    # print("\nRunning Flavor Extraction...")
    # df = classify_flavor_extract_df(df)
    
    print(f"\nSaving final output to: {output_path}")
    df.to_csv(output_path, index=False)

    print("\nPipeline completed successfully!")
    return df

# ###############################################
# # FLAVOR AND OTHER FLAVOR PIPELINE
# ################################################
from process.flavor_classify.classify import classify_flavor_df
from process.other_flavor_classify.classify import classify_other_flavor_df

def run_flavor_pipeline(input_path: str, output_path: str):
    print(f"Loading dataset: {input_path}")
    df = load_input_or_query(input_path, read_sql_file(INGEST_DATA_DIR / "sql/flavor.sql"))

    # ---- FLAVOR CLASSIFICATION ----
    print("\nRunning Flavor Classification...")
    df = classify_flavor_df(df)

    # # ---- OTHER FLAVOR CLASSIFICATION ----
    # print("\nRunning Other Flavor Classification...")
    # df = classify_other_flavor_df(df)

    print(f"\nSaving final output to: {output_path}")
    df.to_csv(output_path, index=False)

    print("\nFlavor Pipeline completed successfully!")
    return df


if __name__ == "__main__":
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    INPUT_PRODUCT = INGEST_DATA_DIR / "data/products.csv"
    OUTPUT_PRODUCT = NLP_ROOT / f"output/azure_product_data_output_{ts}.csv"
    run_product_pipeline(INPUT_PRODUCT, OUTPUT_PRODUCT)

    INPUT_FLAVOR = INGEST_DATA_DIR / "data/flavors.csv"
    OUTPUT_FLAVOR = NLP_ROOT / f"output/azure_flavor_data_output_{ts}.csv"
    run_flavor_pipeline(INPUT_FLAVOR, OUTPUT_FLAVOR)
