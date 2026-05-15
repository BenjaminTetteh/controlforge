import json
import pandas as pd


def export_findings(findings: list, output_path) -> None:
    json_path = output_path / "findings.json"
    csv_path = output_path / "findings.csv"

    with open(json_path, "w") as json_file:
        json.dump(findings, json_file, indent=4)

    findings_df = pd.DataFrame(findings)
    findings_df.to_csv(csv_path, index=False)

    print("\nFindings exported successfully:")
    print(f"- {json_path}")
    print(f"- {csv_path}")

def export_audit_summary(summary: dict, output_path) -> None:
    summary_path = output_path / "audit_summary.json"

    with open(summary_path, "w") as json_file:
        json.dump(summary, json_file, indent=4)

    print("\nAudit summary exported:")
    print(f"- {summary_path}")

def export_text_report(
    report_text: str,
    output_path,
    filename: str
):

    report_file = output_path / filename

    with open(report_file, "w") as file:
        file.write(report_text)

    print("\nReport exported:")
    print(f"- {report_file}")