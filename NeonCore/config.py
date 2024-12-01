import os

# Read directly from environment or use defaults
AI_CONFIG = {
    "default_backend": "grok",
    "xai_api_key": os.environ.get("XAI_API_KEY"),
    "xai_api_base": "https://api.x.ai/v1",
    "ollama_host": os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
}
