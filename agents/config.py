import os
from dotenv import load_dotenv

load_dotenv()

class AIConfig:
    MODE = os.getenv("AI_MODE", "hybrid").strip()
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral").strip()
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434").strip()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
    FALLBACK_TO_LOCAL = True
