from pathlib import Path
import json


OUTPUT_DIR = Path("outputs/metadata")


def export_evidence_manifest(
    evidence_metadata: list
):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        OUTPUT_DIR / "evidence_manifest.json"
    )

    with open(output_file, "w") as file:
        json.dump(
            evidence_metadata,
            file,
            indent=4
        )

    print("\nEvidence manifest exported:")
    print(f"- {output_file}")