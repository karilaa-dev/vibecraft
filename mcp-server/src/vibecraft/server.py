#!/usr/bin/env python3
"""
VibeCraft MCP Server - Main Server Implementation
Exposes ALL WorldEdit commands via MCP for AI-powered building in Minecraft
"""

import asyncio
import json
import logging
import math
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Sequence, List, Optional

from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, EmbeddedResource
import mcp.server.stdio

from .config import load_config, VibeCraftConfig
from .rcon_manager import RCONManager
from .sanitizer import (
    sanitize_command,
    validate_coordinates_in_bounds,
    check_player_context_warning,
)
from .terrain import TerrainAnalyzer
from .building_tools import (
    CircleCalculator,
    WindowPlacementCalculator,
    SymmetryChecker,
    LightingAnalyzer,
    StructureValidator
)
from .furniture_placer import FurniturePlacer
from .pattern_placer import PatternPlacer
from .workflow import BuildWorkflowCoordinator
from .terrain_generation import TerrainGenerator
from .resources import (
    PATTERN_SYNTAX_GUIDE,
    MASK_SYNTAX_GUIDE,
    EXPRESSION_SYNTAX_GUIDE,
    COORDINATE_GUIDE,
    COMMON_WORKFLOWS,
    PLAYER_CONTEXT_WARNING,
)
from .schematic_manager import (
    list_schematics,
    read_metadata,
    copy_to_server,
    SCHEM_SOURCE_DIR,
    SCHEM_DEST_DIR,
)

# Configure logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
log_dir = Path(__file__).parent.parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Create log file with timestamp
log_file = log_dir / f"vibecraft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Configure logging to both console and file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console output (for when run manually)
        logging.FileHandler(log_file)  # File output (always available)
    ]
)
logger = logging.getLogger("vibecraft")
logger.info(f"Logging to file: {log_file}")

# Load Minecraft items data
def load_minecraft_items():
    """Load Minecraft items database from JSON file"""
    # Try to find the items file in the parent directory
    items_file = Path(__file__).parent.parent.parent.parent / "minecraft_items_filtered.json"

    if not items_file.exists():
        logger.warning(f"Minecraft items file not found at {items_file}")
        return []

    try:
        with open(items_file) as f:
            items = json.load(f)
        logger.info(f"Loaded {len(items)} Minecraft items from database")
        return items
    except Exception as e:
        logger.error(f"Error loading Minecraft items: {e}")
        return []

# Initialize server
app = Server("vibecraft")

# Global config and RCON manager (initialized in main)
config: VibeCraftConfig
rcon: RCONManager

# Minecraft items database (loaded once at startup)
minecraft_items = load_minecraft_items()


# Cached context loaders ----------------------------------------------------

CONTEXT_DIR = Path(__file__).parent.parent.parent.parent / "context"


def _load_json_list(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        logger.warning(f"Context file not found: {path}")
        return []

    try:
        with open(path, "r") as handle:
            data = json.load(handle)
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "patterns" in data:
                # For pattern files that store entries under a dict key
                return list(data["patterns"].values())
            logger.warning(f"Unexpected data format in {path}")
    except Exception as exc:  # pragma: no cover - logging path for runtime
        logger.error(f"Unable to load context file {path}: {exc}")
    return []


def load_furniture_layouts() -> List[Dict[str, Any]]:
    return _load_json_list(CONTEXT_DIR / "minecraft_furniture_layouts.json")


def load_furniture_catalog() -> List[Dict[str, Any]]:
    return _load_json_list(CONTEXT_DIR / "minecraft_furniture_catalog.json")


def load_structured_patterns() -> List[Dict[str, Any]]:
    return _load_json_list(CONTEXT_DIR / "building_patterns_structured.json")


workflow_state_path = Path(__file__).parent.parent.parent / "logs" / "workflow_state.json"
workflow = BuildWorkflowCoordinator(workflow_state_path)


def _resolve_schematic_path(name: str) -> Path:
    filename = name if name.endswith(".schem") else f"{name}.schem"
    return SCHEM_SOURCE_DIR / filename


# Default prefixes for WorldEdit tool wrappers (None = require explicit slash)
WORLD_EDIT_TOOL_PREFIXES = {
    "worldedit_selection": "//",
    "worldedit_region": "//",
    "worldedit_generation": "//",
    "worldedit_clipboard": "//",
    "worldedit_schematic": "/",
    "worldedit_history": "//",
    "worldedit_utility": "/",
    "worldedit_biome": "/",
    "worldedit_brush": "/",
    "worldedit_general": "//",
    "worldedit_navigation": "/",
    "worldedit_chunk": "/",
    "worldedit_snapshot": "/",
    "worldedit_scripting": "/",
    "worldedit_reference": "/",
    "worldedit_tools": "/",
}


def prepare_worldedit_command(tool_name: str, command: str) -> str:
    """Add appropriate prefix for categorized WorldEdit tools."""

    if command.startswith("//") or command.startswith("/"):
        return command

    normalized = command.lower()

    if tool_name == "worldedit_reference":
        if normalized.startswith("help"):
            return "//" + command
        return "/" + command

    if tool_name == "worldedit_tools":
        # Super pickaxe shorthand uses /sp, other tools use /tool, /mask, etc.
        if normalized.startswith("sp ") or normalized.startswith("superpickaxe"):
            return "/" + command
        return "/" + command

    prefix = WORLD_EDIT_TOOL_PREFIXES.get(tool_name)
    if prefix:
        return prefix + command

    return command


def format_terrain_analysis(result: Dict[str, Any]) -> str:
    """Format terrain analysis results for display."""
    output = []

    # Title
    output.append("🗺️ **Terrain Analysis Report**\n")

    # Summary first (natural language)
    if 'summary' in result:
        output.append(result['summary'])
        output.append("\n---\n")

    # Region information
    region = result.get('region', {})
    output.append("**Region Details:**")
    output.append(f"- Coordinates: ({region['min'][0]}, {region['min'][1]}, {region['min'][2]}) to ({region['max'][0]}, {region['max'][1]}, {region['max'][2]})")
    output.append(f"- Dimensions: {region['dimensions'][0]}×{region['dimensions'][1]}×{region['dimensions'][2]} blocks (W×H×D)")
    output.append(f"- Total volume: {region.get('total_blocks', 0):,} blocks")
    output.append(f"- Samples collected: {region.get('samples_taken', 0):,} (resolution: {region.get('resolution', 1)})")
    output.append("")

    # Elevation statistics
    elevation = result.get('elevation', {})
    if elevation and 'error' not in elevation:
        output.append("**Elevation Analysis:**")
        output.append(f"- Terrain type: {elevation.get('terrain_type', 'Unknown')}")
        output.append(f"- Height range: Y={elevation.get('min_y')} to Y={elevation.get('max_y')} ({elevation.get('range')} blocks)")
        output.append(f"- Average height: Y={elevation.get('avg_y')}")
        output.append(f"- Variation (std dev): {elevation.get('std_dev')} blocks")
        output.append(f"- Slope index: {elevation.get('slope_index')}")
        output.append("")

    # Block composition
    composition = result.get('composition', {})
    if composition:
        output.append("**Block Composition:**")
        output.append(f"- Unique block types: {composition.get('unique_blocks', 0)}")

        top_blocks = composition.get('top_blocks', [])
        if top_blocks:
            output.append("- Top 5 blocks:")
            for block_info in top_blocks[:5]:
                output.append(f"  - {block_info['block']}: {block_info['count']} ({block_info['percentage']}%)")

        liquids = composition.get('liquids', {})
        if liquids.get('count', 0) > 0:
            output.append(f"- Liquids: {liquids['count']} blocks ({liquids['percentage']}%)")

        vegetation = composition.get('vegetation', {})
        if vegetation.get('count', 0) > 0:
            output.append(f"- Vegetation: {vegetation['count']} blocks ({vegetation['percentage']}%)")

        cavities = composition.get('air_cavities', {})
        if cavities.get('count', 0) > 0:
            output.append(f"- Air cavities (caves): {cavities['count']} blocks ({cavities['percentage']}%)")

        output.append("")

    # Biomes
    biomes = result.get('biomes', {})
    if biomes.get('detected'):
        output.append("**Biome Distribution:**")
        biome_list = biomes.get('biomes', [])
        for biome_info in biome_list:
            output.append(f"- {biome_info['biome']}: {biome_info['count']} samples ({biome_info['percentage']}%)")
        output.append("")
    elif not biomes.get('detected'):
        output.append("**Biomes:** Detection not available (use WorldEdit //biomeinfo for biome data)")
        output.append("")

    # Hazards
    hazards = result.get('hazards', [])
    if hazards:
        output.append("⚠️ **Hazards Detected:**")
        for hazard in hazards:
            severity_icon = "🔴" if hazard.get('severity') == 'high' else "🟡" if hazard.get('severity') == 'medium' else "🟢"
            output.append(f"{severity_icon} **{hazard['type']}** ({hazard.get('severity', 'unknown')} severity)")
            if 'count' in hazard:
                output.append(f"   - Affected blocks: {hazard['count']} ({hazard.get('percentage', 0)}%)")
            if 'details' in hazard:
                output.append(f"   - Details: {hazard['details']}")
            if 'recommendation' in hazard:
                output.append(f"   - 💡 {hazard['recommendation']}")
        output.append("")
    else:
        output.append("✅ **No hazards detected** - area appears safe for building")
        output.append("")

    # Opportunities
    opportunities = result.get('opportunities', [])
    if opportunities:
        output.append("🌟 **Building Opportunities:**")
        for opp in opportunities:
            quality_icon = "⭐⭐⭐" if opp.get('quality') == 'excellent' else "⭐⭐" if opp.get('quality') == 'good' else "⭐"
            output.append(f"{quality_icon} **{opp['type']}** ({opp.get('quality', 'fair')} quality)")
            output.append(f"   - {opp.get('description', '')}")
            if 'use_cases' in opp:
                output.append(f"   - 💡 Ideal for: {opp['use_cases']}")
        output.append("")

    # JSON data reference
    output.append("---")
    output.append("💾 **Full JSON data available in result object for programmatic use**")

    return '\n'.join(output)


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available documentation resources for AI"""
    return [
        Resource(
            uri="vibecraft://guide/patterns",
            name="WorldEdit Pattern Syntax Guide",
            mimeType="text/markdown",
            description="Complete guide to WorldEdit pattern syntax with examples",
        ),
        Resource(
            uri="vibecraft://guide/masks",
            name="WorldEdit Mask Syntax Guide",
            mimeType="text/markdown",
            description="Complete guide to WorldEdit mask syntax with examples",
        ),
        Resource(
            uri="vibecraft://guide/expressions",
            name="WorldEdit Expression Syntax Guide",
            mimeType="text/markdown",
            description="Complete guide to WorldEdit expression syntax with examples",
        ),
        Resource(
            uri="vibecraft://guide/coordinates",
            name="WorldEdit Coordinate System Guide",
            mimeType="text/markdown",
            description="Guide to coordinate systems and console command syntax",
        ),
        Resource(
            uri="vibecraft://guide/workflows",
            name="Common WorldEdit Workflows",
            mimeType="text/markdown",
            description="Common building workflows and command sequences",
        ),
        Resource(
            uri="vibecraft://guide/player-context",
            name="Player Context Commands Warning",
            mimeType="text/markdown",
            description="Important information about commands that require player context",
        ),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read documentation resource by URI"""
    resource_map = {
        "vibecraft://guide/patterns": PATTERN_SYNTAX_GUIDE,
        "vibecraft://guide/masks": MASK_SYNTAX_GUIDE,
        "vibecraft://guide/expressions": EXPRESSION_SYNTAX_GUIDE,
        "vibecraft://guide/coordinates": COORDINATE_GUIDE,
        "vibecraft://guide/workflows": COMMON_WORKFLOWS,
        "vibecraft://guide/player-context": PLAYER_CONTEXT_WARNING,
    }

    if uri not in resource_map:
        raise ValueError(f"Unknown resource URI: {uri}")

    return resource_map[uri]


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools for AI to use"""
    return [
        # TIER 1: Generic RCON Tool
        Tool(
            name="rcon_command",
            description="""Execute any Minecraft or WorldEdit command via RCON.

This is the most flexible tool - it can execute ANY command supported by Minecraft or WorldEdit.
Use this for commands not covered by specialized tools, or when you need full control.

IMPORTANT - Console Command Syntax:
- WorldEdit position commands use comma-separated coords: //pos1 X,Y,Z (not spaces!)
- Remove leading slash - it's added automatically
- Some commands require player context and may not work from console

Examples:
- "list" - List players
- "time set day" - Set time to day
- "//pos1 100,64,100" - Set WorldEdit position 1
- "//set stone" - Fill selection with stone
- "//copy" - Copy selection to clipboard
- "//paste" - Paste clipboard

Safety: Commands are validated before execution. Dangerous commands are blocked by default.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute (without leading /)",
                    }
                },
                "required": ["command"],
            },
        ),
        # TIER 2: Categorized WorldEdit Tools
        Tool(
            name="worldedit_selection",
            description="""WorldEdit Selection Commands - Define and manipulate the selected region.

Before performing operations on a region, you must define it by setting positions.

Key Commands:
- //pos1 X,Y,Z - Set first corner (comma-separated!)
- //pos2 X,Y,Z - Set second corner (comma-separated!)
- //sel [mode] - Change selection mode (cuboid, extend, poly, ellipsoid, sphere, cyl, convex)
- //expand <amount> [direction] - Expand selection
- //expand vert - Expand selection vertically to world limits (Y=-64 to Y=319)
- //contract <amount> [direction] - Contract selection
- //inset <amount> - Inset selection (contract all faces equally)
- //outset <amount> - Outset selection (expand all faces equally)
- //shift <amount> [direction] - Shift selection
- //size - Get selection information
- //count <mask> - Count blocks matching mask

Example Workflow:
1. //pos1 100,64,100
2. //pos2 120,80,120
3. //size
4. Now you can use region commands like //set

Selection Modes:
- cuboid (default) - Standard box selection
- extend - Extend selection with each click
- poly - 2D polygon selection
- ellipsoid - Ellipsoid selection
- sphere - Spherical selection
- cyl - Cylindrical selection
- convex - Convex hull selection

Special:
- //expand vert - Extends selection from bedrock to build limit (full height)
- //inset 2 - Shrinks selection by 2 blocks on all sides
- //outset 3 - Expands selection by 3 blocks on all sides

Note: Always use comma-separated coordinates from console!
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Selection command (e.g., 'pos1 100,64,100' or 'size' or 'sel sphere')",
                    }
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_region",
            description="""WorldEdit Region Commands - Modify the selected region.

These commands operate on your current selection (set with //pos1 and //pos2).

Most Common Commands:
- //set <pattern> - Fill region with pattern
- //replace [from] <to> - Replace blocks in selection
- //replacenear <size> <from> <to> - Replace blocks in sphere around you (no selection needed!)
- //walls <pattern> - Build walls (sides only)
- //faces <pattern> - Build all 6 faces
- //overlay <pattern> - Overlay pattern on top surface
- //center <pattern> - Set center blocks
- //hollow [thickness] - Hollow out the region
- //line <pattern> [thickness] [-h] - Draw line (use -h for hollow)
- //curve <pattern> [thickness] [-h] - Draw curve (use -h for hollow)
- //smooth [iterations] - Smooth terrain elevation
- //naturalize - Create natural dirt/stone layers

Advanced Movement:
- //move [count] [direction] [replace] [-s] [-a] [-b] [-e] [-m <mask>]
  -s: Move without copying (cut)
  -a: Skip air blocks
  -b: Copy biomes
  -e: Copy entities
  -m: Source mask

- //stack [count] [direction] [-s] [-a] [-b] [-e] [-r] [-m <mask>]
  -s: Stack without original
  -a: Skip air blocks
  -b: Copy biomes
  -e: Copy entities
  -r: Move in reverse
  -m: Source mask

Pattern Examples:
- stone
- 50%stone,30%cobblestone,20%andesite
- ##wool (random wool colors)

Example Usage:
//set stone_bricks - Fill region with stone bricks
//walls oak_planks - Create wooden walls
//replace stone air - Remove all stone in selection
//replacenear 20 stone cobblestone - Replace stone with cobblestone within 20 blocks
//move 10 north -s - Cut and move 10 blocks north
//stack 5 up -a - Stack 5 times upward, skip air

Note: //replacenear is more intuitive for quick edits - no selection needed!
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Region command (e.g., 'set stone' or 'replacenear 10 dirt grass_block')",
                    }
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_generation",
            description="""WorldEdit Generation Commands - Generate shapes and structures.

Create geometric shapes at your current position or specified location.

Sphere Commands:
- //sphere <pattern> <radius> - Filled sphere
- //hsphere <pattern> <radius> - Hollow sphere
- //sphere -r <pattern> <radius> - Raised (centered at feet)

Cylinder Commands:
- //cyl <pattern> <radius> [height] - Filled cylinder
- //hcyl <pattern> <radius> [height] - Hollow cylinder
- //cone <pattern> <radius> [height] - Cone shape

Pyramid Commands:
- //pyramid <pattern> <size> - Filled pyramid
- //hpyramid <pattern> <size> - Hollow pyramid

Formula-Based:
- //generate <pattern> <expression> - Generate by math formula
  Example: //generate stone y-64<10&&x^2+z^2<100

Feature Generation:
- //feature <feature> - Generate Minecraft features
- //structure <structure> - Generate Minecraft structures

Example: Create a stone sphere with 10 block radius
//sphere stone 10
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Generation command (e.g., 'sphere stone 10')",
                    }
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_clipboard",
            description="""WorldEdit Clipboard Commands - Copy, cut, and paste structures.

Workflow:
1. Select region with //pos1 and //pos2
2. Copy or cut to clipboard
3. Move to new location
4. Paste

Copy/Cut Commands:
- //copy [-b] [-e] [-m <mask>] - Copy selection to clipboard
  -b: Copy biomes
  -e: Copy entities
  -m: Source mask

- //cut [pattern] [-b] [-e] [-m <mask>] - Cut selection (fill with pattern)
  -b: Copy biomes
  -e: Copy entities
  -m: Source mask

Paste Commands:
- //paste [-a] [-b] [-e] [-n] [-o] [-s] [-v] [-m <sourceMask>]
  -a: Skip air blocks
  -b: Paste biomes
  -e: Paste entities
  -n: No biomes
  -o: Paste at original position
  -s: Select pasted region
  -v: Include structure void
  -m: Source mask

Transform Commands:
- //rotate <y> [x] [z] - Rotate clipboard
- //flip [direction] - Flip clipboard

Clear:
- /clearclipboard - Clear clipboard

Example Workflow:
1. //pos1 100,64,100
2. //pos2 110,70,110
3. //copy -e - Copy with entities
4. //pos1 200,64,200
5. //paste -a - Paste, skip air
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Clipboard command (e.g., 'copy' or 'paste -a')",
                    }
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_schematic",
            description="""WorldEdit Schematic Commands - Save and load structures from files.

Schematics let you save structures to files and load them later.

Commands:
- /schem list [-p page] - List available schematics
- /schem load <filename> - Load schematic to clipboard
- /schem save <filename> - Save clipboard to schematic file
- /schem delete <filename> - Delete a schematic file

Workflow:
1. Build or copy a structure to clipboard
2. //schem save my_house
3. Later: //schem load my_house
4. //paste

Note: Schematic operations may be read-only depending on server configuration.
File access requires proper permissions on the server.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Schematic command (e.g., 'list' or 'load my_house')",
                    }
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_history",
            description="""WorldEdit History Commands - Undo and redo changes.

Manage edit history to undo mistakes or redo undone changes.

Commands:
- //undo [times] - Undo last edit(s)
- //redo [times] - Redo undone edit(s)
- //clearhistory - Clear edit history

Examples:
- //undo - Undo last edit
- //undo 5 - Undo last 5 edits
- //redo - Redo last undone edit
- //clearhistory - Clear all history (free memory)

Note: History is per-session and limited by server configuration.
Large edits consume more history memory.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "History command (e.g., 'undo' or 'redo 3')",
                    }
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_utility",
            description="""WorldEdit Utility Commands - Various useful operations.

Fill & Drain:
- //fill <pattern> <radius> [depth] - Fill holes
- //fillr <pattern> <radius> [depth] - Recursive fill
- //drain <radius> - Drain water/lava pools

Block Removal:
- /removeabove [size] [height] - Remove blocks above
- /removebelow [size] [height] - Remove blocks below
- /removenear <mask> [radius] - Remove nearby blocks

Environment:
- /fixwater <radius> - Fix water flow
- /fixlava <radius> - Fix lava flow
- /snow [size] - Simulate snowfall
- /thaw [size] - Melt snow/ice
- /green [size] - Convert dirt to grass
- /extinguish [radius] - Remove fire

Entity Management:
- /butcher [radius] - Remove mobs
- /remove <type> <radius> - Remove entities

Math:
- //calc <expression> - Evaluate math expression

Examples:
//drain 10 - Drain water within 10 blocks
/removeabove 20 5 - Remove 20 blocks up to 5 blocks high
/extinguish 30 - Put out fires within 30 blocks
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Utility command (e.g., 'drain 10' or 'green 20')",
                    }
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_biome",
            description="""WorldEdit Biome Commands - View and modify biomes.

Biomes affect terrain generation, mob spawning, weather, and more.

Commands:
- /biomelist [-p page] - List all biomes
- /biomeinfo [-t] - Get biome at location
  -t: Use target block instead of feet
- //setbiome <biome> - Set biome in selection

Example Usage:
1. //pos1 100,64,100
2. //pos2 150,100,150
3. //setbiome minecraft:plains

Common Biomes:
- minecraft:plains
- minecraft:forest
- minecraft:desert
- minecraft:taiga
- minecraft:savanna
- minecraft:jungle
- minecraft:swamp

Note: Biome changes affect new chunks and may require relogging to see effects.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Biome command (e.g., 'biomelist' or 'setbiome minecraft:plains')",
                    }
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_brush",
            description="""WorldEdit Brush Commands - Create brushes for click-based editing.

⚠️ IMPORTANT: Brushes require player interaction (clicking). Most won't work from console/RCON.
However, you CAN configure brushes from console using the configuration commands below.

BRUSH CONFIGURATION (works from console):
- /mask <mask> - Set brush mask (which blocks to affect)
- /material <pattern> - Set brush material/pattern
- /size <size> - Set brush size/radius
- /range <range> - Set brush range (reach distance)
- /tracemask [mask] - Set trace mask (what stops ray-trace)
- // or /, - Toggle super pickaxe

BASIC BRUSHES (require player interaction):
- /br sphere <pattern> [radius] [-h] - Sphere brush (-h for hollow)
- /br cylinder <pattern> [radius] [height] [-h] - Cylinder brush
- /br smooth [radius] [iterations] [mask] - Terrain smoother
- /br gravity [radius] [-h <height>] - Gravity simulator
- /br clipboard [-a] [-v] [-o] [-e] [-b] [-m <mask>] - Clipboard brush
- /br snowsmooth [radius] [iterations] - Snow terrain smoother
- /br extinguish [radius] - Fire extinguisher
- /br butcher [radius] [-p] [-n] [-g] [-a] [-b] - Kill mobs brush
- /br splatter <pattern> [radius] [decay] - Splatter brush

ADVANCED BRUSH SYSTEMS (require player interaction):

/brush apply <shape> [radius] <type> <params>
  Applies operations in specific shapes (sphere, cylinder, cuboid)
  Types:
  - forest <tree_type> - Plant trees in shape
  - item <item> [direction] - Use item in shape
  - set <pattern> - Place blocks in shape

  Examples:
  /br apply sphere 10 forest oak
  /br apply cylinder 15 set stone_bricks
  /br apply cuboid 20 item bone_meal up

/brush paint <shape> [radius] [density] <type> <params>
  Paints operations with density control (0-100% coverage)
  Types:
  - forest <tree_type> - Paint trees with density
  - item <item> [direction] - Paint with item at density
  - set <pattern> - Paint blocks at density

  Examples:
  /br paint sphere 15 30 forest oak  (30% tree coverage)
  /br paint cylinder 12 50 set grass_block  (50% grass coverage)

BRUSH WORKFLOW EXAMPLE:
1. /br sphere stone 5 - Create stone sphere brush
2. /mask dirt,grass_block - Only affect dirt/grass
3. /size 10 - Change size to 10
4. Player right-clicks to use brush

For AI/programmatic building, use region or generation commands instead of brushes.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Brush command (e.g., 'sphere stone 5')",
                    }
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_general",
            description="""WorldEdit Session & Global Commands - Manage limits, masks, and global options.

Includes history, side-effect, and mask controls:
- //undo, //redo, //clearhistory
- //limit, //timeout, //perf, //update, //reorder, //drawsel
- //gmask <mask>, //world <world>, //watchdog <mode>
- /worldedit help|version|reload

Include the proper leading / or // in the command string.

Examples:
//limit 500000
//gmask !air
/worldedit version
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "General WorldEdit command (include leading / or //)",
                    }
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_navigation",
            description="""WorldEdit Navigation Commands - Move the player or adjust position quickly.

Commands:
- /ascend [levels], /descend [levels]
- /ceil [-fg] [clearance], /thru, /up <distance>
- /unstuck, /jumpto

Most navigation commands require player context. From console, pair with
`execute as <player> run <command>` when necessary.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Navigation command (e.g., '/ascend 1')",
                    }
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_chunk",
            description="""WorldEdit Chunk Commands - Inspect or delete chunks in the world.

Commands:
- /chunkinfo - Show information about the chunk you target
- /listchunks [-p <page>] - List chunks in the current selection
- /delchunks [-o <age>] - Delete chunks (dangerous, now allowed by default)

Use with extreme caution—deleting chunks cannot be undone.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Chunk command (e.g., '/delchunks -o 30d')",
                    }
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_snapshot",
            description="""WorldEdit Snapshot Commands - Manage snapshot selection and restoration.

Commands:
- /snap list [-p <page>]
- /snap use <name>, /snap sel <index>
- /snap before <date>, /snap after <date>
- /restore [snapshot]

Ensure snapshots are configured on the server before using these commands.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Snapshot command (e.g., '/snap list')",
                    }
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_scripting",
            description="""WorldEdit Scripting Commands - Execute CraftScripts on the server.

Commands:
- /cs <filename> [args...] - Run a CraftScript in the scripts directory
- /.s [args...] - Re-run the previous script with optional arguments

Scripts must exist on the server filesystem. Include any required arguments.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Scripting command (e.g., '/cs terraform.js 10')",
                    }
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_reference",
            description="""WorldEdit Reference Commands - Search blocks/items or read help.

Commands:
- /searchitem [-bi] [-p <page>] <query>
- //help [-s] [-p <page>] [command]
- /schem formats, /we report

Use this tool to surface documentation directly inside the client.
Include the leading slash in each command.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Reference command (e.g., '/searchitem oak')",
                    }
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_tools",
            description="""WorldEdit Tool Binding Commands - Configure tool and brush options.

Tool Modes:
- /tool selwand - Selection wand (left click = pos1, right click = pos2)
- /tool tree [type] - Tree placer (right click to place trees)
- /tool repl <pattern> - Replacer tool (left click = source, right click = replace with pattern)
- /tool cycler - Block data cycler (cycle through block states)
- /tool stacker [range] [mask] - Block stacker
- /tool info - Block information tool
- /tool farwand - Long-range position setting (extends selection range)
- /none - Unbind current tool

Tool Configuration:
- /mask <mask> - Set which blocks the tool affects
- /material <pattern> - Set material for tool
- /range <distance> - Set tool reach distance
- /size <radius> - Set tool size/radius
- /tracemask [mask] - Set trace mask (what stops ray-trace)

Super Pickaxe:
- // or /, - Toggle super pickaxe on/off
- /sp single - Single block mode
- /sp area <radius> - Area destruction mode
- /sp recursive <radius> - Recursive destruction mode

Other:
- /toggleeditwand - Toggle edit wand on/off
- //wand - Get selection wand item

Tool Usage Examples:
- /tool repl stone_bricks - Left-click source block, right-click to paste stone bricks
- /tool tree oak - Right-click to place oak trees
- /tool farwand - Extend selection range for distant positioning

Note: Most commands require the player to hold an item; configure from console, then
have the player interact in-game with left/right clicks.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Tool binding command (include leading / or //)",
                    }
                },
                "required": ["command"],
            },
        ),
        # TIER 3: Helper Utilities
        Tool(
            name="validate_pattern",
            description="""Validate a WorldEdit pattern before using it in commands.

This tool helps you check if a pattern is valid and provides suggestions.

Pattern types supported:
- Single: stone, oak_planks
- Random: 50%stone,30%dirt,20%gravel
- Block states: oak_stairs[facing=north]
- Categories: ##wool, ##logs
- Special: #clipboard, *oak_log

Returns: Validation result and explanation of the pattern.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "The pattern to validate",
                    }
                },
                "required": ["pattern"],
            },
        ),
        Tool(
            name="validate_mask",
            description="""Validate a WorldEdit mask before using it in commands.

Masks determine which blocks are affected by operations.

Mask types supported:
- Block: stone, !air
- Categories: ##wool
- Special: #existing, #solid, #surface
- Expressions: =y<64, =x^2+z^2<100
- Random: %50

Returns: Validation result and explanation of the mask.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "mask": {
                        "type": "string",
                        "description": "The mask to validate",
                    }
                },
                "required": ["mask"],
            },
        ),
        Tool(
            name="get_server_info",
            description="""Get information about the Minecraft server.

Returns:
- Connected players
- Current time
- Server difficulty
- WorldEdit version (if detected)

Useful for checking server status before executing commands.
""",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="calculate_region_size",
            description="""Calculate the size and block count of a region.

Given two corner coordinates, calculates:
- Dimensions (width, height, depth)
- Total block count
- Estimated WorldEdit operation time

Useful for planning large builds and checking if operations will exceed limits.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "x1": {"type": "integer", "description": "First corner X"},
                    "y1": {"type": "integer", "description": "First corner Y"},
                    "z1": {"type": "integer", "description": "First corner Z"},
                    "x2": {"type": "integer", "description": "Second corner X"},
                    "y2": {"type": "integer", "description": "Second corner Y"},
                    "z2": {"type": "integer", "description": "Second corner Z"},
                },
                "required": ["x1", "y1", "z1", "x2", "y2", "z2"],
            },
        ),
        Tool(
            name="search_minecraft_item",
            description="""Search for Minecraft blocks/items by name.

Find blocks and items from Minecraft 1.21.3 to use in your builds.
Returns item ID, name, display name, and stack size.

Search examples:
- "stone" - finds stone, stone_bricks, stone_stairs, etc.
- "concrete" - finds all concrete colors
- "oak" - finds oak_planks, oak_log, oak_stairs, etc.
- "red" - finds red_wool, red_concrete, red_terracotta, etc.

Use this before building to:
- Check exact block names for WorldEdit commands
- Find color variants (e.g., all wool colors)
- Discover building material options
- Verify block exists in Minecraft 1.21.3

Returns: Up to 20 matching items with details.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term (partial name match, case-insensitive)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results to return (default: 20, max: 50)",
                        "default": 20,
                    }
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_player_position",
            description="""Get comprehensive position data for a player in the Minecraft world.

Returns:
- Player X, Y, Z coordinates (feet position)
- Player rotation (yaw, pitch - which direction they're facing)
- Target block (the block the player is looking at, if within 5 blocks)
- Surface level at player's position (for building context)

Useful for:
- Building at the player's current location
- Building where the player is looking (target block)
- Determining ground level for structures
- Understanding player orientation for directional builds

If no player_name is provided, gets the position of the first online player.

Returns: Comprehensive position context including coordinates, rotation, look target, and surface level.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "player_name": {
                        "type": "string",
                        "description": "Name of the player (optional - uses first online player if not specified)",
                    }
                },
                "required": [],
            },
        ),
        Tool(
            name="get_surface_level",
            description="""Find the surface (top solid block) Y-coordinate at given X, Z coordinates.

Useful for:
- Determining where to place building foundations
- Finding ground level before terraforming
- Calculating structure height above terrain
- Smart building placement on uneven terrain

Uses raycast from Y=320 (build limit) down to bedrock to find first solid block.

Returns: Surface Y-coordinate and block type at that location.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {
                        "type": "integer",
                        "description": "X coordinate",
                    },
                    "z": {
                        "type": "integer",
                        "description": "Z coordinate",
                    }
                },
                "required": ["x", "z"],
            },
        ),
        Tool(
            name="furniture_lookup",
            description="""Search and retrieve Minecraft furniture layouts for automated building.

This tool provides access to pre-designed furniture blueprints that can be automatically
placed in the world using WorldEdit commands.

Two operations:
1. **search** - Find furniture by name, category, or tags
2. **get** - Retrieve complete layout data for a specific furniture piece by ID

Each layout includes:
- Precise block placements with coordinates
- Material requirements and counts
- Bounding box dimensions
- Clearance requirements
- Design notes and variants

Use this to:
- Browse available furniture options
- Get exact specifications for furniture building
- Check material requirements before building
- Find furniture that matches a specific style or category

Examples:
- search: {"action": "search", "query": "table"} - Find all table designs
- search: {"action": "search", "category": "bedroom"} - Find bedroom furniture
- search: {"action": "search", "tags": ["compact", "modern"]} - Find compact modern furniture
- get: {"action": "get", "furniture_id": "simple_dining_table"} - Get full layout for dining table

After retrieving a layout, use the placement helper tool to build it in the world.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["search", "get"],
                        "description": "Operation to perform: 'search' for finding furniture, 'get' for retrieving specific layout",
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query (for action='search') - matches name, category, or tags",
                    },
                    "category": {
                        "type": "string",
                        "description": "Filter by category (for action='search'): bedroom, kitchen, living_room, etc.",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by tags (for action='search'): compact, modern, wood, stone, etc.",
                    },
                    "furniture_id": {
                        "type": "string",
                        "description": "Furniture ID to retrieve (for action='get')",
                    },
                },
                "required": ["action"],
            },
        ),
        Tool(
            name="place_furniture",
            description="""Place a furniture layout from the library at a world location.

This tool executes the exact WorldEdit and vanilla commands needed to instantiate a
layout. Use `preview_only=true` to review the commands before running them.

Inputs:
- `furniture_id` from furniture_lookup (must be a layout with automated coordinates)
- `origin_x`, `origin_y`, `origin_z` for the layout origin
- Optional `facing` override (north/east/south/west)
- `place_on_surface` (default: true) - If true, origin_y is treated as the FLOOR LEVEL
  and furniture is placed ON TOP (at origin_y + 1). If false, furniture is placed
  exactly at origin_y (may replace floor blocks).

IMPORTANT: When using get_surface_level, pass the returned Y directly as origin_y.
The furniture will automatically be placed on top of the surface. Example:
  surface_y = 64 (the floor block)
  place_furniture(origin_y=64, place_on_surface=true)  # Places furniture at Y=65 (on floor)

The tool reports a placement summary and highlights any command failures so you can
//undo if necessary.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "furniture_id": {
                        "type": "string",
                        "description": "Layout ID returned by furniture_lookup",
                    },
                    "origin_x": {"type": "integer", "description": "World origin X"},
                    "origin_y": {
                        "type": "integer",
                        "description": "World origin Y (floor level when place_on_surface=true, exact Y when false)"
                    },
                    "origin_z": {"type": "integer", "description": "World origin Z"},
                    "facing": {
                        "type": "string",
                        "enum": ["north", "south", "east", "west"],
                        "description": "Optional facing override"
                    },
                    "place_on_surface": {
                        "type": "boolean",
                        "description": "If true (default), treat origin_y as floor level and place furniture on top. If false, place at exact origin_y.",
                        "default": True
                    },
                    "preview_only": {
                        "type": "boolean",
                        "description": "Return commands without executing",
                        "default": False
                    }
                },
                "required": ["furniture_id", "origin_x", "origin_y", "origin_z"]
            },
        ),
        Tool(
            name="terrain_analyzer",
            description="""Analyze terrain in a Minecraft region to inform building decisions.

Scans a 3D region and provides comprehensive terrain analysis including:
- **Elevation statistics**: Min/max height, average, standard deviation, slope index
- **Block composition**: Surface blocks, liquids, vegetation, caves/cavities
- **Biome distribution**: Primary biomes in the region (when available)
- **Hazards**: Lava, water bodies, steep terrain, caves, dangerous blocks
- **Opportunities**: Flat areas, cliffs, coastlines, forested zones, large buildable spaces

Use this tool before:
- Planning large builds (castles, cities, farms)
- Deciding on foundation placement
- Assessing terraforming requirements
- Identifying scenic building locations
- Evaluating build site safety

The tool returns both machine-readable JSON data and a natural language summary.

**Performance Notes**:
- Resolution parameter controls sampling density (1=every block, 5=every 5th block, etc.)
- Default resolution=5 provides good balance of speed and accuracy
- Max samples limit prevents excessive scanning (default 10,000 blocks)
- Larger regions or finer resolution = longer scan time
- Recommended: Use resolution=5-10 for large areas, resolution=2-3 for small detailed scans

**Example Usage**:
- Quick overview: terrain_analyzer(x1=0, y1=60, z1=0, x2=200, y2=100, z2=200) (uses default resolution=5)
- Detailed scan: terrain_analyzer(x1=100, y1=60, z1=200, x2=150, y2=80, z2=250, resolution=2)
- Fast large area: terrain_analyzer(x1=0, y1=0, z1=0, x2=500, y2=100, z2=500, resolution=10)
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "x1": {
                        "type": "integer",
                        "description": "First corner X coordinate",
                    },
                    "y1": {
                        "type": "integer",
                        "description": "First corner Y coordinate",
                    },
                    "z1": {
                        "type": "integer",
                        "description": "First corner Z coordinate",
                    },
                    "x2": {
                        "type": "integer",
                        "description": "Second corner X coordinate",
                    },
                    "y2": {
                        "type": "integer",
                        "description": "Second corner Y coordinate",
                    },
                    "z2": {
                        "type": "integer",
                        "description": "Second corner Z coordinate",
                    },
                    "resolution": {
                        "type": "integer",
                        "description": "Sampling resolution (1=every block, 2=every other block, etc.). Default: 5. Higher = faster, lower = more accurate.",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 20,
                    },
                    "max_samples": {
                        "type": "integer",
                        "description": "Maximum number of samples to take (safety limit). Default: 10000",
                        "default": 10000,
                        "minimum": 100,
                        "maximum": 50000,
                    },
                },
                "required": ["x1", "y1", "z1", "x2", "y2", "z2"],
            },
        ),
        Tool(
            name="analyze_placement_area",
            description="""Analyze blocks in a local area to provide spatial context for precise placement.

**CRITICAL**: Use this tool BEFORE placing furniture or building roofs to understand the local spatial context.

**Solves Key Problems**:
1. **Furniture Placement**: Find exact floor/ceiling Y coordinates to avoid placing furniture in floor or floating in air
2. **Roof Construction**: Detect existing stairs, get next layer offset to avoid stacking stairs vertically
3. **Any Precise Placement**: Understand local block configuration before building

**When to Use**:
- ✅ BEFORE placing furniture → scan to find floor_y and ceiling_y
- ✅ BEFORE adding roof layer → scan to find existing stairs and next offset
- ✅ BEFORE placing any block that needs to align with existing structure

**Analysis Types**:
- **furniture_placement** - Find floor/ceiling surfaces for furniture placement
- **roof_context** - Analyze existing roof structure, get next layer offset
- **surfaces** - Detect floor, ceiling, walls only
- **general** - All analysis (surfaces + furniture + roof + block grid)

**Parameters**:
- center_x, center_y, center_z - Point to analyze around
- radius - Scan radius (default 5 blocks, max 10 for performance)
- analysis_type - What to detect (default "general")

**Returns**:
- **surfaces**: floor_y (top of floor block), ceiling_y (bottom of ceiling block), walls (N/S/E/W)
- **furniture_placement**: recommended_floor_y (place furniture here), recommended_ceiling_y (hang lamps here), placement_type, clear_space
- **roof_context**: existing_stairs, slope_direction, last_stair_layer_y, next_layer_offset (step inward), recommendation

**Example Workflows**:

**Furniture Placement**:
```
1. analyze_placement_area(center_x=100, center_y=65, center_z=200, analysis_type="furniture_placement")
   → Returns: {"furniture_placement": {"recommended_floor_y": 65}}
2. place_furniture(furniture_id="table", origin_x=100, origin_y=65, origin_z=200)
   → Furniture placed correctly ON TOP of floor!
```

**Roof Construction**:
```
1. analyze_placement_area(center_x=100, center_y=72, center_z=105, radius=8, analysis_type="roof_context")
   → Returns: {"roof_context": {"next_layer_offset": {"x": 0, "y": 1, "z": 1}, "recommendation": "Step inward Z+1 and up Y+1"}}
2. Place next stair layer at Y=73, Z=106 (stepped inward)
   → Stairs properly offset, not stacked!
```

**Performance**: Scans up to 500 blocks (5×5×5 radius ≈ 125 blocks). Use smaller radius for speed.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "center_x": {
                        "type": "integer",
                        "description": "Center X coordinate"
                    },
                    "center_y": {
                        "type": "integer",
                        "description": "Center Y coordinate"
                    },
                    "center_z": {
                        "type": "integer",
                        "description": "Center Z coordinate"
                    },
                    "radius": {
                        "type": "integer",
                        "description": "Scan radius in blocks (default 5, max 10)",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 10
                    },
                    "analysis_type": {
                        "type": "string",
                        "enum": ["general", "surfaces", "furniture_placement", "roof_context"],
                        "description": "Type of analysis to perform (default 'general')",
                        "default": "general"
                    }
                },
                "required": ["center_x", "center_y", "center_z"]
            },
        ),
        Tool(
            name="spatial_awareness_scan",
            description="""⚡ ADVANCED SPATIAL AWARENESS V2 - Fast multi-strategy spatial analysis (10-20x faster than V1!)

**🎯 WHEN TO USE**: Use this tool BEFORE placing ANY blocks to understand the spatial context.

**⚠️ MANDATORY FOR**:
- ✅ ALL furniture placement → Scan at furniture center BEFORE placing
- ✅ ALL roof construction → Scan each layer BEFORE placing stairs
- ✅ ALL interior walls → Scan to ensure ceiling height clearance
- ✅ ALL window placement → Scan to detect wall thickness and frame depth
- ✅ ANY block placement requiring alignment with existing structure

**WHY V2 IS BETTER**:
- 🚀 10-20x faster (2-10 seconds vs 30-60 seconds)
- 📊 MORE information (clearance, materials, structure type)
- 🎯 Better recommendations (style matching, placement guidance)
- ⚡ Uses WorldEdit bulk operations (not per-block queries)

**DETAIL LEVELS** (choose speed vs. information tradeoff):

**LOW** (~50 commands, 2-3 seconds):
- Floor/ceiling detection (Y coordinates)
- 3D voxel density map
- Basic material summary
- USE FOR: Quick checks before simple placements

**MEDIUM** (~100 commands, 4-5 seconds) - ⭐ RECOMMENDED:
- Everything in LOW +
- Clearance in 6 directions (north/south/east/west/up/down)
- Blocked direction detection
- USE FOR: Most furniture, wall, and structural placements

**HIGH** (~200 commands, 8-10 seconds):
- Everything in MEDIUM +
- Material palette detection (style matching)
- Structure pattern detection (roof/building/wall classification)
- Architectural style inference (medieval/modern/rustic)
- USE FOR: Complex builds, style-matching requirements, quality builds

**RETURNS**:
```json
{
  "floor_y": 64,              // Y coordinate of floor block
  "ceiling_y": 69,            // Y coordinate of ceiling block
  "clearance": {              // Space in each direction
    "north": {"clearance": 5, "blocked_at": null},
    "south": {"clearance": 3, "blocked_at": 4, "blocking_block": "stone_bricks"},
    "up": {"clearance": 5},
    "down": {"clearance": 0, "blocked_at": 1}
  },
  "material_summary": {
    "dominant_material": "oak_planks",
    "all_materials": ["oak_planks", "stone_bricks", "glass"],
    "material_diversity": 0.65
  },
  "structure_patterns": {      // HIGH detail only
    "structure_type": "building",
    "has_stairs": true,
    "has_windows": true,
    "complexity": "high",
    "is_hollow": true
  },
  "material_palette": {         // HIGH detail only
    "primary_materials": ["oak_planks", "stone_bricks", "glass"],
    "wood_type": "oak",
    "stone_type": "stone_bricks",
    "style": "medieval"
  },
  "recommendations": {
    "floor_placement_y": 65,    // Place floor furniture HERE
    "ceiling_placement_y": 69,  // Hang ceiling items HERE
    "ceiling_height": 4,        // Blocks between floor and ceiling
    "clear_for_placement": true,
    "suggested_materials": ["oak_planks", "stone_bricks"],
    "detected_style": "medieval",
    "warnings": ["Low ceiling - may feel cramped"]
  },
  "summary": "Human-readable text summary..."
}
```

**EXAMPLE WORKFLOWS**:

**Furniture Placement (MEDIUM detail)**:
```
1. spatial_awareness_scan(center_x=100, center_y=65, center_z=200, radius=5, detail_level="medium")
   → Returns: floor_placement_y=65, ceiling_placement_y=69, clearance in all directions
2. Verify clearance: north=5 blocks, east=3 blocks → Table will fit!
3. place_furniture(furniture_id="table", origin_x=100, origin_y=65, origin_z=200)
   → Perfect placement on floor with confirmed clearance!
```

**Roof Construction (LOW detail - fast repeated scans)**:
```
1. spatial_awareness_scan(center_x=100, center_y=72, center_z=105, radius=8, detail_level="low")
   → Returns: Detects existing structures at Y=71
2. Place stairs at Y=72 (offset from Y=71 layer)
3. Repeat scan at Y=73 for next layer
   → Fast enough to scan before each layer!
```

**Style-Matching Build (HIGH detail)**:
```
1. spatial_awareness_scan(center_x=100, center_y=65, center_z=200, radius=10, detail_level="high")
   → Returns: style="medieval", wood_type="oak", stone_type="stone_bricks"
2. Build new structure using oak_planks and stone_bricks to match
   → Cohesive architectural style!
```

**Performance Tips**:
- Use LOW for quick/repeated scans (roof layers, simple checks)
- Use MEDIUM for most placements (furniture, walls, interiors)
- Use HIGH when you need style matching or detailed structure analysis
- Smaller radius = faster (radius 3-5 is usually sufficient)

**Comparison to V1 (analyze_placement_area)**:
- V1: 1,500+ RCON commands, 30-60 seconds, limited information
- V2 LOW: 50 commands, 2-3 seconds, MORE information
- V2 MEDIUM: 100 commands, 4-5 seconds, MUCH MORE information
- V2 HIGH: 200 commands, 8-10 seconds, COMPREHENSIVE analysis

**⚠️ CRITICAL REMINDER**: ALWAYS scan before placing blocks that need alignment!
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "center_x": {
                        "type": "integer",
                        "description": "Center X coordinate to analyze around"
                    },
                    "center_y": {
                        "type": "integer",
                        "description": "Center Y coordinate to analyze around"
                    },
                    "center_z": {
                        "type": "integer",
                        "description": "Center Z coordinate to analyze around"
                    },
                    "radius": {
                        "type": "integer",
                        "description": "Scan radius in blocks (default 5, recommended 3-8 for balance)",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 15
                    },
                    "detail_level": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Analysis detail level: 'low' (fast, 2-3s), 'medium' (balanced, 4-5s, RECOMMENDED), 'high' (comprehensive, 8-10s)",
                        "default": "medium"
                    }
                },
                "required": ["center_x", "center_y", "center_z"]
            },
        ),
        Tool(
            name="calculate_shape",
            description="""Calculate perfect circles, spheres, domes, ellipses, and arches for Minecraft building.

Uses Bresenham's algorithms for pixel-perfect mathematical accuracy. Returns coordinate lists and ASCII previews.

**Shape Types**:
- **circle**: 2D circle (for towers, ponds, circular rooms)
- **sphere**: 3D sphere (hollow or filled)
- **dome**: Hemisphere or partial sphere (for roofs, domes)
- **ellipse**: 2D ellipse (oval shapes)
- **arch**: Arch structure (for doorways, bridges, windows)

**Common Uses**:
- Tower foundations (circle)
- Dome roofs (dome, hemisphere style)
- Spherical structures (sphere, hollow)
- Arched doorways and bridges (arch)
- Oval rooms and ponds (ellipse)

**Output**: Returns coordinates list, block count, ASCII preview, and usage tips.

**Examples**:
- Circle tower base: calculate_shape(shape="circle", radius=10, filled=True)
- Hollow sphere: calculate_shape(shape="sphere", radius=8, hollow=True)
- Cathedral dome: calculate_shape(shape="dome", radius=15, style="hemisphere")
- Bridge arch: calculate_shape(shape="arch", width=10, height=8, depth=2)
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "shape": {
                        "type": "string",
                        "description": "Shape type: 'circle', 'sphere', 'dome', 'ellipse', or 'arch'",
                        "enum": ["circle", "sphere", "dome", "ellipse", "arch"]
                    },
                    "radius": {
                        "type": "integer",
                        "description": "Radius in blocks (for circle, sphere, dome)",
                        "minimum": 1,
                        "maximum": 100
                    },
                    "width": {
                        "type": "integer",
                        "description": "Width in blocks (for ellipse, arch)",
                        "minimum": 1,
                        "maximum": 100
                    },
                    "height": {
                        "type": "integer",
                        "description": "Height in blocks (for ellipse, arch)",
                        "minimum": 1,
                        "maximum": 100
                    },
                    "depth": {
                        "type": "integer",
                        "description": "Depth/thickness in blocks (for arch). Default: 1",
                        "minimum": 1,
                        "maximum": 20,
                        "default": 1
                    },
                    "filled": {
                        "type": "boolean",
                        "description": "Fill interior (for circle, ellipse). Default: false",
                        "default": False
                    },
                    "hollow": {
                        "type": "boolean",
                        "description": "Hollow shell only (for sphere). Default: true",
                        "default": True
                    },
                    "style": {
                        "type": "string",
                        "description": "Dome style: 'hemisphere', 'three_quarter', 'low'. Default: hemisphere",
                        "enum": ["hemisphere", "three_quarter", "low"],
                        "default": "hemisphere"
                    }
                },
                "required": ["shape"]
            }
        ),
        Tool(
            name="calculate_window_spacing",
            description="""Calculate optimal window and door placement for building facades.

Based on architectural principles and aesthetic guidelines. Returns precise positions with spacing recommendations.

**Spacing Styles**:
- **even**: Evenly distributed with equal spacing (modern, balanced)
- **golden_ratio**: Positioned using φ = 1.618 (artistic, organic)
- **symmetric**: Mirrored around center axis (classical, formal)
- **clustered**: Grouped in pairs/triplets (contemporary, rhythmic)

**Use Cases**:
- Facade design (calculate all windows at once)
- Door placement (centered, offset, left/right)
- Architectural rhythm and balance
- Style-specific layouts (medieval, modern, classical)

**Output**: Returns window positions, spacing details, and architectural recommendations.

**Examples**:
- Castle wall: calculate_window_spacing(wall_length=20, window_width=2, spacing_style="symmetric")
- Modern facade: calculate_window_spacing(wall_length=30, window_width=3, spacing_style="even", window_count=5)
- Villa windows: calculate_window_spacing(wall_length=25, window_width=2, spacing_style="golden_ratio")
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "wall_length": {
                        "type": "integer",
                        "description": "Total wall length in blocks",
                        "minimum": 3,
                        "maximum": 200
                    },
                    "window_width": {
                        "type": "integer",
                        "description": "Width of each window in blocks",
                        "minimum": 1,
                        "maximum": 10
                    },
                    "spacing_style": {
                        "type": "string",
                        "description": "Spacing style: 'even', 'golden_ratio', 'symmetric', or 'clustered'. Default: even",
                        "enum": ["even", "golden_ratio", "symmetric", "clustered"],
                        "default": "even"
                    },
                    "window_count": {
                        "type": "integer",
                        "description": "Number of windows (auto-calculated if not specified)",
                        "minimum": 1,
                        "maximum": 50
                    }
                },
                "required": ["wall_length", "window_width"]
            }
        ),
        Tool(
            name="check_symmetry",
            description="""Check structural symmetry across an axis for quality assurance.

Analyzes mirrored block positions to detect asymmetries in builds. Essential for castles, palaces, and formal architecture.

**Axes**:
- **x**: Mirror across X axis (left/right symmetry)
- **z**: Mirror across Z axis (front/back symmetry)
- **y**: Mirror across Y axis (top/bottom symmetry)

**Use Cases**:
- Castle quality control (check if towers are symmetric)
- Palace facade verification (ensure balanced design)
- Formal architecture validation (classical builds require symmetry)
- Error detection (find builder mistakes instantly)

**Parameters**:
- `tolerance`: Allow N asymmetric blocks (0 = perfect symmetry required)
- `resolution`: 1 = check every block, 2 = check every other block (faster)

**Output**: Symmetry score (0-100%), asymmetric block list with fix recommendations.

**Examples**:
- Check castle: check_symmetry(x1=100, y1=64, z1=100, x2=150, y2=90, z2=150, axis="x")
- Palace facade: check_symmetry(x1=100, y1=60, z1=100, x2=120, y2=80, z2=140, axis="z", tolerance=5)
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "x1": {"type": "integer", "description": "First corner X"},
                    "y1": {"type": "integer", "description": "First corner Y"},
                    "z1": {"type": "integer", "description": "First corner Z"},
                    "x2": {"type": "integer", "description": "Second corner X"},
                    "y2": {"type": "integer", "description": "Second corner Y"},
                    "z2": {"type": "integer", "description": "Second corner Z"},
                    "axis": {
                        "type": "string",
                        "description": "Axis to check: 'x', 'z', or 'y'. Default: x",
                        "enum": ["x", "z", "y"],
                        "default": "x"
                    },
                    "tolerance": {
                        "type": "integer",
                        "description": "Allowed asymmetric blocks (0 = perfect symmetry). Default: 0",
                        "minimum": 0,
                        "default": 0
                    },
                    "resolution": {
                        "type": "integer",
                        "description": "Sampling resolution (1 = every block, 2 = every other). Default: 1",
                        "minimum": 1,
                        "maximum": 5,
                        "default": 1
                    }
                },
                "required": ["x1", "y1", "z1", "x2", "y2", "z2"]
            }
        ),
        Tool(
            name="analyze_lighting",
            description="""Analyze lighting levels and suggest optimal torch/lantern placement.

Identifies dark spots where mobs can spawn (light level < 8). Prevents surprises and ensures safe, well-lit builds.

**Analysis Provides**:
- Average light level across region
- Dark spot detection and count
- Mob spawn risk assessment (HIGH/MEDIUM/LOW)
- Light distribution breakdown (well-lit/dim/dark percentages)
- Optimal light source placement recommendations

**Use Cases**:
- Interior lighting design (rooms, hallways, chambers)
- Cave illumination (prevent mob spawns underground)
- Exterior lighting (pathways, courtyards, walls)
- Safety verification (check if areas are spawn-proof)

**Output**: Light analysis with dark spot coordinates and recommended torch/lantern positions.

**Examples**:
- Check interior: analyze_lighting(x1=100, y1=64, z1=100, x2=120, y2=70, z2=120, resolution=2)
- Cave safety: analyze_lighting(x1=0, y1=10, z1=0, x2=50, y2=30, z2=50)
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "x1": {"type": "integer", "description": "First corner X"},
                    "y1": {"type": "integer", "description": "First corner Y"},
                    "z1": {"type": "integer", "description": "First corner Z"},
                    "x2": {"type": "integer", "description": "Second corner X"},
                    "y2": {"type": "integer", "description": "Second corner Y"},
                    "z2": {"type": "integer", "description": "Second corner Z"},
                    "resolution": {
                        "type": "integer",
                        "description": "Sampling resolution (1-5). Default: 2",
                        "minimum": 1,
                        "maximum": 5,
                        "default": 2
                    }
                },
                "required": ["x1", "y1", "z1", "x2", "y2", "z2"]
            }
        ),
        Tool(
            name="validate_structure",
            description="""Validate structural integrity and detect physics violations.

Checks for floating blocks, unsupported gravity-affected blocks (sand, gravel), and physics glitches before they happen.

**Detects**:
- **Gravity violations**: Sand, gravel, concrete powder without support
- **Floating blocks**: Blocks with no adjacent solid blocks
- **Unsupported regions**: Large overhangs with no pillars
- **Physics glitches**: Blocks that will fall when updated

**Prevents**:
- Unexpected collapses during gameplay
- Redstone update cascades
- Visual glitches and unnatural structures
- Player-caused accidents (breaking support blocks)

**Use Cases**:
- Pre-build validation (check before completing)
- Quality assurance (ensure realistic structure)
- Bridge verification (check cantilever supports)
- Terraforming safety (verify modified terrain)

**Output**: Validation report with issue list, severity levels, and fix recommendations.

**Examples**:
- Check bridge: validate_structure(x1=100, y1=60, z1=100, x2=150, y2=70, z2=110)
- Verify building: validate_structure(x1=200, y1=64, z1=200, x2=220, y2=80, z2=220, resolution=2)
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "x1": {"type": "integer", "description": "First corner X"},
                    "y1": {"type": "integer", "description": "First corner Y"},
                    "z1": {"type": "integer", "description": "First corner Z"},
                    "x2": {"type": "integer", "description": "Second corner X"},
                    "y2": {"type": "integer", "description": "Second corner Y"},
                    "z2": {"type": "integer", "description": "Second corner Z"},
                    "resolution": {
                        "type": "integer",
                        "description": "Sampling resolution (1-3). Default: 1",
                        "minimum": 1,
                        "maximum": 3,
                        "default": 1
                    }
                },
                "required": ["x1", "y1", "z1", "x2", "y2", "z2"]
            }
        ),
        Tool(
            name="generate_terrain",
            description="""Generate realistic terrain features using WorldEdit noise functions.

Creates natural-looking landscapes with pre-tested recipes for hills, mountains, valleys, plateaus, and ranges.

**Terrain Types**:
- **rolling_hills**: Gentle undulating hills (Perlin noise)
- **rugged_mountains**: Sharp peaks and ridges (Ridged Multifractal)
- **valley_network**: Interconnected valleys for rivers (Inverted Perlin)
- **mountain_range**: Linear mountain chain in a direction (Oriented Ridged)
- **plateau**: Flat-topped elevation with rough edges

**Process**:
1. Sets WorldEdit selection
2. Applies noise-based deformation
3. Smooths terrain for natural appearance
4. Returns summary with parameters used

**Safety**: Amplitude capped at 50 blocks, region size limited

**Use Cases**:
- Create backdrop for castle/fortress
- Generate farmland with gentle slopes
- Add river valley systems
- Build continental divide features
- Make dramatic mesa formations

**Examples**:
- Gentle hills: generate_terrain(type="rolling_hills", x1=0, y1=64, z1=0, x2=100, y2=80, z2=100, scale=18, amplitude=6)
- Mountains: generate_terrain(type="rugged_mountains", x1=0, y1=64, z1=0, x2=100, y2=100, z2=100, scale=28, amplitude=18)
- Valleys: generate_terrain(type="valley_network", x1=0, y1=64, z1=0, x2=100, y2=80, z2=100, scale=22, depth=10)
- Range: generate_terrain(type="mountain_range", x1=0, y1=64, z1=0, x2=200, y2=100, z2=100, direction="north-south", amplitude=20)
- Plateau: generate_terrain(type="plateau", x1=0, y1=64, z1=0, x2=80, y2=85, z2=80, height=15)
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["rolling_hills", "rugged_mountains", "valley_network", "mountain_range", "plateau"],
                        "description": "Terrain type to generate"
                    },
                    "x1": {"type": "integer", "description": "Region corner 1 X"},
                    "y1": {"type": "integer", "description": "Region corner 1 Y (base elevation)"},
                    "z1": {"type": "integer", "description": "Region corner 1 Z"},
                    "x2": {"type": "integer", "description": "Region corner 2 X"},
                    "y2": {"type": "integer", "description": "Region corner 2 Y (max elevation)"},
                    "z2": {"type": "integer", "description": "Region corner 2 Z"},
                    "scale": {
                        "type": "integer",
                        "description": "Feature scale/breadth (10-40, varies by type)",
                        "minimum": 10,
                        "maximum": 40
                    },
                    "amplitude": {
                        "type": "integer",
                        "description": "Height variation for hills/mountains (3-30)",
                        "minimum": 3,
                        "maximum": 50
                    },
                    "depth": {
                        "type": "integer",
                        "description": "Valley depth (5-20, for valley_network only)",
                        "minimum": 5,
                        "maximum": 20
                    },
                    "height": {
                        "type": "integer",
                        "description": "Plateau height (10-25, for plateau only)",
                        "minimum": 10,
                        "maximum": 25
                    },
                    "direction": {
                        "type": "string",
                        "enum": ["north-south", "east-west", "northeast-southwest", "northwest-southeast"],
                        "description": "Range direction (for mountain_range only)"
                    },
                    "octaves": {
                        "type": "integer",
                        "description": "Noise detail level (3-6, more = finer details)",
                        "minimum": 3,
                        "maximum": 6
                    },
                    "smooth_iterations": {
                        "type": "integer",
                        "description": "Post-smoothing passes (1-4, more = smoother)",
                        "minimum": 1,
                        "maximum": 10
                    },
                    "seed": {
                        "type": "integer",
                        "description": "Random seed (optional, auto-generated if omitted)"
                    }
                },
                "required": ["type", "x1", "y1", "z1", "x2", "y2", "z2"]
            }
        ),
        Tool(
            name="texture_terrain",
            description="""Apply natural surface texturing to terrain based on biome/style.

Replaces base blocks and overlays surface patterns to create realistic-looking landscapes.

**Texturing Styles**:
- **temperate**: Grass, moss, dirt (plains/forest biomes)
- **alpine**: Stone, snow, gravel (high altitude)
- **desert**: Sand, sandstone, terracotta (arid regions)
- **volcanic**: Basalt, magma, blackstone (lava zones)
- **jungle**: Rich soil, podzol, moss (tropical)
- **swamp**: Mud, clay, damp grass (wetlands)

**Process**:
1. Sets WorldEdit selection
2. Replaces bulk material (stone → style-appropriate base)
3. Overlays surface pattern (grass/snow/sand on top)
4. Returns confirmation

**When to Use**:
- AFTER terrain shaping (hills, mountains, etc.)
- To convert raw stone terrain to natural-looking landscape
- To theme an area for specific biome
- For visual cohesion across large regions

**Examples**:
- Grass hills: texture_terrain(style="temperate", x1=0, y1=64, z1=0, x2=100, y2=80, z2=100)
- Snowy peaks: texture_terrain(style="alpine", x1=0, y1=64, z1=0, x2=100, y2=100, z2=100)
- Desert mesa: texture_terrain(style="desert", x1=0, y1=64, z1=0, x2=100, y2=85, z2=100)
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "style": {
                        "type": "string",
                        "enum": ["temperate", "alpine", "desert", "volcanic", "jungle", "swamp"],
                        "description": "Texturing style/biome theme"
                    },
                    "x1": {"type": "integer", "description": "Region corner 1 X"},
                    "y1": {"type": "integer", "description": "Region corner 1 Y"},
                    "z1": {"type": "integer", "description": "Region corner 1 Z"},
                    "x2": {"type": "integer", "description": "Region corner 2 X"},
                    "y2": {"type": "integer", "description": "Region corner 2 Y"},
                    "z2": {"type": "integer", "description": "Region corner 2 Z"}
                },
                "required": ["style", "x1", "y1", "z1", "x2", "y2", "z2"]
            }
        ),
        Tool(
            name="smooth_terrain",
            description="""Smooth terrain to remove blocky/steppy appearance.

Applies WorldEdit smoothing algorithm to blend block heights naturally.

**Use Cases**:
- Post-processing after terrain generation
- Fixing blocky noise artifacts
- Creating gentle transitions between elevations
- Reducing harsh cliffs to natural slopes

**Parameters**:
- iterations: More passes = smoother (2-4 recommended)
- Less smoothing preserves sharp features (mountains)
- More smoothing creates gentler slopes (hills)

**Best Practices**:
- Always smooth after //deform operations
- Use 1-2 iterations for mountains (preserve peaks)
- Use 3-4 iterations for rolling hills (gentle)
- Can apply mask to smooth only certain blocks

**Examples**:
- Light smoothing: smooth_terrain(x1=0, y1=64, z1=0, x2=100, y2=80, z2=100, iterations=2)
- Heavy smoothing: smooth_terrain(x1=0, y1=64, z1=0, x2=100, y2=80, z2=100, iterations=4)
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "x1": {"type": "integer", "description": "Region corner 1 X"},
                    "y1": {"type": "integer", "description": "Region corner 1 Y"},
                    "z1": {"type": "integer", "description": "Region corner 1 Z"},
                    "x2": {"type": "integer", "description": "Region corner 2 X"},
                    "y2": {"type": "integer", "description": "Region corner 2 Y"},
                    "z2": {"type": "integer", "description": "Region corner 2 Z"},
                    "iterations": {
                        "type": "integer",
                        "description": "Number of smoothing passes (1-10)",
                        "minimum": 1,
                        "maximum": 10,
                        "default": 2
                    },
                    "mask": {
                        "type": "string",
                        "description": "Optional mask to limit smoothing (e.g., 'grass_block,dirt')"
                    }
                },
                "required": ["x1", "y1", "z1", "x2", "y2", "z2"]
            }
        ),
        Tool(
            name="building_pattern_lookup",
            description="""Search and retrieve building patterns for architectural elements in Minecraft.

This tool provides access to a comprehensive library of building patterns including roofs,
windows, doors, corner pillars, chimneys, and other architectural elements with layer-by-layer
construction instructions.

**IMPORTANT - Discovery First**: If you don't know what's available, use discovery actions:
1. **browse** - List all available patterns (names and IDs only)
2. **categories** - List all categories with pattern counts
3. **subcategories** - List subcategories for a specific category
4. **tags** - List all available tags with usage counts
5. **search** - Find patterns by name, category, subcategory, or tags
6. **get** - Retrieve complete pattern data with full layer-by-layer instructions

**Discovery Workflow (RECOMMENDED)**:
1. Start with action="browse" or action="categories" to see what's available
2. Use action="subcategories" with category="roofing" to see roof types
3. Then search specifically: action="search" with appropriate filters
4. Finally get the pattern: action="get" with pattern_id

**Pattern Contents**:
- Layer-by-layer block placement instructions (3D blueprints)
- Material requirements and counts
- Dimensions (width, height, depth)
- Construction notes and best practices
- Related patterns and variants
- Difficulty level

**Examples**:
- browse: {"action": "browse"} - List all 29 patterns (quick overview)
- categories: {"action": "categories"} - See available categories and counts
- subcategories: {"action": "subcategories", "category": "roofing"} - List roof types
- tags: {"action": "tags"} - See all available tags
- search: {"action": "search", "query": "gable"} - Find all gable roof patterns
- search: {"action": "search", "category": "roofing"} - All roofing patterns
- get: {"action": "get", "pattern_id": "gable_oak_medium"} - Get full instructions

After retrieving a pattern, use the layer information to build with WorldEdit commands.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["browse", "categories", "subcategories", "tags", "search", "get"],
                        "description": "Operation: 'browse' (list all), 'categories' (list categories), 'subcategories' (list subcats), 'tags' (list tags), 'search' (find patterns), 'get' (retrieve pattern)",
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query (for action='search') - matches name, category, subcategory, or tags",
                    },
                    "category": {
                        "type": "string",
                        "description": "Category name (for action='search' or action='subcategories'): roofing, facades, corners, details",
                    },
                    "subcategory": {
                        "type": "string",
                        "description": "Filter by subcategory (for action='search'): gable, hip, slab_roof, etc.",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by tags (for action='search'): oak, stone, easy, medium, hard, etc.",
                    },
                    "pattern_id": {
                        "type": "string",
                        "description": "Pattern ID to retrieve (for action='get')",
                    },
                },
                "required": ["action"],
            },
        ),
        Tool(
            name="place_building_pattern",
            description="""Instantiate a structured building pattern at the desired coordinates.

Patterns with detailed layer data can be placed automatically. Use `preview_only=true`
to inspect the generated commands before modifying the world.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern_id": {
                        "type": "string",
                        "description": "Pattern identifier from building_pattern_lookup",
                    },
                    "origin_x": {"type": "integer", "description": "Placement origin X"},
                    "origin_y": {"type": "integer", "description": "Placement origin Y"},
                    "origin_z": {"type": "integer", "description": "Placement origin Z"},
                    "facing": {
                        "type": "string",
                        "enum": ["north", "south", "east", "west"],
                        "description": "Optional facing override"
                    },
                    "preview_only": {
                        "type": "boolean",
                        "description": "Return commands instead of executing",
                        "default": False
                    }
                },
                "required": ["pattern_id", "origin_x", "origin_y", "origin_z"]
            },
        ),
        Tool(
            name="schematic_library",
            description="""Manage local `.schem` files and load them into the WorldEdit schematic folder.

Actions:
- `list` – show available schematics under the repository `schemas/` directory
- `info` – inspect dimensions/metadata for a specific schematic
- `prepare` – copy the schematic into the Minecraft server's schematics folder without loading
- `load` – copy (if needed) and execute `//schem load schem <name>` so it is ready to paste

After loading, use the `worldedit_clipboard` tool with `command="paste -a -o"` (or similar) to place it in the world.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["list", "info", "prepare", "load"],
                        "description": "Operation to perform"
                    },
                    "name": {
                        "type": "string",
                        "description": "Schematic filename (with or without .schem extension)"
                    },
                    "target_name": {
                        "type": "string",
                        "description": "Optional destination name when copying to the server schematics folder"
                    }
                },
                "required": ["action"],
            },
        ),
        Tool(
            name="terrain_pattern_lookup",
            description="""Search and retrieve terrain patterns for natural elements in Minecraft.

This tool provides access to a comprehensive library of terrain patterns including trees,
bushes, rocks, ponds, paths, and decorative natural elements with layer-by-layer
construction instructions.

**IMPORTANT - Discovery First**: If you don't know what's available, use discovery actions:
1. **browse** - List all available patterns (names and IDs only)
2. **categories** - List all categories with pattern counts
3. **subcategories** - List subcategories for a specific category
4. **tags** - List all available tags with usage counts
5. **search** - Find patterns by name, category, subcategory, or tags
6. **get** - Retrieve complete pattern data with full layer-by-layer instructions

**Discovery Workflow (RECOMMENDED)**:
1. Start with action="browse" or action="categories" to see what's available
2. Use action="subcategories" with category="vegetation" to see tree/bush types
3. Then search specifically: action="search" with appropriate filters
4. Finally get the pattern: action="get" with pattern_id

**Pattern Contents**:
- Layer-by-layer block placement instructions (3D blueprints)
- Material requirements and counts
- Dimensions (width, height, depth)
- Construction notes and placement tips
- Related patterns and variants
- Difficulty level

**Examples**:
- browse: {"action": "browse"} - List all 41 patterns (quick overview)
- categories: {"action": "categories"} - See available categories and counts
- subcategories: {"action": "subcategories", "category": "vegetation"} - List tree/bush types
- tags: {"action": "tags"} - See all available tags
- search: {"action": "search", "query": "oak tree"} - Find oak tree patterns
- search: {"action": "search", "category": "vegetation"} - All vegetation patterns
- get: {"action": "get", "pattern_id": "oak_tree_medium"} - Get full instructions

After retrieving a pattern, use the layer information to build with WorldEdit commands.
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["browse", "categories", "subcategories", "tags", "search", "get"],
                        "description": "Operation: 'browse' (list all), 'categories' (list categories), 'subcategories' (list subcats), 'tags' (list tags), 'search' (find patterns), 'get' (retrieve pattern)",
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query (for action='search') - matches name, category, subcategory, or tags",
                    },
                    "category": {
                        "type": "string",
                        "description": "Category name (for action='search' or action='subcategories'): vegetation, features, paths, details",
                    },
                    "subcategory": {
                        "type": "string",
                        "description": "Filter by subcategory (for action='search'): trees, bushes, rocks, ponds, etc.",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by tags (for action='search'): oak, small, medium, large, natural, etc.",
                    },
                    "pattern_id": {
                        "type": "string",
                        "description": "Pattern ID to retrieve (for action='get')",
                    },
                },
                "required": ["action"],
            },
        ),
        Tool(
            name="workflow_status",
            description="""Show the current build workflow phase, completed checkpoints, and pending validations.

Use this to understand which specialist phase is active and what validations are still required before advancing.
""",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="building_template",
            description="""Search and use parametric building templates for rapid, high-quality construction.

Building templates are reusable,  parametric designs for common structures (towers, houses, barns, etc.) that can be customized with user preferences.

**Available Templates** (5 templates):
1. **medieval_round_tower** (intermediate) - Circular stone tower with spiral stairs, arrow slits, crenellations
2. **simple_cottage** (beginner) - Cozy rectangular cottage with gabled roof, chimney
3. **guard_tower** (beginner) - Square defensive tower with observation platform
4. **wizard_tower** (intermediate) - Mystical tower with purple accents, glowing lights, cone roof
5. **simple_barn** (beginner) - Rustic wooden barn with large doors and hayloft

**Actions**:
- **list** - List all available templates with brief descriptions
- **search** - Find templates by category, difficulty, or style tags
- **get** - Retrieve full template with parameters and build instructions
- **customize** - Show customization options for a template

**Template Benefits**:
- ⚡ 10x faster than building from scratch
- ✅ Consistent, professional quality
- 🎨 Fully customizable (height, size, materials, style)
- 📐 Pre-calculated dimensions and proportions
- 🏗️ Step-by-step build sequence

**Usage Workflow**:
1. Search or list templates: `building_template(action="list")` or `building_template(action="search", category="towers")`
2. Get template details: `building_template(action="get", template_id="medieval_round_tower")`
3. Customize parameters (height, radius, materials, etc.) based on user preferences
4. Follow build_sequence to construct using WorldEdit commands
5. Each component provides specific commands with parameter substitution

**Example**:
building_template(action="get", template_id="simple_cottage")
→ Returns cottage template with parameters: width (7-15, default 9), depth (7-15, default 11), materials, etc.
→ User: "Make it 11×13 with stone walls"
→ Agent customizes: width=11, depth=13, wall_material="cobblestone"
→ Agent follows build_sequence: foundation → walls → floor → door → windows → roof → chimney
→ Result: Custom cottage in ~60 seconds

**Customization**:
Templates support parameters like:
- Dimensions: height, width, depth, radius (integer ranges with min/max)
- Materials: wall_material, roof_material, floor_material (enum with options)
- Features: has_windows, has_chimney, roof_style (boolean or enum)
- Complexity: num_floors, size (affects build scope)

**Categories**: towers, houses, agricultural, defensive, decorative, industrial, fantasy, religious
**Difficulty Levels**: beginner, intermediate, advanced
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["list", "search", "get", "customize"],
                        "description": "Action to perform"
                    },
                    "template_id": {
                        "type": "string",
                        "description": "Template identifier (required for get and customize actions)"
                    },
                    "category": {
                        "type": "string",
                        "description": "Filter by category (for search action)"
                    },
                    "difficulty": {
                        "type": "string",
                        "enum": ["beginner", "intermediate", "advanced"],
                        "description": "Filter by difficulty (for search action)"
                    },
                    "style_tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by style tags (for search action)"
                    }
                },
                "required": ["action"]
            },
        ),
        Tool(
            name="workflow_advance",
            description="""Advance to the next build phase once all required validations are complete.

The coordinator will refuse to advance if mandatory validations have not been recorded (e.g., structure_validation, lighting_analysis, symmetry_check).
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "force": {
                        "type": "boolean",
                        "description": "Reserved for future use; currently ignored",
                        "default": False
                    }
                },
                "required": []
            },
        ),
        Tool(
            name="workflow_reset",
            description="""Reset the build workflow back to the planning phase.

All recorded validations will be cleared. Use with caution (primarily for starting a new project).
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "confirm": {
                        "type": "boolean",
                        "description": "Must be true to confirm reset",
                        "default": False
                    }
                },
                "required": []
            },
        ),
        Tool(
            name="worldedit_deform",
            description="""Apply mathematical deformations to terrain in WorldEdit.

**⚠️ POWERFUL COMMAND - Use with caution!**

The //deform command uses mathematical expressions to deform terrain in the current selection.
Variables available: x, y, z (current coordinates), and you reassign them to move blocks.

**Common Deformations**:

**Sine wave terrain**:
```
//deform y-=0.2*sin(x*5)
```
Creates wavy terrain with amplitude 0.2 and frequency 5.

**Radial stretch**:
```
//deform x*=1.5;z*=1.5
```
Stretches selection outward from center.

**Twist effect**:
```
//deform x-=0.3*sin(y*5);z-=0.3*cos(y*5)
```
Twists terrain vertically.

**Sphere/dome**:
```
//deform y+=sqrt(64-(x^2+z^2))
```
Creates domed/spherical deformation.

**Safety Notes**:
- Always test on small selections first
- Use //undo if result is unexpected
- Expressions execute per-block (expensive on large areas)
- Check coordinates carefully (x, y, z syntax)

**Examples**:
- deform: {"expression": "y-=0.2*sin(x*5)"} - Wavy terrain
- deform: {"expression": "x*=1.2;z*=1.2"} - Radial expansion
- deform: {"expression": "y+=0.5*cos(x)*sin(z)"} - Organic bumps
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression for deformation (e.g., 'y-=0.2*sin(x*5)')",
                    },
                },
                "required": ["expression"],
            },
        ),
        Tool(
            name="worldedit_vegetation",
            description="""Generate vegetation (flora, forests, trees) in WorldEdit.

Add natural vegetation to terrain quickly with density control.

**Commands**:

**//flora [density]** - Generate flora in selection
- Density: 0-100 (default 10)
- Places grass, flowers, mushrooms, dead bushes based on biome
- Respects existing terrain (only places on valid blocks)
- Example: flora(density=20) for moderate vegetation

**//forest [type] [density]** - Generate forest in selection
- Types: oak, birch, spruce, jungle, acacia, dark_oak, random
- Density: 0-100 (default 5)
- Automatically spaces trees naturally
- Respects terrain height
- Example: forest(type="oak", density=10) for oak forest

**/tool tree [type]** - Tree placer tool
- Bind to held item: right-click to place trees
- Types: oak, birch, spruce, jungle, acacia, dark_oak, random
- Size: small, medium, large (varies by tree type)
- Example: tool_tree(type="oak", size="medium")

**Best Practices**:
- Start with low density (5-10) and increase if needed
- Use //flora for undergrowth, //forest for trees
- Combine both for realistic forests
- Use selection to limit vegetation to specific areas

**Examples**:
- flora: {"density": 15} - Moderate flora coverage
- forest: {"type": "oak", "density": 7} - Oak forest
- forest: {"type": "random", "density": 10} - Mixed forest
- tool_tree: {"type": "spruce", "size": "large"} - Large spruce placer
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "enum": ["flora", "forest", "tool_tree"],
                        "description": "Vegetation command to execute",
                    },
                    "type": {
                        "type": "string",
                        "description": "Tree type (for forest/tool_tree): oak, birch, spruce, jungle, acacia, dark_oak, random",
                    },
                    "density": {
                        "type": "integer",
                        "description": "Density 0-100 (flora default 10, forest default 5)",
                        "minimum": 0,
                        "maximum": 100,
                    },
                    "size": {
                        "type": "string",
                        "enum": ["small", "medium", "large"],
                        "description": "Tree size (for tool_tree, default medium)",
                    },
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_terrain_advanced",
            description="""Advanced terrain generation (caves, ore, regeneration) in WorldEdit.

Generate natural terrain features or restore original terrain.

**Commands**:

**//caves [size] [freq] [rarity] [minY] [maxY]** - Generate cave systems
- Size: 1-100 (default 8) - Cave tunnel size
- Frequency: 1-100 (default 40) - How many cave branches
- Rarity: 1-100 (default 7) - How common caves are (higher = rarer)
- minY/maxY: Y-level range (default: minY=1, maxY=128)
- Creates natural cave networks with varying sizes
- Example: caves(size=10, freq=50, rarity=5) for extensive caves

**//ore <pattern> <size> <freq> <rarity> <minY> <maxY>** - Generate ore veins
- Pattern: Block type (e.g., "iron_ore", "diamond_ore")
- Size: Vein size 1-50 (default 8)
- Frequency: Attempts per chunk 1-100 (default 10)
- Rarity: 1-100 (default 100, lower = rarer)
- minY/maxY: Y-level range
- Example: ore(pattern="iron_ore", size=8, freq=20, rarity=50, minY=0, maxY=64)

**//regen** - Regenerate selection to original terrain
- Restores terrain to world seed generation
- Removes all player-made modifications
- Uses chunk-based regeneration
- ⚠️ DESTRUCTIVE - Cannot undo, backs up automatically
- Example: regen() to restore natural terrain

**Safety Notes**:
- Cave generation is expensive (limit selection size)
- Ore generation follows vanilla patterns
- //regen is irreversible (creates backup first)
- Test on small areas before large operations

**Examples**:
- caves: {"size": 8, "freq": 40, "rarity": 7} - Natural caves
- ore: {"pattern": "diamond_ore", "size": 5, "freq": 2, "rarity": 100, "minY": 0, "maxY": 16} - Diamond veins
- regen: {} - Regenerate to original terrain
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "enum": ["caves", "ore", "regen"],
                        "description": "Terrain generation command",
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Block pattern (for ore command, e.g., 'iron_ore')",
                    },
                    "size": {
                        "type": "integer",
                        "description": "Size parameter (caves: tunnel size, ore: vein size)",
                    },
                    "freq": {
                        "type": "integer",
                        "description": "Frequency parameter (how many/often)",
                        "minimum": 1,
                        "maximum": 100,
                    },
                    "rarity": {
                        "type": "integer",
                        "description": "Rarity parameter (higher = rarer)",
                        "minimum": 1,
                        "maximum": 100,
                    },
                    "minY": {
                        "type": "integer",
                        "description": "Minimum Y level",
                    },
                    "maxY": {
                        "type": "integer",
                        "description": "Maximum Y level",
                    },
                },
                "required": ["command"],
            },
        ),
        Tool(
            name="worldedit_analysis",
            description="""Analyze selections and perform calculations in WorldEdit.

Get information about selections or evaluate mathematical expressions.

**Commands**:

**//distr** - Block distribution in selection
- Shows count of each block type in current selection
- Displays percentages for each block
- Useful for analyzing terrain composition
- Helps plan material requirements
- Example: distr() to see what blocks are in selection

**//calc <expression>** - Mathematical calculator
- Evaluates math expressions
- Supports: +, -, *, /, ^, sqrt, sin, cos, tan, abs, floor, ceil
- Variables: pi, e
- Useful for coordinate calculations, scaling, planning
- Examples:
  - calc("100 * 1.5") = 150 (scale coordinates)
  - calc("sqrt(100^2 + 100^2)") = 141.42 (diagonal distance)
  - calc("64 / 8") = 8 (chunk calculations)
  - calc("pi * 10^2") = 314.16 (circle area)

**Use Cases**:
- Analyze block composition before modifications
- Calculate distances and dimensions
- Plan material requirements
- Verify selection contents
- Math for complex builds

**Examples**:
- distr: {} - Show block distribution in selection
- calc: {"expression": "150 * 2.5"} - Calculate scaled dimension
- calc: {"expression": "sqrt(50^2 + 50^2)"} - Diagonal distance
- calc: {"expression": "pi * 20"} - Circumference of radius 20
""",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "enum": ["distr", "calc"],
                        "description": "Analysis command to execute",
                    },
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression (for calc command)",
                    },
                },
                "required": ["command"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """Handle tool calls from AI"""

    try:
        # TIER 1: Generic RCON Command
        if name == "rcon_command":
            command = arguments.get("command", "").strip()

            # Validate command
            if config.enable_safety_checks:
                validation = sanitize_command(
                    command,
                    allow_dangerous=config.allow_dangerous_commands,
                    max_length=config.max_command_length,
                )

                if not validation.is_valid:
                    return [
                        TextContent(
                            type="text", text=f"❌ Command validation failed: {validation.error_message}"
                        )
                    ]

                command = validation.sanitized_command

                # Check coordinate bounds if configured
                bounds_validation = validate_coordinates_in_bounds(
                    command,
                    config.build_min_x,
                    config.build_max_x,
                    config.build_min_y,
                    config.build_max_y,
                    config.build_min_z,
                    config.build_max_z,
                )

                if not bounds_validation.is_valid:
                    return [
                        TextContent(
                            type="text",
                            text=f"❌ Coordinate validation failed: {bounds_validation.error_message}",
                        )
                    ]

            # Check for player context warning
            warning = check_player_context_warning(command)

            # Execute command
            try:
                response = rcon.execute_command(command)
                result = f"✅ Command executed: {command}\n\nResponse: {response}"

                if warning:
                    result = f"⚠️ {warning}\n\n{result}"

                return [TextContent(type="text", text=result)]

            except Exception as e:
                return [TextContent(type="text", text=f"❌ Error executing command: {str(e)}")]

        # TIER 2: Categorized WorldEdit Commands
        elif name in WORLD_EDIT_TOOL_PREFIXES:
            command = arguments.get("command", "").strip()

            if not command:
                return [TextContent(type="text", text="❌ Command cannot be empty")]

            command = prepare_worldedit_command(name, command)

            # Use the generic rcon_command handler
            return await call_tool("rcon_command", {"command": command})

        # TIER 3: Helper Utilities
        elif name == "validate_pattern":
            pattern = arguments.get("pattern", "").strip()

            if not pattern:
                return [TextContent(type="text", text="❌ Pattern cannot be empty")]

            # Basic pattern validation
            analysis = ["Pattern Analysis:", ""]

            # Check for percentages (random pattern)
            if "%" in pattern:
                analysis.append("✓ Random weighted pattern detected")
                parts = pattern.split(",")
                total_weight = 0
                for part in parts:
                    if "%" in part:
                        weight = part.split("%")[0]
                        try:
                            total_weight += int(weight)
                        except ValueError:
                            pass
                if total_weight > 0:
                    analysis.append(f"  Total weight: {total_weight}%")

            # Check for special patterns
            if pattern.startswith("#"):
                analysis.append("✓ Special pattern detected")
                if pattern == "#clipboard":
                    analysis.append("  Uses clipboard contents")
                elif pattern.startswith("##"):
                    analysis.append(f"  Block category: {pattern[2:]}")

            # Check for block states
            if "[" in pattern and "]" in pattern:
                analysis.append("✓ Block states detected")

            # Check for asterisk (random state)
            if pattern.startswith("*"):
                analysis.append("✓ Random block state pattern")

            if len(analysis) == 2:  # Only header and empty line
                analysis.append("✓ Simple block pattern")

            analysis.append("")
            analysis.append("Pattern appears valid. Use it in commands like:")
            analysis.append(f"  //set {pattern}")
            analysis.append(f"  //replace stone {pattern}")

            return [TextContent(type="text", text="\n".join(analysis))]

        elif name == "validate_mask":
            mask = arguments.get("mask", "").strip()

            if not mask:
                return [TextContent(type="text", text="❌ Mask cannot be empty")]

            analysis = ["Mask Analysis:", ""]

            # Check for special masks
            if mask.startswith("#"):
                analysis.append("✓ Special mask detected")
                if mask == "#existing":
                    analysis.append("  Matches all non-air blocks")
                elif mask == "#solid":
                    analysis.append("  Matches solid blocks")
                elif mask.startswith("##"):
                    analysis.append(f"  Block category: {mask[2:]}")

            # Check for negation
            if mask.startswith("!"):
                analysis.append("✓ Negation mask (inverted)")

            # Check for percentage
            if mask.startswith("%"):
                try:
                    pct = int(mask[1:])
                    analysis.append(f"✓ Random mask: {pct}% chance")
                except ValueError:
                    pass

            # Check for expression
            if mask.startswith("="):
                analysis.append("✓ Expression mask detected")
                analysis.append("  Mathematical expression will be evaluated")

            # Check for offset masks
            if mask.startswith(">") or mask.startswith("<"):
                analysis.append("✓ Offset mask detected")
                if mask.startswith(">"):
                    analysis.append("  Matches blocks above the specified type")
                else:
                    analysis.append("  Matches blocks below the specified type")

            if len(analysis) == 2:
                analysis.append("✓ Simple block mask")

            analysis.append("")
            analysis.append("Mask appears valid. Use it in commands like:")
            analysis.append(f"  //replace {mask} stone")
            analysis.append(f"  //set stone -m {mask}")

            return [TextContent(type="text", text="\n".join(analysis))]

        elif name == "get_server_info":
            info = rcon.get_server_info()

            # Try to detect WorldEdit version if enabled
            worldedit_version = "Unknown"
            if config.enable_version_detection:
                detected = rcon.detect_worldedit_version()
                if detected:
                    worldedit_version = detected

            result = [
                "🖥️ Server Information:",
                "",
                f"Players: {info.get('players', 'Unknown')}",
                f"Time: {info.get('time', 'Unknown')}",
                f"Difficulty: {info.get('difficulty', 'Unknown')}",
                f"WorldEdit Version: {worldedit_version}",
                "",
                f"RCON Host: {config.rcon_host}:{config.rcon_port}",
                f"Safety Checks: {'Enabled' if config.enable_safety_checks else 'Disabled'}",
            ]

            return [TextContent(type="text", text="\n".join(result))]

        elif name == "calculate_region_size":
            x1, y1, z1 = arguments["x1"], arguments["y1"], arguments["z1"]
            x2, y2, z2 = arguments["x2"], arguments["y2"], arguments["z2"]

            # Calculate dimensions
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            depth = abs(z2 - z1) + 1

            # Calculate block count
            block_count = width * height * depth

            # Estimate operation time (very rough)
            # Assume ~100k blocks/second for simple operations
            estimated_seconds = block_count / 100000
            if estimated_seconds < 0.1:
                time_estimate = "< 0.1 seconds"
            elif estimated_seconds < 60:
                time_estimate = f"~{estimated_seconds:.1f} seconds"
            else:
                time_estimate = f"~{estimated_seconds/60:.1f} minutes"

            result = [
                "📐 Region Size Calculation:",
                "",
                f"Corner 1: ({x1}, {y1}, {z1})",
                f"Corner 2: ({x2}, {y2}, {z2})",
                "",
                f"Dimensions:",
                f"  Width (X): {width} blocks",
                f"  Height (Y): {height} blocks",
                f"  Depth (Z): {depth} blocks",
                "",
                f"Total Blocks: {block_count:,}",
                f"Estimated Time: {time_estimate}",
                "",
            ]

            # Warnings for large operations
            if block_count > 1000000:
                result.append("⚠️ WARNING: Very large region! Operation may take significant time.")
                result.append("   Consider breaking into smaller operations.")
            elif block_count > 100000:
                result.append("⚠️ Note: Large region. Operation may take some time.")

            return [TextContent(type="text", text="\n".join(result))]

        elif name == "search_minecraft_item":
            query = arguments.get("query", "").strip().lower()
            limit = arguments.get("limit", 20)

            if not query:
                return [TextContent(type="text", text="❌ Search query cannot be empty")]

            # Limit bounds checking
            if limit < 1:
                limit = 1
            elif limit > 50:
                limit = 50

            # Search through minecraft items
            matches = []
            for item in minecraft_items:
                # Case-insensitive partial match on name or displayName
                if query in item.get("name", "").lower() or query in item.get("displayName", "").lower():
                    matches.append(item)

                if len(matches) >= limit:
                    break

            if not matches:
                return [TextContent(type="text", text=f"❌ No items found matching '{query}'\n\nTry a different search term or check spelling.")]

            # Format results
            result = [
                f"🔍 Found {len(matches)} item(s) matching '{query}':",
                "",
            ]

            for item in matches:
                result.append(f"• **{item['displayName']}** (`{item['name']}`)")
                result.append(f"  - ID: {item['id']}")

                # Add usage hints for common blocks
                name = item['name']
                if "concrete" in name:
                    result.append("  - Use: Modern builds, clean aesthetic")
                elif "stone_bricks" in name or "stone_brick" in name:
                    result.append("  - Use: Medieval, refined builds")
                elif "cobblestone" in name:
                    result.append("  - Use: Medieval, rustic, foundations")
                elif "planks" in name or "plank" in name:
                    result.append("  - Use: Warm interiors, traditional builds")
                elif "glass" in name:
                    result.append("  - Use: Windows, modern walls, transparency")
                elif "terracotta" in name:
                    result.append("  - Use: Colorful accents, southwestern style")
                elif "wool" in name:
                    result.append("  - Use: Colorful builds, soft textures")

                result.append("")

            if len(minecraft_items) > limit:
                result.append(f"💡 Showing first {limit} results. Use limit parameter for more.")

            return [TextContent(type="text", text="\n".join(result))]

        elif name == "get_player_position":
            player_name = arguments.get("player_name", "").strip()

            # If no player specified, get first online player
            if not player_name:
                info = rcon.get_server_info()
                players = info.get('players', '')
                if not players or players == "0":
                    return [TextContent(type="text", text="❌ No players online. Please specify a player name or have someone join the server.")]

                # Try to extract first player name from the players string
                if ":" in players:
                    player_name = players.split(":", 1)[1].strip().split(",")[0].strip()
                else:
                    list_result = rcon.send_command("list")
                    if ":" in list_result:
                        player_list = list_result.split(":", 1)[1].strip()
                        if player_list:
                            player_name = player_list.split(",")[0].strip()

                if not player_name:
                    return [TextContent(type="text", text="❌ Could not determine player name. Please specify player_name parameter.")]

            try:
                # Get player position
                pos_result = rcon.send_command(f"data get entity {player_name} Pos")
                coord_match = re.search(r'\[([-\d.]+)d?,\s*([-\d.]+)d?,\s*([-\d.]+)d?\]', pos_result)

                if not coord_match:
                    return [TextContent(type="text", text=f"❌ Player '{player_name}' not found or error getting position")]

                x = float(coord_match.group(1))
                y = float(coord_match.group(2))
                z = float(coord_match.group(3))

                # Get player rotation (yaw, pitch)
                rot_result = rcon.send_command(f"data get entity {player_name} Rotation")
                rot_match = re.search(r'\[([-\d.]+)f?,\s*([-\d.]+)f?\]', rot_result)

                yaw = 0.0
                pitch = 0.0
                direction = "unknown"

                if rot_match:
                    yaw = float(rot_match.group(1))
                    pitch = float(rot_match.group(2))

                    # Convert yaw to cardinal direction
                    # Yaw: -180 to 180, where 0=south, 90=west, -90=east, 180/-180=north
                    yaw_normalized = yaw % 360
                    if 315 <= yaw_normalized or yaw_normalized < 45:
                        direction = "South (+Z)"
                    elif 45 <= yaw_normalized < 135:
                        direction = "West (-X)"
                    elif 135 <= yaw_normalized < 225:
                        direction = "North (-Z)"
                    else:
                        direction = "East (+X)"

                # Attempt to find target block using raycast
                # Execute at player, position relative to look direction
                target_info = "Not detected (no block in range)"

                # Calculate look vector from pitch and yaw
                # Raycast up to 5 blocks
                yaw_rad = math.radians(yaw)
                pitch_rad = math.radians(pitch)

                # Try execute raycast - position 1-5 blocks in look direction
                for distance in [1, 2, 3, 4, 5]:
                    # Calculate offset using look direction
                    dx = -math.sin(yaw_rad) * math.cos(pitch_rad) * distance
                    dz = math.cos(yaw_rad) * math.cos(pitch_rad) * distance
                    dy = -math.sin(pitch_rad) * distance

                    target_x = int(x + dx)
                    target_y = int(y + 1.62 + dy)  # Eye level
                    target_z = int(z + dz)

                    # Check if there's a non-air block at this position
                    block_check = rcon.send_command(f"execute positioned {target_x} {target_y} {target_z} run data get block ~ ~ ~ id")

                    if "air" not in block_check.lower() and "has the following" in block_check:
                        # Found a non-air block
                        block_match = re.search(r'"minecraft:([^"]+)"', block_check)
                        if block_match:
                            block_type = block_match.group(1)
                            target_info = f"{block_type} at {target_x},{target_y},{target_z} ({distance} blocks away)"
                            break

                # Use player Y position as ground reference (simpler and more reliable)
                # Player is always standing on solid ground, so their feet Y IS the ground level
                player_y = int(y)

                # Check block directly below player's feet to identify surface type
                surface_block = "unknown"
                block_check = rcon.send_command(f"execute positioned {int(x)} {player_y - 1} {int(z)} run data get block ~ ~ ~ id")
                if "has the following" in block_check:
                    block_match = re.search(r'"minecraft:([^"]+)"', block_check)
                    if block_match:
                        surface_block = block_match.group(1)

                # Build surface info section
                surface_info = f"""**Ground Level (Player-based):**
Player feet at: Y={player_y}
Block below feet: {surface_block}
Ground level: Y={player_y - 1}"""

                # Build suggestions section - simplified, using player Y as reference
                suggestions = f"""**Building Coordinates:**
- On ground (RECOMMENDED): {int(x)},{player_y},{int(z)} - builds at player's feet level
- Foundation layer: {int(x)},{player_y - 1},{int(z)} - replaces block below player
- Elevated (1 block up): {int(x)},{player_y + 1},{int(z)} - builds above player
- Where player is looking: Use target block if available"""

                return [TextContent(type="text", text=f"""📍 Comprehensive Player Context: {player_name}

**Position:**
X: {x:.2f} → {int(x)}
Y: {y:.2f} → {int(y)}
Z: {z:.2f} → {int(z)}

**Rotation:**
Yaw: {yaw:.1f}°
Pitch: {pitch:.1f}°
Facing: {direction}

**Looking At:**
{target_info}

{surface_info}

{suggestions}

**Orientation Note:**
Player facing {direction} - structure front should face this direction for alignment
""")]

            except Exception as e:
                logger.error(f"Error in get_player_position: {str(e)}", exc_info=True)
                return [TextContent(type="text", text=f"❌ Error getting player position: {str(e)}")]

        elif name == "get_surface_level":
            x = arguments["x"]
            z = arguments["z"]

            try:
                # SIMPLIFIED SURFACE DETECTION
                # Uses player Y position as baseline reference for ground level
                # This avoids complex raycasting that often fails

                logger.info(f"Detecting surface level at X={x}, Z={z}")

                # Get player position as baseline reference
                player_y_baseline = 64  # Default fallback (typical overworld surface)

                try:
                    info = rcon.get_server_info()
                    players_str = info.get('players', '')

                    if players_str and ":" in players_str:
                        player_list = players_str.split(":")[1].strip().split(",")
                        if player_list:
                            player_name = player_list[0].strip()
                            player_data = rcon.send_command(f"data get entity {player_name} Pos")

                            if "has the following entity data" in player_data:
                                pos_match = re.search(r'\[([+-]?\d+\.?\d*)d,\s*([+-]?\d+\.?\d*)d,\s*([+-]?\d+\.?\d*)d\]', player_data)
                                if pos_match:
                                    player_y_baseline = int(float(pos_match.group(2)))
                                    logger.info(f"Using player Y position {player_y_baseline} as baseline reference")
                except Exception as e:
                    logger.warning(f"Could not get player position, using default Y=64: {e}")

                # Use player Y as the ground level for the target coordinates
                # This assumes terrain doesn't vary drastically across the world
                surface_y = player_y_baseline - 1  # Ground is typically 1 block below player feet

                # Check what block is at that level
                surface_block = "unknown"
                block_check = rcon.send_command(f"execute positioned {x} {surface_y} {z} run data get block ~ ~ ~ id")
                if "has the following" in block_check:
                    block_match = re.search(r'"minecraft:([^"]+)"', block_check)
                    if block_match:
                        surface_block = block_match.group(1)

                logger.info(f"Surface at ({x}, {z}): Y={surface_y}, block={surface_block}")

                return [TextContent(type="text", text=f"""🏔️ Surface Detection at X={x}, Z={z}

**Surface Level:** Y={surface_y}
**Block Type:** {surface_block}
**Detection Method:** Player Y baseline ({player_y_baseline})

**Building Coordinates:**
- On surface (RECOMMENDED): {x},{surface_y + 1},{z} - builds on top of ground
- Foundation level: {x},{surface_y},{z} - replaces surface block
- Elevated: {x},{surface_y + 2},{z} - builds 1 block above surface

**Note:** This uses player's current Y position as reference for ground level.
For best results, be near your build location before checking surface.
If terrain varies significantly, use `get_player_position` while standing at the exact build site.
""")]

            except Exception as e:
                logger.error(f"Error in get_surface_level: {str(e)}", exc_info=True)
                return [TextContent(type="text", text=f"❌ Error finding surface level: {str(e)}")]

        elif name == "furniture_lookup":
            action = arguments.get("action")

            if not action:
                return [TextContent(type="text", text="❌ Error: 'action' parameter is required (must be 'search' or 'get')")]

            layouts = load_furniture_layouts()
            catalog = load_furniture_catalog()

            if not layouts and not catalog:
                return [TextContent(type="text", text="❌ Error: No furniture data available (both layouts and catalog missing)")]

            # Create lookup index: map IDs to layouts
            layout_index = {layout['id']: layout for layout in layouts}

            # Filter catalog to only actual furniture (not category headings)
            furniture_items = [item for item in catalog if item.get('heading_level', 2) >= 3]

            if action == "search":
                # Search for furniture by query, category, or tags
                query = arguments.get("query", "").lower()
                category_filter = arguments.get("category", "").lower()
                tags_filter = arguments.get("tags", [])
                tags_filter = [tag.lower() for tag in tags_filter] if tags_filter else []

                results = []
                seen_ids = set()

                # First, search through layouts (these have precise coordinates)
                for layout in layouts:
                    # Check if matches search criteria
                    matches = True

                    if query:
                        # Search in name, category, subcategory, and tags
                        name_match = query in layout.get("name", "").lower()
                        id_match = query in layout.get("id", "").lower()
                        cat_match = query in layout.get("category", "").lower()
                        subcat_match = query in layout.get("subcategory", "").lower()
                        tags_match = any(query in tag.lower() for tag in layout.get("tags", []))

                        matches = matches and (name_match or id_match or cat_match or subcat_match or tags_match)

                    if category_filter:
                        matches = matches and (category_filter in layout.get("category", "").lower())

                    if tags_filter:
                        layout_tags = [tag.lower() for tag in layout.get("tags", [])]
                        # Check if ALL filter tags are present
                        matches = matches and all(tag in layout_tags for tag in tags_filter)

                    if matches:
                        seen_ids.add(layout.get("id"))
                        # Add to results (summary only, not full layout)
                        results.append({
                            "name": layout.get("name"),
                            "id": layout.get("id"),
                            "category": layout.get("category"),
                            "subcategory": layout.get("subcategory"),
                            "tags": layout.get("tags", []),
                            "bounds": layout.get("bounds"),
                            "materials_count": sum(layout.get("materials", {}).values()),
                            "notes": layout.get("notes", "")[:100] + "..." if len(layout.get("notes", "")) > 100 else layout.get("notes", ""),
                            "has_layout": True,
                            "source": "layout"
                        })

                # Then, search through catalog items (text-based instructions)
                for item in furniture_items:
                    # Skip if already in layouts
                    if item.get("id") in seen_ids:
                        continue

                    matches = True

                    if query:
                        # Search in name and category
                        name_match = query in item.get("name", "").lower()
                        id_match = query in item.get("id", "").lower()
                        cat_match = query in item.get("category", "").lower()

                        matches = matches and (name_match or id_match or cat_match)

                    if category_filter:
                        matches = matches and (category_filter in item.get("category", "").lower())

                    # Catalog items don't have tags, so skip tag filtering for them

                    if matches:
                        # Extract first sentence from content_blocks
                        description = ""
                        for block in item.get("content_blocks", []):
                            if block.get("type") == "paragraph":
                                text = block.get("text", "")
                                description = text[:100] + "..." if len(text) > 100 else text
                                break

                        results.append({
                            "name": item.get("name"),
                            "id": item.get("id"),
                            "category": item.get("category"),
                            "subcategory": item.get("subcategory"),
                            "tags": [],
                            "bounds": None,
                            "materials_count": 0,
                            "notes": description,
                            "has_layout": False,
                            "source": "catalog"
                        })

                if not results:
                    search_params = []
                    if query:
                        search_params.append(f"query='{query}'")
                    if category_filter:
                        search_params.append(f"category='{category_filter}'")
                    if tags_filter:
                        search_params.append(f"tags={tags_filter}")

                    return [TextContent(type="text", text=f"🔍 No furniture found matching: {', '.join(search_params)}\n\nTry:\n- Broader search terms\n- Different category (bedroom, kitchen, living_room, etc.)\n- Fewer tag filters")]

                # Format results
                layout_count = sum(1 for r in results if r['has_layout'])
                catalog_count = sum(1 for r in results if not r['has_layout'])

                result_text = f"🪑 Found {len(results)} furniture item(s):\n"
                result_text += f"   - {layout_count} with automated layouts\n"
                result_text += f"   - {catalog_count} with manual instructions only\n\n"

                for i, item in enumerate(results, 1):
                    # Indicate if has layout or catalog only
                    status_icon = "✅" if item['has_layout'] else "📝"

                    result_text += f"{i}. {status_icon} **{item['name']}** (ID: `{item['id']}`)\n"
                    result_text += f"   - Category: {item['category']}"
                    if item.get('subcategory'):
                        result_text += f" > {item['subcategory']}"
                    result_text += "\n"

                    if item['has_layout']:
                        bounds = item['bounds']
                        result_text += f"   - Size: {bounds['width']}×{bounds['height']}×{bounds['depth']} blocks (W×H×D)\n"
                        result_text += f"   - Materials: {item['materials_count']} total blocks\n"
                        if item.get('tags'):
                            result_text += f"   - Tags: {', '.join(item['tags'])}\n"
                        result_text += f"   - ✅ Automated layout available\n"
                    else:
                        result_text += f"   - 📝 Manual instructions only (no automated layout yet)\n"

                    if item.get('notes'):
                        result_text += f"   - Notes: {item['notes']}\n"
                    result_text += "\n"

                result_text += f"\n💡 Legend:\n"
                result_text += f"   ✅ = Has automated layout (can be placed with furniture_placer)\n"
                result_text += f"   📝 = Manual instructions only (build by hand using catalog)\n\n"
                result_text += f"To get details, use: `furniture_lookup` with action='get' and furniture_id='<id>'"

                return [TextContent(type="text", text=result_text)]

            elif action == "get":
                # Get specific furniture layout or catalog item by ID
                furniture_id = arguments.get("furniture_id")

                if not furniture_id:
                    return [TextContent(type="text", text="❌ Error: 'furniture_id' parameter is required for action='get'")]

                # Try to find in layouts first
                layout = None
                for item in layouts:
                    if item.get("id") == furniture_id:
                        layout = item
                        break

                # If not in layouts, try catalog
                catalog_item = None
                if not layout:
                    for item in furniture_items:
                        if item.get("id") == furniture_id:
                            catalog_item = item
                            break

                if not layout and not catalog_item:
                    return [TextContent(type="text", text=f"❌ Furniture not found: '{furniture_id}'\n\nUse action='search' to find available furniture IDs.")]

                # If found in catalog but not layouts, return catalog info
                if catalog_item and not layout:
                    result_text = f"📝 **{catalog_item['name']}** (ID: `{catalog_item['id']}`)\n\n"
                    result_text += "**Status:** Manual instructions only (no automated layout yet)\n\n"

                    result_text += "**Category:** " + catalog_item['category']
                    if catalog_item.get('subcategory'):
                        result_text += f" > {catalog_item['subcategory']}"
                    result_text += "\n\n"

                    result_text += "**Build Instructions:**\n\n"

                    # Extract all content blocks
                    for block in catalog_item.get('content_blocks', []):
                        if block.get('type') == 'paragraph':
                            result_text += block.get('text', '') + "\n\n"
                        elif block.get('type') == 'list':
                            style = block.get('style', 'unordered')
                            prefix = '-' if style == 'unordered' else '1.'
                            for i, item_text in enumerate(block.get('items', []), 1):
                                if style == 'ordered':
                                    result_text += f"{i}. {item_text}\n"
                                else:
                                    result_text += f"- {item_text}\n"
                            result_text += "\n"
                        elif block.get('type') == 'table':
                            result_text += "\n**Table:**\n"
                            headers = block.get('headers', [])
                            if headers:
                                result_text += "| " + " | ".join(headers) + " |\n"
                                result_text += "| " + " | ".join(['---'] * len(headers)) + " |\n"
                            for row in block.get('rows', []):
                                result_text += "| " + " | ".join(row) + " |\n"
                            result_text += "\n"

                    result_text += "\n💡 This furniture currently only has manual build instructions.\n"
                    result_text += "To create an automated layout, define precise block coordinates in minecraft_furniture_layouts.json"

                    return [TextContent(type="text", text=result_text)]

                # Return full layout as formatted JSON
                result_text = f"🪑 **{layout['name']}** (ID: `{layout['id']}`)\n\n"

                # Basic info
                result_text += "**Category:** " + layout['category']
                if layout.get('subcategory'):
                    result_text += f" > {layout['subcategory']}"
                result_text += "\n\n"

                # Dimensions
                bounds = layout['bounds']
                result_text += f"**Dimensions:** {bounds['width']}×{bounds['height']}×{bounds['depth']} blocks (Width × Height × Depth)\n\n"

                # Origin
                origin = layout.get('origin', {})
                result_text += f"**Origin:** {origin.get('type', 'front_left_bottom')} (facing {origin.get('facing', 'north')})\n\n"

                # Materials
                materials = layout.get('materials', {})
                if materials:
                    result_text += "**Materials Required:**\n"
                    for block, count in materials.items():
                        result_text += f"  - {block}: {count}\n"
                    result_text += f"  Total: {sum(materials.values())} blocks\n\n"

                # Placements
                placements = layout.get('placements', [])
                result_text += f"**Placements:** ({len(placements)} operations)\n"
                for i, placement in enumerate(placements[:10], 1):  # Show first 10
                    ptype = placement.get('type')
                    if ptype == 'block':
                        pos = placement['pos']
                        block = placement['block']
                        state = placement.get('state', '')
                        result_text += f"  {i}. Block at ({pos['x']},{pos['y']},{pos['z']}): {block}{state}\n"
                    elif ptype == 'fill':
                        from_pos = placement['from']
                        to_pos = placement['to']
                        block = placement['block']
                        result_text += f"  {i}. Fill ({from_pos['x']},{from_pos['y']},{from_pos['z']}) to ({to_pos['x']},{to_pos['y']},{to_pos['z']}): {block}\n"
                    elif ptype == 'line':
                        from_pos = placement['from']
                        to_pos = placement['to']
                        block = placement['block']
                        result_text += f"  {i}. Line ({from_pos['x']},{from_pos['y']},{from_pos['z']}) to ({to_pos['x']},{to_pos['y']},{to_pos['z']}): {block}\n"
                    elif ptype == 'layer':
                        y = placement['y']
                        pattern = placement['pattern']
                        result_text += f"  {i}. Layer at Y={y}: {pattern}\n"

                if len(placements) > 10:
                    result_text += f"  ... and {len(placements) - 10} more placements\n"
                result_text += "\n"

                # Clearance
                clearance = layout.get('clearance')
                if clearance:
                    result_text += "**Clearance Required:**\n"
                    result_text += f"  - Front: {clearance.get('front', 0)} blocks\n"
                    result_text += f"  - Back: {clearance.get('back', 0)} blocks\n"
                    result_text += f"  - Left: {clearance.get('left', 0)} blocks\n"
                    result_text += f"  - Right: {clearance.get('right', 0)} blocks\n"
                    result_text += f"  - Top: {clearance.get('top', 0)} blocks\n\n"

                # Notes
                if layout.get('notes'):
                    result_text += f"**Notes:** {layout['notes']}\n\n"

                # Variants
                variants = layout.get('variants', [])
                if variants:
                    result_text += f"**Variants:** ({len(variants)} available)\n"
                    for variant in variants:
                        result_text += f"  - {variant['name']} (ID: `{variant['id']}`): {variant['changes']}\n"
                    result_text += "\n"

                # Tags
                if layout.get('tags'):
                    result_text += f"**Tags:** {', '.join(layout['tags'])}\n\n"

                # Full layout data as JSON
                result_text += "**Full Layout Data (JSON):**\n```json\n"
                result_text += json.dumps(layout, indent=2)
                result_text += "\n```\n\n"

                result_text += "💡 Use the placement helper tool to build this furniture at specific coordinates."

                return [TextContent(type="text", text=result_text)]

            else:
                return [TextContent(type="text", text=f"❌ Invalid action: '{action}'. Must be 'search' or 'get'.")]

        elif name == "place_furniture":
            furniture_id = arguments.get("furniture_id")
            origin_x = arguments.get("origin_x")
            origin_y = arguments.get("origin_y")
            origin_z = arguments.get("origin_z")
            facing = arguments.get("facing")
            place_on_surface = arguments.get("place_on_surface", True)
            preview_only = arguments.get("preview_only", False)

            missing = [field for field in ("furniture_id", "origin_x", "origin_y", "origin_z") if arguments.get(field) is None]
            if missing:
                return [TextContent(type="text", text=f"❌ Missing required field(s): {', '.join(missing)}")]

            if facing:
                facing = facing.lower()
                if facing not in FurniturePlacer.ROTATIONS:
                    valid = ", ".join(FurniturePlacer.ROTATIONS.keys())
                    return [TextContent(type="text", text=f"❌ Invalid facing '{facing}'. Valid options: {valid}")]

            layout = next((item for item in load_furniture_layouts() if item.get('id') == furniture_id), None)
            if not layout:
                return [TextContent(type="text", text=f"❌ Furniture layout '{furniture_id}' not found or does not have an automated blueprint.")]

            try:
                commands = FurniturePlacer.get_placement_commands(
                    layout=layout,
                    origin_x=int(origin_x),
                    origin_y=int(origin_y),
                    origin_z=int(origin_z),
                    facing=facing,
                    place_on_surface=place_on_surface,
                )
            except ValueError as exc:
                logger.error(f"Error generating placement commands: {exc}")
                return [TextContent(type="text", text=f"❌ Failed to generate commands: {exc}")]

            summary = FurniturePlacer.get_command_summary(commands)
            final_facing = facing or layout.get('origin', {}).get('facing', 'north')

            if preview_only:
                command_listing = '\n'.join(commands)
                preview_text = [
                    "🛋️ **Furniture Placement Preview**",
                    f"Layout: {layout.get('name')} (`{layout.get('id')}`)",
                    f"Origin: ({origin_x},{origin_y},{origin_z})",
                    f"Facing: {final_facing}",
                    "",
                    summary,
                    "Commands:",
                    "```plain",
                    command_listing,
                    "```",
                    "Set `preview_only` to false to execute these commands.",
                ]
                return [TextContent(type="text", text='\n'.join(preview_text))]

            executed_commands: List[str] = []
            try:
                for command in commands:
                    stripped = command.strip()
                    if not stripped or stripped.startswith('#'):
                        continue
                    executed_commands.append(stripped)
                    rcon.execute_command(stripped)
            except Exception as exc:
                logger.error(f"Furniture placement failed: {exc}", exc_info=True)
                failure_output = [
                    "❌ **Furniture placement failed**",
                    f"Layout: {layout.get('name')} (`{layout.get('id')}`)",
                    f"Origin: ({origin_x},{origin_y},{origin_z})",
                    f"Facing: {final_facing}",
                    "",
                    "Commands executed before failure:",
                ]
                for cmd in executed_commands[-10:]:
                    failure_output.append(f"- `{cmd}`")
                failure_output.extend([
                    "",
                    f"Error: {exc}",
                    "Use `//undo` to revert the changes if necessary.",
                ])
                return [TextContent(type="text", text='\n'.join(failure_output))]

            materials = layout.get('materials', {})
            clearance = layout.get('clearance', {})

            material_lines = []
            if materials:
                for block, count in sorted(materials.items(), key=lambda item: item[0])[:10]:
                    material_lines.append(f"- {block}: {count}")
                if len(materials) > 10:
                    material_lines.append(f"- … ({len(materials) - 10} more entries)")

            clearance_lines = []
            if clearance:
                for side, distance in clearance.items():
                    clearance_lines.append(f"- {side.title()}: {distance}")

            success_lines = [
                "✅ **Furniture placed successfully**",
                f"Layout: {layout.get('name')} (`{layout.get('id')}`)",
                f"Origin: ({origin_x},{origin_y},{origin_z})",
                f"Facing: {final_facing}",
                "",
                summary,
            ]

            if material_lines:
                success_lines.extend(["**Materials Used:**"] + material_lines + [""])

            if clearance_lines:
                success_lines.extend(["**Recommended Clearance:**"] + clearance_lines + [""])

            displayed_commands = executed_commands[:10]
            if displayed_commands:
                success_lines.append("**Executed Commands (first 10):**")
                for cmd in displayed_commands:
                    success_lines.append(f"- `{cmd}`")
                if len(executed_commands) > 10:
                    success_lines.append(f"- … ({len(executed_commands) - 10} more)")
                success_lines.append("")

            success_lines.append("Undo tip: run `//undo` if you need to revert this placement.")

            return [TextContent(type="text", text='\n'.join(success_lines))]

        elif name == "building_pattern_lookup":
            action = arguments.get("action")

            if not action:
                return [TextContent(type="text", text="❌ Error: 'action' parameter is required (must be 'search' or 'get')")]

            # Load building patterns
            patterns = _load_json_list(CONTEXT_DIR / 'building_patterns_complete.json')
            structured_patterns = {p.get('id'): p for p in load_structured_patterns() if p.get('id')}

            if not patterns:
                return [TextContent(type="text", text="❌ Error: No building pattern metadata available.")]

            # Discovery actions
            if action == "browse":
                # List all patterns (names and IDs only)
                result_text = f"🏗️ **Building Pattern Library** - {len(patterns)} patterns available\n\n"

                # Group by category
                by_category = {}
                for pattern in patterns:
                    cat = pattern.get("category", "unknown")
                    if cat not in by_category:
                        by_category[cat] = []
                    by_category[cat].append(pattern)

                for category, cat_patterns in sorted(by_category.items()):
                    result_text += f"**{category.upper()}** ({len(cat_patterns)} patterns):\n"
                    for pattern in sorted(cat_patterns, key=lambda p: p.get("id", "")):
                        structured_flag = " ✅" if pattern.get('id') in structured_patterns else ""
                        result_text += f"  - {pattern.get('name')} (ID: `{pattern.get('id')}`){structured_flag}\n"
                    result_text += "\n"

                result_text += "✅ indicates structured placement data is available.\n"
                result_text += "💡 Use action='get' with pattern_id to retrieve full construction details."

                return [TextContent(type="text", text=result_text)]

            elif action == "categories":
                # List all categories with counts
                category_counts = {}
                category_subcats = {}

                for pattern in patterns:
                    cat = pattern.get("category", "unknown")
                    subcat = pattern.get("subcategory", "")

                    category_counts[cat] = category_counts.get(cat, 0) + 1

                    if cat not in category_subcats:
                        category_subcats[cat] = set()
                    if subcat:
                        category_subcats[cat].add(subcat)

                result_text = "🏗️ **Building Pattern Categories**\n\n"

                for category in sorted(category_counts.keys()):
                    count = category_counts[category]
                    subcats = sorted(category_subcats.get(category, set()))

                    result_text += f"**{category}** ({count} patterns)\n"
                    if subcats:
                        result_text += f"  Subcategories: {', '.join(subcats)}\n"
                    result_text += "\n"

                result_text += "💡 Use action='subcategories' with category='<name>' to see patterns in that category.\n"
                result_text += "💡 Use action='search' with category='<name>' to find patterns."
                result_text += "\n✅ Structured patterns can be placed automatically with place_building_pattern."

                return [TextContent(type="text", text=result_text)]

            elif action == "subcategories":
                # List subcategories for a specific category
                category = arguments.get("category", "").lower()

                if not category:
                    return [TextContent(type="text", text="❌ Error: 'category' parameter required for action='subcategories'")]

                # Find patterns in this category
                cat_patterns = [p for p in patterns if p.get("category", "").lower() == category]

                if not cat_patterns:
                    return [TextContent(type="text", text=f"❌ No patterns found in category '{category}'. Use action='categories' to see available categories.")]

                # Group by subcategory
                by_subcat = {}
                for pattern in cat_patterns:
                    subcat = pattern.get("subcategory", "none")
                    if subcat not in by_subcat:
                        by_subcat[subcat] = []
                    by_subcat[subcat].append(pattern)

                result_text = f"🏗️ **{category.upper()} Category** - {len(cat_patterns)} patterns\n\n"

                for subcat, subcat_patterns in sorted(by_subcat.items()):
                    result_text += f"**{subcat}** ({len(subcat_patterns)} patterns):\n"
                    for pattern in sorted(subcat_patterns, key=lambda p: p.get("id", "")):
                        dims = pattern.get("dimensions", {})
                        size = f"{dims.get('width')}×{dims.get('height')}×{dims.get('depth')}"
                        result_text += f"  - {pattern.get('name')} (ID: `{pattern.get('id')}`) - {size}\n"
                    result_text += "\n"

                result_text += "💡 Use action='get' with pattern_id to retrieve full construction details."

                return [TextContent(type="text", text=result_text)]

            elif action == "tags":
                # List all tags with usage counts
                tag_counts = {}

                for pattern in patterns:
                    for tag in pattern.get("tags", []):
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1

                result_text = "🏗️ **Building Pattern Tags**\n\n"

                # Sort by count (most used first)
                sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)

                for tag, count in sorted_tags:
                    result_text += f"- **{tag}** ({count} patterns)\n"

                result_text += "\n💡 Use action='search' with tags=['<tag>'] to find patterns with specific tags."

                return [TextContent(type="text", text=result_text)]

            elif action == "search":
                # Search for patterns by query, category, subcategory, or tags
                query = arguments.get("query", "").lower()
                category_filter = arguments.get("category", "").lower()
                subcategory_filter = arguments.get("subcategory", "").lower()
                tags_filter = arguments.get("tags", [])
                tags_filter = [tag.lower() for tag in tags_filter] if tags_filter else []

                results = []

                for pattern in patterns:
                    # Check if matches search criteria
                    matches = True

                    if query:
                        # Search in name, id, category, subcategory, and tags
                        name_match = query in pattern.get("name", "").lower()
                        id_match = query in pattern.get("id", "").lower()
                        cat_match = query in pattern.get("category", "").lower()
                        subcat_match = query in pattern.get("subcategory", "").lower()
                        desc_match = query in pattern.get("description", "").lower()
                        tags_match = any(query in tag.lower() for tag in pattern.get("tags", []))

                        matches = matches and (name_match or id_match or cat_match or subcat_match or desc_match or tags_match)

                    if category_filter:
                        matches = matches and (category_filter in pattern.get("category", "").lower())

                    if subcategory_filter:
                        matches = matches and (subcategory_filter in pattern.get("subcategory", "").lower())

                    if tags_filter:
                        pattern_tags = [tag.lower() for tag in pattern.get("tags", [])]
                        # Check if ALL filter tags are present
                        matches = matches and all(tag in pattern_tags for tag in tags_filter)

                    if matches:
                        # Add to results (summary only, not full pattern)
                        dims = pattern.get("dimensions", {})
                        pattern_id = pattern.get("id")
                        results.append({
                            "name": pattern.get("name"),
                            "id": pattern_id,
                            "category": pattern.get("category"),
                            "subcategory": pattern.get("subcategory"),
                            "tags": pattern.get("tags", []),
                            "dimensions": f"{dims.get('width')}×{dims.get('height')}×{dims.get('depth')}",
                            "difficulty": pattern.get("difficulty", "medium"),
                            "materials_count": sum(pattern.get("materials", {}).values()),
                            "layer_count": len(pattern.get("layers", [])),
                            "description": pattern.get("description", "")[:150] + "..." if len(pattern.get("description", "")) > 150 else pattern.get("description", ""),
                            "has_structure": pattern_id in structured_patterns,
                        })

                if not results:
                    search_params = []
                    if query:
                        search_params.append(f"query='{query}'")
                    if category_filter:
                        search_params.append(f"category='{category_filter}'")
                    if subcategory_filter:
                        search_params.append(f"subcategory='{subcategory_filter}'")
                    if tags_filter:
                        search_params.append(f"tags={tags_filter}")

                    return [TextContent(type="text", text=f"🔍 No building patterns found matching: {', '.join(search_params)}\n\nTry:\n- Broader search terms\n- Different category (roofing, facades, corners, details)\n- Different subcategory (gable, hip, slab_roof, etc.)\n- Fewer tag filters")]

                # Format results
                result_text = f"🏗️ Found {len(results)} building pattern(s):\n\n"

                for i, item in enumerate(results, 1):
                    structured_flag = " ✅" if item.get('has_structure') else ""
                    result_text += f"{i}. **{item['name']}** (ID: `{item['id']}`){structured_flag}\n"
                    result_text += f"   - Category: {item['category']}"
                    if item.get('subcategory'):
                        result_text += f" > {item['subcategory']}"
                    result_text += "\n"
                    result_text += f"   - Size: {item['dimensions']} blocks (W×H×D)\n"
                    result_text += f"   - Materials: {item['materials_count']} total blocks\n"
                    result_text += f"   - Layers: {item['layer_count']} construction layers\n"
                    result_text += f"   - Difficulty: {item['difficulty']}\n"
                    if item.get('tags'):
                        result_text += f"   - Tags: {', '.join(item['tags'])}\n"
                    if item.get('description'):
                        result_text += f"   - Description: {item['description']}\n"
                    result_text += "\n"

                result_text += "✅ indicates automatic placement data is available.\n"
                result_text += f"💡 To get full construction instructions, use: building_pattern_lookup with action='get' and pattern_id='<id>'"
                result_text += "\n💡 Use place_building_pattern to instantiate structured patterns."

                return [TextContent(type="text", text=result_text)]

            elif action == "get":
                # Get specific pattern by ID
                pattern_id = arguments.get("pattern_id")

                if not pattern_id:
                    return [TextContent(type="text", text="❌ Error: 'pattern_id' parameter is required for action='get'")]

                # Find pattern
                pattern = None
                for item in patterns:
                    if item.get("id") == pattern_id:
                        pattern = item
                        break

                if not pattern:
                    return [TextContent(type="text", text=f"❌ Error: Pattern with ID '{pattern_id}' not found.\n\nUse action='search' to find available patterns.")]

                # Format full pattern details
                result_text = f"🏗️ **{pattern.get('name')}** (ID: `{pattern.get('id')}`)\n\n"

                # Basic info
                result_text += f"**Category:** {pattern.get('category')}"
                if pattern.get('subcategory'):
                    result_text += f" > {pattern.get('subcategory')}"
                result_text += "\n\n"

                result_text += f"**Description:** {pattern.get('description', 'No description available.')}\n\n"

                # Dimensions
                dims = pattern.get('dimensions', {})
                result_text += f"**Dimensions:**\n"
                result_text += f"  - Width: {dims.get('width')} blocks\n"
                result_text += f"  - Height: {dims.get('height')} blocks\n"
                result_text += f"  - Depth: {dims.get('depth')} blocks\n\n"

                # Difficulty
                result_text += f"**Difficulty:** {pattern.get('difficulty', 'medium')}\n\n"

                # Materials
                materials = pattern.get('materials', {})
                if materials:
                    result_text += f"**Materials Required:** ({sum(materials.values())} total blocks)\n"
                    for material, count in sorted(materials.items(), key=lambda x: x[1], reverse=True):
                        result_text += f"  - {material}: {count}\n"
                    result_text += "\n"

                # Construction method
                if pattern.get('construction_method'):
                    result_text += f"**Construction Method:** {pattern.get('construction_method')}\n\n"

                # Layer-by-layer instructions
                layers = pattern.get('layers', [])
                if layers:
                    result_text += f"**Layer-by-Layer Instructions:** ({len(layers)} layers)\n\n"
                    for layer in layers[:5]:  # Show first 5 layers in detail
                        result_text += f"**Layer {layer.get('layer')}** (Y-offset: {layer.get('y_offset')})\n"
                        if layer.get('description'):
                            result_text += f"  Description: {layer.get('description')}\n"

                        blocks = layer.get('blocks', [])
                        result_text += f"  Blocks: {len(blocks)} placements\n"

                        # Show first few blocks as examples
                        if blocks:
                            result_text += f"  Example blocks:\n"
                            for block in blocks[:3]:
                                result_text += f"    - ({block.get('x')}, {block.get('z')}): {block.get('block')}\n"
                            if len(blocks) > 3:
                                result_text += f"    ... and {len(blocks) - 3} more blocks\n"

                        if layer.get('notes'):
                            result_text += f"  Notes: {layer.get('notes')}\n"
                        result_text += "\n"

                    if len(layers) > 5:
                        result_text += f"... and {len(layers) - 5} more layers (see full JSON below)\n\n"

                # Placement notes
                if pattern.get('placement_notes'):
                    result_text += f"**Placement Notes:** {pattern.get('placement_notes')}\n\n"

                # Use cases
                use_cases = pattern.get('use_cases', [])
                if use_cases:
                    result_text += f"**Use Cases:**\n"
                    for use_case in use_cases:
                        result_text += f"  - {use_case}\n"
                    result_text += "\n"

                # Variants
                variants = pattern.get('variants', [])
                if variants:
                    result_text += f"**Variants:** {', '.join(variants)}\n\n"

                # Related patterns
                related = pattern.get('related_patterns', [])
                if related:
                    result_text += f"**Related Patterns:** {', '.join(related)}\n\n"

                # Tags
                if pattern.get('tags'):
                    result_text += f"**Tags:** {', '.join(pattern['tags'])}\n\n"

                structured = structured_patterns.get(pattern_id)
                if structured:
                    palette = structured.get('palette', {})
                    struct_layers = structured.get('layers', [])
                    result_text += "✅ **Structured placement data available.**\n"
                    result_text += "Run `place_building_pattern` with this pattern_id to build automatically.\n\n"

                    if palette:
                        result_text += "**Palette Legend:**\n"
                        for symbol, block in palette.items():
                            printable = symbol if symbol.strip() else "<space>"
                            result_text += f"  - `{printable}` → {block}\n"
                        result_text += "\n"

                    result_text += f"Structured Layers: {len(struct_layers)} (see building_patterns_structured.json for full grid data)\n\n"

                # Full pattern data as JSON
                result_text += "**Full Pattern Data (JSON):**\n```json\n"
                result_text += json.dumps(pattern, indent=2)
                result_text += "\n```\n\n"

                result_text += "💡 Use WorldEdit commands to build this pattern layer by layer at your desired location."

                return [TextContent(type="text", text=result_text)]

            else:
                return [TextContent(type="text", text=f"❌ Invalid action: '{action}'. Must be 'search' or 'get'.")]

        elif name == "place_building_pattern":
            pattern_id = arguments.get("pattern_id")
            origin_x = arguments.get("origin_x")
            origin_y = arguments.get("origin_y")
            origin_z = arguments.get("origin_z")
            facing = arguments.get("facing")
            preview_only = arguments.get("preview_only", False)

            missing = [field for field in ("pattern_id", "origin_x", "origin_y", "origin_z") if arguments.get(field) is None]
            if missing:
                return [TextContent(type="text", text=f"❌ Missing required field(s): {', '.join(missing)}")]

            if facing:
                facing = facing.lower()
                if facing not in FurniturePlacer.ROTATIONS:
                    valid = ", ".join(FurniturePlacer.ROTATIONS.keys())
                    return [TextContent(type="text", text=f"❌ Invalid facing '{facing}'. Valid options: {valid}")]

            structured = next((p for p in load_structured_patterns() if p.get('id') == pattern_id), None)
            if not structured:
                return [TextContent(type="text", text=f"❌ Pattern '{pattern_id}' does not have structured placement data yet.")]

            metadata_pattern = next((p for p in _load_json_list(CONTEXT_DIR / 'building_patterns_complete.json') if p.get('id') == pattern_id), None)
            pattern_name = structured.get('name') or (metadata_pattern or {}).get('name') or pattern_id

            try:
                commands = PatternPlacer.get_placement_commands(
                    pattern=structured,
                    origin_x=int(origin_x),
                    origin_y=int(origin_y),
                    origin_z=int(origin_z),
                    facing=facing,
                )
            except ValueError as exc:
                logger.error(f"Error generating pattern placement commands: {exc}")
                return [TextContent(type="text", text=f"❌ Failed to generate commands: {exc}")]

            summary = PatternPlacer.get_command_summary(commands)
            final_facing = facing or structured.get('origin', {}).get('facing', 'north')

            if preview_only:
                command_block = '\n'.join(commands)
                output = [
                    "🏗️ **Building Pattern Preview**",
                    f"Pattern: {pattern_name} (`{pattern_id}`)",
                    f"Origin: ({origin_x},{origin_y},{origin_z})",
                    f"Facing: {final_facing}",
                    "",
                    summary,
                    "Commands:",
                    "```plain",
                    command_block,
                    "```",
                    "Set `preview_only` to false to execute these commands.",
                ]
                return [TextContent(type="text", text='\n'.join(output))]

            executed_commands: List[str] = []
            try:
                for command in commands:
                    stripped = command.strip()
                    if not stripped or stripped.startswith('#'):
                        continue
                    executed_commands.append(stripped)
                    rcon.execute_command(stripped)
            except Exception as exc:
                logger.error(f"Pattern placement failed: {exc}", exc_info=True)
                failure_output = [
                    "❌ **Pattern placement failed**",
                    f"Pattern: {pattern_name} (`{pattern_id}`)",
                    f"Origin: ({origin_x},{origin_y},{origin_z})",
                    f"Facing: {final_facing}",
                    "",
                    "Commands executed before failure:",
                ]
                for cmd in executed_commands[-10:]:
                    failure_output.append(f"- `{cmd}`")
                failure_output.extend([
                    "",
                    f"Error: {exc}",
                    "Use `//undo` to revert the changes if necessary.",
                ])
                return [TextContent(type="text", text='\n'.join(failure_output))]

            palette = structured.get('palette', {})
            materials = (metadata_pattern or {}).get('materials', {})

            palette_lines = []
            if palette:
                palette_lines.append("**Palette Legend:**")
                for symbol, block in palette.items():
                    printable = symbol if symbol.strip() else "<space>"
                    palette_lines.append(f"- `{printable}` → {block}")

            material_lines = []
            if materials:
                material_lines.append("**Metadata Materials:**")
                for block, count in sorted(materials.items(), key=lambda item: item[0])[:10]:
                    material_lines.append(f"- {block}: {count}")
                if len(materials) > 10:
                    material_lines.append(f"- … ({len(materials) - 10} more)")

            success_lines = [
                "✅ **Pattern placed successfully**",
                f"Pattern: {pattern_name} (`{pattern_id}`)",
                f"Origin: ({origin_x},{origin_y},{origin_z})",
                f"Facing: {final_facing}",
                "",
                summary,
            ]

            if palette_lines:
                success_lines.append("")
                success_lines.extend(palette_lines)

            if material_lines:
                success_lines.append("")
                success_lines.extend(material_lines)

            displayed_commands = executed_commands[:10]
            if displayed_commands:
                success_lines.append("")
                success_lines.append("**Executed Commands (first 10):**")
                for cmd in displayed_commands:
                    success_lines.append(f"- `{cmd}`")
                if len(executed_commands) > 10:
                    success_lines.append(f"- … ({len(executed_commands) - 10} more)")

            success_lines.append("")
            success_lines.append("Undo tip: run `//undo` if you need to revert this placement.")

            return [TextContent(type="text", text='\n'.join(success_lines))]

        elif name == "schematic_library":
            action = arguments.get("action")

            if not action:
                return [TextContent(type="text", text="❌ Error: 'action' parameter is required")]

            try:
                if action == "list":
                    schematics = list_schematics()
                    if not schematics:
                        return [TextContent(type="text", text="📁 No .schem files found in the `schemas/` directory.")]

                    lines = [
                        "📁 **Available Schematics**",
                        f"Source folder: {SCHEM_SOURCE_DIR}",
                        f"WorldEdit folder: {SCHEM_DEST_DIR}",
                        "",
                    ]

                    for schem in schematics:
                        size = (
                            f"{schem.width}×{schem.height}×{schem.length}"
                            if schem.width and schem.height and schem.length
                            else "unknown"
                        )
                        server_flag = "✅" if schem.exists_on_server else "➕"
                        lines.append(
                            f"{server_flag} `{schem.name}` – size: {size} (blocks: {schem.block_count or 'unknown'})"
                        )
                    lines.append("")
                    lines.append("Legend: ✅ already copied to server, ➕ needs prepare/load")

                    return [TextContent(type="text", text='\n'.join(lines))]

                if action == "info":
                    name = arguments.get("name")
                    if not name:
                        return [TextContent(type="text", text="❌ 'name' is required for action='info'")]

                    meta = read_metadata(_resolve_schematic_path(name))
                    if not meta:
                        return [TextContent(type="text", text=f"❌ Schematic '{name}' not found")]

                    server_path = SCHEM_DEST_DIR / f"{meta.path.stem}.schem"
                    meta.exists_on_server = server_path.exists()

                    lines = [
                        f"🧾 **Schematic Metadata:** `{meta.name}`",
                        f"Path: {meta.path}",
                        f"Size: {meta.width or '?'}×{meta.height or '?'}×{meta.length or '?'} (W×H×D)",
                        f"Block data length: {meta.block_count or 'unknown'}",
                        f"Offset: {meta.offset or 'not set'}",
                        f"Exists on server: {'✅ yes' if meta.exists_on_server else '❌ no'}",
                    ]
                    return [TextContent(type="text", text='\n'.join(lines))]

                if action in {"prepare", "load"}:
                    name = arguments.get("name")
                    if not name:
                        return [TextContent(type="text", text=f"❌ 'name' is required for action='{action}'")]

                    target_name = arguments.get("target_name")
                    destination = copy_to_server(name, target_name)
                    dest_stem = destination.stem

                    if " " in dest_stem:
                        return [TextContent(type="text", text=(
                            "❌ Destination name contains spaces. Please use a name without spaces (e.g., 'modern_villa_1')."
                        ))]

                    if action == "prepare":
                        lines = [
                            f"✅ Schematic copied to server schematics folder as `{destination.name}`",
                            f"Location: {destination}",
                            "Run `schematic_library` with action='load' (or execute //schem load manually) when you're ready to use it.",
                        ]
                        return [TextContent(type="text", text='\n'.join(lines))]

                    # action == "load"
                    command = f"//schem load schem {dest_stem}"
                    rcon.execute_command(command)

                    lines = [
                        f"✅ Schematic `{destination.name}` prepared and loaded via `{command}`",
                        f"Copied from: {_resolve_schematic_path(name)}",
                        f"Server path: {destination}",
                        "Next steps:",
                        "1. Move the paste anchor (e.g., use //pos or teleport commands)",
                        "2. Run `worldedit_clipboard` with `command='paste -a -o'` (or desired flags)",
                        "   Example: worldedit_clipboard(command='paste -a -o')",
                    ]
                    return [TextContent(type="text", text='\n'.join(lines))]

                return [TextContent(type="text", text=f"❌ Unknown action '{action}' for schematic_library")]

            except FileNotFoundError as exc:
                return [TextContent(type="text", text=f"❌ {exc}")]
            except Exception as exc:
                logger.error(f"Error handling schematic_library action '{action}': {exc}", exc_info=True)
                return [TextContent(type="text", text=f"❌ Schematic operation failed: {exc}")]

        elif name == "building_template":
            import json
            from pathlib import Path

            action = arguments.get("action")
            if not action:
                return [TextContent(type="text", text="❌ Error: 'action' parameter is required")]

            # Load templates from JSON file
            templates_file = Path(__file__).parent.parent.parent.parent / "context" / "building_templates.json"

            try:
                with open(templates_file, 'r') as f:
                    templates_data = json.load(f)
                    templates = templates_data.get("templates", {})
            except FileNotFoundError:
                return [TextContent(type="text", text=f"❌ Templates file not found: {templates_file}")]
            except json.JSONDecodeError as e:
                return [TextContent(type="text", text=f"❌ Error parsing templates JSON: {e}")]

            if action == "list":
                # List all templates with brief info
                result_text = f"📚 **Building Templates Library** ({len(templates)} templates)\n\n"

                # Group by category
                by_category = {}
                for tid, tmpl in templates.items():
                    cat = tmpl["metadata"]["category"]
                    if cat not in by_category:
                        by_category[cat] = []
                    by_category[cat].append(tmpl)

                for category, tmpls in sorted(by_category.items()):
                    result_text += f"**{category.title()}** ({len(tmpls)}):\n"
                    for tmpl in tmpls:
                        meta = tmpl["metadata"]
                        diff_emoji = {"beginner": "🟢", "intermediate": "🟡", "advanced": "🔴"}
                        emoji = diff_emoji.get(meta["difficulty"], "⚪")
                        result_text += f"  {emoji} **{tmpl['template_id']}** - {meta['name']} ({meta['difficulty']})\n"
                        result_text += f"     {meta['description']}\n"
                    result_text += "\n"

                result_text += "\n💡 Use building_template(action='get', template_id='<id>') to view full details\n"
                result_text += "💡 Use building_template(action='search', category='<cat>') to filter by category"

                return [TextContent(type="text", text=result_text)]

            elif action == "search":
                # Search templates
                category_filter = arguments.get("category")
                difficulty_filter = arguments.get("difficulty")
                style_tags_filter = arguments.get("style_tags", [])

                results = []
                for tid, tmpl in templates.items():
                    meta = tmpl["metadata"]

                    # Apply filters
                    if category_filter and meta["category"] != category_filter:
                        continue
                    if difficulty_filter and meta["difficulty"] != difficulty_filter:
                        continue
                    if style_tags_filter:
                        tmpl_tags = meta.get("style_tags", [])
                        if not any(tag in tmpl_tags for tag in style_tags_filter):
                            continue

                    results.append(tmpl)

                if not results:
                    return [TextContent(type="text", text="❌ No templates found matching your criteria")]

                result_text = f"🔍 **Search Results** ({len(results)} found)\n\n"
                for tmpl in results:
                    meta = tmpl["metadata"]
                    diff_emoji = {"beginner": "🟢", "intermediate": "🟡", "advanced": "🔴"}
                    emoji = diff_emoji.get(meta["difficulty"], "⚪")
                    result_text += f"{emoji} **{tmpl['template_id']}** - {meta['name']}\n"
                    result_text += f"   Category: {meta['category']} | Difficulty: {meta['difficulty']}\n"
                    result_text += f"   {meta['description']}\n"
                    tags = ", ".join(meta.get("style_tags", []))
                    if tags:
                        result_text += f"   Tags: {tags}\n"
                    result_text += "\n"

                result_text += "\n💡 Use building_template(action='get', template_id='<id>') to view full template"

                return [TextContent(type="text", text=result_text)]

            elif action == "get":
                # Get full template details
                template_id = arguments.get("template_id")
                if not template_id:
                    return [TextContent(type="text", text="❌ Error: 'template_id' required for get action")]

                if template_id not in templates:
                    available = ", ".join(templates.keys())
                    return [TextContent(type="text", text=f"❌ Template '{template_id}' not found. Available: {available}")]

                tmpl = templates[template_id]
                meta = tmpl["metadata"]
                params = tmpl["parameters"]
                components = tmpl["components"]
                build_seq = tmpl["build_sequence"]
                dims = tmpl.get("dimensions", {})

                result_text = f"🏗️ **{meta['name']}**\n\n"
                result_text += f"**Description**: {meta['description']}\n"
                result_text += f"**Category**: {meta['category']} | **Difficulty**: {meta['difficulty']}\n"
                result_text += f"**Estimated Time**: ~{meta.get('estimated_time_seconds', 60)} seconds\n"
                tags = ", ".join(meta.get("style_tags", []))
                if tags:
                    result_text += f"**Style Tags**: {tags}\n"
                result_text += "\n"

                # Dimensions
                result_text += "📐 **Dimensions**:\n"
                result_text += f"   Footprint: {dims.get('footprint', 'Varies by parameters')}\n"
                result_text += f"   Height: {dims.get('total_height', 'Varies by parameters')}\n"
                if "interior_space" in dims:
                    result_text += f"   Interior: {dims['interior_space']}\n"
                result_text += "\n"

                # Parameters
                result_text += "⚙️ **Customizable Parameters**:\n"
                for param_name, param_def in params.items():
                    ptype = param_def["type"]
                    default = param_def["default"]
                    desc = param_def.get("description", "")

                    if ptype == "integer":
                        min_val = param_def.get("min", "")
                        max_val = param_def.get("max", "")
                        result_text += f"   • {param_name}: {min_val}-{max_val} blocks (default: {default}) - {desc}\n"
                    elif ptype == "enum":
                        options = ", ".join(param_def.get("options", []))
                        result_text += f"   • {param_name}: {options} (default: {default}) - {desc}\n"
                    elif ptype == "boolean":
                        result_text += f"   • {param_name}: true/false (default: {default}) - {desc}\n"
                result_text += "\n"

                # Build sequence
                result_text += "🔨 **Build Sequence** ({} components):\n".format(len(build_seq))
                for i, step in enumerate(build_seq, 1):
                    comp_id = step["component_id"]
                    comp = components.get(comp_id, {})
                    checkpoint = " 🛑 [CHECKPOINT]" if step.get("checkpoint") else ""
                    result_text += f"   {i}. **{comp_id}**{checkpoint}\n"
                    result_text += f"      {comp.get('description', 'No description')}\n"

                    # Show first step of component as example
                    steps = comp.get("steps", [])
                    if steps:
                        first_step = steps[0]
                        result_text += f"      Example: {first_step.get('action', '')} (tool: {first_step.get('tool', '')})\n"
                        if "command" in first_step:
                            result_text += f"      Command: {first_step['command']}\n"

                result_text += "\n"

                # Material palette reference
                if "material_palette" in tmpl:
                    result_text += f"🎨 **Material Palette**: {tmpl['material_palette']}\n"
                    result_text += f"   (See context/minecraft_material_palettes.json for details)\n\n"

                result_text += "💡 **Usage**:\n"
                result_text += "1. Customize parameters based on user preferences\n"
                result_text += "2. Follow build_sequence in order\n"
                result_text += "3. For each component, execute steps using specified tools\n"
                result_text += "4. Replace {{parameter}} placeholders with actual values\n"
                result_text += "5. Use checkpoints to verify progress with user\n"

                return [TextContent(type="text", text=result_text)]

            elif action == "customize":
                # Show customization guide for a template
                template_id = arguments.get("template_id")
                if not template_id:
                    return [TextContent(type="text", text="❌ Error: 'template_id' required for customize action")]

                if template_id not in templates:
                    return [TextContent(type="text", text=f"❌ Template '{template_id}' not found")]

                tmpl = templates[template_id]
                meta = tmpl["metadata"]
                params = tmpl["parameters"]

                result_text = f"🎨 **Customization Guide: {meta['name']}**\n\n"
                result_text += "**How to Customize**:\n"
                result_text += "1. Review parameters below\n"
                result_text += "2. Ask user for preferences (or use defaults)\n"
                result_text += "3. Validate values are within min/max ranges\n"
                result_text += "4. Substitute {{parameter}} in component commands\n\n"

                result_text += "**Available Parameters**:\n\n"
                for param_name, param_def in params.items():
                    ptype = param_def["type"]
                    default = param_def["default"]
                    desc = param_def.get("description", "")

                    result_text += f"**{param_name}**\n"
                    result_text += f"  Type: {ptype}\n"
                    result_text += f"  Default: {default}\n"

                    if ptype == "integer":
                        min_val = param_def.get("min")
                        max_val = param_def.get("max")
                        result_text += f"  Range: {min_val} to {max_val}\n"
                    elif ptype == "enum":
                        options = param_def.get("options", [])
                        result_text += f"  Options: {', '.join(options)}\n"

                    result_text += f"  Description: {desc}\n\n"

                result_text += "**Example Customization**:\n"
                result_text += "User: 'Make it taller and use dark materials'\n"
                result_text += "Agent: Sets parameters:\n"

                # Show example customization based on first few parameters
                for param_name, param_def in list(params.items())[:3]:
                    ptype = param_def["type"]
                    if ptype == "integer" and "height" in param_name.lower():
                        max_val = param_def.get("max")
                        result_text += f"  {param_name} = {max_val} (max height)\n"
                    elif ptype == "enum" and "material" in param_name.lower():
                        options = param_def.get("options", [])
                        dark_option = next((opt for opt in options if "dark" in opt.lower()), options[0])
                        result_text += f"  {param_name} = '{dark_option}' (dark material)\n"

                return [TextContent(type="text", text=result_text)]

            else:
                return [TextContent(type="text", text=f"❌ Unknown action: {action}. Use 'list', 'search', 'get', or 'customize'")]

        elif name == "terrain_pattern_lookup":
            action = arguments.get("action")

            if not action:
                return [TextContent(type="text", text="❌ Error: 'action' parameter is required (must be 'search' or 'get')")]

            # Load terrain patterns
            patterns_path = Path(__file__).parent.parent.parent.parent / 'context' / 'terrain_patterns_complete.json'
            patterns = []
            if patterns_path.exists():
                try:
                    with open(patterns_path, 'r') as f:
                        data = json.load(f)
                        # Handle both array format and object format
                        if isinstance(data, list):
                            patterns = data
                        elif isinstance(data, dict):
                            # If it's a dict with a "patterns" key, extract those
                            if "patterns" in data:
                                patterns_dict = data["patterns"]
                                # Convert dict of patterns to list
                                patterns = list(patterns_dict.values())
                            else:
                                # Assume the dict itself contains patterns
                                patterns = list(data.values())
                except Exception as e:
                    logger.warning(f"Could not load terrain patterns: {str(e)}")
                    return [TextContent(type="text", text=f"❌ Error loading terrain patterns: {str(e)}")]
            else:
                logger.warning(f"Terrain patterns file not found at: {patterns_path}")
                return [TextContent(type="text", text=f"❌ Error: Terrain patterns file not found at {patterns_path}")]

            # Discovery actions
            if action == "browse":
                # List all patterns (names and IDs only)
                result_text = f"🌲 **Terrain Pattern Library** - {len(patterns)} patterns available\n\n"

                # Group by category
                by_category = {}
                for pattern in patterns:
                    cat = pattern.get("category", "unknown")
                    if cat not in by_category:
                        by_category[cat] = []
                    by_category[cat].append(pattern)

                for category, cat_patterns in sorted(by_category.items()):
                    result_text += f"**{category.upper()}** ({len(cat_patterns)} patterns):\n"
                    for pattern in sorted(cat_patterns, key=lambda p: p.get("id", "")):
                        result_text += f"  - {pattern.get('name')} (ID: `{pattern.get('id')}`)\n"
                    result_text += "\n"

                result_text += "💡 Use action='get' with pattern_id to retrieve full construction details."

                return [TextContent(type="text", text=result_text)]

            elif action == "categories":
                # List all categories with counts
                category_counts = {}
                category_subcats = {}

                for pattern in patterns:
                    cat = pattern.get("category", "unknown")
                    subcat = pattern.get("subcategory", "")

                    category_counts[cat] = category_counts.get(cat, 0) + 1

                    if cat not in category_subcats:
                        category_subcats[cat] = set()
                    if subcat:
                        category_subcats[cat].add(subcat)

                result_text = "🌲 **Terrain Pattern Categories**\n\n"

                for category in sorted(category_counts.keys()):
                    count = category_counts[category]
                    subcats = sorted(category_subcats.get(category, set()))

                    result_text += f"**{category}** ({count} patterns)\n"
                    if subcats:
                        result_text += f"  Subcategories: {', '.join(subcats)}\n"
                    result_text += "\n"

                result_text += "💡 Use action='subcategories' with category='<name>' to see patterns in that category.\n"
                result_text += "💡 Use action='search' with category='<name>' to find patterns."

                return [TextContent(type="text", text=result_text)]

            elif action == "subcategories":
                # List subcategories for a specific category
                category = arguments.get("category", "").lower()

                if not category:
                    return [TextContent(type="text", text="❌ Error: 'category' parameter required for action='subcategories'")]

                # Find patterns in this category
                cat_patterns = [p for p in patterns if p.get("category", "").lower() == category]

                if not cat_patterns:
                    return [TextContent(type="text", text=f"❌ No patterns found in category '{category}'. Use action='categories' to see available categories.")]

                # Group by subcategory
                by_subcat = {}
                for pattern in cat_patterns:
                    subcat = pattern.get("subcategory", "none")
                    if subcat not in by_subcat:
                        by_subcat[subcat] = []
                    by_subcat[subcat].append(pattern)

                result_text = f"🌲 **{category.upper()} Category** - {len(cat_patterns)} patterns\n\n"

                for subcat, subcat_patterns in sorted(by_subcat.items()):
                    result_text += f"**{subcat}** ({len(subcat_patterns)} patterns):\n"
                    for pattern in sorted(subcat_patterns, key=lambda p: p.get("id", "")):
                        dims = pattern.get("dimensions", {})
                        size = f"{dims.get('width')}×{dims.get('height')}×{dims.get('depth')}"
                        result_text += f"  - {pattern.get('name')} (ID: `{pattern.get('id')}`) - {size}\n"
                    result_text += "\n"

                result_text += "💡 Use action='get' with pattern_id to retrieve full construction details."

                return [TextContent(type="text", text=result_text)]

            elif action == "tags":
                # List all tags with usage counts
                tag_counts = {}

                for pattern in patterns:
                    for tag in pattern.get("tags", []):
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1

                result_text = "🌲 **Terrain Pattern Tags**\n\n"

                # Sort by count (most used first)
                sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)

                for tag, count in sorted_tags:
                    result_text += f"- **{tag}** ({count} patterns)\n"

                result_text += "\n💡 Use action='search' with tags=['<tag>'] to find patterns with specific tags."

                return [TextContent(type="text", text=result_text)]

            elif action == "search":
                # Search for patterns by query, category, subcategory, or tags
                query = arguments.get("query", "").lower()
                category_filter = arguments.get("category", "").lower()
                subcategory_filter = arguments.get("subcategory", "").lower()
                tags_filter = arguments.get("tags", [])
                tags_filter = [tag.lower() for tag in tags_filter] if tags_filter else []

                results = []

                for pattern in patterns:
                    # Check if matches search criteria
                    matches = True

                    if query:
                        # Search in name, id, category, subcategory, and tags
                        name_match = query in pattern.get("name", "").lower()
                        id_match = query in pattern.get("id", "").lower()
                        cat_match = query in pattern.get("category", "").lower()
                        subcat_match = query in pattern.get("subcategory", "").lower()
                        desc_match = query in pattern.get("description", "").lower()
                        tags_match = any(query in tag.lower() for tag in pattern.get("tags", []))

                        matches = matches and (name_match or id_match or cat_match or subcat_match or desc_match or tags_match)

                    if category_filter:
                        matches = matches and (category_filter in pattern.get("category", "").lower())

                    if subcategory_filter:
                        matches = matches and (subcategory_filter in pattern.get("subcategory", "").lower())

                    if tags_filter:
                        pattern_tags = [tag.lower() for tag in pattern.get("tags", [])]
                        # Check if ALL filter tags are present
                        matches = matches and all(tag in pattern_tags for tag in tags_filter)

                    if matches:
                        # Add to results (summary only, not full pattern)
                        dims = pattern.get("dimensions", {})
                        results.append({
                            "name": pattern.get("name"),
                            "id": pattern.get("id"),
                            "category": pattern.get("category"),
                            "subcategory": pattern.get("subcategory"),
                            "tags": pattern.get("tags", []),
                            "dimensions": f"{dims.get('width')}×{dims.get('height')}×{dims.get('depth')}",
                            "difficulty": pattern.get("difficulty", "medium"),
                            "materials_count": sum(pattern.get("materials", {}).values()),
                            "layer_count": len(pattern.get("layers", [])),
                            "description": pattern.get("description", "")[:150] + "..." if len(pattern.get("description", "")) > 150 else pattern.get("description", "")
                        })

                if not results:
                    search_params = []
                    if query:
                        search_params.append(f"query='{query}'")
                    if category_filter:
                        search_params.append(f"category='{category_filter}'")
                    if subcategory_filter:
                        search_params.append(f"subcategory='{subcategory_filter}'")
                    if tags_filter:
                        search_params.append(f"tags={tags_filter}")

                    return [TextContent(type="text", text=f"🔍 No terrain patterns found matching: {', '.join(search_params)}\n\nTry:\n- Broader search terms\n- Different category (vegetation, features, paths, details)\n- Different subcategory (trees, bushes, rocks, ponds, etc.)\n- Fewer tag filters")]

                # Format results
                result_text = f"🌲 Found {len(results)} terrain pattern(s):\n\n"

                for i, item in enumerate(results, 1):
                    result_text += f"{i}. **{item['name']}** (ID: `{item['id']}`)\n"
                    result_text += f"   - Category: {item['category']}"
                    if item.get('subcategory'):
                        result_text += f" > {item['subcategory']}"
                    result_text += "\n"
                    result_text += f"   - Size: {item['dimensions']} blocks (W×H×D)\n"
                    result_text += f"   - Materials: {item['materials_count']} total blocks\n"
                    result_text += f"   - Layers: {item['layer_count']} construction layers\n"
                    result_text += f"   - Difficulty: {item['difficulty']}\n"
                    if item.get('tags'):
                        result_text += f"   - Tags: {', '.join(item['tags'])}\n"
                    if item.get('description'):
                        result_text += f"   - Description: {item['description']}\n"
                    result_text += "\n"

                result_text += f"\n💡 To get full construction instructions, use: terrain_pattern_lookup with action='get' and pattern_id='<id>'"

                return [TextContent(type="text", text=result_text)]

            elif action == "get":
                # Get specific pattern by ID
                pattern_id = arguments.get("pattern_id")

                if not pattern_id:
                    return [TextContent(type="text", text="❌ Error: 'pattern_id' parameter is required for action='get'")]

                # Find pattern
                pattern = None
                for item in patterns:
                    if item.get("id") == pattern_id:
                        pattern = item
                        break

                if not pattern:
                    return [TextContent(type="text", text=f"❌ Error: Pattern with ID '{pattern_id}' not found.\n\nUse action='search' to find available patterns.")]

                # Format full pattern details
                result_text = f"🌲 **{pattern.get('name')}** (ID: `{pattern.get('id')}`)\n\n"

                # Basic info
                result_text += f"**Category:** {pattern.get('category')}"
                if pattern.get('subcategory'):
                    result_text += f" > {pattern.get('subcategory')}"
                result_text += "\n\n"

                result_text += f"**Description:** {pattern.get('description', 'No description available.')}\n\n"

                # Dimensions
                dims = pattern.get('dimensions', {})
                result_text += f"**Dimensions:**\n"
                result_text += f"  - Width: {dims.get('width')} blocks\n"
                result_text += f"  - Height: {dims.get('height')} blocks\n"
                result_text += f"  - Depth: {dims.get('depth')} blocks\n\n"

                # Difficulty
                result_text += f"**Difficulty:** {pattern.get('difficulty', 'medium')}\n\n"

                # Materials
                materials = pattern.get('materials', {})
                if materials:
                    result_text += f"**Materials Required:** ({sum(materials.values())} total blocks)\n"
                    for material, count in sorted(materials.items(), key=lambda x: x[1], reverse=True):
                        result_text += f"  - {material}: {count}\n"
                    result_text += "\n"

                # Construction method
                if pattern.get('construction_method'):
                    result_text += f"**Construction Method:** {pattern.get('construction_method')}\n\n"

                # Layer-by-layer instructions
                layers = pattern.get('layers', [])
                if layers:
                    result_text += f"**Layer-by-Layer Instructions:** ({len(layers)} layers)\n\n"
                    for layer in layers[:5]:  # Show first 5 layers in detail
                        result_text += f"**Layer {layer.get('layer')}** (Y-offset: {layer.get('y_offset')})\n"
                        if layer.get('description'):
                            result_text += f"  Description: {layer.get('description')}\n"

                        blocks = layer.get('blocks', [])
                        result_text += f"  Blocks: {len(blocks)} placements\n"

                        # Show first few blocks as examples
                        if blocks:
                            result_text += f"  Example blocks:\n"
                            for block in blocks[:3]:
                                result_text += f"    - ({block.get('x')}, {block.get('z')}): {block.get('block')}\n"
                            if len(blocks) > 3:
                                result_text += f"    ... and {len(blocks) - 3} more blocks\n"

                        if layer.get('notes'):
                            result_text += f"  Notes: {layer.get('notes')}\n"
                        result_text += "\n"

                    if len(layers) > 5:
                        result_text += f"... and {len(layers) - 5} more layers (see full JSON below)\n\n"

                # Placement notes
                if pattern.get('placement_notes'):
                    result_text += f"**Placement Notes:** {pattern.get('placement_notes')}\n\n"

                # Use cases
                use_cases = pattern.get('use_cases', [])
                if use_cases:
                    result_text += f"**Use Cases:**\n"
                    for use_case in use_cases:
                        result_text += f"  - {use_case}\n"
                    result_text += "\n"

                # Variants
                variants = pattern.get('variants', [])
                if variants:
                    result_text += f"**Variants:** {', '.join(variants)}\n\n"

                # Related patterns
                related = pattern.get('related_patterns', [])
                if related:
                    result_text += f"**Related Patterns:** {', '.join(related)}\n\n"

                # Tags
                if pattern.get('tags'):
                    result_text += f"**Tags:** {', '.join(pattern['tags'])}\n\n"

                # Full pattern data as JSON
                result_text += "**Full Pattern Data (JSON):**\n```json\n"
                result_text += json.dumps(pattern, indent=2)
                result_text += "\n```\n\n"

                result_text += "💡 Use WorldEdit commands to build this pattern layer by layer at your desired location."

                return [TextContent(type="text", text=result_text)]

            else:
                return [TextContent(type="text", text=f"❌ Invalid action: '{action}'. Must be 'search' or 'get'.")]

        elif name == "analyze_placement_area":
            from .spatial_analyzer import SpatialAnalyzer
            import json

            # Get parameters
            center_x = arguments.get("center_x")
            center_y = arguments.get("center_y")
            center_z = arguments.get("center_z")
            radius = arguments.get("radius", 5)
            analysis_type = arguments.get("analysis_type", "general")

            # Validate required parameters
            if center_x is None or center_y is None or center_z is None:
                return [TextContent(type="text", text="❌ Error: center_x, center_y, and center_z are required")]

            # Create spatial analyzer
            analyzer = SpatialAnalyzer(rcon_manager)

            try:
                # Perform analysis
                result = analyzer.analyze_area(
                    center_x=center_x,
                    center_y=center_y,
                    center_z=center_z,
                    radius=radius,
                    analysis_type=analysis_type
                )

                # Format result for display
                result_text = f"📍 **Spatial Analysis**: ({center_x}, {center_y}, {center_z})\n\n"

                # Surfaces
                if "surfaces" in result:
                    surfaces = result["surfaces"]
                    result_text += "**Surfaces Detected**:\n"
                    if surfaces["floor_y"] is not None:
                        result_text += f"  Floor: Y={surfaces['floor_y']} (solid block)\n"
                    else:
                        result_text += f"  Floor: Not detected (scan down from center)\n"

                    if surfaces["ceiling_y"] is not None:
                        result_text += f"  Ceiling: Y={surfaces['ceiling_y']} (solid block)\n"
                    else:
                        result_text += f"  Ceiling: Not detected (scan up from center)\n"

                    if surfaces["walls"]:
                        walls = ", ".join(surfaces["walls"])
                        result_text += f"  Walls: {walls}\n"
                    else:
                        result_text += f"  Walls: No walls detected adjacent to center\n"
                    result_text += "\n"

                # Furniture placement
                if "furniture_placement" in result:
                    furn = result["furniture_placement"]
                    result_text += "**Furniture Placement Recommendation**:\n"
                    result_text += f"  Type: {furn['placement_type']} furniture\n"

                    if furn['placement_type'] == "floor":
                        result_text += f"  ✅ Place at Y={furn['recommended_floor_y']} (ON TOP of floor block at Y={furn.get('floor_block_y')})\n"
                    else:
                        result_text += f"  ✅ Hang at Y={furn['recommended_ceiling_y']} (ATTACHED to ceiling block at Y={furn.get('ceiling_block_y')})\n"

                    if furn['clear_space']:
                        result_text += f"  ✅ Clear space available\n"
                    else:
                        result_text += f"  ⚠️ WARNING: Space may be obstructed!\n"
                    result_text += "\n"

                # Roof context
                if "roof_context" in result:
                    roof = result["roof_context"]
                    result_text += "**Roof Construction Context**:\n"

                    if roof.get("total_stairs_found", 0) > 0:
                        result_text += f"  Found: {roof['total_stairs_found']} stair blocks\n"
                        result_text += f"  Slope Direction: {roof['slope_direction']}\n"
                        result_text += f"  Highest Stair Layer: Y={roof['last_stair_layer_y']}\n"

                        offset = roof["next_layer_offset"]
                        result_text += f"  \n"
                        result_text += f"  **Next Layer Offset**:\n"
                        result_text += f"    X offset: {offset['x']} (step {'east' if offset['x'] > 0 else 'west' if offset['x'] < 0 else 'none'})\n"
                        result_text += f"    Y offset: {offset['y']} (step up)\n"
                        result_text += f"    Z offset: {offset['z']} (step {'south' if offset['z'] > 0 else 'north' if offset['z'] < 0 else 'none'})\n"
                        result_text += f"  \n"
                        result_text += f"  💡 **Recommendation**: {roof.get('recommendation', 'Continue offset pattern')}\n"

                        if roof.get('uses_full_blocks'):
                            result_text += f"  📝 Ridge uses full blocks (not stairs)\n"

                    else:
                        result_text += f"  No existing stairs detected\n"
                        result_text += f"  💡 Start fresh: Build stair layers stepping inward horizontally (NOT stacked vertically)\n"

                    result_text += "\n"

                # Add raw JSON for advanced users
                result_text += "\n**Raw Analysis Data** (JSON):\n```json\n"
                result_text += json.dumps(result, indent=2)
                result_text += "\n```"

                return [TextContent(type="text", text=result_text)]

            except Exception as e:
                logger.error(f"Error in analyze_placement_area: {e}", exc_info=True)
                return [TextContent(type="text", text=f"❌ Spatial analysis failed: {e}")]

        elif name == "spatial_awareness_scan":
            from .spatial_analyzer_v2 import SpatialAnalyzerV2
            import json

            # Get parameters
            center_x = arguments.get("center_x")
            center_y = arguments.get("center_y")
            center_z = arguments.get("center_z")
            radius = arguments.get("radius", 5)
            detail_level = arguments.get("detail_level", "medium")

            # Validate required parameters
            if center_x is None or center_y is None or center_z is None:
                return [TextContent(type="text", text="❌ Error: center_x, center_y, and center_z are required")]

            # Create spatial analyzer V2
            analyzer = SpatialAnalyzerV2(rcon)

            try:
                logger.info(f"Starting spatial awareness scan V2: center=({center_x},{center_y},{center_z}), radius={radius}, detail={detail_level}")

                # Perform analysis
                result = analyzer.analyze_area(
                    center_x=center_x,
                    center_y=center_y,
                    center_z=center_z,
                    radius=radius,
                    detail_level=detail_level
                )

                # Use the built-in summary from the analyzer
                summary_text = result.get('summary', 'Analysis complete')

                # Add JSON data at the end
                full_text = summary_text + "\n\n**📊 Complete Analysis Data (JSON)**:\n```json\n"
                full_text += json.dumps(result, indent=2)
                full_text += "\n```"

                logger.info("Spatial awareness scan V2 complete")
                return [TextContent(type="text", text=full_text)]

            except Exception as e:
                logger.error(f"Error in spatial_awareness_scan: {e}", exc_info=True)
                return [TextContent(type="text", text=f"❌ Spatial awareness scan failed: {e}")]

        elif name == "terrain_analyzer":
            # Get parameters
            x1 = arguments.get("x1")
            y1 = arguments.get("y1")
            z1 = arguments.get("z1")
            x2 = arguments.get("x2")
            y2 = arguments.get("y2")
            z2 = arguments.get("z2")
            resolution = arguments.get("resolution", 2)
            max_samples = arguments.get("max_samples", 10000)

            # Validate required parameters
            if any(coord is None for coord in [x1, y1, z1, x2, y2, z2]):
                return [TextContent(type="text", text="❌ Error: All coordinate parameters (x1, y1, z1, x2, y2, z2) are required")]

            # Basic coordinate validation (ensure they're within Minecraft world limits)
            # Minecraft Y range: -64 to 320, X/Z range: -30000000 to 30000000
            if not (-30000000 <= x1 <= 30000000 and -30000000 <= x2 <= 30000000):
                return [TextContent(type="text", text="❌ Error: X coordinates must be between -30,000,000 and 30,000,000")]
            if not (-64 <= y1 <= 320 and -64 <= y2 <= 320):
                return [TextContent(type="text", text="❌ Error: Y coordinates must be between -64 and 320")]
            if not (-30000000 <= z1 <= 30000000 and -30000000 <= z2 <= 30000000):
                return [TextContent(type="text", text="❌ Error: Z coordinates must be between -30,000,000 and 30,000,000")]

            # Calculate region size
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            depth = abs(z2 - z1) + 1
            total_blocks = width * height * depth

            # Safety check: prevent analyzing extremely large regions
            if total_blocks > 1000000:  # 1 million blocks
                return [TextContent(type="text", text=f"❌ Error: Region too large ({total_blocks:,} blocks). Maximum 1,000,000 blocks.\nTry:\n- Reducing region size\n- Increasing resolution parameter")]

            # Create terrain analyzer
            analyzer = TerrainAnalyzer(rcon)

            try:
                logger.info(f"Starting terrain analysis: ({x1},{y1},{z1}) to ({x2},{y2},{z2}), resolution={resolution}")

                # Perform analysis
                result = analyzer.analyze_region(
                    x1, y1, z1,
                    x2, y2, z2,
                    resolution=resolution,
                    max_samples=max_samples
                )

                # Check for errors in result
                if 'error' in result:
                    return [TextContent(type="text", text=f"❌ Analysis error: {result['error']}")]

                # Format output
                output = format_terrain_analysis(result)

                logger.info(f"Terrain analysis complete: {result['region']['samples_taken']} samples collected")

                return [TextContent(type="text", text=output)]

            except Exception as e:
                logger.error(f"Error in terrain analysis: {str(e)}", exc_info=True)
                return [TextContent(type="text", text=f"❌ Analysis failed: {str(e)}")]

        elif name == "calculate_shape":
            shape_type = arguments.get("shape")

            try:
                if shape_type == "circle":
                    radius = arguments.get("radius")
                    filled = arguments.get("filled", False)

                    if radius is None:
                        return [TextContent(type="text", text="❌ Error: 'radius' parameter required for circle")]

                    result = CircleCalculator.calculate_circle(radius=radius, filled=filled)

                elif shape_type == "sphere":
                    radius = arguments.get("radius")
                    hollow = arguments.get("hollow", True)

                    if radius is None:
                        return [TextContent(type="text", text="❌ Error: 'radius' parameter required for sphere")]

                    result = CircleCalculator.calculate_sphere(radius=radius, hollow=hollow)

                elif shape_type == "dome":
                    radius = arguments.get("radius")
                    style = arguments.get("style", "hemisphere")

                    if radius is None:
                        return [TextContent(type="text", text="❌ Error: 'radius' parameter required for dome")]

                    result = CircleCalculator.calculate_dome(radius=radius, style=style)

                elif shape_type == "ellipse":
                    width = arguments.get("width")
                    height = arguments.get("height")
                    filled = arguments.get("filled", False)

                    if width is None or height is None:
                        return [TextContent(type="text", text="❌ Error: 'width' and 'height' parameters required for ellipse")]

                    result = CircleCalculator.calculate_ellipse(width=width, height=height, filled=filled)

                elif shape_type == "arch":
                    width = arguments.get("width")
                    height = arguments.get("height")
                    depth = arguments.get("depth", 1)

                    if width is None or height is None:
                        return [TextContent(type="text", text="❌ Error: 'width' and 'height' parameters required for arch")]

                    result = CircleCalculator.calculate_arch(width=width, height=height, depth=depth)

                else:
                    return [TextContent(type="text", text=f"❌ Error: Unknown shape type '{shape_type}'")]

                # Format output
                output = f"🔷 {result['shape'].upper()} Calculation\n\n"

                # Add shape-specific info
                if 'radius' in result:
                    output += f"**Radius:** {result['radius']} blocks\n"
                if 'width' in result:
                    output += f"**Width:** {result['width']} blocks\n"
                if 'height' in result:
                    output += f"**Height:** {result['height']} blocks\n"
                if 'depth' in result:
                    output += f"**Depth:** {result['depth']} blocks\n"
                if 'style' in result:
                    output += f"**Style:** {result['style']}\n"
                if 'filled' in result:
                    output += f"**Filled:** {'Yes' if result['filled'] else 'No (hollow outline)'}\n"
                if 'hollow' in result:
                    output += f"**Hollow:** {'Yes' if result['hollow'] else 'No (filled solid)'}\n"

                output += f"\n**Blocks Required:** {result['blocks_count']}\n\n"

                # Add ASCII preview for 2D shapes
                if 'ascii_preview' in result and result['ascii_preview']:
                    output += "**Preview:**\n```\n" + result['ascii_preview'] + "\n```\n\n"

                # Add usage tip
                if 'usage_tip' in result:
                    output += f"💡 **Tip:** {result['usage_tip']}\n\n"

                # Add WorldEdit command if available
                if 'worldedit_command' in result:
                    output += f"**WorldEdit Command:** `{result['worldedit_command']}`\n\n"

                # Add coordinate sample (first 20 coordinates)
                coords = result['coordinates'][:20]
                output += f"**Coordinates** (showing first 20 of {result['blocks_count']}):\n"
                for i, coord in enumerate(coords, 1):
                    if len(coord) == 2:
                        output += f"  {i}. ({coord[0]}, {coord[1]})\n"
                    else:
                        output += f"  {i}. ({coord[0]}, {coord[1]}, {coord[2]})\n"

                if len(result['coordinates']) > 20:
                    output += f"  ... and {len(result['coordinates']) - 20} more coordinates\n"

                output += "\n**Next Steps:**\n"
                output += "1. Use these coordinates to place blocks manually with setblock commands\n"
                output += "2. Or use WorldEdit's shape commands (//sphere, //cyl) as reference\n"
                output += "3. Build layer by layer for 3D shapes\n"

                logger.info(f"Shape calculation complete: {result['shape']} with {result['blocks_count']} blocks")

                return [TextContent(type="text", text=output)]

            except Exception as e:
                logger.error(f"Error in shape calculation: {str(e)}", exc_info=True)
                return [TextContent(type="text", text=f"❌ Calculation failed: {str(e)}")]

        elif name == "calculate_window_spacing":
            wall_length = arguments.get("wall_length")
            window_width = arguments.get("window_width")
            spacing_style = arguments.get("spacing_style", "even")
            window_count = arguments.get("window_count")

            try:
                result = WindowPlacementCalculator.calculate_window_spacing(
                    wall_length=wall_length,
                    window_width=window_width,
                    spacing_style=spacing_style,
                    window_count=window_count
                )

                # Format output
                output = f"🪟 Window Spacing Calculator\n\n"
                output += f"**Wall Length:** {result['wall_length']} blocks\n"
                output += f"**Window Width:** {result['window_width']} blocks\n"
                output += f"**Number of Windows:** {result['window_count']}\n"
                output += f"**Spacing Style:** {result['spacing_style']}\n\n"

                # Add spacing info
                spacing_info = result['spacing_info']
                output += "**Spacing Details:**\n"
                for key, value in spacing_info.items():
                    output += f"  - {key.replace('_', ' ').title()}: {value}\n"
                output += "\n"

                # Add window positions
                output += "**Window Placements:**\n"
                for window in result['windows']:
                    output += f"  {window['index']}. Position {window['start_position']}-{window['end_position']} (center: {window['center']})\n"
                output += "\n"

                # Add recommendation
                output += f"💡 **Recommendation:** {result['recommendation']}\n\n"

                output += "**Next Steps:**\n"
                output += "1. Use these positions to place windows at the correct spacing\n"
                output += "2. Apply this pattern to all walls of your building for consistency\n"
                output += "3. Adjust Y-coordinate for window height (typically 2-3 blocks above floor)\n"

                logger.info(f"Window spacing calculated: {result['window_count']} windows, {spacing_style} style")

                return [TextContent(type="text", text=output)]

            except Exception as e:
                logger.error(f"Error in window spacing calculation: {str(e)}", exc_info=True)
                return [TextContent(type="text", text=f"❌ Calculation failed: {str(e)}")]

        elif name == "check_symmetry":
            x1 = arguments.get("x1")
            y1 = arguments.get("y1")
            z1 = arguments.get("z1")
            x2 = arguments.get("x2")
            y2 = arguments.get("y2")
            z2 = arguments.get("z2")
            axis = arguments.get("axis", "x")
            tolerance = arguments.get("tolerance", 0)
            resolution = arguments.get("resolution", 1)

            try:
                checker = SymmetryChecker(rcon)
                result = checker.check_symmetry(x1, y1, z1, x2, y2, z2, axis, tolerance, resolution)

                if 'error' in result:
                    return [TextContent(type="text", text=f"❌ Error: {result['error']}")]

                # Format output
                output = f"🔄 Symmetry Check: {axis.upper()} Axis\n\n"
                output += f"**Symmetry Score:** {result['symmetry_score']}% ({result['verdict']})\n"
                output += f"**Center Plane:** {axis.upper()}={result['center_plane']}\n"
                output += f"**Blocks Checked:** {result['total_blocks_checked']:,}\n"
                output += f"**Symmetric:** {result['symmetric_blocks']:,} blocks\n"
                output += f"**Asymmetric:** {result['asymmetric_blocks']:,} blocks\n"
                output += f"**Tolerance:** {result['tolerance']} blocks allowed\n\n"

                output += f"**Summary:** {result['summary']}\n\n"

                if result['differences']:
                    output += f"**Asymmetric Blocks** (showing first {min(len(result['differences']), 50)} of {result['total_differences']}):\n"
                    for i, diff in enumerate(result['differences'][:10], 1):
                        output += f"  {i}. ({diff['position1'][0]},{diff['position1'][1]},{diff['position1'][2]}): {diff['block1']} ≠ "
                        output += f"({diff['position2'][0]},{diff['position2'][1]},{diff['position2'][2]}): {diff['block2']}\n"
                        output += f"     → {diff['recommendation']}\n"

                    if len(result['differences']) > 10:
                        output += f"  ... and {len(result['differences']) - 10} more differences\n"
                else:
                    output += "✅ **Perfect Symmetry!** No asymmetries detected.\n"

                logger.info(f"Symmetry check complete: {result['symmetry_score']}% on {axis} axis")

                workflow.record_validation(
                    "symmetry_check",
                    {
                        "region": {
                            "x1": x1,
                            "y1": y1,
                            "z1": z1,
                            "x2": x2,
                            "y2": y2,
                            "z2": z2,
                        },
                        "axis": axis,
                        "resolution": resolution,
                        "symmetry_score": result['symmetry_score'],
                        "differences": result['asymmetric_blocks'],
                    },
                )

                return [TextContent(type="text", text=output)]

            except Exception as e:
                logger.error(f"Error in symmetry check: {str(e)}", exc_info=True)
                return [TextContent(type="text", text=f"❌ Symmetry check failed: {str(e)}")]

        elif name == "analyze_lighting":
            x1 = arguments.get("x1")
            y1 = arguments.get("y1")
            z1 = arguments.get("z1")
            x2 = arguments.get("x2")
            y2 = arguments.get("y2")
            z2 = arguments.get("z2")
            resolution = arguments.get("resolution", 2)

            try:
                analyzer = LightingAnalyzer(rcon)
                result = analyzer.analyze_lighting(x1, y1, z1, x2, y2, z2, resolution)

                if 'error' in result:
                    return [TextContent(type="text", text=f"❌ Error: {result['error']}")]

                # Format output
                output = f"💡 Lighting Analysis\n\n"
                output += f"**Average Light Level:** {result['average_light_level']}\n"
                output += f"**Total Samples:** {result['total_samples']:,}\n"
                output += f"**Dark Spots:** {result['dark_spots_count']:,}\n"
                output += f"**Mob Spawn Risk:** {result['mob_spawn_risk']}\n\n"

                dist = result['light_distribution']
                output += "**Light Distribution:**\n"
                output += f"  - Well-lit (≥12): {dist['well_lit']:,} blocks ({dist['well_lit_percentage']}%)\n"
                output += f"  - Dim (8-11): {dist['dim']:,} blocks ({dist['dim_percentage']}%)\n"
                output += f"  - Dark (<8): {dist['dark']:,} blocks ({dist['dark_percentage']}%)\n\n"

                output += f"**Summary:** {result['summary']}\n\n"

                if result['optimal_placements']:
                    output += f"**Recommended Light Placements** ({len(result['optimal_placements'])} suggested):\n"
                    for i, placement in enumerate(result['optimal_placements'][:15], 1):
                        pos = placement['position']
                        output += f"  {i}. {placement['suggested_source'].capitalize()} at ({pos[0]},{pos[1]},{pos[2]}) - {placement['reason']}\n"

                    if len(result['optimal_placements']) > 15:
                        output += f"  ... and {len(result['optimal_placements']) - 15} more placements\n"
                else:
                    output += "✅ **Lighting adequate!** No additional light sources needed.\n"

                logger.info(f"Lighting analysis complete: {result['average_light_level']} avg light, {result['dark_spots_count']} dark spots")

                workflow.record_validation(
                    "lighting_analysis",
                    {
                        "region": {
                            "x1": x1,
                            "y1": y1,
                            "z1": z1,
                            "x2": x2,
                            "y2": y2,
                            "z2": z2,
                        },
                        "resolution": resolution,
                        "average_light": result['average_light_level'],
                        "dark_spots": result['dark_spots_count'],
                    },
                )

                return [TextContent(type="text", text=output)]

            except Exception as e:
                logger.error(f"Error in lighting analysis: {str(e)}", exc_info=True)
                return [TextContent(type="text", text=f"❌ Lighting analysis failed: {str(e)}")]

        elif name == "validate_structure":
            x1 = arguments.get("x1")
            y1 = arguments.get("y1")
            z1 = arguments.get("z1")
            x2 = arguments.get("x2")
            y2 = arguments.get("y2")
            z2 = arguments.get("z2")
            resolution = arguments.get("resolution", 1)

            try:
                validator = StructureValidator(rcon)
                result = validator.validate_structure(x1, y1, z1, x2, y2, z2, resolution)

                if 'error' in result:
                    return [TextContent(type="text", text=f"❌ Error: {result['error']}")]

                # Format output
                output = f"🏗️ Structure Integrity Validation\n\n"
                output += f"**Status:** {'✅ VALID' if result['structure_valid'] else '⚠️ ISSUES FOUND'}\n"
                output += f"**Blocks Checked:** {result['total_blocks_checked']:,}\n"
                output += f"**Issues Found:** {result['issues_found']}\n\n"

                output += f"**Summary:** {result['summary']}\n\n"

                if result['gravity_violations']:
                    output += f"**Gravity Violations** ({len(result['gravity_violations'])} found):\n"
                    for i, violation in enumerate(result['gravity_violations'][:10], 1):
                        pos = violation['position']
                        output += f"  {i}. {violation['block']} at ({pos[0]},{pos[1]},{pos[2]})\n"
                        output += f"     ⚠️ {violation['severity']}: {violation['issue']}\n"
                        output += f"     → {violation['recommendation']}\n"

                    if len(result['gravity_violations']) > 10:
                        output += f"  ... and {len(result['gravity_violations']) - 10} more violations\n"
                    output += "\n"

                if result['floating_blocks']:
                    output += f"**Floating Blocks** ({result['total_floating']} found, showing first 10):\n"
                    for i, floating in enumerate(result['floating_blocks'][:10], 1):
                        pos = floating['position']
                        output += f"  {i}. {floating['block']} at ({pos[0]},{pos[1]},{pos[2]})\n"
                        output += f"     ⚠️ {floating['severity']}: {floating['issue']}\n"
                        output += f"     → {floating['recommendation']}\n"

                    if result['total_floating'] > 10:
                        output += f"  ... and {result['total_floating'] - 10} more floating blocks\n"
                    output += "\n"

                if result['structure_valid']:
                    output += "✅ **Structure passed all validation checks!**\n"
                    output += "No physics violations or floating blocks detected.\n"

                logger.info(f"Structure validation complete: {result['issues_found']} issues found")

                workflow.record_validation(
                    "structure_validation",
                    {
                        "region": {
                            "x1": x1,
                            "y1": y1,
                            "z1": z1,
                            "x2": x2,
                            "y2": y2,
                            "z2": z2,
                        },
                        "resolution": resolution,
                        "issues_found": result['issues_found'],
                        "valid": result['structure_valid'],
                    },
                )

                return [TextContent(type="text", text=output)]

            except Exception as e:
                logger.error(f"Error in structure validation: {str(e)}", exc_info=True)
                return [TextContent(type="text", text=f"❌ Structure validation failed: {str(e)}")]

        elif name == "generate_terrain":
            terrain_type = arguments.get("type")
            x1, y1, z1 = arguments.get("x1"), arguments.get("y1"), arguments.get("z1")
            x2, y2, z2 = arguments.get("x2"), arguments.get("y2"), arguments.get("z2")

            # Optional parameters (vary by terrain type)
            scale = arguments.get("scale")
            amplitude = arguments.get("amplitude")
            depth = arguments.get("depth")
            height = arguments.get("height")
            direction = arguments.get("direction")
            octaves = arguments.get("octaves")
            smooth_iterations = arguments.get("smooth_iterations")
            seed = arguments.get("seed")

            try:
                generator = TerrainGenerator(rcon)

                # Call appropriate generation method based on type
                if terrain_type == "rolling_hills":
                    kwargs = {"x1": x1, "y1": y1, "z1": z1, "x2": x2, "y2": y2, "z2": z2}
                    if scale: kwargs["scale"] = scale
                    if amplitude: kwargs["amplitude"] = amplitude
                    if octaves: kwargs["octaves"] = octaves
                    if smooth_iterations: kwargs["smooth_iterations"] = smooth_iterations
                    if seed: kwargs["seed"] = seed
                    result = generator.generate_hills(**kwargs)

                elif terrain_type == "rugged_mountains":
                    kwargs = {"x1": x1, "y1": y1, "z1": z1, "x2": x2, "y2": y2, "z2": z2}
                    if scale: kwargs["scale"] = scale
                    if amplitude: kwargs["amplitude"] = amplitude
                    if octaves: kwargs["octaves"] = octaves
                    if smooth_iterations: kwargs["smooth_iterations"] = smooth_iterations
                    if seed: kwargs["seed"] = seed
                    result = generator.generate_mountains(**kwargs)

                elif terrain_type == "valley_network":
                    kwargs = {"x1": x1, "y1": y1, "z1": z1, "x2": x2, "y2": y2, "z2": z2}
                    if scale: kwargs["scale"] = scale
                    if depth: kwargs["depth"] = depth
                    if octaves: kwargs["octaves"] = octaves
                    if smooth_iterations: kwargs["smooth_iterations"] = smooth_iterations
                    if seed: kwargs["seed"] = seed
                    result = generator.generate_valleys(**kwargs)

                elif terrain_type == "mountain_range":
                    kwargs = {"x1": x1, "y1": y1, "z1": z1, "x2": x2, "y2": y2, "z2": z2}
                    if direction: kwargs["direction"] = direction
                    if scale: kwargs["scale"] = scale
                    if amplitude: kwargs["amplitude"] = amplitude
                    if octaves: kwargs["octaves"] = octaves
                    if smooth_iterations: kwargs["smooth_iterations"] = smooth_iterations
                    if seed: kwargs["seed"] = seed
                    result = generator.generate_mountain_range(**kwargs)

                elif terrain_type == "plateau":
                    kwargs = {"x1": x1, "y1": y1, "z1": z1, "x2": x2, "y2": y2, "z2": z2}
                    if height: kwargs["height"] = height
                    if smooth_iterations: kwargs["smooth_iterations"] = smooth_iterations
                    if seed: kwargs["seed"] = seed
                    result = generator.generate_plateau(**kwargs)

                else:
                    return [TextContent(type="text", text=f"❌ Unknown terrain type: {terrain_type}")]

                if not result.get("success"):
                    return [TextContent(type="text", text=f"❌ Error: {result.get('error', 'Unknown error')}")]

                # Format output
                output = f"🏔️ Terrain Generation Complete\n\n"
                output += f"**Type:** {result['terrain_type'].replace('_', ' ').title()}\n"
                output += f"**Summary:** {result['summary']}\n\n"

                output += "**Parameters Used:**\n"
                for key, value in result.get('parameters', {}).items():
                    output += f"  - {key}: {value}\n"
                output += "\n"

                output += "**Operations Performed:**\n"
                for i, (operation, step_result) in enumerate(result.get('steps', []), 1):
                    output += f"  {i}. {operation}\n"
                    if operation == "Selection" and step_result.get("success"):
                        region = step_result.get("region", {})
                        output += f"     Region: {region.get('volume', 0):,} blocks\n"
                output += "\n"

                output += "**Next Steps:**\n"
                output += "  • Apply texturing with texture_terrain() for natural appearance\n"
                output += "  • Add additional smoothing if needed with smooth_terrain()\n"
                output += "  • Overlay vegetation, water features, or structures\n"

                logger.info(f"Terrain generation complete: {terrain_type} at ({x1},{y1},{z1}) to ({x2},{y2},{z2})")

                return [TextContent(type="text", text=output)]

            except Exception as e:
                logger.error(f"Error generating terrain: {str(e)}", exc_info=True)
                return [TextContent(type="text", text=f"❌ Terrain generation failed: {str(e)}")]

        elif name == "texture_terrain":
            style = arguments.get("style")
            x1, y1, z1 = arguments.get("x1"), arguments.get("y1"), arguments.get("z1")
            x2, y2, z2 = arguments.get("x2"), arguments.get("y2"), arguments.get("z2")

            try:
                generator = TerrainGenerator(rcon)
                result = generator.texture_natural_slopes(x1, y1, z1, x2, y2, z2, style)

                if not result.get("success"):
                    return [TextContent(type="text", text=f"❌ Error: {result.get('error', 'Unknown error')}")]

                # Format output
                output = f"🎨 Terrain Texturing Complete\n\n"
                output += f"**Style:** {style.title()}\n"
                output += f"**Summary:** {result['summary']}\n\n"

                recipe = result.get('recipe', {})
                output += "**Materials Applied:**\n"
                output += f"  - Base: {recipe.get('base', 'N/A')}\n"
                output += f"  - Surface: {recipe.get('surface', 'N/A')}\n\n"

                output += "**Operations Performed:**\n"
                for i, (operation, step_result) in enumerate(result.get('steps', []), 1):
                    output += f"  {i}. {operation}\n"
                output += "\n"

                output += "**Texture applied successfully!** Your terrain now has a natural appearance.\n"

                logger.info(f"Terrain texturing complete: {style} style at ({x1},{y1},{z1}) to ({x2},{y2},{z2})")

                return [TextContent(type="text", text=output)]

            except Exception as e:
                logger.error(f"Error texturing terrain: {str(e)}", exc_info=True)
                return [TextContent(type="text", text=f"❌ Terrain texturing failed: {str(e)}")]

        elif name == "smooth_terrain":
            x1, y1, z1 = arguments.get("x1"), arguments.get("y1"), arguments.get("z1")
            x2, y2, z2 = arguments.get("x2"), arguments.get("y2"), arguments.get("z2")
            iterations = arguments.get("iterations", 2)
            mask = arguments.get("mask")

            try:
                generator = TerrainGenerator(rcon)

                # Set selection first
                select_result = generator.set_selection(x1, y1, z1, x2, y2, z2)
                if not select_result.get("success"):
                    return [TextContent(type="text", text=f"❌ Error: {select_result.get('error', 'Selection failed')}")]

                # Apply smoothing
                result = generator.smooth(iterations, mask)

                if not result.get("success"):
                    return [TextContent(type="text", text=f"❌ Error: {result.get('error', 'Unknown error')}")]

                # Format output
                output = f"✨ Terrain Smoothing Complete\n\n"
                output += f"**Iterations:** {result['iterations']}\n"
                output += f"**Region:** {select_result['region']['volume']:,} blocks\n"
                if mask:
                    output += f"**Mask:** {mask}\n"
                output += "\n"

                output += f"**Result:** {result['output']}\n\n"
                output += "Terrain has been smoothed for a more natural appearance.\n"

                logger.info(f"Terrain smoothing complete: {iterations} iterations at ({x1},{y1},{z1}) to ({x2},{y2},{z2})")

                return [TextContent(type="text", text=output)]

            except Exception as e:
                logger.error(f"Error smoothing terrain: {str(e)}", exc_info=True)
                return [TextContent(type="text", text=f"❌ Terrain smoothing failed: {str(e)}")]

        elif name == "workflow_status":
            status = workflow.get_status()
            current = workflow.current_phase()

            output = [
                "🗂️ **Build Workflow Status**",
                "",
                f"**Current Phase:** {current.name} (`{current.identifier}`)",
                "",
            ]

            for phase_info in status["phases"]:
                emoji = {
                    "completed": "✅",
                    "in_progress": "🟡",
                    "pending": "⚪",
                }.get(phase_info["status"], "⚪")

                line = f"{emoji} {phase_info['name']} (`{phase_info['id']}`)"
                if phase_info["required_validations"]:
                    completed = phase_info["completed_validations"]
                    requirements = ', '.join(
                        f"{req} ({completed.get(req, 0)})" for req in phase_info["required_validations"]
                    )
                    line += f" – validations: {requirements}"
                output.append(line)

            output.append("")
            output.append("Recorded validations:")
            validations = status.get("validations", {})
            if validations:
                for vtype, entries in validations.items():
                    output.append(f"- {vtype}: {len(entries)} run(s)")
            else:
                output.append("- none yet")

            return [TextContent(type="text", text='\n'.join(output))]

        elif name == "workflow_advance":
            advance_result = workflow.advance()

            if advance_result.get("advanced"):
                next_phase = workflow.current_phase()
                message = [
                    "✅ **Workflow advanced**",
                    f"Next phase: {next_phase.name} (`{next_phase.identifier}`)",
                ]
                return [TextContent(type="text", text='\n'.join(message))]

            missing = advance_result.get("missing")
            if missing:
                message = [
                    "⚠️ **Cannot advance yet**",
                    f"Phase `{advance_result.get('phase')}` still requires: {', '.join(missing)}",
                    "Run the required validations and try again.",
                ]
            else:
                message = [
                    "ℹ️ Workflow advance skipped",
                    advance_result.get("reason", "No additional information"),
                ]
            return [TextContent(type="text", text='\n'.join(message))]

        elif name == "workflow_reset":
            if not arguments.get("confirm", False):
                return [TextContent(type="text", text="⚠️ Reset not confirmed. Pass `confirm=true` to reset the workflow.")]

            workflow.reset()
            return [TextContent(type="text", text="✅ Workflow reset to planning phase.")]

        # Phase 1+2 WorldEdit Expansion: New Specialized Tools
        elif name == "worldedit_deform":
            expression = arguments.get("expression", "").strip()

            if not expression:
                return [TextContent(type="text", text="❌ Deformation expression cannot be empty")]

            command = f"//deform {expression}"

            # Add safety warning for deformations
            warning = "⚠️ **Deformation Warning**: //deform modifies terrain mathematically. Ensure you have a selection set and understand the expression.\n\n"

            # Use the generic rcon_command handler
            result = await call_tool("rcon_command", {"command": command})

            # Prepend warning to result
            if result and len(result) > 0:
                original_text = result[0].text
                result[0].text = warning + original_text

            return result

        elif name == "worldedit_vegetation":
            cmd = arguments.get("command")

            if not cmd:
                return [TextContent(type="text", text="❌ Command type must be specified (flora, forest, or tool_tree)")]

            if cmd == "flora":
                density = arguments.get("density", 10)
                if density < 0 or density > 100:
                    return [TextContent(type="text", text="❌ Density must be between 0 and 100")]
                command = f"//flora {density}"

            elif cmd == "forest":
                tree_type = arguments.get("type", "oak").lower()
                density = arguments.get("density", 5)

                if density < 0 or density > 100:
                    return [TextContent(type="text", text="❌ Density must be between 0 and 100")]

                # Validate tree type
                valid_types = ["oak", "birch", "spruce", "jungle", "acacia", "dark_oak", "mangrove", "cherry", "random"]
                if tree_type not in valid_types:
                    return [TextContent(type="text", text=f"❌ Invalid tree type. Valid types: {', '.join(valid_types)}")]

                command = f"//forest {tree_type} {density}"

            elif cmd == "tool_tree":
                tree_type = arguments.get("type", "oak").lower()
                size = arguments.get("size", "medium").lower()

                # Validate tree type
                valid_types = ["oak", "birch", "spruce", "jungle", "acacia", "dark_oak", "mangrove", "cherry"]
                if tree_type not in valid_types:
                    return [TextContent(type="text", text=f"❌ Invalid tree type. Valid types: {', '.join(valid_types)}")]

                # Validate size
                valid_sizes = ["small", "medium", "large"]
                if size not in valid_sizes:
                    return [TextContent(type="text", text=f"❌ Invalid size. Valid sizes: {', '.join(valid_sizes)}")]

                # Map size to tree type suffix
                size_suffix = ""
                if size == "small":
                    size_suffix = "_small"
                elif size == "large":
                    size_suffix = "_large"

                tree_with_size = tree_type + size_suffix if size_suffix else tree_type
                command = f"/tool tree {tree_with_size}"

            else:
                return [TextContent(type="text", text=f"❌ Unknown vegetation command: {cmd}")]

            # Use the generic rcon_command handler
            return await call_tool("rcon_command", {"command": command})

        elif name == "worldedit_terrain_advanced":
            cmd = arguments.get("command")

            if not cmd:
                return [TextContent(type="text", text="❌ Command type must be specified (caves, ore, or regen)")]

            if cmd == "caves":
                size = arguments.get("size", 8)
                freq = arguments.get("freq", 40)
                rarity = arguments.get("rarity", 7)
                minY = arguments.get("minY", 0)
                maxY = arguments.get("maxY", 128)

                # Validate parameters
                if freq < 1 or freq > 100:
                    return [TextContent(type="text", text="❌ Frequency must be between 1 and 100")]
                if rarity < 1 or rarity > 100:
                    return [TextContent(type="text", text="❌ Rarity must be between 1 and 100")]

                command = f"//caves {size} {freq} {rarity} {minY} {maxY}"

            elif cmd == "ore":
                pattern = arguments.get("pattern", "").strip()
                size = arguments.get("size", 4)
                freq = arguments.get("freq", 10)
                rarity = arguments.get("rarity", 100)
                minY = arguments.get("minY", -64)
                maxY = arguments.get("maxY", 64)

                if not pattern:
                    return [TextContent(type="text", text="❌ Pattern (ore type) must be specified")]

                # Validate parameters
                if freq < 1 or freq > 100:
                    return [TextContent(type="text", text="❌ Frequency must be between 1 and 100")]
                if rarity < 1 or rarity > 100:
                    return [TextContent(type="text", text="❌ Rarity must be between 1 and 100")]

                command = f"//ore {pattern} {size} {freq} {rarity} {minY} {maxY}"

            elif cmd == "regen":
                # Add warning for destructive command
                warning = "⚠️ **Regeneration Warning**: //regen will DESTROY all modifications in the selection and restore original terrain. This cannot be undone (except with //undo).\n\n"
                command = "//regen"

                # Use the generic rcon_command handler
                result = await call_tool("rcon_command", {"command": command})

                # Prepend warning to result
                if result and len(result) > 0:
                    original_text = result[0].text
                    result[0].text = warning + original_text

                return result

            else:
                return [TextContent(type="text", text=f"❌ Unknown terrain command: {cmd}")]

            # Use the generic rcon_command handler
            return await call_tool("rcon_command", {"command": command})

        elif name == "worldedit_analysis":
            cmd = arguments.get("command")

            if not cmd:
                return [TextContent(type="text", text="❌ Command type must be specified (distr or calc)")]

            if cmd == "distr":
                command = "//distr"

            elif cmd == "calc":
                expression = arguments.get("expression", "").strip()

                if not expression:
                    return [TextContent(type="text", text="❌ Expression for calculation must be provided")]

                command = f"//calc {expression}"

            else:
                return [TextContent(type="text", text=f"❌ Unknown analysis command: {cmd}")]

            # Use the generic rcon_command handler
            return await call_tool("rcon_command", {"command": command})

        else:
            return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}", exc_info=True)
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


async def main() -> None:
    """Main entry point for the MCP server"""
    global config, rcon

    # Load configuration
    config = load_config()

    logger.info("=" * 60)
    logger.info("🎮 VibeCraft MCP Server Starting...")
    logger.info("=" * 60)
    logger.info(f"RCON Host: {config.rcon_host}:{config.rcon_port}")
    logger.info(f"Safety Checks: {'Enabled' if config.enable_safety_checks else 'Disabled'}")
    logger.info(f"Dangerous Commands: {'Allowed' if config.allow_dangerous_commands else 'Blocked'}")

    # Initialize RCON manager
    rcon = RCONManager(config)

    # Test connection
    logger.info("Testing RCON connection...")
    if rcon.test_connection():
        logger.info("✅ RCON connection successful!")

        # Detect WorldEdit version if enabled
        if config.enable_version_detection:
            version = rcon.detect_worldedit_version()
            if version:
                logger.info(f"✅ WorldEdit {version} detected")
            else:
                logger.warning("⚠️ Could not detect WorldEdit version")
    else:
        logger.warning("⚠️ RCON connection test failed. Server may not be running.")
        logger.warning("   The MCP server will start anyway, but commands will fail until connection is established.")

    logger.info("=" * 60)
    logger.info("🚀 VibeCraft MCP Server Ready!")
    logger.info("   AI can now build in Minecraft using WorldEdit commands")
    logger.info("=" * 60)

    # Run the MCP server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
