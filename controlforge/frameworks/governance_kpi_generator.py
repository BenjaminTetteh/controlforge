def generate_governance_kpis(
    scorecard: dict,
    concentrations: list,
    trends: dict
):

    critical_domains = len([
        item
        for item in concentrations
        if item["risk_level"] == "Critical Risk"
    ])

    improving_trends = len([
        value
        for value in trends.values()
        if value == "Improving"
    ])

    if improving_trends >= 2:
        governance_trend = "Improving"

    elif improving_trends == 1:
        governance_trend = "Stable"

    else:
        governance_trend = "Deteriorating"

    remediation_progress = max(
        0,
        100 - scorecard["open_findings"]
    )

    return {
        "governance_posture":
            scorecard["governance_posture"],

        "control_coverage":
            scorecard["coverage_percent"],

        "critical_risk_domains":
            critical_domains,

        "remediation_progress":
            remediation_progress,

        "governance_trend":
            governance_trend
    }