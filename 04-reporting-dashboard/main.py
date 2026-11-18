"""
Reads sales/lead data (CSV here; swap for a DB/API query in a real job) and serves
a dashboard: KPI tiles, revenue by source, revenue by day.
"""
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)
DATA_FILE = "data.csv"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    return df


@app.route("/")
def dashboard():
    df = load_data()

    total_revenue = df["amount"].sum()
    total_orders = len(df)
    avg_order = total_revenue / total_orders if total_orders else 0

    by_source = df.groupby("source")["amount"].sum().sort_values(ascending=False)
    by_day = df.groupby(df["date"].dt.strftime("%Y-%m-%d"))["amount"].sum().sort_index()

    return render_template(
        "dashboard.html",
        total_revenue=f"{total_revenue:,.0f}",
        total_orders=total_orders,
        avg_order=f"{avg_order:,.0f}",
        source_labels=list(by_source.index),
        source_values=[float(v) for v in by_source.values],
        day_labels=list(by_day.index),
        day_values=[float(v) for v in by_day.values],
    )


if __name__ == "__main__":
    app.run(port=8100, debug=True)
