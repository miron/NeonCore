
import asyncio
import websockets
import sys

async def receive_messages(websocket):
    """Listen for messages from the server and print them."""
    try:
        async for message in websocket:
            sys.stdout.write(message)
            sys.stdout.flush()
    except websockets.exceptions.ConnectionClosed:
        print("\n[Connection closed by server]")

async def send_messages(websocket):
    """Read input from stdin and send to server."""
    loop = asyncio.get_running_loop()
    try:
        while True:
            # Use run_in_executor to make input() non-blocking
            message = await loop.run_in_executor(None, input)
            await websocket.send(message)
            if message.strip().lower() == "quit":
                # Let the server handle the quit command, but we can also break here
                # waiting a bit for server response before closing
                await asyncio.sleep(0.5) 
                break
    except EOFError:
        pass

async def main():
    uri = "ws://localhost:8000/ws"
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected! Game starting...\n")
            
            receiver = asyncio.create_task(receive_messages(websocket))
            sender = asyncio.create_task(send_messages(websocket))
            
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
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient Interrupted.")
