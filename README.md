# Tavus Pipecat Quickstart

A complete, production-ready starter project for building conversational AI bots with real-time video using [Pipecat](https://github.com/pipecat-ai/pipecat) and [Tavus](https://www.tavus.io/).

## 🎉 Hackathon Sponsorship

![Tavus Hackathon Sponsor](images/image.png)

**Tavus is proud to be sponsoring this year's hackathon!** We build APIs that let you create video agents, AI humans that can see, hear, and respond face-to-face in real time (and even take actions).

You can use Tavus in two ways:

**Full Pipeline**: Get everything out of the box: WebRTC, real-time ASR, Tavus LLM, and Phoenix, Sparrow, and Raven models for lifelike video. Spin up conversational video agents in minutes.

**Bring Your Own LLM**: Already have a stack? Plug in your LLM or TTS and use Tavus' perception, timing, and avatars for humanlike video conversations.

This repo implements the **Bring Your Own LLM** flow using Daily's Pipecat for real-time media handling and Google Gemini as the LLM backend.

## 🎥 What This Project Does

This project creates a conversational AI assistant that:
- **Listens** to your voice in real-time
- **Understands** what you're saying using speech recognition
- **Thinks** and generates intelligent responses using an LLM
- **Speaks** back with natural-sounding voice
- **Shows** a realistic video avatar (digital replica) speaking your response

All of this happens in real-time over WebRTC with sub-second latency!

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
