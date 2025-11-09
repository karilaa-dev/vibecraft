# Context Directory Deep Analysis

**Date**: 2025-11-05
**Purpose**: Understand every file in context/, identify redundancy, clean up

---

## Current Files (14 files, 602KB total)

### Files Actually Loaded by Production Code ✅

**Loaded in server.py:**
1. ✅ `minecraft_items_filtered.json` (138KB) - Item search tool
   - **Used by**: `load_minecraft_items()` function
   - **Purpose**: Powers `search_minecraft_item` MCP tool
   - **KEEP**: Critical for production

2. ✅ `minecraft_furniture_layouts.json` (78KB) - Furniture placer
   - **Used by**: `load_furniture_layouts()` function
   - **Purpose**: Automated furniture placement
   - **KEEP**: Critical for furniture tools

3. ✅ `minecraft_furniture_catalog.json` (115KB) - Furniture metadata
   - **Used by**: `load_furniture_catalog()` function
   - **Purpose**: Furniture descriptions and instructions
   - **KEEP**: Critical for furniture tools

4. ✅ `building_patterns_structured.json` (2.4KB) - Pattern blueprints
   - **Used by**: `load_structured_patterns()` function
   - **Purpose**: Automated pattern placement (4 patterns currently)
   - **KEEP**: Critical for pattern placement

**Loaded in tools/patterns.py:**
5. ✅ `building_patterns_complete.json` (22KB) - Pattern metadata
   - **Used by**: `building_pattern_lookup` tool
   - **Purpose**: Pattern search and discovery
   - **KEEP**: Critical for pattern discovery

6. ✅ `terrain_patterns_complete.json` (34KB) - Terrain patterns
   - **Used by**: `terrain_pattern_lookup` tool
   - **Purpose**: Terrain pattern search
   - **KEEP**: Critical for terrain patterns

**Loaded in tools/core_tools.py:**
7. ✅ `building_templates.json` (24KB) - Building templates
   - **Used by**: `building_template` tool
   - **Purpose**: Parametric building templates
   - **KEEP**: Critical for template system

8. ⚠️ `minecraft_material_palettes.json` (15KB) - Material palettes
   - **Referenced in**: `building_template` tool (string reference only)
   - **Purpose**: Material color schemes
   - **STATUS**: Referenced but not loaded by code
   - **DECISION NEEDED**: Is this used? Referenced in CLAUDE.md

---

### Files Referenced in CLAUDE.md but NOT Loaded ⚠️

9. ⚠️ `minecraft_items.txt` (129KB, TOON format)
   - **Referenced**: CLAUDE.md line mentions "TOON format"
   - **Purpose**: Token-efficient item list (1,375 items)
   - **Problem**: Outdated! Only 1,375 items vs 7,662 in filtered JSON
   - **RECOMMENDATION**: **DELETE** - Superseded by minecraft_items_filtered.json

10. ⚠️ `minecraft_scale_reference.txt` (15KB, TOON format)
    - **Referenced**: CLAUDE.md mentions room sizes
    - **Purpose**: Architectural dimensions for realistic builds
    - **Format**: YAML-like TOON format
    - **Usage**: Reference for AI when planning builds
    - **RECOMMENDATION**: **KEEP** - Useful reference, good TOON format

11. ⚠️ `terrain_recipes.json` (14KB)
    - **Referenced**: CLAUDE.md mentions "pre-tested terrain formulas"
    - **Purpose**: WorldEdit noise function recipes
    - **Problem**: NOT loaded by terrain generation code!
    - **RECOMMENDATION**: **DELETE or MOVE to dev_docs** - Not actively used

12. ⚠️ `worldedit_recipe_book.md` (6.4KB)
    - **Referenced**: CLAUDE.md mentions "command sequences"
    - **Purpose**: Ready-made WorldEdit command recipes
    - **Usage**: Reference for building patterns
    - **RECOMMENDATION**: **KEEP** - Useful reference guide

---

### Files NOT Referenced Anywhere ❌

13. ❌ `minecraft_architectural_patterns.md` (22KB)
    - **Not referenced**: Not in CLAUDE.md, not loaded by code
    - **Purpose**: Comprehensive building technique guide
    - **Content**: Foundation, walls, roofs, lighting, materials
    - **RECOMMENDATION**: **DELETE or MOVE to docs/** - This is user documentation, not AI context

14. ❌ `terrain_generation_guide.md` (13KB)
    - **Not referenced**: Not in CLAUDE.md, not loaded by code
    - **Purpose**: Guide to terrain generation techniques
    - **Content**: Noise functions, recipes, examples
    - **RECOMMENDATION**: **DELETE or MOVE to docs/** - This is user documentation

15. ❌ `worldedit_basic_guide.md` (4.2KB)
    - **Not referenced**: Not in CLAUDE.md (has different guides)
    - **Purpose**: WorldEdit basics quickstart
    - **Content**: Selection, set/replace, copy/paste
    - **RECOMMENDATION**: **DELETE or MOVE to docs/** - Redundant, CLAUDE.md has its own guide

16. ❌ `minecraft_items.json` (166KB, unfiltered)
    - **Not referenced**: Not loaded, not in CLAUDE.md
    - **Purpose**: Source file for filtered version (9,037 items)
    - **Usage**: Data processing only
    - **RECOMMENDATION**: **KEEP** - Archive for regenerating filtered data

---

## Summary by Status

### ✅ KEEP (Production Critical) - 7 files
1. minecraft_items_filtered.json (138KB)
2. minecraft_furniture_layouts.json (78KB)
3. minecraft_furniture_catalog.json (115KB)
4. building_patterns_structured.json (2.4KB)
5. building_patterns_complete.json (22KB)
6. terrain_patterns_complete.json (34KB)
7. building_templates.json (24KB)

**Subtotal**: 413KB (69% of total)

### ⚠️ KEEP (Useful Reference) - 2 files
8. minecraft_scale_reference.txt (15KB) - Architectural dimensions
9. worldedit_recipe_book.md (6.4KB) - Command recipes

**Subtotal**: 21.4KB (4% of total)

### ⚠️ INVESTIGATE - 1 file
10. minecraft_material_palettes.json (15KB) - Referenced but not loaded

### ❌ DELETE or RELOCATE - 4 files
11. minecraft_items.txt (129KB) - **DELETE** Outdated TOON version
12. terrain_recipes.json (14KB) - **DELETE/MOVE** Not used by code
13. minecraft_architectural_patterns.md (22KB) - **MOVE to docs/**
14. terrain_generation_guide.md (13KB) - **MOVE to docs/**
15. worldedit_basic_guide.md (4.2KB) - **DELETE** Redundant

**Subtotal**: 182KB (30% of total)

### 📦 ARCHIVE (Keep but not active) - 1 file
16. minecraft_items.json (166KB) - Source file for filtered version

---

## Recommendations

### Priority 1: Delete Clearly Redundant Files

**DELETE:**
1. `minecraft_items.txt` (129KB)
   - Reason: Outdated (1,375 items vs 7,662 in JSON)
   - Superseded by: minecraft_items_filtered.json

2. `worldedit_basic_guide.md` (4.2KB)
   - Reason: Redundant with CLAUDE.md WorldEdit sections
   - Not referenced anywhere

### Priority 2: Move Documentation to docs/

**MOVE to docs/**:
3. `minecraft_architectural_patterns.md` (22KB)
   - Reason: User-facing documentation, not AI context
   - Better suited for docs/ directory

4. `terrain_generation_guide.md` (13KB)
   - Reason: User-facing guide, not AI context
   - Better suited for docs/ directory

### Priority 3: Decision Needed on Reference Files

**INVESTIGATE:**
5. `terrain_recipes.json` (14KB)
   - Not loaded by code
   - Referenced in CLAUDE.md
   - **Options**:
     a. Delete (not actively used)
     b. Move to dev_docs (reference only)
     c. Keep if planning to use in future

6. `minecraft_material_palettes.json` (15KB)
   - Referenced in template tool
   - Referenced in CLAUDE.md
   - **Check**: Is this actually used by users?

### Priority 4: File Format Conversions

**NO CONVERSIONS NEEDED**:
- `minecraft_scale_reference.txt` - Correctly formatted as TOON
- `worldedit_recipe_book.md` - Already markdown
- All other files are appropriate format

---

## After Cleanup

### Option A: Conservative Cleanup (Delete only redundant)
```
KEEP: 7 production files (413KB)
KEEP: 2 reference files (21KB)
KEEP: 1 palette file (15KB) [investigate]
KEEP: 1 archive file (166KB)
DELETE: 2 files (133KB) - minecraft_items.txt, worldedit_basic_guide.md
MOVE: 2 files to docs/ (35KB) - architectural + terrain guides
UNCLEAR: terrain_recipes.json (14KB)

Result: 11 files, 615KB (from 14 files, 602KB)
Freed from context: 168KB moved to docs/deleted
```

### Option B: Aggressive Cleanup (Delete all non-production)
```
KEEP: 7 production files (413KB)
KEEP: 2 reference files (21KB)
KEEP: 1 archive file (166KB)
DELETE: minecraft_items.txt (129KB)
DELETE: worldedit_basic_guide.md (4.2KB)
DELETE: terrain_recipes.json (14KB)
DELETE: minecraft_architectural_patterns.md (22KB)
DELETE: terrain_generation_guide.md (13KB)
UNCLEAR: minecraft_material_palettes.json (15KB)

Result: 10 files, 615KB (from 14 files, 602KB)
Freed: 182KB deleted
```

---

## Proposed Action Plan

### Step 1: Delete Obviously Redundant
```bash
rm context/minecraft_items.txt                    # Outdated TOON version
rm context/worldedit_basic_guide.md               # Redundant guide
```

### Step 2: Move User Documentation
```bash
mv context/minecraft_architectural_patterns.md docs/
mv context/terrain_generation_guide.md docs/
```

### Step 3: Decide on terrain_recipes.json
**Question**: Is this used as reference or can it be deleted?
- If reference: Keep
- If unused: Delete

### Step 4: Verify material_palettes.json usage
**Question**: Is this file actually used by the template system?
- Check if users reference it
- Check if templates use it
- If yes: Keep
- If no: Delete

### Step 5: Update CLAUDE.md
- Remove references to deleted files
- Update file paths for moved files

### Step 6: Update context/README.md
- Remove deleted file entries
- Update file list

---

## Final Recommended Context Directory

**Production Data (7 files)**:
- minecraft_items_filtered.json
- minecraft_furniture_layouts.json
- minecraft_furniture_catalog.json
- building_patterns_structured.json
- building_patterns_complete.json
- terrain_patterns_complete.json
- building_templates.json

**Reference Files (2-3 files)**:
- minecraft_scale_reference.txt
- worldedit_recipe_book.md
- minecraft_material_palettes.json (if used)

**Archive (1 file)**:
- minecraft_items.json (source data)

**Total**: 10-11 files, ~615KB, all with clear purpose!

---

**Ready to execute cleanup?**
