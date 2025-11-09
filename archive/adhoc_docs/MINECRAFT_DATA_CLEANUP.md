# Minecraft Data Files Cleanup

**Date**: 2025-11-05
**Action**: Moved minecraft_items*.json files to context directory

---

## What Was Done

Relocated Minecraft item database files from project root to the appropriate data directory.

## Files Moved

From root → `context/`:

1. **minecraft_items_filtered.json** (138KB, 7,662 items)
   - Actively used by server.py for `search_minecraft_item` tool
   - Powers block/item search functionality
   - Now correctly located with other reference data

2. **minecraft_items.json** (166KB, 9,037 items)
   - Unfiltered source version
   - Kept for data processing workflows
   - Referenced only by gitignored playground scripts

## Code Changes

**mcp-server/src/vibecraft/server.py** (line 66):
```python
# Before:
items_file = Path(__file__).parent.parent.parent.parent / "minecraft_items_filtered.json"

# After:
items_file = CONTEXT_DIR / "minecraft_items_filtered.json"
```

**Benefits**:
- Cleaner path resolution (uses CONTEXT_DIR constant)
- More maintainable (no fragile parent.parent.parent chain)
- Consistent with other data files (all in context/)

## Documentation Updated

**context/README.md**:
- Added documentation for both JSON files
- Explained relationship (unfiltered source → filtered active)
- Noted which is used by production code
- Updated item counts (7,662 filtered, 9,037 unfiltered)

## Why This Location?

The `context/` directory is the established location for all reference data:
- ✅ `minecraft_items_filtered.json` - Item database (NOW HERE)
- ✅ `minecraft_items.json` - Source file (NOW HERE)
- ✅ `minecraft_items.txt` - TOON format items
- ✅ `minecraft_furniture_catalog.json` - Furniture database
- ✅ `minecraft_material_palettes.json` - Material palettes
- ✅ `minecraft_scale_reference.txt` - Architectural dimensions
- ✅ `worldedit_recipe_book.md` - Command recipes

**Result**: All reference data in one organized location

---

## Before vs After

**Before**:
```
vibecraft/
├── minecraft_items.json          ← WRONG location (root)
├── minecraft_items_filtered.json ← WRONG location (root)
├── context/
│   ├── minecraft_items.txt
│   └── (other data files)
└── mcp-server/
    └── src/vibecraft/server.py  ← Complex path: ../../../../minecraft_items_filtered.json
```

**After**:
```
vibecraft/
├── context/
│   ├── minecraft_items.json          ← Organized with data files
│   ├── minecraft_items_filtered.json ← Organized with data files
│   ├── minecraft_items.txt
│   └── (other data files)
└── mcp-server/
    └── src/vibecraft/server.py  ← Clean path: CONTEXT_DIR / "minecraft_items_filtered.json"
```

---

**Result**: Clean root directory, organized data files, maintainable code paths! ✨
