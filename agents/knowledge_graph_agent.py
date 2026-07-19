import networkx as nx
import pandas as pd

class KnowledgeGraphAgent:
    def __init__(self):
        self.graph = nx.Graph()
        try:
            self.build_graph()
        except:
            pass
    
    def build_graph(self):
        try:
            # Load data
            finance = pd.read_csv("data/finances.csv")
            inventory = pd.read_csv("data/inventory.csv")
            members = pd.read_csv("data/members.csv")
            orders = pd.read_csv("data/orders.csv")
            rules = pd.read_csv("data/company_rules.csv")
            
            # Add nodes and edges
            for _, row in finance.iterrows():
                self.graph.add_node(row['category'], type='category')
            
            for _, row in inventory.iterrows():
                self.graph.add_node(row['item_name'], type='product')
                self.graph.add_node(row['category'], type='category')
                self.graph.add_edge(row['item_name'], row['category'])
            
            for _, row in members.iterrows():
                self.graph.add_node(row['name'], type='member')
                self.graph.add_node(row['role'], type='role')
                self.graph.add_edge(row['name'], row['role'])
            
            for _, row in orders.iterrows():
                self.graph.add_node(row['customer'], type='customer')
                self.graph.add_edge(row['customer'], 'orders')
            
            for _, row in rules.iterrows():
                self.graph.add_node(row['rule_name'], type='rule')
                self.graph.add_node(row['category'], type='category')
                self.graph.add_edge(row['rule_name'], row['category'])
        except Exception as e:
            print(f"Error building graph: {e}")
    
    def get_connections(self, node):
        if node in self.graph:
            return list(self.graph.neighbors(node))
        return []
    
    def get_graph_data(self):
        """Return graph data as dict for visualization"""
        nodes = []
        for node, attrs in self.graph.nodes(data=True):
            nodes.append({
                'id': node,
                'type': attrs.get('type', 'unknown'),
                'label': node
            })
        
        edges = []
        for u, v in self.graph.edges():
            edges.append({'from': u, 'to': v})
        
        return {'nodes': nodes, 'edges': edges}
