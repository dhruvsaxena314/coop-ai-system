from agents.base_agent import BaseAgent

class InventoryAgent(BaseAgent):
    def get_summary(self):
        df = self.data['inventory']
        if df.empty:
            return None
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df['reorder_level'] = pd.to_numeric(df['reorder_level'], errors='coerce')
        low_stock = df[df['quantity'] < df['reorder_level']]
        return {
            'total_items': len(df),
            'total_quantity': df['quantity'].sum(),
            'low_stock_items': low_stock.to_dict('records'),
            'categories': df['category'].unique().tolist()
        }
    
    def analyze(self, context=None):
        summary = self.get_summary()
        if not summary:
            return {"agent": "Inventory Agent", "finding": "No inventory data", "confidence": 0}
        low_count = len(summary['low_stock_items'])
        finding = f"{summary['total_items']} items, total qty {summary['total_quantity']:,.0f}"
        if low_count > 0:
            finding += f", ⚠️ {low_count} items low stock"
        return {
            "agent": "Inventory Agent",
            "finding": finding,
            "confidence": 0.9,
            "details": summary
        }
