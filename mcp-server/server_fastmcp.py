#!/usr/bin/env python3
"""
VibeCraft MCP Server - FastMCP Implementation
A proper MCP server using FastMCP that can run as HTTP/SSE
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fastmcp import FastMCP

# Import VibeCraft modules
from vibecraft.config import load_config
from vibecraft.rcon_manager import RCONManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("vibecraft.fastmcp")

# Create the MCP server
mcp = FastMCP("vibecraft")

# Global instances
config = None
rcon = None

def initialize():
    """Initialize VibeCraft components"""
    global config, rcon

    if config is None:
        config = load_config()
        config.enable_command_logging = True  # Always log in shared mode

        rcon = RCONManager(config)

        # Test RCON connection
        try:
            result = rcon.execute_command("list")
            logger.info(f"✅ RCON connected: {result}")
        except Exception as e:
            logger.error(f"❌ RCON connection failed: {e}")
            raise


# ============================================
# RCON Command Tool
# ============================================

@mcp.tool()
def rcon_command(command: str, description: Optional[str] = None) -> str:
    """
    Execute any Minecraft or WorldEdit command via RCON.

    Args:
        command: The command to execute (without leading /)
        description: Optional description of what this command does

    Returns:
        The server's response
    """
    initialize()

    if description:
        logger.info(f"Executing: {description}")

    try:
        result = rcon.execute_command(command)
        logger.info(f"Command: {command}")
        logger.info(f"Response: {result[:200]}")
        return result
    except Exception as e:
        error_msg = f"Command failed: {str(e)}"
        logger.error(error_msg)
        return error_msg


# ============================================
# WorldEdit Tools
# ============================================

@mcp.tool()
def worldedit_selection(command: str) -> str:
    """
    WorldEdit Selection Commands - Define and manipulate the selected region.

    Commands:
    - pos1 X,Y,Z - Set first corner
    - pos2 X,Y,Z - Set second corner
    - expand <amount> [direction]
    - size - Get selection info

    Note: Use comma-separated coordinates from console!

    Args:
        command: Selection command (e.g., 'pos1 100,64,100')

    Returns:
        Command result
    """
    initialize()

    # Add // prefix if not present
    if not command.startswith("//"):
        command = f"//{command}"

    return rcon.execute_command(command)


@mcp.tool()
def worldedit_region(command: str) -> str:
    """
    WorldEdit Region Commands - Modify the selected region.

    Commands:
    - set <pattern> - Fill region
    - replace [from] <to> - Replace blocks
    - walls <pattern> - Build walls
    - move [count] [direction] - Move region
    - stack [count] [direction] - Duplicate region

    Args:
        command: Region command (e.g., 'set stone')

    Returns:
        Command result
    """
    initialize()

    # Add // prefix if not present
    if not command.startswith("//"):
        command = f"//{command}"

    return rcon.execute_command(command)


@mcp.tool()
def worldedit_generation(command: str) -> str:
    """
    WorldEdit Generation Commands - Generate shapes and structures.

    Commands:
    - sphere <pattern> <radius> - Create sphere
    - cyl <pattern> <radius> [height] - Create cylinder
    - pyramid <pattern> <size> - Create pyramid

    Args:
        command: Generation command (e.g., 'sphere stone 10')

    Returns:
        Command result
    """
    initialize()

    # Add // prefix if not present
    if not command.startswith("//"):
        command = f"//{command}"

    return rcon.execute_command(command)


@mcp.tool()
def worldedit_clipboard(command: str) -> str:
    """
    WorldEdit Clipboard Commands - Copy, cut, and paste structures.

    Commands:
    - copy - Copy selection to clipboard
    - cut [pattern] - Cut selection
    - paste - Paste from clipboard
    - rotate <y> [x] [z] - Rotate clipboard

    Args:
        command: Clipboard command (e.g., 'copy' or 'paste -a')

    Returns:
        Command result
    """
    initialize()

    # Add // prefix if not present
    if not command.startswith("//"):
        command = f"//{command}"

    return rcon.execute_command(command)


@mcp.tool()
def worldedit_history(command: str) -> str:
    """
    WorldEdit History Commands - Undo and redo changes.

    Commands:
    - undo [times] - Undo last edit(s)
    - redo [times] - Redo undone edit(s)
    - clearhistory - Clear edit history

    Args:
        command: History command (e.g., 'undo' or 'redo 3')

    Returns:
        Command result
    """
    initialize()

    # Add // prefix if not present
    if not command.startswith("//"):
        command = f"//{command}"

    return rcon.execute_command(command)


@mcp.tool()
def get_server_info() -> Dict[str, Any]:
    """
    Get information about the Minecraft server.

    Returns:
        Server information including players, time, difficulty
    """
    initialize()

    try:
        # Get player list
        players = rcon.execute_command("list")

        # Get time
        time_result = rcon.execute_command("time query daytime")

        # Get difficulty
        diff_result = rcon.execute_command("difficulty")

        return {
            "status": "online",
            "players": players,
            "time": time_result,
            "difficulty": diff_result
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
def get_player_position(player_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get comprehensive position data for a player.

    Args:
        player_name: Name of the player (optional)

    Returns:
        Player position, rotation, target block, surface level
    """
    initialize()

    try:
        # Get player list to find a player if not specified
        if not player_name:
            list_result = rcon.execute_command("list")
            # Extract player name from result
            import re
            match = re.search(r"online: (.+)", list_result)
            if match:
                players = match.group(1).split(", ")
                if players:
                    player_name = players[0]

        if not player_name:
            return {"error": "No players online"}

        # Get player position
        pos_result = rcon.execute_command(f"execute as {player_name} run tp @s ~ ~ ~")

        # Parse position from result
        # Example: "Teleported ereidjustpeed to 100.5, 64.0, 200.5"
        match = re.search(r"to ([\d.-]+), ([\d.-]+), ([\d.-]+)", pos_result)
        if match:
            x, y, z = float(match.group(1)), float(match.group(2)), float(match.group(3))
            return {
                "player": player_name,
                "x": x,
                "y": y,
                "z": z,
                "surface_level": int(y - 1)  # Player stands on the block below
            }

        return {"error": "Could not parse position"}

    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def search_minecraft_item(query: str, limit: int = 20) -> list:
    """
    Search for Minecraft blocks/items by name.

    Args:
        query: Search term
        limit: Maximum results (default 20)

    Returns:
        List of matching items
    """
    # This would need the minecraft items database loaded
    # For now, return a simple mock response
    return [
        {"id": "minecraft:stone", "name": "Stone"},
        {"id": "minecraft:oak_planks", "name": "Oak Planks"},
        {"id": "minecraft:glass", "name": "Glass"}
    ]


# ============================================
# Resources (Documentation)
# ============================================

@mcp.resource("vibecraft://patterns")
def get_pattern_syntax() -> str:
    """WorldEdit pattern syntax guide"""
    return """
    # WorldEdit Pattern Syntax

    - Single block: stone
    - Mixed: 50%stone,30%dirt
    - Random states: *oak_log
    - Categories: ##wool
    """


@mcp.resource("vibecraft://masks")
def get_mask_syntax() -> str:
    """WorldEdit mask syntax guide"""
    return """
    # WorldEdit Mask Syntax

    - Block masks: stone, !air
    - Categories: ##wool
    - Special: #existing, #solid
    - Expressions: >y64
    """


@mcp.resource("vibecraft://coordinates")
def get_coordinate_guide() -> str:
    """Coordinate system reference"""
    return """
    # Minecraft Coordinate System

    - X: East (+) / West (-)
    - Y: Up (+) / Down (-)
    - Z: South (+) / North (-)
    - Console format: X,Y,Z (comma-separated)
    """


# ============================================
# Main entry point
# ============================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="VibeCraft FastMCP Server")
    parser.add_argument("--port", type=int, default=8765, help="Port to run on (for HTTP mode)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind to (for HTTP mode)")
    parser.add_argument("--transport", type=str, default="stdio", choices=["stdio", "http"],
                        help="Transport type: stdio (default) or http")
    args = parser.parse_args()

    print("\n" + "="*60)
    print("🎮 VibeCraft FastMCP Server")
    print("="*60)

    # Initialize on startup
    try:
        initialize()
        print("✅ RCON connection successful!")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("\nMake sure:")
        print("  1. Minecraft server is running")
        print("  2. RCON is enabled in server.properties")
        print("  3. RCON password matches your .env file")
        sys.exit(1)

    if args.transport == "http":
        print(f"\n📡 Starting HTTP server on http://{args.host}:{args.port}")
        print("\nAdd to Claude Desktop config:")
        print(f"""
{{
  "mcpServers": {{
    "vibecraft-shared": {{
      "url": "http://{args.host}:{args.port}"
    }}
  }}
}}
""")
        print("\n👀 All debug output will appear here!")
        print("Press Ctrl+C to stop")
        print("="*60 + "\n")

        # Run as HTTP server
        mcp.run(transport="sse", port=args.port, host=args.host)
    else:
        print("\n📡 Starting stdio server")
        print("\nAdd to Claude Desktop config:")
        print(f"""
{{
  "mcpServers": {{
    "vibecraft": {{
      "command": "uv",
      "args": ["run", "python", "server_fastmcp.py"],
      "cwd": "/Users/er/Repos/vibecraft/mcp-server"
    }}
  }}
}}
""")
        print("\nPress Ctrl+C to stop")
        print("="*60 + "\n")

        # Run as stdio server
        mcp.run(transport="stdio")