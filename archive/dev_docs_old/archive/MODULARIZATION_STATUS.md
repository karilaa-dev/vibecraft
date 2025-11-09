# VibeCraft Server.py Modularization - Status & Continuation Guide

**Date**: 2025-11-05
**Current State**: Infrastructure complete, 1 module extracted, ready for systematic continuation
**Progress**: 5,927 → 5,727 lines (200 lines removed via V1 cleanup)

---

## ✅ Completed Work

### 1. Blockers Resolved (CODE_REVIEW_FOLLOWUP.md)
- ✅ Fixed pytest import paths (conftest.py created)
- ✅ Fixed manual script paths (correct parent directory resolution)
- ✅ Completely removed V1 spatial analyzer (not just deprecated)

### 2. Infrastructure Created
- ✅ Created `mcp-server/src/vibecraft/tools/` directory
- ✅ Created tool registry system in `tools/__init__.py`
- ✅ Defined `@register_tool` decorator pattern
- ✅ Created first extracted module: `tools/spatial.py`

### 3. First Module Extracted
- ✅ Extracted `spatial_awareness_scan` → `tools/spatial.py`
- ✅ Registered in TOOL_REGISTRY
- ✅ Ready to update server.py to use it

---

## 📊 Extraction Analysis

### Tool Categories & Line Counts

| Category | Tools | Lines | Priority | Status |
|----------|-------|-------|----------|--------|
| **Spatial Analysis** | spatial_awareness_scan | ~80 | 🔴 Critical | ✅ Extracted |
| **Validation Tools** | validate_pattern, validate_mask, check_symmetry, analyze_lighting, validate_structure | ~400 | 🔴 Critical | 🔲 Ready |
| **Furniture Tools** | furniture_lookup, place_furniture | ~400 | 🟡 High | 🔲 Ready |
| **Pattern Tools** | building_pattern_lookup, place_building_pattern, terrain_pattern_lookup | ~500 | 🟡 High | 🔲 Ready |
| **Terrain Tools** | terrain_analyzer, generate_terrain, texture_terrain, smooth_terrain | ~600 | 🟡 High | 🔲 Ready |
| **Geometry Tools** | calculate_shape, calculate_window_spacing | ~300 | 🟢 Medium | 🔲 Ready |
| **Advanced WorldEdit** | worldedit_deform, worldedit_vegetation, worldedit_terrain_advanced, worldedit_analysis | ~250 | 🟢 Medium | 🔲 Ready |
| **Workflow Tools** | workflow_status, workflow_advance, workflow_reset | ~150 | 🟢 Medium | 🔲 Ready |
| **Helper Utilities** | search_minecraft_item, get_player_position, get_surface_level | ~220 | 🟢 Medium | 🔲 Ready |
| **WorldEdit Core** | 15+ tools (selection, region, etc.) | ~10 | ⚪ Keep | N/A - Already optimal |

**Total Extractable**: ~2,900 lines
**Keep in server.py**: ~2,800 lines (tool definitions, resources, infrastructure)
**Target**: 2,627 lines in server.py

---

## 🔧 Extraction Template

### Step-by-Step Process

For each tool category, follow this exact pattern:

#### 1. Create Module File

```python
# Example: tools/validation.py
"""
Validation Tool Handlers

Pattern/mask validation, symmetry checking, lighting analysis, structure validation.
"""

import logging
from typing import Dict, Any, List
from mcp.types import TextContent

logger = logging.getLogger(__name__)


async def handle_validate_pattern(
    arguments: Dict[str, Any],
    rcon,
    config,
    logger_instance: logging.Logger
) -> List[TextContent]:
    """
    Handle validate_pattern tool.

    Copy implementation from server.py:2735-2784
    """
    # Copy validation logic from server.py
    pattern = arguments.get("pattern", "").strip()

    if not pattern:
        return [TextContent(type="text", text="❌ Pattern cannot be empty")]

    # ... rest of implementation ...
    return [TextContent(type="text", text=analysis_text)]


async def handle_validate_mask(
    arguments: Dict[str, Any],
    rcon,
    config,
    logger_instance: logging.Logger
) -> List[TextContent]:
    """
    Handle validate_mask tool.

    Copy implementation from server.py:2785-2834
    """
    # Copy validation logic
    pass


# Add remaining handlers: check_symmetry, analyze_lighting, validate_structure
```

#### 2. Register in tools/__init__.py

```python
# Add to tools/__init__.py
from . import validation

# Register all handlers
TOOL_REGISTRY["validate_pattern"] = validation.handle_validate_pattern
TOOL_REGISTRY["validate_mask"] = validation.handle_validate_mask
TOOL_REGISTRY["check_symmetry"] = validation.handle_check_symmetry
TOOL_REGISTRY["analyze_lighting"] = validation.handle_analyze_lighting
TOOL_REGISTRY["validate_structure"] = validation.handle_validate_structure
```

#### 3. Test Import

```bash
cd mcp-server
python -c "from vibecraft.tools import TOOL_REGISTRY; print(len(TOOL_REGISTRY))"
# Should show number of registered tools
```

#### 4. Update server.py (Final Step - Do Once After All Extractions)

```python
# In server.py, replace the massive if/elif chain:

# OLD (5,000+ lines):
@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    if name == "rcon_command":
        # ...
    elif name == "spatial_awareness_scan":
        # ... 80 lines ...
    elif name == "validate_pattern":
        # ... 50 lines ...
    # ... 40 more tools ...

# NEW (much shorter):
from vibecraft.tools import TOOL_REGISTRY

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    # Handle special cases first (rcon_command, WorldEdit passthrough)
    if name == "rcon_command":
        # Keep existing implementation
        pass
    elif name in WORLD_EDIT_TOOL_PREFIXES:
        # Keep existing implementation
        pass

    # Use registry for all extracted tools
    elif name in TOOL_REGISTRY:
        handler = TOOL_REGISTRY[name]
        return await handler(arguments, rcon, config, logger)

    else:
        return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]
```

#### 5. Remove Extracted Code from server.py

After verifying the tool works, delete the original elif block from server.py.

---

## 🎯 Priority Extraction Order

### Week 1: High-Value Extractions
1. **Day 1**: Validation tools (~400 lines)
   - Extract: validate_pattern, validate_mask, check_symmetry, analyze_lighting, validate_structure
   - Test: Run pytest + manual validation tests
   - Remove from server.py

2. **Day 2**: Furniture tools (~400 lines)
   - Extract: furniture_lookup, place_furniture
   - Test: Run furniture placement scripts
   - Remove from server.py

3. **Day 3**: Pattern tools (~500 lines)
   - Extract: building_pattern_lookup, place_building_pattern, terrain_pattern_lookup
   - Test: Pattern placement verification
   - Remove from server.py

**Week 1 Target**: Remove 1,300 lines → **4,427 lines remaining**

### Week 2: Medium-Priority Extractions
4. **Day 4**: Terrain tools (~600 lines)
5. **Day 5**: Geometry tools (~300 lines)
6. **Day 6**: Advanced WorldEdit (~250 lines)

**Week 2 Target**: Remove 1,150 lines → **3,277 lines remaining**

### Week 3: Remaining + Integration
7. **Day 7**: Workflow tools (~150 lines)
8. **Day 8**: Helper utilities (~220 lines)
9. **Day 9**: Update server.py to use registry (replace if/elif chain)
10. **Day 10**: Final testing, documentation, cleanup

**Week 3 Target**: Remove 370 lines + integrate → **~2,600 lines final**

---

## 📝 Tool Handler Locations in server.py

Quick reference for finding tool implementations:

```
validate_pattern:        Line 2735-2784
validate_mask:           Line 2785-2834
search_minecraft_item:   Line 2835-2883
get_player_position:     Line 2884-3033
get_surface_level:       Line 3034-3084
calculate_region_size:   Line 3085-3130
furniture_lookup:        Line 3131-3390
place_furniture:         Line 3391-3610
terrain_analyzer:        Line 4828-4920
calculate_shape:         Line 3611-3755
calculate_window_spacing: Line 3756-3825
check_symmetry:          Line 5053-5119
analyze_lighting:        Line 5120-5186
validate_structure:      Line 5187-5258
generate_terrain:        Line 5259-5357
texture_terrain:         Line 5358-5406
smooth_terrain:          Line 5407-5454
building_pattern_lookup: Line 4455-4643
place_building_pattern:  Line 4644-4727
terrain_pattern_lookup:  Line 4728-4782
spatial_awareness_scan:  Line 4784-4826 (✅ Already extracted!)
worldedit_deform:        Line 5511-5531
worldedit_vegetation:    Line 5532-5587
worldedit_terrain_advanced: Line 5588-5648
worldedit_analysis:      Line 5649-5689
workflow_status:         Line 5690-5710
workflow_advance:        Line 5711-5733
workflow_reset:          Line 5734-5754
```

---

## 🧪 Testing Checklist

After each extraction:

```bash
# 1. Import test
cd mcp-server
python -c "from vibecraft.tools import TOOL_REGISTRY; print(list(TOOL_REGISTRY.keys()))"

# 2. Pytest
pytest tests/ -v

# 3. Server startup
python -m src.vibecraft.server
# (Ctrl+C after startup confirmation)

# 4. Tool-specific tests
# (Run relevant manual scripts from scripts/ directory)
```

---

## 📚 Module Organization

Final structure will look like:

```
mcp-server/src/vibecraft/
├── server.py (~2,600 lines)
│   ├── Tool definitions (MCP metadata)
│   ├── Resource definitions
│   ├── Main async loop
│   └── Special handlers (rcon_command, WorldEdit passthrough)
│
├── tools/
│   ├── __init__.py (Tool registry)
│   ├── spatial.py ✅ (spatial_awareness_scan)
│   ├── validation.py (validate_*, check_symmetry, analyze_lighting)
│   ├── furniture_tools.py (furniture_lookup, place_furniture)
│   ├── patterns.py (pattern lookups and placers)
│   ├── terrain_tools.py (terrain analyzer, generator, texture, smooth)
│   ├── geometry.py (calculate_shape, calculate_window_spacing)
│   ├── worldedit_advanced.py (deform, vegetation, terrain_advanced, analysis)
│   ├── workflow_tools.py (workflow_status, advance, reset)
│   └── helpers.py (search_item, get_player_pos, get_surface_level)
│
├── core/ (Already extracted - no changes needed)
│   ├── rcon_manager.py
│   ├── config.py
│   ├── sanitizer.py
│   └── ...
```

---

## 🚀 Getting Started

To continue modularization:

```bash
cd /Users/er/Repos/vibecraft/mcp-server/src/vibecraft

# 1. Create next module (e.g., validation.py)
touch tools/validation.py

# 2. Copy tool implementations from server.py (see line numbers above)
# Edit tools/validation.py and paste implementations

# 3. Register tools in tools/__init__.py

# 4. Test import
python -c "from vibecraft.tools import TOOL_REGISTRY; print(TOOL_REGISTRY.keys())"

# 5. Test server startup
cd /Users/er/Repos/vibecraft/mcp-server
python -m src.vibecraft.server

# 6. Once verified, remove original code from server.py

# 7. Commit
git add -A
git commit -m "Extract validation tools to tools/validation.py"
```

---

## Summary

**What's Done**:
- ✅ All CODE_REVIEW_FOLLOWUP.md blockers resolved
- ✅ Infrastructure for modularization created
- ✅ First tool extracted as template (spatial.py)
- ✅ Clear roadmap with line numbers and extraction order

**What's Next**:
- Follow the template above to extract remaining 12 tool categories
- Each extraction is independent and can be done incrementally
- Full completion estimated: 10-15 developer-days

**Current State**:
- Server.py: 5,727 lines
- After complete extraction: ~2,600 lines (55% reduction)
- Tools extracted: 1/13 categories
- Ready for systematic continuation by engineering team
