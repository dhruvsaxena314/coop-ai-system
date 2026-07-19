import pandas as pd
import os

class InventoryAgent:
    def __init__(self, data_path="data/inventory.csv"):
        self.data_path = data_path
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_path):
            return pd.read_csv(self.data_path)
        return pd.DataFrame()

    def check_availability(self, item_name, quantity):
        if self.data.empty:
            return {"available": False, "message": "No inventory data"}

        item = self.data[self.data['item_name'].str.contains(item_name, case=False)]
        if item.empty:
            return {"available": False, "message": f"Item '{item_name}' not found"}

        available = item.iloc[0]['quantity']
        return {
            "available": available >= quantity,
            "available_quantity": available,
            "required": quantity,
            "item_name": item_name,
            "unit_price": item.iloc[0]['unit_price'],
            "shortfall": max(0, quantity - available)
        }

    def get_items_needing_reorder(self):
        if self.data.empty:
            return []
        low_stock = self.data[self.data['quantity'] < self.data['reorder_level']]
        return low_stock.to_dict('records')

    def calculate_cost(self, item_name, quantity):
        if self.data.empty:
            return {"error": "No inventory data"}

        item = self.data[self.data['item_name'].str.contains(item_name, case=False)]
        if item.empty:
            return {"error": "Item not found"}

        unit_price = item.iloc[0]['unit_price']
        return {
            "item_name": item_name,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_cost": unit_price * quantity,
            "available": item.iloc[0]['quantity'] >= quantity
        }

    def analyze(self, query_context=None):
        if self.data.empty:
            return {
                "agent": "Inventory Agent",
                "finding": "No inventory data available",
                "confidence": 0.5,
                "details": {}
            }

        total_items = len(self.data)
        total_quantity = self.data['quantity'].sum()
        low_stock = self.get_items_needing_reorder()

        finding = f"Total inventory: {total_quantity} units across {total_items} items. "
        if low_stock:
            finding += f"{len(low_stock)} items need reordering."
        else:
            finding += "All items are above reorder level."

        return {
            "agent": "Inventory Agent",
            "finding": finding,
            "confidence": 0.88,
            "details": {
                "total_items": total_items,
                "total_quantity": total_quantity,
                "low_stock_items": low_stock
            }
        }
