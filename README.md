# Morwse

A space bar interaction tool with multiple modes and WebSocket logging.

## Features

- **5 Interactive Modes:**
  - Mode 1: Background color change
  - Mode 2: Green circle in center
  - Mode 3: Audio sine wave
  - Mode 4: Morse code oscilloscope visualizer
  - Mode 5: All effects combined
- **WebSocket Logging:** Server logs space bar events with timestamps
- **ESC Key:** Clear screen and reset to mode 1

## Quick Start

### 1. Start the WebSocket Server

```bash
cd server
uv run uvicorn main:app --reload
```

The server will run on `http://localhost:8000`

### 2. Open the Client

Open `client/index.html` in your web browser.

### 3. Use the Interface

- **Space Bar:** Hold to activate current mode effects
- **Keys 1-5:** Switch between modes
- **ESC:** Clear screen and reset to mode 1

## Server Output

The server will log space bar events with timestamps:

```
[2025-01-18 14:23:45.123] WebSocket connected
[2025-01-18 14:23:45.456] - 1
[2025-01-18 14:23:45.789] - 0
```

## Requirements

- Python with `uv` package manager
- Modern web browser with WebSocket support
