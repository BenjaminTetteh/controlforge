def score_maturity(
    coverage_percent: float
):

    if coverage_percent >= 90:
        return {
            "maturity_level": "Optimized",
            "governance_posture": "Strong"
        }

    if coverage_percent >= 75:
        return {
            "maturity_level": "Managed",
            "governance_posture": "Satisfactory"
        }

    if coverage_percent >= 50:
        return {
            "maturity_level": "Developing",
            "governance_posture": "Moderate"
        }

    if coverage_percent > 0:
        return {
            "maturity_level": "Initial",
            "governance_posture": "Weak"
        }

    return {
        "maturity_level": "Not Implemented",
        "governance_posture": "Severe"
    }