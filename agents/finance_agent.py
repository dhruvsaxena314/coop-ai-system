from agents.base_agent import BaseAgent

class FinanceAgent(BaseAgent):
    def get_summary(self):
        df = self.data['finances']
        if df.empty:
            return None
        income = df[df['type'] == 'income']['amount'].sum()
        expenses = df[df['type'] == 'expense']['amount'].sum()
        profit = income - expenses
        return {
            'income': income,
            'expenses': expenses,
            'profit': profit,
            'profit_margin': (profit / income * 100) if income > 0 else 0,
            'total_transactions': len(df),
            'latest': df.tail(5).to_dict('records')
        }
    
    def analyze(self, context=None):
        summary = self.get_summary()
        if not summary:
            return {"agent": "Finance Agent", "finding": "No data available", "confidence": 0}
        
        findings = []
        if summary['profit'] < 0:
            findings.append(f"Net loss of Rs {abs(summary['profit']):,.0f} (margin: {summary['profit_margin']:.1f}%)")
        elif summary['profit'] < 10000:
            findings.append(f"Low profit: Rs {summary['profit']:,.0f} (margin: {summary['profit_margin']:.1f}%)")
        else:
            findings.append(f"Healthy profit: Rs {summary['profit']:,.0f} (margin: {summary['profit_margin']:.1f}%)")
        
        return {
            "agent": "Finance Agent",
            "finding": " | ".join(findings),
            "confidence": 0.92,
            "details": summary
        }
