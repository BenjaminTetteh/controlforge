def generate_adaptive_governance_narrative(
    governance_posture: str,
    maturity_level: str,
    critical_findings: int,
    trend: str
):

    if (
        governance_posture == "Strong"
        and trend == "Improving"
    ):

        return (
            "Governance controls are operating "
            "effectively with improving maturity "
            "and a strong overall governance posture. "
            "Continued monitoring and optimization "
            "activities are recommended to sustain "
            "governance effectiveness."
        )

    if (
        governance_posture in [
            "Satisfactory",
            "Moderate"
        ]
        and trend in [
            "Stable",
            "Improving"
        ]
    ):

        return (
            "Governance controls are generally "
            "operating effectively; however, "
            "continued remediation and targeted "
            "governance improvements are recommended "
            "to further strengthen control maturity "
            "and reduce operational risk exposure."
        )

    if critical_findings >= 10:

        return (
            "Immediate management attention is "
            "required due to elevated critical "
            "control deficiencies and increased "
            "governance risk exposure. "
            "Accelerated remediation activities "
            "should be prioritized."
        )

    return (
        "Governance weaknesses require continued "
        "management oversight and remediation "
        "monitoring to improve governance posture "
        "and operational control effectiveness."
    )