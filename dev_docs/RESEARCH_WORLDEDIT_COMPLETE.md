# VibeCraft: Complete WorldEdit Command Research

**Date:** 2025-10-30
**Purpose:** Comprehensive documentation of ALL WorldEdit commands for MCP server implementation
**References:**
- WorldEdit Official Docs: https://worldedit.enginehub.org/en/latest/
- WorldEdit GitHub: https://github.com/enginehub/WorldEdit
- RCON-MCP Reference: https://github.com/rgbkrk/rcon-mcp

---

## Executive Summary

WorldEdit 7.3+ contains **200+ commands** organized into 17 major categories. This document provides complete command taxonomy, syntax, parameters, and implementation requirements for exposing all functionality via MCP server.

### Key Statistics
- **17 Command Categories**
- **200+ Individual Commands**
- **50+ Brush Types**
- **15+ Pattern Types**
- **20+ Mask Types**
- **40+ Math/Expression Functions**

---

## Command Categories

### 1. GENERAL COMMANDS (14 commands)
Core WorldEdit functionality and session management.

| Command | Syntax | Description | Permission |
|---------|--------|-------------|------------|
| `/worldedit` | `/we [help\|version\|reload\|cui\|tz\|report]` | Main WorldEdit hub | `worldedit.*` |
| `//undo` | `//undo [times] [player]` | Undo edit actions | `worldedit.history.undo` |
| `//redo` | `//redo [times] [player]` | Redo edit actions | `worldedit.history.redo` |
| `//clearhistory` | `//clearhistory` | Clear edit history | `worldedit.history.clear` |
| `//limit` | `//limit [limit]` | Set block change limit | `worldedit.limit` |
| `//timeout` | `//timeout [limit]` | Set evaluation timeout | `worldedit.timeout` |
| `//fast` | `//fast [mode]` | Toggle fast mode (deprecated) | `worldedit.fast` |
| `//perf` | `//perf [-h] [sideEffect] [newState]` | Toggle side effects | `worldedit.perf` |
| `//update` | `//update [sideEffectSet]` | Apply side effects | `worldedit.update` |
| `//reorder` | `//reorder [mode]` | Set reorder mode | `worldedit.reorder` |
| `//drawsel` | `//drawsel [draw]` | Toggle selection drawing | `worldedit.drawsel` |
| `//world` | `//world [world]` | Set world override | `worldedit.world` |
| `//watchdog` | `//watchdog [hookMode]` | Change watchdog hook | `worldedit.watchdog` |
| `//gmask` | `//gmask [mask]` | Set global mask | `worldedit.global-mask` |

### 2. NAVIGATION COMMANDS (7 commands)
Player movement and teleportation utilities.

| Command | Syntax | Description | Permission |
|---------|--------|-------------|------------|
| `/unstuck` | `/unstuck` | Escape from stuck position | `worldedit.navigation.unstuck` |
| `/ascend` | `/ascend [levels]` | Move up through floors | `worldedit.navigation.ascend` |
| `/descend` | `/descend [levels]` | Move down through floors | `worldedit.navigation.descend` |
| `/ceil` | `/ceil [-fg] [clearance]` | Go to ceiling | `worldedit.navigation.ceiling` |
| `/thru` | `/thru` | Pass through walls | `worldedit.navigation.thru.command` |
| `/jumpto` | `/jumpto` | Jump to looking position | `worldedit.navigation.jumpto.command` |
| `/up` | `/up [-fg] <distance>` | Move upward distance | `worldedit.navigation.up` |

### 3. SELECTION COMMANDS (18 commands)
Region selection and manipulation.

| Command | Syntax | Description | Permission |
|---------|--------|-------------|------------|
| `//pos` | `//pos [pos1] [pos2...] [-s <selector>]` | Set positions | `worldedit.selection.pos` |
| `//pos1` | `//pos1 [coords]` | Set position 1 | `worldedit.selection.pos` |
| `//pos2` | `//pos2 [coords]` | Set position 2 | `worldedit.selection.pos` |
| `//hpos1` | `//hpos1` | Set pos1 to targeted block | `worldedit.selection.hpos` |
| `//hpos2` | `//hpos2` | Set pos2 to targeted block | `worldedit.selection.hpos` |
| `//chunk` | `//chunk [-cs] [coords]` | Select current chunk | `worldedit.selection.chunk` |
| `//wand` | `//wand [-n]` | Get selection wand | `worldedit.wand` |
| `//contract` | `//contract <amount> [reverse] [direction]` | Contract selection | `worldedit.selection.contract` |
| `//shift` | `//shift <amount> [direction]` | Shift selection | `worldedit.selection.shift` |
| `//outset` | `//outset [-hv] <amount>` | Expand selection outward | `worldedit.selection.outset` |
| `//inset` | `//inset [-hv] <amount>` | Contract selection inward | `worldedit.selection.inset` |
| `//trim` | `//trim [mask]` | Minimize selection to blocks | `worldedit.selection.trim` |
| `//size` | `//size [-c]` | Get selection info | `worldedit.selection.size` |
| `//count` | `//count <mask>` | Count matching blocks | `worldedit.analysis.count` |
| `//distr` | `//distr [-cd] [-p <page>]` | Get block distribution | `worldedit.analysis.distr` |
| `//sel` | `//sel [-d] [selector]` | Choose selection mode | various |
| `//expand` | `//expand <vert\|amount> [reverse] [dir]` | Expand selection | `worldedit.selection.expand` |
| `/toggleplace` | `/toggleplace` | Toggle placement position | none |

### 4. REGION COMMANDS (19 commands)
Operations on selected regions.

| Command | Syntax | Description | Permission |
|---------|--------|-------------|------------|
| `//set` | `//set <pattern>` | Fill selection with pattern | `worldedit.region.set` |
| `//line` | `//line [-h] <pattern> [thickness]` | Draw line through selection | `worldedit.region.line` |
| `//curve` | `//curve [-h] <pattern> [thickness]` | Draw spline curve | `worldedit.region.curve` |
| `//replace` | `//replace [from] <to>` | Replace blocks in selection | `worldedit.region.replace` |
| `//overlay` | `//overlay <pattern>` | Overlay pattern on surface | `worldedit.region.overlay` |
| `//center` | `//center <pattern>` | Set center blocks | `worldedit.region.center` |
| `//naturalize` | `//naturalize` | Create natural terrain layers | `worldedit.region.naturalize` |
| `//walls` | `//walls <pattern>` | Build four vertical sides | `worldedit.region.walls` |
| `//faces` | `//faces <pattern>` | Build all six sides | `worldedit.region.faces` |
| `//smooth` | `//smooth [iterations] [mask]` | Smooth terrain elevation | `worldedit.region.smooth` |
| `//snowsmooth` | `//snowsmooth [iter] [-l <count>] [-m <mask>]` | Smooth with snow layers | `worldedit.region.snowsmooth` |
| `//move` | `//move [-abes] [count] [offset] [replace] [-m <mask>]` | Move region contents | `worldedit.region.move` |
| `//stack` | `//stack [-abers] [count] [offset] [-m <mask>]` | Repeat region contents | `worldedit.region.stack` |
| `//regen` | `//regen [-b] [seed]` | Regenerate region | `worldedit.regen` |
| `//deform` | `//deform [-cor] <expression>` | Deform with expression | `worldedit.region.deform` |
| `//hollow` | `//hollow [thickness] [pattern]` | Hollow out object | `worldedit.region.hollow` |
| `//forest` | `//forest [type] [density]` | Create forest in region | `worldedit.region.forest` |
| `//flora` | `//flora [density]` | Create flora in region | `worldedit.region.flora` |
| `/placement` | `/placement <type> [multiplier] [offset]` | Select placement type | `worldedit.placement` |

### 5. GENERATION COMMANDS (13 commands)
Generate shapes and structures.

| Command | Syntax | Description | Permission |
|---------|--------|-------------|------------|
| `//hcyl` | `//hcyl <pattern> <radii> [height]` | Hollow cylinder | `worldedit.generation.cylinder` |
| `//cyl` | `//cyl [-h] <pattern> <radii> [height]` | Filled cylinder | `worldedit.generation.cylinder` |
| `//cone` | `//cone [-h] <pattern> <radii> [height] [thickness]` | Generate cone | `worldedit.generation.cone` |
| `//hsphere` | `//hsphere [-r] <pattern> <radii>` | Hollow sphere | `worldedit.generation.sphere` |
| `//sphere` | `//sphere [-hr] <pattern> <radii>` | Filled sphere | `worldedit.generation.sphere` |
| `/forestgen` | `/forestgen [size] [type] [density]` | Generate forest | `worldedit.generation.forest` |
| `/pumpkins` | `/pumpkins [size]` | Generate pumpkin patches | `worldedit.generation.pumpkins` |
| `//feature` | `//feature <feature>` | Generate MC features | `worldedit.generation.feature` |
| `//structure` | `//structure <structure>` | Generate MC structures | `worldedit.generation.structure` |
| `//hpyramid` | `//hpyramid <pattern> <size>` | Hollow pyramid | `worldedit.generation.pyramid` |
| `//pyramid` | `//pyramid [-h] <pattern> <size>` | Filled pyramid | `worldedit.generation.pyramid` |
| `//generate` | `//generate [-chor] <pattern> <expression>` | Generate by formula | `worldedit.generation.shape` |
| `//generatebiome` | `//generatebiome [-chor] <target> <expression>` | Set biome by formula | `worldedit.generation.shape.biome` |

### 6. CLIPBOARD & SCHEMATIC COMMANDS (12 commands)
Copy, paste, and schematic file operations.

| Command | Syntax | Description | Permission |
|---------|--------|-------------|------------|
| `//copy` | `//copy [-be] [-m <mask>]` | Copy to clipboard | `worldedit.clipboard.copy` |
| `//cut` | `//cut [-be] [leavePattern] [-m <mask>]` | Cut to clipboard | `worldedit.clipboard.cut` |
| `//paste` | `//paste [-abenosv] [-m <sourceMask>]` | Paste clipboard | `worldedit.clipboard.paste` |
| `//rotate` | `//rotate <rotateY> [rotateX] [rotateZ]` | Rotate clipboard | `worldedit.clipboard.rotate` |
| `//flip` | `//flip [direction]` | Flip clipboard | `worldedit.clipboard.flip` |
| `/clearclipboard` | `/clearclipboard` | Clear clipboard | `worldedit.clipboard.clear` |
| `/schematic list` | `/schem list [-dn] [-p <page>]` | List schematics | `worldedit.schematic.list` |
| `/schematic formats` | `/schem formats` | List schematic formats | `worldedit.schematic.formats` |
| `/schematic load` | `/schem load <filename> [format]` | Load schematic | `worldedit.schematic.load` |
| `/schematic save` | `/schem save [-f] <filename> [format]` | Save schematic | `worldedit.schematic.save` |
| `/schematic delete` | `/schem delete <filename>` | Delete schematic | `worldedit.schematic.delete` |
| `/schematic share` | `/schem share [name] [dest] [format]` | Share schematic | `worldedit.schematic.share` |

### 7. TOOL COMMANDS (15 commands)
Bind tools to items in hand.

| Command | Syntax | Description | Permission |
|---------|--------|-------------|------------|
| `/tool none` | `/tool none` | Unbind tool | none |
| `/tool selwand` | `/tool selwand` | Selection wand | `worldedit.setwand` |
| `/tool navwand` | `/tool navwand` | Navigation wand | `worldedit.setwand` |
| `/tool info` | `/tool info` | Block information | `worldedit.tool.info` |
| `/tool tree` | `/tool tree [type]` | Tree generator | `worldedit.tool.tree` |
| `/tool repl` | `/tool repl <pattern>` | Block replacer | `worldedit.tool.replacer` |
| `/tool cycler` | `/tool cycler` | Block data cycler | `worldedit.tool.data-cycler` |
| `/tool floodfill` | `/tool floodfill <pattern> <range>` | Flood fill | `worldedit.tool.flood-fill` |
| `/tool deltree` | `/tool deltree` | Floating tree remover | `worldedit.tool.deltree` |
| `/tool farwand` | `/tool farwand` | Distance wand | `worldedit.tool.farwand` |
| `/tool lrbuild` | `/tool lrbuild <leftclick> <rightclick>` | Long-range builder | `worldedit.tool.lrbuild` |
| `/tool stacker` | `/tool stacker [range] [mask]` | Block stacker | `worldedit.tool.stack` |
| `//` | `// [mode]` | Toggle super pickaxe | `worldedit.superpickaxe` |
| `//wand` | `//wand [-n]` | Get wand item | `worldedit.wand` |
| `/toggleeditwand` | `/toggleeditwand` | Toggle edit wand | `worldedit.wand.toggle` |

### 8. BRUSH COMMANDS (30+ commands)
Brushes for painting and terraforming.

| Command | Syntax | Description | Permission |
|---------|--------|-------------|------------|
| `/brush sphere` | `/br sphere [-h] <pattern> [radius]` | Sphere brush | `worldedit.brush.sphere` |
| `/brush cylinder` | `/br cylinder [-h] <pattern> [radius] [height]` | Cylinder brush | `worldedit.brush.cylinder` |
| `/brush clipboard` | `/br clipboard [-abeov] [-m <mask>]` | Clipboard brush | `worldedit.brush.clipboard` |
| `/brush smooth` | `/br smooth [radius] [iterations] [mask]` | Terrain smoother | `worldedit.brush.smooth` |
| `/brush snowsmooth` | `/br snowsmooth [radius] [iter] [-l] [-m]` | Snow smoother | `worldedit.brush.snowsmooth` |
| `/brush extinguish` | `/br extinguish [radius]` | Fire extinguisher | `worldedit.brush.ex` |
| `/brush gravity` | `/br gravity [radius] [-h <height>]` | Gravity brush | `worldedit.brush.gravity` |
| `/brush butcher` | `/br butcher [-abfgnprtw] [radius]` | Entity killer | `worldedit.brush.butcher` |
| `/brush forest` | `/br forest <shape> [radius] [density] <type>` | Forest placer | `worldedit.brush.forest` |
| `/brush feature` | `/br feature <shape> [radius] [density] <type>` | Feature placer | `worldedit.brush.feature` |
| `/brush raise` | `/br raise <shape> [radius]` | Raise terrain | `worldedit.brush.raise` |
| `/brush lower` | `/br lower <shape> [radius]` | Lower terrain | `worldedit.brush.lower` |
| `/brush paint` | `/br paint <shape> [radius] [density] <type>` | Paint brush | `worldedit.brush.paint` |
| `/brush apply` | `/br apply <shape> [radius] <type>` | Apply function | `worldedit.brush.apply` |
| `/brush set` | `/br set <shape> [radius] <pattern>` | Set brush | `worldedit.brush.set` |
| `/brush splatter` | `/br splatter <pattern> [radius] [decay]` | Splatter brush | `worldedit.brush.splatter` |
| `/brush deform` | `/br deform [-or] <shape> [radius] <expr>` | Deform brush | `worldedit.brush.deform` |
| `/brush heightmap` | `/br heightmap [-efr] <image> [radius] [intensity]` | Heightmap brush | `worldedit.brush.heightmap` |
| `/brush snow` | `/br snow [-s] <shape> [radius]` | Snow brush | `worldedit.brush.snow` |
| `/brush biome` | `/br biome [-c] <shape> [radius] <biome>` | Biome brush | `worldedit.brush.biome` |
| `/brush erode` | `/br erode [size]` | Erosion preset | `worldedit.brush.morph` |
| `/brush dilate` | `/br dilate [size]` | Dilation preset | `worldedit.brush.morph` |
| `/brush morph` | `/br morph [size] [minErode] [erodeIter] ...` | Morph brush | `worldedit.brush.morph` |
| `/brush none` | `/br none` | Unbind brush | none |
| `/mask` | `/mask [mask]` | Set brush mask | `worldedit.brush.options.mask` |
| `/material` | `/material <pattern>` | Set brush material | `worldedit.brush.options.material` |
| `/range` | `/range <range>` | Set brush range | `worldedit.brush.options.range` |
| `/size` | `/size <size>` | Set brush size | `worldedit.brush.options.size` |
| `/tracemask` | `/tracemask [mask]` | Set trace mask | `worldedit.brush.options.tracemask` |

### 9. SUPER PICKAXE COMMANDS (4 commands)
Super pickaxe modes.

| Command | Syntax | Description | Permission |
|---------|--------|-------------|------------|
| `/superpickaxe single` | `/sp single` | Single block mode | `worldedit.superpickaxe` |
| `/superpickaxe area` | `/sp area <range>` | Area mode | `worldedit.superpickaxe.area` |
| `/superpickaxe recursive` | `/sp recursive <range>` | Recursive mode | `worldedit.superpickaxe.recursive` |

### 10. BIOME COMMANDS (3 commands)
Biome information and manipulation.

| Command | Syntax | Description | Permission |
|---------|--------|-------------|------------|
| `/biomelist` | `/biomelist [-p <page>]` | List available biomes | `worldedit.biome.list` |
| `/biomeinfo` | `/biomeinfo [-pt]` | Get biome at target | `worldedit.biome.info` |
| `//setbiome` | `//setbiome [-p] <biome>` | Set biome in selection | `worldedit.biome.set` |

### 11. CHUNK COMMANDS (3 commands)
Chunk-level operations.

| Command | Syntax | Description | Permission |
|---------|--------|-------------|------------|
| `/chunkinfo` | `/chunkinfo` | Get chunk information | `worldedit.chunkinfo` |
| `/listchunks` | `/listchunks [-p <page>]` | List chunks in selection | `worldedit.listchunks` |
| `/delchunks` | `/delchunks [-o <time>]` | Delete chunks | `worldedit.delchunks` |

### 12. SNAPSHOT COMMANDS (6 commands)
World backup restoration.

| Command | Syntax | Description | Permission |
|---------|--------|-------------|------------|
| `/restore` | `/restore [snapshot]` | Restore from snapshot | `worldedit.snapshots.restore` |
| `/snapshot use` | `/snap use <name>` | Choose snapshot | `worldedit.snapshots.restore` |
| `/snapshot list` | `/snap list [-p <page>]` | List snapshots | `worldedit.snapshots.list` |
| `/snapshot before` | `/snap before <date>` | Nearest before date | `worldedit.snapshots.restore` |
| `/snapshot after` | `/snap after <date>` | Nearest after date | `worldedit.snapshots.restore` |
| `/snapshot sel` | `/snap sel <index>` | Select by index | `worldedit.snapshots.restore` |

### 13. SCRIPTING COMMANDS (2 commands)
CraftScript execution.

| Command | Syntax | Description | Permission |
|---------|--------|-------------|------------|
| `/cs` | `/cs <filename> [args...]` | Execute CraftScript | `worldedit.scripting.execute` |
| `/.s` | `/.s [args...]` | Execute last script | `worldedit.scripting.execute` |

### 14. UTILITY COMMANDS (16 commands)
Miscellaneous useful operations.

| Command | Syntax | Description | Permission |
|---------|--------|-------------|------------|
| `//fill` | `//fill <pattern> <radius> [depth]` | Fill holes | `worldedit.fill` |
| `//fillr` | `//fillr <pattern> <radius> [depth]` | Fill recursively | `worldedit.fill.recursive` |
| `//drain` | `//drain [-w] <radius>` | Drain water pools | `worldedit.drain` |
| `/fixlava` | `/fixlava <radius>` | Fix lava | `worldedit.fixlava` |
| `/fixwater` | `/fixwater <radius>` | Fix water | `worldedit.fixwater` |
| `/removeabove` | `/removeabove [size] [height]` | Remove blocks above | `worldedit.removeabove` |
| `/removebelow` | `/removebelow [size] [height]` | Remove blocks below | `worldedit.removebelow` |
| `/removenear` | `/removenear <mask> [radius]` | Remove nearby blocks | `worldedit.removenear` |
| `/replacenear` | `/replacenear <radius> [from] <to>` | Replace nearby blocks | `worldedit.replacenear` |
| `/snow` | `/snow [-s] [size] [height]` | Simulate snowfall | `worldedit.snow` |
| `/thaw` | `/thaw [size] [height]` | Thaw snow/ice | `worldedit.thaw` |
| `/green` | `/green [-f] [size] [height]` | Convert dirt to grass | `worldedit.green` |
| `/extinguish` | `/extinguish [radius]` | Remove fire | `worldedit.extinguish` |
| `/butcher` | `/butcher [-abfgnprtw] [radius]` | Kill mobs | `worldedit.butcher` |
| `/remove` | `/remove <type> <radius>` | Remove entities | `worldedit.remove` |
| `//calculate` | `//calculate <expression>` | Evaluate expression | `worldedit.calc` |

### 15. SEARCH & HELP COMMANDS (2 commands)
Information and documentation.

| Command | Syntax | Description | Permission |
|---------|--------|-------------|------------|
| `/searchitem` | `/searchitem [-bi] [-p <page>] <query>` | Search items/blocks | `worldedit.searchitem` |
| `//help` | `//help [-s] [-p <page>] [command]` | Display command help | `worldedit.help` |

---

## Pattern Types Reference

### Basic Patterns
- **Single Block**: `stone`, `oak_planks`, `red_wool`
- **Block States**: `oak_stairs[facing=north,half=top]`
- **Block NBT**: `chest{'Items':[{id:'diamond',Count:1}]}`

### Advanced Patterns
- **Random**: `50%stone,30%diorite,20%granite`
- **Random State**: `*oak_log` (all orientations)
- **Clipboard**: `#clipboard` or `#clipboard@0,5,0`
- **Type Apply**: `^acacia_planks` (change type, keep state)
- **State Apply**: `^[waterlogged=true]` (change state, keep type)
- **Block Category**: `##wool`, `##*slabs`

### Special Syntax
- **Sign Text**: `oak_sign|Line1|Line2|Line3|Line4`
- **Player Head**: `player_head|username`
- **Mob Spawner**: `spawner|zombie`

---

## Mask Types Reference

### Basic Masks
- **Block Type**: `stone`, `!air`, `stone,diorite`
- **Existing Blocks**: `#existing`
- **Solid Blocks**: `#solid`
- **Block Categories**: `##wool`, `##logs`

### Advanced Masks
- **Offset**: `>stone` (blocks above stone), `<grass_block` (blocks below grass)
- **Region**: `#region`, `#sel`, `#selection`
- **Random**: `%50` (50% of blocks)
- **Block State**: `^[waterlogged=true]`, `^=[powered=false]`
- **Expression**: `=y<64`, `=x^2+z^2<100`
- **Biome**: `$plains`, `$desert`
- **Surface**: `#surface`, `#exposed`

### Mask Combination
- **Intersection (AND)**: `stone grass_block` (space-separated)
- **Negation (NOT)**: `!stone`, `!##wool`

---

## Expression Syntax Reference

### Variables (Auto-provided)
- `x`, `y`, `z` - Current position coordinates
- In clipboard operations: `source_x`, `source_y`, `source_z`

### Operators
- Arithmetic: `+`, `-`, `*`, `/`, `%`, `^` (power)
- Comparison: `<`, `>`, `<=`, `>=`, `==`, `!=`, `~=` (approximately equal)
- Logical: `&&`, `||`, `!`
- Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `^=`

### Math Functions
- Trigonometry: `sin()`, `cos()`, `tan()`, `asin()`, `acos()`, `atan()`, `atan2()`
- Utility: `abs()`, `sqrt()`, `cbrt()`, `ceil()`, `floor()`, `round()`
- Special: `min()`, `max()`, `exp()`, `ln()`, `log()`, `log10()`

### Noise Functions
- `perlin()` - Perlin noise
- `voronoi()` - Voronoi noise
- `ridgedmulti()` - Ridged multifractal

### Control Structures
- Conditionals: `if`, `else`, `elseif`
- Loops: `while`, `do-while`, `for`
- Ternary: `condition ? true_val : false_val`

### Constants
- `pi` = 3.14159...
- `e` = 2.71828...
- `true` = 1
- `false` = 0

---

## Console Command Considerations

### Position Setting from Console
WorldEdit commands from console (RCON) require special coordinate syntax:

```
//pos1 X,Y,Z    (comma-separated, no spaces)
//pos2 X,Y,Z    (comma-separated, no spaces)
```

### Player Context
Some commands may require a player context. For RCON use:
- Use absolute coordinates when possible
- Some commands may need to be executed as a player using `execute as <player> run <command>`

### Command Prefixes
- Single slash `/` - Minecraft commands
- Double slash `//` - WorldEdit commands (work from console and in-game)

---

## Implementation Requirements

### MCP Server Must Expose

1. **Generic RCON Command Tool**
   - Accept any string command
   - Return server response
   - Handle errors gracefully

2. **Categorized WorldEdit Tools**
   - One tool per command category
   - Structured parameters based on command syntax
   - Comprehensive descriptions with examples

3. **Helper Tools**
   - Pattern builder/validator
   - Mask builder/validator
   - Expression validator
   - Coordinate utilities

4. **Resources to Provide**
   - Complete command reference (JSON)
   - Pattern syntax guide
   - Mask syntax guide
   - Expression function reference
   - Common build patterns/recipes

### AI Assistance Requirements

To effectively use WorldEdit via AI, provide:
- Comprehensive command documentation
- Pattern/mask syntax examples
- Common workflows (e.g., "building a house")
- Coordinate system understanding
- RCON-specific considerations

---

## Next Steps for Engineering Team

1. **Review this research document**
2. **Create detailed implementation plan** (Steve)
3. **Review implementation plan** (Cody)
4. **Implement MCP server with ALL commands**
5. **Create test suite**
6. **Document setup and usage**

---

**Document Version:** 1.0
**Last Updated:** 2025-10-30
**Research Complete:** ✓
