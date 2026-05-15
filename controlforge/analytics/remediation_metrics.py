from datetime import datetime
from datetime import date


def calculate_remediation_metrics(
    findings: list
):

    open_findings = []
    closed_findings = []

    closure_durations = []

    for finding in findings:

        status = finding.get("status")

        remediation_due_date = finding.get(
                        "remediation_due_date"
                    )    

        if status == "Closed":
            closed_findings.append(finding)

            created_at = finding.get(
                "created_at"
            )

            closed_at = finding.get(
                "closed_at"
            )

            if created_at and closed_at:

                created_date = datetime.strptime(
                    created_at,
                    "%Y-%m-%d %H:%M:%S"
                )

                closed_date = datetime.strptime(
                    closed_at,
                    "%Y-%m-%d %H:%M:%S"
                )

                duration_days = (
                    closed_date - created_date
                ).days

                closure_durations.append(
                    duration_days
                )

        else:
            open_findings.append(finding)

            overdue_findings = 0

        today = date.today()

        for finding in open_findings:

            due_date = finding.get(
                "remediation_due_date"
            )

            if not due_date:
                continue

            due_date_obj = datetime.strptime(
                due_date,
                "%Y-%m-%d"
            ).date()

            if due_date_obj < today:
                overdue_findings += 1

    average_closure_time = 0

    if closure_durations:

        average_closure_time = round(
            sum(closure_durations)
            / len(closure_durations),
            2
        )

    return {
        "total_findings": len(findings),
        "open_findings": len(open_findings),
        "closed_findings": len(closed_findings),
        "overdue_findings": overdue_findings,
        "average_closure_time_days": (
            average_closure_time
        )
    }