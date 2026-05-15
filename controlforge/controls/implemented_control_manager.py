import json


def save_implemented_controls(
    engagement_path,
    controls: list
):

    controls_file = (
        engagement_path
        / "implemented_controls.json"
    )

    with open(controls_file, "w") as file:
        json.dump(
            sorted(set(controls)),
            file,
            indent=4
        )


def enable_control(
    engagement_path,
    control_id: str
):

    controls_file = (
        engagement_path
        / "implemented_controls.json"
    )

    if controls_file.exists():
        with open(controls_file, "r") as file:
            controls = json.load(file)
    else:
        controls = []

    controls.append(control_id)

    save_implemented_controls(
        engagement_path,
        controls
    )


def disable_control(
    engagement_path,
    control_id: str
):

    controls_file = (
        engagement_path
        / "implemented_controls.json"
    )

    if controls_file.exists():
        with open(controls_file, "r") as file:
            controls = json.load(file)
    else:
        controls = []

    controls = [
        control
        for control in controls
        if control != control_id
    ]

    save_implemented_controls(
        engagement_path,
        controls
    )