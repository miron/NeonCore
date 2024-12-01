from openai import OpenAI
from .base import AIBackend
from ..config import AI_CONFIG # Import the config

class GrokBackend(AIBackend):
    def __init__(self):
        self.api_key = AI_CONFIG["xai_api_key"]
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=AI_CONFIG["xai_api_base"]
            )
        else:
            self.client = None

    def is_available(self):
        return self.client is not None

    def get_chat_completion(self, messages):
        if not self.is_available():
            raise Exception("Grok API key not found")

        try:
            completion = self.client.chat.completions.create(
                model="grok-beta",
                messages=messages
            )
            return {"message": {"content": completion.choices[0].message.content}}
        except Exception as e:
            raise Exception(f"Grok API request failed: {str(e)}")
