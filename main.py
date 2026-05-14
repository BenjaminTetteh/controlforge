from tabulate import tabulate
import pandas as pd

from controlforge.context.engagement_context import EngagementContext
from controlforge.reports.engagement_report import display_engagement_context

from controlforge.workspace.workspace_manager import (
    WorkspaceManager
)

from controlforge.ingestion.loaders import load_all_evidence
from controlforge.ingestion.evidence_integrity import (
    generate_evidence_metadata
)

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
from controlforge.controls.sod_checks import (
    detect_sod_conflicts
)

from controlforge.findings.findings_engine import (
    generate_terminated_user_findings,
    generate_orphaned_account_findings,
    generate_dormant_account_findings,
    generate_mfa_gap_findings,
    generate_sod_findings
)

from controlforge.reports.exporter import (
    export_findings,
    export_audit_summary
)
from controlforge.reports.audit_summary import AuditSummary
from controlforge.reports.evidence_manifest import (
    export_evidence_manifest
)

from controlforge.history.history_manager import (
    AuditHistoryManager
)


EVIDENCE_FILES = [
    "hr_records.csv",
    "ad_accounts.csv",
    "role_assignments.csv",
    "sod_rules.csv"
]


def display_audit_summary(summary: dict):
    print("\nAudit Run Summary")
    print("=================")

    summary_table = [
        ["Audit Timestamp", summary["audit_timestamp"]],
        ["Controls Executed", summary["controls_executed"]],
        ["Total Findings", summary["total_findings"]],
        ["Critical Findings", summary["critical_findings"]],
        ["High Findings", summary["high_findings"]],
        ["Medium Findings", summary["medium_findings"]],
        ["Low Findings", summary["low_findings"]],
        ["Execution Time", f"{summary['execution_time_seconds']} seconds"],
    ]

    print(
        tabulate(
            summary_table,
            headers=["Metric", "Value"],
            tablefmt="grid"
        )
    )


def display_evidence_metadata(evidence_metadata: list):
    print("\nEvidence Integrity Summary")
    print("==========================")

    display_rows = []

    for item in evidence_metadata:
        display_rows.append([
            item["file_name"],
            item["row_count"],
            item["file_size_bytes"],
            item["sha256"][:12] + "..."
        ])

    print(
        tabulate(
            display_rows,
            headers=[
                "Evidence File",
                "Rows",
                "Size Bytes",
                "SHA256 Preview"
            ],
            tablefmt="grid"
        )
    )


def display_findings(findings: list):
    findings_df = pd.DataFrame(findings)

    if findings_df.empty:
        print("\nNo findings detected.")
        return

    display_columns = [
        "finding_id",
        "severity",
        "control_name",
        "affected_user",
        "source_system"
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

    audit_summary = AuditSummary()

    engagement = EngagementContext(
        client_name="Meridian Financial Group",
        engagement_id="2026-Q2-SOX-ITGC",
        framework="SOX",
        audit_period="Q2 2026",
        auditor_name="Benjamin Tetteh"
    )

    engagement_context = engagement.to_dict()

    workspace = WorkspaceManager(
        client_name=engagement_context["client_name"],
        engagement_id=engagement_context["engagement_id"]
    )

    workspace.create_workspace()

    paths = workspace.get_paths()

    history_manager = AuditHistoryManager(
        paths["history"]
    )

    print("\nControlForge Audit Engine")
    print("=========================")

    display_engagement_context(engagement_context)

    evidence_metadata = []

    for filename in EVIDENCE_FILES:
        metadata = generate_evidence_metadata(filename)
        evidence_metadata.append(metadata)

    display_evidence_metadata(evidence_metadata)

    export_evidence_manifest(
        evidence_metadata,
        paths["metadata"]
    )

    evidence = load_all_evidence()

    hr_df = evidence["hr_records"]
    ad_df = evidence["ad_accounts"]
    role_df = evidence["role_assignments"]
    sod_rules_df = evidence["sod_rules"]

    terminated_accounts = detect_terminated_active_accounts(hr_df, ad_df)
    terminated_findings = generate_terminated_user_findings(
        terminated_accounts,
        engagement_context
    )

    orphaned_accounts = detect_orphaned_accounts(hr_df, ad_df)
    orphaned_findings = generate_orphaned_account_findings(
        orphaned_accounts,
        engagement_context
    )

    dormant_accounts = detect_dormant_accounts(
        ad_df,
        threshold_days=90
    )

    dormant_findings = generate_dormant_account_findings(
        dormant_accounts,
        engagement_context
    )

    mfa_gaps = detect_mfa_gaps(ad_df)

    mfa_findings = generate_mfa_gap_findings(
        mfa_gaps,
        engagement_context
    )

    sod_conflicts = detect_sod_conflicts(
        role_df,
        sod_rules_df
    )

    sod_findings = generate_sod_findings(
        sod_conflicts,
        engagement_context
    )

    findings = (
        terminated_findings
        + orphaned_findings
        + dormant_findings
        + mfa_findings
        + sod_findings
    )

    controls_executed = 5

    summary = audit_summary.generate_summary(
        findings=findings,
        controls_executed=controls_executed
    )

    summary.update({
        "client_name": engagement_context["client_name"],
        "engagement_id": engagement_context["engagement_id"],
        "framework": engagement_context["framework"],
        "audit_period": engagement_context["audit_period"],
        "auditor_name": engagement_context["auditor_name"]
    })

    display_audit_summary(summary)

    export_audit_summary(
        summary,
        paths["reports"]
    )

    history_manager.append_audit_run(
        summary
    )

    display_findings(findings)

    export_findings(
        findings,
        paths["findings"]
    )


if __name__ == "__main__":
    main()