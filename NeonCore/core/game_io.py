import asyncio
from abc import ABC, abstractmethod
import sys
from typing import Any
from ..utils.console_renderer import ConsoleRenderer

class GameIO(ABC):
    """Abstract base class for Game Input/Output."""

    @abstractmethod
    async def send(self, text: str):
        """Send text to the client."""
        pass

    @abstractmethod
    async def prompt(self, text: str = "") -> str:
        """Get input from the client."""
        pass


class ConsoleIO(GameIO):
    """Standard Console I/O implementation."""

    async def send(self, text: str):
        print(text)


    async def prompt(self, text: str = "") -> str:
        # Run synchronous input() in a thread to avoid blocking the event loop
        # effectively making it async-compatible
        return await asyncio.to_thread(input, text)
