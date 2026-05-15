def get_finding_timeline(
    logs: list,
    finding_id: str
) -> list:

    timeline = []

    for event in logs:

        if event.get("event_type") != "workflow_action":
            continue

        if event.get("finding_id") != finding_id:
            continue

        timeline.append(event)

    return timeline