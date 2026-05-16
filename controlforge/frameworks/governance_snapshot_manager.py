import json

from datetime import datetime

#
def save_governance_snapshot(
    engagement_path,
    scorecard: dict
):

    snapshot_dir = (
        engagement_path
        / "governance_snapshots"
    )

    snapshot_dir.mkdir(
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    snapshot_file = (
        snapshot_dir
        / f"{timestamp}.json"
    )

    with open(snapshot_file, "w") as file:
        json.dump(
            scorecard,
            file,
            indent=4
        )

    return snapshot_file

# This function can be used to load the previous snapshot for trend analysis
def load_previous_snapshot(
    engagement_path
):

    snapshot_dir = (
        engagement_path
        / "governance_snapshots"
    )

    if not snapshot_dir.exists():
        return None

    snapshot_files = sorted(
        snapshot_dir.glob("*.json")
    )

    if len(snapshot_files) < 2:
        return None

    previous_snapshot = snapshot_files[-2]

    with open(previous_snapshot, "r") as file:
        return json.load(file)