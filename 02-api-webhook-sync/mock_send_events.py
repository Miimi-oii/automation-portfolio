"""
Fires sample order webhooks at the receiver (main.py), as if System A (Shopify/GHL/etc.) sent them.
Run after main.py and mock_target_api.py are both running: python mock_send_events.py
"""
import requests

WEBHOOK_URL = "http://127.0.0.1:8000/webhook"

sample_orders = [
    {"id": "ord_1001", "customer_name": "Somchai Jaidee", "customer_email": "somchai@example.com", "total_price": 1290},
    {"id": "ord_1002", "customer_name": "Malee Suwan", "customer_email": "malee@example.com", "total_price": 650},
    {"id": "ord_1003", "customer_name": "Niran Thong", "customer_email": "niran@example.com", "total_price": 3200},
]

for order in sample_orders:
    resp = requests.post(WEBHOOK_URL, json=order, timeout=10)
    print(f"sent {order['id']} -> status {resp.status_code}: {resp.json()}")
