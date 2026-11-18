# Scheduled Report Bot

Pulls data on a cron schedule, summarizes it, pushes a report to LINE Notify.

## Setup
1. `pip install -r requirements.txt`
2. Copy `.env.example` → `.env`, fill LINE Notify token + data source URL.
3. Edit `build_summary()` for the client's real metrics.

## Run
```
python main.py
```
Runs continuously, fires the job daily at 08:00 (Asia/Bangkok).

## Portfolio pitch
"Daily/weekly auto-report straight to LINE or email — no one has to log in and pull numbers manually."
