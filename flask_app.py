from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

CSV_FILE = "/home/TransactionSummary/transactions.csv"

# Ensure CSV file exists with headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "date", "description", "transaction", "amount"
        ])
        writer.writeheader()

@app.route("/add", methods=["POST"])
def add_transaction():
    data = request.get_json(force=True)

    required_fields = ["date", "description", "transaction", "amount"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=[
                "date", "description", "transaction", "amount"
            ])
            writer.writerow({
                "date": data["date"],
                "description": data["description"],
                "transaction": data["transaction"],
                "amount": data["amount"],
            })
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str({e})}), 500


if __name__ == "__main__":
    app.run()
