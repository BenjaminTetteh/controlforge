from tabulate import tabulate


def display_engagement_context(
    context: dict
):

    print("\nEngagement Context")
    print("==================")

    table = [
        ["Client", context["client_name"]],
        ["Engagement ID", context["engagement_id"]],
        ["Framework", context["framework"]],
        ["Audit Period", context["audit_period"]],
        ["Auditor", context["auditor_name"]],
        ["Execution Timestamp", context["execution_timestamp"]]
    ]

    print(
        tabulate(
            table,
            headers=["Field", "Value"],
            tablefmt="grid"
        )
    )