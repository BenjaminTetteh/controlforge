import csv


FRAMEWORK_TEMPLATES = {
    "SOX": {
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
    },

    "ISO27001": {
        "asset_inventory.csv": [
            "asset_id",
            "asset_name",
            "owner",
            "criticality"
        ],
        "vulnerability_scan.csv": [
            "asset_id",
            "vulnerability",
            "severity",
            "status"
        ],
        "risk_register.csv": [
            "risk_id",
            "risk_description",
            "likelihood",
            "impact"
        ]
    },

    "PCI-DSS": {
        "firewall_rules.csv": [
            "rule_id",
            "source",
            "destination",
            "port",
            "action"
        ],
        "privileged_access.csv": [
            "account_name",
            "system",
            "privilege_level"
        ]
    }
}


def create_evidence_templates(
    framework: str,
    evidence_path
):

    templates = FRAMEWORK_TEMPLATES.get(
        framework,
        {}
    )

    for filename, headers in templates.items():

        file_path = evidence_path / filename

        if file_path.exists():
            continue

        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)