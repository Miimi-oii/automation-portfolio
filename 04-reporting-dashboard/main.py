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
REQUIRED_COLUMNS = {"date", "source", "amount"}


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    return df


def validate_upload(file_storage) -> tuple[pd.DataFrame | None, str | None]:
    """Returns (dataframe, None) on success, or (None, error_message) on failure."""
    try:
        df = pd.read_csv(file_storage)
    except Exception as e:
        return None, f"Couldn't read file as CSV: {e}"

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        return None, f"Missing required column(s): {', '.join(sorted(missing))}"

    if df.empty:
        return None, "File has no data rows."

    try:
        df["date"] = pd.to_datetime(df["date"])
    except Exception:
        return None, "Column 'date' has values that aren't valid dates."

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    if df["amount"].isna().any():
        bad_rows = df[df["amount"].isna()].index.tolist()
        return None, f"Column 'amount' has non-numeric values in row(s): {bad_rows}"

    return df, None


def filtered_data(start: str | None, end: str | None) -> pd.DataFrame:
    df = load_data()
    if start:
        df = df[df["date"] >= pd.to_datetime(start)]
    if end:
        df = df[df["date"] <= pd.to_datetime(end)]
    return df


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file or file.filename == "":
        return dashboard(error="No file selected.")

    df, error = validate_upload(file)
    if error:
        return dashboard(error=error)

    df.to_csv(DATA_FILE, index=False)
    return dashboard(message=f"Uploaded {len(df)} rows successfully.")


@app.route("/")
def dashboard(error: str | None = None, message: str | None = None):
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
        error=error,
        message=message,
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
