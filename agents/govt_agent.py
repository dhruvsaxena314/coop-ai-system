import json
import os
from datetime import datetime

class GovtAgent:
    def __init__(self, data_path="data/policies.json"):
        self.data_path = data_path
        self.policies = self._load_policies()

    def _load_policies(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r') as f:
                return json.load(f)
        return {"local": [], "national": [], "food": [], "last_updated": datetime.now().isoformat()}

    def get_policies(self, category=None):
        if category:
            return self.policies.get(category, [])
        return self.policies

    def check_ban(self, product, location=None):
        bans = []
        for policy_type in ["local", "national", "food"]:
            for policy in self.policies.get(policy_type, []):
                if "ban" in policy.get("requirement", "").lower():
                    bans.append(policy)
        return {"has_bans": len(bans) > 0, "bans": bans}

    def get_compliance_requirements(self, business_type):
        requirements = []
        for policy_type in ["local", "national", "food"]:
            for policy in self.policies.get(policy_type, []):
                if policy.get("status") == "active":
                    requirements.append({
                        "type": policy_type,
                        "name": policy["name"],
                        "requirement": policy["requirement"]
                    })
        return requirements

    def check_fssai_compliance(self, product_type):
        fssai_rules = self.policies.get("food", [])
        applicable = [r for r in fssai_rules if r["status"] == "active"]
        return {
            "compliant": len(applicable) > 0,
            "requirements": applicable,
            "last_updated": self.policies.get("last_updated", "Unknown")
        }

    def update_policies(self, new_policies):
        for category, policies in new_policies.items():
            if category in self.policies:
                self.policies[category] = policies
        self.policies["last_updated"] = datetime.now().isoformat()
        with open(self.data_path, 'w') as f:
            json.dump(self.policies, f, indent=2)
        return {"status": "updated", "last_updated": self.policies["last_updated"]}

    def analyze(self, query_context=None):
        total = sum(len(self.policies.get(t, [])) for t in ["local", "national", "food"])
        bans = self.check_ban(None)

        finding = f"Government policies: {total} active policies tracked. "
        if bans["has_bans"]:
            finding += f"Warning: {len(bans['bans'])} bans are in effect. "
        else:
            finding += "No active bans detected. "

        finding += f"Last updated: {self.policies.get('last_updated', 'Never')}."

        return {
            "agent": "Government Agent",
            "finding": finding,
            "confidence": 0.88,
            "details": {
                "total_policies": total,
                "policies_by_type": {t: len(self.policies.get(t, [])) for t in ["local", "national", "food"]},
                "bans": bans["bans"],
                "last_updated": self.policies.get("last_updated", "Never")
            }
        }
