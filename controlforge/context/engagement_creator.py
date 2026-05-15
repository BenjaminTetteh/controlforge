import json
from pathlib import Path

from controlforge.context.engagement_templates import (
    create_evidence_templates
)


def create_engagement(
    client_slug: str,
    engagement_slug: str,
    client_name: str,
    engagement_id: str,
    framework: str,
    audit_period: str,
    auditor_name: str
):

    engagement_path = (
        Path("clients")
        / client_slug
        / engagement_slug
    )

    folders = [
        "findings",
        "metadata",
        "reports",
        "evidence",
        "history",
        "logs"
    ]

    engagement_path.mkdir(
        parents=True,
        exist_ok=True
    )

    for folder in folders:
        (engagement_path / folder).mkdir(
            exist_ok=True
        )

    create_evidence_templates(
        framework=framework,
        evidence_path=engagement_path / "evidence"
    )

    engagement_config = {
        "client_name": client_name,
        "engagement_id": engagement_id,
        "framework": framework,
        "audit_period": audit_period,
        "auditor_name": auditor_name
    }

    engagement_file = (
        engagement_path / "engagement.json"
    )

    with open(engagement_file, "w") as file:
        json.dump(
            engagement_config,
            file,
            indent=4
        )

    return engagement_path