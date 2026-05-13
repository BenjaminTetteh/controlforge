from pathlib import Path
import pandas as pd


RAW_DATA_DIR = Path("data/raw")


def load_csv(filename: str) -> pd.DataFrame:
    file_path = RAW_DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Missing required file: {file_path}")

    return pd.read_csv(file_path)


def load_all_evidence() -> dict:
    return {
        "hr_records": load_csv("hr_records.csv"),
        "ad_accounts": load_csv("ad_accounts.csv"),
        "role_assignments": load_csv("role_assignments.csv"),
        "sod_rules": load_csv("sod_rules.csv"),
    }