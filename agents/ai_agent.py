import requests
import json
import ollama
from config import AIConfig

class FlexibleAIAgent:
    def __init__(self):
        self.mode = AIConfig.MODE
        self.local_model = AIConfig.OLLAMA_MODEL
        self.ollama_url = AIConfig.OLLAMA_URL
        self.fallback = AIConfig.FALLBACK_TO_LOCAL
        self.openrouter_key = AIConfig.OPENROUTER_API_KEY
        self.openrouter_model = AIConfig.OPENROUTER_MODEL
        
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
    
    def _query_openrouter(self, prompt):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.openrouter_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return None
        except:
            return None
    
    def chat(self, message):
        prompt = f"""
        You are an AI assistant for a cooperative business.
        Answer the following question based on your knowledge.
        
        Question: {message}
        
        Keep answers concise and actionable.
        """
        
        if self.mode == "local":
            if self.ollama_available:
                return self._query_local(prompt)
            return "Local AI not available. Please start Ollama or switch to web mode."
        
        elif self.mode == "web":
            response = self._query_openrouter(prompt)
            if response:
                return response
            return "OpenRouter API error. Check your API key or internet connection."
        
        elif self.mode == "hybrid":
            # Try OpenRouter first
            response = self._query_openrouter(prompt)
            if response:
                return response
            
            # Fallback to local
            if self.fallback and self.ollama_available:
                return self._query_local(prompt)
            
            return "All AI services unavailable. Please check your configuration."
        
        return "Invalid mode. Choose 'local', 'web', or 'hybrid'."
    
    def get_status(self):
        status = {
            "mode": self.mode,
            "ollama_available": self.ollama_available,
            "local_model": self.local_model if self.ollama_available else "Not running",
            "openrouter": "Configured" if self.openrouter_key else "Not configured",
            "openrouter_model": self.openrouter_model
        }
        return status
    
    def list_ollama_models(self):
        """Get list of available Ollama models"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [m['name'] for m in models]
            return []
        except:
            return []
    
    def set_local_model(self, model_name):
        """Change the local model"""
        self.local_model = model_name
        # Save to env or config for persistence
        return {"status": "updated", "model": model_name}
    
    def set_mode(self, mode):
        """Change the mode"""
        if mode in ['local', 'web', 'hybrid']:
            self.mode = mode
            return {"status": "updated", "mode": mode}
        return {"status": "error", "message": "Invalid mode"}
