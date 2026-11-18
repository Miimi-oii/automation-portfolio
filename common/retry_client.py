"""
Reusable HTTP-call-with-retry: retries with exponential backoff, logs permanently-failed
calls to a JSON file for replay, and alerts Slack on final failure.
Used by any sync/integration project that pushes to an external API.
"""
import json
import os
import time
import requests


class RetryClient:
    def __init__(self, failed_events_file: str = "failed_events.json",
                 max_retries: int = 3, slack_webhook_url: str | None = None):
        self.failed_events_file = failed_events_file
        self.max_retries = max_retries
        self.slack_webhook_url = slack_webhook_url

    def post(self, url: str, json_body: dict, headers: dict | None = None,
              timeout: int = 10) -> requests.Response:
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = requests.post(url, json=json_body, headers=headers, timeout=timeout)
                resp.raise_for_status()
                return resp
            except requests.RequestException as e:
                last_error = str(e)
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)  # 2s, 4s, ...
        self._log_failed_event(json_body, last_error)
        self._alert_slack(f":rotating_light: Sync failed after {self.max_retries} retries: "
                           f"{last_error}\nRecord: {json_body}")
        raise RuntimeError(last_error)

    def read_failed_events(self) -> list[dict]:
        if not os.path.exists(self.failed_events_file):
            return []
        with open(self.failed_events_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _log_failed_event(self, record: dict, error: str) -> None:
        events = self.read_failed_events()
        events.append({"record": record, "error": error, "time": time.time()})
        with open(self.failed_events_file, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=2)

    def _alert_slack(self, message: str) -> None:
        if not self.slack_webhook_url:
            return
        requests.post(self.slack_webhook_url, json={"text": message}, timeout=10)
