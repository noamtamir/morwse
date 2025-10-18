# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Morwse is a real-time interactive space bar tool with WebSocket broadcasting. When users press the space bar, visual effects (background color, circle, audio sine wave, and morse code oscilloscope) are triggered locally and broadcast to all connected clients.

## Architecture

### Client-Server Structure
- **Client**: Single HTML file (`client/index.html`) containing vanilla JavaScript
- **Server**: FastAPI WebSocket server (`server/main.py`) for broadcasting events

### Communication Protocol
- WebSocket messages are sent as binary data (single byte: 0 for release, 1 for press)
- Server broadcasts space bar events to all connected clients except the sender
- All visual effects are always active (no mode switching)

### Key Components

**Server (`server/main.py`)**:
- `ConnectionManager`: Handles WebSocket connections and broadcasting
- Binary message protocol using `int.from_bytes()` and `Uint8Array`
- Detailed logging with timestamps for all events

**Client (`client/index.html`)**:
- Web Audio API for sine wave generation (440Hz local, 880Hz remote)
- Canvas-based morse code visualizer with scrolling animation
- Real-time WebSocket message handling for remote user events
- ESC key clears all effects and resets state

## Development Commands

### Start the WebSocket Server
```bash
cd server
uv run uvicorn main:app --reload
```
Server runs on `http://localhost:8000`

### Open the Client
Open `client/index.html` directly in a web browser. No build process required.

## Dependencies

- **Server**: Python 3.13+ with `uv` package manager, FastAPI, Uvicorn
- **Client**: Modern browser with WebSocket and Web Audio API support

## Testing the Application

1. Start the server
2. Open multiple browser tabs/windows with `client/index.html`
3. Press space bar in one tab - effects should appear in all connected tabs
4. Check server console for connection and message logs
5. Use ESC to clear effects

## Key Technical Details

- Audio requires user interaction to initialize (Web Audio API restriction)
- Canvas animations use `requestAnimationFrame` for smooth scrolling
- WebSocket reconnection is not implemented - refresh page if connection drops
- Remote user effects use orange color scheme vs green for local user