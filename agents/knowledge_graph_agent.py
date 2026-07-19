import networkx as nx
import pandas as pd
from pyvis.network import Network

class KnowledgeGraphAgent:
    def __init__(self):
        self.graph = nx.Graph()
        self.build_graph()
    
    def build_graph(self):
        """Build knowledge graph from CSV data"""
        try:
            # Load all data
            finance = pd.read_csv("data/finances.csv")
            inventory = pd.read_csv("data/inventory.csv")
            members = pd.read_csv("data/members.csv")
            orders = pd.read_csv("data/orders.csv")
            rules = pd.read_csv("data/company_rules.csv")
            
            # Add nodes for each entity type
            for _, row in finance.iterrows():
                self.graph.add_node(row['category'], type='category')
            
            for _, row in inventory.iterrows():
                self.graph.add_node(row['item_name'], type='product')
                self.graph.add_node(row['category'], type='category')
                self.graph.add_edge(row['item_name'], row['category'], relationship='belongs_to')
            
            for _, row in members.iterrows():
                self.graph.add_node(row['name'], type='member')
                self.graph.add_node(row['role'], type='role')
                self.graph.add_edge(row['name'], row['role'], relationship='has_role')
            
            for _, row in orders.iterrows():
                self.graph.add_node(row['customer'], type='customer')
                self.graph.add_edge(row['customer'], 'orders', relationship='has_order')
            
            # Add relationships
            for _, row in rules.iterrows():
                self.graph.add_node(row['rule_name'], type='rule')
                self.graph.add_node(row['category'], type='category')
                self.graph.add_edge(row['rule_name'], row['category'], relationship='applies_to')
        except:
            pass  # If files don't exist, just use empty graph
    
    def query_graph(self, entity_type=None, relationship=None):
        """Query the knowledge graph"""
        if entity_type:
            nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == entity_type]
            return nodes
        return list(self.graph.nodes)
    
    def get_connections(self, node):
        """Get all connections for a node"""
        if node in self.graph:
            return list(self.graph.neighbors(node))
        return []
    
    def visualize_graph(self):
        """Create interactive graph visualization"""
        net = Network(height="500px", width="100%", bgcolor="#1e2128", font_color="#ffffff")
        
        # Add nodes
        for node in self.graph.nodes():
            node_type = self.graph.nodes[node].get('type', 'unknown')
            color_map = {
                'category': '#ff6b6b',
                'product': '#4ecdc4',
                'member': '#45b7d1',
                'role': '#96ceb4',
                'customer': '#ffd93d',
                'rule': '#6c5ce7'
            }
            net.add_node(node, label=node, title=f"Type: {node_type}", 
                        color=color_map.get(node_type, '#808080'))
        
        # Add edges
        for edge in self.graph.edges():
            net.add_edge(edge[0], edge[1])
        
        return net
