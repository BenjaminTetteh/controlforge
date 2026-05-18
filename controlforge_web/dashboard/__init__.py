import re
from pathlib import Path

from flask import Blueprint, abort, render_template

from controlforge.analytics.findings_loader import (
    load_saved_findings
)

from controlforge.frameworks.governance_scorecard import (
    generate_governance_scorecard
)

from controlforge.frameworks.risk_concentration_analyzer import (
    analyze_risk_concentration
)

from controlforge.frameworks.governance_kpi_generator import (
    generate_governance_kpis
)

from controlforge.context.engagement_loader import (
    load_engagement_context
)


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


def is_safe_slug(value: str) -> bool:

    return bool(
        re.fullmatch(
            r"[a-z0-9-]+",
            value
        )
    )


@dashboard_bp.route(
    "/<client_slug>/<engagement_slug>"
)
def engagement_dashboard(
    client_slug,
    engagement_slug
):

    if (
        not is_safe_slug(client_slug)
        or not is_safe_slug(engagement_slug)
    ):
        abort(400)

    engagement_path = (
        Path("clients")
        / client_slug
        / engagement_slug
    )

    if not engagement_path.exists():
        abort(404)

    engagement_context = load_engagement_context(
        engagement_path
    )

    findings_path = (
        engagement_path
        / "findings"
    )

    findings = load_saved_findings(
        findings_path
    )

    scorecard = generate_governance_scorecard(
        framework_code="SOX",
        engagement_path=engagement_path,
        findings=findings
    )

    concentrations = analyze_risk_concentration(
        findings
    )

    trends = {
        "coverage_trend": "Stable",
        "critical_findings_trend": "Stable",
        "open_findings_trend": "Stable"
    }

    kpis = generate_governance_kpis(
        scorecard=scorecard,
        concentrations=concentrations,
        trends=trends
    )

    kpi_classes = {
        "governance_posture": get_posture_class(
            kpis["governance_posture"]
        ),
        "governance_trend": get_trend_class(
            kpis["governance_trend"]
        )
    }

    return render_template(
        "dashboard.html",
        kpis=kpis,
        engagement=engagement_context,
        kpi_classes=kpi_classes,
        concentrations=concentrations
    )

def get_posture_class(posture):

    if posture == "Strong":
        return "kpi-strong"

    if posture in ["Moderate", "Satisfactory"]:
        return "kpi-moderate"

    return "kpi-risk"


def get_trend_class(trend):

    if trend == "Improving":
        return "kpi-strong"

    if trend == "Stable":
        return "kpi-moderate"

    return "kpi-risk"