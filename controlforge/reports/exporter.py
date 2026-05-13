from pathlib import Path
import json
import pandas as pd


OUTPUT_DIR = Path("outputs")


def export_findings(findings: list) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    json_path = OUTPUT_DIR / "findings.json"
    csv_path = OUTPUT_DIR / "findings.csv"

    with open(json_path, "w") as json_file:
        json.dump(findings, json_file, indent=4)

    findings_df = pd.DataFrame(findings)
    findings_df.to_csv(csv_path, index=False)

    print(f"\nFindings exported successfully:")
    print(f"- {json_path}")
    print(f"- {csv_path}")