import os
from dotenv import load_dotenv

load_dotenv()

class AIConfig:
    # Add .strip() to EVERY env var to remove newlines/spaces
    MODE = os.getenv("AI_MODE", "hybrid").strip()
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral").strip()
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434").strip()
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.2-3b-instruct:free").strip()
    FALLBACK_TO_LOCAL = True
