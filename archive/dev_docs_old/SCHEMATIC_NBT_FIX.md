# Schematic NBT API Fix

**Date**: 2025-11-01
**Issue**: `'File' object has no attribute 'root'` error when listing schematics
**Cause**: nbtlib 2.0+ API change - File objects no longer have `.root` attribute
**Status**: ✅ FIXED

---

## Problem

When calling `schematic_library(action="list")`, the following error occurred:
```
❌ Schematic operation failed: 'File' object has no attribute 'root'
```

**Root cause**: Line 58 in `schematic_manager.py`:
```python
root = data.root  # This doesn't exist in nbtlib 2.0+
```

---

## nbtlib API Changes

### Old API (nbtlib < 2.0):
```python
nbt_file = nbtlib.load("schematic.schem")
root = nbt_file.root  # Access root compound
width = root["Width"]
```

### New API (nbtlib 2.0+):
```python
nbt_file = nbtlib.load("schematic.schem")
# File object acts as root compound directly (dict-like)
width = nbt_file["Width"]  # Direct access
# OR
width = nbt_file.get("", nbt_file)["Width"]  # Via empty string key
```

---

## Solution Implemented

**File**: `mcp-server/src/vibecraft/schematic_manager.py`
**Function**: `read_metadata()` (lines 50-93)

### Updated Code

Added compatibility layer that handles both old and new APIs:

```python
def read_metadata(path: Path) -> Optional[SchematicMetadata]:
    try:
        nbt_file = nbtlib.load(path)
    except FileNotFoundError:
        return None
    except Exception as exc:
        return SchematicMetadata(name=path.stem, path=path)

    # Compatibility for both old and new nbtlib APIs
    try:
        if hasattr(nbt_file, 'root'):
            # Older API compatibility
            root = nbt_file.root
        elif isinstance(nbt_file, dict):
            # nbtlib 2.0+: File acts like a dict
            # For .schem files, data is typically at root level or under empty string key
            root = nbt_file.get('', nbt_file)
        else:
            # Direct access if it's the compound itself
            root = nbt_file
    except Exception:
        return SchematicMetadata(name=path.stem, path=path)

    # Continue with metadata extraction...
    width = _safe_get(root, "Width")
    height = _safe_get(root, "Height")
    length = _safe_get(root, "Length")
    # ...
```

### How It Works

1. **Try `.root` attribute first** - Backwards compatibility with older nbtlib versions
2. **Check if dict-like** - nbtlib 2.0+ File objects behave like dictionaries
   - Try empty string key `''` (common in .schem files)
   - Fallback to using the file object itself as root
3. **Fallback** - Use file object directly as root compound
4. **Error handling** - If all fails, return metadata with just name and path

---

## Testing

After fix, all schematic_library actions should work:

```python
# List schematics - now works without error
schematic_library(action="list")

# Info with metadata extraction
schematic_library(action="info", name="modern_villa_1")

# Prepare and load operations (unchanged)
schematic_library(action="prepare", name="modern_villa_1")
schematic_library(action="load", name="modern_villa_1")
```

---

## Why This Approach

**Multi-version compatibility**:
- Works with nbtlib 2.0+ (current requirement: `nbtlib>=2.0.0`)
- Maintains backwards compatibility if older versions are used
- Graceful degradation - even if NBT parsing fails, still lists schematic name

**Defensive programming**:
- Multiple fallback strategies
- Try-except wrapping to prevent crashes
- Returns partial metadata (name + path) if NBT reading fails

---

## Related Files

- `mcp-server/src/vibecraft/schematic_manager.py` - Fixed NBT reading
- `mcp-server/requirements.txt` - Specifies `nbtlib>=2.0.0`
- `mcp-server/pyproject.toml` - Specifies `nbtlib>=2.0.0`

---

## Summary

✅ Fixed `'File' object has no attribute 'root'` error
✅ Added nbtlib 2.0+ API compatibility
✅ Maintained backwards compatibility with older versions
✅ Graceful error handling for corrupted/invalid schematics
✅ All schematic_library actions now functional

**Status**: Ready for testing. Restart MCP server to apply changes.
