from controlforge.frameworks.framework_control_loader import (
    get_framework_controls
)

from controlforge.controls.implemented_control_loader import (
    load_implemented_controls
)

from controlforge.frameworks.maturity_scorer import (
    score_maturity
)

def analyze_control_coverage(
    framework_code: str,
    engagement_path
):

    mapped_controls = get_framework_controls(
        framework_code
    )

    mapped_ids = {
        control["control_id"]
        for control in mapped_controls
    }

    implemented_ids = set(
        load_implemented_controls(
            engagement_path
        )
    )

    implemented_controls = (
        mapped_ids & implemented_ids
    )

    coverage_percent = 0

    if mapped_ids:
        coverage_percent = round(
            (
                len(implemented_controls)
                / len(mapped_ids)
            ) * 100,
            2
        )

        maturity = score_maturity(
            coverage_percent
        ) 

    return {
        "framework": framework_code,
        "mapped_controls": len(mapped_ids),
        "implemented_controls": len(
            implemented_controls
        ),
        "coverage_percent": coverage_percent,
        "maturity_level": maturity["maturity_level"],
        "governance_posture": maturity["governance_posture"]
    }