from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                             QRadioButton, QButtonGroup, QHBoxLayout,
                             QSpacerItem, QSizePolicy, QDateEdit, QTextEdit,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import QDate
import requests
import sys
import csv


class TransactionsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Transaction")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Event date
        self.date_label = QLabel("Event Date:")
        self.date_picker = QDateEdit()
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.setCalendarPopup(True)
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_picker)

        # Description
        self.description_label = QLabel("Description")
        self.description_input = QTextEdit()
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)

        # Transaction Type
        self.radio_label = QLabel("Transaction Type:")
        layout.addWidget(self.radio_label)
        radio_layout = QHBoxLayout()
        self.expense_radio = QRadioButton("Expense")
        self.income_radio = QRadioButton("Income")

        radio_layout.addWidget(self.expense_radio)
        radio_layout.addWidget(self.income_radio)

        self.group = QButtonGroup(self)
        self.group.addButton(self.expense_radio)
        self.group.addButton(self.income_radio)

        layout.addLayout(radio_layout)

        # Amount
        self.amount_label = QLabel("Amount")
        self.amount_input = QLineEdit()
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)

        # Buttons layout
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Add Transaction")
        self.submit_button.clicked.connect(self.submit_transaction)
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)

        layout.addSpacerItem(QSpacerItem(20, 40,
                                         QSizePolicy.Policy.Minimum,
                                         QSizePolicy.Policy.Expanding))

        self.setLayout(layout)

    def submit_transaction(self):
        date = self.date_picker.date().toString("yyyy-MM-dd")
        if self.expense_radio.isChecked():
            transaction_type = self.expense_radio.text()
        elif self.income_radio.isChecked():
            transaction_type = self.income_radio.text()
        else:
            transaction_type = ""

        data = {
            "date": date,
            "description": self.description_input.toPlainText(),
            "transaction": transaction_type,
            "amount": self.amount_input.text()
        }

        response = requests.post("https://transactionsummary.pythonanywhere.com/add", json=data)

        # with open("transactions.csv", "a", newline="") as file:
        #     writer = csv.DictWriter(file, fieldnames=["date", "description", "transaction", "amount"])
        #     writer.writerow(data)

        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Transaction added successfully!")
            self.description_input.clear()
            self.group.setExclusive(False)
            self.expense_radio.setChecked(False)
            self.income_radio.setChecked(False)
            self.group.setExclusive(True)
            self.amount_input.clear()


app = QApplication(sys.argv)
window = TransactionsApp()
window.show()
sys.exit(app.exec())
