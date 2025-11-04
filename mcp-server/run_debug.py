#!/usr/bin/env python3
"""
VibeCraft MCP Server - Debug Mode with Visible Logging
Run this to see all MCP communication and RCON commands in your terminal
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import mcp.server.stdio
from vibecraft.server import app, config, rcon
from vibecraft.config import load_config
from vibecraft.rcon_manager import RCONManager


class DebugStdioTransport:
    """Wrapper for stdio transport that logs all messages"""

    def __init__(self, read_stream, write_stream):
        self.read_stream = read_stream
        self.write_stream = write_stream
        self.message_count = 0

    async def read(self):
        """Read from stdin and log"""
        while True:
            line = await self.read_stream.readline()
            if not line:
                break

            # Log incoming message
            self.message_count += 1
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

            try:
                # Try to parse as JSON for pretty printing
                msg = json.loads(line.decode())
                msg_type = msg.get("method", msg.get("type", "unknown"))
                print(f"\n[{timestamp}] ← IN #{self.message_count} ({msg_type})")

                # Show important details
                if "method" in msg:
                    if msg["method"] == "tools/call":
                        tool_name = msg.get("params", {}).get("name", "unknown")
                        print(f"  Tool: {tool_name}")
                        if "arguments" in msg.get("params", {}):
                            args = msg["params"]["arguments"]
                            print(f"  Args: {json.dumps(args, indent=2)}")

                # Show full message in debug
                print(f"  Full: {json.dumps(msg)[:200]}...")

            except json.JSONDecodeError:
                print(f"[{timestamp}] ← IN #{self.message_count} (raw)")
                print(f"  Data: {line.decode()[:100]}...")

            yield line

    async def write(self, data):
        """Write to stdout and log"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        try:
            # Try to parse as JSON for pretty printing
            msg = json.loads(data.decode())
            msg_type = msg.get("method", msg.get("type", "unknown"))
            print(f"\n[{timestamp}] → OUT ({msg_type})")

            # Show important details
            if "result" in msg:
                result = str(msg["result"])[:200]
                print(f"  Result: {result}...")

            # Show full message in debug
            print(f"  Full: {json.dumps(msg)[:200]}...")

        except json.JSONDecodeError:
            print(f"[{timestamp}] → OUT (raw)")
            print(f"  Data: {data.decode()[:100]}...")

        await self.write_stream.write(data)
        await self.write_stream.drain()


async def main_debug():
    """Run MCP server with debug logging"""
    global config, rcon

    print("\n" + "="*60)
    print("🔍 VibeCraft MCP Server - DEBUG MODE")
    print("="*60)

    # Load configuration
    config = load_config()

    # Force verbose logging
    config.enable_command_logging = True

    # Initialize RCON
    rcon = RCONManager(config)

    # Test RCON connection
    print(f"\n📡 RCON Host: {config.rcon_host}:{config.rcon_port}")
    print("Testing RCON connection...")

    try:
        result = rcon.execute_command("list")
        print(f"✅ RCON connected: {result}")
    except Exception as e:
        print(f"❌ RCON connection failed: {e}")
        print("\nMake sure:")
        print("  1. Minecraft server is running")
        print("  2. RCON is enabled in server.properties")
        print("  3. RCON password matches your .env file")
        return

    # Check WorldEdit
    try:
        result = rcon.execute_command("version WorldEdit")
        if "WorldEdit" in result:
            print(f"✅ WorldEdit detected")
    except:
        print("⚠️  WorldEdit not detected")

    print("\n" + "="*60)
    print("🚀 Debug Server Ready!")
    print("="*60)
    print("\n📝 How to connect Claude:")
    print("  1. Update claude_desktop_config.json:")
    print('     "command": "python3",')
    print('     "args": ["run_debug.py"],')
    print(f'     "cwd": "{Path(__file__).parent}",')
    print("\n  2. Restart Claude Desktop")
    print("\n👀 You'll see all MCP messages here!")
    print("="*60 + "\n")

    # Run with debug wrapper
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        # Wrap streams with debug logging
        debug_transport = DebugStdioTransport(read_stream, write_stream)

        # Create async iterables from streams
        async def read_messages():
            async for line in debug_transport.read():
                yield line

        # Run the app
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    try:
        asyncio.run(main_debug())
    except KeyboardInterrupt:
        print("\n\n👋 Debug server stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()