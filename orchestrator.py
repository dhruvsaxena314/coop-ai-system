from agents.finance_agent import FinanceAgent
from agents.inventory_agent import InventoryAgent
from agents.hr_agent import HRAgent
from agents.logistics_agent import LogisticsAgent
from agents.compliance_agent import ComplianceAgent
from agents.company_rules_agent import CompanyRulesAgent
from agents.govt_agent import GovtAgent

class Orchestrator:
    def __init__(self):
        self.finance = FinanceAgent()
        self.inventory = InventoryAgent()
        self.hr = HRAgent()
        self.logistics = LogisticsAgent()
        self.compliance = ComplianceAgent()
        self.rules = CompanyRulesAgent()
        self.govt = GovtAgent()

    def analyze_query(self, query):
        agents = [
            self.finance.analyze(query),
            self.inventory.analyze(query),
            self.hr.analyze(query),
            self.logistics.analyze(query),
            self.compliance.analyze(query),
            self.rules.analyze(query),
            self.govt.analyze(query)
        ]

        risk_keywords = ["warning", "shortfall", "not available", "expires", "ban"]
        risk_count = 0
        for agent in agents:
            finding = agent["finding"].lower()
            if any(kw in finding for kw in risk_keywords):
                risk_count += 1

        if risk_count >= 3:
            recommendation = "High risk detected. Recommend review before proceeding."
            risk_level = "High"
            confidence = 0.8
        elif risk_count >= 1:
            recommendation = "Some risks identified. Proceed with caution."
            risk_level = "Medium"
            confidence = 0.9
        else:
            recommendation = "No significant risks. Proceed with the plan."
            risk_level = "Low"
            confidence = 0.95

        return {
            "agents": agents,
            "recommendation": recommendation,
            "risk_level": risk_level,
            "risk_count": risk_count,
            "confidence": confidence
        }

    def analyze_order(self, order_data):
        finance_check = self.finance.can_afford(order_data.get("total_cost", 0))
        inventory_check = self.inventory.check_availability(
            order_data.get("item_name", ""),
            order_data.get("quantity", 0)
        )
        hr_check = self.hr.check_capacity(
            order_data.get("task_type", ""),
            order_data.get("skill", "")
        )
        logistics_check = self.logistics.estimate_delivery(
            order_data.get("destination", ""),
            order_data.get("weight", 0)
        )
        compliance_check = self.compliance.check_compliance(
            order_data.get("order_type", ""),
            order_data.get("location", "")
        )
        rules_check = self.rules.check_rule(
            order_data.get("action", ""),
            order_data.get("category", "")
        )
        govt_check = self.govt.check_ban(
            order_data.get("product", ""),
            order_data.get("location", "")
        )

        can_proceed = all([
            finance_check["can_afford"],
            inventory_check["available"],
            hr_check["has_capacity"],
            rules_check["allowed"],
            not govt_check["has_bans"]
        ])

        return {
            "can_proceed": can_proceed,
            "finance": finance_check,
            "inventory": inventory_check,
            "hr": hr_check,
            "logistics": logistics_check,
            "compliance": compliance_check,
            "rules": rules_check,
            "govt": govt_check
        }
