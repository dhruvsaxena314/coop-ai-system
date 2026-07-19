import networkx as nx
import pandas as pd
from pyvis.network import Network

class KnowledgeGraphAgent:
    def __init__(self):
        self.graph = nx.Graph()
        self._built = False
        self._build_graph()
    
    def _build_graph(self):
        try:
            # Load CSVs
            finance = pd.read_csv("data/finances.csv")
            inventory = pd.read_csv("data/inventory.csv")
            members = pd.read_csv("data/members.csv")
            orders = pd.read_csv("data/orders.csv")
            rules = pd.read_csv("data/company_rules.csv")
            
            # Nodes and edges
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
            
            self._built = True
        except Exception as e:
            print("KG build error:", e)
            self._built = False
    
    def get_connections(self, node):
        if node in self.graph:
            return list(self.graph.neighbors(node))
        return []
    
    def visualize(self):
        if not self._built or len(self.graph.nodes) == 0:
            return None
        net = Network(height="500px", width="100%", bgcolor="#1e2128", font_color="#ffffff")
        color_map = {
            'category': '#ff6b6b',
            'product': '#4ecdc4',
            'member': '#45b7d1',
            'role': '#96ceb4',
            'customer': '#ffd93d',
            'rule': '#6c5ce7'
        }
        for node in self.graph.nodes():
            typ = self.graph.nodes[node].get('type', 'unknown')
            net.add_node(node, label=node, color=color_map.get(typ, '#808080'))
        for u, v in self.graph.edges():
            net.add_edge(u, v)
        return net
