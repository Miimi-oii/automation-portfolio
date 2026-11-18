"""
Dashboard on top of tracker.py: counts by flag, breakdown by owner/category, full table.
"""
from flask import Flask, render_template
from tracker import load_tracker

app = Flask(__name__)


@app.route("/")
def dashboard():
    df = load_tracker("data.csv")

    flag_counts = df["flag"].value_counts().reindex(["Overdue", "Due Soon", "On Track", "Done"], fill_value=0)
    by_owner = df.groupby("owner").size()

    rows = df.sort_values("due_date").to_dict(orient="records")
    for r in rows:
        r["due_date"] = r["due_date"].strftime("%Y-%m-%d")

    return render_template(
        "dashboard.html",
        overdue_count=int(flag_counts["Overdue"]),
        due_soon_count=int(flag_counts["Due Soon"]),
        on_track_count=int(flag_counts["On Track"]),
        done_count=int(flag_counts["Done"]),
        owner_labels=list(by_owner.index),
        owner_values=[int(v) for v in by_owner.values],
        rows=rows,
    )


if __name__ == "__main__":
    app.run(port=8200, debug=True)
