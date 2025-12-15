import os
from dotenv import load_dotenv

load_dotenv()

# Read directly from environment or use defaults
AI_CONFIG = {
    "default_backend": "gemini",
    "gemini_api_key": os.environ.get("GEMINI_API_KEY"),
    "ollama_host": os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
}
