import os
from dotenv import load_dotenv

load_dotenv()

class AIConfig:
    MODE = os.getenv("AI_MODE", "hybrid")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")  # ← EMPTY
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.2-3b-instruct:free")
    FALLBACK_TO_LOCAL = True
