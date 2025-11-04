# TOON Minecraft Items - Project Summary

## What Was Done

Successfully converted Minecraft 1.21.3 items database to token-efficient TOON format and created a Python playground for analysis.

## Files Created

### 1. Core Data Files
- **`minecraft_items.json`** (169,898 bytes)
  - Original JSON from PrismarineJS minecraft-data
  - 1,375 Minecraft items with id, name, displayName, stackSize

- **`minecraft_items_toon.txt`** (131,729 bytes)
  - TOON format conversion
  - **22.5% smaller** than JSON
  - **~9,542 fewer tokens** for LLM processing

### 2. Python Playground
- **`toon/python_playground.py`**
  - Analyzes Minecraft items data
  - Creates color-organized palettes
  - Extracts building blocks
  - Generates Claude-friendly exports
  - Compares JSON vs TOON efficiency

### 3. Generated Resources
- **`minecraft_blocks_essential.md`**
  - 16 essential building blocks
  - Includes usage hints
  - Ready to add to VibeCraft

### 4. TOON Repository
- **`toon/`** (cloned from https://github.com/johannschopplich/toon)
  - Token-Oriented Object Notation library
  - Optimized for LLM token efficiency
  - CLI tool for JSON to TOON conversion

## Key Statistics

### Data Efficiency
```
JSON:  169,898 bytes (~42,474 tokens)
TOON:  131,729 bytes (~32,932 tokens)
─────────────────────────────────────
Savings: 38,169 bytes (22.5% reduction)
         ~9,542 tokens saved
```

### Minecraft Items Breakdown
- **Total items**: 1,375
- **Stackable (64)**: 1,125 items (82%)
- **Stackable (16)**: 47 items (3%)
- **Stackable (1)**: 203 items (15%)

### Building Blocks
- **Total building blocks**: 297
- **Color categories**: 10 colors
- **Material types**:
  - Stone variants: 91
  - Bricks: 35
  - Glass: 37
  - Terracotta: 33
  - Concrete: 32
  - Wood types: 23
  - Logs: 18
  - Wool: 16
  - Planks: 12

## Python Playground Features

### 1. Item Analysis
- Stack size distribution
- Category grouping (building, wood, weapons, tools)
- Item statistics

### 2. Color Palette
- Organizes blocks by color
- 10 color categories (white, gray, black, brown, red, orange, yellow, green, blue, purple)
- Perfect for aesthetic building

### 3. Building Blocks
- Extracts 297 building-specific blocks
- Groups by material type
- Shows variants for each category

### 4. Essential Blocks Export
- Creates curated list of common blocks
- Adds usage hints (modern, medieval, etc.)
- Formatted for Claude integration

### 5. Format Comparison
- Measures JSON vs TOON efficiency
- Calculates token savings
- Shows space reduction

## How to Use

### Run the Python Playground
```bash
cd /Users/er/Repos/vibecraft/toon
python3 python_playground.py
```

### Convert JSON to TOON
```bash
cd /Users/er/Repos/vibecraft/toon
node bin/toon.mjs ../minecraft_items.json > output.toon
```

### Access the Data
- **JSON**: `/Users/er/Repos/vibecraft/minecraft_items.json`
- **TOON**: `/Users/er/Repos/vibecraft/minecraft_items_toon.txt`
- **Essential blocks**: `/Users/er/Repos/vibecraft/minecraft_blocks_essential.md`

## Integration with VibeCraft

### Option 1: Add to CLAUDE.md
Add essential blocks section:
```markdown
## Minecraft Building Blocks

### Common Materials
- **Cobblestone** (id: 35) - Medieval, rustic, foundations
- **Stone Bricks** (id: 353) - Refined builds, formal structures
- **Oak Planks** (id: 36) - Warm interiors, traditional
- **White Concrete** (id: 569) - Modern, clean aesthetic
[...]
```

### Option 2: Create MCP Resource
Add as `vibecraft://blocks` resource:
- Use TOON format for efficiency
- ~9,500 fewer tokens than JSON
- Full 1,375 item database available

### Option 3: Curated Lists
Create targeted resources:
- `vibecraft://blocks-building` - 297 building blocks
- `vibecraft://blocks-essential` - 16 most common
- `vibecraft://blocks-colors` - Organized by color

## Benefits for VibeCraft

### 1. Block Knowledge
Claude now knows:
- All 1,375 Minecraft items by ID and name
- Stack sizes for inventory planning
- Color organization for palettes
- Building material categories

### 2. Better Suggestions
- "Build in gray" → knows stone_bricks, andesite, gray_concrete
- "Modern aesthetic" → suggests white_concrete, glass
- "Medieval castle" → recommends cobblestone, stone_bricks

### 3. Token Efficiency
- TOON format saves 22.5% tokens
- Can include full database without token explosion
- More room for other context

### 4. Material Awareness
- Knows which blocks stack (most stack to 64)
- Understands non-stackable items (tools, weapons)
- Can plan inventory efficiently

## Sample Python Output

### Color Palette
```
WHITE (15 items):
  - white_wool
  - white_terracotta
  - white_concrete
  - white_stained_glass
  [...]

GRAY (28 items):
  - gray_wool
  - gray_concrete
  - light_gray_terracotta
  [...]
```

### Building Blocks
```
CONCRETE (32 variants):
  - White Concrete (id: 569)
  - Gray Concrete (id: 576)
  - Black Concrete (id: 581)
  [...]

STONE (91 variants):
  - Stone (id: 1)
  - Cobblestone (id: 35)
  - Stone Bricks (id: 353)
  [...]
```

## Next Steps

### Immediate
1. ✅ JSON downloaded and converted to TOON
2. ✅ Python playground created and tested
3. ✅ Essential blocks extracted

### Recommended
1. **Add to CLAUDE.md** - Include essential blocks list
2. **Create MCP resource** - Add full TOON database as `vibecraft://blocks`
3. **Test with Claude** - Verify improved block suggestions

### Optional
1. Add block properties (hardness, blast resistance, flammable)
2. Create texture family groupings
3. Add biome-specific material lists
4. Include crafting recipes

## Technical Details

### TOON Format Structure
```
[1375]:
  - id: 0
    name: air
    displayName: Air
    stackSize: 64
  - id: 1
    name: stone
    displayName: Stone
    stackSize: 64
  [...]
```

### Why TOON?
- **Compact**: 22.5% smaller than JSON
- **Readable**: Human-friendly format
- **Structured**: Maintains data integrity
- **LLM-optimized**: Designed for AI prompts
- **Tabular**: Perfect for uniform arrays

### Format Comparison
| Format | Size | Tokens | Use Case |
|--------|------|--------|----------|
| JSON | 169,898 bytes | ~42,474 | Standard API responses |
| TOON | 131,729 bytes | ~32,932 | LLM context, data-heavy prompts |
| Savings | 38,169 bytes | ~9,542 | **22.5% reduction** |

## Resources

### Links
- TOON Repo: https://github.com/johannschopplich/toon
- Minecraft Data: https://github.com/PrismarineJS/minecraft-data
- TOON Spec: https://github.com/johannschopplich/toon/blob/main/SPEC.md

### Files
- Python Playground: `toon/python_playground.py`
- Items JSON: `minecraft_items.json`
- Items TOON: `minecraft_items_toon.txt`
- Essential Blocks: `minecraft_blocks_essential.md`

## Conclusion

Successfully created a token-efficient Minecraft items database using TOON format, with a Python playground for analysis and extraction of building-relevant data. The TOON format provides 22.5% token savings while maintaining full data fidelity, making it perfect for LLM context.

**Ready to integrate into VibeCraft!** 🎮✨

---

**Created**: October 31, 2025
**Minecraft Version**: 1.21.3
**Items Count**: 1,375
**Format**: TOON (Token-Oriented Object Notation)
