import networkx as nx
import pandas as pd
import json
import os
from pyvis.network import Network

class KnowledgeGraphAgent:
    def __init__(self):
        self.graph = nx.Graph()
        self._built = False
        self._build_graph()
    
    def _build_graph(self):
        try:
            # Load internal data
            files = {
                'finances': 'data/finances.csv',
                'inventory': 'data/inventory.csv',
                'members': 'data/members.csv',
                'orders': 'data/orders.csv',
                'rules': 'data/company_rules.csv'
            }
            data = {}
            for key, path in files.items():
                if os.path.exists(path):
                    data[key] = pd.read_csv(path)
                else:
                    data[key] = pd.DataFrame()
            
            # Build nodes and edges
            if not data['finances'].empty:
                for _, row in data['finances'].iterrows():
                    self.graph.add_node(row['category'], type='category')
            
            if not data['inventory'].empty:
                for _, row in data['inventory'].iterrows():
                    self.graph.add_node(row['item_name'], type='product')
                    self.graph.add_node(row['category'], type='category')
                    self.graph.add_edge(row['item_name'], row['category'], relationship='belongs_to')
            
            if not data['members'].empty:
                for _, row in data['members'].iterrows():
                    self.graph.add_node(row['name'], type='member')
                    self.graph.add_node(row['role'], type='role')
                    self.graph.add_edge(row['name'], row['role'], relationship='has_role')
            
            if not data['orders'].empty:
                for _, row in data['orders'].iterrows():
                    self.graph.add_node(row['customer'], type='customer')
                    self.graph.add_edge(row['customer'], 'orders', relationship='has_order')
            
            if not data['rules'].empty:
                for _, row in data['rules'].iterrows():
                    self.graph.add_node(row['rule_name'], type='rule')
                    self.graph.add_edge(row['rule_name'], row['category'], relationship='applies_to')
            
            # Add external policy nodes
            if os.path.exists('data/policies_ext.json'):
                with open('data/policies_ext.json', 'r') as f:
                    policies = json.load(f)
                    for p in policies.get('policies', []):
                        self.graph.add_node(p['name'], type='policy', category=p.get('category', 'general'))
                        self.graph.add_edge(p['name'], p.get('category', 'general'), relationship='regulates')
            
            self._built = True
        except Exception as e:
            print(f"KG build error: {e}")
            self._built = False
    
    def get_connections(self, node):
        if node in self.graph:
            return list(self.graph.neighbors(node))
        return []
    
    def get_nodes_by_type(self, node_type):
        return [n for n, d in self.graph.nodes(data=True) if d.get('type') == node_type]
    
    def visualize(self):
        if not self._built or len(self.graph.nodes) == 0:
            return None
        
        net = Network(height="550px", width="100%", bgcolor="#1a1f2a", font_color="#ffffff")
        
        color_map = {
            'category': '#ff6b6b',
            'product': '#4ecdc4',
            'member': '#45b7d1',
            'role': '#96ceb4',
            'customer': '#ffd93d',
            'rule': '#6c5ce7',
            'policy': '#ff8a65'
        }
        
        for node in self.graph.nodes():
            typ = self.graph.nodes[node].get('type', 'unknown')
            net.add_node(node, label=node, color=color_map.get(typ, '#808080'), title=f"Type: {typ}")
        
        for u, v in self.graph.edges():
            rel = self.graph.edges[u, v].get('relationship', 'connects')
            net.add_edge(u, v, title=rel)
        
        return net
