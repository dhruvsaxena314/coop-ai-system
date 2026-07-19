from agents.finance_agent import FinanceAgent
from agents.inventory_agent import InventoryAgent
from agents.hr_agent import HRAgent
from agents.logistics_agent import LogisticsAgent
from agents.compliance_agent import ComplianceAgent
from agents.company_rules_agent import CompanyRulesAgent
from agents.govt_agent import GovtAgent
from agents.external_agent import ExternalAgent
from agents.govt_policy_agent import GovtPolicyAgent
from agents.decision_engine import DecisionEngine
from agents.ai_agent import FlexibleAIAgent
from agents.analysis_agent import AnalysisAgent

class Orchestrator:
    def __init__(self):
        # Internal agents
        self.finance = FinanceAgent()
        self.inventory = InventoryAgent()
        self.hr = HRAgent()
        self.logistics = LogisticsAgent()
        self.compliance = ComplianceAgent()
        self.rules = CompanyRulesAgent()
        self.govt = GovtAgent()
        
        # External agents
        self.external = ExternalAgent()
        self.policy = GovtPolicyAgent()
        
        # Decision engine
        self.decision = DecisionEngine()
        
        # AI agents
        self.ai_agent = FlexibleAIAgent()
        self.analysis = AnalysisAgent()
    
    def analyze_query(self, query):
        """Main orchestration method"""
        # Step 1: Gather all data
        context = self._gather_context()
        
        # Step 2: Analyze with agents
        agent_results = self._run_agents(query, context)
        
        # Step 3: Decision engine evaluation
        decision = self._evaluate_decision(query, context)
        
        # Step 4: AI synthesis
        synthesis = self._synthesize(query, context, agent_results, decision)
        
        return {
            "context": context,
            "agents": agent_results,
            "decision": decision,
            "synthesis": synthesis
        }
    
    def _gather_context(self):
        """Gather all data into a single context"""
        finance = self.finance.get_summary()
        inventory = self.inventory.get_summary()
        members = self.hr.get_summary()
        orders = self.analysis.get_order_summary()
        external = self.external.get_all()
        policies = self.policy.get_active_policies()
        
        return {
            "finance": finance,
            "inventory": inventory,
            "members": members,
            "orders": orders,
            "external": external,
            "policies": policies,
            "timestamp": pd.Timestamp.now().isoformat()
        }
    
    def _run_agents(self, query, context):
        """Run all agents and collect results"""
        agents = [
            self.finance.analyze(query),
            self.inventory.analyze(query),
            self.hr.analyze(query),
            self.logistics.analyze(query),
            self.compliance.analyze(query),
            self.rules.analyze(query),
            self.govt.analyze(query),
            self.policy.analyze(query)
        ]
        return agents
    
    def _evaluate_decision(self, query, context):
        """Use decision engine"""
        # Compute risk
        risk = DecisionEngine.compute_risk_score(context)
        
        # Evaluate order if relevant
        order_eval = None
        if 'order' in query.lower() or 'accept' in query.lower():
            order_eval = DecisionEngine.evaluate_order({}, context)
        
        return {
            "risk_score": risk,
            "risk_level": "High" if risk > 0.7 else "Medium" if risk > 0.4 else "Low",
            "order_evaluation": order_eval,
            "recommendation": "Proceed" if risk < 0.5 else "Review" if risk < 0.7 else "Reconsider"
        }
    
    def _synthesize(self, query, context, agent_results, decision):
        """Synthesize everything into final response"""
        # Build context string for AI
        context_str = self._build_context_string(context)
        
        # Get AI response
        ai_response = self.ai_agent.chat(query, context_str)
        
        return {
            "response": ai_response,
            "risk": decision.get("risk_level"),
            "recommendation": decision.get("recommendation")
        }
    
    def _build_context_string(self, context):
        """Build context string for AI"""
        lines = []
        
        finance = context.get('finance')
        if finance:
            lines.append(f"FINANCES: Income Rs {finance.get('income', 0):,.0f}, Expenses Rs {finance.get('expenses', 0):,.0f}, Profit Rs {finance.get('profit', 0):,.0f}")
        
        inventory = context.get('inventory')
        if inventory:
            lines.append(f"INVENTORY: {inventory.get('total_items', 0)} items, low stock: {len(inventory.get('low_stock_items', []))}")
        
        members = context.get('members')
        if members:
            lines.append(f"MEMBERS: {members.get('available', 0)} of {members.get('total', 0)} available")
        
        external = context.get('external', {})
        if external.get('cotton'):
            lines.append(f"COTTON PRICE: ${external['cotton']}")
        if external.get('exchange'):
            lines.append(f"USD/INR: {external['exchange']}")
        if external.get('weather'):
            w = external['weather'][0]
            lines.append(f"WEATHER: {w['weather'][0]['description']}, {w['main']['temp']}°C")
        
        policies = context.get('policies', [])
        if policies:
            lines.append(f"GOVT POLICIES: {len(policies)} active")
        
        return "\n".join(lines)
