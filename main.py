from tabulate import tabulate
import pandas as pd

from controlforge.ingestion.loaders import load_all_evidence

from controlforge.controls.termination_checks import (
    detect_terminated_active_accounts
)

from controlforge.controls.orphan_checks import (
    detect_orphaned_accounts
)

from controlforge.controls.dormant_checks import (
    detect_dormant_accounts
)

from controlforge.controls.mfa_checks import (
    detect_mfa_gaps
)

from controlforge.findings.findings_engine import (
    generate_terminated_user_findings,
    generate_orphaned_account_findings,
    generate_dormant_account_findings,
    generate_mfa_gap_findings
)

from controlforge.reports.exporter import export_findings


def display_findings(findings: list):
    findings_df = pd.DataFrame(findings)

    if findings_df.empty:
        print("\nNo findings detected.")
        return

    display_columns = [
        "finding_id",
        "severity",
        "control_name",
        "affected_user"
    ]

    print("\nAudit Findings Summary")
    print("======================")

    print(
        tabulate(
            findings_df[display_columns],
            headers="keys",
            tablefmt="grid",
            showindex=False
        )
    )


def main():
    print("\nControlForge Audit Engine")
    print("=========================")

    evidence = load_all_evidence()

    hr_df = evidence["hr_records"]
    ad_df = evidence["ad_accounts"]

    terminated_accounts = detect_terminated_active_accounts(hr_df, ad_df)
    terminated_findings = generate_terminated_user_findings(terminated_accounts)

    orphaned_accounts = detect_orphaned_accounts(hr_df, ad_df)
    orphaned_findings = generate_orphaned_account_findings(orphaned_accounts)

    dormant_accounts = detect_dormant_accounts(ad_df, threshold_days=90)
    dormant_findings = generate_dormant_account_findings(dormant_accounts)

    mfa_gaps = detect_mfa_gaps(ad_df)
    mfa_findings = generate_mfa_gap_findings(mfa_gaps)

    findings = (
        terminated_findings
        + orphaned_findings
        + dormant_findings
        + mfa_findings
    )

    print(f"\nTotal findings generated: {len(findings)}")

    display_findings(findings)

    export_findings(findings)


if __name__ == "__main__":
    main()