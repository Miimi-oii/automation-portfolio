# Tracker + Dashboard (overdue flags)

Status tracker (supplier/task/vendor onboarding, etc.) with an auto-computed overdue flag and a live dashboard.
Matches the "Google Sheets tracker with dashboard & overdue flags" pattern seen often on Upwork —
built here as Python/Flask so the business rule (`tracker.py:flag_row`) is testable code, not a spreadsheet
formula. The same logic ports directly into a real Google Sheet via gspread + Apps Script if the client wants
it native in Sheets instead.

## Setup
```
pip install -r requirements.txt
```

## Run
```
python main.py
```
Open http://127.0.0.1:8200 — KPI tiles (Overdue / Due Soon / On Track / Done), breakdown by owner, full table
with the computed flag per row. `data.csv` is the source; swap `tracker.load_tracker()` for a real
Google Sheets/Airtable read in production.

## Test the logic directly
```
python tracker.py
```
Prints every row's computed flag against today's date.

## Portfolio pitch
"Turns a status list into a dashboard that flags what's overdue automatically — no one has to
eyeball due dates every morning."
