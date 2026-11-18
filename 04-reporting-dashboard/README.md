# Reporting Dashboard

Reads sales/lead data and serves a live dashboard: KPI tiles + revenue by source + revenue by day.
`data.csv` is a stand-in for a real source (Airtable, Google Sheets, DB, API) — swap `load_data()` for the real query.

## Setup
```
pip install -r requirements.txt
```

## Run
```
python main.py
```
Open http://127.0.0.1:8100

## CSV upload
"Upload data" form (`/upload`) accepts a CSV with columns `date, source, amount`, validates
column presence, date parsing, and that `amount` is numeric — rejects with a clear error
message otherwise. Matches the "Excel/CSV import with validation" requirement seen in
real Upwork dashboard job posts.

## Design
Sidebar nav, icon-badged KPI cards, and a donut "revenue goal" chart — matching the
common admin-dashboard layout pattern (sidebar + icon KPIs + a goal/progress ring).

## Date filter + export
Filter by date range with the From/To pickers (`?start=YYYY-MM-DD&end=YYYY-MM-DD`), then
"Export CSV" downloads the same filtered rows.

## Portfolio pitch
"On top of any automation pipeline — turns the raw data your sync/scraper collects into a live dashboard (revenue by source, by day, KPI tiles), so no one has to open a spreadsheet to see how the business is doing."
