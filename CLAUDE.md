# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Morwse is a real-time multi-user space bar interaction tool with WebSocket communication and per-user morse code visualization. Each user gets a randomly generated username and their own morse code visualization row with unique audio frequency.

## Architecture

### Client-Server Structure
- **Client**: Single HTML file (`index.html`) containing vanilla JavaScript
- **Server**: FastAPI WebSocket server (`server/main.py`) for user management and event broadcasting

### Communication Protocol
- WebSocket messages use JSON format for user info, user lists, and space events
- Server generates unique usernames (e.g., "SwiftEagle42") on connection
- Binary space bar data (0/1) sent from client, converted to JSON with user ID for broadcasting
- No backward compatibility with old binary-only protocol

### Key Components

**Server (`server/main.py`)**:
- `ConnectionManager`: Manages WebSocket connections with user IDs
- `generate_username()`: Creates random usernames using adjectives + animals + numbers
- JSON message protocol for `user_info`, `user_list`, and `space_event` types
- Detailed logging with usernames and timestamps

**Client (`index.html`)**:
- User identification system with `currentUserId` and `connectedUsers` tracking
- Per-user canvas-based morse code visualization (one horizontal row per user)
- Hash-based frequency generation (220Hz-880Hz range) for unique user audio tones
- User list display in top-right with current user highlighted
- No mode switching - all effects always active

## Development Commands

### Start the WebSocket Server
```bash
cd server
uv run uvicorn main:app --reload
```
Server runs on `http://localhost:8000`

### Open the Client
Open `index.html` directly in a web browser. Each window gets a unique username.

## Dependencies

- **Server**: Python 3.13+ with `uv` package manager, FastAPI, Uvicorn
- **Client**: Modern browser with WebSocket and Web Audio API support

## Testing the Application

1. Start the server
2. Open multiple browser tabs/windows with `index.html`
3. Each tab gets a unique username shown in top-right
4. Press space bar in any tab - morse visualization appears on that user's row in all tabs
5. Each user has distinct audio frequency based on username hash
6. Check server console for user connection and space event logs

## Key Technical Details

### User Management
- Usernames generated from adjectives + animals + numbers (e.g., "CleverWolf73")
- User list updates in real-time when users connect/disconnect
- Current user shown with "(Me)" suffix and white color

### Audio System
- Hash function converts usernames to frequencies: `220 + (Math.abs(hash) % 661)`
- Each user retains same frequency throughout session
- Current user volume: 0.3, remote users: 0.2

### Morse Code Visualization
- Each user gets individual canvas positioned to left of their name
- Canvas width: `calc(100vw - 140px)` to account for username space
- Right-to-left scrolling animation using `requestAnimationFrame`
- Current user: white morse lines, other users: green morse lines

### Message Protocol
- `user_info`: Server sends user their own ID
- `user_list`: Server broadcasts current user list to all clients
- `space_event`: Server broadcasts space events with user ID and value (0/1)