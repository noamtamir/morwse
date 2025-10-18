from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime
import asyncio

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] WebSocket connected")
    
    try:
        while True:
            data = await websocket.receive_bytes()
            # Convert binary data to boolean (0 or 1)
            value = int.from_bytes(data, byteorder='big')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(f"[{timestamp}] - {value}")
            
    except WebSocketDisconnect:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] WebSocket disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
