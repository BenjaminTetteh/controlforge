from controlforge.controls.registry.framework_mappings import (
    FRAMEWORK_MAPPINGS
)


def enrich_finding_with_frameworks(
    finding: dict
) -> dict:

    control_id = finding["control_id"]

    framework_mappings = FRAMEWORK_MAPPINGS.get(
        control_id,
        []
    )

    finding["framework_mappings"] = (
        framework_mappings
    )

    return finding