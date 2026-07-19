import json
import os
from datetime import datetime

class GovtPolicyAgent:
    def __init__(self, policy_file="data/policies_ext.json"):
        self.policy_file = policy_file
        self.policies = self._load_policies()
    
    def _load_policies(self):
        if os.path.exists(self.policy_file):
            try:
                with open(self.policy_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"policies": []}
    
    def get_active_policies(self, category=None):
        active = [p for p in self.policies.get("policies", []) if p.get("status", "active") == "active"]
        if category:
            active = [p for p in active if p.get("category", "").lower() == category.lower()]
        return active
    
    def get_policy_impact(self, policy_name, business_type="cooperative"):
        """Analyze impact of a specific policy"""
        for p in self.policies.get("policies", []):
            if p.get("name", "").lower() == policy_name.lower():
                return {
                    "name": p.get("name"),
                    "category": p.get("category"),
                    "description": p.get("description"),
                    "effective": p.get("effective", "Unknown"),
                    "impact_score": self._calculate_impact(p, business_type),
                    "action_required": p.get("action_required", "Review")
                }
        return None
    
    def _calculate_impact(self, policy, business_type):
        # Simplified impact scoring
        score = 0
        if policy.get("category") == "financial":
            score += 2
        if business_type == "cooperative" and "coop" in policy.get("description", "").lower():
            score += 1
        if policy.get("status") == "active":
            score += 1
        return min(score, 5)
    
    def analyze(self, context=None):
        active = self.get_active_policies()
        if not active:
            return {
                "agent": "Govt Policy Agent",
                "finding": "No active government policies tracked",
                "confidence": 0.5,
                "details": {}
            }
        
        # Categorize
        categories = {}
        for p in active:
            cat = p.get("category", "general")
            categories[cat] = categories.get(cat, 0) + 1
        
        finding = f"{len(active)} active policies tracked. Categories: {', '.join([f'{k}({v})' for k,v in categories.items()])}"
        
        # Highlight critical policies
        critical = [p for p in active if p.get("impact_score", 0) >= 4]
        if critical:
            finding += f" | Critical: {', '.join([p['name'] for p in critical])}"
        
        return {
            "agent": "Govt Policy Agent",
            "finding": finding,
            "confidence": 0.85,
            "details": {
                "total_policies": len(active),
                "categories": categories,
                "critical": critical,
                "all": active
            }
        }
