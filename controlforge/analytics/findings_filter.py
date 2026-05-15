def filter_findings(
    findings: list,
    severity: str = None,
    status: str = None,
    control: str = None
):

    filtered = findings

    if severity:

        filtered = [
            finding
            for finding in filtered
            if finding["severity"].lower()
            == severity.lower()
        ]

    if status:

        filtered = [
            finding
            for finding in filtered
            if finding["status"].lower()
            == status.lower()
        ]

    if control:

        filtered = [
            finding
            for finding in filtered
            if control.lower()
            in finding["control_name"].lower()
        ]

    return filtered