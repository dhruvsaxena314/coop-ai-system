import pandas as pd
import os

class CompanyRulesAgent:
    def __init__(self, data_path="data/company_rules.csv"):
        self.data_path = data_path
        self.rules = self._load_rules()

    def _load_rules(self):
        if os.path.exists(self.data_path):
            return pd.read_csv(self.data_path)
        return pd.DataFrame()

    def check_rule(self, action, category=None):
        if self.rules.empty:
            return {"allowed": True, "message": "No rules found"}

        relevant = self.rules
        if category:
            relevant = relevant[relevant['category'] == category]

        applicable = []
        for _, rule in relevant.iterrows():
            if rule['status'] == 'active':
                applicable.append(rule['rule_name'])

        return {
            "allowed": True,
            "applicable_rules": applicable,
            "count": len(applicable),
            "message": f"{len(applicable)} rules apply to this action"
        }

    def get_rules_by_category(self, category):
        if self.rules.empty:
            return []
        filtered = self.rules[self.rules['category'] == category]
        return filtered.to_dict('records')

    def add_rule(self, rule_name, category, description):
        new_rule = {
            'rule_id': f"R{len(self.rules) + 1:03d}",
            'rule_name': rule_name,
            'category': category,
            'description': description,
            'status': 'active',
            'date_added': pd.Timestamp.now().strftime('%Y-%m-%d')
        }
        self.rules = pd.concat([self.rules, pd.DataFrame([new_rule])], ignore_index=True)
        self.rules.to_csv(self.data_path, index=False)
        return new_rule

    def analyze(self, query_context=None):
        if self.rules.empty:
            return {
                "agent": "Company Rules Agent",
                "finding": "No company rules defined",
                "confidence": 0.5,
                "details": {}
            }

        active = len(self.rules[self.rules['status'] == 'active'])
        categories = self.rules['category'].unique().tolist()

        finding = f"Company has {active} active rules. "
        finding += f"Categories: {', '.join(categories)}."

        return {
            "agent": "Company Rules Agent",
            "finding": finding,
            "confidence": 0.9,
            "details": {
                "total_rules": len(self.rules),
                "active_rules": active,
                "categories": categories,
                "rules": self.rules.to_dict('records')
            }
        }
