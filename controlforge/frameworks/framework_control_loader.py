from controlforge.frameworks.framework_control_mappings import (
    FRAMEWORK_CONTROL_MAPPINGS
)

from controlforge.controls.control_registry import (
    CONTROL_REGISTRY
)


def get_framework_controls(
    framework_code: str
):

    control_ids = FRAMEWORK_CONTROL_MAPPINGS.get(
        framework_code,
        []
    )

    controls = []

    for control_id in control_ids:

        control = CONTROL_REGISTRY.get(
            control_id
        )

        if control:

            controls.append(
                {
                    "control_id": control_id,
                    **control
                }
            )

    return controls