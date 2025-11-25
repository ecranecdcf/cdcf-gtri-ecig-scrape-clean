import pandas as pd
import numpy as np
import pyodbc
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

# Point to the appropriate .env file for credentials to Azure DB
# PATH FUNCTIONS
NLP_ROOT = Path(__file__).resolve().parent.parent
INGEST_DATA_DIR = NLP_ROOT / "ingest"
CONFIG_PATH = NLP_ROOT / "config" / ".env"
print(CONFIG_PATH)
load_dotenv(CONFIG_PATH)

# Query the Azure SQL Database and return a DataFrame 
def get_data(query):
    # Set up the connection variables to Azure SQL Database
    print(os.getenv("AZURE_SERVER"))
    server = os.getenv("AZURE_SERVER")
    database = os.getenv("AZURE_DATABASE")
    username = os.getenv("AZURE_USERNAME")
    password = os.getenv("AZURE_PASSWORD")
    driver = os.getenv("AZURE_DRIVER", "{ODBC Driver 18 for SQL Server}")
    connection_string = (
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "PORT=1433;"
        "TrustServerCertificate=yes;"
    )
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame.from_records(data, columns=columns)
    return df

# Load input data from CSV or fallback to SQL query
def load_input_or_query(input_path, fallback_sql=None):
    input_path = Path(input_path)

    if input_path.exists():
        logging.info(f"Loading dataset from CSV: {input_path}")
        return pd.read_csv(input_path)

    logging.warning(f"CSV not found at path: {input_path}")

    if fallback_sql is None:
        raise FileNotFoundError(
            f"File not found: {input_path} and no fallback SQL query provided."
        )

    logging.info("Attempting fallback SQL query...")

    try:
        df = get_data(fallback_sql)
        export_to_csv(df, input_path.stem)
        logging.info("Loaded dataset from Azure SQL database.")
        return df
    except Exception as e:
        logging.error(f"SQL fallback failed: {e}")
        raise

# Read SQL file from the sql directory
def read_sql_file(name):
    sql_path = INGEST_DATA_DIR / name
    print(f"Reading SQL file from: {sql_path}")
    with open(sql_path, "r") as f:
        return f.read()

# Export Dataframe to CSV with timestamp
def export_to_csv(df, filename):
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{filename}_{timestamp}.csv"
    output_path = os.path.join(INGEST_DATA_DIR, "data", output_filename)
    df.to_csv(output_path, index=False)
    print(f"Data exported to {output_path}")