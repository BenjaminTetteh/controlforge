from pathlib import Path
from datetime import datetime
import hashlib
import pandas as pd


RAW_DATA_DIR = Path("data/raw")


def generate_file_hash(file_path: Path) -> str:

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def generate_evidence_metadata(
    filename: str
) -> dict:

    file_path = RAW_DATA_DIR / filename

    file_hash = generate_file_hash(file_path)

    file_size = file_path.stat().st_size

    row_count = len(pd.read_csv(file_path))

    metadata = {
        "file_name": filename,
        "sha256": file_hash,
        "file_size_bytes": file_size,
        "row_count": row_count,
        "ingested_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    return metadata