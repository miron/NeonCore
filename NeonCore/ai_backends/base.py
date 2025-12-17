from abc import ABC, abstractmethod


class AIBackend(ABC):
    @abstractmethod
    def get_chat_completion(self, messages):
        pass

    @abstractmethod
    def is_available(self):
        """Check if the backend is available (API key set, service running, etc)"""
        pass
