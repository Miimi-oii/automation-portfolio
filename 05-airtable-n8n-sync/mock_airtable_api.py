"""
Stands in for the real Airtable REST API (same request/response shape) so the sync
logic can be built and tested without a live base. Two tables: Contacts, Deals
(Deals links back to Contacts via a "Contact" field holding a list of record ids,
same as a real Airtable linked-record field).
Run: python mock_airtable_api.py
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

tables = {"Contacts": {}, "Deals": {}}
next_id = {"Contacts": 1, "Deals": 1}


def new_record_id(table: str) -> str:
    rid = f"rec{table[:1]}{next_id[table]:03d}"
    next_id[table] += 1
    return rid


@app.route("/v0/<base_id>/<table>", methods=["GET"])
def list_records(base_id, table):
    return jsonify({"records": [{"id": rid, "fields": f} for rid, f in tables[table].items()]})


@app.route("/v0/<base_id>/<table>", methods=["POST"])
def create_record(base_id, table):
    fields = request.get_json(force=True)["fields"]
    rid = new_record_id(table)
    tables[table][rid] = fields
    print(f"[mock airtable] {table} created {rid}: {fields}")
    return jsonify({"id": rid, "fields": fields}), 200


@app.route("/v0/<base_id>/<table>/<record_id>", methods=["PATCH"])
def update_record(base_id, table, record_id):
    fields = request.get_json(force=True)["fields"]
    tables[table][record_id].update(fields)
    print(f"[mock airtable] {table} updated {record_id}: {tables[table][record_id]}")
    return jsonify({"id": record_id, "fields": tables[table][record_id]}), 200


if __name__ == "__main__":
    app.run(port=9100)
