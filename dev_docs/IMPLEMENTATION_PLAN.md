# VibeCraft MCP Server: Comprehensive Implementation Plan

**Project:** VibeCraft MCP Server
**Version:** 1.0
**Date:** 2025-10-30
**Author:** Steve (Junior Engineer)
**Status:** Awaiting Review by Cody

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current State Analysis](#current-state-analysis)
3. [Architecture Design](#architecture-design)
4. [Technology Stack](#technology-stack)
5. [Tool Design Strategy](#tool-design-strategy)
6. [Implementation Phases](#implementation-phases)
7. [Testing Strategy](#testing-strategy)
8. [Configuration & Deployment](#configuration--deployment)
9. [Documentation Requirements](#documentation-requirements)
10. [Risk Analysis & Mitigation](#risk-analysis--mitigation)
11. [Success Criteria](#success-criteria)
12. [Open Questions](#open-questions)

---

## Executive Summary

### Project Goal
Build a comprehensive MCP (Model Context Protocol) server that exposes ALL 200+ WorldEdit commands to AI assistants like Claude, enabling automated building and world manipulation in Minecraft via RCON.

### Key Statistics
- **200+ WorldEdit commands** to expose across 17 categories
- **50+ brush types**, **15+ pattern types**, **20+ mask types**
- **40+ math/expression functions** to support
- **3 major tool types**: Generic RCON, Categorized WorldEdit, Helper utilities

### Implementation Approach
**Hybrid Strategy**: Combine a flexible generic RCON tool with specialized categorized tools and comprehensive documentation resources. This provides both ease-of-use for AI and complete access to all functionality.

### Timeline Estimate
- **Phase 1 (MVP):** 2-3 days - Core RCON + Basic commands
- **Phase 2 (Core Commands):** 3-4 days - Essential 80 commands
- **Phase 3 (Complete):** 4-5 days - All 200+ commands + advanced features
- **Phase 4 (Polish):** 2-3 days - Testing, documentation, refinement
- **Total:** 11-15 days

---

## Current State Analysis

### Existing Implementation
The `/Users/er/Repos/vibecraft/mcp-server/server.py` contains a basic MCP server with:

**Strengths:**
- ✅ RCON connection established using `mcrcon` library
- ✅ Basic MCP server structure using official Python SDK
- ✅ Environment variable configuration (RCON_HOST, RCON_PORT, RCON_PASSWORD)
- ✅ Three tools implemented:
  - `minecraft_command`: Generic command execution
  - `worldedit_set_region`: Convenience wrapper for region operations
  - `get_server_info`: Server information retrieval
- ✅ Proper error handling and logging
- ✅ Console-compatible WorldEdit syntax (comma-separated coordinates)

**Limitations:**
- ❌ Only 3 tools out of 200+ commands exposed
- ❌ No comprehensive command documentation
- ❌ No pattern, mask, or expression helpers
- ❌ Limited AI guidance on command syntax
- ❌ No command validation or parameter checking
- ❌ No resources (JSON references, command lists)
- ❌ Missing brush, schematic, clipboard, and advanced operations
- ❌ No categorization of commands for better AI understanding

### Gap Analysis

| Category | Commands | Current Coverage | Gap |
|----------|----------|------------------|-----|
| General | 14 | 0 dedicated tools | 14 |
| Navigation | 7 | 0 | 7 |
| Selection | 18 | 1 partial (worldedit_set_region) | 17 |
| Region | 19 | 1 partial (via minecraft_command) | 18 |
| Generation | 13 | 0 | 13 |
| Clipboard | 12 | 0 | 12 |
| Tools | 15 | 0 | 15 |
| Brushes | 30+ | 0 | 30+ |
| Super Pickaxe | 4 | 0 | 4 |
| Biome | 3 | 0 | 3 |
| Chunk | 3 | 0 | 3 |
| Snapshot | 6 | 0 | 6 |
| Scripting | 2 | 0 | 2 |
| Utility | 16 | 0 | 16 |
| Search/Help | 2 | 0 | 2 |
| **TOTAL** | **200+** | **~3** | **~197** |

---

## Architecture Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI Assistant (Claude)                     │
│                    Natural Language Interface                    │
└────────────────────────────┬────────────────────────────────────┘
                             │ MCP Protocol
                             │ (stdio/JSON-RPC)
┌────────────────────────────▼────────────────────────────────────┐
│                     VibeCraft MCP Server                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Tool Registry & Dispatcher                     │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │  Core Tools:                                                │ │
│  │  • Generic RCON Tool (fallback for any command)            │ │
│  │  • Server Management Tools (info, status, logs)            │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │  Categorized WorldEdit Tools (17 categories):              │ │
│  │  • Selection Tools (18 commands)                           │ │
│  │  • Region Tools (19 commands)                              │ │
│  │  • Generation Tools (13 commands)                          │ │
│  │  • Clipboard Tools (12 commands)                           │ │
│  │  • Brush Tools (30+ commands)                              │ │
│  │  • Utility Tools (16 commands)                             │ │
│  │  • Navigation Tools (7 commands)                           │ │
│  │  • Biome Tools (3 commands)                                │ │
│  │  • ... (remaining 9 categories)                            │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │  Helper & Utility Tools:                                   │ │
│  │  • Pattern Builder/Validator                               │ │
│  │  • Mask Builder/Validator                                  │ │
│  │  • Expression Validator                                    │ │
│  │  • Coordinate Utilities                                    │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │  Resource Provider:                                        │ │
│  │  • Command Reference JSON                                  │ │
│  │  • Pattern Syntax Guide                                    │ │
│  │  • Mask Syntax Guide                                       │ │
│  │  • Expression Function Reference                           │ │
│  │  • Common Build Patterns/Recipes                           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │         RCON Connection Manager                             │ │
│  │  • Connection pooling                                       │ │
│  │  • Automatic reconnection                                   │ │
│  │  • Error handling & retry logic                             │ │
│  │  • Command queue management                                 │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │ RCON Protocol
                             │ (TCP port 25575)
┌────────────────────────────▼────────────────────────────────────┐
│                     Minecraft Server                             │
│  • Paper/Spigot/Bukkit (1.21+)                                  │
│  • WorldEdit Plugin (7.3+)                                      │
│  • RCON Enabled                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Component Design

#### 1. Core Server (`server.py`)
**Responsibilities:**
- Initialize MCP server instance
- Register all tools and resources
- Handle MCP protocol communication (stdio)
- Manage RCON connection lifecycle
- Coordinate between tools and RCON

**Key Classes:**
```python
class VibeCraftMCPServer:
    - app: Server (MCP server instance)
    - rcon_manager: RCONConnectionManager
    - tool_registry: ToolRegistry
    - resource_provider: ResourceProvider
```

#### 2. RCON Connection Manager (`rcon_manager.py`)
**Responsibilities:**
- Establish and maintain RCON connections
- Handle connection pooling (for potential parallel commands)
- Implement retry logic with exponential backoff
- Parse and sanitize RCON responses
- Track connection health

**Key Classes:**
```python
class RCONConnectionManager:
    - host: str
    - port: int
    - password: str
    - connection_pool: list[MCRcon]
    - max_retries: int = 3
    - retry_delay: float = 1.0

    def execute_command(command: str) -> str
    def execute_batch(commands: list[str]) -> list[str]
    def test_connection() -> bool
    def reconnect() -> bool
```

#### 3. Tool Registry (`tools/registry.py`)
**Responsibilities:**
- Register all MCP tools
- Organize tools by category
- Generate tool schemas dynamically
- Route tool calls to appropriate handlers

**Structure:**
```python
class ToolRegistry:
    - core_tools: dict[str, Tool]
    - worldedit_tools: dict[str, dict[str, Tool]]  # category -> tools
    - helper_tools: dict[str, Tool]

    def register_tool(tool: Tool, category: str)
    def get_all_tools() -> list[Tool]
    def get_tools_by_category(category: str) -> list[Tool]
```

#### 4. Tool Implementations
**File Organization:**
```
tools/
├── __init__.py
├── registry.py              # Tool registration and management
├── core/
│   ├── __init__.py
│   ├── rcon.py             # Generic RCON command tool
│   └── server.py           # Server management tools
├── worldedit/
│   ├── __init__.py
│   ├── selection.py        # Selection commands (18)
│   ├── region.py           # Region commands (19)
│   ├── generation.py       # Generation commands (13)
│   ├── clipboard.py        # Clipboard commands (12)
│   ├── brush.py            # Brush commands (30+)
│   ├── utility.py          # Utility commands (16)
│   ├── navigation.py       # Navigation commands (7)
│   ├── biome.py            # Biome commands (3)
│   ├── chunk.py            # Chunk commands (3)
│   ├── snapshot.py         # Snapshot commands (6)
│   ├── tool_commands.py    # Tool binding commands (15)
│   ├── super_pickaxe.py    # Super pickaxe commands (4)
│   ├── scripting.py        # Scripting commands (2)
│   └── general.py          # General WE commands (14)
└── helpers/
    ├── __init__.py
    ├── patterns.py         # Pattern building and validation
    ├── masks.py            # Mask building and validation
    ├── expressions.py      # Expression validation
    └── coordinates.py      # Coordinate utilities
```

#### 5. Resource Provider (`resources/provider.py`)
**Responsibilities:**
- Serve static reference documentation to AI
- Provide command syntax guides
- Offer example patterns and common recipes

**Resources to Provide:**
```
resources/
├── commands/
│   ├── all_commands.json       # Complete command reference
│   ├── by_category.json        # Commands organized by category
│   └── quick_reference.json    # Most common commands
├── syntax/
│   ├── patterns.md            # Pattern syntax guide
│   ├── masks.md               # Mask syntax guide
│   └── expressions.md         # Expression syntax guide
├── examples/
│   ├── basic_building.md      # Common building patterns
│   ├── terraforming.md        # Terrain manipulation recipes
│   └── advanced_techniques.md # Complex operations
└── reference/
    ├── block_types.json       # Valid block types
    ├── biome_types.json       # Valid biome types
    └── entity_types.json      # Valid entity types
```

#### 6. Configuration Manager (`config.py`)
**Responsibilities:**
- Load configuration from environment variables
- Validate configuration values
- Provide defaults
- Support configuration file override

**Configuration Parameters:**
```python
class Config:
    # RCON Settings
    rcon_host: str = "127.0.0.1"
    rcon_port: int = 25575
    rcon_password: str
    rcon_timeout: int = 30

    # Server Settings
    log_level: str = "INFO"
    max_command_length: int = 32500  # RCON limit
    enable_validation: bool = True

    # Safety Settings
    max_batch_size: int = 10
    coordinate_bounds: dict = None  # Optional safety limits
    dangerous_commands: list[str] = []  # Block list
```

---

## Technology Stack

### Core Technologies

#### Programming Language
**Python 3.10+**
- **Rationale:**
  - Official MCP SDK available in Python
  - Excellent library ecosystem for RCON and async operations
  - Easy to maintain and extend
  - FastMCP provides simplified MCP server development
  - Good match with reference implementation
- **Alternatives Considered:** TypeScript (good MCP support but more complex for this use case)

#### MCP Framework
**FastMCP (mcp>=1.0.0)**
- **Rationale:**
  - Simplified API for MCP server development
  - Built-in tool and resource management
  - Well-documented and actively maintained
  - Used in reference implementation
- **Benefits:**
  - Decorator-based tool registration
  - Automatic schema generation
  - Built-in stdio server support
  - Clean async/await patterns

#### RCON Library
**mcrcon (0.7.0+)**
- **Rationale:**
  - Pure Python, no external dependencies
  - Simple API: `MCRcon.command()`
  - Context manager support for connection handling
  - Proven reliability in reference implementation
- **Alternatives Considered:**
  - `mcipc`: More features but more complex
  - `rcon`: Less maintained
  - Custom implementation: Unnecessary reinvention

### Required Dependencies

```toml
[project]
name = "vibecraft-mcp"
version = "1.0.0"
description = "MCP server exposing WorldEdit commands to AI assistants"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",           # MCP SDK
    "mcrcon>=0.7.0",        # RCON client
    "pydantic>=2.0.0",      # Data validation
    "pydantic-settings>=2.0.0",  # Environment config
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",        # Testing framework
    "pytest-asyncio>=0.21.0",  # Async test support
    "pytest-mock>=3.11.0",  # Mocking utilities
    "black>=23.0.0",        # Code formatting
    "ruff>=0.1.0",          # Linting
    "mypy>=1.5.0",          # Type checking
]
```

### Development Tools

- **Version Control:** Git
- **Code Quality:** Black (formatting), Ruff (linting), MyPy (type checking)
- **Testing:** pytest with async support
- **Documentation:** Markdown for guides, JSON for structured data
- **Logging:** Python's built-in `logging` module with structured output

---

## Tool Design Strategy

### Philosophy: Hybrid Approach

We will implement a **three-tier tool strategy** that balances completeness, usability, and AI understanding:

#### Tier 1: Generic RCON Tool (Universal Fallback)
**Purpose:** Execute ANY command, including edge cases not covered by specialized tools

**Tool Design:**
```python
{
    "name": "rcon_command",
    "description": """Execute any Minecraft or WorldEdit command via RCON.

    This is a universal tool that can run ANY command. Use this when:
    - You need a command not covered by specialized tools
    - You want to execute a complex custom command
    - You're experimenting with new WorldEdit features

    WorldEdit Command Prefixes:
    - // for WorldEdit commands (e.g., //set stone)
    - / for vanilla Minecraft commands (e.g., /setblock 0 64 0 stone)

    Console Coordinate Format:
    - WorldEdit position commands use comma-separated coords: //pos1 X,Y,Z
    - Vanilla commands use space-separated coords: /setblock X Y Z block

    Examples:
    - rcon_command("//set minecraft:stone")
    - rcon_command("//sphere wool 5")
    - rcon_command("/fill 0 64 0 10 70 10 minecraft:glass")
    """,
    "inputSchema": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The exact command to execute (with or without leading /)"
            }
        },
        "required": ["command"]
    }
}
```

**Implementation Notes:**
- Minimal validation, maximum flexibility
- Command sanitization (remove dangerous shell characters)
- Return raw RCON response
- Log all commands for debugging

#### Tier 2: Categorized WorldEdit Tools (Semantic Organization)

**Purpose:** Provide structured, well-documented tools organized by WorldEdit functionality

**Design Principles:**
1. **One tool per major operation type** (not one per command)
2. **Rich descriptions with examples and syntax**
3. **Structured parameters with validation**
4. **Clear error messages**

**Category Structure (17 categories):**

##### 2.1 Selection Tools
```python
{
    "name": "worldedit_selection",
    "description": """Manage WorldEdit region selections.

    Operations:
    - set_positions: Define pos1 and pos2
    - expand: Grow selection in direction
    - contract: Shrink selection
    - shift: Move selection without resizing
    - size: Get selection dimensions
    - count: Count blocks matching mask

    Console Usage:
    Positions must be comma-separated: X,Y,Z
    """,
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["set_positions", "expand", "contract", "shift",
                         "outset", "inset", "size", "count", "distribute"]
            },
            "pos1": {
                "type": "object",
                "properties": {
                    "x": {"type": "integer"},
                    "y": {"type": "integer"},
                    "z": {"type": "integer"}
                }
            },
            "pos2": {
                "type": "object",
                "properties": {
                    "x": {"type": "integer"},
                    "y": {"type": "integer"},
                    "z": {"type": "integer"}
                }
            },
            # ... additional operation-specific parameters
        }
    }
}
```

##### 2.2 Region Operations Tools
```python
{
    "name": "worldedit_region",
    "description": """Perform operations on selected regions.

    Operations:
    - set: Fill with pattern
    - replace: Replace blocks matching mask
    - overlay: Add layer on top
    - walls: Create hollow walls
    - faces: Create all 6 faces
    - smooth: Smooth terrain
    - move: Relocate region contents
    - stack: Duplicate region

    Patterns:
    - Single: "stone", "oak_planks"
    - Random: "50%stone,30%diorite,20%granite"
    - States: "oak_stairs[facing=north,half=top]"

    Masks:
    - Block: "stone", "!air"
    - Expression: "=y<64"
    - Random: "%50" (affects 50% of blocks)
    """,
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["set", "replace", "overlay", "walls", "faces",
                         "smooth", "move", "stack", "hollow", "naturalize"]
            },
            "pattern": {"type": "string"},
            "mask": {"type": "string", "optional": True},
            # ... operation-specific parameters
        }
    }
}
```

##### 2.3 Generation Tools
```python
{
    "name": "worldedit_generate",
    "description": """Generate shapes and structures.

    Shapes:
    - sphere/hsphere: Solid or hollow sphere
    - cylinder/hcyl: Solid or hollow cylinder
    - pyramid/hpyramid: Solid or hollow pyramid
    - cone: Cone shape

    Advanced:
    - generate: Create shape from mathematical expression
    - feature: Place Minecraft features (trees, ores, etc.)
    - structure: Place Minecraft structures

    Expression Variables:
    - x, y, z: Current coordinates
    - Functions: sin, cos, sqrt, abs, min, max, etc.

    Example Expressions:
    - Sphere: "x^2+y^2+z^2<radius^2"
    - Torus: "(radius-sqrt(x^2+y^2))^2+z^2<tubeRadius^2"
    """,
    "inputSchema": {
        "type": "object",
        "properties": {
            "shape": {
                "type": "string",
                "enum": ["sphere", "hsphere", "cylinder", "hcyl",
                         "pyramid", "hpyramid", "cone", "generate"]
            },
            "pattern": {"type": "string"},
            "radius": {"type": "number", "optional": True},
            "height": {"type": "integer", "optional": True},
            "expression": {"type": "string", "optional": True},
            # ... shape-specific parameters
        }
    }
}
```

##### 2.4 Clipboard Tools
```python
{
    "name": "worldedit_clipboard",
    "description": """Copy, cut, paste, and manipulate clipboard.

    Operations:
    - copy: Copy selection to clipboard
    - cut: Cut selection to clipboard
    - paste: Paste clipboard at position
    - rotate: Rotate clipboard
    - flip: Flip clipboard along axis

    Paste Options:
    - -a: Skip air blocks
    - -o: Paste at original position
    - -s: Select pasted region
    - -e: Also paste entities
    - -b: Also paste biomes

    Rotation:
    - Angles: 90, 180, 270 degrees
    - Axes: Y (default), X, Z
    """,
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["copy", "cut", "paste", "rotate", "flip", "clear"]
            },
            "flags": {
                "type": "array",
                "items": {"type": "string"},
                "optional": True
            },
            # ... operation-specific parameters
        }
    }
}
```

##### 2.5 Brush Tools
```python
{
    "name": "worldedit_brush",
    "description": """Create and configure WorldEdit brushes.

    Note: Brushes require a player context and held item. From console/RCON,
    brushes have limited functionality. Use these commands to set up brushes
    for players to use manually.

    Brush Types:
    - sphere: Sphere brush
    - cylinder: Cylinder brush
    - smooth: Terrain smoother
    - gravity: Gravity brush
    - forest: Plant trees
    - raise/lower: Terrain elevation

    Brush Settings:
    - /mask <mask>: Set brush mask
    - /size <size>: Set brush radius
    - /range <range>: Set brush range
    - /material <pattern>: Set brush material
    """,
    "inputSchema": {
        "type": "object",
        "properties": {
            "brush_type": {"type": "string"},
            "pattern": {"type": "string", "optional": True},
            "size": {"type": "integer", "optional": True},
            # ... brush-specific parameters
        }
    }
}
```

##### 2.6 Utility Tools
```python
{
    "name": "worldedit_utility",
    "description": """Miscellaneous useful operations.

    Operations:
    - fill: Fill holes and pools
    - drain: Remove water/lava
    - fixwater/fixlava: Fix flowing liquids
    - removeabove/removebelow: Clear blocks above/below
    - replacenear: Replace blocks near position
    - snow/thaw: Simulate snow/ice
    - green: Convert dirt to grass
    - extinguish: Remove fire
    - butcher: Kill entities

    Each operation has specific parameters for radius, height, masks, etc.
    """,
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {"type": "string"},
            "radius": {"type": "integer", "optional": True},
            # ... operation-specific parameters
        }
    }
}
```

**Remaining Categories (implemented similarly):**
- `worldedit_navigation`: 7 commands for player movement
- `worldedit_biome`: 3 commands for biome operations
- `worldedit_chunk`: 3 commands for chunk management
- `worldedit_snapshot`: 6 commands for world restoration
- `worldedit_tool_commands`: 15 commands for tool binding
- `worldedit_super_pickaxe`: 4 commands for pickaxe modes
- `worldedit_scripting`: 2 commands for CraftScript execution
- `worldedit_general`: 14 commands for session management
- `worldedit_help`: 2 commands for documentation

#### Tier 3: Helper Utilities (Syntax Support)

**Purpose:** Assist AI in building valid patterns, masks, and expressions

##### 3.1 Pattern Helper
```python
{
    "name": "build_pattern",
    "description": """Build and validate WorldEdit pattern syntax.

    This helper constructs valid pattern strings from structured input.
    Use this when you need to create complex patterns.

    Pattern Types Supported:
    - single: Single block type
    - random: Weighted random blocks
    - random_state: Random block states
    - clipboard: Use clipboard as pattern
    - gradient: Linear gradient between blocks
    """,
    "inputSchema": {
        "type": "object",
        "properties": {
            "pattern_type": {
                "type": "string",
                "enum": ["single", "random", "random_state", "clipboard", "gradient"]
            },
            "blocks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "block": {"type": "string"},
                        "weight": {"type": "number", "optional": True},
                        "state": {"type": "object", "optional": True}
                    }
                }
            }
        }
    }
}
```

##### 3.2 Mask Helper
```python
{
    "name": "build_mask",
    "description": """Build and validate WorldEdit mask syntax.

    Combines multiple mask criteria with proper syntax.

    Mask Types:
    - block: Match specific blocks
    - expression: Mathematical conditions
    - region: Within selection
    - biome: Match biome type
    - offset: Blocks adjacent to others
    - random: Random percentage

    Operators:
    - Space: AND (intersection)
    - !: NOT (negation)
    """,
    "inputSchema": {
        "type": "object",
        "properties": {
            "masks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "value": {"type": "string"},
                        "negate": {"type": "boolean", "optional": True}
                    }
                }
            },
            "operator": {
                "type": "string",
                "enum": ["AND", "OR"],
                "default": "AND"
            }
        }
    }
}
```

##### 3.3 Expression Helper
```python
{
    "name": "validate_expression",
    "description": """Validate WorldEdit expression syntax.

    Checks mathematical expressions for:
    - Valid syntax
    - Available variables (x, y, z)
    - Supported functions
    - Balanced parentheses

    Returns:
    - valid: boolean
    - error: string (if invalid)
    - simplified: string (optimized expression)
    """,
    "inputSchema": {
        "type": "object",
        "properties": {
            "expression": {"type": "string"},
            "variables": {
                "type": "array",
                "items": {"type": "string"},
                "default": ["x", "y", "z"]
            }
        }
    }
}
```

##### 3.4 Coordinate Helper
```python
{
    "name": "coordinate_utils",
    "description": """Coordinate calculation and validation utilities.

    Operations:
    - calculate_bounds: Compute min/max from two points
    - offset: Calculate offset coordinates
    - distance: Distance between points
    - format_for_console: Format coords for WorldEdit console
    - validate_bounds: Check if coords within safety limits
    """,
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {"type": "string"},
            "coords": {"type": "array", "items": {"type": "integer"}},
            # ... operation-specific parameters
        }
    }
}
```

### Tool Naming Convention

**Pattern:** `{category}_{operation}` or `{category}_{subcategory}`

**Examples:**
- `rcon_command` - Generic RCON execution
- `worldedit_selection` - Selection operations category
- `worldedit_region` - Region operations category
- `worldedit_generate` - Shape generation category
- `build_pattern` - Pattern helper utility
- `build_mask` - Mask helper utility
- `server_info` - Server management

**Benefits:**
- Clear namespace separation
- Easy to understand tool purpose
- Searchable and filterable
- Consistent with MCP conventions

### Parameter Validation Strategy

**Validation Levels:**

1. **Schema-level (MCP):** Type checking via JSON Schema
2. **Application-level (Python):** Business logic validation using Pydantic
3. **Runtime-level (RCON):** Minecraft server validates actual commands

**Validation Implementation:**
```python
from pydantic import BaseModel, Field, validator

class RegionOperation(BaseModel):
    operation: Literal["set", "replace", "walls", "overlay"]
    pattern: str = Field(..., min_length=1, max_length=500)
    mask: Optional[str] = Field(None, max_length=500)

    @validator('pattern')
    def validate_pattern(cls, v):
        # Check pattern syntax
        if not Pattern.is_valid(v):
            raise ValueError(f"Invalid pattern syntax: {v}")
        return v

    @validator('mask')
    def validate_mask(cls, v):
        if v and not Mask.is_valid(v):
            raise ValueError(f"Invalid mask syntax: {v}")
        return v
```

### Error Handling Strategy

**Error Categories:**

1. **Connection Errors:** RCON connection failed
   - Retry with exponential backoff
   - Return clear error message to AI
   - Log for debugging

2. **Command Syntax Errors:** Invalid WorldEdit command
   - Parse RCON error response
   - Extract helpful error message
   - Suggest corrections if possible

3. **Permission Errors:** Insufficient permissions
   - Inform AI about permission requirements
   - Suggest alternative approaches

4. **Validation Errors:** Invalid parameters
   - Return structured validation errors
   - Include examples of valid input

**Implementation:**
```python
class VibeCraftError(Exception):
    """Base exception for VibeCraft errors"""
    pass

class RCONConnectionError(VibeCraftError):
    """RCON connection failed"""
    pass

class CommandExecutionError(VibeCraftError):
    """Command execution failed on server"""
    def __init__(self, command: str, server_response: str):
        self.command = command
        self.server_response = server_response
        super().__init__(f"Command failed: {command}\nServer: {server_response}")

class ValidationError(VibeCraftError):
    """Parameter validation failed"""
    pass
```

---

## Implementation Phases

### Phase 1: Foundation & MVP (Days 1-3)

**Goal:** Establish robust foundation and basic functionality

**Deliverables:**
1. ✅ Project structure and configuration
2. ✅ RCON connection manager with retry logic
3. ✅ Enhanced generic RCON tool
4. ✅ Server management tools
5. ✅ Basic error handling and logging
6. ✅ Configuration system (env vars + config file)
7. ✅ Unit tests for core components

**Tasks:**

**Day 1: Project Setup & Infrastructure**
- [ ] Set up project structure (directories, __init__.py files)
- [ ] Configure pyproject.toml with all dependencies
- [ ] Implement Config class with Pydantic settings
- [ ] Create RCONConnectionManager with connection pooling
- [ ] Add comprehensive logging
- [ ] Write unit tests for connection manager
- [ ] Document configuration options

**Day 2: Core Tools**
- [ ] Refactor existing rcon_command tool with better docs
- [ ] Implement server_info tool (list, status, stats)
- [ ] Add server_logs tool
- [ ] Create command sanitization utilities
- [ ] Implement basic validation framework
- [ ] Write unit tests for core tools
- [ ] Test end-to-end with real Minecraft server

**Day 3: Resource System**
- [ ] Design resource JSON structure
- [ ] Create ResourceProvider class
- [ ] Implement MCP resource endpoints
- [ ] Generate initial command reference JSON
- [ ] Create pattern syntax guide (Markdown)
- [ ] Create mask syntax guide (Markdown)
- [ ] Test resource retrieval from AI

**Success Criteria:**
- ✅ AI can execute any command via rcon_command
- ✅ Connection automatically recovers from failures
- ✅ AI can access command reference documentation
- ✅ All core components have unit tests
- ✅ Configuration is externalized and documented

---

### Phase 2: Essential WorldEdit Commands (Days 4-7)

**Goal:** Implement 80% of common use cases with categorized tools

**Deliverables:**
1. ✅ Selection tools (18 commands)
2. ✅ Region operation tools (19 commands)
3. ✅ Generation tools (13 commands)
4. ✅ Clipboard tools (12 commands)
5. ✅ Utility tools (16 commands)
6. ✅ Navigation tools (7 commands)
7. ✅ Comprehensive tool documentation
8. ✅ Integration tests for each category

**Tasks:**

**Day 4: Selection & Region Tools**
- [ ] Implement worldedit_selection tool
  - set_positions, expand, contract, shift, outset, inset
  - size, count, distribute operations
- [ ] Implement worldedit_region tool
  - set, replace, overlay, walls, faces
  - smooth, move, stack, hollow, naturalize
- [ ] Create comprehensive docstrings with examples
- [ ] Write integration tests with mock RCON
- [ ] Test with real WorldEdit commands

**Day 5: Generation & Clipboard Tools**
- [ ] Implement worldedit_generate tool
  - sphere, hsphere, cylinder, hcyl
  - pyramid, hpyramid, cone
  - generate (expression-based shapes)
- [ ] Implement worldedit_clipboard tool
  - copy, cut, paste
  - rotate, flip, clear
- [ ] Add flag parsing for clipboard operations
- [ ] Write integration tests
- [ ] Test complex generation operations

**Day 6: Utility & Navigation Tools**
- [ ] Implement worldedit_utility tool
  - fill, drain, fixwater, fixlava
  - removeabove, removebelow, replacenear
  - snow, thaw, green, extinguish, butcher
- [ ] Implement worldedit_navigation tool
  - unstuck, ascend, descend, ceil
  - thru, jumpto, up
- [ ] Write integration tests
- [ ] Test utility operations on server

**Day 7: Documentation & Refinement**
- [ ] Create comprehensive usage examples for each tool
- [ ] Generate API reference documentation
- [ ] Write "Getting Started" guide
- [ ] Create example workflows (building house, terraforming, etc.)
- [ ] Refactor common code patterns
- [ ] Performance optimization pass
- [ ] Fix bugs discovered during testing

**Success Criteria:**
- ✅ AI can perform all common building operations
- ✅ Selection, region, generation workflows are smooth
- ✅ Copy/paste operations work correctly
- ✅ Each tool has comprehensive examples
- ✅ Integration tests cover happy paths and edge cases

---

### Phase 3: Complete Command Coverage (Days 8-12)

**Goal:** Expose ALL 200+ WorldEdit commands

**Deliverables:**
1. ✅ Brush tools (30+ commands)
2. ✅ Biome tools (3 commands)
3. ✅ Chunk tools (3 commands)
4. ✅ Snapshot tools (6 commands)
5. ✅ Tool binding commands (15 commands)
6. ✅ Super pickaxe commands (4 commands)
7. ✅ Scripting commands (2 commands)
8. ✅ General/session commands (14 commands)
9. ✅ Help/search commands (2 commands)
10. ✅ Helper utilities (pattern, mask, expression, coordinate)

**Tasks:**

**Day 8: Brush & Biome Tools**
- [ ] Implement worldedit_brush tool
  - sphere, cylinder, smooth, gravity
  - forest, raise, lower, paint
  - deform, heightmap, snow, biome
  - morph, erode, dilate
- [ ] Implement brush configuration tools
  - mask, material, range, size, tracemask
- [ ] Implement worldedit_biome tool
  - biomelist, biomeinfo, setbiome
- [ ] Write tests and documentation

**Day 9: Chunk, Snapshot, & Tool Binding**
- [ ] Implement worldedit_chunk tool
  - chunkinfo, listchunks, delchunks
- [ ] Implement worldedit_snapshot tool
  - restore, list, use, before, after, sel
- [ ] Implement worldedit_tool_commands tool
  - All 15 tool binding commands
- [ ] Note player context requirements in docs
- [ ] Write tests and documentation

**Day 10: Pickaxe, Scripting, & General Commands**
- [ ] Implement worldedit_super_pickaxe tool
  - single, area, recursive modes
- [ ] Implement worldedit_scripting tool
  - cs (execute script), .s (execute last)
- [ ] Implement worldedit_general tool
  - undo, redo, clearhistory
  - limit, timeout, fast, perf, update
  - reorder, drawsel, world, watchdog, gmask
- [ ] Implement worldedit_help tool
  - help command, searchitem
- [ ] Write tests and documentation

**Day 11: Helper Utilities**
- [ ] Implement build_pattern helper
  - Parse and construct pattern syntax
  - Validate pattern components
  - Support all pattern types from research doc
- [ ] Implement build_mask helper
  - Parse and construct mask syntax
  - Support mask combinations
  - Validate mask expressions
- [ ] Implement validate_expression helper
  - Parse mathematical expressions
  - Validate function usage
  - Check variable references
- [ ] Implement coordinate_utils helper
  - Coordinate calculations
  - Format conversion
  - Bounds validation
- [ ] Write comprehensive tests

**Day 12: Integration & Validation**
- [ ] End-to-end testing of all 200+ commands
- [ ] Create comprehensive test suite
  - Unit tests: 80%+ coverage
  - Integration tests: All categories
  - End-to-end tests: Common workflows
- [ ] Performance testing
  - Measure command execution time
  - Test connection pool efficiency
  - Validate memory usage
- [ ] Create command compatibility matrix
- [ ] Fix bugs and edge cases
- [ ] Optimize slow operations

**Success Criteria:**
- ✅ ALL 200+ WorldEdit commands accessible
- ✅ All 17 categories implemented
- ✅ Helper utilities functional and tested
- ✅ Comprehensive test coverage
- ✅ Performance meets targets (<100ms overhead)

---

### Phase 4: Polish, Documentation & Deployment (Days 13-15)

**Goal:** Production-ready release with excellent documentation

**Deliverables:**
1. ✅ Complete user documentation
2. ✅ Developer documentation
3. ✅ Installation and setup guides
4. ✅ Example projects and tutorials
5. ✅ Error message improvements
6. ✅ Performance optimizations
7. ✅ Security hardening
8. ✅ Release package

**Tasks:**

**Day 13: Documentation**
- [ ] Write comprehensive README.md
  - Project overview and features
  - Quick start guide
  - Installation instructions
  - Configuration guide
- [ ] Create USER_GUIDE.md
  - Tool-by-tool documentation
  - Example use cases
  - Best practices
  - Troubleshooting
- [ ] Create DEVELOPER_GUIDE.md
  - Architecture overview
  - Code organization
  - Adding new tools
  - Testing guidelines
- [ ] Create API_REFERENCE.md
  - All tools with full schemas
  - Helper utilities
  - Configuration options
- [ ] Create EXAMPLES.md
  - 10+ practical examples
  - Common building patterns
  - Advanced techniques

**Day 14: Polish & Security**
- [ ] Improve error messages
  - Clear, actionable messages
  - Include suggestions for fixes
  - Link to relevant documentation
- [ ] Security hardening
  - Input sanitization review
  - Command injection prevention
  - Implement coordinate bounds checking
  - Add dangerous command blocklist
  - Rate limiting considerations
- [ ] Performance optimization
  - Profile slow operations
  - Optimize pattern/mask parsing
  - Improve connection pooling
  - Cache frequently accessed resources
- [ ] Code cleanup
  - Remove debug code
  - Improve code comments
  - Ensure consistent style
  - Run linters and type checkers

**Day 15: Packaging & Release**
- [ ] Create installation package
  - Setup.py / pyproject.toml finalization
  - Verify all dependencies
  - Test installation on clean system
- [ ] Create Docker image (optional)
  - Dockerfile for easy deployment
  - Docker Compose example
  - Multi-stage build optimization
- [ ] Create example configurations
  - Basic config (local server)
  - Advanced config (remote server, bounds checking)
  - Development config (debug logging)
- [ ] Write CHANGELOG.md
  - Version history
  - Feature additions
  - Bug fixes
- [ ] Create CONTRIBUTING.md
  - How to contribute
  - Code style guide
  - Testing requirements
  - PR process
- [ ] Final testing
  - Fresh installation test
  - All examples working
  - Documentation accuracy check
- [ ] Tag release v1.0.0

**Success Criteria:**
- ✅ Documentation is comprehensive and clear
- ✅ Installation is straightforward
- ✅ Security measures are in place
- ✅ Performance is optimized
- ✅ Ready for production use

---

## Testing Strategy

### Testing Pyramid

```
                    ┌─────────────┐
                    │   E2E Tests │  (10%)
                    │   5-10 tests │
                    └──────┬──────┘
                ┌──────────┴──────────┐
                │  Integration Tests  │  (30%)
                │     30-40 tests     │
                └──────────┬──────────┘
        ┌───────────────────┴────────────────────┐
        │           Unit Tests                   │  (60%)
        │          100+ tests                    │
        └────────────────────────────────────────┘
```

### Unit Tests (60% of tests)

**Scope:** Individual functions and classes in isolation

**Components to Test:**
1. **Configuration Manager**
   - Load from environment
   - Defaults application
   - Validation

2. **RCON Connection Manager**
   - Connection establishment
   - Reconnection logic
   - Command execution
   - Error handling
   - Connection pooling

3. **Tool Registry**
   - Tool registration
   - Tool lookup
   - Schema generation

4. **Helper Utilities**
   - Pattern parsing and building
   - Mask parsing and building
   - Expression validation
   - Coordinate calculations

5. **Validation Logic**
   - Parameter validation
   - Command sanitization
   - Bounds checking

**Testing Framework:**
```python
# tests/unit/test_rcon_manager.py
import pytest
from unittest.mock import Mock, patch
from vibecraft.rcon_manager import RCONConnectionManager

@pytest.fixture
def rcon_manager():
    return RCONConnectionManager(
        host="127.0.0.1",
        port=25575,
        password="test"
    )

def test_execute_command_success(rcon_manager):
    with patch('mcrcon.MCRcon') as mock_rcon:
        mock_rcon.return_value.__enter__.return_value.command.return_value = "Success"
        result = rcon_manager.execute_command("//set stone")
        assert result == "Success"

def test_execute_command_retry_on_failure(rcon_manager):
    with patch('mcrcon.MCRcon') as mock_rcon:
        # First call fails, second succeeds
        mock_rcon.return_value.__enter__.return_value.command.side_effect = [
            Exception("Connection lost"),
            "Success"
        ]
        result = rcon_manager.execute_command("//set stone")
        assert result == "Success"
        assert mock_rcon.call_count == 2
```

**Coverage Target:** 80%+ line coverage

---

### Integration Tests (30% of tests)

**Scope:** Multiple components working together, mocked RCON

**Test Scenarios:**

1. **Tool Execution Flow**
   - Tool receives parameters from AI
   - Parameters are validated
   - RCON command is generated
   - Command is executed via connection manager
   - Response is formatted and returned

2. **Multi-Command Sequences**
   - Set pos1 → set pos2 → execute region command
   - Copy → rotate → paste sequence
   - Generate shape → smooth → overlay

3. **Error Propagation**
   - RCON connection error → user-friendly error message
   - Invalid parameter → validation error with suggestions
   - Permission error → clear permission message

4. **Resource Access**
   - AI requests command reference
   - Resource is loaded and returned
   - Content is in expected format

**Testing Framework:**
```python
# tests/integration/test_worldedit_region.py
import pytest
from unittest.mock import Mock, AsyncMock
from vibecraft.tools.worldedit.region import RegionTool
from vibecraft.rcon_manager import RCONConnectionManager

@pytest.fixture
def mock_rcon():
    rcon = Mock(spec=RCONConnectionManager)
    rcon.execute_command = Mock(return_value="1000 blocks changed")
    return rcon

@pytest.fixture
def region_tool(mock_rcon):
    return RegionTool(rcon=mock_rcon)

@pytest.mark.asyncio
async def test_set_region_flow(region_tool, mock_rcon):
    # Test the complete flow of setting a region
    result = await region_tool.execute(
        operation="set",
        pos1={"x": 0, "y": 64, "z": 0},
        pos2={"x": 10, "y": 70, "z": 10},
        pattern="stone"
    )

    # Verify correct commands were issued
    assert mock_rcon.execute_command.call_count == 3
    calls = mock_rcon.execute_command.call_args_list
    assert "//pos1 0,64,0" in calls[0][0][0]
    assert "//pos2 10,70,10" in calls[1][0][0]
    assert "//set stone" in calls[2][0][0]

    # Verify result
    assert "1000 blocks changed" in result
```

**Coverage Target:** All tool categories, common workflows

---

### End-to-End Tests (10% of tests)

**Scope:** Full system with real Minecraft server (or realistic mock)

**Test Scenarios:**

1. **Complete Building Workflow**
   ```python
   async def test_build_house_workflow():
       # Set up region
       await worldedit_selection.set_positions(...)

       # Build foundation
       await worldedit_region.set(pattern="stone")

       # Build walls
       await worldedit_region.walls(pattern="oak_planks")

       # Add roof
       await worldedit_generate.pyramid(...)

       # Verify structure exists (query blocks)
       result = await rcon_command("testforblock ...")
       assert "Found" in result
   ```

2. **Clipboard Operations**
   ```python
   async def test_copy_rotate_paste():
       # Build original structure
       await worldedit_region.set(...)

       # Copy
       await worldedit_clipboard.copy()

       # Rotate
       await worldedit_clipboard.rotate(angle=90)

       # Move and paste
       await worldedit_clipboard.paste(offset=[20, 0, 0])

       # Verify copy exists at new location
       ...
   ```

3. **Error Handling**
   ```python
   async def test_connection_recovery():
       # Execute command successfully
       result1 = await rcon_command("list")
       assert "players" in result1.lower()

       # Simulate connection loss
       stop_minecraft_server()

       # Try command (should fail gracefully)
       result2 = await rcon_command("list")
       assert "connection error" in result2.lower()

       # Restart server
       start_minecraft_server()

       # Verify recovery
       result3 = await rcon_command("list")
       assert "players" in result3.lower()
   ```

**Test Environment:**
- Docker container with Minecraft server
- WorldEdit plugin pre-installed
- RCON enabled
- Automated startup/teardown scripts

**Coverage Target:** Critical user paths, error scenarios

---

### Testing Tools & Infrastructure

**Testing Stack:**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = """
    -v
    --cov=vibecraft
    --cov-report=html
    --cov-report=term
    --cov-fail-under=80
    --asyncio-mode=auto
"""

[tool.coverage.run]
source = ["vibecraft"]
omit = ["tests/*", "venv/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

**Mock Strategies:**

1. **RCON Mocking:**
   ```python
   @pytest.fixture
   def mock_rcon_responses():
       return {
           "//set stone": "1000 blocks changed",
           "//pos1 0,64,0": "First position set to (0, 64, 0)",
           "list": "There are 0 of a max 20 players online:",
           # ... more responses
       }

   @pytest.fixture
   def mock_rcon(mock_rcon_responses):
       def mock_command(cmd):
           return mock_rcon_responses.get(cmd, f"Unknown command: {cmd}")

       rcon = Mock(spec=RCONConnectionManager)
       rcon.execute_command = Mock(side_effect=mock_command)
       return rcon
   ```

2. **Minecraft Server Mocking (for E2E):**
   ```python
   class MockMinecraftServer:
       def __init__(self):
           self.world = {}  # Block storage
           self.selection = None

       def execute(self, command):
           if command.startswith("//set"):
               return self._handle_set(command)
           elif command.startswith("//pos"):
               return self._handle_pos(command)
           # ... handle all commands
   ```

**Continuous Integration:**
- GitHub Actions workflow
- Run tests on every PR
- Test on Python 3.10, 3.11, 3.12
- Test on Ubuntu, macOS
- Automated coverage reporting

---

## Configuration & Deployment

### Configuration System

#### Environment Variables
```bash
# RCON Connection
RCON_HOST=127.0.0.1          # Minecraft server host
RCON_PORT=25575              # RCON port
RCON_PASSWORD=your_password  # RCON password
RCON_TIMEOUT=30              # Command timeout in seconds

# Server Settings
LOG_LEVEL=INFO               # Logging level (DEBUG, INFO, WARNING, ERROR)
MAX_COMMAND_LENGTH=32500     # Maximum RCON command length
ENABLE_VALIDATION=true       # Enable parameter validation

# Safety Settings
MAX_BATCH_SIZE=10            # Maximum commands in batch
COORDINATE_MIN_X=-1000       # Minimum X coordinate (optional)
COORDINATE_MAX_X=1000        # Maximum X coordinate (optional)
COORDINATE_MIN_Y=-64         # Minimum Y coordinate (optional)
COORDINATE_MAX_Y=320         # Maximum Y coordinate (optional)
COORDINATE_MIN_Z=-1000       # Minimum Z coordinate (optional)
COORDINATE_MAX_Z=1000        # Maximum Z coordinate (optional)

# Feature Flags
ENABLE_DANGEROUS_COMMANDS=false  # Allow regen, delchunks, etc.
ENABLE_SCRIPTING=false           # Allow CraftScript execution
```

#### Configuration File (Optional)
```yaml
# vibecraft-config.yaml
rcon:
  host: 127.0.0.1
  port: 25575
  password: ${RCON_PASSWORD}  # Can reference env vars
  timeout: 30
  max_retries: 3
  retry_delay: 1.0

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: vibecraft-mcp.log

validation:
  enabled: true
  strict_mode: false  # Fail on warnings

safety:
  coordinate_bounds:
    x: [-1000, 1000]
    y: [-64, 320]
    z: [-1000, 1000]

  blocked_commands:
    - "stop"
    - "restart"
    - "/op"
    - "/deop"

  dangerous_commands_enabled: false
  scripting_enabled: false

performance:
  connection_pool_size: 3
  command_queue_size: 100
  max_batch_size: 10
```

#### Configuration Loading (Pydantic)
```python
# vibecraft/config.py
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List

class CoordinateBounds(BaseSettings):
    min_x: Optional[int] = None
    max_x: Optional[int] = None
    min_y: Optional[int] = -64
    max_y: Optional[int] = 320
    min_z: Optional[int] = None
    max_z: Optional[int] = None

class RCONSettings(BaseSettings):
    host: str = Field(default="127.0.0.1", env="RCON_HOST")
    port: int = Field(default=25575, env="RCON_PORT")
    password: str = Field(env="RCON_PASSWORD")
    timeout: int = Field(default=30, env="RCON_TIMEOUT")
    max_retries: int = 3
    retry_delay: float = 1.0

class SafetySettings(BaseSettings):
    coordinate_bounds: CoordinateBounds = CoordinateBounds()
    blocked_commands: List[str] = Field(default_factory=lambda: ["stop", "restart"])
    dangerous_commands_enabled: bool = False
    scripting_enabled: bool = False

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        yaml_file="vibecraft-config.yaml",
        yaml_file_encoding="utf-8",
    )

    rcon: RCONSettings
    safety: SafetySettings
    log_level: str = "INFO"
    enable_validation: bool = True
    max_batch_size: int = 10
```

### Installation Methods

#### Method 1: pip install (Recommended)
```bash
# Install from PyPI (when published)
pip install vibecraft-mcp

# Or install from source
git clone https://github.com/yourusername/vibecraft.git
cd vibecraft/mcp-server
pip install -e .

# Set up configuration
export RCON_PASSWORD="your_password"
export RCON_HOST="127.0.0.1"

# Run the server
python -m vibecraft.server
```

#### Method 2: uv (Fast Python package manager)
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create project
uv init vibecraft-project
cd vibecraft-project

# Add vibecraft-mcp
uv add vibecraft-mcp

# Configure
echo "RCON_PASSWORD=your_password" > .env

# Run
uv run python -m vibecraft.server
```

#### Method 3: Docker (Isolated environment)
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install -e .

# Copy source
COPY vibecraft ./vibecraft

# Configuration
ENV RCON_HOST=minecraft-server
ENV RCON_PORT=25575

CMD ["python", "-m", "vibecraft.server"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  minecraft:
    image: itzg/minecraft-server
    environment:
      EULA: "TRUE"
      TYPE: "PAPER"
      VERSION: "1.21"
      ENABLE_RCON: "true"
      RCON_PASSWORD: "minecraft"
      RCON_PORT: 25575
    volumes:
      - ./minecraft-data:/data
      - ./plugins:/plugins  # Pre-install WorldEdit here
    ports:
      - "25565:25565"
      - "25575:25575"
    networks:
      - vibecraft-net

  vibecraft-mcp:
    build: ./mcp-server
    environment:
      RCON_HOST: minecraft
      RCON_PORT: 25575
      RCON_PASSWORD: minecraft
    depends_on:
      - minecraft
    networks:
      - vibecraft-net
    stdin_open: true
    tty: true

networks:
  vibecraft-net:
```

### Claude Desktop Integration

#### Configuration File Location
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

#### Configuration Entry
```json
{
  "mcpServers": {
    "vibecraft": {
      "command": "python",
      "args": ["-m", "vibecraft.server"],
      "env": {
        "RCON_HOST": "127.0.0.1",
        "RCON_PORT": "25575",
        "RCON_PASSWORD": "your_password_here",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

#### Alternative: Using uv
```json
{
  "mcpServers": {
    "vibecraft": {
      "command": "uv",
      "args": ["run", "vibecraft-mcp"],
      "env": {
        "RCON_HOST": "127.0.0.1",
        "RCON_PORT": "25575",
        "RCON_PASSWORD": "your_password_here"
      }
    }
  }
}
```

#### Verification
1. Restart Claude Desktop
2. Open new conversation
3. Look for "vibecraft" in available tools
4. Test with: "What tools do you have available?"

### Deployment Checklist

- [ ] **Prerequisites Installed**
  - Python 3.10+
  - pip or uv
  - Minecraft server with WorldEdit
  - RCON enabled on Minecraft server

- [ ] **Configuration Set**
  - Environment variables configured
  - RCON credentials correct
  - Optional: Config file created
  - Optional: Safety bounds configured

- [ ] **Installation Complete**
  - Package installed via pip/uv
  - Dependencies resolved
  - No import errors

- [ ] **Connection Test**
  - Test RCON connection manually
  - Verify WorldEdit is loaded
  - Test simple command (e.g., `list`)

- [ ] **MCP Server Test**
  - Start server manually
  - Check for startup errors
  - Verify tools are registered
  - Test resource access

- [ ] **Claude Integration**
  - Configuration file updated
  - Claude Desktop restarted
  - Tools visible in Claude
  - Test simple command via Claude

- [ ] **End-to-End Test**
  - Ask Claude to set region and fill with blocks
  - Verify blocks appear in Minecraft
  - Check for errors in logs

### Troubleshooting Guide

**Problem:** RCON connection refused
- **Check:** Is Minecraft server running?
- **Check:** Is RCON enabled in server.properties?
- **Check:** Is RCON port correct (default 25575)?
- **Check:** Firewall blocking connection?
- **Test:** `telnet localhost 25575`

**Problem:** Authentication failed
- **Check:** RCON password matches server.properties
- **Check:** Password has no special characters causing issues
- **Fix:** Update RCON_PASSWORD environment variable

**Problem:** Claude doesn't see tools
- **Check:** Configuration file location correct
- **Check:** JSON syntax is valid
- **Check:** Server path is correct
- **Fix:** Restart Claude Desktop after config changes

**Problem:** Commands fail with permission errors
- **Check:** Player executing commands has WorldEdit permissions
- **Check:** Console has operator status
- **Fix:** Grant permissions in permissions plugin or ops.json

**Problem:** Commands timeout
- **Check:** Minecraft server is responsive
- **Check:** WorldEdit isn't overloaded with huge operation
- **Fix:** Increase RCON_TIMEOUT
- **Fix:** Break large operations into smaller chunks

---

## Documentation Requirements

### User Documentation

#### 1. README.md
**Sections:**
- Project overview and features
- Quick start (5-minute setup)
- Installation instructions
- Basic usage examples
- Links to detailed docs
- Contribution guidelines
- License information

#### 2. QUICK_START.md
**Sections:**
- Prerequisites
- Installation steps
- Configuration
- First command via Claude
- Simple building example
- Next steps

#### 3. USER_GUIDE.md
**Sections:**
- Understanding the MCP server
- Tool categories overview
- Using each tool category (with examples)
- Pattern syntax guide
- Mask syntax guide
- Expression syntax guide
- Common workflows
- Best practices
- Tips and tricks
- Troubleshooting

#### 4. API_REFERENCE.md
**Sections:**
- Complete tool listing
- Each tool with:
  - Name
  - Description
  - Parameters (with types and constraints)
  - Return value format
  - Examples
  - Related tools
- Helper utilities reference
- Resource listing

#### 5. EXAMPLES.md
**Sections:**
- Example 1: Building a simple structure
- Example 2: Terraforming terrain
- Example 3: Copy and paste operations
- Example 4: Using patterns and masks
- Example 5: Creating complex shapes with expressions
- Example 6: Working with schematics
- Example 7: Batch operations
- Example 8: Error handling
- Example 9: Building a house (end-to-end)
- Example 10: Creating a landscape (advanced)

#### 6. FAQ.md
**Sections:**
- General questions
- Installation and setup
- Usage and commands
- Troubleshooting
- Performance
- Security

### Developer Documentation

#### 1. DEVELOPER_GUIDE.md
**Sections:**
- Architecture overview
- Code organization
- Key components explanation
- Adding a new tool (step-by-step)
- Adding a new resource
- Extending validation
- Testing guidelines
- Code style guide
- Debugging tips

#### 2. CONTRIBUTING.md
**Sections:**
- How to contribute
- Setting up development environment
- Code style guidelines
- Testing requirements
- Submitting PRs
- Issue reporting guidelines

#### 3. ARCHITECTURE.md
**Sections:**
- System architecture diagram
- Component responsibilities
- Data flow diagrams
- Tool execution flow
- RCON communication flow
- Error handling flow
- Resource provision flow
- Design decisions and rationale

#### 4. TESTING.md
**Sections:**
- Testing philosophy
- Test structure
- Running tests
- Writing unit tests
- Writing integration tests
- Writing E2E tests
- Mocking strategies
- Coverage requirements

### Resource Documentation (Embedded)

#### 1. resources/README.md
**Purpose:** Overview of all resources available to AI

#### 2. resources/commands/README.md
**Purpose:** Explain command JSON structure

#### 3. resources/syntax/patterns.md
**Purpose:** Complete pattern syntax guide with examples

#### 4. resources/syntax/masks.md
**Purpose:** Complete mask syntax guide with examples

#### 5. resources/syntax/expressions.md
**Purpose:** Complete expression syntax guide with examples

---

## Risk Analysis & Mitigation

### Technical Risks

#### Risk 1: RCON Connection Instability
**Severity:** High
**Probability:** Medium
**Impact:** Commands fail, poor user experience

**Mitigation:**
- Implement robust retry logic with exponential backoff
- Connection pooling for redundancy
- Automatic reconnection on connection loss
- Clear error messages to AI when connection fails
- Health check endpoint to monitor connection status

#### Risk 2: Command Length Limits
**Severity:** Medium
**Probability:** Medium
**Impact:** Large patterns/expressions may fail

**Mitigation:**
- Validate command length before sending (RCON limit: ~32KB)
- Break large operations into multiple commands
- Warn AI when command is approaching limit
- Provide batch execution helper for complex operations

#### Risk 3: WorldEdit Console Compatibility
**Severity:** High
**Probability:** Low-Medium
**Impact:** Some commands may not work from console

**Mitigation:**
- Thorough testing of all 200+ commands from RCON
- Document which commands require player context
- Provide workarounds using equivalent console commands
- Clear error messages when player context is needed

#### Risk 4: Performance Impact on Minecraft Server
**Severity:** Medium
**Probability:** Medium
**Impact:** Server lag during large operations

**Mitigation:**
- Implement rate limiting in MCP server
- Warn AI about performance impact of large operations
- Suggest breaking large builds into chunks
- Provide async operation tracking (when supported by WorldEdit)
- Document performance best practices

#### Risk 5: Version Compatibility
**Severity:** Medium
**Probability:** Medium
**Impact:** Commands may differ across WorldEdit versions

**Mitigation:**
- Target WorldEdit 7.3+ (latest stable)
- Document version requirements clearly
- Version detection in server (query WorldEdit version)
- Graceful degradation for unavailable commands
- Maintain compatibility matrix

### Security Risks

#### Risk 6: Command Injection
**Severity:** Critical
**Probability:** Low (with mitigations)
**Impact:** Arbitrary code execution on server

**Mitigation:**
- Strict input sanitization
- Parameterized command construction
- No shell interpolation
- Whitelist of allowed characters
- Command pattern validation
- Security audit of all input paths

#### Risk 7: Unauthorized Access
**Severity:** Critical
**Probability:** Low
**Impact:** Unauthorized world manipulation

**Mitigation:**
- RCON password in environment variables (not code)
- No password logging
- Secure configuration storage
- Document security best practices
- Recommend firewall rules (RCON not exposed to internet)

#### Risk 8: Destructive Operations
**Severity:** High
**Probability:** Medium
**Impact:** Accidental world destruction

**Mitigation:**
- Coordinate bounds checking (optional)
- Dangerous command blocklist (optional)
- Clear warnings in tool descriptions
- Require confirmation for destructive ops (future enhancement)
- Document backup/snapshot best practices
- Undo history integration

#### Risk 9: Resource Exhaustion
**Severity:** Medium
**Probability:** Low
**Impact:** MCP server or Minecraft server crashes

**Mitigation:**
- Command rate limiting
- Maximum batch size limits
- Timeout on long-running operations
- Memory usage monitoring
- CPU usage monitoring
- Resource cleanup on errors

### Operational Risks

#### Risk 10: Complex Tool Usage by AI
**Severity:** Medium
**Probability:** Medium
**Impact:** AI uses tools incorrectly, poor results

**Mitigation:**
- Extremely detailed tool descriptions
- Multiple examples per tool
- Clear parameter documentation
- Validation with helpful error messages
- Resource documentation for syntax help
- "Learn by example" approach in docs

#### Risk 11: Documentation Drift
**Severity:** Low
**Probability:** High (without process)
**Impact:** Outdated docs cause confusion

**Mitigation:**
- Documentation as code (in repo)
- Documentation review in PR process
- Auto-generated API reference where possible
- Version documentation with code
- Regular documentation audits

#### Risk 12: Maintenance Burden
**Severity:** Medium
**Probability:** Medium
**Impact:** Project becomes unmaintainable

**Mitigation:**
- Clean, modular architecture
- Comprehensive test coverage
- Clear code documentation
- Contribution guidelines
- Automated testing and linting
- Regular dependency updates

---

## Success Criteria

### Functional Requirements

✅ **Complete Command Coverage**
- All 200+ WorldEdit commands accessible
- All 17 command categories implemented
- All pattern types supported
- All mask types supported
- All expression functions available

✅ **Robust RCON Communication**
- Connection established and maintained
- Automatic reconnection on failure
- Command execution with retry logic
- Response parsing and error handling
- Batch command support

✅ **Comprehensive Tool Design**
- Generic RCON tool for flexibility
- Categorized tools for common operations
- Helper utilities for syntax support
- Clear, detailed descriptions
- Structured parameter schemas
- Validation with helpful errors

✅ **Resource Provision**
- Command reference accessible to AI
- Pattern syntax guide available
- Mask syntax guide available
- Expression syntax guide available
- Example workflows and recipes

### Quality Requirements

✅ **Testing**
- 80%+ unit test coverage
- Integration tests for all categories
- E2E tests for critical workflows
- All tests passing
- CI/CD pipeline configured

✅ **Documentation**
- README with quick start
- Comprehensive user guide
- Complete API reference
- Developer guide
- 10+ practical examples
- Troubleshooting guide
- FAQ

✅ **Code Quality**
- Passes all linters (ruff)
- Formatted consistently (black)
- Type-checked (mypy)
- No critical security issues
- Clear code comments
- Modular architecture

✅ **Performance**
- <100ms overhead for simple commands
- <500ms for complex operations
- <30s for largest operations
- No memory leaks
- Efficient resource usage

✅ **Security**
- Input sanitization implemented
- Command injection prevented
- No sensitive data in logs
- Secure configuration management
- Optional safety bounds checking

### User Experience Requirements

✅ **Installation**
- Single command install (`pip install vibecraft-mcp`)
- Clear installation instructions
- Works on macOS, Linux, Windows
- Minimal dependencies

✅ **Configuration**
- Simple environment variable setup
- Optional advanced configuration file
- Clear configuration documentation
- Sensible defaults

✅ **Claude Integration**
- Works with Claude Desktop
- Tools appear correctly
- Clear tool descriptions
- Resources accessible
- Smooth user experience

✅ **AI Usability**
- AI understands tool purposes
- AI can construct correct commands
- AI receives helpful error messages
- AI can access syntax help
- AI can complete common workflows

✅ **Reliability**
- Graceful error handling
- Clear error messages
- Automatic recovery from failures
- Stable performance
- No crashes or hangs

---

## Open Questions

### Technical Questions

**Q1:** Should we implement a command queue with priority?
- **Context:** Some commands (like `//undo`) should execute immediately
- **Options:**
  - A) Simple FIFO queue
  - B) Priority queue (interactive > automated)
  - C) No queue, direct execution
- **Recommendation:** Start with C, add queue in future if needed
- **Decision:** TBD (Cody review)

**Q2:** How should we handle long-running operations?
- **Context:** Large smooth operations can take minutes
- **Options:**
  - A) Block until complete
  - B) Return immediately with operation ID (if WE supports)
  - C) Timeout and suggest breaking into chunks
- **Recommendation:** A for MVP, with timeout and helpful error
- **Decision:** TBD (Cody review)

**Q3:** Should we expose raw schematics file operations?
- **Context:** Schematics are files on server filesystem
- **Options:**
  - A) Only support load/save by name (existing files)
  - B) Also support listing files, checking existence
  - C) Also support upload/download of schematic files
- **Recommendation:** B for MVP (read-only filesystem access)
- **Decision:** TBD (Cody review)

**Q4:** How to handle player-context-required commands?
- **Context:** Some commands (brushes, navigation) need player
- **Options:**
  - A) Document as not supported from console
  - B) Try to execute, let server error
  - C) Implement "execute as player" wrapper
- **Recommendation:** A for MVP, B as fallback
- **Decision:** TBD (Cody review)

### Architecture Questions

**Q5:** Should we use a plugin instead of RCON?
- **Context:** Custom plugin could provide better API
- **Pros:** Structured responses, better error handling, async support
- **Cons:** More complex, requires Java, harder to install
- **Recommendation:** RCON for MVP, plugin as future enhancement
- **Decision:** TBD (Cody review)

**Q6:** Should tools be granular (one per command) or grouped (by category)?
- **Context:** Trade-off between tool count and flexibility
- **Options:**
  - A) 200+ individual tools (one per command)
  - B) 17 category tools (grouped)
  - C) Hybrid (generic + categories + common)
- **Recommendation:** C (hybrid approach proposed in this plan)
- **Decision:** TBD (Cody review)

**Q7:** Should we provide a FastMCP or standard MCP implementation?
- **Context:** FastMCP is simpler, standard MCP is more flexible
- **Current:** Using FastMCP (follows reference)
- **Recommendation:** FastMCP for ease of development
- **Decision:** TBD (Cody review)

### Feature Questions

**Q8:** Should we implement a "preview" mode?
- **Context:** Let AI see what would change before executing
- **Options:**
  - A) No preview (execute immediately)
  - B) Use WorldEdit's preview (if available)
  - C) Implement custom preview (show affected blocks)
- **Recommendation:** A for MVP, B as future enhancement
- **Decision:** TBD (Cody review)

**Q9:** Should we support multi-server connections?
- **Context:** User might want to control multiple servers
- **Options:**
  - A) Single server only
  - B) Multiple servers, switch with command
  - C) Multiple servers, specify in each command
- **Recommendation:** A for MVP, B as future enhancement
- **Decision:** TBD (Cody review)

**Q10:** Should we add visualization/screenshot capabilities?
- **Context:** AI could request screenshots to verify builds
- **Options:**
  - A) No visualization (out of scope)
  - B) Integration with Minecraft screenshot mods
  - C) Custom rendering using world data
- **Recommendation:** A for MVP (very complex to add)
- **Decision:** TBD (Cody review)

### Documentation Questions

**Q11:** Should we provide video tutorials?
- **Context:** Some users prefer video over text
- **Recommendation:** Text docs for MVP, videos as future enhancement
- **Decision:** TBD (Cody review)

**Q12:** Should we create a gallery of AI-built structures?
- **Context:** Showcase what's possible, inspire users
- **Recommendation:** Yes, as part of marketing/community building
- **Decision:** TBD (Cody review)

---

## Appendix: Command Mapping

### Complete Command Coverage Matrix

| Category | Commands | Tool Name | Priority |
|----------|----------|-----------|----------|
| General | 14 | `worldedit_general` | P2 |
| Navigation | 7 | `worldedit_navigation` | P3 |
| Selection | 18 | `worldedit_selection` | P1 |
| Region | 19 | `worldedit_region` | P1 |
| Generation | 13 | `worldedit_generate` | P1 |
| Clipboard | 12 | `worldedit_clipboard` | P2 |
| Tools | 15 | `worldedit_tool_commands` | P3 |
| Brushes | 30+ | `worldedit_brush` | P3 |
| Super Pickaxe | 4 | `worldedit_super_pickaxe` | P3 |
| Biome | 3 | `worldedit_biome` | P3 |
| Chunk | 3 | `worldedit_chunk` | P3 |
| Snapshot | 6 | `worldedit_snapshot` | P3 |
| Scripting | 2 | `worldedit_scripting` | P4 |
| Utility | 16 | `worldedit_utility` | P2 |
| Search/Help | 2 | `worldedit_help` | P2 |

**Priority Levels:**
- **P1 (Phase 2):** Core building functionality (80% of use cases)
- **P2 (Phase 2-3):** Common operations
- **P3 (Phase 3):** Advanced features
- **P4 (Phase 3):** Edge cases and rarely used features

---

## Conclusion

This implementation plan provides a comprehensive roadmap for building the VibeCraft MCP server. The hybrid approach balances completeness (generic RCON tool), usability (categorized tools), and AI understanding (helpers and resources).

### Key Decisions Made:
1. ✅ **Hybrid tool strategy:** Generic + Categorized + Helpers
2. ✅ **Python with FastMCP:** Matches reference, simple development
3. ✅ **mcrcon library:** Proven, reliable RCON communication
4. ✅ **Phased implementation:** MVP → Core → Complete → Polish
5. ✅ **Comprehensive testing:** Unit + Integration + E2E
6. ✅ **Rich documentation:** Users, developers, and AI assistants

### Next Steps:
1. **Cody reviews this plan** (identifies issues, suggests improvements)
2. **Steve incorporates feedback** into v2 plan
3. **Implementation begins** following the phased approach
4. **Cody performs code review** after implementation
5. **Steve addresses code review feedback**
6. **Release v1.0.0** 🚀

### Timeline Summary:
- **Phase 1 (MVP):** Days 1-3
- **Phase 2 (Core):** Days 4-7
- **Phase 3 (Complete):** Days 8-12
- **Phase 4 (Polish):** Days 13-15
- **Total:** 11-15 business days

### Success Metrics:
- ✅ All 200+ commands accessible
- ✅ Smooth AI experience
- ✅ 80%+ test coverage
- ✅ Comprehensive documentation
- ✅ Easy installation and setup
- ✅ Production-ready quality

---

**Document Status:** Ready for Review
**Reviewer:** Cody (Senior Engineer)
**Next Action:** Review meeting to discuss open questions and refine plan
