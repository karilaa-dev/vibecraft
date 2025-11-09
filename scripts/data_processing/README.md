# Data Processing Scripts

**Status**: Archived
**Date**: 2025-11-05

---

## Overview

These scripts were used during development to extract, process, and validate data files used by VibeCraft.

## Scripts

### `extract_furniture_inventory.py`
**Purpose**: Extracted furniture layout data from source files and generated structured JSON

**Output**: Produced furniture catalog data used by furniture placement tools

**Usage**: One-time processing during initial furniture system development

### `validate_furniture_layouts.py`
**Purpose**: Validated furniture layout JSON files for correctness

**Checks**:
- JSON syntax validation
- Required field presence
- Coordinate ranges
- Material validity
- Dimension consistency

**Usage**: Quality assurance during furniture library creation

## Data Files Produced

These scripts generated or validated:
- `context/minecraft_furniture_catalog.json` - Main furniture catalog
- Furniture layout data used by `furniture_placer.py`

## When to Use

Re-run these scripts if you need to:
- Regenerate furniture data from updated source
- Validate new furniture layouts
- Process additional furniture designs
- Update furniture catalog structure

## Running the Scripts

```bash
cd scripts/data_processing

# Extract furniture inventory
python extract_furniture_inventory.py

# Validate furniture layouts
python validate_furniture_layouts.py
```

## Dependencies

Check script headers for required packages (likely standard library only).

## Related Files

- **Furniture catalog**: `context/minecraft_furniture_catalog.json`
- **Furniture placer**: `mcp-server/src/vibecraft/furniture_placer.py`
- **Furniture tools**: `mcp-server/src/vibecraft/tools/furniture_tools.py`

---

**Archived**: 2025-11-05
**Reason**: One-time processing completed
**Preserved**: For regenerating data if needed
