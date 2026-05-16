def classify_trend(
    current: float,
    previous: float
):

    if current > previous:
        return "Improving"

    if current < previous:
        return "Deteriorating"

    return "Stable"


def analyze_governance_trends(
    current_scorecard: dict,
    previous_scorecard: dict
):

    return {

        "coverage_trend": classify_trend(
            current_scorecard["coverage_percent"],
            previous_scorecard["coverage_percent"]
        ),

        "critical_findings_trend": classify_trend(
            previous_scorecard["critical_findings"],
            current_scorecard["critical_findings"]
        ),

        "open_findings_trend": classify_trend(
            previous_scorecard["open_findings"],
            current_scorecard["open_findings"]
        )
    }