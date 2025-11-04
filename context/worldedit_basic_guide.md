# WorldEdit for Beginners (Quick Reference)

Adapted from ManaCube's “WorldEdit for Beginners” guide and aligned with VibeCraft's MCP toolset. Designed to give Claude a concise onboarding to core commands, selection mechanics, and safety habits.

---

## 1. Getting Started

- **Enable WorldEdit** – Players need the WorldEdit wand (`//wand`) and proper permissions. Claude uses the MCP server through `worldedit_selection` for the same effect.
- **Wand Alternatives** – Console/RCON must rely on coordinates: `//pos1 x,y,z`, `//pos2 x,y,z` (comma separated!).
- **Selections** – Always define pos1/pos2 before running region commands.

**Tool mapping:** `worldedit_selection`

Common commands:
```
//wand               # Give selection wand (players)
//pos1 100,64,100    # Corner 1
//pos2 110,70,110    # Corner 2
//size               # Selection summary
```

---

## 2. Editing the Selected Region

**Fill & Replace** – Use `//set` and `//replace` with block IDs or patterns.
```
//set stone_bricks
//replace stone_bricks 70%stone_bricks,30%cracked_stone_bricks
```

**Hollow & Walls**
```
//walls oak_planks
//faces stone
//hollow 1
```

**Stack & Move**
```
//stack 3 north
//move 5 up -s
```

**Tool mapping:** `worldedit_region`

---

## 3. Copy, Paste, and Schematics

**Clipboard Basics**
```
//copy -e -b    # Copy selection with entities and biomes
//cut -a        # Cut selection, skip air
//paste -a -o   # Paste at original offset, skip air
```

**Rotate / Flip**
```
//rotate 90
//flip x
```

**Schematics**
```
/schem save castle_keep
/schem load castle_keep
//paste -a
```

**Tool mapping:** `worldedit_clipboard`, `worldedit_schematic`

---

## 4. Undo, Redo, and Safety Nets

```
//undo          # Step back one change
//redo          # Reapply undone change
//clearhistory  # Free memory (rare)
```

**Tool mapping:** `worldedit_history`

Tips:
- Always confirm selection with `//size` before running large edits.
- Keep track of successive edits so `//undo` restores the correct step.
- For massive operations, set a limit via `//limit 250000` (tool: `worldedit_general`).

---

## 5. Masks, Patterns, and Brushes (Intro)

- **Masks (`-m`)** limit commands to targeted blocks. Example: `//set cobblestone -m !air`.
- **Patterns** combine multiple blocks: `50%stone,30%cobblestone,20%andesite`.
- **Brushes** allow click-based editing; they still require player context but Claude can configure them via console:
```
/br sphere stone 4
/mask dirt,grass_block
/size 10
```

**Tool mapping:** `worldedit_region` (mask usage), `worldedit_tools`, `worldedit_brush`

---

## 6. Helpful Utility Commands

```
//naturalize             # Soil/grass layering
//smooth 3               # Averages terrain
//drain 10               # Remove water/lava
/fixwater 20             # Fix water sources
/extinguish 50           # Remove fire
```

**Tool mapping:** `worldedit_utility`

---

## 7. Quick Reference Table

| Beginner Task | Command | MCP Tool | Status |
|---------------|---------|----------|--------|
| Create selection | `//pos1`, `//pos2`, `//size` | `worldedit_selection` | ✅ |
| Fill / replace | `//set`, `//replace` | `worldedit_region` | ✅ |
| Build walls / hollow | `//walls`, `//hollow` | `worldedit_region` | ✅ |
| Stack / move | `//stack`, `//move` | `worldedit_region` | ✅ |
| Copy & paste | `//copy`, `//paste`, `//rotate`, `//flip` | `worldedit_clipboard` | ✅ |
| Schematics | `/schem save/load` | `worldedit_schematic` | ✅ |
| Undo / redo | `//undo`, `//redo`, `//clearhistory` | `worldedit_history` | ✅ |
| Set limits | `//limit` | `worldedit_general` | ✅ |
| Masks | `-m`, `//gmask` | `worldedit_region`, `worldedit_general` | ✅ |
| Brushes | `/br`, `/mask`, `/size` | `worldedit_brush`, `worldedit_tools` | ✅ |
| Utilities | `//smooth`, `//drain`, `/fixwater` | `worldedit_utility` | ✅ |

All commands correspond to functionality exposed in `mcp-server/src/vibecraft/server.py`.

---

## Habit Checklist for Claude

1. **State the selection**: confirm coords before editing.
2. **Preview with `//size`**: ensures expectations match the selection size.
3. **Use limits for bulk work**: `//limit` prevents accidental mega-fills.
4. **Call the correct tool**: prefer specialized tools over raw `rcon_command`.
5. **Announce undo plan**: remind users `//undo` exists after big edits.

