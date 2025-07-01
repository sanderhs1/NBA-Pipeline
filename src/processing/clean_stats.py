import pandas as pd
import os
import argparse
from pathlib import Path

PROCESSED_DIR = Path("data/processed")

def clean_column_names(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("%", "pct")
        .str.replace("/", "_per_")
    )
    return df

def convert_types(df):
    if 'game_date' in df.columns:
        df['game_date'] = pd.to_datetime(df['game_date'], errors='coerce')

    for col in df.select_dtypes(include='object').columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')

    return df

def add_features(df):
    if 'min' in df.columns and 'pts' in df.columns:
        df['min'] = df['min'].apply(lambda x: int(x.split(":")[0]) if isinstance(x, str) and ":" in x else pd.to_numeric(x, errors='coerce'))
        df['pts_per_min'] = df['pts'] / df['min'].replace(0, pd.NA)
    return df

def clean_stats(input_file, output_file):
    print("Reading:", input_file)
    df = pd.read_csv(input_file)
    df = clean_column_names(df)
    df = convert_types(df)
    df = add_features(df)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df.to_csv(output_file, index=False)
    print("Saved:", output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True, help="Full path to raw CSV file")
    parser.add_argument("--output_file", type=str, required=False, help="Full path for cleaned CSV output")

    args = parser.parse_args()

    input_path = Path(args.input_file)
    if args.output_file:
        output_path = Path(args.output_file)
    else:
        stem = input_path.stem.replace(".csv", "") + "_clean.csv"
        output_path = PROCESSED_DIR / stem

    clean_stats(str(input_path), str(output_path))
