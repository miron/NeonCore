import os
import google.generativeai as genai
from .base import AIBackend
from ..config import AI_CONFIG


class GeminiBackend(AIBackend):
    def __init__(self):
        self.api_key = AI_CONFIG.get("gemini_api_key")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-2.5-flash")
        else:
            self.model = None

    def is_available(self):
        return self.api_key is not None

    def get_chat_completion(self, messages):
        if not self.is_available():
            raise Exception("Gemini API key not found")

        # Gemini 1.5 Flash supports system instructions in the model init.
        # We need to separate system prompt from the conversation history.
        system_instruction = None
        history = []
        last_user_message = ""

        # Simple robust parsing of role-based messages
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                system_instruction = content
            elif role == "user":
                last_user_message = content
            elif role == "assistant":
                # Map 'assistant' to 'model' for Gemini history
                history.append({"role": "model", "parts": [content]})

        try:
            # Re-instantiate model with system instruction if present (stateless optimization)
            model = genai.GenerativeModel(
                "gemini-2.5-flash", system_instruction=system_instruction
            )

            # TODO: If we want real multi-turn history, we would use start_chat(history=...)
            # But the current game loop seems to send the full context each time?
            # For now, we generate content based on the last message, assuming context is handled elsewhere
            # or integrated into the system prompt.
            # Reviewing do_talk: it sends a list with system + user. It's single turn.

            response = model.generate_content(last_user_message)
            return {"message": {"content": response.text}}

        except Exception as e:
            raise Exception(f"Gemini API request failed: {str(e)}")
