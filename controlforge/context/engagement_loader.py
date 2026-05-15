import json


def load_engagement_context(
    engagement_path
) -> dict:

    engagement_file = (
        engagement_path / "engagement.json"
    )

    if not engagement_file.exists():
        raise FileNotFoundError(
            f"Engagement configuration not found: {engagement_file}"
        )

    with open(engagement_file, "r") as file:
        return json.load(file)