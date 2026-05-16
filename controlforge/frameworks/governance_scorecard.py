from controlforge.frameworks.control_coverage_analyzer import (
    analyze_control_coverage
)

from controlforge.analytics.metrics import (
    calculate_finding_metrics
)


def generate_governance_scorecard(
    framework_code: str,
    engagement_path,
    findings: list
):

    coverage = analyze_control_coverage(
        framework_code=framework_code,
        engagement_path=engagement_path
    )

    finding_metrics = calculate_finding_metrics(
        findings
    )

    return {
        "framework": framework_code,
        "coverage_percent": coverage[
            "coverage_percent"
        ],
        "maturity_level": coverage[
            "maturity_level"
        ],
        "governance_posture": coverage[
            "governance_posture"
        ],
        "critical_findings": finding_metrics[
            "critical_findings"
        ],
        "open_findings": finding_metrics[
            "open_findings"
        ],
        "total_findings": finding_metrics[
            "total_findings"
        ]
    }