# WorldEdit Recipe Book (VibeCraft Edition)

Curated building playbook adapted from the ManaCube Advanced WorldEdit guide, tailored for VibeCraft's MCP tools. Every recipe below maps directly to a supported tool, so Claude can execute it safely through the MCP server.

> **Tool Key**
>
> - `sel` → `worldedit_selection`
> - `region` → `worldedit_region`
> - `gen` → `worldedit_generation`
> - `clip` → `worldedit_clipboard`
> - `schem` → `worldedit_schematic`
> - `hist` → `worldedit_history`
> - `util` → `worldedit_utility`
> - `biome` → `worldedit_biome`
> - `brush` → `worldedit_brush`
> - `general` → `worldedit_general`
> - `nav` → `worldedit_navigation`
> - `chunk` → `worldedit_chunk`
> - `snapshot` → `worldedit_snapshot`
> - `script` → `worldedit_scripting`
> - `ref` → `worldedit_reference`
> - `tools` → `worldedit_tools`
> - `rcon` → `rcon_command` (fallback for anything else)

---

## 1. Selection & Region Recipes

### Expand / Contract Towers
- Tool: `sel`
- Flow:
  1. `//pos1 100,64,100`
  2. `//pos2 110,70,110`
  3. `//expand vert` – maximizes tower height.
  4. `//contract 2 up` – trims roof space.

### Hollow Shell in One Shot
- Tool: `region`
- Commands:
  - `//set stone_bricks`
  - `//hollow 1`

### Wall Banding
- Tool: `region`
- Commands:
  1. `//stack 1 up`
  2. `//replace stone 70%stone,30%cracked_stone_bricks`
  3. `//overlay stone_brick_slab`

### Organic Arch / Bridge
- Tool: `region`
- Commands:
  1. `//curve spruce_log 2`
  2. `//line spruce_planks 3`
  3. `//stack 2 forward`

### Smooth Terrain Pads
- Tool: `region`
- Commands:
  - `//naturalize`
  - `//smooth 3`

## 2. Pattern & Mask Recipes

### Gradient Facade
- Tool: `region`
- Pattern: `30%stone_bricks,25%stone,25%andesite,20%cobblestone`
- Command: `//replace stone_bricks 30%stone_bricks,25%stone,25%andesite,20%cobblestone`

### Targeted Replacement
- Tools: `region` + mask parameter `-m`
- Command: `//set calcite -m #surface`

### Layered Snow Cap
- Tool: `region`
- Command: `//set snow_block -m >stone`

### Biome Striping
- Tool: `biome`
- Commands:
  1. `//pos1 ...`, `//pos2 ...`
  2. `//setbiome minecraft:grove`

## 3. Generation Recipes

### Dome + Oculus
- Tool: `gen`
- Commands:
  1. `//sphere glass 12`
  2. `//hsphere dark_prismarine 12`
  3. `//replace glass air -m %30` (random opening)

### Mountain Outcrop
- Tool: `gen`
- Commands:
  1. `//pos1 base`, `//pos2 top`
  2. `//generate stone y < 80 + perlin(x*0.1,z*0.1)*18`
  3. `//deform y+=sin(x*0.08)*1.5`
  4. `//overlay grass_block`

### Crystal Spire
- Tool: `gen`
- Commands:
  - `//cyl packed_ice 4 25`
  - `//cone light_blue_stained_glass 0 30`
  - `//stack 1 up`

## 4. Clipboard & Schematic Recipes

### Modular Tower Duplication
- Tools: `clip`, `schem`
- Flow:
  1. `//pos1`, `//pos2`
  2. `//copy -e -b`
  3. `//stack 3 up`
  4. `//schem save tower_core`

### Mirror Build Across Axis
- Tool: `clip`
- Commands:
  1. `//copy`
  2. `//flip x`
  3. `//paste -o`

### Prefab Library Refresh
- Tool: `schem`
- Commands:
  - `/schem list`
  - `/schem load cathedral`
  - `//paste -a`

## 5. Brush Workflows

### Rock Spikes
- Tool: `brush`
- Commands:
  1. `/br cylinder stone 2 8`
  2. `/mask dirt,stone`
  3. `/range 30`
  4. `/size 6`

### Forest Scatter
- Tool: `brush`
- Commands:
  1. `/br paint sphere 12 40 forest oak`
  2. `/mask grass_block`

### Terrain Carving
- Tool: `brush`
- Commands:
  1. `/br smooth 10 4`
  2. `/mask #solid`
  3. `/br gravity 6`

## 6. Navigation & Utility Recipes

### Rapid Layer Placement
- Tools: `nav`, `region`
- Commands:
  - `/up 15`
  - `//pos1 ~0,~0,~0`
  - `//pos2 ~10,~-5,~10`

### Flood Fill Caverns
- Tool: `util`
- Commands:
  - `//fill water 6`
  - `//drain 6`

### Lighting Pass
- Tool: `util`
- Commands:
  - `/removenear fire 50`
  - `/extinguish 50`
  - `//calc 4*PI*radius^2` (optional math check)

## 7. Snapshots, Scripts & Reference

### Snapshot Safety Net
- Tool: `snapshot`
- Commands:
  1. `/snap list`
  2. `/snap use latest`
  3. `/restore` (warn player before running)

### CraftScript Automation
- Tool: `script`
- Commands:
  1. `/cs spiral.js 12`
  2. `/cs floodfill.js water`

### Live Syntax Lookup
- Tool: `ref`
- Commands:
  - `/searchitem crimson`
  - `//help deform`

## 8. Chunk & Global Controls

### Chunk Cleanup
- Tool: `chunk`
- Commands:
  - `/listchunks`
  - `/delchunks -o 7d`

### Global Mask & Limits
- Tool: `general`
- Commands:
  - `//gmask !air`
  - `//limit 500000`

### Undo Insurance
- Tool: `hist`
- Commands:
  - `//undo`
  - `//redo`
  - `//clearhistory`

---

## Coverage Checklist

| Feature | Commands Used | MCP Tool | Status |
|---------|---------------|----------|--------|
| Advanced selections | `//expand`, `//contract`, `//size` | `worldedit_selection` | ✅ |
| Region transforms | `//set`, `//hollow`, `//replace`, `//stack`, `//naturalize`, `//smooth` | `worldedit_region` | ✅ |
| Expression generation | `//generate`, `//deform`, `//overlay` | `worldedit_generation` | ✅ |
| Clipboard workflows | `//copy`, `//paste`, `//flip`, `/schem save/load` | `worldedit_clipboard`, `worldedit_schematic` | ✅ |
| Brush systems | `/br` suite, `/mask`, `/range`, `/size` | `worldedit_brush`, `worldedit_tools` | ✅ |
| Utilities | `//fill`, `//drain`, `/extinguish`, `/calc` | `worldedit_utility` | ✅ |
| Biome edits | `//setbiome`, `/biomelist` | `worldedit_biome` | ✅ |
| Navigation | `/up`, `/ascend`, `/thru` | `worldedit_navigation` | ✅ |
| Snapshots | `/snap list/use`, `/restore` | `worldedit_snapshot` | ✅ |
| CraftScripts | `/cs`, `/.s` | `worldedit_scripting` | ✅ |
| Chunk management | `/listchunks`, `/delchunks` | `worldedit_chunk` | ✅ |
| Global settings | `//gmask`, `//limit`, `/worldedit` | `worldedit_general` | ✅ |
| History | `//undo`, `//redo`, `//clearhistory` | `worldedit_history` | ✅ |
| Reference | `/searchitem`, `//help` | `worldedit_reference` | ✅ |

All recipes rely on commands exposed via the VibeCraft MCP server (see `mcp-server/src/vibecraft/server.py`).

---

## Usage Tips for Claude

1. **Announce the recipe** you are executing (e.g., “Applying Mountain Outcrop recipe”).
2. **Reference the tool name** when calling MCP actions to avoid generic `rcon_command` unless necessary.
3. **Warn players** before destructive actions (`/delchunks`, `/restore`).
4. **Undo plan**: After large edits, remind the user about `//undo` availability.
5. **Customize patterns**: The gradients provided are templates—adjust block palettes to match user style.

