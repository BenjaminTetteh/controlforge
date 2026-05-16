from collections import defaultdict


def calculate_priority_score(
    critical: int,
    high: int,
    medium: int
):

    return (
        (critical * 5)
        + (high * 3)
        + medium
    )


def generate_remediation_priorities(
    concentrations: list
):

    priorities = []

    for item in concentrations:

        score = calculate_priority_score(
            item["critical"],
            item["high"],
            item["medium"]
        )

        priorities.append(
            {
                "domain": item["domain"],
                "risk_level": item["risk_level"],
                "priority_score": score
            }
        )

    priorities = sorted(
        priorities,
        key=lambda x: x["priority_score"],
        reverse=True
    )

    return priorities