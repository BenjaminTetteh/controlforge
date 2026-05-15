import csv


EVIDENCE_TEMPLATES = {
    "hr_records.csv": [
        "account_name",
        "full_name",
        "job_title",
        "employment_status",
        "termination_date"
    ],
    "ad_accounts.csv": [
        "account_name",
        "full_name",
        "account_status",
        "last_login_date",
        "is_privileged",
        "mfa_enabled"
    ],
    "role_assignments.csv": [
        "account_name",
        "system_name",
        "role_code"
    ],
    "sod_rules.csv": [
        "system_name",
        "conflicting_role_1",
        "conflicting_role_2",
        "risk_level"
    ]
}


def create_evidence_templates(
    evidence_path
):

    for filename, headers in EVIDENCE_TEMPLATES.items():

        file_path = evidence_path / filename

        if file_path.exists():
            continue

        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)