import pandas as pd
import os
from datetime import datetime, timedelta

class FinanceAgent:
    def __init__(self, data_path="data/finances.csv"):
        self.data_path = data_path
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_path):
            return pd.read_csv(self.data_path)
        return pd.DataFrame()

    def get_cash_flow(self):
        if self.data.empty:
            return {"cash_flow": 0, "income": 0, "expenses": 0}

        income = self.data[self.data['type'] == 'income']['amount'].sum()
        expenses = self.data[self.data['type'] == 'expense']['amount'].sum()
        cash_flow = income - expenses

        return {"cash_flow": cash_flow, "income": income, "expenses": expenses}

    def can_afford(self, amount):
        cash_flow = self.get_cash_flow()
        return {
            "can_afford": cash_flow["cash_flow"] >= amount,
            "current_balance": cash_flow["cash_flow"],
            "required": amount,
            "shortfall": max(0, amount - cash_flow["cash_flow"])
        }

    def get_recent_transactions(self, days=30):
        if self.data.empty:
            return []
        cutoff = datetime.now() - timedelta(days=days)
        recent = self.data[pd.to_datetime(self.data['date']) >= cutoff]
        return recent.to_dict('records')

    def analyze(self, query_context=None):
        cash_flow = self.get_cash_flow()

        finding = f"Current balance: Rs {cash_flow['cash_flow']:,.2f}. "
        finding += f"Monthly income: Rs {cash_flow['income']:,.2f}, "
        finding += f"expenses: Rs {cash_flow['expenses']:,.2f}."

        return {
            "agent": "Finance Agent",
            "finding": finding,
            "confidence": 0.92,
            "details": cash_flow
        }
