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

## Portfolio pitch
"On top of any automation pipeline — turns the raw data your sync/scraper collects into a live dashboard (revenue by source, by day, KPI tiles), so no one has to open a spreadsheet to see how the business is doing."
