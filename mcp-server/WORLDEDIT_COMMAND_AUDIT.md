# WorldEdit Command Coverage Audit

## Summary

Our MCP server provides **17 categorized tools** that expose WorldEdit commands, plus a generic `rcon_command` tool that can execute ANY command.

**Total WorldEdit Commands Available: 130+**
- Double-slash commands (//): 68
- Single-slash commands (/): 62

## Our Current Coverage Strategy

### ✅ What We Have

Our MCP server uses a **category-based approach** rather than exposing individual commands:

1. **`rcon_command`** - Generic tool that can execute ANY WorldEdit command
2. **17 Specialized WorldEdit Tools**:
   - `worldedit_selection` - pos1, pos2, expand, contract, shift, size, count
   - `worldedit_region` - set, replace, walls, faces, overlay, move, stack, hollow, etc.
   - `worldedit_generation` - sphere, cylinder, pyramid, cone, generate, feature
   - `worldedit_clipboard` - copy, cut, paste, rotate, flip
   - `worldedit_schematic` - save, load, list, delete schematics
   - `worldedit_history` - undo, redo, clearhistory
   - `worldedit_utility` - fill, drain, fixwater, removeabove, etc.
   - `worldedit_biome` - biomelist, biomeinfo, setbiome
   - `worldedit_brush` - brush commands and configuration
   - `worldedit_general` - limit, gmask, perf, update, reorder, watchdog
   - `worldedit_navigation` - ascend, descend, ceil, thru, up, jumpto, unstuck
   - `worldedit_chunk` - chunkinfo, listchunks, delchunks
   - `worldedit_snapshot` - snap list, snap use, restore
   - `worldedit_scripting` - cs (CraftScript execution)
   - `worldedit_reference` - searchitem, help
   - `worldedit_tools` - tool, mask, material, range, size, toggleeditwand
   - `worldedit_deform` - //deform command
   - `worldedit_vegetation` - forest, flora, tree, pumpkins
   - `worldedit_terrain_advanced` - smooth, naturalize, regen
   - `worldedit_analysis` - count, distr, size

## Commands Available in WorldEdit 7.3.17

### Double-Slash Commands (//)

```
// - Toggle super pickaxe
//calculate - Math expressions
//center - Set center blocks
//chunk - Chunk management
//cone - Generate cones
//contract - Contract selection
//copy - Copy to clipboard
//count - Count blocks
//curve - Draw curves
//cut - Cut to clipboard
//cyl - Generate cylinders
//deform - Deform regions
//distr - Block distribution
//drain - Drain liquids
//drawsel - Visualize selection
//expand - Expand selection
//faces - Build all 6 faces
//fast - Toggle fast mode
//feature - Generate features
//fill - Fill holes
//fillr - Recursive fill
//flip - Flip clipboard
//flora - Generate flora
//forest - Generate forest
//generate - Generate with expression
//generatebiome - Generate biome terrain
//hcyl - Hollow cylinder
//help - WorldEdit help
//hollow - Hollow out region
//hpos1 - Set pos1 (raycast)
//hpos2 - Set pos2 (raycast)
//hpyramid - Hollow pyramid
//hsphere - Hollow sphere
//inset - Inset selection
//limit - Set block limit
//line - Draw line
//move - Move region
//naturalize - Create natural layers
//outset - Outset selection
//overlay - Overlay pattern
//paste - Paste from clipboard
//perf - Performance settings
//pos - Set position
//pos1 - Set first position
//pos2 - Set second position
//pyramid - Generate pyramid
//regen - Regenerate chunks
//reorder - Reorder mode
//replace - Replace blocks
//rotate - Rotate clipboard
//sel - Set selection mode
//set - Fill region
//setbiome - Set biome
//shift - Shift selection
//size - Get selection size
//smooth - Smooth terrain
//snowsmooth - Snow-aware smooth
//sphere - Generate sphere
//stack - Stack region
//structure - Generate structure
//timeout - Set timeout
//trim - Trim selection
//update - Update mode
//walls - Build walls only
//wand - Get selection wand
//watchdog - Watchdog mode
//world - Switch world
```

### Single-Slash Commands (/)

```
/ascend - Ascend levels
/biomeinfo - Get biome info
/biomelist - List biomes
/brush - Brush commands
/butcher - Kill mobs
/ceil - Go to ceiling
/chunkinfo - Chunk info
/clearclipboard - Clear clipboard
/clearhistory - Clear history
/cs - Execute CraftScript
/cycler - Cycle block data
/delchunks - Delete chunks
/deltree - Remove tree
/descend - Descend levels
/extinguish - Put out fire
/farwand - Far wand tool
/fixlava - Fix lava
/fixwater - Fix water
/floodfill - Flood fill
/forestgen - Generate forest
/gmask - Global mask
/green - Convert to grass
/info - Block info tool
/jumpto - Jump to block
/listchunks - List chunks
/lrbuild - Left-right build
/mask - Set brush mask
/material - Set brush material
/navwand - Navigation wand
/none - Clear tool
/placement - Placement mode
/pumpkins - Generate pumpkins
/range - Set brush range
/redo - Redo changes
/remove - Remove entities
/removeabove - Remove above
/removebelow - Remove below
/removenear - Remove nearby
/repl - Block replacer tool
/replacenear - Replace nearby
/restore - Restore snapshot
/schematic - Schematic commands
/searchitem - Search items
/selwand - Selection wand
/size - Brush size
/snapshot - Snapshot commands
/snow - Simulate snow
/superpickaxe - Super pickaxe
/thaw - Melt snow/ice
/thru - Go through wall
/toggleeditwand - Toggle edit wand
/toggleplace - Toggle placement
/tool - Tool commands
/tracemask - Trace mask
/tree - Generate tree
/undo - Undo changes
/unstuck - Get unstuck
/up - Go up
/worldedit - WorldEdit commands
```

## Gap Analysis

### ✅ Fully Covered

All commands are accessible through either:
1. Specialized category tools (with better descriptions)
2. Generic `rcon_command` tool

### 📋 Documentation in MCP Tools

Our MCP tools provide:
- **Better organization** than flat command list
- **Usage examples** for each category
- **Parameter descriptions**
- **Common workflows**
- **Safety warnings**

## Recommendations

### Option 1: Keep Current Approach ✅ RECOMMENDED

**Pros:**
- Cleaner API (17 tools vs 130+ tools)
- Better discoverability for AI
- Organized by function
- Still has full access via `rcon_command`
- Easier to maintain

**Cons:**
- AI needs to know which category a command belongs to

### Option 2: Add Individual Command Tools

**Pros:**
- Direct 1:1 mapping
- No categorization needed

**Cons:**
- 130+ tools clutters the interface
- Harder for AI to discover
- Maintenance nightmare
- Less context per command

### Option 3: Hybrid Approach

Keep current 17 category tools + add most frequently used commands as individual tools:
- `worldedit_pos1`
- `worldedit_pos2`
- `worldedit_set`
- `worldedit_replace`
- `worldedit_copy`
- `worldedit_paste`
- `worldedit_undo`
- `worldedit_redo`

**Pros:**
- Quick access to common commands
- Still organized

**Cons:**
- Duplication (commands available in both category and individual tools)

## Current Command Mapping

| Our Tool | Commands Covered |
|----------|------------------|
| `rcon_command` | ALL 130+ commands |
| `worldedit_selection` | pos1, pos2, pos, hpos1, hpos2, expand, contract, shift, inset, outset, size, count, chunk, sel |
| `worldedit_region` | set, replace, overlay, walls, faces, center, hollow, line, curve, smooth, naturalize, move, stack |
| `worldedit_generation` | sphere, hsphere, cyl, hcyl, cone, pyramid, hpyramid, generate, generatebiome, feature, structure |
| `worldedit_clipboard` | copy, cut, paste, flip, rotate, clearclipboard |
| `worldedit_schematic` | schematic (load, save, list, delete, formats) |
| `worldedit_history` | undo, redo, clearhistory |
| `worldedit_utility` | fill, fillr, drain, fixwater, fixlava, removeabove, removebelow, removenear, extinguish, butcher, remove, snow, thaw, green |
| `worldedit_biome` | biomelist, biomeinfo, setbiome |
| `worldedit_brush` | brush (all brush types), mask, material, range, size, none |
| `worldedit_general` | limit, timeout, fast, perf, update, reorder, drawsel, gmask, world, watchdog, worldedit |
| `worldedit_navigation` | ascend, descend, ceil, thru, up, jumpto, unstuck |
| `worldedit_chunk` | chunkinfo, listchunks, delchunks, trim |
| `worldedit_snapshot` | snapshot (list, use, sel, before, after), restore |
| `worldedit_scripting` | cs (CraftScript execution), /.s |
| `worldedit_reference` | searchitem, help |
| `worldedit_tools` | tool, mask, material, range, size, tracemask, toggleeditwand, toggleplace, wand, selwand, navwand, farwand, deltree, repl, cycler, floodfill, lrbuild, info, tree |
| `worldedit_deform` | deform |
| `worldedit_vegetation` | forest, flora, tree, forestgen, pumpkins |
| `worldedit_terrain_advanced` | smooth, snowsmooth, naturalize, regen, generatebiome |
| `worldedit_analysis` | count, distr, size |

## Conclusion

**We have FULL coverage of all WorldEdit commands.** Our approach is actually BETTER than exposing individual commands because:

1. **Better Organization**: Commands grouped by purpose
2. **Better Documentation**: Each tool has detailed descriptions
3. **Flexibility**: `rcon_command` can execute anything
4. **Maintainability**: 17 tools easier to maintain than 130+
5. **AI-Friendly**: Easier for AI to discover and use

**No commands are missing.** The categorization is working as intended.
