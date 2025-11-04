#!/usr/bin/env python3
"""
VibeCraft MCP Shared Server - HTTP/SSE Mode
A single server instance that multiple Claude clients can connect to
Shows all debug output in the terminal
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Set
import uuid

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("vibecraft.shared")

# Try to import required packages
try:
    from sse_starlette.sse import EventSourceResponse
    from starlette.applications import Starlette
    from starlette.routing import Route
    from starlette.responses import JSONResponse, Response
    from starlette.middleware.cors import CORSMiddleware
    import uvicorn
    HTTP_DEPS_AVAILABLE = True
except ImportError:
    HTTP_DEPS_AVAILABLE = False


class SharedMCPServer:
    """Shared MCP server that handles multiple clients"""

    def __init__(self):
        self.clients: Dict[str, asyncio.Queue] = {}
        self.app = None
        self.config = None
        self.rcon = None
        self.initialized = False

    async def initialize(self):
        """Initialize the MCP server components"""
        if self.initialized:
            return

        from vibecraft.server import app
        from vibecraft.config import load_config
        from vibecraft.rcon_manager import RCONManager

        # Load config
        self.config = load_config()
        self.config.enable_command_logging = True  # Force logging

        # Initialize RCON
        self.rcon = RCONManager(self.config)

        # Test connection
        logger.info("Testing RCON connection...")
        try:
            result = self.rcon.execute_command("list")
            logger.info(f"✅ RCON connected: {result}")
        except Exception as e:
            logger.error(f"❌ RCON failed: {e}")
            raise

        # Store the MCP app
        self.app = app
        self.initialized = True

        logger.info("✅ MCP Server initialized")

    async def handle_sse(self, request):
        """Handle SSE connections from Claude clients"""
        client_id = str(uuid.uuid4())
        logger.info(f"🔌 New SSE client connected: {client_id}")

        # Create queue for this client
        queue = asyncio.Queue()
        self.clients[client_id] = queue

        async def event_generator():
            """Generate SSE events for this client"""
            try:
                # Send initial connection event
                yield {
                    "event": "connected",
                    "data": json.dumps({
                        "client_id": client_id,
                        "server": "vibecraft",
                        "version": "1.0.0"
                    })
                }

                # Send events from queue
                while True:
                    try:
                        # Wait for events with timeout
                        event = await asyncio.wait_for(queue.get(), timeout=30.0)

                        # Send heartbeat if timeout
                        if event is None:
                            yield {
                                "event": "ping",
                                "data": json.dumps({"timestamp": datetime.now().isoformat()})
                            }
                        else:
                            yield event

                    except asyncio.TimeoutError:
                        # Send keepalive
                        yield {
                            "event": "ping",
                            "data": json.dumps({"timestamp": datetime.now().isoformat()})
                        }

            except asyncio.CancelledError:
                logger.info(f"🔌 SSE client disconnected: {client_id}")
                del self.clients[client_id]
                raise

        return EventSourceResponse(event_generator())

    async def handle_message(self, request):
        """Handle JSON-RPC messages from Claude clients"""
        try:
            # Get request body
            body = await request.body()
            message = json.loads(body)

            # Log the incoming message
            method = message.get("method", "unknown")
            msg_id = message.get("id")
            logger.info(f"← Message: {method} (id: {msg_id})")

            if "params" in message and method == "tools/call":
                tool_name = message["params"].get("name", "unknown")
                logger.info(f"  Tool: {tool_name}")
                logger.debug(f"  Args: {message['params'].get('arguments', {})}")

            # Process the message with our MCP app
            # This is where we'd integrate with the actual MCP server logic
            # For now, return a mock response
            response = await self.process_mcp_message(message)

            # Log the response
            logger.info(f"→ Response for id {msg_id}")
            logger.debug(f"  Result: {str(response.get('result', 'error'))[:100]}")

            return JSONResponse(response)

        except Exception as e:
            logger.error(f"Error handling message: {e}")
            return JSONResponse(
                {"error": {"code": -32603, "message": str(e)}},
                status_code=500
            )

    async def process_mcp_message(self, message):
        """Process MCP protocol messages"""
        # Initialize if needed
        if not self.initialized:
            await self.initialize()

        method = message.get("method")
        params = message.get("params", {})
        msg_id = message.get("id")

        # Handle different MCP methods
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "1.0.0",
                    "serverInfo": {
                        "name": "vibecraft",
                        "version": "1.0.0"
                    },
                    "capabilities": {
                        "tools": True,
                        "resources": True
                    }
                }
            }

        elif method == "tools/list":
            # Return available tools
            from vibecraft.server import get_tool_definitions
            tools = get_tool_definitions()
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"tools": tools}
            }

        elif method == "tools/call":
            # Execute tool
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})

            logger.info(f"🔧 Executing tool: {tool_name}")

            # Here we'd call the actual tool handler from vibecraft.server
            # For now, return a mock response
            result = await self.execute_tool(tool_name, tool_args)

            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": result
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }

    async def execute_tool(self, tool_name: str, arguments: dict):
        """Execute a VibeCraft tool"""
        # This would integrate with the actual tool handlers
        # For now, just log and return success
        logger.info(f"  Tool execution: {tool_name}")
        logger.debug(f"  Arguments: {arguments}")

        # Example: Execute RCON command if it's the rcon_command tool
        if tool_name == "rcon_command" and self.rcon:
            command = arguments.get("command")
            if command:
                try:
                    result = self.rcon.execute_command(command)
                    logger.info(f"  RCON result: {result[:100]}")
                    return {"output": result}
                except Exception as e:
                    logger.error(f"  RCON error: {e}")
                    return {"error": str(e)}

        return {"status": "ok", "tool": tool_name}

    def create_app(self):
        """Create Starlette application"""
        app = Starlette()

        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Root endpoint - SSE servers need this
        async def root(request):
            return JSONResponse({
                "url": "http://127.0.0.1:8765",
                "type": "sse",
                "name": "vibecraft-shared",
                "description": "VibeCraft Shared MCP Server"
            })

        # Add routes
        app.add_route("/", root, methods=["GET"])
        app.add_route("/sse", self.handle_sse, methods=["GET"])
        app.add_route("/messages", self.handle_message, methods=["POST"])

        # Health check
        async def health(request):
            return JSONResponse({
                "status": "healthy",
                "clients": len(self.clients),
                "initialized": self.initialized
            })

        app.add_route("/health", health, methods=["GET"])

        return app


async def main():
    """Main entry point"""
    if not HTTP_DEPS_AVAILABLE:
        print("\n❌ Missing HTTP/SSE dependencies!")
        print("\n📦 Install them with:")
        print("  cd /Users/er/Repos/vibecraft/mcp-server")
        print("  chmod +x install_http_deps.sh")
        print("  ./install_http_deps.sh")
        print("\nThen run again: python run_shared_server.py")
        sys.exit(1)

    print("\n" + "="*70)
    print("🌐 VibeCraft MCP Shared Server (HTTP/SSE Mode)")
    print("="*70)

    # Create shared server
    server = SharedMCPServer()

    # Initialize
    try:
        await server.initialize()
    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        print("\nMake sure:")
        print("  1. Minecraft server is running")
        print("  2. RCON is enabled and configured")
        sys.exit(1)

    # Create app
    app = server.create_app()

    print("\n✅ Server initialized successfully!")
    print("="*70)
    print("\n📡 Server URL: http://127.0.0.1:8765")
    print("\n📝 Add to Claude Desktop config:")
    print("""
{
  "mcpServers": {
    "vibecraft-shared": {
      "transport": "sse",
      "url": "http://127.0.0.1:8765"
    }
  }
}
""")
    print("👀 All debug output will appear here!")
    print("\nPress Ctrl+C to stop")
    print("="*70 + "\n")

    # Run server
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8765,
        log_level="info"
    )
    server_runner = uvicorn.Server(config)
    await server_runner.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Shared server stopped")