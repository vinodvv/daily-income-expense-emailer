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


@app.route("/transactions", methods=["GET"])
def get_transactions():
    try:
        transactions = []

        # Check if file exists
        if not os.path.exists(CSV_FILE):
            return jsonify({"transactions": []}), 200

        # Read CSV file
        with open(CSV_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(row)

        return jsonify({"transactions": transactions}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/transactions/filter", methods=["GET"])
def filter_transactions():
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        transaction_type = request.args.get('transaction')  # "credit" or "debit"

        transactions = []

        # Check if file exists
        if not os.path.exists(CSV_FILE):
            return jsonify({"transactions": []}), 200

        # Read CSV file
        with open(CSV_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Apply filters
                include = True

                # Filter by start date
                if start_date and row['date'] < start_date:
                    include = False

                # Filter by end date
                if end_date and row['date'] > end_date:
                    include = False

                # Filter by transaction type
                if transaction_type and row['transaction'].lower() != transaction_type.lower():
                    include = False

                if include:
                    transactions.append(row)

        return jsonify({
            "transactions": transactions,
            "count": len(transactions)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/transactions/summary", methods=["GET"])
def get_summary():
    try:
        # Get optional query parameters for filtering
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        total_credit = 0.0
        total_debit = 0.0
        credit_count = 0
        debit_count = 0

        # Check if file exists
        if not os.path.exists(CSV_FILE):
            return jsonify({
                "total_credit": 0,
                "total_debit": 0,
                "net_balance": 0,
                "credit_count": 0,
                "debit_count": 0,
                "total_transactions": 0
            }), 200

        # Read CSV file
        with open(CSV_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Apply date filters if provided
                include = True

                # Filter start date
                if start_date and row['date'] < start_date:
                    include = False

                # Filter end date
                if end_date and row['date'] > end_date:
                    include = False

                if include:
                    amount = float(row['amount'])
                    if row['transaction'].lower() == "income":
                        total_credit += amount
                        credit_count += 1
                    elif row['transaction'].lower() == 'expense':
                        total_debit += amount
                        debit_count += 1

        net_balance = total_credit - total_debit
        total_transactions = credit_count + debit_count

        return jsonify({
            "total_credit": round(total_credit, 2),
            "total_debit": round(total_debit, 2),
            "net_balance": round(net_balance, 2),
            "credit_count": credit_count,
            "debit_count": debit_count,
            "total_transactions": total_transactions
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
