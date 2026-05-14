CONTROL_REGISTRY = {
    "terminated_user_access": {
        "control_id": "CTRL-IAM-001",
        "control_name": "Terminated User Access Review",
        "control_version": "1.0",
        "source_evidence": "hr_records.csv, ad_accounts.csv",
        "normalized_evidence": "hr_records_normalized.csv, ad_accounts_normalized.csv"
    },
    "orphaned_accounts": {
        "control_id": "CTRL-IAM-002",
        "control_name": "Orphaned Account Review",
        "control_version": "1.0",
        "source_evidence": "hr_records.csv, ad_accounts.csv",
        "normalized_evidence": "hr_records_normalized.csv, ad_accounts_normalized.csv"
    },
    "dormant_accounts": {
        "control_id": "CTRL-IAM-003",
        "control_name": "Dormant Account Review",
        "control_version": "1.0",
        "source_evidence": "ad_accounts.csv",
        "normalized_evidence": "ad_accounts_normalized.csv"
    },
    "mfa_compliance": {
        "control_id": "CTRL-IAM-004",
        "control_name": "MFA Compliance Review",
        "control_version": "1.0",
        "source_evidence": "ad_accounts.csv",
        "normalized_evidence": "ad_accounts_normalized.csv"
    },
    "sod_conflicts": {
        "control_id": "CTRL-IAM-005",
        "control_name": "Segregation of Duties Review",
        "control_version": "1.0",
        "source_evidence": "role_assignments.csv, sod_rules.csv",
        "normalized_evidence": "role_assignments_normalized.csv, sod_rules_normalized.csv"
    }
}