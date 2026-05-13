import pandas as pd


def detect_orphaned_accounts(
    hr_df: pd.DataFrame,
    ad_df: pd.DataFrame
) -> pd.DataFrame:

    orphaned_accounts = ad_df[
        ~ad_df["account_name"].isin(hr_df["account_name"])
    ]

    return orphaned_accounts