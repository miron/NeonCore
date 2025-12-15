import json
import urllib.request
from .base import AIBackend
from ..config import AI_CONFIG

class OllamaBackend(AIBackend):
    def __init__(self):
        self.host = AI_CONFIG["ollama_host"]
        self.model = AI_CONFIG["ollama_model"]

    def is_available(self):
        try:
            urllib.request.urlopen(f"{self.host}/api/tags")
            return True
        except:
            return False

    def get_chat_completion(self, messages):
        url = f"{self.host}/api/chat"
        headers = {"Content-Type": "application/json"}
        data = {"model": self.model, "messages": messages, "stream": False}

        req = urllib.request.Request(
            url, headers=headers, data=json.dumps(data).encode()
        )
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode())
