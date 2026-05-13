import pandas as pd


def detect_mfa_gaps(ad_df: pd.DataFrame) -> pd.DataFrame:
    ad_df = ad_df.copy()

    ad_df["mfa_enabled_normalized"] = (
        ad_df["mfa_enabled"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    mfa_gaps = ad_df[
        (ad_df["account_status"] == "Active") &
        (ad_df["mfa_enabled_normalized"] == "false")
    ]

    return mfa_gaps