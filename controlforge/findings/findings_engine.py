from datetime import datetime
import pandas as pd


def generate_terminated_user_findings(
    findings_df: pd.DataFrame
) -> list:

    findings = []

    for index, row in findings_df.iterrows():

        finding = {
            "finding_id": f"FND-TERM-{index + 1:03}",
            "severity": "Critical",
            "control_name": "Terminated User Access Review",
            "affected_user": row["account_name"],
            "full_name": row["full_name"],
            "issue_description": (
                "Terminated employee still has an active "
                "Active Directory account."
            ),
            "risk_statement": (
                "Unauthorized access may occur if terminated "
                "accounts remain active."
            ),
            "recommendation": (
                "Disable the account immediately and review "
                "offboarding procedures."
            ),
            "source_system": "Active Directory",
            "termination_date": row["termination_date"],
            "detected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        findings.append(finding)

    return findings


def generate_orphaned_account_findings(
    findings_df: pd.DataFrame
) -> list:

    findings = []

    for index, row in findings_df.iterrows():

        finding = {
            "finding_id": f"FND-ORPH-{index + 1:03}",
            "severity": "High",
            "control_name": "Orphaned Account Review",
            "affected_user": row["account_name"],
            "full_name": "Unknown / Not Found in HR",
            "issue_description": (
                "Active Directory account exists without a matching "
                "HR employee record."
            ),
            "risk_statement": (
                "Unowned or unmanaged accounts may be used for unauthorized "
                "access and may bypass standard joiner/mover/leaver controls."
            ),
            "recommendation": (
                "Investigate account ownership, disable if not required, "
                "and reconcile identity records with HR."
            ),
            "source_system": "Active Directory",
            "termination_date": "",
            "detected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        findings.append(finding)

    return findings


def generate_dormant_account_findings(
    findings_df: pd.DataFrame
) -> list:

    findings = []

    for index, row in findings_df.iterrows():

        is_privileged = str(row["is_privileged"]).lower() == "true"

        severity = "High" if is_privileged else "Medium"

        control_name = (
            "Dormant Privileged Account Review"
            if is_privileged
            else "Dormant Account Review"
        )

        finding = {
            "finding_id": f"FND-DORM-{index + 1:03}",
            "severity": severity,
            "control_name": control_name,
            "affected_user": row["account_name"],
            "full_name": "N/A",
            "issue_description": (
                f"Active account has not logged in for "
                f"{row['days_since_last_login']} days."
            ),
            "risk_statement": (
                "Dormant accounts may be exploited by unauthorized users, "
                "especially where access is privileged or no longer required."
            ),
            "recommendation": (
                "Review business need for the account and disable or remove "
                "access where no longer required."
            ),
            "source_system": "Active Directory",
            "termination_date": "",
            "last_login_date": str(row["last_login_date"].date()),
            "days_since_last_login": int(row["days_since_last_login"]),
            "detected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        findings.append(finding)

    return findings


def generate_mfa_gap_findings(
    findings_df: pd.DataFrame
) -> list:

    findings = []

    for index, row in findings_df.iterrows():

        is_privileged = str(row["is_privileged"]).lower() == "true"

        finding = {
            "finding_id": f"FND-MFA-{index + 1:03}",
            "severity": "Critical" if is_privileged else "High",
            "control_name": "MFA Compliance Review",
            "affected_user": row["account_name"],
            "full_name": "N/A",
            "issue_description": (
                "Active account does not have multi-factor "
                "authentication enabled."
            ),
            "risk_statement": (
                "Accounts without MFA are more vulnerable to credential theft, "
                "phishing, and unauthorized access."
            ),
            "recommendation": (
                "Enable MFA for the account and enforce MFA through "
                "identity provider policy."
            ),
            "source_system": "Active Directory",
            "termination_date": "",
            "mfa_enabled": row["mfa_enabled"],
            "detected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        findings.append(finding)

    return findings