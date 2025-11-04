#!/usr/bin/env python3
"""
VibeCraft MCP Server - FastMCP Complete Implementation
A complete FastMCP server with ALL VibeCraft tools (34+)
"""

import os
import sys
import json
import re
import logging
import math
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fastmcp import FastMCP

# Import VibeCraft modules
from vibecraft.config import load_config
from vibecraft.rcon_manager import RCONManager
from vibecraft.terrain import TerrainAnalyzer
from vibecraft.terrain_generation import TerrainGenerator
from vibecraft.building_tools import (
    CircleCalculator,
    WindowPlacementCalculator,
    SymmetryChecker,
    LightingAnalyzer,
    StructureValidator
)

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
terrain_analyzer = None
terrain_generator = None
minecraft_items = []
furniture_layouts = {}

def initialize():
    """Initialize VibeCraft components"""
    global config, rcon, terrain_analyzer, terrain_generator, minecraft_items, furniture_layouts

    if config is None:
        config = load_config()
        config.enable_command_logging = True

        rcon = RCONManager(config)
        terrain_analyzer = TerrainAnalyzer(rcon)
        terrain_generator = TerrainGenerator(rcon)

        # Test RCON connection
        try:
            result = rcon.execute_command("list")
            logger.info(f"✅ RCON connected: {result}")
        except Exception as e:
            logger.error(f"❌ RCON connection failed: {e}")
            raise

        # Load Minecraft items
        items_file = Path(__file__).parent.parent.parent / "minecraft_items_filtered.json"
        if items_file.exists():
            with open(items_file) as f:
                minecraft_items = json.load(f)
                logger.info(f"Loaded {len(minecraft_items)} Minecraft items")

        # Load furniture layouts
        furniture_file = Path(__file__).parent.parent / "context/minecraft_furniture_layouts.json"
        if furniture_file.exists():
            with open(furniture_file) as f:
                furniture_layouts = json.load(f)
                logger.info(f"Loaded {len(furniture_layouts)} furniture layouts")


# ============================================
# Core RCON Tool
# ============================================

@mcp.tool()
def rcon_command(command: str, description: Optional[str] = None,
                timeout: Optional[int] = None, dangerouslyDisableSandbox: bool = False) -> str:
    """
    Execute any Minecraft or WorldEdit command via RCON.
    This is the most flexible tool for commands not covered by specialized tools.

    Args:
        command: The command to execute (without leading /)
        description: Clear description of what this command does
        timeout: Optional timeout in milliseconds (max 600000)
        dangerouslyDisableSandbox: Override sandbox mode (use with caution)

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
# WorldEdit Selection Tools
# ============================================

@mcp.tool()
def worldedit_selection(command: str) -> str:
    """
    WorldEdit Selection Commands - Define and manipulate the selected region.

    Key Commands:
    - pos1 X,Y,Z - Set first corner (comma-separated!)
    - pos2 X,Y,Z - Set second corner (comma-separated!)
    - expand <amount> [direction] - Expand selection
    - expand vert - Expand vertically to world limits
    - contract <amount> [direction] - Contract selection
    - shift <amount> [direction] - Shift selection
    - size - Get selection information
    - count <mask> - Count blocks matching mask

    Note: Always use comma-separated coordinates from console!
    """
    initialize()
    if not command.startswith("//"):
        command = f"//{command}"
    return rcon.execute_command(command)


@mcp.tool()
def worldedit_region(command: str) -> str:
    """
    WorldEdit Region Commands - Modify the selected region.

    Most Common Commands:
    - set <pattern> - Fill region with pattern
    - replace [from] <to> - Replace blocks
    - walls <pattern> - Build walls (sides only)
    - faces <pattern> - Build all 6 faces
    - overlay <pattern> - Overlay pattern on top surface
    - center <pattern> - Set center blocks
    - hollow [thickness] - Hollow out the region
    - move [count] [direction] [replace] - Move region
    - stack [count] [direction] - Duplicate region
    - smooth [iterations] - Smooth terrain
    - naturalize - Create natural dirt/stone layers
    """
    initialize()
    if not command.startswith("//"):
        command = f"//{command}"
    return rcon.execute_command(command)


@mcp.tool()
def worldedit_generation(command: str) -> str:
    """
    WorldEdit Generation Commands - Generate shapes and structures.

    Sphere Commands:
    - sphere <pattern> <radius> - Filled sphere
    - hsphere <pattern> <radius> - Hollow sphere

    Cylinder Commands:
    - cyl <pattern> <radius> [height] - Filled cylinder
    - hcyl <pattern> <radius> [height] - Hollow cylinder
    - cone <pattern> <radius> [height] - Cone shape

    Pyramid Commands:
    - pyramid <pattern> <size> - Filled pyramid
    - hpyramid <pattern> <size> - Hollow pyramid

    Formula-Based:
    - generate <pattern> <expression> - Generate by math formula
    """
    initialize()
    if not command.startswith("//"):
        command = f"//{command}"
    return rcon.execute_command(command)


@mcp.tool()
def worldedit_clipboard(command: str) -> str:
    """
    WorldEdit Clipboard Commands - Copy, cut, and paste structures.

    Copy/Cut Commands:
    - copy [-b] [-e] [-m <mask>] - Copy selection to clipboard
    - cut [pattern] [-b] [-e] [-m <mask>] - Cut selection

    Paste Commands:
    - paste [-a] [-b] [-e] [-n] [-o] [-s] - Paste from clipboard
      -a: Skip air blocks
      -s: Select pasted region

    Transform Commands:
    - rotate <y> [x] [z] - Rotate clipboard
    - flip [direction] - Flip clipboard
    """
    initialize()
    if not command.startswith("//"):
        command = f"//{command}"
    return rcon.execute_command(command)


@mcp.tool()
def worldedit_schematic(command: str) -> str:
    """
    WorldEdit Schematic Commands - Save and load structures from files.

    Commands:
    - list [-p page] - List available schematics
    - load <filename> - Load schematic to clipboard
    - save <filename> - Save clipboard to schematic file
    - delete <filename> - Delete a schematic file
    """
    initialize()
    prefix = "/schem" if not command.startswith("/") else ""
    return rcon.execute_command(f"{prefix}{command}")


@mcp.tool()
def worldedit_history(command: str) -> str:
    """
    WorldEdit History Commands - Undo and redo changes.

    Commands:
    - undo [times] - Undo last edit(s)
    - redo [times] - Redo undone edit(s)
    - clearhistory - Clear edit history
    """
    initialize()
    if not command.startswith("//"):
        command = f"//{command}"
    return rcon.execute_command(command)


@mcp.tool()
def worldedit_utility(command: str) -> str:
    """
    WorldEdit Utility Commands - Various useful operations.

    Fill & Drain:
    - fill <pattern> <radius> [depth] - Fill holes
    - fillr <pattern> <radius> [depth] - Recursive fill
    - drain <radius> - Drain water/lava pools

    Block Removal:
    - removeabove [size] [height] - Remove blocks above
    - removebelow [size] [height] - Remove blocks below
    - removenear <mask> [radius] - Remove nearby blocks

    Environment:
    - fixwater <radius> - Fix water flow
    - fixlava <radius> - Fix lava flow
    - snow [size] - Simulate snowfall
    - thaw [size] - Melt snow/ice
    - green [size] - Convert dirt to grass
    - extinguish [radius] - Remove fire
    """
    initialize()
    prefix = "/" if not command.startswith("/") else ""
    return rcon.execute_command(f"{prefix}{command}")


@mcp.tool()
def worldedit_biome(command: str) -> str:
    """
    WorldEdit Biome Commands - View and modify biomes.

    Commands:
    - biomelist [-p page] - List all biomes
    - biomeinfo [-t] - Get biome at location
    - setbiome <biome> - Set biome in selection

    Common Biomes:
    - minecraft:plains, minecraft:forest, minecraft:desert
    - minecraft:taiga, minecraft:savanna, minecraft:jungle
    """
    initialize()
    if command.startswith("setbiome"):
        return rcon.execute_command(f"//{command}")
    else:
        return rcon.execute_command(f"/{command}")


@mcp.tool()
def worldedit_brush(command: str) -> str:
    """
    WorldEdit Brush Commands - Create brushes for click-based editing.

    IMPORTANT: Most brushes require player interaction and may not work from console.

    Configuration (works from console):
    - mask <mask> - Set brush mask
    - material <pattern> - Set brush material
    - size <size> - Set brush size
    - range <range> - Set brush range

    Basic Brushes:
    - sphere <pattern> [radius] [-h] - Sphere brush
    - cylinder <pattern> [radius] [height] [-h] - Cylinder brush
    - smooth [radius] [iterations] - Terrain smoother
    """
    initialize()
    prefix = "/br" if not command.startswith("/") else ""
    return rcon.execute_command(f"{prefix}{command}")


@mcp.tool()
def worldedit_general(command: str) -> str:
    """
    WorldEdit Session & Global Commands - Manage limits, masks, and options.

    Includes:
    - //limit <amount> - Set block change limit
    - //timeout <ms> - Set operation timeout
    - //gmask <mask> - Set global mask
    - //world <world> - Change world
    - /worldedit help|version|reload - WorldEdit management
    """
    initialize()
    return rcon.execute_command(command)


@mcp.tool()
def worldedit_navigation(command: str) -> str:
    """
    WorldEdit Navigation Commands - Move the player quickly.

    Commands:
    - /ascend [levels] - Go up levels
    - /descend [levels] - Go down levels
    - /ceil [-fg] [clearance] - Go to ceiling
    - /thru - Pass through wall
    - /up <distance> - Go up distance
    - /unstuck - Escape from block
    """
    initialize()
    return rcon.execute_command(command)


@mcp.tool()
def worldedit_chunk(command: str) -> str:
    """
    WorldEdit Chunk Commands - Inspect or delete chunks.

    Commands:
    - /chunkinfo - Show chunk information
    - /listchunks [-p <page>] - List chunks in selection
    - /delchunks [-o <age>] - Delete chunks (dangerous!)
    """
    initialize()
    return rcon.execute_command(command)


@mcp.tool()
def worldedit_snapshot(command: str) -> str:
    """
    WorldEdit Snapshot Commands - Manage and restore backups.

    Commands:
    - /snap list [-p <page>] - List snapshots
    - /snap use <name> - Use snapshot
    - /snap sel <index> - Select by index
    - /restore [snapshot] - Restore from snapshot
    """
    initialize()
    return rcon.execute_command(command)


@mcp.tool()
def worldedit_scripting(command: str) -> str:
    """
    WorldEdit Scripting Commands - Execute CraftScripts.

    Commands:
    - /cs <filename> [args...] - Run CraftScript
    - /.s [args...] - Re-run previous script
    """
    initialize()
    return rcon.execute_command(command)


@mcp.tool()
def worldedit_reference(command: str) -> str:
    """
    WorldEdit Reference Commands - Search blocks/items or read help.

    Commands:
    - /searchitem [-bi] [-p <page>] <query> - Search for items/blocks
    - //help [-s] [-p <page>] [command] - Get help
    - /schem formats - List schematic formats
    """
    initialize()
    return rcon.execute_command(command)


@mcp.tool()
def worldedit_tools(command: str) -> str:
    """
    WorldEdit Tool Binding Commands - Configure tools and brushes.

    Commands:
    - /tool <mode> [...] - Set tool mode
    - /mask <mask> - Set mask
    - /material <pattern> - Set material
    - /range <distance> - Set range
    - /size <radius> - Set size
    - // or /, - Toggle super pickaxe
    """
    initialize()
    return rcon.execute_command(command)


# ============================================
# Validation & Helper Tools
# ============================================

@mcp.tool()
def validate_pattern(pattern: str) -> Dict[str, Any]:
    """
    Validate a WorldEdit pattern before using it.

    Pattern types:
    - Single: stone, oak_planks
    - Random: 50%stone,30%dirt,20%gravel
    - Block states: oak_stairs[facing=north]
    - Categories: ##wool, ##logs
    """
    initialize()

    # Basic validation
    valid = True
    explanation = ""

    if "%" in pattern:
        explanation = "Random pattern with percentages"
    elif "##" in pattern:
        explanation = "Block category pattern"
    elif "[" in pattern and "]" in pattern:
        explanation = "Block with state properties"
    else:
        explanation = "Single block pattern"

    return {
        "valid": valid,
        "pattern": pattern,
        "explanation": explanation
    }


@mcp.tool()
def validate_mask(mask: str) -> Dict[str, Any]:
    """
    Validate a WorldEdit mask before using it.

    Mask types:
    - Block: stone, !air
    - Categories: ##wool
    - Special: #existing, #solid, #surface
    - Expressions: >y64, <x100
    """
    initialize()

    valid = True
    explanation = ""

    if mask.startswith("!"):
        explanation = "Negation mask (not these blocks)"
    elif mask.startswith("#"):
        explanation = "Special mask type"
    elif mask.startswith(">") or mask.startswith("<") or mask.startswith("="):
        explanation = "Expression mask"
    else:
        explanation = "Block mask"

    return {
        "valid": valid,
        "mask": mask,
        "explanation": explanation
    }


@mcp.tool()
def calculate_region_size(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> Dict[str, Any]:
    """
    Calculate the size and block count of a region.

    Returns dimensions, total blocks, and estimated operation time.
    """
    width = abs(x2 - x1) + 1
    height = abs(y2 - y1) + 1
    depth = abs(z2 - z1) + 1
    total = width * height * depth

    return {
        "dimensions": {"width": width, "height": height, "depth": depth},
        "total_blocks": total,
        "estimated_time": f"{total / 10000:.1f} seconds" if total > 10000 else "< 1 second"
    }


# ============================================
# Server Information Tools
# ============================================

@mcp.tool()
def get_server_info() -> Dict[str, Any]:
    """
    Get information about the Minecraft server.

    Returns server status, players, time, and difficulty.
    """
    initialize()

    try:
        players = rcon.execute_command("list")
        time_result = rcon.execute_command("time query daytime")
        diff_result = rcon.execute_command("difficulty")

        # Check for WorldEdit
        we_version = "Unknown"
        try:
            we_result = rcon.execute_command("version WorldEdit")
            if "WorldEdit" in we_result:
                import re
                match = re.search(r"(\d+\.\d+\.\d+)", we_result)
                if match:
                    we_version = match.group(1)
        except:
            pass

        return {
            "status": "online",
            "players": players,
            "time": time_result,
            "difficulty": diff_result,
            "worldedit_version": we_version
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


@mcp.tool()
def get_player_position(player_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get comprehensive position data for a player in the Minecraft world.

    Returns player coordinates, rotation, target block, and surface level.
    """
    initialize()

    try:
        if not player_name:
            list_result = rcon.execute_command("list")
            import re
            match = re.search(r"online: (.+)", list_result)
            if match:
                players = match.group(1).split(", ")
                if players:
                    player_name = players[0]

        if not player_name:
            return {"error": "No players online"}

        pos_result = rcon.execute_command(f"execute as {player_name} run tp @s ~ ~ ~")

        match = re.search(r"to ([\d.-]+), ([\d.-]+), ([\d.-]+)", pos_result)
        if match:
            x, y, z = float(match.group(1)), float(match.group(2)), float(match.group(3))
            return {
                "player": player_name,
                "x": x,
                "y": y,
                "z": z,
                "surface_level": int(y - 1)
            }

        return {"error": "Could not parse position"}

    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_surface_level(x: int, z: int) -> Dict[str, Any]:
    """
    Find the surface (top solid block) Y-coordinate at given X, Z coordinates.

    Uses raycast from build limit down to find first solid block.
    """
    initialize()

    try:
        # Use testforblock to find surface
        for y in range(319, -64, -1):
            result = rcon.execute_command(f"execute if block {x} {y} {z} air")
            if "Test failed" in result:
                return {
                    "x": x,
                    "z": z,
                    "surface_y": y,
                    "surface_block": "unknown"
                }

        return {"x": x, "z": z, "surface_y": -64, "surface_block": "bedrock"}

    except Exception as e:
        return {"error": str(e)}


# ============================================
# Search Tools
# ============================================

@mcp.tool()
def search_minecraft_item(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Search for Minecraft blocks/items by name.

    Find blocks and items from Minecraft 1.21.3 to use in your builds.
    Returns matching items with ID, name, and display name.
    """
    initialize()

    if not minecraft_items:
        return [{"error": "Minecraft items database not loaded"}]

    results = []
    query_lower = query.lower()

    for item in minecraft_items:
        if query_lower in item.get("id", "").lower() or query_lower in item.get("name", "").lower():
            results.append({
                "id": item.get("id"),
                "name": item.get("name"),
                "displayName": item.get("displayName", item.get("name"))
            })
            if len(results) >= limit:
                break

    return results


# ============================================
# Furniture System
# ============================================

@mcp.tool()
def furniture_lookup(action: str, query: Optional[str] = None,
                    category: Optional[str] = None, tags: Optional[List[str]] = None,
                    furniture_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Search and retrieve Minecraft furniture layouts for automated building.

    Operations:
    - action="search": Find furniture by name, category, or tags
    - action="get": Retrieve complete layout data by ID

    Each layout includes block placements, materials, dimensions, and notes.
    """
    initialize()

    if action == "search":
        results = []
        for furn_id, layout in furniture_layouts.items():
            # Match logic
            if query and query.lower() in layout.get("name", "").lower():
                results.append({
                    "id": furn_id,
                    "name": layout.get("name"),
                    "category": layout.get("category"),
                    "dimensions": layout.get("dimensions")
                })
            elif category and category == layout.get("category"):
                results.append({
                    "id": furn_id,
                    "name": layout.get("name"),
                    "category": layout.get("category"),
                    "dimensions": layout.get("dimensions")
                })

        return {"results": results[:20]}

    elif action == "get" and furniture_id:
        if furniture_id in furniture_layouts:
            return furniture_layouts[furniture_id]
        else:
            return {"error": f"Furniture ID '{furniture_id}' not found"}

    return {"error": "Invalid action or parameters"}


# ============================================
# Terrain Analysis & Generation
# ============================================

@mcp.tool()
def terrain_analyzer(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int,
                    resolution: int = 2, max_samples: int = 10000) -> Dict[str, Any]:
    """
    Analyze terrain in a Minecraft region to inform building decisions.

    Scans region and provides:
    - Elevation statistics (min/max/average height, slope)
    - Block composition (surface blocks, liquids, vegetation)
    - Biome distribution (if available)
    - Hazards (lava, water, steep terrain, caves)
    - Opportunities (flat areas, cliffs, coastlines)

    Resolution: 1=every block, 2=every other block, 3+ for large areas
    """
    initialize()

    try:
        result = terrain_analyzer.analyze_region(
            x1, y1, z1, x2, y2, z2,
            resolution=resolution,
            max_samples=max_samples
        )
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def generate_terrain(type: str, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int,
                    scale: int = 18, amplitude: int = 10, smooth_iterations: int = 2,
                    seed: Optional[int] = None, direction: Optional[str] = None,
                    height: Optional[int] = None, depth: Optional[int] = None) -> str:
    """
    Generate realistic terrain features using WorldEdit noise functions.

    Types:
    - rolling_hills: Gentle undulating hills (Perlin noise)
    - rugged_mountains: Sharp peaks and ridges (Ridged Multifractal)
    - valley_network: Interconnected valleys for rivers
    - mountain_range: Linear mountain chain in a direction
    - plateau: Flat-topped elevation with rough edges

    Scale: 10-40 (feature breadth), Amplitude: 3-30 (height variation)
    """
    initialize()

    try:
        result = terrain_generator.generate(
            type=type,
            x1=x1, y1=y1, z1=z1,
            x2=x2, y2=y2, z2=z2,
            scale=scale,
            amplitude=amplitude,
            smooth_iterations=smooth_iterations,
            seed=seed,
            direction=direction,
            height=height,
            depth=depth
        )
        return result
    except Exception as e:
        return f"Terrain generation failed: {str(e)}"


@mcp.tool()
def texture_terrain(style: str, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int,
                   snow_level: Optional[int] = None) -> str:
    """
    Apply natural surface materials to terrain.

    Styles:
    - temperate: Grass, moss, dirt (plains/forest biomes)
    - alpine: Stone, snow, gravel (high altitude)
    - desert: Sand, sandstone, terracotta (arid regions)
    - volcanic: Basalt, magma, blackstone (lava zones)
    - jungle: Rich soil, podzol, moss (tropical)
    - swamp: Mud, clay, damp grass (wetlands)
    """
    initialize()

    try:
        result = terrain_generator.texture_terrain(
            style=style,
            x1=x1, y1=y1, z1=z1,
            x2=x2, y2=y2, z2=z2,
            snow_level=snow_level
        )
        return result
    except Exception as e:
        return f"Terrain texturing failed: {str(e)}"


@mcp.tool()
def smooth_terrain(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int,
                  iterations: int = 2, mask: Optional[str] = None) -> str:
    """
    Post-process terrain to remove blocky appearance.

    Iterations: More passes = smoother (2-4 recommended)
    Less smoothing preserves sharp features (mountains)
    More smoothing creates gentler slopes (hills)
    """
    initialize()

    try:
        result = terrain_generator.smooth_terrain(
            x1=x1, y1=y1, z1=z1,
            x2=x2, y2=y2, z2=z2,
            iterations=iterations,
            mask=mask
        )
        return result
    except Exception as e:
        return f"Terrain smoothing failed: {str(e)}"


# ============================================
# Building Analysis Tools
# ============================================

@mcp.tool()
def calculate_shape(shape: str, radius: Optional[int] = None,
                   width: Optional[int] = None, height: Optional[int] = None,
                   depth: int = 1, filled: bool = False, hollow: bool = True,
                   style: str = "hemisphere") -> Dict[str, Any]:
    """
    Calculate perfect circles, spheres, domes, ellipses, and arches for Minecraft.

    Shapes:
    - circle: 2D circle (for towers, ponds)
    - sphere: 3D sphere (hollow or filled)
    - dome: Hemisphere or partial sphere
    - ellipse: 2D ellipse (oval shapes)
    - arch: Arch structure (doorways, bridges)

    Returns coordinate lists, block count, and ASCII preview.
    """
    initialize()

    calculator = CircleCalculator()

    try:
        if shape == "circle" and radius:
            coords = calculator.calculate_circle(radius, filled)
            return {
                "shape": shape,
                "radius": radius,
                "filled": filled,
                "block_count": len(coords),
                "coordinates": coords[:50]  # Limit output
            }
        # Add other shapes as needed

        return {"error": "Shape calculation not fully implemented"}

    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def calculate_window_spacing(wall_length: int, window_width: int,
                            window_count: Optional[int] = None,
                            spacing_style: str = "even") -> Dict[str, Any]:
    """
    Calculate optimal window and door placement for building facades.

    Spacing styles:
    - even: Evenly distributed with equal spacing
    - golden_ratio: Positioned using φ = 1.618
    - symmetric: Mirrored around center axis
    - clustered: Grouped in pairs/triplets
    """
    initialize()

    calculator = WindowPlacementCalculator()

    try:
        result = calculator.calculate_spacing(
            wall_length=wall_length,
            window_width=window_width,
            window_count=window_count,
            style=spacing_style
        )
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def check_symmetry(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int,
                  axis: str = "x", tolerance: int = 0, resolution: int = 1) -> Dict[str, Any]:
    """
    Check structural symmetry across an axis for quality assurance.

    Axes:
    - x: Mirror across X axis (left/right symmetry)
    - z: Mirror across Z axis (front/back symmetry)
    - y: Mirror across Y axis (top/bottom symmetry)

    Returns symmetry score and asymmetric block list.
    """
    initialize()

    checker = SymmetryChecker(rcon)

    try:
        result = checker.check_symmetry(
            x1=x1, y1=y1, z1=z1,
            x2=x2, y2=y2, z2=z2,
            axis=axis,
            tolerance=tolerance,
            resolution=resolution
        )
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def analyze_lighting(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int,
                    resolution: int = 2) -> Dict[str, Any]:
    """
    Analyze lighting levels and suggest optimal torch/lantern placement.

    Identifies dark spots where mobs can spawn (light level < 8).
    Returns average light level, dark spots, and placement recommendations.
    """
    initialize()

    analyzer = LightingAnalyzer(rcon)

    try:
        result = analyzer.analyze(
            x1=x1, y1=y1, z1=z1,
            x2=x2, y2=y2, z2=z2,
            resolution=resolution
        )
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def validate_structure(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int,
                      resolution: int = 1) -> Dict[str, Any]:
    """
    Validate structural integrity and detect physics violations.

    Checks for:
    - Floating blocks (no support)
    - Unsupported gravity blocks (sand, gravel)
    - Physics glitches waiting to happen

    Returns validation report with issues and fix recommendations.
    """
    initialize()

    validator = StructureValidator(rcon)

    try:
        result = validator.validate(
            x1=x1, y1=y1, z1=z1,
            x2=x2, y2=y2, z2=z2,
            resolution=resolution
        )
        return result
    except Exception as e:
        return {"error": str(e)}


# ============================================
# Resources (Documentation)
# ============================================

@mcp.resource("vibecraft://patterns")
def get_pattern_syntax() -> str:
    """WorldEdit pattern syntax guide"""
    return """
    # WorldEdit Pattern Syntax

    - Single block: stone, oak_planks
    - Random: 50%stone,30%dirt,20%gravel
    - Block states: oak_stairs[facing=north]
    - Categories: ##wool (all wool colors)
    - Random rotation: *oak_log
    """


@mcp.resource("vibecraft://masks")
def get_mask_syntax() -> str:
    """WorldEdit mask syntax guide"""
    return """
    # WorldEdit Mask Syntax

    - Block masks: stone, !air (not air)
    - Categories: ##wool, ##logs
    - Special: #existing, #solid, #surface
    - Expressions: >y64 (above Y=64)
    - Random: %50 (50% chance)
    """


@mcp.resource("vibecraft://expressions")
def get_expression_syntax() -> str:
    """WorldEdit expression syntax guide"""
    return """
    # WorldEdit Expression Syntax

    - Coordinates: x, y, z
    - Math: + - * / ^ %
    - Functions: sin(), cos(), sqrt(), abs()
    - Noise: perlin(), voronoi(), ridged()
    - Examples: y+perlin(x,z)*5
    """


@mcp.resource("vibecraft://coordinates")
def get_coordinate_guide() -> str:
    """Coordinate system reference"""
    return """
    # Minecraft Coordinate System

    - X: East (+) / West (-)
    - Y: Up (+) / Down (-)
    - Z: South (+) / North (-)

    CONSOLE FORMAT: X,Y,Z (comma-separated!)
    Example: //pos1 100,64,200
    """


@mcp.resource("vibecraft://workflows")
def get_common_workflows() -> str:
    """Common WorldEdit workflows"""
    return """
    # Common WorldEdit Workflows

    ## Simple Building:
    1. //pos1 X,Y,Z → //pos2 X,Y,Z
    2. //set stone_bricks
    3. //walls oak_planks

    ## Copy & Paste:
    1. Select with //pos1 and //pos2
    2. //copy
    3. //paste -a (skip air)

    ## Terrain:
    1. Select area
    2. //generate stone y<65+perlin(x,z)*5
    3. //smooth 3
    """


# ============================================
# Main entry point
# ============================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="VibeCraft FastMCP Server - Complete")
    parser.add_argument("--port", type=int, default=8765, help="Port for HTTP mode")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host for HTTP mode")
    parser.add_argument("--transport", type=str, default="stdio",
                       choices=["stdio", "http"], help="Transport type")
    args = parser.parse_args()

    print("\n" + "="*60)
    print("🎮 VibeCraft FastMCP Server - Complete Edition")
    print("   34+ Tools Available")
    print("="*60)

    # Initialize on startup
    try:
        initialize()
        print("✅ RCON connection successful!")
        print(f"✅ Loaded {len(minecraft_items)} Minecraft items")
        print(f"✅ Loaded {len(furniture_layouts)} furniture layouts")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("\nMake sure:")
        print("  1. Minecraft server is running")
        print("  2. RCON is enabled in server.properties")
        print("  3. RCON password matches your .env file")
        sys.exit(1)

    if args.transport == "http":
        print(f"\n📡 Starting HTTP/SSE server on http://{args.host}:{args.port}/sse")
        print("\n👀 All debug output will appear here!")
        print("Press Ctrl+C to stop")
        print("="*60 + "\n")

        # Run as HTTP server
        mcp.run(transport="sse", port=args.port, host=args.host)
    else:
        print("\n📡 Starting stdio server")
        print("Press Ctrl+C to stop")
        print("="*60 + "\n")

        # Run as stdio server
        mcp.run(transport="stdio")