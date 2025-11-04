#!/usr/bin/env python3
"""
VibeCraft MCP Server - HTTP/SSE Mode
Run this for a single server instance that multiple Claude clients can connect to
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Force HTTP mode through environment variable
os.environ["MCP_TRANSPORT"] = "sse"

async def main():
    # Import after setting env vars
    from vibecraft.server import main as server_main

    print("\n" + "="*60)
    print("🌐 Starting VibeCraft in HTTP/SSE mode...")
    print("="*60)
    print("\n⚠️  Note: HTTP/SSE mode requires additional setup")
    print("  See instructions below if this fails\n")

    try:
        # Try to import SSE transport
        from mcp.server import Server
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Route
        from starlette.responses import Response, PlainTextResponse
        import uvicorn

        # Import our server app
        from vibecraft.server import app, config, rcon
        from vibecraft.config import load_config
        from vibecraft.rcon_manager import RCONManager

        # Initialize config and RCON
        config_obj = load_config()
        rcon_obj = RCONManager(config_obj)

        # Test RCON connection
        print("Testing RCON connection...")
        try:
            result = rcon_obj.execute_command("list")
            print(f"✅ RCON connected: {result}")
        except Exception as e:
            print(f"❌ RCON failed: {e}")
            return

        # Create SSE transport
        sse_transport = SseServerTransport("/messages")

        async def handle_sse(request):
            """Handle SSE endpoint"""
            print(f"New SSE connection from {request.client}")
            return sse_transport.handle_sse(request)

        async def handle_messages(request):
            """Handle messages endpoint"""
            print(f"Message from {request.client}")
            return await sse_transport.handle_message(request)

        # Create Starlette app
        starlette_app = Starlette(
            routes=[
                Route("/sse", endpoint=handle_sse, methods=["GET"]),
                Route("/messages", endpoint=handle_messages, methods=["POST"]),
            ],
        )

        # Add the MCP app to the transport
        @starlette_app.on_event("startup")
        async def startup():
            """Initialize MCP app with transport"""
            # Connect our MCP app to the SSE transport
            read_stream = await sse_transport.connect_stdin()
            write_stream = await sse_transport.connect_stdout()

            # Run MCP app
            asyncio.create_task(
                app.run(read_stream, write_stream, app.create_initialization_options())
            )

        # Configure and run
        print("\n" + "="*60)
        print("🚀 VibeCraft HTTP/SSE Server Ready!")
        print("="*60)
        print("\n📡 Server URL: http://127.0.0.1:8765")
        print("📝 Add to Claude config:")
        print('   "transport": ["sse"],')
        print('   "url": "http://127.0.0.1:8765"')
        print("\nPress Ctrl+C to stop\n")

        config = uvicorn.Config(
            starlette_app,
            host="127.0.0.1",
            port=8765,
            log_level="info",
        )
        server = uvicorn.Server(config)
        await server.serve()

    except ImportError as e:
        print("\n❌ Missing dependencies for HTTP/SSE mode!")
        print(f"   Error: {e}")
        print("\n📦 Install required packages:")
        print("   cd /Users/er/Repos/vibecraft/mcp-server")
        print("   source .venv/bin/activate")
        print("   pip install sse-starlette starlette uvicorn")
        print("\n   Then try again: python run_http.py")
        return

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Server stopped")