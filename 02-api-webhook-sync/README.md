# API Webhook Sync

Receives a webhook from System A, transforms the payload, pushes it into System B's API.
Retries on failure (3x, exponential backoff), logs permanently-failed events to `failed_events.json` for replay, and alerts Slack when a sync can't be recovered.

## Setup
1. `pip install -r requirements.txt`
2. Copy `.env.example` → `.env`, fill target API URL/key (`SLACK_WEBHOOK_URL` optional).
3. Edit `transform()` to map source fields → target schema.

## Run
```
python main.py
```
Point System A's webhook (e.g. Shopify order-created) at `http://<host>:8000/webhook`.
Check failed syncs: `GET http://<host>:8000/failed-events`.

## Self-contained demo (no real client needed)
1. `python mock_target_api.py` — stands in for System B, stores whatever lands on it.
2. `python main.py` — the receiver under test.
3. `python mock_send_events.py` — fires 3 sample orders through the webhook.
4. `curl http://127.0.0.1:9000/records` — see the data that actually landed.
5. Kill `mock_target_api.py`, send another order — it retries 3x, then shows up in `GET /failed-events` instead of vanishing.

## Portfolio pitch
"Connects two systems in real time — new order/lead in System A automatically creates a record in System B (CRM, Airtable, Sheet). Survives transient API/network failures with retries, keeps a replayable log of anything that still fails, and pages the team in Slack."
