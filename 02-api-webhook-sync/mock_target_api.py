"""
Stands in for 'System B' (CRM/Airtable/whatever the real client's target API is).
Stores whatever main.py pushes to it, in memory, so you can see the data that actually landed.
Run on a different port from the webhook receiver: python mock_target_api.py
"""
from flask import Flask, request, jsonify

app = Flask(__name__)
records = []


@app.route("/records", methods=["POST"])
def create_record():
    data = request.get_json(force=True)
    data["_id"] = len(records) + 1
    records.append(data)
    print(f"[mock target] stored record #{data['_id']}: {data}")
    return jsonify(data), 201


@app.route("/records", methods=["GET"])
def list_records():
    return jsonify(records)


if __name__ == "__main__":
    app.run(port=9000)
