def __init__(self):
    self.mode = AIConfig.MODE
    self.local_model = AIConfig.OLLAMA_MODEL
    self.ollama_url = AIConfig.OLLAMA_URL
    self.fallback = AIConfig.FALLBACK_TO_LOCAL
    
    # Groq settings
    self.groq_key = AIConfig.GROQ_API_KEY
    self.groq_model = AIConfig.GROQ_MODEL
    
    self.ollama_available = self._check_ollama()
