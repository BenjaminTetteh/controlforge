import pandas as pd


def detect_sod_conflicts(
    role_df: pd.DataFrame,
    sod_rules_df: pd.DataFrame
) -> pd.DataFrame:

    findings = []

    grouped_roles = (
        role_df.groupby("account_name")["role_code"]
        .apply(list)
        .to_dict()
    )

    for _, rule in sod_rules_df.iterrows():

        role_1 = rule["conflicting_role_1"]
        role_2 = rule["conflicting_role_2"]

        for account_name, user_roles in grouped_roles.items():

            if role_1 in user_roles and role_2 in user_roles:

                findings.append({
                    "account_name": account_name,
                    "system_name": rule["system_name"],
                    "role_1": role_1,
                    "role_2": role_2,
                    "conflict_description": (
                        rule["conflict_description"]
                    ),
                    "severity": rule["severity"]
                })

    findings_df = pd.DataFrame(findings)

    return findings_df