import requests
import json
import ollama
import time
from config import AIConfig

class FlexibleAIAgent:
    def __init__(self):
        self.mode = AIConfig.MODE
        self.local_model = AIConfig.OLLAMA_MODEL
        self.ollama_url = AIConfig.OLLAMA_URL
        self.fallback = AIConfig.FALLBACK_TO_LOCAL
        
        # Groq settings
        self.groq_key = AIConfig.GROQ_API_KEY
        self.groq_model = AIConfig.GROQ_MODEL
        
        self.ollama_available = self._check_ollama()
    
    def _check_ollama(self):
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def _query_local(self, prompt):
        try:
            response = ollama.chat(
                model=self.local_model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Local AI error: {str(e)}"
    
    def _query_groq(self, prompt):
        if not self.groq_key:
            return None
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.groq_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 800
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=15)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            elif response.status_code == 429:
                time.sleep(2)
                response = requests.post(url, headers=headers, json=data, timeout=15)
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
            return None
        except:
            return None
    
    def chat(self, message, data_context=None):
        """
        Main chat method with optional data context.
        
        Args:
            message: User's question
            data_context: Company data summary from AnalysisAgent
        """
        
        # Build prompt with data context if provided
        if data_context:
            prompt = f"""
You are an AI Decision Intelligence System for a cooperative business.
You have access to REAL company data. Use it to make decisions.

COMPANY DATA:
{data_context}

USER QUESTION: {message}

INSTRUCTIONS:
1. Use the data above to answer. Be specific with numbers.
2. If the question is about orders, check pending orders and value.
3. If about money, check income/expenses/profit.
4. If about inventory, check stock levels and low stock items.
5. If about members, check availability and skills.
6. Provide a clear, actionable recommendation.
7. Include specific data points from the company data.

Keep answers concise but data-driven.
"""
        else:
            prompt = f"""
You are an AI assistant for a cooperative business.
Answer the following question based on your knowledge.

Question: {message}

Keep answers concise and actionable.
"""
        
        # Route based on mode
        if self.mode == "local":
            if self.ollama_available:
                return self._query_local(prompt)
            return "Local AI not available. Please start Ollama or switch to web mode."
        
        elif self.mode == "web":
            response = self._query_groq(prompt)
            if response:
                return response
            if self.ollama_available:
                return self._query_local(prompt)
            return "Groq API error. Check your API key or internet connection."
        
        elif self.mode == "hybrid":
            response = self._query_groq(prompt)
            if response:
                return response
            if self.fallback and self.ollama_available:
                return self._query_local(prompt)
            return "AI service unavailable. Please check your configuration."
        
        return "Invalid mode. Choose 'local', 'web', or 'hybrid'."
    
    def get_status(self):
        status = {
            "mode": self.mode,
            "ollama_available": self.ollama_available,
            "local_model": self.local_model if self.ollama_available else "Not running",
            "groq": "Configured" if self.groq_key else "Not configured",
            "groq_model": self.groq_model
        }
        return status
    
    def list_ollama_models(self):
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [m['name'] for m in models]
            return []
        except:
            return []
    
    def set_local_model(self, model_name):
        self.local_model = model_name
        return {"status": "updated", "model": model_name}
    
    def set_mode(self, mode):
        if mode in ['local', 'web', 'hybrid']:
            self.mode = mode
            return {"status": "updated", "mode": mode}
        return {"status": "error", "message": "Invalid mode"}
