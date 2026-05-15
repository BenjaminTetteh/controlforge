from pathlib import Path


def discover_engagements():

    clients_dir = Path("clients")

    if not clients_dir.exists():
        return []

    engagements = []

    for client_dir in clients_dir.iterdir():

        if not client_dir.is_dir():
            continue

        for engagement_dir in client_dir.iterdir():

            if not engagement_dir.is_dir():
                continue

            engagement_file = (
                engagement_dir
                / "engagement.json"
            )

            if engagement_file.exists():

                engagements.append(
                    {
                        "client": client_dir.name,
                        "engagement": engagement_dir.name
                    }
                )

    return engagements