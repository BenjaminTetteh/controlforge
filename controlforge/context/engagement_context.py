from datetime import datetime


class EngagementContext:

    def __init__(
        self,
        client_name: str,
        engagement_id: str,
        framework: str,
        audit_period: str,
        auditor_name: str
    ):

        self.client_name = client_name
        self.engagement_id = engagement_id
        self.framework = framework
        self.audit_period = audit_period
        self.auditor_name = auditor_name

        self.execution_timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def to_dict(self):

        return {
            "client_name": self.client_name,
            "engagement_id": self.engagement_id,
            "framework": self.framework,
            "audit_period": self.audit_period,
            "auditor_name": self.auditor_name,
            "execution_timestamp": self.execution_timestamp
        }