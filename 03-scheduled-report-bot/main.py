"""
Daily scheduled job: pull data from a source (API/CSV/DB), summarize, send report to LINE Notify.
"""
import sys
import os
import requests
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

load_dotenv()
sys.stdout.reconfigure(encoding="utf-8")

LINE_NOTIFY_TOKEN = os.environ["LINE_NOTIFY_TOKEN"]
DATA_SOURCE_URL = os.environ["DATA_SOURCE_URL"]


def fetch_data() -> pd.DataFrame:
    resp = requests.get(DATA_SOURCE_URL, timeout=10)
    resp.raise_for_status()
    return pd.DataFrame(resp.json())


def build_summary(df: pd.DataFrame) -> str:
    # TODO: swap for the real metrics the client wants (sales, stock, leads, etc.)
    total = df["amount"].sum() if "amount" in df.columns else 0
    count = len(df)
    return f"รายงานประจำวัน\nรายการ: {count}\nยอดรวม: {total:,.2f}"


def send_line_notify(message: str) -> None:
    requests.post(
        "https://notify-api.line.me/api/notify",
        headers={"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"},
        data={"message": message},
        timeout=10,
    )


def run_report() -> None:
    df = fetch_data()
    summary = build_summary(df)
    send_line_notify(summary)
    print(summary)


if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Bangkok")
    scheduler.add_job(run_report, "cron", hour=8, minute=0)  # daily 08:00
    print("Scheduler started. Ctrl+C to stop.")
    scheduler.start()
