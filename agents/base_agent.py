from abc import ABC, abstractmethod
import pandas as pd
import os

class BaseAgent(ABC):
    def __init__(self):
        self.data = {}
        self._load_data()
    
    def _load_data(self):
        files = {
            'finances': 'data/finances.csv',
            'inventory': 'data/inventory.csv',
            'members': 'data/members.csv',
            'orders': 'data/orders.csv',
            'rules': 'data/company_rules.csv'
        }
        for key, path in files.items():
            try:
                if os.path.exists(path):
                    df = pd.read_csv(path)
                    if key == 'finances':
                        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
                    elif key == 'inventory':
                        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
                        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
                        df['reorder_level'] = pd.to_numeric(df['reorder_level'], errors='coerce')
                    elif key == 'orders':
                        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
                        df['total_value'] = pd.to_numeric(df['total_value'], errors='coerce')
                    self.data[key] = df
                else:
                    self.data[key] = pd.DataFrame()
            except Exception as e:
                print(f"Error loading {key}: {e}")
                self.data[key] = pd.DataFrame()
    
    @abstractmethod
    def analyze(self, context=None):
        pass
    
    @abstractmethod
    def get_summary(self):
        pass
    
    def get_metric(self, metric_name, default=0):
        summary = self.get_summary()
        return summary.get(metric_name, default) if summary else default
