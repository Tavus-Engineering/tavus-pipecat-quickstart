# Quick Start Guide

This guide will help you set up and run the Tavus Pipecat Quickstart project. The application consists of two parts:
1. **Backend**: A Python bot server using Pipecat framework
2. **Frontend**: A React web app using Pipecat RTVI SDK

## Prerequisites

Before you begin, make sure you have:
- **Python 3.10+** installed
- **Node.js 14+** and **npm** installed
- API keys for:
  - Deepgram (Speech-to-Text)
  - Cartesia (Text-to-Speech)
  - Google (Gemini LLM)
  - Tavus (Video replica)

## Step 1: Get Your API Keys

Create a `.env` file in the project root with your API keys:

```bash
# Create .env file
touch .env
```

Add the following to your `.env` file:

```env
DEEPGRAM_API_KEY=your_deepgram_api_key_here
CARTESIA_API_KEY=your_cartesia_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
TAVUS_API_KEY=your_tavus_api_key_here
TAVUS_REPLICA_ID=your_tavus_replica_id_here
```

**Where to get API keys:**
- **Deepgram**: [https://console.deepgram.com/](https://console.deepgram.com/)
- **Cartesia**: [https://cartesia.ai/](https://cartesia.ai/)
- **Google (Gemini)**: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
- **Tavus**: [https://platform.tavus.io/](https://platform.tavus.io/)

## Step 2: Install Python Dependencies

This project uses [uv](https://docs.astral.sh/uv/) for fast Python dependency management.

### Option A: Using uv (Recommended)

1. **Install uv:**

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use pip
pip install uv
```

2. **Install dependencies:**

```bash
# uv will automatically create a virtual environment and install all dependencies
uv sync
```

### Option B: Using pip

If you prefer using traditional pip:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Step 3: Install Frontend Dependencies

The frontend uses the Pipecat RTVI SDK (`@pipecat-ai/client-js`) for WebRTC communication.

```bash
cd frontend
npm install
cd ..
```

## Step 4: Run the Application

You need to run two processes: the backend bot server and the frontend web app.

### Terminal 1: Start the Backend Bot Server

Open a terminal and run:

```bash
# If using uv:
uv run python tavus-pipecat.py --transport webrtc --host localhost --port 8080

# Or if using pip/venv:
# source .venv/bin/activate  # Activate your venv first
# python tavus-pipecat.py --transport webrtc --host localhost --port 8080
```

**Wait for this message before proceeding:**
```
🚀 Bot ready!
   → WebRTC transport listening on localhost:8080
```

This starts the Pipecat bot server on port 8080. The server uses the RTVI (Real-Time Voice Interaction) protocol, which ensures proper coordination between the client and server, preventing the bot's first turn from being dropped.

**What's happening in the backend:**
- The server initializes all AI services (Deepgram, Cartesia, Google Gemini, Tavus)
- Sets up a WebRTC transport for real-time communication
- Creates a processing pipeline that handles: speech-to-text → LLM → text-to-speech → video generation
- Listens for incoming WebRTC connections on `http://localhost:8080/api/offer`

### Terminal 2: Start the Frontend Web App

Open a **new terminal** and run:

```bash
cd frontend
npm start
```

The React app will automatically open in your browser at `http://localhost:3000`

**What's happening in the frontend:**
- The frontend uses the **Pipecat RTVI JavaScript SDK** (`@pipecat-ai/client-js`)
- It connects to the backend bot server at `http://localhost:8080`
- Establishes a WebRTC connection for real-time audio/video streaming
- Handles the RTVI handshake to ensure proper synchronization

### Step 5: Start Talking!

1. **Grant Permissions**: When the page loads, your browser will ask for camera and microphone permissions. Click "Allow" for both.

2. **Wait for Connection**: The app will connect to the bot server. You'll see status updates on screen.

3. **Start the Conversation**: Once connected, the bot will greet you with a video message. Start talking to have a conversation!

**Tips:**
- Speak clearly and at a normal pace
- Wait for the bot to finish speaking before responding (like a real conversation)
- The bot's video is generated in real-time by Tavus based on the AI's responses

## Troubleshooting

### Connection Issues

**Problem: "Failed to connect to bot server"**

Solution:
1. Make sure the backend bot server is running (Terminal 1)
2. Check that you see the "Bot ready!" message
3. Verify the bot is listening on port 8080
4. Check the backend terminal for error messages

**Problem: "Could not access camera/microphone"**

Solution:
1. Click "Allow" when your browser asks for permissions
2. Check that no other app is using your camera/microphone
3. Try refreshing the page
4. Check your browser's site settings (camera/microphone should be allowed)

**Problem: "Connection established but no video"**

Solution:
1. Check the backend terminal for Tavus-related errors
2. Verify your `TAVUS_API_KEY` and `TAVUS_REPLICA_ID` are correct in `.env`
3. Make sure your Tavus account has an active replica

**Problem: "Bot doesn't respond to my voice"**

Solution:
1. Check your microphone is working (test in system settings)
2. Speak clearly and at normal volume
3. Check backend terminal for Deepgram errors
4. Verify your `DEEPGRAM_API_KEY` is valid

**Problem: "No audio from bot"**

Solution:
1. Check your speaker/headphone volume
2. Check backend terminal for Cartesia errors
3. Verify your `CARTESIA_API_KEY` is valid
4. Try a different browser

### Debugging Steps

1. **Check Browser Console**
   - Open Developer Tools (F12 or Right-click → Inspect)
   - Go to the Console tab
   - Look for errors or connection messages
   - You should see: "Connecting to Pipecat server...", "WebRTC connection established", etc.

2. **Check Backend Logs**
   - Look at Terminal 1 (backend server)
   - You should see messages like:
     - "Starting bot"
     - "Client ready - setting bot ready"
     - "Bot is ready to start conversation"

3. **Verify Environment Variables**
   - Make sure your `.env` file exists in the project root
   - Check all required keys are present:
     ```
     DEEPGRAM_API_KEY=...
     CARTESIA_API_KEY=...
     GOOGLE_API_KEY=...
     TAVUS_API_KEY=...
     TAVUS_REPLICA_ID=...
     ```

4. **Test API Keys**
   - Verify each API key is active and has available credits
   - Check the respective service dashboards for any issues

### Still Having Issues?

If you're still experiencing problems:

1. **Restart both servers**: Stop both terminals (Ctrl+C) and restart them
2. **Clear browser cache**: Hard refresh the page (Ctrl+Shift+R or Cmd+Shift+R)
3. **Try a different browser**: Some browsers handle WebRTC differently
4. **Check firewall settings**: Make sure localhost:8080 and localhost:3000 are not blocked

## Understanding the Architecture

### How It Works

```
User speaks → Microphone → WebRTC → Backend Server
                                          ↓
                                    Deepgram STT
                                          ↓
                                    Google Gemini LLM
                                          ↓
                                    Cartesia TTS
                                          ↓
                                    Tavus Video
                                          ↓
Backend Server → WebRTC → Browser → Video Display
```

### The RTVI Protocol

This project uses the **RTVI (Real-Time Voice Interaction)** protocol, which provides:

- **Client-ready/Bot-ready Handshake**: Ensures both sides are synchronized before starting
- **No Dropped First Turn**: The bot's initial greeting is never lost
- **Better Audio Quality**: Optimized audio routing and reduced glitches
- **Event Coordination**: Client and server stay perfectly synchronized

### Tech Stack

**Backend (Python):**
- **Pipecat**: Framework for building voice AI applications
- **Deepgram**: Real-time speech-to-text
- **Cartesia**: High-quality text-to-speech
- **Google Gemini**: Large language model for conversation
- **Tavus**: Real-time video replica generation
- **WebRTC**: Real-time communication transport

**Frontend (React):**
- **React**: UI framework
- **Pipecat RTVI SDK**: JavaScript client for RTVI protocol
- **Small WebRTC Transport**: Lightweight WebRTC implementation

## Next Steps

Now that you have the quickstart running, you can:

1. **Customize the Bot's Personality**: Edit the system prompt in `tavus-pipecat.py` (line 135)
2. **Change the Voice**: Modify the `voice_id` in `tavus-pipecat.py` (line 114)
3. **Adjust Video Quality**: Change `video_out_width` and `video_out_height` in `tavus-pipecat.py` (lines 72-73)
4. **Try Different LLMs**: Pipecat supports OpenAI, Anthropic, and other LLM providers
5. **Customize the UI**: Edit the React components in `frontend/src/components/`

## Helpful Resources

### Documentation
- **Pipecat Documentation**: [https://docs.pipecat.ai/](https://docs.pipecat.ai/)
- **Pipecat RTVI Client Docs**: [https://docs.pipecat.ai/client/introduction](https://docs.pipecat.ai/client/introduction)
- **Tavus Documentation**: [https://docs.tavus.io/sections/introduction](https://docs.tavus.io/sections/introduction)
- **Deepgram Docs**: [https://developers.deepgram.com/](https://developers.deepgram.com/)
- **Cartesia Docs**: [https://docs.cartesia.ai/](https://docs.cartesia.ai/)

### Example Projects
- **Voice UI Kit**: [https://github.com/pipecat-ai/voice-ui-kit](https://github.com/pipecat-ai/voice-ui-kit) - Components and templates for building React voice AI applications
- **Pipecat Examples**: [https://github.com/pipecat-ai/pipecat-examples](https://github.com/pipecat-ai/pipecat-examples) - Example applications and patterns for building voice AI apps

### Tools
- **uv**: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/) - Fast Python package installer and resolver
