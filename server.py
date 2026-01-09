
import asyncio
from typing import Any
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# Import core game components
from NeonCore.core.game_io import GameIO
from NeonCore.core.dependencies import GameDependencies
from NeonCore.utils.console_renderer import ConsoleRenderer

app = FastAPI()

class WebSocketIO(GameIO):
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket

    async def send(self, text: str):
        """Send text message to client"""
        await self.websocket.send_text(text)

    async def prompt(self, text: str = "") -> str:
        """Send prompt and wait for response"""
        if text:
            await self.send(text)
        # Wait for input from client
        data = await self.websocket.receive_text()
        return data

    async def display(self, data: Any, view_type: str = "text"):
        """
        Display structured data.
        For the MVP WebSocket client (which is terminal-like), 
        we will render it to ASCII text using ConsoleRenderer on the server side.
        In the future, we can send raw JSON-serialized data for a web frontend to render.
        """
        if view_type == "character_sheet":
             output = ConsoleRenderer.render_character_sheet(data)
             await self.send(output)
        else:
             await self.send(str(data))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"Client connected: {websocket.client}")
    
    # Create a wrapper IO for this connection
    io = WebSocketIO(websocket)
    
    # Initialize a fresh game instance for this player
    # This creates new CharacterManager, World, etc.
    game_manager = GameDependencies.initialize_game(io=io)
    
    try:
        # Start the game loop
        # cmdloop will call io.prompt() which awaits websocket.receive_text()
        await game_manager.cmdloop()
    except WebSocketDisconnect:
        print(f"Client disconnected: {websocket.client}")
    except Exception as e:
        print(f"Game session error: {e}")
        # Try to close if not already closed
        try:
            await websocket.close()
        except:
            pass
