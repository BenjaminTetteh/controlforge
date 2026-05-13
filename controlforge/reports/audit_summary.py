from collections import Counter
from datetime import datetime
import time


class AuditSummary:

    def __init__(self):
        self.start_time = time.time()
        self.audit_timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def generate_summary(
        self,
        findings: list,
        controls_executed: int
    ) -> dict:

        severity_counts = Counter(
            finding["severity"]
            for finding in findings
        )

        execution_time = round(
            time.time() - self.start_time,
            2
        )

        summary = {
            "audit_timestamp": self.audit_timestamp,
            "controls_executed": controls_executed,
            "total_findings": len(findings),
            "critical_findings": severity_counts.get(
                "Critical", 0
            ),
            "high_findings": severity_counts.get(
                "High", 0
            ),
            "medium_findings": severity_counts.get(
                "Medium", 0
            ),
            "low_findings": severity_counts.get(
                "Low", 0
            ),
            "execution_time_seconds": execution_time
        }

        return summary