"""
Reads sales/lead data (CSV here; swap for a DB/API query in a real job) and serves
a dashboard: KPI tiles, revenue by source, revenue by day. Filterable by date range,
and exportable to CSV with the same filter applied.
"""
import io
import pandas as pd
from flask import Flask, render_template, request, Response

app = Flask(__name__)
DATA_FILE = "data.csv"
REVENUE_TARGET = 20000


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    return df


def filtered_data(start: str | None, end: str | None) -> pd.DataFrame:
    df = load_data()
    if start:
        df = df[df["date"] >= pd.to_datetime(start)]
    if end:
        df = df[df["date"] <= pd.to_datetime(end)]
    return df


@app.route("/")
def dashboard():
    start = request.args.get("start", "")
    end = request.args.get("end", "")
    df = filtered_data(start or None, end or None)

    total_revenue = df["amount"].sum()
    total_orders = len(df)
    avg_order = total_revenue / total_orders if total_orders else 0

    by_source = df.groupby("source")["amount"].sum().sort_values(ascending=False)
    by_day = df.groupby(df["date"].dt.strftime("%Y-%m-%d"))["amount"].sum().sort_index()

    goal_pct = min(round(total_revenue / REVENUE_TARGET * 100), 100) if REVENUE_TARGET else 0

    return render_template(
        "dashboard.html",
        start=start,
        end=end,
        total_revenue=f"{total_revenue:,.0f}",
        total_orders=total_orders,
        avg_order=f"{avg_order:,.0f}",
        goal_pct=goal_pct,
        source_labels=list(by_source.index),
        source_values=[float(v) for v in by_source.values],
        day_labels=list(by_day.index),
        day_values=[float(v) for v in by_day.values],
    )


@app.route("/export.csv")
def export_csv():
    start = request.args.get("start", "")
    end = request.args.get("end", "")
    df = filtered_data(start or None, end or None)

    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return Response(buf.getvalue(), mimetype="text/csv",
                     headers={"Content-Disposition": "attachment; filename=sales_export.csv"})


if __name__ == "__main__":
    app.run(port=8100, debug=True)
