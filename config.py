import os
from dotenv import load_dotenv

load_dotenv()

class AIConfig:
    # AI Mode
    MODE = os.getenv("AI_MODE", "hybrid").strip()
    
    # Local Ollama
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral").strip()
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434").strip()
    
    # Groq
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
    
    # External APIs
    OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY", "").strip()
    ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY", "").strip()
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "").strip()
    
    FALLBACK_TO_LOCAL = True
    
    # Decision Engine Weights
    DECISION_WEIGHTS = {
        "profitability": 0.30,
        "risk": 0.25,
        "capacity": 0.20,
        "compliance": 0.15,
        "sustainability": 0.10
    }
    
    # Thresholds
    PROFIT_THRESHOLD = 10000
    LOW_STOCK_THRESHOLD = 0.6
    COTTON_PRICE_THRESHOLD = 70
    RISK_HIGH_THRESHOLD = 0.7
