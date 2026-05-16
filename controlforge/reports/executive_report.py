from datetime import datetime

from controlforge.reports.risk_themes import (
    analyze_risk_themes,
    determine_dominant_themes
)

from controlforge.reports.report_builder import (
    add_section,
    render_text_report
)

from controlforge.frameworks.risk_concentration_analyzer import (
    analyze_risk_concentration
)

from controlforge.reports.risk_narrative_generator import (
    generate_risk_concentration_narrative
)

from controlforge.reports.adaptive_narrative_generator import (
    generate_adaptive_governance_narrative
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


def build_executive_report_sections(
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

    framework_metadata = engagement_context.get(
        "framework_metadata",
        {}
    )

    framework_name = framework_metadata.get(
        "name",
        framework
    )

    framework_description = framework_metadata.get(
        "description",
        ""
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

    critical_trend = "Stable"

    if trends.get("critical_change", 0) < 0:
        critical_trend = "Improving"

    if trends.get("critical_change", 0) > 0:
        critical_trend = "Deteriorating"

    adaptive_narrative = generate_adaptive_governance_narrative(
        governance_posture=risk_posture,
        maturity_level="",
        critical_findings=metrics["critical_findings"],
        trend=critical_trend
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

    risk_concentrations = analyze_risk_concentration(
        findings
    )

    risk_concentration_narrative = (
        generate_risk_concentration_narrative(
            risk_concentrations
        )
    )

    sections = []

    add_section(
        sections,
        "Executive Governance Summary",
        f"""
Client: {client_name}

Engagement ID: {engagement_id}

Framework: {framework_name} ({framework})

Audit Period: {audit_period}

Prepared By: {auditor_name}

Generated: {generated_at}
"""
    )

    add_section(
        sections,
        "Executive Overview",
        f"""
    An audit assessment of the IT control environment was performed to evaluate the effectiveness of governance, access management, and operational control activities supporting the organization’s control framework.

    Overall control environment posture was assessed as:
    {risk_posture}

    {adaptive_narrative}
    """
    )

    add_section(
        sections,
        "Scope and Objectives",
        f"""
    This engagement was performed in alignment with {framework_name}. {framework_description}    
    The review assessed key IT general controls relating to:

    - User access management
    - Privileged access governance
    - Segregation of duties
    - Dormant account monitoring
    - Identity lifecycle management

    Audit procedures included automated control testing, evidence reconciliation, and governance analytics.
    """
    )

    add_section(
        sections,
        "Overall Control Environment Assessment",
        f"""
    {governance_narrative}

    Risk exposure may result in:
    - Unauthorized access
    - Segregation of duties conflicts
    - Delayed remediation response
    - Elevated operational and compliance risk

    Management should strengthen governance oversight and remediation monitoring processes.
    """
    )

    add_section(
        sections,
        "Risk Concentration Analysis",
        risk_concentration_narrative
    )

    add_section(
        sections,
        "Significant Findings",
        significant_findings
    )

    add_section(
        sections,
        "Remediation Status",
        f"""
    - Total Findings: {metrics['total_findings']}
    - Open Findings: {metrics['open_findings']}
    - Closed Findings: {metrics['closed_findings']}
    - Overdue Findings: {remediation_metrics['overdue_findings']}

    Remediation efforts are underway for identified control deficiencies.
    """
    )

    add_section(
        sections,
        "Trend Analysis",
        f"""
    - Audit Runs Reviewed: {trends['total_runs']}
    - Findings Change Since Previous Audit: {trends['findings_change']}
    - Critical Findings Change: {trends['critical_change']}

    Trend analysis indicates recurring governance issues requiring continued management focus.
    """
    )

    add_section(
        sections,
        "Management Recommendations",
        """
    Management should prioritize:

    - Strengthening access governance controls
    - Enhancing remediation tracking processes
    - Improving segregation of duties oversight
    - Increasing governance monitoring activities
    - Accelerating remediation of critical findings
    """
    )

    add_section(
        sections,
        "Conclusion",
        """
    The audit identified governance and control weaknesses requiring continued remediation oversight and management attention.

    Continued improvement of governance processes, access controls, and operational monitoring activities will strengthen the overall control environment.
    """
    )

    return sections


def generate_executive_summary(
    engagement_context: dict,
    findings: list,
    metrics: dict,
    remediation_metrics: dict,
    trends: dict
):

    sections = build_executive_report_sections(
        engagement_context=engagement_context,
        findings=findings,
        metrics=metrics,
        remediation_metrics=remediation_metrics,
        trends=trends
    )

    return render_text_report(
        sections
    )