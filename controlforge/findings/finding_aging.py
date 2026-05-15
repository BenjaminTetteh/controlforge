from datetime import datetime


def detect_overdue_findings(
    findings: list
) -> list:

    overdue = []

    today = datetime.now().date()

    for finding in findings:

        due_date = datetime.strptime(
            finding["remediation_due_date"],
            "%Y-%m-%d"
        ).date()

        if (
            due_date < today
            and finding["status"] != "Closed"
        ):

            days_overdue = (
                today - due_date
            ).days

            overdue.append({
                "finding_id": (
                    finding["finding_id"]
                ),
                "affected_user": (
                    finding["affected_user"]
                ),
                "control_name": (
                    finding["control_name"]
                ),
                "severity": (
                    finding["severity"]
                ),
                "days_overdue": (
                    days_overdue
                )
            })

    return overdue