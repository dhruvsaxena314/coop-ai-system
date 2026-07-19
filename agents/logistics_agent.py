import pandas as pd
import os
import random

class LogisticsAgent:
    def __init__(self, data_path="data/orders.csv"):
        self.data_path = data_path
        self.data = self._load_data()
        self.delivery_partners = ["QuickShip", "SafeTrans", "EcoLogistics", "FastTrack"]

    def _load_data(self):
        if os.path.exists(self.data_path):
            return pd.read_csv(self.data_path)
        return pd.DataFrame()

    def estimate_delivery(self, destination, weight_kg):
        base_cost = 50 + (weight_kg * 2)
        base_time = 2 + (weight_kg * 0.1)

        if "city" in destination.lower():
            time_multiplier = 1.0
            cost_multiplier = 1.0
        elif "rural" in destination.lower():
            time_multiplier = 1.5
            cost_multiplier = 1.3
        else:
            time_multiplier = 1.2
            cost_multiplier = 1.1

        return {
            "estimated_days": round(base_time * time_multiplier, 1),
            "estimated_cost": round(base_cost * cost_multiplier, 2),
            "partner": random.choice(self.delivery_partners),
            "destination": destination,
            "weight": weight_kg
        }

    def get_pending_orders(self):
        if self.data.empty:
            return []
        return self.data[self.data['status'] == 'pending'].to_dict('records')

    def get_delivery_capacity(self):
        pending = self.get_pending_orders()
        available_drivers = 2

        return {
            "pending_orders": len(pending),
            "available_drivers": available_drivers,
            "can_handle_more": len(pending) < available_drivers * 2,
            "days_of_backlog": len(pending) // 2 if pending else 0
        }

    def analyze(self, query_context=None):
        capacity = self.get_delivery_capacity()

        finding = f"Delivery status: {capacity['pending_orders']} orders pending, "
        finding += f"{capacity['available_drivers']} drivers available."

        return {
            "agent": "Logistics Agent",
            "finding": finding,
            "confidence": 0.85,
            "details": capacity
        }
