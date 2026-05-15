def preserve_existing_finding_state(
    current_findings: list,
    previous_findings: list
):

    previous_findings_map = {
        finding["finding_id"]: finding
        for finding in previous_findings
    }

    persistent_fields = [
        "status",
        "remediation_owner",
        "remediation_status",
        "remediation_evidence",
        "remediation_submitted_at",
        "validated_by_auditor",
        "auditor_validation_notes",
        "validated_at",
        "closure_approved",
        "closed_at"
    ]

    for finding in current_findings:

        previous = previous_findings_map.get(
            finding["finding_id"]
        )

        if not previous:
            continue

        for field in persistent_fields:

            if field in previous:

                finding[field] = previous[field]

    return current_findings