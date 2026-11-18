"""
Webhook receiver: System A pushes an event -> transform -> push to System B's API.
Example wiring: Shopify order webhook -> normalize -> create row in Airtable/CRM.
Retries on failure, logs permanently-failed events to failed_events.json, alerts Slack
(logic lives in ../common/retry_client.py, shared across sync projects).
"""
import os
import sys
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.retry_client import RetryClient

load_dotenv()

app = Flask(__name__)

TARGET_API_URL = os.environ["TARGET_API_URL"]
TARGET_API_KEY = os.environ["TARGET_API_KEY"]
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

client = RetryClient(slack_webhook_url=SLACK_WEBHOOK_URL)


def transform(payload: dict) -> dict:
    # TODO: map source webhook fields -> target API's expected shape
    return {
        "name": payload.get("customer_name", ""),
        "email": payload.get("customer_email", ""),
        "amount": payload.get("total_price", 0),
        "source_id": payload.get("id", ""),
    }


@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json(force=True)
    record = transform(payload)

    try:
        resp = client.post(TARGET_API_URL, record, headers={"Authorization": f"Bearer {TARGET_API_KEY}"})
    except RuntimeError as e:
        return jsonify({"status": "failed", "error": str(e)}), 502

    return jsonify({"status": "synced", "target_response": resp.json()}), 200


@app.route("/failed-events", methods=["GET"])
def failed_events():
    return jsonify(client.read_failed_events())


if __name__ == "__main__":
    app.run(port=8000)
