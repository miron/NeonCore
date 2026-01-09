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
    async def display(self, data: Any, view_type: str = "text"):
        """Display structured data."""
        pass

    @abstractmethod
    async def prompt(self, text: str = "") -> str:
        """Get input from the client."""
        pass


from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.patch_stdout import patch_stdout

class LocalCompleter(Completer):
    def __init__(self, cmd_handler):
        self.cmd_handler = cmd_handler

    def get_completions(self, document, complete_event):
        """
        Synchronous method required by abstract base class.
        We rely on async implementation.
        """
        return []


    # We use get_completions_async to allow awaiting AsyncCmd
    async def get_completions_async(self, document, complete_event):
        if not self.cmd_handler:
            return

        text = document.text_before_cursor
        line = document.text
        endidx = document.cursor_position
        
        # Heuristic for begidx (start of current word)
        last_sep = line.rfind(' ', 0, endidx)
        if last_sep == -1:
             begidx = 0
        else:
             begidx = last_sep + 1
             
        # Extract the specific word being completed, NOT the full line
        text = line[begidx:endidx]
        

        try:
            # We mock endidx as cursor position
            matches = await self.cmd_handler.get_completions(text, line, begidx, endidx)
        except Exception as e:
            matches = []
        
        # matches contains full strings e.g. "take".
        # prompt_toolkit expects completion to replace the word.
        # Deduplicate and force space (consistency with remote client)
        unique_matches = sorted(list(set(m.rstrip() + " " for m in matches)))
        word = document.get_word_before_cursor()
        
        for m in unique_matches:
            # start_position must be negative length of the replacement
            # e.g. if replacing "f", start_position=-1
            s_pos = -len(text)
            if m.startswith(word):
                yield Completion(m, start_position=-len(word))
            else:
                yield Completion(m, start_position=s_pos)


class ConsoleIO(GameIO):
    """Standard Console I/O implementation using prompt_toolkit."""

    def __init__(self):
        self.cmd_handler = None
        self.session = None # Lazy init to avoid loop issues?

    def set_cmd_handler(self, cmd_handler):
        self.cmd_handler = cmd_handler
        # Initialize session here now that we have a handler
        self.session = PromptSession(
            completer=LocalCompleter(cmd_handler),
            complete_while_typing=False
        )

    async def send(self, text: str):
        # Use patch_stdout logic if we were in a loop, but simple print is usually fine
        # unless prompt is active. prompt_app usually handles this.
        print(text)

    async def display(self, data: Any, view_type: str = "text"):
        if view_type == "text":
             print(data)
        elif view_type == "character_sheet":
             output = ConsoleRenderer.render_character_sheet(data)
             print(output)
        else:
             print(f"[Unknown View: {view_type}] {data}")

    async def prompt(self, text: str = "") -> str:
        if self.session is None:
             # Fallback if no handler set yet (e.g. login screen? or just plain input)
             # or just init session without completer
             self.session = PromptSession()

        # We must allow async output to print above the prompt
        with patch_stdout():
            return await self.session.prompt_async(text)
