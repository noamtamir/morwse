# Morwse

A real-time multi-user space bar interaction tool with WebSocket communication and per-user morse code visualization.

## Features

- **Multi-user Support:** Each user gets a randomly generated username (e.g., "SwiftEagle42")
- **Real-time Synchronization:** Space bar events are broadcast to all connected users
- **Per-user Morse Code:** Each user has their own horizontal morse code visualization row
- **Unique Audio Frequencies:** Each user gets a distinct audio tone based on their username (220Hz-880Hz)
- **User List Display:** Shows all connected users with current user highlighted
- **Visual Effects:** Background color change and audio sine waves

## Quick Start

### 1. Start the WebSocket Server

```bash
cd server
uv run uvicorn main:app --reload
```

The server will run on `http://localhost:8000`

### 2. Open the Client

Open `client/index.html` in your web browser. Each browser window/tab will be assigned a unique username.

### 3. Use the Interface

- **Space Bar:** Hold to activate visual and audio effects (visible to all users)
- Open multiple browser windows to see multi-user interaction

## How It Works

- **User Identification:** Server generates unique usernames on connection
- **Real-time Broadcasting:** Space bar events are sent via WebSocket to all other users
- **Morse Code Visualization:** Each user gets a horizontal row that scrolls morse patterns from right to left
- **Audio Distinction:** Each user's username is hashed to generate a unique frequency between 220Hz and 880Hz

## Server Output

The server logs user connections and space bar events:

```
[2025-01-18 14:23:45.123] WebSocket connected: SwiftEagle42 (Total: 1)
[2025-01-18 14:23:45.456] SwiftEagle42 - 1 (Broadcasting to 0 other clients)
[2025-01-18 14:23:45.789] SwiftEagle42 - 0 (Broadcasting to 0 other clients)
```

## Requirements

- Python 3.13+ with `uv` package manager
- Modern web browser with WebSocket and Web Audio API support
