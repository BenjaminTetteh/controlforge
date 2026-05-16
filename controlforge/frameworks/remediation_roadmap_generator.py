def generate_remediation_roadmap(
    priorities: list
):

    roadmap = []

    phase = 1

    remediation_actions = {

        "Identity and Access Management": (
            "Enable MFA enforcement and "
            "remediate privileged access weaknesses."
        ),

        "Access Governance": (
            "Resolve segregation of duties "
            "conflicts and strengthen "
            "access governance controls."
        ),

        "Identity Lifecycle Management": (
            "Improve identity lifecycle "
            "governance and inactive "
            "account remediation processes."
        )
    }

    for item in priorities:

        domain = item["domain"]

        action = remediation_actions.get(
            domain,
            "Perform governance remediation activities."
        )

        roadmap.append(
            {
                "phase": phase,
                "domain": domain,
                "action": action
            }
        )

        phase += 1

    return roadmap