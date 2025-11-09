# WorldEdit Command Audit - MCP Coverage Analysis

**Date**: 2025-11-01
**Purpose**: Comprehensive audit of WorldEdit commands vs VibeCraft MCP tools
**Reference**: minecraft-worldedit.fandom.com/wiki/Worldedit_Commands

---

## Current MCP Tool Coverage

### Selection Commands
**Tool**: `worldedit_selection`

**Covered**:
- ✅ `//pos1 [coords]` - Set position 1
- ✅ `//pos2 [coords]` - Set position 2
- ✅ `//expand <amount> [direction]` - Expand selection
- ✅ `//expand vert` - Expand to world height
- ✅ `//contract <amount> [direction]` - Contract selection
- ✅ `//shift <amount> [direction]` - Shift selection
- ✅ `//size` - Get selection info
- ✅ `//count <mask>` - Count blocks matching mask

**MISSING**:
- ❌ `//sel [mode]` - Change selection mode (cuboid, extend, poly, ellipsoid, sphere, cyl, convex)
- ❌ `//deselect` (or `//desel`) - Clear current selection
- ❌ `//inset <amount>` - Inset selection
- ❌ `//outset <amount>` - Outset selection
- ❌ `//distr` - Show block distribution in selection
- ❌ `//chunk` - Select entire chunk

---

### Region Commands
**Tool**: `worldedit_region`

**Covered**:
- ✅ `//set <pattern>` - Fill region
- ✅ `//replace <from> <to>` - Replace blocks
- ✅ `//overlay <pattern>` - Add layer on top
- ✅ `//walls <pattern>` - Build walls
- ✅ `//faces <pattern>` - Build faces
- ✅ `//smooth [iterations]` - Smooth terrain
- ✅ `//move <count> [direction]` - Move region
- ✅ `//stack <count> [direction]` - Stack region
- ✅ `//hollow [thickness]` - Hollow out
- ✅ `//center <pattern>` - Set center
- ✅ `//naturalize` - Create natural layers
- ✅ `//line <pattern>` - Draw line
- ✅ `//curve <pattern>` - Draw curve

**MISSING**:
- ❌ `//deform <expression>` - Mathematical deformation (VERY POWERFUL)
- ❌ `//regen` - Regenerate selection to original terrain
- ❌ `//flora [density]` - Generate flora in selection
- ❌ `//forest [type] [density]` - Generate forest
- ❌ `//pumpkins [density]` - Generate pumpkin patches

---

### Generation Commands
**Tool**: `worldedit_generation`

**Covered**:
- ✅ `//sphere <pattern> <radius>` - Create sphere
- ✅ `//hsphere <pattern> <radius>` - Create hollow sphere
- ✅ `//cyl <pattern> <radius> [height]` - Create cylinder
- ✅ `//hcyl <pattern> <radius> [height]` - Create hollow cylinder
- ✅ `//pyramid <pattern> <size>` - Create pyramid
- ✅ `//hpyramid <pattern> <size>` - Create hollow pyramid
- ✅ `//generate <pattern> <expression>` - Generate by math formula

**MISSING**:
- ❌ `//cone <pattern> <radius> [height]` - Cone shape (mentioned but not implemented?)
- ❌ `//caves [size] [freq] [rarity]` - Generate cave systems
- ❌ `//ore <pattern> <size> <freq> <rarity> <minY> <maxY>` - Generate ore veins

---

### Clipboard Commands
**Tool**: `worldedit_clipboard`

**Covered**:
- ✅ `//copy` - Copy to clipboard
- ✅ `//cut [pattern]` - Cut to clipboard
- ✅ `//paste` - Paste from clipboard
- ✅ `//rotate <y> [x] [z]` - Rotate clipboard
- ✅ `//flip [direction]` - Flip clipboard
- ✅ `/clearclipboard` - Clear clipboard

**MISSING**:
- ❌ `//lazycopy` - Copy without storing in history
- ❌ `//lazycut` - Cut without storing in history
- ❌ `//place` - Place without moving origin

---

### History Commands
**Tool**: `worldedit_history`

**Covered**:
- ✅ `//undo [times]` - Undo edits
- ✅ `//redo [times]` - Redo edits
- ✅ `//clearhistory` - Clear history

**ALL COVERED** ✅

---

### Schematic Commands
**Tool**: `worldedit_schematic`

**Covered**:
- ✅ `/schem list` - List schematics
- ✅ `/schem load <name>` - Load schematic
- ✅ `/schem save <name>` - Save schematic
- ✅ `/schem delete <name>` - Delete schematic

**MISSING**:
- ❌ `/schem formats` - List supported formats
- ❌ `/schem loadall` - Load all schematics from directory

---

### Utility Commands
**Tool**: `worldedit_utility`

**Covered**:
- ✅ `//fill <pattern> <radius> [depth]` - Fill holes
- ✅ `//fillr <pattern> <radius> [depth]` - Recursive fill
- ✅ `//drain <radius>` - Drain water/lava
- ✅ `/removeabove [size] [height]` - Remove blocks above
- ✅ `/removebelow [size] [height]` - Remove blocks below
- ✅ `/removenear <mask> [radius]` - Remove nearby blocks
- ✅ `/fixwater <radius>` - Fix water
- ✅ `/fixlava <radius>` - Fix lava
- ✅ `/snow [size]` - Simulate snow
- ✅ `/thaw [size]` - Melt snow/ice
- ✅ `/green [size]` - Convert dirt to grass
- ✅ `/extinguish [radius]` - Remove fire
- ✅ `/butcher [radius]` - Remove mobs
- ✅ `/remove <type> <radius>` - Remove entities

**MISSING**:
- ❌ `//replacenear <size> <from> <to>` - Replace nearby blocks
- ❌ `//ex [radius]` - Extinguish (alias for /extinguish)
- ❌ `/kill` - Kill all entities

---

### Biome Commands
**Tool**: `worldedit_biome`

**Covered**:
- ✅ `/biomelist` - List biomes
- ✅ `/biomeinfo` - Get biome at location
- ✅ `//setbiome <biome>` - Set biome

**ALL COVERED** ✅

---

### Brush Commands
**Tool**: `worldedit_brush`

**Covered**:
- ✅ `/br sphere` - Sphere brush
- ✅ `/br cylinder` - Cylinder brush
- ✅ `/br smooth` - Smooth brush
- ✅ `/br gravity` - Gravity brush
- ✅ `/br clipboard` - Clipboard brush
- ✅ `/br extinguish` - Fire extinguisher
- ✅ `/br butcher` - Mob killer brush
- ✅ `/mask` - Set brush mask
- ✅ `/material` - Set brush material
- ✅ `/size` - Set brush size
- ✅ `/range` - Set brush range

**MISSING**:
- ❌ `/br forest` - Forest brush
- ❌ `/br raise` - Raise terrain brush
- ❌ `/br lower` - Lower terrain brush
- ❌ `/br deform` - Deform brush
- ❌ `/br apply` - Apply expression brush
- ❌ `/br paint` - Paint brush
- ❌ `/br splatter` - Splatter brush (exists but needs testing)
- ❌ `/br scmd` - Script command brush
- ❌ `/br scroll` - Scroll action for brushes

---

### Tool Commands
**Tool**: `worldedit_tools`

**Covered**:
- ✅ `/tool` - Bind tools to items
- ✅ `/mask` - Set tool mask
- ✅ `/material` - Set tool material
- ✅ `/range` - Set tool range
- ✅ `/size` - Set tool size
- ✅ `//` or `/,` - Toggle super pickaxe
- ✅ `/sp` - Configure super pickaxe

**MISSING**:
- ❌ `/tool repl <pattern>` - Replacer tool
- ❌ `/tool cycler` - Block data cycler
- ❌ `/tool tree [type]` - Tree placer
- ❌ `/tool deltree` - Tree remover
- ❌ `/tool farwand` - Long-range wand
- ❌ `/tool lrbuild` - Left/right click builder
- ❌ `/tool info` - Information tool
- ❌ `/none` - Unbind tool

---

### Navigation Commands
**Tool**: `worldedit_navigation`

**Covered**:
- ✅ `/ascend [levels]` - Go up
- ✅ `/descend [levels]` - Go down
- ✅ `/ceil [clearance]` - Go to ceiling
- ✅ `/thru` - Pass through wall
- ✅ `/up <distance>` - Go up distance
- ✅ `/unstuck` - Get unstuck
- ✅ `/jumpto` - Jump to block

**ALL COVERED** ✅

---

### Chunk Commands
**Tool**: `worldedit_chunk`

**Covered**:
- ✅ `/chunkinfo` - Show chunk info
- ✅ `/listchunks` - List chunks in selection
- ✅ `/delchunks` - Delete chunks

**ALL COVERED** ✅

---

### Snapshot Commands
**Tool**: `worldedit_snapshot`

**Covered**:
- ✅ `/snap list` - List snapshots
- ✅ `/snap use <name>` - Use snapshot
- ✅ `/snap sel <index>` - Select snapshot
- ✅ `/snap before <date>` - Select before date
- ✅ `/snap after <date>` - Select after date
- ✅ `/restore [snapshot]` - Restore from snapshot

**ALL COVERED** ✅

---

### Scripting Commands
**Tool**: `worldedit_scripting`

**Covered**:
- ✅ `/cs <filename>` - Run CraftScript
- ✅ `/.s [args]` - Re-run previous script

**MISSING**:
- ❌ `.js <code>` - Execute JavaScript
- ❌ `/execute` - Execute command as player

---

### General/Session Commands
**Tool**: `worldedit_general`

**Covered**:
- ✅ `//limit <limit>` - Set block change limit
- ✅ `//timeout <time>` - Set calculation timeout
- ✅ `//gmask <mask>` - Set global mask
- ✅ `//perf` - Toggle side effects
- ✅ `//update` - Update lighting
- ✅ `//reorder` - Reorder chunk loading
- ✅ `//drawsel` - Toggle selection visualization
- ✅ `//world <world>` - Change world
- ✅ `//watchdog` - Set watchdog mode
- ✅ `/worldedit help` - Show help
- ✅ `/worldedit version` - Show version
- ✅ `/worldedit reload` - Reload config

**MISSING**:
- ❌ `//fast` - Toggle fast mode (skip lighting/physics)
- ❌ `//searchitem` - Search for items (exists in reference tool)
- ❌ `//help [page]` - Show help pages (exists in reference tool)
- ❌ `//tracemask` - Set trace mask (exists in brush tool)

---

### Reference Commands
**Tool**: `worldedit_reference`

**Covered**:
- ✅ `/searchitem` - Search items
- ✅ `//help` - Get help

**MISSING**:
- ❌ `/we report` - Generate diagnostic report

---

### Calculation/Analysis Commands
**NOT IN ANY TOOL** ❌

**MISSING**:
- ❌ `//calc <expression>` - Calculator for math expressions
- ❌ `//distr` - Block distribution in selection
- ❌ `//count <mask>` - Count blocks (might be in selection?)

---

## Summary of Missing Commands

### CRITICAL MISSING (High Value, Common Use)

1. **`//deform <expression>`** - Mathematical terrain deformation
   - VERY powerful for organic shapes
   - Uses math expressions like `y-=0.2*sin(x*5)`
   - Essential for advanced terrain sculpting

2. **`//sel [mode]`** - Change selection mode
   - cuboid (default), sphere, poly, ellipsoid, cyl
   - Required for non-box selections
   - Very common need

3. **`//distr`** - Block distribution analysis
   - Shows what blocks are in selection and counts
   - Essential for analysis and planning

4. **`//flora [density]`** - Generate flora
   - Quick vegetation in selection
   - Much faster than manual placement

5. **`//forest [type] [density]`** - Generate forest
   - Tree generation with density control
   - Better than pattern-based for large forests

6. **`//calc <expression>`** - Calculator
   - Math evaluation for planning
   - Useful for coordinate calculations

### HIGH PRIORITY MISSING (Valuable)

7. **`//caves [size] [freq] [rarity]`** - Generate caves
   - Natural cave systems
   - Terrain generation feature

8. **`//ore <pattern> <size> <freq> <rarity> <minY> <maxY>`** - Ore generation
   - Generate ore veins naturally
   - Terrain generation feature

9. **`//regen`** - Regenerate to original terrain
   - Restore terrain to world seed
   - Undo extensive modifications

10. **`//replacenear <size> <from> <to>`** - Replace nearby
    - Like //replace but spherical around player
    - More intuitive than region selection

11. **`/tool tree [type]`** - Tree placer tool
    - Right-click to place trees
    - Faster than commands

12. **`/tool repl <pattern>`** - Replacer tool
    - Left-click = source block, right-click = paste
    - Very useful for copying blocks

### MEDIUM PRIORITY MISSING (Useful)

13. **`//inset <amount>`** - Inset selection
14. **`//outset <amount>`** - Outset selection
15. **`//pumpkins [density]`** - Pumpkin patches
16. **`//chunk`** - Select entire chunk
17. **`/tool farwand`** - Long-range position setting
18. **`/tool info`** - Block information tool
19. **`/br forest`** - Forest brush
20. **`/br raise/lower`** - Terrain height brushes
21. **`//fast`** - Fast mode toggle
22. **`.js <code>`** - JavaScript execution
23. **`//lazycopy/lazycut`** - No-history clipboard operations

### LOW PRIORITY (Edge Cases)

24. Various other tool variants
25. Advanced brush modes
26. Specialized utility commands

---

## Implementation Priority

### Phase 1: Essential Commands (Must Have)
1. `//deform` - Mathematical deformations
2. `//sel` - Selection mode changing
3. `//distr` - Block distribution
4. `//calc` - Calculator
5. `//flora` - Flora generation
6. `//forest` - Forest generation

### Phase 2: High-Value Commands (Should Have)
7. `//caves` - Cave generation
8. `//ore` - Ore generation
9. `//regen` - Terrain regeneration
10. `//replacenear` - Nearby replacement
11. `/tool tree` - Tree placer
12. `/tool repl` - Replacer tool

### Phase 3: Nice-to-Have Commands
13. `//inset/outset` - Selection modification
14. `//pumpkins` - Pumpkin generation
15. `/tool farwand` - Long-range wand
16. `/tool info` - Information tool
17. Various brush enhancements

---

## Recommended Approach

### Option 1: Expand Existing Tools
Add missing commands to appropriate existing tools:
- Add `//deform`, `//flora`, `//forest`, `//regen` to `worldedit_region`
- Add `//sel`, `//distr`, `//inset`, `//outset`, `//chunk` to `worldedit_selection`
- Add `//caves`, `//ore` to `worldedit_generation`
- Add `//calc` to `worldedit_general`
- Add `/tool tree`, `/tool repl`, `/tool farwand` to `worldedit_tools`

### Option 2: Create New Specialized Tools
Create focused tools for specific domains:
- `worldedit_analysis` - //distr, //count, //calc
- `worldedit_vegetation` - //flora, //forest, //pumpkins, /tool tree
- `worldedit_terrain` - //caves, //ore, //regen, //deform
- `worldedit_selection_advanced` - //sel, //inset, //outset, //chunk

### Option 3: Hybrid Approach (RECOMMENDED)
- Add simple commands to existing tools
- Create new tools for complex domains:
  - **`worldedit_deform`** - //deform with safety and examples
  - **`worldedit_vegetation`** - //flora, //forest, //pumpkins
  - **`worldedit_caves`** - //caves, //ore
  - **Expand `worldedit_selection`** - Add //sel, //distr, //inset, //outset
  - **Expand `worldedit_general`** - Add //calc, //regen

---

## Implementation Estimate

**Phase 1** (6 commands):
- Lines: ~300 (tool definitions + handlers)
- Complexity: Medium to High (//deform is complex)
- Time: 2-3 hours

**Phase 2** (6 commands):
- Lines: ~200
- Complexity: Medium
- Time: 1-2 hours

**Phase 3** (7+ commands):
- Lines: ~250
- Complexity: Low to Medium
- Time: 1-2 hours

**Total**: ~750 lines of code, 4-7 hours implementation

---

## Next Steps

1. **User decision**: Which phase to implement first?
2. **Approach decision**: Expand existing tools or create new ones?
3. **Implementation**: Code and test
4. **Documentation**: Update CLAUDE.md with new commands
5. **Testing**: Verify all commands work correctly

---

**Status**: Audit complete, awaiting direction on implementation priority
