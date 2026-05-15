import json


def load_implemented_controls(
    engagement_path
):

    controls_file = (
        engagement_path
        / "implemented_controls.json"
    )

    if not controls_file.exists():
        return []

    with open(controls_file, "r") as file:
        return json.load(file)