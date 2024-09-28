import asyncio
import websockets
import threading

# Global variable to store connected clients
connected_clients = set()

# Port for WebSocket communication
PORT = 8765


async def handle_client(websocket, path):
    """Handle incoming connections from clients."""
    print(f"New client connected: {websocket.remote_address}")
    connected_clients.add(websocket)

    try:
        async for message in websocket:
            print(f"Message received from {websocket.remote_address}: {message}")
            await broadcast_message(message, websocket)
    except websockets.ConnectionClosed:
        print(f"Client {websocket.remote_address} disconnected.")
    finally:
        connected_clients.remove(websocket)


async def broadcast_message(message, sender_socket):
    """Broadcast a message to all connected clients except the sender."""
    for client in connected_clients:
        if client != sender_socket:  # Don't send the message back to the sender
            await client.send(message)


async def start_server():
    """Start the WebSocket server."""
    server = await websockets.serve(handle_client, '0.0.0.0', PORT)
    print(f"WebSocket server started on port {PORT}. Waiting for clients to connect...")
    await server.wait_closed()


def run_server():
    """Run the WebSocket server in a separate thread."""
    asyncio.run(start_server())


async def send_message(uri):
    """Send a message to a WebSocket server."""
    async with websockets.connect(uri) as websocket:
        while True:
            message = input("Enter message to send: ")
            await websocket.send(message)
            reply = await websocket.recv()
            print(f"Reply received: {reply}")


def start_client(uri):
    """Start the WebSocket client."""
    asyncio.run(send_message(uri))


if __name__ == "__main__":
    # Run the WebSocket server in a background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Allow user to connect to another WebSocket server
    target_uri = input("Enter the WebSocket server URI to connect (e.g., ws://localhost:8765): ")
    start_client(target_uri)
