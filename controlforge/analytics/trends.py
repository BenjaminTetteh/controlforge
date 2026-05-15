def calculate_trends(audit_history: list) -> dict:
    if not audit_history:
        return {
            "total_runs": 0,
            "latest_total_findings": 0,
            "previous_total_findings": 0,
            "findings_change": 0,
            "latest_critical_findings": 0,
            "previous_critical_findings": 0,
            "critical_change": 0
        }

    latest = audit_history[-1]
    previous = audit_history[-2] if len(audit_history) > 1 else {}

    latest_total = latest.get("total_findings", 0)
    previous_total = previous.get("total_findings", 0)

    latest_critical = latest.get("critical_findings", 0)
    previous_critical = previous.get("critical_findings", 0)

    return {
        "total_runs": len(audit_history),
        "latest_total_findings": latest_total,
        "previous_total_findings": previous_total,
        "findings_change": latest_total - previous_total,
        "latest_critical_findings": latest_critical,
        "previous_critical_findings": previous_critical,
        "critical_change": latest_critical - previous_critical
    }