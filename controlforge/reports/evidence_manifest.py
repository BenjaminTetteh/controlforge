import json


def export_evidence_manifest(
    evidence_metadata: list,
    output_path
):
    output_file = output_path / "evidence_manifest.json"

    with open(output_file, "w") as file:
        json.dump(
            evidence_metadata,
            file,
            indent=4
        )

    print("\nEvidence manifest exported:")
    print(f"- {output_file}")