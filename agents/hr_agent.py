import pandas as pd
import os

class HRAgent:
    def __init__(self, data_path="data/members.csv"):
        self.data_path = data_path
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_path):
            return pd.read_csv(self.data_path)
        return pd.DataFrame()

    def get_available_members(self):
        if self.data.empty:
            return []
        return self.data[self.data['status'] == 'available'].to_dict('records')

    def check_capacity(self, task_type, required_skill):
        available = self.get_available_members()
        if not available:
            return {"has_capacity": False, "available_members": 0, "message": "No members available"}

        skilled = [m for m in available if required_skill.lower() in m['skills'].lower()]

        return {
            "has_capacity": len(skilled) > 0,
            "available_members": len(available),
            "skilled_members": len(skilled),
            "skilled_list": skilled
        }

    def get_workforce_summary(self):
        if self.data.empty:
            return {"total": 0, "available": 0, "on_leave": 0, "skills": []}

        total = len(self.data)
        available = len(self.data[self.data['status'] == 'available'])
        on_leave = len(self.data[self.data['status'] == 'on_leave'])
        skills = self.data['skills'].unique().tolist()

        return {"total": total, "available": available, "on_leave": on_leave, "skills": skills}

    def analyze(self, query_context=None):
        summary = self.get_workforce_summary()

        finding = f"Workforce: {summary['total']} members total, "
        finding += f"{summary['available']} available, "
        finding += f"{summary['on_leave']} on leave."

        return {
            "agent": "HR Agent",
            "finding": finding,
            "confidence": 0.9,
            "details": summary
        }
