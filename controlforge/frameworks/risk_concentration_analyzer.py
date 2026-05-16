from collections import defaultdict

from controlforge.controls.control_registry import (
    CONTROL_REGISTRY
)


def classify_domain_risk(
    critical: int,
    high: int,
    medium: int
):

    score = (
        (critical * 5)
        + (high * 3)
        + (medium * 1)
    )

    if score >= 40:
        return "Critical Risk"

    if score >= 20:
        return "High Risk"

    if score >= 10:
        return "Moderate Risk"

    return "Low Risk"


def analyze_risk_concentration(
    findings: list
):

    domain_metrics = defaultdict(
        lambda: {
            "critical": 0,
            "high": 0,
            "medium": 0
        }
    )

    finding_control_mapping = {
        "MFA Compliance Review":
            "MFA_ENFORCEMENT",

        "Terminated User Access Review":
            "TERMINATED_USER_ACCESS",

        "Segregation of Duties Review":
            "SOD_CONFLICTS"
    }

    for finding in findings:

        finding_name = finding.get(
            "control_name",
            ""
        )

        control_id = (
            finding_control_mapping.get(
                finding_name
            )
        )

        if not control_id:
            continue

        control = CONTROL_REGISTRY.get(
            control_id
        )

        if not control:
            continue

        domain = control["domain"]

        severity = finding.get(
            "severity",
            ""
        ).lower()

        if severity in [
            "critical",
            "high",
            "medium"
        ]:
            domain_metrics[domain][severity] += 1

    results = []

    for domain, metrics in domain_metrics.items():

        classification = classify_domain_risk(
            metrics["critical"],
            metrics["high"],
            metrics["medium"]
        )

        results.append(
            {
                "domain": domain,
                "critical": metrics["critical"],
                "high": metrics["high"],
                "medium": metrics["medium"],
                "risk_level": classification
            }
        )

    return results
