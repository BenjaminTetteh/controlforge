import json
from datetime import datetime


class ExecutionLogger:

    def __init__(
        self,
        logs_path
    ):

        self.logs_file = (
            logs_path / "execution_log.json"
        )

    def load_logs(self):

        if not self.logs_file.exists():
            return []

        with open(self.logs_file, "r") as file:
            return json.load(file)

    def log_execution(
        self,
        execution_event: dict
    ):

        logs = self.load_logs()

        logs.append(execution_event)

        with open(self.logs_file, "w") as file:
            json.dump(
                logs,
                file,
                indent=4
            )

    def create_execution_event(
        self,
        engagement_context: dict,
        controls_executed: int,
        total_findings: int
    ) -> dict:

        return {
            "execution_timestamp": (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            ),
            "client_name": (
                engagement_context["client_name"]
            ),
            "engagement_id": (
                engagement_context["engagement_id"]
            ),
            "framework": (
                engagement_context["framework"]
            ),
            "audit_period": (
                engagement_context["audit_period"]
            ),
            "auditor_name": (
                engagement_context["auditor_name"]
            ),
            "controls_executed": (
                controls_executed
            ),
            "total_findings": (
                total_findings
            )
        }
    
    def create_workflow_event(
        self,
        engagement_context: dict,
        action: str,
        finding_id: str,
        performed_by: str
    ):

        return {
            "event_type": "workflow_action",
            "action": action,
            "finding_id": finding_id,
            "performed_by": performed_by,
            "client_name": engagement_context["client_name"],
            "engagement_id": engagement_context["engagement_id"],
            "framework": engagement_context["framework"],
            "audit_period": engagement_context["audit_period"],
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }