from controlforge.findings.frameworks import (
    enrich_finding_with_frameworks
)

from controlforge.controls.registry.control_registry import CONTROL_REGISTRY


def enrich_finding_with_control_metadata(
    finding: dict,
    control_key: str,
    engagement_context: dict
) -> dict:

    control_metadata = CONTROL_REGISTRY[control_key]

    finding["control_id"] = control_metadata["control_id"]
    finding["control_version"] = control_metadata["control_version"]
    finding["source_evidence"] = control_metadata["source_evidence"]
    finding["normalized_evidence"] = control_metadata["normalized_evidence"]

    finding["engagement_id"] = engagement_context["engagement_id"]
    finding["client_name"] = engagement_context["client_name"]
    finding["framework"] = engagement_context["framework"]
    finding["audit_period"] = engagement_context["audit_period"]

    finding = enrich_finding_with_frameworks(
        finding
    )

    return finding