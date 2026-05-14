from pathlib import Path
import pandas as pd

from controlforge.normalization.normalizer import (
    normalize_csv
)


NORMALIZED_DATA_DIR = Path("data/normalized")


def load_csv(filename: str) -> pd.DataFrame:

    file_path = NORMALIZED_DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Missing normalized file: {file_path}"
        )

    return pd.read_csv(file_path)


def normalize_all_evidence():

    normalize_csv(
        input_filename="hr_records.csv",
        mapping_filename="hr_mapping.json",
        output_filename="hr_records_normalized.csv"
    )

    normalize_csv(
        input_filename="ad_accounts.csv",
        mapping_filename="ad_mapping.json",
        output_filename="ad_accounts_normalized.csv"
    )

    normalize_csv(
        input_filename="role_assignments.csv",
        mapping_filename="roles_mapping.json",
        output_filename="role_assignments_normalized.csv"
    )

    normalize_csv(
        input_filename="sod_rules.csv",
        mapping_filename="sod_mapping.json",
        output_filename="sod_rules_normalized.csv"
    )


def load_all_evidence() -> dict:

    normalize_all_evidence()

    return {
        "hr_records": load_csv(
            "hr_records_normalized.csv"
        ),

        "ad_accounts": load_csv(
            "ad_accounts_normalized.csv"
        ),

        "role_assignments": load_csv(
            "role_assignments_normalized.csv"
        ),

        "sod_rules": load_csv(
            "sod_rules_normalized.csv"
        )
    }