"""
Mirrors an n8n workflow: Trigger -> Dedupe -> Upsert Contact -> Create linked Deal.
In real n8n this is 4 nodes wired on a canvas; this script is the same logic in code,
for cases where a client wants it versioned/testable outside the n8n UI.
"""
import csv
import requests

AIRTABLE_URL = "http://127.0.0.1:9100/v0/appDEMO123"


def trigger_read_leads(csv_path: str) -> list[dict]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def find_existing_contact_by_email(email: str) -> dict | None:
    resp = requests.get(f"{AIRTABLE_URL}/Contacts", timeout=10)
    for record in resp.json()["records"]:
        if record["fields"].get("Email") == email:
            return record
    return None


def upsert_contact(lead: dict) -> str:
    existing = find_existing_contact_by_email(lead["email"])
    fields = {"Name": lead["name"], "Email": lead["email"], "Source": lead["source"]}

    if existing:
        requests.patch(f"{AIRTABLE_URL}/Contacts/{existing['id']}", json={"fields": fields}, timeout=10)
        return existing["id"]

    resp = requests.post(f"{AIRTABLE_URL}/Contacts", json={"fields": fields}, timeout=10)
    return resp.json()["id"]


def create_deal(contact_id: str, lead: dict) -> None:
    fields = {"Contact": [contact_id], "Value": float(lead["deal_value"]), "Stage": "New"}
    requests.post(f"{AIRTABLE_URL}/Deals", json={"fields": fields}, timeout=10)


def run_workflow(csv_path: str) -> None:
    leads = trigger_read_leads(csv_path)
    for lead in leads:
        contact_id = upsert_contact(lead)
        create_deal(contact_id, lead)
        print(f"synced {lead['email']} -> contact {contact_id}")


if __name__ == "__main__":
    run_workflow("incoming_leads.csv")
