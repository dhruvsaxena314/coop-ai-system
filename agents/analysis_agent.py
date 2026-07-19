import pandas as pd
import os
from agents.external_agent import ExternalAgent

class AnalysisAgent:
    def __init__(self):
        self.data = self._load_all_data()
    
    def _load_all_data(self):
        data = {}
        files = {
            'finances': 'data/finances.csv',
            'inventory': 'data/inventory.csv',
            'members': 'data/members.csv',
            'orders': 'data/orders.csv',
            'rules': 'data/company_rules.csv'
        }
        for key, path in files.items():
            try:
                if os.path.exists(path):
                    df = pd.read_csv(path)
                    # Ensure numeric columns
                    if key == 'finances':
                        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
                    elif key == 'inventory':
                        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
                        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
                        df['reorder_level'] = pd.to_numeric(df['reorder_level'], errors='coerce')
                    elif key == 'orders':
                        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
                        df['total_value'] = pd.to_numeric(df['total_value'], errors='coerce')
                    data[key] = df
                else:
                    data[key] = pd.DataFrame()
            except Exception as e:
                print(f"Error loading {key}: {e}")
                data[key] = pd.DataFrame()
        return data
    
    def get_finance_summary(self):
        df = self.data['finances']
        if df.empty:
            return None
        income = df[df['type'] == 'income']['amount'].sum()
        expenses = df[df['type'] == 'expense']['amount'].sum()
        return {
            'income': income,
            'expenses': expenses,
            'profit': income - expenses,
            'total_transactions': len(df),
            'latest': df.tail(5).to_dict('records')
        }
    
    def get_inventory_summary(self):
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
    
    def get_member_summary(self):
        df = self.data['members']
        if df.empty:
            return None
        return {
            'total': len(df),
            'available': len(df[df['status'] == 'available']),
            'on_leave': len(df[df['status'] == 'on_leave']),
            'skills': df['skills'].unique().tolist()
        }
    
    def get_order_summary(self):
        df = self.data['orders']
        if df.empty:
            return None
        df['total_value'] = pd.to_numeric(df['total_value'], errors='coerce')
        pending = df[df['status'] == 'pending']
        processing = df[df['status'] == 'processing']
        return {
            'total': len(df),
            'pending': len(pending),
            'pending_value': pending['total_value'].sum() if not pending.empty else 0,
            'processing': len(processing),
            'processing_value': processing['total_value'].sum() if not processing.empty else 0,
            'customers': df['customer'].unique().tolist()
        }
    
    def get_rule_summary(self):
        df = self.data['rules']
        if df.empty:
            return None
        return {
            'total': len(df),
            'active': len(df[df['status'] == 'active']),
            'categories': df['category'].unique().tolist()
        }
    
    def analyze(self, question):
        # Internal summaries
        finance = self.get_finance_summary()
        inventory = self.get_inventory_summary()
        members = self.get_member_summary()
        orders = self.get_order_summary()
        rules = self.get_rule_summary()
        
        # External data
        ext = ExternalAgent()
        weather = ext.get_weather()
        cotton_price = ext.get_cotton_price()
        news = ext.get_news()
        exchange_rate = ext.get_exchange_rate()
        
        # Build context
        context_lines = []
        if finance:
            context_lines.append(f"FINANCES: Income Rs {finance['income']:,.0f}, Expenses Rs {finance['expenses']:,.0f}, Profit Rs {finance['profit']:,.0f}")
        if inventory:
            context_lines.append(f"INVENTORY: {inventory['total_items']} items, total qty {inventory['total_quantity']:,.0f}, low stock items: {len(inventory['low_stock_items'])}")
        if members:
            context_lines.append(f"MEMBERS: {members['total']} total, {members['available']} available, {members['on_leave']} on leave")
        if orders:
            context_lines.append(f"ORDERS: {orders['total']} total, {orders['pending']} pending (Rs {orders['pending_value']:,.0f}), {orders['processing']} processing")
        if rules:
            context_lines.append(f"RULES: {rules['total']} total, {rules['active']} active")
        
        # External context
        if cotton_price:
            context_lines.append(f"COTTON PRICE: ${cotton_price} per pound")
        if weather:
            day1 = weather[0]
            context_lines.append(f"WEATHER (next 3h): {day1['weather'][0]['description']}, {day1['main']['temp']}°C")
        if exchange_rate:
            context_lines.append(f"USD/INR: {exchange_rate}")
        if news:
            headlines = " | ".join([n["title"] for n in news[:2]])
            context_lines.append(f"INDUSTRY NEWS: {headlines}")
        
        context = "\n".join(context_lines)
        
        # Insights
        insights = []
        references = []
        if orders and orders['pending'] > 0:
            insights.append(f"{orders['pending']} orders pending worth Rs {orders['pending_value']:,.0f}")
            references.append("orders.csv → pending status")
        if finance and finance['profit'] < 0:
            insights.append(f"⚠️ Net loss of Rs {abs(finance['profit']):,.0f}")
            references.append("finances.csv → income vs expenses")
        if inventory and len(inventory['low_stock_items']) > 0:
            low_names = [item['item_name'] for item in inventory['low_stock_items']]
            insights.append(f"Low stock: {', '.join(low_names[:3])}{'...' if len(low_names)>3 else ''}")
            references.append("inventory.csv → reorder_level check")
        if members and members['available'] < members['total'] * 0.6:
            insights.append(f"Only {members['available']} of {members['total']} members available")
            references.append("members.csv → availability status")
        
        # External insights
        if cotton_price and cotton_price is not None:
            try:
                if float(cotton_price) > 70:
                    insights.append(f"⚠️ Cotton price is high (${cotton_price}) – consider sourcing alternatives")
                    references.append("Alpha Vantage → cotton price")
            except:
                pass
        if weather and weather[0]['weather'][0]['description'].lower().find('rain') != -1:
            insights.append("🌧️ Rain forecast – prepare for delivery delays")
            references.append("OpenWeatherMap → forecast")
        
        # Chain-of-Thought
        cot = []
        if 'order' in question.lower() or 'accept' in question.lower():
            if orders and orders['pending'] > 0:
                cot.append(f"Step 1: There are {orders['pending']} pending orders worth Rs {orders['pending_value']:,.0f}.")
            if inventory and len(inventory['low_stock_items']) > 0:
                cot.append(f"Step 2: Inventory is low on {len(inventory['low_stock_items'])} items – may affect production.")
            if members and members['available'] >= 5:
                cot.append(f"Step 3: {members['available']} members are available, enough to handle extra work.")
            if finance and finance['profit'] > 10000:
                cot.append(f"Step 4: Positive profit of Rs {finance['profit']:,.0f} suggests financial capacity.")
            if cotton_price and cotton_price is not None:
                try:
                    if float(cotton_price) > 70:
                        cot.append(f"Step 5: Cotton price is high (${cotton_price}) – factor in increased material cost.")
                except:
                    pass
            if cot:
                cot.append("Conclusion: Based on data, the cooperative is capable of accepting new orders with caution on inventory and external costs.")
            else:
                cot.append("No clear data conflicts; decision should be based on specific order details.")
        else:
            cot.append("Analysis based on available data:")
            if finance:
                cot.append(f"- Profit: Rs {finance['profit']:,.0f}")
            if orders:
                cot.append(f"- Orders in pipeline: {orders['total']}")
            if members:
                cot.append(f"- Workforce: {members['available']} available")
            if cotton_price:
                cot.append(f"- Cotton price: ${cotton_price}")
        
        return {
            "context": context,
            "insights": insights,
            "references": references,
            "cot": cot,
            "data_available": bool(finance or inventory or members or orders)
        }
