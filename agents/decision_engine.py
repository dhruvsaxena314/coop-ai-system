import numpy as np
from config import AIConfig

class DecisionEngine:
    @staticmethod
    def topsis(alternatives, criteria, weights, impacts):
        """
        TOPSIS Multi-Criteria Decision Making
        
        Args:
            alternatives: list of dicts with criteria values
            criteria: list of criteria names
            weights: list of weights (sum to 1)
            impacts: list of '+' or '-' for benefit/cost
        """
        if not alternatives:
            return []
        
        # Build matrix
        matrix = np.array([[alt.get(c, 0) for c in criteria] for alt in alternatives])
        
        # Normalize
        norm_matrix = matrix / np.sqrt((matrix**2).sum(axis=0) + 1e-9)
        
        # Weighted
        weighted = norm_matrix * np.array(weights)
        
        # Ideal and anti-ideal
        ideal = []
        anti_ideal = []
        for i, imp in enumerate(impacts):
            if imp == '+':
                ideal.append(weighted[:, i].max())
                anti_ideal.append(weighted[:, i].min())
            else:
                ideal.append(weighted[:, i].min())
                anti_ideal.append(weighted[:, i].max())
        
        # Distance
        S_plus = np.sqrt(((weighted - ideal)**2).sum(axis=1))
        S_minus = np.sqrt(((weighted - anti_ideal)**2).sum(axis=1))
        
        # Performance score
        scores = S_minus / (S_plus + S_minus + 1e-9)
        
        # Add scores to alternatives
        for i, alt in enumerate(alternatives):
            alt['score'] = round(scores[i], 4)
            alt['rank'] = int(np.sum(scores > scores[i]) + 1)
        
        return sorted(alternatives, key=lambda x: x['score'], reverse=True)
    
    @classmethod
    def evaluate_order(cls, order_data, context):
        """
        Evaluate an order decision using TOPSIS
        """
        # Extract metrics from context
        finance = context.get('finance', {})
        inventory = context.get('inventory', {})
        members = context.get('members', {})
        
        # Define alternatives
        alternatives = [
            {
                "name": "Accept Order",
                "profitability": finance.get('profit', 0) / 10000,
                "risk": 1.0 - (members.get('available', 0) / max(members.get('total', 1), 1)),
                "capacity": inventory.get('total_items', 0) / 100,
                "compliance": 1.0,
                "sustainability": 0.8 if inventory.get('low_stock_items', 0) < 3 else 0.4
            },
            {
                "name": "Reject Order",
                "profitability": 0.1,
                "risk": 0.0,
                "capacity": 0.0,
                "compliance": 1.0,
                "sustainability": 1.0
            },
            {
                "name": "Defer Order (30 days)",
                "profitability": 0.5,
                "risk": 0.3,
                "capacity": 0.6,
                "compliance": 0.9,
                "sustainability": 0.7
            }
        ]
        
        criteria = ['profitability', 'risk', 'capacity', 'compliance', 'sustainability']
        weights = [
            AIConfig.DECISION_WEIGHTS.get('profitability', 0.30),
            AIConfig.DECISION_WEIGHTS.get('risk', 0.25),
            AIConfig.DECISION_WEIGHTS.get('capacity', 0.20),
            AIConfig.DECISION_WEIGHTS.get('compliance', 0.15),
            AIConfig.DECISION_WEIGHTS.get('sustainability', 0.10)
        ]
        impacts = ['+', '-', '+', '+', '+']
        
        return cls.topsis(alternatives, criteria, weights, impacts)
    
    @classmethod
    def compute_risk_score(cls, context):
        """Compute overall risk score (0-1)"""
        risk = 0.0
        
        # Financial risk
        finance = context.get('finance', {})
        if finance.get('profit', 0) < 0:
            risk += 0.3
        
        # Inventory risk
        inventory = context.get('inventory', {})
        if inventory.get('low_stock_items', 0) > 5:
            risk += 0.2
        
        # HR risk
        members = context.get('members', {})
        if members.get('available', 0) < members.get('total', 1) * 0.5:
            risk += 0.2
        
        # External risk
        external = context.get('external', {})
        if external.get('cotton', 0) and float(external['cotton']) > 70:
            risk += 0.15
        
        # Weather risk
        weather = external.get('weather', [])
        if weather and 'rain' in weather[0].get('weather', [{}])[0].get('description', '').lower():
            risk += 0.15
        
        return min(risk, 1.0)
