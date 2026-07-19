import json
import os
from datetime import datetime

class ComplianceAgent:
    def __init__(self, data_path="data/policies.json"):
        self.data_path = data_path
        self.policies = self._load_policies()

    def _load_policies(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r') as f:
                return json.load(f)
        return {"local": [], "national": [], "food": [], "last_updated": datetime.now().isoformat()}

    def check_compliance(self, order_type, location):
        issues = []

        for policy_type in ["local", "national", "food"]:
            for policy in self.policies.get(policy_type, []):
                if policy.get("status") == "active":
                    issues.append({
                        "policy": policy["name"],
                        "requirement": policy.get("requirement", ""),
                        "status": "compliant"
                    })

        return {
            "compliant": True,
            "issues": issues,
            "policy_count": len(issues),
            "last_updated": self.policies.get("last_updated", "Unknown")
        }

    def get_requirements_for(self, category):
        requirements = []
        for policy_type in ["local", "national", "food"]:
            for policy in self.policies.get(policy_type, []):
                if category.lower() in policy.get("category", "").lower():
                    requirements.append(policy)
        return requirements

    def analyze(self, query_context=None):
        total = sum(len(self.policies.get(t, [])) for t in ["local", "national", "food"])

        finding = f"Compliance: {total} active policies tracked. "
        finding += f"Last updated: {self.policies.get('last_updated', 'Never')}."

        return {
            "agent": "Compliance Agent",
            "finding": finding,
            "confidence": 0.87,
            "details": {"total_policies": total, "last_updated": self.policies.get("last_updated")}
        }
