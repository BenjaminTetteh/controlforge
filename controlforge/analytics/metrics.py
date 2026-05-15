from collections import Counter
from datetime import datetime


def calculate_finding_metrics(findings: list) -> dict:
    severity_counts = Counter(
        finding.get("severity", "Unknown")
        for finding in findings
    )

    status_counts = Counter(
        finding.get("status", "Unknown")
        for finding in findings
    )

    remediation_owner_counts = Counter(
        finding.get("remediation_owner", "Unassigned")
        for finding in findings
    )

    open_findings = [
        finding for finding in findings
        if finding.get("status") != "Closed"
    ]

    closed_findings = [
        finding for finding in findings
        if finding.get("status") == "Closed"
    ]

    return {
        "total_findings": len(findings),
        "open_findings": len(open_findings),
        "closed_findings": len(closed_findings),
        "critical_findings": severity_counts.get("Critical", 0),
        "high_findings": severity_counts.get("High", 0),
        "medium_findings": severity_counts.get("Medium", 0),
        "low_findings": severity_counts.get("Low", 0),
        "unassigned_findings": remediation_owner_counts.get("Unassigned", 0),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }