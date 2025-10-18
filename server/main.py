from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime
import asyncio
import json
import random
import string
from typing import List, Dict

app = FastAPI()

# Generate random username
def generate_username():
    adjectives = ["Swift", "Bold", "Clever", "Bright", "Sharp", "Quick", "Silent", "Fierce", "Calm", "Wise"]
    nouns = ["Eagle", "Wolf", "Fox", "Bear", "Hawk", "Lion", "Tiger", "Raven", "Shark", "Lynx"]
    return f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(10, 99)}"

# Store active connections with user info
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, str] = {}  # websocket -> user_id

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        user_id = generate_username()
        self.active_connections[websocket] = user_id
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] WebSocket connected: {user_id} (Total: {len(self.active_connections)})")

        # Send initial user info and user list to the new client
        await self.send_user_info(websocket, user_id)
        await self.broadcast_user_list()

        return user_id

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            user_id = self.active_connections[websocket]
            del self.active_connections[websocket]
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] WebSocket disconnected: {user_id} (Total: {len(self.active_connections)})")
            # Broadcast updated user list to remaining clients
            asyncio.create_task(self.broadcast_user_list())

    async def send_user_info(self, websocket: WebSocket, user_id: str):
        """Send user's own ID to them"""
        message = {
            "type": "user_info",
            "user_id": user_id
        }
        await websocket.send_text(json.dumps(message))

    async def broadcast_user_list(self):
        """Broadcast current user list to all clients"""
        user_list = list(self.active_connections.values())
        message = {
            "type": "user_list",
            "users": user_list
        }
        message_text = json.dumps(message)

        # Send to all connected clients
        for websocket in list(self.active_connections.keys()):
            try:
                await websocket.send_text(message_text)
            except Exception as e:
                print(f"Failed to send user list to client: {e}")
                # Remove failed connection
                if websocket in self.active_connections:
                    del self.active_connections[websocket]

    async def broadcast_space_event(self, message: bytes, sender: WebSocket):
        """Broadcast space bar event to all connected clients except the sender"""
        sender_id = self.active_connections.get(sender, "Unknown")
        print(f"Broadcasting space event from {sender_id} to {len(self.active_connections)} total connections")

        if len(self.active_connections) <= 1:
            print("No other clients to broadcast to")
            return

        # Create message with user ID
        value = int.from_bytes(message, byteorder='big')
        space_message = {
            "type": "space_event",
            "user_id": sender_id,
            "value": value
        }
        message_text = json.dumps(space_message)

        # Send to all clients except sender
        connections_to_notify = [conn for conn in self.active_connections.keys() if conn != sender]
        print(f"Broadcasting to {len(connections_to_notify)} other clients")

        for i, connection in enumerate(connections_to_notify):
            try:
                print(f"Sending to client {i+1}")
                await connection.send_text(message_text)
                print(f"Successfully sent to client {i+1}")
            except Exception as e:
                print(f"Failed to send to client {i+1}: {e}")
                # Remove failed connections
                if connection in self.active_connections:
                    del self.active_connections[connection]
                    print(f"Removed failed connection. Remaining: {len(self.active_connections)}")

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    user_id = await manager.connect(websocket)

    try:
        while True:
            print("Waiting for message...")
            data = await websocket.receive_bytes()
            print(f"Received raw data: {data.hex()}")
            # Convert binary data to boolean (0 or 1)
            value = int.from_bytes(data, byteorder='big')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(f"[{timestamp}] {user_id} - {value} (Broadcasting to {len(manager.active_connections)-1} other clients)")

            # Broadcast to other clients
            print("Starting broadcast...")
            await manager.broadcast_space_event(data, websocket)
            print("Broadcast completed")

    except WebSocketDisconnect:
        print("WebSocket disconnected")
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
