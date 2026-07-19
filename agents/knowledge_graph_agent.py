import networkx as nx
import pandas as pd
from pyvis.network import Network

class KnowledgeGraphAgent:
    def __init__(self):
        self.graph = nx.Graph()
        try:
            self.build_graph()
        except:
            pass  # Fail silently if files missing
    
    def build_graph(self):
        try:
            finance = pd.read_csv("data/finances.csv")
            inventory = pd.read_csv("data/inventory.csv")
            members = pd.read_csv("data/members.csv")
            orders = pd.read_csv("data/orders.csv")
            rules = pd.read_csv("data/company_rules.csv")
            
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
        except:
            pass
    
    def get_connections(self, node):
        if node in self.graph:
            return list(self.graph.neighbors(node))
        return []
    
    def visualize_graph(self):
        net = Network(height="500px", width="100%", bgcolor="#1e2128", font_color="#ffffff")
        
        for node in self.graph.nodes():
            node_type = self.graph.nodes[node].get('type', 'unknown')
            colors = {
                'category': '#ff6b6b',
                'product': '#4ecdc4',
                'member': '#45b7d1',
                'role': '#96ceb4',
                'customer': '#ffd93d',
                'rule': '#6c5ce7'
            }
            net.add_node(node, label=node, color=colors.get(node_type, '#808080'))
        
        for edge in self.graph.edges():
            net.add_edge(edge[0], edge[1])
        
        return net
