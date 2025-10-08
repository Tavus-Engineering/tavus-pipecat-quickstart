"""
Tavus Pipecat Quickstart Bot

This module implements a conversational AI bot using Pipecat framework with:
- Real-time video using Tavus replicas
- Speech-to-text with Deepgram
- Text-to-speech with Cartesia
- LLM with Google Gemini
- WebRTC transport with RTVI protocol

The bot uses the RTVI (Real-Time Voice Interaction) protocol to ensure proper
coordination between the client and server, preventing dropped first turns and
providing a better conversation experience.
"""

import os

import aiohttp
from dotenv import load_dotenv
from loguru import logger

# Pipecat audio processing components
from pipecat.audio.turn.smart_turn.base_smart_turn import SmartTurnParams
from pipecat.audio.turn.smart_turn.local_smart_turn_v3 import LocalSmartTurnAnalyzerV3
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.audio.vad.vad_analyzer import VADParams

# Pipecat core components
from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask

# Pipecat processors and aggregators
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
from pipecat.processors.frameworks.rtvi import RTVIProcessor

# Pipecat runner and transport
from pipecat.runner.types import RunnerArguments
from pipecat.runner.utils import create_transport

# Service integrations
from pipecat.services.cartesia.tts import CartesiaTTSService
from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.services.google.llm import GoogleLLMService
from pipecat.services.tavus.video import TavusVideoService
from pipecat.transports.base_transport import BaseTransport, TransportParams

# Load environment variables from .env file
# override=True ensures .env values take precedence over existing environment variables
load_dotenv(override=True)

# Transport configuration for different transport types
# We use a lambda function to delay instantiation until the transport is actually selected
# This prevents creating unnecessary objects for unused transports
transport_params = {
    "webrtc": lambda: TransportParams(
        # Enable audio input (user's microphone)
        audio_in_enabled=True,
        
        # Enable audio output (bot's voice)
        audio_out_enabled=True,
        
        # Enable video output (Tavus replica video)
        video_out_enabled=True,
        
        # Set to True for real-time video streaming (not pre-recorded)
        video_out_is_live=True,
        
        # Video resolution: 1280x720 (720p) - good balance of quality and bandwidth
        video_out_width=1280,
        video_out_height=720,
        
        # VAD (Voice Activity Detection) using Silero model
        # stop_secs=0.2 means the bot will wait 0.2 seconds of silence before processing
        vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.2)),
        
        # Smart turn analyzer for better conversation flow
        # Helps determine when it's the bot's turn to speak
        turn_analyzer=LocalSmartTurnAnalyzerV3(params=SmartTurnParams()),
    ),
}


async def run_bot(transport: BaseTransport, runner_args: RunnerArguments):
    """
    Main bot logic that sets up and runs the Pipecat pipeline
    
    This function:
    1. Initializes all service components (STT, TTS, LLM, Video)
    2. Sets up the conversation context and system prompt
    3. Creates a processing pipeline
    4. Configures RTVI protocol for client-server coordination
    5. Runs the pipeline and handles events
    
    Args:
        transport: The transport layer (e.g., WebRTC) for communication
        runner_args: Configuration arguments for the pipeline runner
    """
    logger.info(f"Starting bot")
    
    # Use aiohttp session for async HTTP requests (required by Tavus service)
    async with aiohttp.ClientSession() as session:
        # Initialize Speech-to-Text service using Deepgram
        # This converts the user's spoken words into text
        stt = DeepgramSTTService(api_key=os.getenv("DEEPGRAM_API_KEY"))

        # Initialize Text-to-Speech service using Cartesia
        # This converts the bot's text responses into natural-sounding speech
        # voice_id specifies which voice to use (this is a male voice)
        tts = CartesiaTTSService(
            api_key=os.getenv("CARTESIA_API_KEY"),
            voice_id="a167e0f3-df7e-4d52-a9c3-f949145efdab",  # Cartesia voice ID
        )

        # Initialize Large Language Model using Google Gemini
        # This generates intelligent responses to user queries
        llm = GoogleLLMService(api_key=os.getenv("GOOGLE_API_KEY"))

        # Initialize Tavus Video Service
        # This generates real-time video of a digital replica speaking
        # The replica_id identifies which Tavus replica to use
        tavus = TavusVideoService(
            api_key=os.getenv("TAVUS_API_KEY"),
            replica_id=os.getenv("TAVUS_REPLICA_ID"),
            session=session,
        )

        # Initialize conversation messages with a system prompt
        # The system prompt defines the bot's behavior and personality
        messages = [
            {
                "role": "system",
                "content": "You are a helpful LLM in a WebRTC call. Your goal is to demonstrate your capabilities in a succinct way. Your output will be converted to audio so don't include special characters in your answers. Respond to what the user said in a creative and helpful way.",
            },
        ]

        # Create LLM context to store conversation history
        # This maintains the full conversation between user and bot
        context = LLMContext(messages)
        
        # Context aggregator handles accumulating messages from both user and assistant
        # It splits into two processors: one for user messages, one for assistant responses
        context_aggregator = LLMContextAggregatorPair(context)

        # Create RTVI processor for proper client-ready/bot-ready handshake
        # This ensures the client and server are coordinated before starting the conversation
        # It prevents the bot's first turn from being dropped
        rtvi = RTVIProcessor()

        # Create the processing pipeline
        # The pipeline defines the flow of data through the system
        # Data flows from top to bottom through these processors
        pipeline = Pipeline(
            [
                transport.input(),                  # 1. Receive audio/video from user via WebRTC
                rtvi,                                # 2. RTVI processor handles client-server coordination
                stt,                                 # 3. Convert user's speech to text (Deepgram)
                context_aggregator.user(),           # 4. Add user's text to conversation context
                llm,                                 # 5. Generate response using LLM (Google Gemini)
                tts,                                 # 6. Convert response text to speech (Cartesia)
                tavus,                               # 7. Generate video of replica speaking (Tavus)
                transport.output(),                  # 8. Send audio/video to user via WebRTC
                context_aggregator.assistant(),      # 9. Add assistant's response to conversation context
            ]
        )

        # Create a pipeline task with configuration parameters
        task = PipelineTask(
            pipeline,
            params=PipelineParams(
                # Audio input sample rate (from user's microphone)
                # 16kHz is standard for speech recognition
                audio_in_sample_rate=16000,
                
                # Audio output sample rate (to user's speakers)
                # 24kHz provides higher quality audio output
                audio_out_sample_rate=24000,
                
                # Enable metrics collection for monitoring and debugging
                enable_metrics=True,
                
                # Enable usage metrics (e.g., API usage tracking)
                enable_usage_metrics=True,
            ),
            # Automatically stop the pipeline after this many seconds of inactivity
            # Helps prevent zombie sessions from consuming resources
            idle_timeout_secs=runner_args.pipeline_idle_timeout_secs,
        )

        # Event handler for when the client signals it's ready
        # This is part of the RTVI protocol handshake
        @rtvi.event_handler("on_client_ready")
        async def on_client_ready(rtvi):
            logger.info("Client ready - setting bot ready")
            
            # Signal to the client that the bot is ready to start
            # This completes the RTVI handshake
            await rtvi.set_bot_ready()
            
            # Add a system message to kick off the conversation
            # This tells the LLM to greet the user and start the interaction
            messages.append(
                {
                    "role": "system",
                    "content": "Start by greeting the user and ask how you can help.",
                }
            )
            
            # Queue an LLMRunFrame to trigger the LLM to generate the greeting
            # This starts the conversation flow
            await task.queue_frames([LLMRunFrame()])

        # Event handler for when the client disconnects
        @transport.event_handler("on_client_disconnected")
        async def on_client_disconnected(transport, client):
            logger.info(f"Client disconnected")
            # Cancel the pipeline task to clean up resources
            await task.cancel()

        # Create the pipeline runner
        # handle_sigint allows graceful shutdown on Ctrl+C
        runner = PipelineRunner(handle_sigint=runner_args.handle_sigint)

        # Run the pipeline task
        # This starts the bot and keeps it running until disconnected or cancelled
        await runner.run(task)


async def bot(runner_args: RunnerArguments):
    """
    Main bot entry point compatible with Pipecat Cloud
    
    This function is called by the Pipecat runner with command-line arguments.
    It creates the appropriate transport (WebRTC, Daily, etc.) and runs the bot.
    
    Args:
        runner_args: Configuration from command-line arguments (transport type, host, port, etc.)
    """
    # Create the transport based on the command-line arguments
    # For example: --transport webrtc --host localhost --port 8080
    transport = await create_transport(runner_args, transport_params)
    
    # Run the main bot logic
    await run_bot(transport, runner_args)


if __name__ == "__main__":
    # Import and run the Pipecat CLI
    # This handles command-line argument parsing and starts the bot
    # 
    # Example usage:
    #   python tavus-pipecat.py --transport webrtc --host localhost --port 8080
    # 
    # Available transports: webrtc, daily
    # The WebRTC transport is recommended for local development
    from pipecat.runner.run import main

    main()