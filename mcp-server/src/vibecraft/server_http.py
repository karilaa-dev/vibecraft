#!/usr/bin/env python3
"""
VibeCraft MCP Server - HTTP Mode
Runs as a standalone HTTP server that multiple Claude instances can connect to
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional
import logging

# Add parent directory to path so we can import vibecraft modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from vibecraft.server import app, main as stdio_main, config, rcon
from vibecraft.config import load_config
from vibecraft.rcon_manager import RCONManager

# Try to import SSE transport (may not be available in all MCP versions)
try:
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.routing import Route
    from starlette.responses import StreamingResponse
    import uvicorn
    HTTP_AVAILABLE = True
except ImportError:
    HTTP_AVAILABLE = False
    print("HTTP/SSE transport not available. Installing required packages...")
    print("Run: pip install 'mcp[sse]' starlette uvicorn")

logger = logging.getLogger("vibecraft.http")


async def handle_sse(request):
    """Handle SSE connections from Claude"""
    logger.info(f"New SSE connection from {request.client}")

    # Create SSE transport
    sse = SseServerTransport("/messages")

    # Run the MCP app with SSE transport
    async def stream():
        async with sse.get_read_stream() as read_stream, \
                   sse.get_write_stream() as write_stream:
            # Run the MCP server
            await app.run(read_stream, write_stream, app.create_initialization_options())

    return StreamingResponse(stream(), media_type="text/event-stream")


async def handle_messages(request):
    """Handle message posts from Claude"""
    logger.info(f"Message received from {request.client}")

    # Get the request body
    body = await request.body()

    # Process with SSE transport
    # This is handled by the SSE transport internally
    return {"status": "ok"}


def create_http_app():
    """Create Starlette app for HTTP/SSE transport"""
    if not HTTP_AVAILABLE:
        raise RuntimeError("HTTP/SSE transport not available. Install required packages.")

    # Create Starlette app with routes
    starlette_app = Starlette(
        routes=[
            Route("/sse", handle_sse, methods=["GET"]),
            Route("/messages", handle_messages, methods=["POST"]),
        ]
    )

    return starlette_app


async def run_http_server(host: str = "127.0.0.1", port: int = 8765):
    """Run VibeCraft as an HTTP/SSE server"""
    global config, rcon

    # Load configuration
    config = load_config()

    # Override some settings for HTTP mode
    config.enable_command_logging = True  # Always log in HTTP mode for debugging

    # Initialize RCON connection
    rcon = RCONManager(config)

    # Test RCON connection
    logger.info("=" * 60)
    logger.info("🎮 VibeCraft MCP Server Starting (HTTP Mode)...")
    logger.info("=" * 60)
    logger.info(f"RCON Host: {config.rcon_host}:{config.rcon_port}")
    logger.info(f"HTTP Server: http://{host}:{port}")
    logger.info("Testing RCON connection...")

    try:
        result = rcon.execute_command("list")
        logger.info(f"✅ RCON connection successful!")
        logger.info(f"   Players online: {result}")
    except Exception as e:
        logger.error(f"❌ RCON connection failed: {e}")
        logger.error("   Make sure Minecraft server is running with RCON enabled")
        return

    # Check for WorldEdit
    try:
        result = rcon.execute_command("version WorldEdit")
        if "WorldEdit" in result:
            import re
            version_match = re.search(r"WorldEdit.*?(\d+\.\d+\.\d+)", result)
            if version_match:
                logger.info(f"✅ WorldEdit {version_match.group(1)} detected")
        else:
            logger.warning("⚠️ WorldEdit not detected - some features may not work")
    except Exception as e:
        logger.warning(f"⚠️ Could not check WorldEdit version: {e}")

    logger.info("=" * 60)
    logger.info("🚀 VibeCraft HTTP Server Ready!")
    logger.info(f"   Connect Claude to: http://{host}:{port}")
    logger.info("   Press Ctrl+C to stop")
    logger.info("=" * 60)

    # Create and run HTTP app
    http_app = create_http_app()

    # Run with uvicorn
    config = uvicorn.Config(
        http_app,
        host=host,
        port=port,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


def main():
    """Main entry point for HTTP server"""
    # Set up logging for better visibility
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if not HTTP_AVAILABLE:
        print("\n❌ HTTP/SSE transport not available!")
        print("\nTo enable HTTP mode, install required packages:")
        print("  cd /Users/er/Repos/vibecraft/mcp-server")
        print("  source .venv/bin/activate")
        print("  pip install 'mcp[sse]' starlette uvicorn sse-starlette")
        print("\nThen run again:")
        print("  python -m src.vibecraft.server_http")
        sys.exit(1)

    # Run the HTTP server
    try:
        asyncio.run(run_http_server())
    except KeyboardInterrupt:
        print("\n\n👋 VibeCraft HTTP Server stopped")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()