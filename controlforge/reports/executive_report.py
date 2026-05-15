from datetime import datetime

from controlforge.reports.risk_themes import (
    analyze_risk_themes,
    determine_dominant_themes
)

def determine_risk_posture(
    metrics: dict
): 

    critical = metrics.get(
        "critical_findings",
        0
    )

    overdue = metrics.get(
        "overdue_findings",
        0
    )

    if critical >= 20:
        return "Severe"

    if critical >= 10 or overdue >= 5:
        return "High"

    if critical >= 5:
        return "Moderate"

    return "Low"


def build_significant_findings(
    findings: list
):

    grouped = {}

    severity_priority = {
        "Critical": 4,
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    for finding in findings:

        control = finding.get(
            "control_name",
            "Unknown Control"
        )

        severity = (
            finding.get("severity", "Low")
            .strip()
            .title()
        )

        issue = finding.get(
            "issue_description",
            ""
        )

        if control not in grouped:
            grouped[control] = {
                "count": 0,
                "severity": severity,
                "representative_issue": issue
            }

        grouped[control]["count"] += 1

        existing_severity = grouped[control]["severity"]

        if severity_priority.get(severity, 1) > severity_priority.get(
            existing_severity,
            1
        ):
            grouped[control]["severity"] = severity
            grouped[control]["representative_issue"] = issue

    sorted_controls = sorted(
        grouped.items(),
        key=lambda item: (
            severity_priority.get(item[1]["severity"], 1),
            item[1]["count"]
        ),
        reverse=True
    )

    output = []

    for control, data in sorted_controls[:5]:
        output.append(
            f"- {control} ({data['severity']} Risk): "
            f"{data['count']} related issue(s) identified. "
            f"Representative observation: "
            f"{data['representative_issue']}"
        )

    return "\n".join(output)


def build_governance_narrative(
    dominant_themes: list
):

    if not dominant_themes:

        return (
            "The audit identified general "
            "control improvement opportunities."
        )

    narrative_parts = []

    for item in dominant_themes:

        narrative_parts.append(
            item["theme"]
        )

    joined = ", ".join(
        narrative_parts
    )

    return (
        f"The audit identified recurring "
        f"governance weaknesses primarily "
        f"relating to {joined}."
    )


def generate_executive_summary(
    engagement_context: dict,
    findings: list,
    metrics: dict,
    remediation_metrics: dict,
    trends: dict
):

    client_name = engagement_context.get(
        "client_name"
    )

    framework = engagement_context.get(
        "framework"
    )

    audit_period = engagement_context.get(
        "audit_period"
    )

    engagement_id = engagement_context.get(
        "engagement_id"
    )

    auditor_name = engagement_context.get(
        "auditor_name"
    )

    generated_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    risk_posture = determine_risk_posture(
        metrics
    )

    significant_findings = (
        build_significant_findings(
            findings
        )
    )

    themes = analyze_risk_themes(
        findings
    )

    dominant_themes = (
        determine_dominant_themes(
            themes
        )
    )

    governance_narrative = (
        build_governance_narrative(
            dominant_themes
        )
    )

    report = f"""


EXECUTIVE GOVERNANCE SUMMARY
============================

Client:
{client_name}

Engagement ID:
{engagement_id}

Framework:
{framework}

Audit Period:
{audit_period}

Prepared By:
{auditor_name}

Generated:
{generated_at}


1. Executive Overview
---------------------

An audit assessment of the IT control environment was performed to evaluate the effectiveness of governance, access management, and operational control activities supporting the organization’s control framework.

Overall control environment posture was assessed as:
{risk_posture}

Control deficiencies were identified requiring management attention and remediation oversight.


2. Scope and Objectives
-----------------------

The review assessed key IT general controls relating to:

- User access management
- Privileged access governance
- Segregation of duties
- Dormant account monitoring
- Identity lifecycle management

Audit procedures included automated control testing, evidence reconciliation, and governance analytics.


3. Overall Control Environment Assessment
-----------------------------------------

{governance_narrative}

Risk exposure may result in:
- Unauthorized access
- Segregation of duties conflicts
- Delayed remediation response
- Elevated operational and compliance risk

Management should strengthen governance oversight and remediation monitoring processes.


4. Significant Findings
-----------------------

{significant_findings}


5. Remediation Status
---------------------

- Total Findings: {metrics['total_findings']}
- Open Findings: {metrics['open_findings']}
- Closed Findings: {metrics['closed_findings']}
- Overdue Findings: {remediation_metrics['overdue_findings']}

Remediation efforts are underway for identified control deficiencies.


6. Trend Analysis
-----------------

- Audit Runs Reviewed: {trends['total_runs']}
- Findings Change Since Previous Audit: {trends['findings_change']}
- Critical Findings Change: {trends['critical_change']}

Trend analysis indicates recurring governance issues requiring continued management focus.


7. Management Recommendations
-----------------------------

Management should prioritize:

- Strengthening access governance controls
- Enhancing remediation tracking processes
- Improving segregation of duties oversight
- Increasing governance monitoring activities
- Accelerating remediation of critical findings


8. Conclusion
-------------

The audit identified governance and control weaknesses requiring continued remediation oversight and management attention.

Continued improvement of governance processes, access controls, and operational monitoring activities will strengthen the overall control environment.

"""

    return report