from pathlib import Path
import json
import pandas as pd


RAW_DATA_DIR = Path("data/raw")
NORMALIZED_DATA_DIR = Path("data/normalized")
MAPPINGS_DIR = Path("data/mappings")


def load_mapping(mapping_file: str) -> dict:

    mapping_path = MAPPINGS_DIR / mapping_file

    with open(mapping_path, "r") as file:
        mapping = json.load(file)

    return mapping


def normalize_csv(
    input_filename: str,
    mapping_filename: str,
    output_filename: str
) -> pd.DataFrame:

    input_path = RAW_DATA_DIR / input_filename

    df = pd.read_csv(input_path)

    mapping = load_mapping(mapping_filename)

    normalized_df = df.rename(columns=mapping)

    NORMALIZED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        NORMALIZED_DATA_DIR / output_filename
    )

    normalized_df.to_csv(
        output_path,
        index=False
    )

    return normalized_df