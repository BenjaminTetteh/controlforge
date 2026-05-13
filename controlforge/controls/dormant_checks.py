from datetime import datetime
import pandas as pd


def detect_dormant_accounts(
    ad_df: pd.DataFrame,
    threshold_days: int = 90
) -> pd.DataFrame:

    today = datetime.today()

    ad_df = ad_df.copy()
    ad_df["last_login_date"] = pd.to_datetime(ad_df["last_login_date"])

    ad_df["days_since_last_login"] = (
        today - ad_df["last_login_date"]
    ).dt.days

    dormant_accounts = ad_df[
        (ad_df["account_status"] == "Active") &
        (ad_df["days_since_last_login"] > threshold_days)
    ]

    return dormant_accounts