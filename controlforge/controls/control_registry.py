CONTROL_REGISTRY = {

    "MFA_ENFORCEMENT": {
        "name": "MFA Compliance Review",
        "domain": "Identity and Access Management",
        "description": (
            "Validates that active accounts "
            "have multi-factor authentication enabled."
        ),
        "risk_statement": (
            "Accounts without MFA increase the risk "
            "of unauthorized access."
        ),
        "severity": "Critical"
    },

    "TERMINATED_USER_ACCESS": {
        "name": "Terminated User Access Review",
        "domain": "Identity Lifecycle Management",
        "description": (
            "Identifies terminated users "
            "with active accounts."
        ),
        "risk_statement": (
            "Active terminated-user accounts may allow "
            "unauthorized system access."
        ),
        "severity": "Critical"
    },

    "SOD_CONFLICTS": {
        "name": "Segregation of Duties Review",
        "domain": "Access Governance",
        "description": (
            "Detects conflicting role assignments."
        ),
        "risk_statement": (
            "Conflicting access may enable "
            "fraudulent or unauthorized activity."
        ),
        "severity": "Critical"
    }
}