import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import os


def load_credentials():
    load_dotenv()
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_recipient = os.getenv("EMAIL_RECIPIENT")
    sender_name = os.getenv("SENDER_NAME", email_address)
    if not email_address or not email_password or not email_recipient:
        raise ValueError("Missing credentials in environment variables.")
    return email_address, email_password, email_recipient, sender_name


def load_transactions(filepath="transactions.csv"):
    try:
        with open(filepath) as file:
            reader = csv.DictReader(file)
            transactions = list(reader)
            return transactions
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []


def previous_day_transactions(transactions, target_date):
    return [txn for txn in transactions if txn.get('date') == target_date]


def login_to_email(email_address, email_password):
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login(email_address, email_password)
    return smtp


def create_content(summary):
    total_expense, total_income = 0.0, 0.0
    lines = []
    for index, record in enumerate(summary, start=1):
        amount = float(record['amount'])
        transaction_type = record['transaction'].strip().lower()

        lines.append(
            f"{index}. {record['date']}: {record['description']} - "
            f"₹ {amount:.2f} ({record['transaction']})"
        )

        if transaction_type == 'expense':
            total_expense += amount
        elif transaction_type == 'income':
            total_income += amount

    return (
            "\n".join(lines) +
            f"\n\nTotal Expense: ₹ {total_expense:.2f}\n"
            f"Total Income: ₹ {total_income:.2f}"
    ), total_expense, total_income


def create_content_html(summary, yesterday, total_expense, total_income, sender_name):
    rows = ""
    for index, record in enumerate(summary, start=1):
        amount = float(record['amount'])
        transaction_type = record['transaction'].strip().lower()
        color = "#d9534f" if transaction_type == "expense" else "#5cb85c"

        rows += (
            f"<tr>"
            f"<td>{index}</td>"
            f"<td>{record['date']}</td>"
            f"<td>{record['description']}</td>"
            f"<td style='color:{color};'>₹ {amount:.2f}</td>"
            f"<td>{record['transaction']}</td>"
            f"</tr>"
        )

    html_content = f"""
    <html>
        <body>
            <p>Dear Jayasree,</p>
            <p>Good morning!</p>
            <p>I hope this message finds you well.</p>
            <p>Please find below the summary of expenses and income recorded as of yesterday, {yesterday}. 
            The transaction details are listed below:</p>
            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse:collapse; width:100%; 
            font-family:Arial; font-size:14px;">
                <thead>
                    <tr style="background-color:#f2f2f2;">
                        <th>#</th><th>Date</th><th>Description</th><th>Amount</th><th>Transaction</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
            <p><strong>Total Expense:</strong> <span style='color:#d9534f;'>₹ {total_expense:.2f}</span></p>
            <p><strong>Total Income:</strong> <span style='color:#5cb85c;'>₹ {total_income:.2f}</span></p>
            <p>Best regards,<br>{sender_name}</p>
        </body>
    </html>
    """
    return html_content


def create_email(subject, sender_name, email_recipient, plain_content, html_content):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_name
    msg["To"] = email_recipient
    msg.set_content(plain_content)
    msg.add_alternative(html_content, "html")
    return msg


def main():
    today = datetime.now()
    previous_day = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday = (today - timedelta(days=1)).strftime("%d-%B-%Y")

    transactions = load_transactions()
    summary = previous_day_transactions(transactions, previous_day)

    email_address, email_password, email_recipient, sender_name = load_credentials()
    smtp = login_to_email(email_address, email_password)

    plain_content, total_expense, total_income = create_content(summary)
    html_content = create_content_html(summary, yesterday, total_expense, total_income, sender_name)

    subject = f"💰 Expenses and Income Summary as of {yesterday}"
    msg = create_email(subject, sender_name, email_recipient, plain_content, html_content)

    try:
        smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email sending failed: {e}")
    finally:
        smtp.quit()


if __name__ == "__main__":
    main()
