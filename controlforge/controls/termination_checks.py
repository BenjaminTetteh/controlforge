import pandas as pd


def detect_terminated_active_accounts(
    hr_df: pd.DataFrame,
    ad_df: pd.DataFrame
) -> pd.DataFrame:

    merged_df = hr_df.merge(
        ad_df,
        on="account_name",
        how="inner"
    )

    findings = merged_df[
        (merged_df["employment_status"] == "Terminated") &
        (merged_df["account_status"] == "Active")
    ]

    return findings