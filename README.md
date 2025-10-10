# Daily Income and Expenses Emailer

This Python app sends a daily email summary of income and expenses from a CSV file. The email includes both plain text and HTML summaries and is sent using Gmail SMTP. The app is ideal for tracking personal or small business finances via automated daily notifications.

## Features

- Reads transaction data from a CSV file (`transactions.csv`)
- Summarizes previous day's income and expenses
- Email is sent automatically each day via Gmail SMTP
- Customizable HTML table with total expense and income highlighting
- Uses environment variables for configuration
- Error handling for missing credentials and failed email delivery

## Setup

1. **Clone the repository**
    ```
    git clone https://github.com/vinodvv/daily-income-expense-emailer.git
    cd daily-income-expense-emailer
    ```

2. **Install dependencies**
    ```
    pip install python-dotenv
    ```

3. **Create your `.env` file**
    ```
    EMAIL_ADDRESS=your_gmail_address@gmail.com
    EMAIL_PASSWORD=your_gmail_app_password
    EMAIL_RECIPIENT=recipient_email@gmail.com
    SENDER_NAME=Your Name
    ```

    > 💡 _Set up an App Password for Gmail 2FA accounts._

4. **Prepare your transactions CSV**

    The `transactions.csv` must include the following columns:
    - `date` (YYYY-MM-DD)
    - `description`
    - `amount` (numeric)
    - `transaction` (Expense or Income)

    Example:
    ```
    date,description,amount,transaction
    2025-10-09,Vegetables,199,Expense
    2025-10-09,Salary,50000,Income
    ```

5. **Run the script**
    ```
    python send_transactions.py
    ```

## License

See [LICENSE](LICENSE) for licensing information.

## Contributing

Pull requests are welcome! Please open an issue first to discuss what you would like to change.

## Author

Vinod VV



