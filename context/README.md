# VibeCraft Context Files

Token-optimized knowledge files for AI-powered Minecraft building.

## Available Files

### minecraft_items.txt
- **Size**: 1,375 items from Minecraft 1.21.3
- **Format**: TOON (Token-Oriented Object Notation)
- **Content**: Item ID, internal name, display name
- **Purpose**: Block name verification, color variants, material discovery
- **Tokens**: ~26,796 tokens (filtered, no stackSize)

### minecraft_scale_reference.txt
- **Size**: 405 lines
- **Format**: TOON with hierarchical organization
- **Content**: Player-scaled architectural dimensions
- **Purpose**: Realistic room proportions, furniture placement, spacing guidelines
- **Tokens**: ~8,000 tokens (estimated)

### worldedit_recipe_book.md
- **Size**: 8 sections + coverage checklist
- **Format**: Markdown (token-lean, recipe focused)
- **Content**: Ready-made WorldEdit command sequences (structures, terrain, brushes, snapshots)
- **Purpose**: Shortcut library for complex edits, each mapped to a VibeCraft MCP tool
- **Tokens**: ~3,500 tokens (estimated)

### worldedit_basic_guide.md
- **Size**: 7 sections + quick-reference table
- **Format**: Markdown quickstart
- **Content**: Selection basics, set/replace, copy & paste, undo, brushes, utilities
- **Purpose**: Beginner ramp for Claude; confirms core commands are MCP-exposed
- **Tokens**: ~2,000 tokens (estimated)

### minecraft_furniture_catalog.json
- **Size**: 63 objects (≈160 KB), 55 actual furniture items
- **Format**: JSON array of structured furniture entries
- **Content**: Every furniture piece from the Minecraft Wiki beginners/advanced guides, including hierarchy, descriptions, bullet lists, tables, and media references
- **Purpose**: Text-based build instructions for manual furniture construction
- **Notes**: `content_blocks` keep the original paragraph/list order; no information removed
- **Tool**: Accessed via `furniture_lookup` MCP tool (action="search" or "get")

### minecraft_furniture_layouts.json
- **Size**: 7 furniture pieces (currently)
- **Format**: JSON array following furniture_layout_schema.json
- **Content**: Machine-actionable furniture blueprints with precise block coordinates
- **Purpose**: Automated furniture placement with WorldEdit commands
- **Includes**: Simple dining table, corner table, wall cabinet, chair, floor lamp, coffee table, closet
- **Schema**: Defined in furniture_layout_schema.json with bounds, placements, materials, clearance
- **Tool**: Accessed via `furniture_lookup` MCP tool (searches both catalog and layouts)

### building_patterns_structured.json
- **Size**: Initial set of 4 architectural patterns
- **Format**: JSON array with palette + layer grids
- **Content**: Machine-readable blueprints for pillars, windows, doors, and chimneys
- **Purpose**: Enables automated placement via `place_building_pattern`
- **Includes**: `pillar_1x1_simple`, `window_medium_2x2`, `door_single`, `chimney_brick_small`
- **Notes**: Complements metadata in `building_patterns_complete.json`

### furniture_layout_schema.json
- **Size**: JSON Schema definition
- **Format**: JSON Schema (draft-07)
- **Content**: Schema for furniture layout format with placement types (block, fill, line, layer)
- **Purpose**: Validation and documentation for creating new furniture layouts
- **Validation**: Use `validate_furniture_layouts.py` to check layouts against schema
- **Documentation**: Full guide in `dev_docs/FURNITURE_LAYOUT_SCHEMA.md`

## Categories in Scale Reference

1. **Player Dimensions** - Base measurements (1.8 blocks tall, 0.6 wide)
2. **Room Sizes** - 15+ room types with minimum/comfortable/spacious dimensions
3. **Furniture Dimensions** - Beds, tables, chairs, chests, counters
4. **Spacing Guidelines** - Windows, columns, torches, furniture clearance
5. **Wall Thicknesses** - Interior, exterior, fortress, defensive
6. **Ceiling Heights** - Cramped (2) to monumental (12 blocks)
7. **Structural Elements** - Columns, beams, stairs, railings
8. **Roof Proportions** - Overhang, pitch, gable heights
9. **Outdoor Spaces** - Patios, gardens, pathways, ponds
10. **Best Practices** - Common guidelines and mistakes to avoid

## How Agents Use These Files

### Minecraft Items Database
- **Search Tool**: `search_minecraft_item` MCP tool for quick lookups
- **Direct Read**: Read full file for comprehensive material palette selection
- **Use Case**: "What concrete colors exist?" → Read file or search "concrete"

### Scale Reference
- **Direct Read**: Always read when planning room layouts
- **Use Case**: "How big should a bedroom be?" → Read room_sizes section
- **Use Case**: "How far apart should torches be?" → Read spacing_guidelines
- **Quality Check**: "Is this room too small?" → Compare to minimum dimensions

### Furniture System
- **Search Tool**: `furniture_lookup(action="search", query="table")` - Find furniture by name/category/tags
- **Get Tool**: `furniture_lookup(action="get", furniture_id="simple_dining_table")` - Retrieve full details
- **Two Types**:
  - **✅ Automated layouts** (7 items): JSON with precise coordinates → Can auto-place with WorldEdit
  - **📝 Manual instructions** (55 items): Text guide from Wiki → Build by hand
- **Use Case**: "I need a dining table" → Search, get layout, place at coordinates
- **Placement**: Use `furniture_placer.py` helper to generate WorldEdit commands from layouts

### Terrain Analyzer
- **Tool**: `terrain_analyzer(x1, y1, z1, x2, y2, z2, resolution=2)` - Comprehensive terrain analysis
- **Analyzes**:
  - **Elevation**: Min/max/avg height, standard deviation, terrain type (flat/hilly/mountainous)
  - **Composition**: Top blocks, liquids, vegetation, caves/cavities
  - **Hazards**: Lava, water, steep terrain, caves, dangerous blocks
  - **Opportunities**: Flat areas, cliffs, coastlines, forests, large buildable zones
  - **Biomes**: Distribution and primary biome (when available)
- **Performance**: Resolution parameter (1=every block, 2=default, 5=fast overview)
- **Use Case**: "Where should I build my castle?" → Analyze region, review hazards/opportunities, choose optimal site
- **Output**: JSON data + natural language summary with recommendations
- **Limits**: Max 1M blocks total volume, adjustable sampling for large areas

## Token Efficiency

Both files use TOON format for maximum token efficiency:
- Compact syntax (key: value)
- Inline comments with # 
- Hierarchical nesting
- No redundant formatting

**Total context budget**: ~35k tokens for both files
**Remaining for build instructions**: ~165k tokens (in 200k context window)

## Future Context Files (Potential)

- `block_palettes.txt` - Pre-designed color combinations
- ~~`furniture_blueprints.txt`~~ - ✅ IMPLEMENTED as minecraft_furniture_layouts.json
- `architectural_patterns.txt` - Arches, columns, windows
- `style_guides.txt` - Medieval, modern, Victorian materials
- More furniture layouts - Currently 7/55 furniture have automated layouts

---

**Note**: All context files are referenced in CLAUDE.md and available to both the main assistant and specialist agents.
