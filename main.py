import argparse

from datetime import datetime

from tabulate import tabulate
import pandas as pd

from controlforge.context.engagement_context import EngagementContext
from controlforge.reports.engagement_report import display_engagement_context

from controlforge.workspace.workspace_manager import WorkspaceManager

from controlforge.ingestion.loaders import load_all_evidence
from controlforge.ingestion.evidence_integrity import generate_evidence_metadata

from controlforge.controls.termination_checks import detect_terminated_active_accounts
from controlforge.controls.orphan_checks import detect_orphaned_accounts
from controlforge.controls.dormant_checks import detect_dormant_accounts
from controlforge.controls.mfa_checks import detect_mfa_gaps
from controlforge.controls.sod_checks import detect_sod_conflicts

from controlforge.findings.findings_engine import (
    generate_terminated_user_findings,
    generate_orphaned_account_findings,
    generate_dormant_account_findings,
    generate_mfa_gap_findings,
    generate_sod_findings
)

from controlforge.findings.remediation_tracker import initialize_remediation_fields
from controlforge.findings.state_manager import preserve_existing_finding_state
from controlforge.findings.finding_aging import detect_overdue_findings

from controlforge.findings.workflow_actions import (
    assign_finding_owner,
    submit_remediation,
    validate_finding,
    close_finding
)

from controlforge.history.history_manager import AuditHistoryManager
from controlforge.history.recurring_findings import (
    load_previous_findings,
    detect_recurring_findings
)

from controlforge.logging.execution_logger import ExecutionLogger

from controlforge.reports.exporter import (
    export_findings,
    export_audit_summary,
    export_text_report
)
from controlforge.reports.audit_summary import AuditSummary
from controlforge.reports.evidence_manifest import export_evidence_manifest

from controlforge.analytics.findings_filter import (
    filter_findings
)

from controlforge.analytics.metrics import (
    calculate_finding_metrics
)

from controlforge.analytics.findings_loader import (
    load_saved_findings
)

from controlforge.analytics.trends import (
    calculate_trends
)

from controlforge.history.finding_timeline import (
    get_finding_timeline
)

from controlforge.analytics.remediation_metrics import (
    calculate_remediation_metrics
)

from controlforge.reports.executive_report import (
    generate_executive_summary,
    build_executive_report_sections
)

from controlforge.analytics.remediation_metrics import (
    calculate_remediation_metrics
)

from controlforge.analytics.trends import (
    calculate_trends
)

from controlforge.reports.pdf_renderer import (
    export_sections_to_pdf
)

from controlforge.reports.chart_renderer import (
    generate_findings_severity_chart
)

from pathlib import Path

from controlforge.context.engagement_loader import (
    load_engagement_context
)

from controlforge.context.engagement_discovery import (
    discover_engagements
)

from controlforge.context.engagement_creator import (
    create_engagement
)

from controlforge.frameworks.framework_loader import (
    get_framework_metadata
)

from controlforge.frameworks.framework_control_loader import (
    get_framework_controls
)

from controlforge.frameworks.control_coverage_analyzer import (
    analyze_control_coverage
)

from controlforge.controls.implemented_control_manager import (
    enable_control,
    disable_control
)

from controlforge.frameworks.governance_scorecard import (
    generate_governance_scorecard
)

from controlforge.frameworks.governance_trend_analyzer import (
    analyze_governance_trends
)

from controlforge.frameworks.governance_snapshot_manager import (
    save_governance_snapshot
)

from controlforge.frameworks.governance_snapshot_manager import (
    save_governance_snapshot,
    load_previous_snapshot
)

from controlforge.frameworks.risk_concentration_analyzer import (
    analyze_risk_concentration
)


# Define the evidence files to be loaded
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


def display_findings(findings: list, limit: int = 20):
    findings_df = pd.DataFrame(findings)

    if findings_df.empty:
        print("\nNo findings detected.")
        return

    display_columns = [
        "finding_id",
        "severity",
        "control_name",
        "affected_user",
        "source_system",
        "status",
        "remediation_owner"
    ]

    print("\nAudit Findings Summary")
    print("======================")

    findings_df = findings_df.head(limit)

    print(
        tabulate(
            findings_df[display_columns],
            headers="keys",
            tablefmt="grid",
            showindex=False
        )
    )


def display_recurring_findings(recurring_findings: list, limit: int = 20):

    if not recurring_findings:
        print("\nNo recurring findings detected.")
        return

    print("\nRecurring Findings Detected")
    print("===========================")

    recurring_findings = recurring_findings[:limit]

    rows = []

    for finding in recurring_findings:

        rows.append([
            finding["finding_id"],
            finding["affected_user"],
            finding["control_name"],
            finding["severity"]
        ])

    print(
        tabulate(
            rows,
            headers=[
                "Finding ID",
                "Affected User",
                "Control",
                "Severity"
            ],
            tablefmt="grid"
        )
    )


def display_overdue_findings(overdue_findings: list):

    if not overdue_findings:
        print("\nNo overdue findings detected.")
        return

    print("\nOverdue Findings")
    print("================")

    rows = []

    for finding in overdue_findings:
        rows.append([
            finding["finding_id"],
            finding["affected_user"],
            finding["control_name"],
            finding["severity"],
            finding["days_overdue"]
        ])

    print(
        tabulate(
            rows,
            headers=[
                "Finding ID",
                "Affected User",
                "Control",
                "Severity",
                "Days Overdue"
            ],
            tablefmt="grid"
        )
    )


def build_engagement_context(
    client_slug: str,
    engagement_slug: str
):
    engagement_path = (
        Path("clients")
        / client_slug
        / engagement_slug
    )

    engagement_context = load_engagement_context(
        engagement_path
    )

    engagement_context["framework_metadata"] = get_framework_metadata(
        engagement_context["framework"]
    )

    engagement_context["execution_timestamp"] = (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    return engagement_context


def build_workspace(engagement_context: dict):
    workspace = WorkspaceManager(
        client_name=engagement_context["client_name"],
        engagement_id=engagement_context["engagement_id"]
    )

    workspace.create_workspace()

    return workspace.get_paths()


def handle_workflow_actions(
    args,
    paths: dict,
    engagement_context: dict,
    execution_logger
) -> bool:

    if args.command == "assign-owner":

        assign_finding_owner(
            findings_path=paths["findings"],
            finding_id=args.finding_id,
            owner=args.owner
        )

        workflow_event = execution_logger.create_workflow_event(
            engagement_context=engagement_context,
            action="assign_owner",
            finding_id=args.finding_id,
            performed_by=engagement_context["auditor_name"]
        )

        execution_logger.log_execution(workflow_event)

        return True

    if args.command == "submit-remediation":

        submit_remediation(
            findings_path=paths["findings"],
            finding_id=args.finding_id,
            remediation_evidence=args.remediation_evidence
        )

        workflow_event = execution_logger.create_workflow_event(
            engagement_context=engagement_context,
            action="submit_remediation",
            finding_id=args.finding_id,
            performed_by=engagement_context["auditor_name"]
        )

        execution_logger.log_execution(workflow_event)

        return True

    if args.command == "validate-finding":

        validate_finding(
            findings_path=paths["findings"],
            finding_id=args.finding_id,
            validation_notes=args.validation_notes
        )

        workflow_event = execution_logger.create_workflow_event(
            engagement_context=engagement_context,
            action="validate_finding",
            finding_id=args.finding_id,
            performed_by=engagement_context["auditor_name"]
        )

        execution_logger.log_execution(workflow_event)

        return True

    if args.command == "close-finding":

        close_finding(
            findings_path=paths["findings"],
            finding_id=args.finding_id
        )

        workflow_event = execution_logger.create_workflow_event(
            engagement_context=engagement_context,
            action="close_finding",
            finding_id=args.finding_id,
            performed_by=engagement_context["auditor_name"]
        )

        execution_logger.log_execution(workflow_event)

        return True

    return False


def parse_args():
    parser = argparse.ArgumentParser(
        description="ControlForge IT Audit Automation Engine"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    run_audit_parser = subparsers.add_parser(
        "run-audit",
        help="Run the full audit engine"
    )

    run_audit_parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Limit the number of findings displayed in the CLI"
    )

    run_audit_parser.add_argument(
        "--severity",
        type=str,
        help="Filter findings by severity"
    )

    run_audit_parser.add_argument(
        "--status",
        type=str,
        help="Filter findings by workflow status"
    )

    run_audit_parser.add_argument(
        "--control",
        type=str,
        help="Filter findings by control name"
    )

    assign_owner_parser = subparsers.add_parser(
        "assign-owner",
        help="Assign a remediation owner to a finding"
    )
    assign_owner_parser.add_argument("finding_id")
    assign_owner_parser.add_argument("owner")

    submit_parser = subparsers.add_parser(
        "submit-remediation",
        help="Submit remediation evidence for a finding"
    )
    submit_parser.add_argument("finding_id")
    submit_parser.add_argument("remediation_evidence")

    validate_parser = subparsers.add_parser(
        "validate-finding",
        help="Validate remediation evidence for a finding"
    )
    validate_parser.add_argument("finding_id")
    validate_parser.add_argument("validation_notes")

    close_parser = subparsers.add_parser(
        "close-finding",
        help="Close a validated finding"
    )
    close_parser.add_argument("finding_id")

    metrics_parser = subparsers.add_parser(
        "metrics",
        help="Display governance and audit metrics"
    )

    metrics_parser.add_argument(
        "--severity",
        type=str,
        help="Filter metrics by severity"
    )

    metrics_parser.add_argument(
        "--status",
        type=str,
        help="Filter metrics by workflow status"
    )

    metrics_parser.add_argument(
        "--control",
        type=str,
        help="Filter metrics by control name"
    )

    subparsers.add_parser(
        "trends",
        help="Display audit trend analytics"
    )

    subparsers.add_parser(
        "remediation-metrics",
        help="Display remediation lifecycle metrics"
    )

    subparsers.add_parser(
        "list-engagements",
        help="List available client engagements"
    )

    subparsers.add_parser(
        "framework-controls",
        help="Display controls mapped to the selected framework"
    )

    subparsers.add_parser(
        "control-coverage",
        help="Display framework control coverage analytics"
    )

    subparsers.add_parser(
        "governance-scorecard",
        help="Display executive governance scorecard"
    )

    subparsers.add_parser(
        "governance-trends",
        help="Display governance posture trends"
    )

    subparsers.add_parser(
        "risk-concentration",
        help="Display governance risk concentration by domain"
    )

    executive_report_parser = subparsers.add_parser(
        "executive-report",
        help="Generate executive governance summary report"
    )

    executive_report_parser.add_argument(
        "--pdf",
        action="store_true",
        help="Export executive report as PDF"
    )

    timeline_parser = subparsers.add_parser(
        "finding-history",
        help="Display workflow history for a finding"
    )

    parser.add_argument(
    "--client",
    default="meridian-financial-group",
    help="Client slug"
    )

    parser.add_argument(
        "--engagement",
        default="2026-q2-sox-itgc",
        help="Engagement slug"
    )

    create_parser = subparsers.add_parser(
    "create-engagement",
        help="Create a new client engagement workspace"
    )

    create_parser.add_argument("--client", required=True)
    create_parser.add_argument("--engagement", required=True)
    create_parser.add_argument("--client-name", required=True)
    create_parser.add_argument("--engagement-id", required=True)
    create_parser.add_argument("--framework", required=True)
    create_parser.add_argument("--audit-period", required=True)
    create_parser.add_argument("--auditor-name", required=True)

    enable_control_parser = subparsers.add_parser(
        "enable-control",
        help="Mark a control as implemented for the selected engagement"
    )
    enable_control_parser.add_argument("control_id")

    disable_control_parser = subparsers.add_parser(
        "disable-control",
        help="Mark a control as not implemented for the selected engagement"
    )
    disable_control_parser.add_argument("control_id")

    timeline_parser.add_argument("finding_id")

    return parser.parse_args()


def display_metrics(metrics: dict):

    print("\nGovernance Metrics")
    print("==================")

    rows = [
        ["Generated At", metrics["generated_at"]],
        ["Total Findings", metrics["total_findings"]],
        ["Open Findings", metrics["open_findings"]],
        ["Closed Findings", metrics["closed_findings"]],
        ["Critical Findings", metrics["critical_findings"]],
        ["High Findings", metrics["high_findings"]],
        ["Medium Findings", metrics["medium_findings"]],
        ["Low Findings", metrics["low_findings"]],
        ["Unassigned Findings", metrics["unassigned_findings"]]
    ]

    print(
        tabulate(
            rows,
            headers=["Metric", "Value"],
            tablefmt="grid"
        )
    )


def display_trends(trends: dict):

    print("\nAudit Trend Analytics")
    print("=====================")

    rows = [
        ["Total Audit Runs", trends["total_runs"]],
        ["Latest Total Findings", trends["latest_total_findings"]],
        ["Previous Total Findings", trends["previous_total_findings"]],
        ["Findings Change", trends["findings_change"]],
        ["Latest Critical Findings", trends["latest_critical_findings"]],
        ["Previous Critical Findings", trends["previous_critical_findings"]],
        ["Critical Findings Change", trends["critical_change"]]
    ]

    print(
        tabulate(
            rows,
            headers=["Metric", "Value"],
            tablefmt="grid"
        )
    )

def display_finding_timeline(
    timeline: list,
    finding_id: str
):

    if not timeline:
        print(f"\nNo workflow history found for {finding_id}.")
        return

    print(f"\nWorkflow Timeline for {finding_id}")
    print("==============================")

    rows = []

    for event in timeline:

        rows.append([
            event.get("timestamp"),
            event.get("action"),
            event.get("performed_by"),
            event.get("client_name"),
            event.get("engagement_id")
        ])

    print(
        tabulate(
            rows,
            headers=[
                "Timestamp",
                "Action",
                "Performed By",
                "Client",
                "Engagement"
            ],
            tablefmt="grid"
        )
    )


def display_remediation_metrics(metrics: dict):

    print("\nRemediation Metrics")
    print("===================")

    rows = [
        ["Total Findings", metrics["total_findings"]],
        ["Open Findings", metrics["open_findings"]],
        ["Closed Findings", metrics["closed_findings"]],
        ["Overdue Findings", metrics["overdue_findings"]],
        [
            "Average Closure Time",
            f"{metrics['average_closure_time_days']} days"
        ]
    ]

    print(
        tabulate(
            rows,
            headers=["Metric", "Value"],
            tablefmt="grid"
        )
    )


def display_engagement_inventory(
    engagements: list
):

    if not engagements:
        print("\nNo engagements found.")
        return

    rows = []

    for engagement in engagements:
        rows.append([
            engagement["client"],
            engagement["engagement"]
        ])

    print("\nAvailable Engagements")
    print("=====================")

    print(
        tabulate(
            rows,
            headers=[
                "Client",
                "Engagement"
            ],
            tablefmt="grid"
        )
    )


def display_framework_controls(
    framework: str,
    controls: list
):

    if not controls:
        print(f"\nNo controls mapped for {framework}.")
        return

    rows = []

    for control in controls:
        rows.append([
            control["control_id"],
            control["name"],
            control["domain"],
            control["severity"]
        ])

    print(f"\nControls mapped to {framework}")
    print("==============================")

    print(
        tabulate(
            rows,
            headers=[
                "Control ID",
                "Control Name",
                "Domain",
                "Severity"
            ],
            tablefmt="grid"
        )
    )


def display_control_coverage(
    coverage: dict
):

    print("\nControl Coverage Analytics")
    print("==========================")

    rows = [
        ["Framework", coverage["framework"]],
        ["Mapped Controls", coverage["mapped_controls"]],
        ["Implemented Controls", coverage["implemented_controls"]],
        ["Coverage", f"{coverage['coverage_percent']}%"],
        ["Maturity Level", coverage["maturity_level"]],
        ["Governance Posture", coverage["governance_posture"]]
    ]

    print(
        tabulate(
            rows,
            headers=["Metric", "Value"],
            tablefmt="grid"
        )
    )


def display_governance_scorecard(
    scorecard: dict
):

    print("\nGovernance Scorecard")
    print("====================")

    rows = [
        ["Framework", scorecard["framework"]],
        ["Coverage", f"{scorecard['coverage_percent']}%"],
        ["Maturity", scorecard["maturity_level"]],
        ["Governance Posture", scorecard["governance_posture"]],
        ["Critical Findings", scorecard["critical_findings"]],
        ["Open Findings", scorecard["open_findings"]],
        ["Total Findings", scorecard["total_findings"]]
    ]

    print(
        tabulate(
            rows,
            headers=["Metric", "Value"],
            tablefmt="grid"
        )
    )


def display_governance_trends(
    trends: dict
):

    print("\nGovernance Trend Analysis")
    print("=========================")

    rows = [
        ["Coverage Trend", trends["coverage_trend"]],
        ["Critical Findings Trend", trends["critical_findings_trend"]],
        ["Open Findings Trend", trends["open_findings_trend"]]
    ]

    print(
        tabulate(
            rows,
            headers=["Metric", "Trend"],
            tablefmt="grid"
        )
    )


def display_risk_concentration(
    concentrations: list
):

    if not concentrations:
        print("\nNo risk concentration data available.")
        return

    rows = []

    for item in concentrations:
        rows.append([
            item["domain"],
            item["critical"],
            item["high"],
            item["medium"],
            item["risk_level"]
        ])

    print("\nGovernance Risk Concentration")
    print("=============================")

    print(
        tabulate(
            rows,
            headers=[
                "Domain",
                "Critical",
                "High",
                "Medium",
                "Risk Level"
            ],
            tablefmt="grid"
        )
    )


def main():
    args = parse_args()
    if args.command == "create-engagement":

        engagement_path = create_engagement(
            client_slug=args.client,
            engagement_slug=args.engagement,
            client_name=args.client_name,
            engagement_id=args.engagement_id,
            framework=args.framework,
            audit_period=args.audit_period,
            auditor_name=args.auditor_name
        )

        print("\nEngagement created successfully:")
        print(f"- {engagement_path}")

        return
    
    audit_summary = AuditSummary()

    engagement_context = build_engagement_context(
        client_slug=args.client,
        engagement_slug=args.engagement
    )
    paths = build_workspace(engagement_context)

    history_manager = AuditHistoryManager(
        paths["history"]
    )
    
    execution_logger = ExecutionLogger(
        paths["logs"]
    )

    if args.command == "risk-concentration":

        findings = load_saved_findings(
            paths["findings"]
        )

        concentrations = analyze_risk_concentration(
            findings
        )

        display_risk_concentration(
            concentrations
        )

        return

    if args.command == "governance-trends":

        findings = load_saved_findings(
            paths["findings"]
        )

        current_scorecard = generate_governance_scorecard(
            framework_code=engagement_context["framework"],
            engagement_path=paths["base"],
            findings=findings
        )

        previous_scorecard = load_previous_snapshot(
            paths["base"]
        )

        if previous_scorecard is None:
            print("\nNot enough governance snapshot history to calculate trends.")
            return

        trends = analyze_governance_trends(
            current_scorecard=current_scorecard,
            previous_scorecard=previous_scorecard
        )

        display_governance_trends(
            trends
        )

        return

    if args.command == "governance-scorecard":

        findings = load_saved_findings(
            paths["findings"]
        )

        scorecard = generate_governance_scorecard(
            framework_code=engagement_context["framework"],
            engagement_path=paths["base"],
            findings=findings
        )

        display_governance_scorecard(
            scorecard
        )

        snapshot_file = save_governance_snapshot(
            engagement_path=paths["base"],
            scorecard=scorecard
        )

        print("\nGovernance snapshot saved:")
        print(f"- {snapshot_file}")

        return

    if args.command == "enable-control":

        enable_control(
            engagement_path=paths["base"],
            control_id=args.control_id
        )

        print(f"\nControl enabled: {args.control_id}")

        return


    if args.command == "disable-control":

        disable_control(
            engagement_path=paths["base"],
            control_id=args.control_id
        )

        print(f"\nControl disabled: {args.control_id}")

        return

    if args.command == "control-coverage":

        coverage = analyze_control_coverage(
            framework_code=engagement_context["framework"],
            engagement_path=paths["base"]
        )

        display_control_coverage(
            coverage
        )

        return

    if args.command == "framework-controls":

        controls = get_framework_controls(
            engagement_context["framework"]
        )

        display_framework_controls(
            engagement_context["framework"],
            controls
        )

        return

    if args.command == "list-engagements":

        engagements = discover_engagements()

        display_engagement_inventory(
            engagements
        )

        return

    if args.command == "metrics":

        findings = load_saved_findings(
            paths["findings"]
        )

        filtered_findings = filter_findings(
            findings=findings,
            severity=args.severity,
            status=args.status,
            control=args.control
        )

        metrics = calculate_finding_metrics(
            filtered_findings
        )

        display_metrics(metrics)

        return
    
    if args.command == "trends":

        audit_history = history_manager.load_history()

        trends = calculate_trends(
            audit_history
        )

        display_trends(trends)

        return
    
    if args.command == "remediation-metrics":

        findings = load_saved_findings(
            paths["findings"]
        )

        metrics = calculate_remediation_metrics(
            findings
        )

        display_remediation_metrics(
            metrics
        )

        return
    
    if args.command == "executive-report":

        findings = load_saved_findings(
            paths["findings"]
        )

        metrics = calculate_finding_metrics(
            findings
        )

        severity_chart = generate_findings_severity_chart(
            metrics=metrics,
            output_path=paths["reports"]
        )

        remediation_metrics = calculate_remediation_metrics(
            findings
        )

        audit_history = history_manager.load_history()

        trends = calculate_trends(
            audit_history
        )

        report = generate_executive_summary(
            engagement_context=engagement_context,
            findings=findings,
            metrics=metrics,
            remediation_metrics=remediation_metrics,
            trends=trends
        )

        print(report)

        export_text_report(
            report_text=report,
            output_path=paths["reports"],
            filename="executive_report.txt"
        )

    if getattr(args, "pdf", False):

        sections = build_executive_report_sections(
            engagement_context=engagement_context,
            findings=findings,
            metrics=metrics,
            remediation_metrics=remediation_metrics,
            trends=trends
        )

        export_sections_to_pdf(
            sections=sections,
            output_path=paths["reports"],
            filename="executive_report.pdf",
            chart_paths=[severity_chart]
        )

        return

    if args.command == "finding-history":

        logs = execution_logger.load_logs()

        timeline = get_finding_timeline(
            logs=logs,
            finding_id=args.finding_id
        )

        display_finding_timeline(
            timeline=timeline,
            finding_id=args.finding_id
        )

        return

    action_handled = handle_workflow_actions(
        args,
        paths,
        engagement_context,
        execution_logger
    )

    if args.command not in [None, "run-audit"]:
        return

    if action_handled:
        return

    previous_findings = load_previous_findings(
        paths["findings"]
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

    findings = initialize_remediation_fields(findings)

    findings = preserve_existing_finding_state(
        current_findings=findings,
        previous_findings=previous_findings
    )

    filtered_findings = filter_findings(
        findings=findings,
        severity=args.severity,
        status=args.status,
        control=args.control
    )

    recurring_findings = detect_recurring_findings(
        current_findings=findings,
        previous_findings=previous_findings
    )

    overdue_findings = detect_overdue_findings(
        findings
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

    execution_event = execution_logger.create_execution_event(
        engagement_context=engagement_context,
        controls_executed=controls_executed,
        total_findings=summary["total_findings"]
    )

    execution_logger.log_execution(
        execution_event
    )

    export_audit_summary(
        summary,
        paths["reports"]
    )

    history_manager.append_audit_run(
        summary
    )

    display_findings(
        filtered_findings,
        limit=args.limit if args.command == "run-audit" else 20
    )

    display_recurring_findings(
        recurring_findings,
        limit=args.limit if args.command == "run-audit" else 20
    )

    display_overdue_findings(
        overdue_findings
    )

    export_findings(
        findings,
        paths["findings"]
    )


if __name__ == "__main__":
    main()