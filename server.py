
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
        self.cmd_handler = None  # Reference to AsyncCmd instance for completions

    def set_cmd_handler(self, cmd_handler):
        self.cmd_handler = cmd_handler

    async def send(self, text: str):
        """Send text message to client"""
        # Send as JSON to distinguish from other message types
        await self.websocket.send_json({"type": "output", "data": text})

    async def prompt(self, text: str = "") -> str:
        """Send prompt and wait for response"""
        # Send a specific 'prompt' message so the client knows this is the input prompt
        # and can render it correctly (e.g. in prompt_toolkit session)
        await self.websocket.send_json({"type": "prompt_request", "data": text})
            
        # Wait for input from client
        while True:
            # We sit in a loop handling "system" messages (like completions)
            # until we get actual "user input" to return to the game loop.
            try:
                raw_data = await self.websocket.receive_text()
                message = json.loads(raw_data)
                
                msg_type = message.get("type")
                
                if msg_type == "input":
                    cmd = message.get("data", "")
                    # print(f"Server received command: '{cmd}'")
                    return cmd
                
                elif msg_type == "complete":
                    # Handle completion request
                    if self.cmd_handler:
                        # Extract context
                        text_to_complete = message.get("text", "")
                        line_buffer = message.get("line", "")
                        begidx = message.get("begidx", 0)
                        endidx = message.get("endidx", 0)
                        
                        try:
                            matches = await self.cmd_handler.get_completions(
                                text_to_complete, line_buffer, begidx, endidx
                            )
                        except Exception as e:
                             print(f"Error getting completions: {e}")
                             matches = []
                        
                        resp = {
                            "type": "completion_result",
                            "matches": matches
                        }
                        await self.websocket.send_json(resp)
                    else:
                        print("Warning: completion requested but cmd_handler is None")
                        await self.websocket.send_json({"type": "completion_result", "matches": []})
                else:
                    print(f"Unknown message type: {msg_type}")
                    
            except json.JSONDecodeError:
                # Fallback for plain text (legacy client compatibility)
                return raw_data
            except WebSocketDisconnect:
                raise # Re-raise to let the main loop handle disconnect

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
    
    # Link the IO back to the game_manager (AsyncCmd) for completions
    io.set_cmd_handler(game_manager)
    
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
