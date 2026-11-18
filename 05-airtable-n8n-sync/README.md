# Airtable + n8n-style Sync

Syncs incoming leads into Airtable: upsert Contact (dedupe by email), create linked Deal record.
`mock_airtable_api.py` mirrors the real Airtable REST API's request/response shape 1:1 — swap the base URL
for `https://api.airtable.com/v0/<your base id>` with a real API key and the sync logic runs unchanged.

Logic mirrors a 4-node n8n workflow: **Trigger → Lookup/Dedupe → Upsert Contact → Create linked Deal**.
Written in code (not the n8n canvas) so it's versionable in Git and testable without opening the n8n UI —
same approach works for porting an existing n8n workflow into code, or the reverse.

## Setup
```
pip install -r requirements.txt
```

## Demo (no real Airtable account needed)
1. `python mock_airtable_api.py` — mock Airtable base (port 9100)
2. `python workflow.py` — syncs `incoming_leads.csv` in
3. `curl http://127.0.0.1:9100/v0/appDEMO123/Contacts` — 3 contacts, deduped by email
4. Run `python workflow.py` again — same 3 Contacts (no duplicates: dedupe works), but Deals grow by 3
   more (each sync run represents a new lead event, so Deals are append-only by design — a real
   client conversation decides whether repeat leads should also skip creating a new Deal)

## Portfolio pitch
"Keeps Airtable clean when leads come from multiple sources — dedupes contacts by email so the same
person never gets two records, while still tracking every new deal/opportunity. Same logic as an n8n
workflow, but versioned in Git."
