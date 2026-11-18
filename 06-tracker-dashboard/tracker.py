"""
Overdue-flag logic for a status tracker (supplier/task/vendor onboarding, etc.).
Same business rule most "tracker + dashboard" Upwork jobs ask for in a Google Sheet,
written as a reusable, testable function instead of a spreadsheet formula.
"""
from datetime import date, timedelta
import pandas as pd

DONE_STAGES = {"Approved", "Rejected"}
DUE_SOON_DAYS = 3


def flag_row(stage: str, due_date: date, today: date) -> str:
    if stage in DONE_STAGES:
        return "Done"
    days_left = (due_date - today).days
    if days_left < 0:
        return "Overdue"
    if days_left <= DUE_SOON_DAYS:
        return "Due Soon"
    return "On Track"


def load_tracker(csv_path: str, today: date | None = None) -> pd.DataFrame:
    today = today or date.today()
    df = pd.read_csv(csv_path, parse_dates=["due_date"])
    df["flag"] = df.apply(lambda r: flag_row(r["stage"], r["due_date"].date(), today), axis=1)
    return df


if __name__ == "__main__":
    df = load_tracker("data.csv")
    print(df[["supplier", "stage", "due_date", "flag"]].to_string(index=False))
