"""
Runs the real fetch+summary logic against a public test API and writes the result
to a local file, instead of sending to real LINE Notify (no token needed to see it work).
"""
from unittest.mock import patch
import main

with patch("main.send_line_notify"):
    df = main.fetch_data()
    summary = main.build_summary(df)

with open("report_output.txt", "w", encoding="utf-8") as f:
    f.write(summary)

print(f"Fetched {len(df)} records -> report_output.txt")
print(summary)
