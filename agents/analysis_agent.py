import pandas as pd
from datetime import datetime

class AnalysisAgent:
    def __init__(self):
        self.data = self._load_all_data()
    
    def _load_all_data(self):
        """Load all CSV data into memory"""
        data = {}
        files = ['finances', 'inventory', 'members', 'orders', 'company_rules']
        for f in files:
            try:
                data[f] = pd.read_csv(f"data/{f}.csv")
            except:
                data[f] = pd.DataFrame()
        return data
    
    def generate_context(self, question):
        """Generate context for AI based on question"""
        context = {}
        
        # Financial context
        if 'finance' in question.lower() or 'money' in question.lower():
            df = self.data['finances']
            if not df.empty:
                income = df[df['type'] == 'income']['amount'].sum()
                expenses = df[df['type'] == 'expense']['amount'].sum()
                context['finance'] = f"Income: Rs {income:,.0f}, Expenses: Rs {expenses:,.0f}, Profit: Rs {income-expenses:,.0f}"
        
        # Inventory context
        if 'inventory' in question.lower() or 'stock' in question.lower() or 'item' in question.lower():
            df = self.data['inventory']
            if not df.empty:
                context['inventory'] = f"Total items: {len(df)}, Total quantity: {df['quantity'].sum():,}"
                low_stock = df[df['quantity'] < df['reorder_level']]
                if not low_stock.empty:
                    context['low_stock'] = low_stock['item_name'].tolist()
        
        # HR context
        if 'member' in question.lower() or 'staff' in question.lower() or 'worker' in question.lower():
            df = self.data['members']
            if not df.empty:
                available = df[df['status'] == 'available']
                context['hr'] = f"Total members: {len(df)}, Available: {len(available)}, On leave: {len(df)-len(available)}"
        
        return context
    
    def analyze(self, question):
        """Analyze and return structured response"""
        context = self.generate_context(question)
        
        # Build data summary
        summary = "Data Summary:\n"
        for key, value in context.items():
            summary += f"- {key}: {value}\n"
        
        # Generate insights based on question
        insights = []
        
        if 'order' in question.lower() or 'accept' in question.lower():
            df = self.data['orders']
            if not df.empty:
                pending = df[df['status'] == 'pending']
                if not pending.empty:
                    insights.append(f"Pending orders: {len(pending)}")
                    insights.append(f"Total order value: Rs {pending['total_value'].sum():,}")
        
        if 'profit' in question.lower() or 'earning' in question.lower():
            df = self.data['finances']
            if not df.empty:
                income = df[df['type'] == 'income']['amount'].sum()
                expenses = df[df['type'] == 'expense']['amount'].sum()
                insights.append(f"Net profit: Rs {income-expenses:,.0f}")
        
        if 'rule' in question.lower() or 'policy' in question.lower():
            df = self.data['company_rules']
            if not df.empty:
                active = df[df['status'] == 'active']
                if not active.empty:
                    insights.append(f"Active rules: {len(active)}")
                    for _, row in active.iterrows():
                        insights.append(f"- {row['rule_name']}: {row['description']}")
        
        return {
            "context": summary,
            "insights": insights,
            "data_available": bool(self.data['finances'].empty == False)
        }
