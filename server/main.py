from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime
import asyncio
from typing import List

app = FastAPI()

# Store active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] WebSocket connected (Total: {len(self.active_connections)})")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] WebSocket disconnected (Total: {len(self.active_connections)})")

    async def broadcast_to_others(self, message: bytes, sender: WebSocket):
        """Broadcast message to all connected clients except the sender"""
        print(f"Broadcasting to {len(self.active_connections)} total connections")
        if len(self.active_connections) <= 1:
            print("No other clients to broadcast to")
            return
            
        # Create a copy of connections to avoid modification during iteration
        connections_to_notify = [conn for conn in self.active_connections if conn != sender]
        print(f"Broadcasting to {len(connections_to_notify)} other clients")
        
        for i, connection in enumerate(connections_to_notify):
            try:
                print(f"Sending to client {i+1}")
                await connection.send_bytes(message)
                print(f"Successfully sent to client {i+1}")
            except Exception as e:
                print(f"Failed to send to client {i+1}: {e}")
                # Remove failed connections
                if connection in self.active_connections:
                    self.active_connections.remove(connection)
                    print(f"Removed failed connection. Remaining: {len(self.active_connections)}")

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        while True:
            print("Waiting for message...")
            data = await websocket.receive_bytes()
            print(f"Received raw data: {data.hex()}")
            # Convert binary data to boolean (0 or 1)
            value = int.from_bytes(data, byteorder='big')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(f"[{timestamp}] - {value} (Broadcasting to {len(manager.active_connections)-1} other clients)")
            
            # Broadcast to other clients
            print("Starting broadcast...")
            await manager.broadcast_to_others(data, websocket)
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
