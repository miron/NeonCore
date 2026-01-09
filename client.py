
import asyncio
import websockets
import sys
import json
from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.patch_stdout import patch_stdout

# Queue for server responses that are NOT completions
msg_queue = asyncio.Queue()
# Queue specifically for completion responses
completion_queue = asyncio.Queue()

class RemoteCompleter(Completer):
    def __init__(self, websocket):
        self.websocket = websocket
    
    def get_completions(self, document, complete_event):
        """
        Synchronous method required by abstract base class.
        We rely on async implementation.
        """
        return []

    async def get_completions_async(self, document, complete_event):
        """
        Ask server for completions for the current document state.
        """
        text_full = document.text_before_cursor
        line = document.text
        # Prompt toolkit uses 0-indexed cursor position within the line
        endidx = document.cursor_position
        
        # Calculate begidx for current word
        last_sep = line.rfind(' ', 0, endidx)
        if last_sep == -1:
             begidx = 0
        else:
             begidx = last_sep + 1
             
        # The text to complete is just the word under cursor
        text_arg = line[begidx:endidx]
        
        req = {
            "type": "complete",
            "text": text_arg,
            "line": line,
            "begidx": begidx, 
            "endidx": endidx
        }
        
        await self.websocket.send(json.dumps(req))
        
        # Wait for the specific completion response
        # Note: This race condition assumes next 'completion_result' is ours.
        # In a real high-frequency app we'd use IDs, but for this it works.
        response = await completion_queue.get()
        
        matches = response.get("matches", [])
        # Deduplicate and sort, verifying strict uniqueness by stripping then adding space back
        # This addresses "double commands" and "auto-space" request
        unique_matches = sorted(list(set(m.rstrip() + " " for m in matches)))
        
        for m in unique_matches:
            # Fix overwrite bug: replace only the typed argument, not the full completion length
            # prompt_toolkit expects negative offset from cursor
            # e.g. replacing 'f', len=1 -> -1
            yield Completion(m, start_position=-len(text_arg))

async def receive_messages(websocket):
    """Listen for messages from the server."""
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get("type")
                
                if msg_type == "output":
                    # Print regular game output with flush to ensure prompt position is correct
                    # Use ANSI to render colors
                    text = data.get("data")
                    if text:
                        print_formatted_text(ANSI(text))
                    
                elif msg_type == "prompt_request":
                    # Signal input loop with new prompt
                    await msg_queue.put(data.get("data", "> "))

                elif msg_type == "completion_result":
                    # Put into completion queue for the Completer to pick up
                    await completion_queue.put(data)
                    
            except json.JSONDecodeError:
                # Legacy / Fallback
                print(message, end="")
                
    except websockets.exceptions.ConnectionClosed:
        print("\n[Connection closed by server]")

async def input_loop(websocket):
    """Rich input loop using prompt_toolkit."""
    # User requested cmd.Cmd-like behavior: No auto-dropdown, Tab to trigger.
    session = PromptSession(
        completer=RemoteCompleter(websocket),
        complete_while_typing=False,
    )
    
    while True:
        try:
            # Wait for the server to request input (and provide prompt text)
            # This ensures we don't show the prompt before the output is done
            prompt_text = await msg_queue.get()
            
            with patch_stdout():
                # Render the prompt received from server
                text = await session.prompt_async(ANSI(prompt_text))
                
            # Send input as JSON
            await websocket.send(json.dumps({"type": "input", "data": text}))
            
            if text.strip().lower() == "quit":
                # Wait for server to ack or close
                await asyncio.sleep(0.5)
                break
                
        except (EOFError, KeyboardInterrupt):
            await websocket.close()
            break

async def main():
    uri = "ws://localhost:8000/ws"
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected! Game starting...\n")
            
            receiver = asyncio.create_task(receive_messages(websocket))
            sender = asyncio.create_task(input_loop(websocket))
            
            # Wait for either to finish
            done, pending = await asyncio.wait(
                [receiver, sender],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            for task in pending:
                task.cancel()

    except ConnectionRefusedError:
        print("Error: Could not connect to server. Ensure 'server.py' is running.")
    except Exception as e:
        print(f"Error ({type(e)}): {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient Interrupted.")
