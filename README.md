# Tavus Pipecat Quickstart

A complete, production-ready starter project for building conversational AI bots with real-time video using [Pipecat](https://github.com/pipecat-ai/pipecat) and [Tavus](https://www.tavus.io/).

## 🎥 What This Project Does

This project creates a conversational AI assistant that:
- **Listens** to your voice in real-time
- **Understands** what you're saying using speech recognition
- **Thinks** and generates intelligent responses using an LLM
- **Speaks** back with natural-sounding voice
- **Shows** a realistic video avatar (digital replica) speaking your response

All of this happens in real-time over WebRTC with sub-second latency!

## ⚡ Key Features

### ✨ RTVI Protocol for Reliable Communication
This project uses the **Pipecat RTVI (Real-Time Voice Interaction)** protocol instead of raw WebRTC. Benefits:

- **No dropped first turn**: The bot's initial greeting is never lost
- **Better audio quality**: Reduced glitches and improved audio routing
- **Perfect synchronization**: Client and server stay coordinated
- **Smoother UX**: Better connection management and error handling

### 🚀 Modern Python Setup
Uses [`uv`](https://docs.astral.sh/uv/) for fast, reliable Python dependency management:

- **Fast**: Up to 10x faster than pip
- **Reliable**: Reproducible builds with lock file
- **Simple**: One command to install everything
- **Compatible**: Works with existing pip/venv workflows

### 🎬 Powered by Best-in-Class AI Services

- **🎤 Deepgram**: Industry-leading speech-to-text with real-time streaming
- **🗣️ Cartesia**: Ultra-realistic text-to-speech voices
- **🧠 Google Gemini**: Powerful LLM for natural conversations
- **🎥 Tavus**: AI Human Interaction
- **📡 WebRTC**: Low-latency peer-to-peer communication

## 🚀 Quick Start

**Get up and running in 5 minutes!** See **[QUICKSTART.md](QUICKSTART.md)** for detailed step-by-step instructions.

```bash
# 1. Install dependencies
uv sync                          # Backend (Python)
cd frontend && npm install       # Frontend (React)

# 2. Configure API keys in .env file
# (See QUICKSTART.md for where to get keys)

# 3. Run the app (2 terminals)
uv run python tavus-pipecat.py --transport webrtc --host localhost --port 8080
cd frontend && npm start

# 4. Open browser at http://localhost:3000 and start talking!
```

👉 **[See QUICKSTART.md for detailed instructions, troubleshooting, and API key setup](QUICKSTART.md)**

## 📁 Project Structure

```
tavus-pipecat-quickstart/
├── tavus-pipecat.py              # 🤖 Main bot server implementation
│                                  #    - Initializes AI services
│                                  #    - Creates processing pipeline
│                                  #    - Handles RTVI protocol
│
├── pyproject.toml                # 📦 Python dependencies (uv format)
├── requirements.txt              # 📦 Legacy requirements (pip format)
├── .env                          # 🔑 API keys (you create this)
│
├── frontend/                     # ⚛️ React web application
│   ├── src/
│   │   ├── webrtc-client.js      # 📡 RTVI WebRTC client wrapper
│   │   │                          #    - Connects to bot server
│   │   │                          #    - Handles media streams
│   │   │                          #    - Manages RTVI protocol
│   │   │
│   │   └── components/
│   │       └── VideoConversation.js  # 🎬 Main UI component
│   │                                  #    - Video display
│   │                                  #    - Controls (mute, camera)
│   │                                  #    - Connection status
│   │
│   └── package.json              # 📦 Frontend dependencies
│
├── QUICKSTART.md                 # 📖 Detailed setup guide
└── README.md                     # 📖 This file
```

## 🔧 How It Works

**High-Level Flow:**

```
You speak → 🎤 Deepgram (STT) → 🧠 Gemini (LLM) → 🗣️ Cartesia (TTS) → 🎥 Tavus (Video) → Bot responds
```

**Architecture:**

```
┌──────────────────┐
│  React Frontend  │  ← User's browser (camera/mic)
│   RTVI Client    │
└────────┬─────────┘
         │ WebRTC Connection
         ↓
┌──────────────────┐
│ Python Backend   │  ← Pipecat server
│  Processing      │     • Speech-to-Text (Deepgram)
│  Pipeline        │     • LLM Generation (Gemini)
│                  │     • Text-to-Speech (Cartesia)
│                  │     • Video Generation (Tavus)
└──────────────────┘
```

All processing happens in **real-time** with **sub-second latency** using the **RTVI protocol** for perfect client-server coordination.

## 🛠️ Technologies

### Backend (Python)
- **Pipecat Framework**: Voice AI pipeline orchestration
- **Deepgram**: Real-time speech-to-text
- **Cartesia**: High-quality text-to-speech
- **Google Gemini**: Large language model
- **Tavus**: AI video replica generation
- **WebRTC**: Real-time communication

### Frontend (JavaScript/React)
- **React**: UI framework
- **Pipecat RTVI SDK** (`@pipecat-ai/client-js`): RTVI protocol client
- **Small WebRTC Transport**: Lightweight WebRTC implementation

## 🎨 Customization

All the code is easily customizable:

- **Bot personality**: Edit system prompt in `tavus-pipecat.py`
- **Voice**: Change Cartesia `voice_id`
- **Video quality**: Adjust resolution settings
- **LLM provider**: Swap Gemini for OpenAI, Anthropic, etc.
- **UI**: Customize React components in `frontend/src/`

See [QUICKSTART.md](QUICKSTART.md#next-steps) for detailed customization examples.

## 📚 Learn More

- **[QUICKSTART.md](QUICKSTART.md)** - Complete setup guide with troubleshooting
- **[Pipecat Docs](https://docs.pipecat.ai/)** - Framework documentation
- **[Pipecat Examples](https://github.com/pipecat-ai/pipecat-examples)** - More example projects
- **[Pipecat Discord](https://discord.gg/pipecat)** - Community support

## 📄 License

See LICENSE file for details.
