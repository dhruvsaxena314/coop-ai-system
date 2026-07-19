import json
import os
from datetime import datetime

class GovtAgent:
    def __init__(self):
        self.data = self._load_data()
    
    def _load_data(self):
        # Load from policies_ext.json if exists
        if os.path.exists('data/policies_ext.json'):
            try:
                with open('data/policies_ext.json', 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"policies": []}
    
    def check_ban(self, product, location=None):
        """Check if a product is banned"""
        bans = []
        for p in self.data.get('policies', []):
            if 'ban' in p.get('description', '').lower():
                bans.append(p)
        return {"has_bans": len(bans) > 0, "bans": bans}
    
    def get_compliance_requirements(self, business_type="cooperative"):
        """Get compliance requirements for the business"""
        requirements = []
        for p in self.data.get('policies', []):
            if p.get('status') == 'active':
                requirements.append({
                    "name": p.get('name'),
                    "category": p.get('category', 'general'),
                    "requirement": p.get('description', '')
                })
        return requirements
    
    def analyze(self, context=None):
        policies = self.data.get('policies', [])
        if not policies:
            return {
                "agent": "Government Agent",
                "finding": "No government policies or bans tracked",
                "confidence": 0.5,
                "details": {}
            }
        
        active = [p for p in policies if p.get('status') == 'active']
        finding = f"Tracking {len(active)} active government policies. "
        bans = self.check_ban(None)
        if bans['has_bans']:
            finding += f"⚠️ {len(bans['bans'])} bans in effect."
        else:
            finding += "No active bans detected."
        
        return {
            "agent": "Government Agent",
            "finding": finding,
            "confidence": 0.85,
            "details": {
                "total_policies": len(active),
                "bans": bans
            }
        }
    
    def get_summary(self):
        policies = self.data.get('policies', [])
        active = [p for p in policies if p.get('status') == 'active']
        return {
            "total_policies": len(policies),
            "active_policies": len(active),
            "categories": list(set(p.get('category', 'general') for p in policies))
        }
