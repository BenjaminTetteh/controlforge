def preserve_existing_finding_state(
    current_findings: list,
    previous_findings: list
) -> list:

    previous_lookup = {}

    for finding in previous_findings:

        key = (
            finding.get("affected_user"),
            finding.get("control_id")
        )

        previous_lookup[key] = finding

    for finding in current_findings:

        key = (
            finding.get("affected_user"),
            finding.get("control_id")
        )

        if key in previous_lookup:

            previous = previous_lookup[key]

            finding["status"] = previous.get(
                "status",
                "Open"
            )

            finding["remediation_owner"] = (
                previous.get(
                    "remediation_owner",
                    "Unassigned"
                )
            )

            finding["remediation_due_date"] = (
                previous.get("remediation_due_date")
                or finding.get("remediation_due_date")
            )

            finding["remediation_notes"] = (
                previous.get(
                    "remediation_notes",
                    ""
                )
            )

            finding["remediation_status"] = (
                previous.get(
                    "remediation_status",
                    "Pending"
                )
            )

            finding["remediation_evidence"] = previous.get(
                "remediation_evidence",
                ""
            )

            finding["remediation_submitted_at"] = previous.get(
                "remediation_submitted_at",
                ""
            )

            finding["validated_by_auditor"] = previous.get(
                "validated_by_auditor",
                False
            )

            finding["auditor_validation_notes"] = previous.get(
                "auditor_validation_notes",
                ""
            )

            finding["validated_at"] = previous.get(
                "validated_at",
                ""
            )

            finding["closure_approved"] = previous.get(
                "closure_approved",
                False
            )

            finding["closed_at"] = previous.get(
                "closed_at",
                ""
            )

    return current_findings