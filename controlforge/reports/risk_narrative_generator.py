def generate_risk_concentration_narrative(
    concentrations: list
):

    if not concentrations:
        return (
            "No governance risk concentration "
            "data was available."
        )

    sorted_domains = sorted(
        concentrations,
        key=lambda x: (
            x["critical"] * 5
            + x["high"] * 3
            + x["medium"]
        ),
        reverse=True
    )

    top_domains = [
        item["domain"]
        for item in sorted_domains[:2]
    ]

    domain_text = ", followed by ".join(
        top_domains
    )

    return (
        "Risk concentration analysis indicates "
        "the highest governance exposure exists "
        f"within {domain_text}. "
        "Management attention should prioritize "
        "remediation activities within these "
        "domains to reduce operational and "
        "compliance risk exposure."
    )