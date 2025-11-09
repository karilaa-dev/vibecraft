# Server.py Refactoring Plan

**Status**: 🚧 In Progress
**Priority**: CRITICAL
**Size**: 5,927 lines → Target: <500 lines per module

## Problem

`mcp-server/src/vibecraft/server.py` is a monolithic 5,900+ line file that bundles:
- Transport setup
- Tool definitions (46 tools)
- Resource loading
- Formatting/presentation
- Workflow orchestration
- Logging/bootstrap
- Business logic for each tool

This makes it extremely difficult to:
- Reason about side effects
- Reuse logic across tools
- Add comprehensive tests
- Navigate and maintain the codebase

## Proposed Module Structure

```
mcp-server/src/vibecraft/
├── server.py                    # Thin entrypoint (<500 lines)
│   ├── Server initialization
│   ├── Tool/resource registration
│   └── Main async loop
│
├── tools/                       # Tool handlers (one file per category)
│   ├── __init__.py
│   ├── worldedit_core.py       # pos1/pos2, set, replace, walls, etc.
│   ├── worldedit_generation.py # sphere, cylinder, pyramid
│   ├── worldedit_clipboard.py  # copy, cut, paste
│   ├── worldedit_advanced.py   # deform, vegetation, terrain_advanced
│   ├── spatial_analysis.py     # analyze_placement_area, spatial_awareness_scan
│   ├── furniture.py            # furniture_lookup, place_furniture
│   ├── patterns.py             # building_pattern_lookup, place_building_pattern
│   ├── terrain.py              # terrain_analyzer, generate/texture/smooth_terrain
│   ├── geometry.py             # calculate_shape, calculate_window_spacing
│   ├── validation.py           # validate_pattern/mask, check_symmetry, analyze_lighting
│   └── workflow.py             # workflow_status, workflow_advance
│
├── resources/                   # Resource providers
│   ├── __init__.py
│   ├── guides.py               # Pattern/mask/expression/coordinate guides
│   ├── catalogs.py             # Furniture/pattern catalogs
│   └── minecraft_data.py       # Item/block data loaders
│
├── formatters/                  # Output formatting
│   ├── __init__.py
│   ├── text.py                 # Plain text formatting
│   ├── json.py                 # JSON formatting
│   └── markdown.py             # Markdown/rich formatting
│
├── core/                        # Existing core modules (already extracted)
│   ├── rcon_manager.py         # ✅ Already modular
│   ├── config.py               # ✅ Already modular
│   ├── sanitizer.py            # ✅ Already modular
│   ├── terrain.py              # ✅ Already modular
│   ├── building_tools.py       # ✅ Already modular
│   └── ...
│
└── logging_setup.py            # Logging configuration (just extracted!)
```

## Refactoring Phases

### Phase 1: Extract Tool Handlers (Priority 1)

**Goal**: Move tool implementations out of server.py into focused modules

#### Step 1.1: Create tools/ directory structure
```bash
mkdir -p mcp-server/src/vibecraft/tools
touch mcp-server/src/vibecraft/tools/__init__.py
```

#### Step 1.2: Define Tool Handler Interface
```python
# tools/__init__.py
from typing import Dict, Any, List, Protocol
from mcp.types import TextContent

class ToolHandler(Protocol):
    """Interface for tool handlers"""
    async def handle(
        self,
        arguments: Dict[str, Any],
        rcon: RCONManager,
        config: VibeCraftConfig,
        logger: logging.Logger
    ) -> List[TextContent]:
        """
        Handle tool execution.

        Args:
            arguments: Tool arguments
            rcon: RCON manager instance
            config: Server configuration
            logger: Logger instance

        Returns:
            List of TextContent responses
        """
        ...
```

#### Step 1.3: Extract first tool module (worldedit_core.py)

Move ALL core WorldEdit tools to `tools/worldedit_core.py`:
- worldedit_selection (pos1, pos2, size, etc.)
- worldedit_region (set, replace, walls, etc.)
- worldedit_history (undo, redo)
- worldedit_utility (fill, drain, etc.)

**Example structure**:
```python
# tools/worldedit_core.py
from typing import Dict, Any, List
from mcp.types import TextContent
import logging

logger = logging.getLogger(__name__)

async def handle_worldedit_selection(
    arguments: Dict[str, Any],
    rcon,
    config,
    logger
) -> List[TextContent]:
    """Handle worldedit_selection tool"""
    command = arguments.get("command")
    # ... implementation ...
    return [TextContent(type="text", text=result)]

async def handle_worldedit_region(arguments, rcon, config, logger) -> List[TextContent]:
    """Handle worldedit_region tool"""
    # ... implementation ...
    pass

# Export handler registry
TOOL_HANDLERS = {
    "worldedit_selection": handle_worldedit_selection,
    "worldedit_region": handle_worldedit_region,
    # ...
}
```

**In server.py**, replace the giant if/elif chain with:
```python
from vibecraft.tools import worldedit_core

# In handle_call_tool
if name in worldedit_core.TOOL_HANDLERS:
    return await worldedit_core.TOOL_HANDLERS[name](arguments, rcon, config, logger)
```

#### Step 1.4: Repeat for other tool categories
- Extract worldedit_generation.py (~200 lines)
- Extract worldedit_clipboard.py (~150 lines)
- Extract spatial_analysis.py (~300 lines)
- Extract furniture.py (~400 lines)
- Extract patterns.py (~500 lines)
- Extract terrain.py (~600 lines)

**Target**: Reduce server.py from 5,900 to ~3,000 lines after Phase 1

### Phase 2: Extract Resource Providers (Priority 2)

Move resource loading logic to `resources/` modules:
- guides.py - Pattern/mask/expression/coordinate guides
- catalogs.py - Furniture/building patterns/terrain patterns
- minecraft_data.py - Item/block data loading

**Example**:
```python
# resources/guides.py
def get_pattern_syntax_guide() -> str:
    """Return pattern syntax guide content"""
    # ... load and return content ...
    pass

def get_mask_syntax_guide() -> str:
    # ... load and return content ...
    pass

# In server.py
from vibecraft.resources import guides

@app.list_resources()
async def list_resources() -> List[Resource]:
    return [
        Resource(uri="guide://patterns", name="Pattern Syntax Guide"),
        Resource(uri="guide://masks", name="Mask Syntax Guide"),
        # ...
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "guide://patterns":
        return guides.get_pattern_syntax_guide()
    elif uri == "guide://masks":
        return guides.get_mask_syntax_guide()
    # ...
```

**Target**: Reduce server.py to ~2,000 lines after Phase 2

### Phase 3: Extract Formatters (Priority 3)

Move output formatting logic to `formatters/` modules:
- text.py - Plain text formatting
- json.py - JSON formatting
- markdown.py - Markdown formatting

**Example**:
```python
# formatters/text.py
def format_spatial_analysis(result: Dict[str, Any]) -> str:
    """Format spatial analysis results as plain text"""
    text = f"📍 **Spatial Analysis**: ({result['center_x']}, {result['center_y']}, {result['center_z']})\n\n"

    if "surfaces" in result:
        text += format_surfaces(result["surfaces"])

    if "clearance" in result:
        text += format_clearance(result["clearance"])

    return text

def format_surfaces(surfaces: Dict[str, Any]) -> str:
    # ... surface formatting logic ...
    pass
```

**Target**: Reduce server.py to ~1,500 lines after Phase 3

### Phase 4: Create Tool Registry (Priority 4)

Replace the massive if/elif chain with a tool registry:

```python
# tools/__init__.py
from typing import Dict, Callable
from . import worldedit_core, worldedit_generation, spatial_analysis, furniture, patterns

# Tool registry maps tool name -> handler function
TOOL_REGISTRY: Dict[str, Callable] = {}

# Register all tool handlers
TOOL_REGISTRY.update(worldedit_core.TOOL_HANDLERS)
TOOL_REGISTRY.update(worldedit_generation.TOOL_HANDLERS)
TOOL_REGISTRY.update(spatial_analysis.TOOL_HANDLERS)
TOOL_REGISTRY.update(furniture.TOOL_HANDLERS)
TOOL_REGISTRY.update(patterns.TOOL_HANDLERS)

# In server.py
from vibecraft.tools import TOOL_REGISTRY

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    if name not in TOOL_REGISTRY:
        return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]

    try:
        return await TOOL_REGISTRY[name](arguments, rcon, config, logger)
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ Error: {e}")]
```

**Target**: Reduce server.py to ~500 lines (GOAL!)

### Phase 5: Add Unit Tests (Priority 5)

Now that modules are separated, add unit tests:

```python
# tests/tools/test_worldedit_core.py
import pytest
from vibecraft.tools.worldedit_core import handle_worldedit_selection
from unittest.mock import Mock, AsyncMock

@pytest.fixture
def mock_rcon():
    rcon = Mock()
    rcon.execute = AsyncMock(return_value="Selection set")
    return rcon

@pytest.mark.asyncio
async def test_handle_worldedit_selection(mock_rcon):
    """Test worldedit_selection handler"""
    arguments = {"command": "pos1 100,64,100"}

    result = await handle_worldedit_selection(
        arguments,
        rcon=mock_rcon,
        config=Mock(),
        logger=Mock()
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Selection set" in result[0].text

    mock_rcon.execute.assert_called_once_with("//pos1 100,64,100")
```

## Migration Strategy

### Approach: Gradual, Non-Breaking

1. **Create parallel structure** - New modules alongside existing server.py
2. **Copy first, then redirect** - Copy tool implementations to new modules, update server.py to call them
3. **Test thoroughly** - Ensure all tools still work after each module extraction
4. **Delete old code** - Once verified, remove duplicated code from server.py
5. **Iterate** - Repeat for each tool category

### Testing During Migration

After each module extraction:

```bash
# Run existing manual tests
python scripts/test_search.py

# Run pytest suite
pytest tests/ -v

# Test MCP server startup
cd mcp-server
source venv/bin/activate
python -m src.vibecraft.server

# Test tools via Claude Code
# (manual verification of tool responses)
```

### Rollback Plan

- Each phase is a separate commit
- If issues arise, `git revert <commit>` to undo
- Keep server.py working at all times (gradual replacement, not big-bang rewrite)

## Benefits After Refactoring

✅ **Maintainability**: Each module has <500 lines, single responsibility
✅ **Testability**: Unit tests for each tool handler
✅ **Reusability**: Common logic extracted and shared
✅ **Navigation**: Easy to find tool implementations
✅ **Onboarding**: New contributors can understand structure quickly
✅ **Extensibility**: Adding new tools requires only one new file

## Timeline Estimate

- **Phase 1** (Tool Handlers): 2-3 days
- **Phase 2** (Resources): 1 day
- **Phase 3** (Formatters): 1 day
- **Phase 4** (Registry): 0.5 day
- **Phase 5** (Tests): 2-3 days

**Total**: 6-8 days for complete refactoring

## Starting Point: Phase 1, Step 1.1

```bash
cd mcp-server/src/vibecraft
mkdir -p tools resources formatters
touch tools/__init__.py resources/__init__.py formatters/__init__.py
```

Begin extracting `worldedit_core.py` as the first module.

---

**Document Status**: Ready for implementation
**Next Action**: Create `tools/` directory structure and extract first module
