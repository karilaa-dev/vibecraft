# Furniture Layout Schema Documentation

## Overview

The furniture layout schema defines machine-actionable blueprints for Minecraft furniture that can be automatically executed with WorldEdit commands. Each layout describes:

- **Dimensions** (bounding box)
- **Block placements** (precise coordinates and block types)
- **Materials** (required blocks and counts)
- **Metadata** (category, tags, clearance requirements)

## Coordinate System

### Origin Point Convention

All coordinates are **relative to the origin (0,0,0)**, which represents the **front-left-bottom corner** of the furniture piece.

```
      North (-Z)
          ↑
          |
West ←----+----→ East
 (-X)     |     (+X)
          |
          ↓
      South (+Z)

Origin (0,0,0) = Front-Left-Bottom Corner
```

### Axis Directions

- **X-axis**: Left to right (increases eastward, +X)
- **Y-axis**: Bottom to top (increases upward, +Y)
- **Z-axis**: Front to back (increases southward, +Z)

### Default Facing

- **facing: "north"** means the furniture "faces" north (-Z direction)
- Front of furniture is at Z=0, back extends in +Z direction
- Player would typically stand north (negative Z) of the furniture to use it

### Example: 3x2x1 Table

```
Front (Z=0)                    Back (Z=1)
     ┌───┬───┬───┐                ┌───┬───┬───┐
     │   │   │   │                │   │   │   │
     └───┴───┴───┘                └───┴───┴───┘
    X=0 X=1 X=2                  X=0 X=1 X=2

Bounds: width=3, height=1, depth=2
Coordinates range: X=[0,2], Y=[0,0], Z=[0,1]
```

## Schema Fields

### Required Fields

#### name
**Type**: `string`
**Description**: Human-readable name of the furniture piece
**Example**: `"Oak Dining Table"`, `"King Size Bed"`

#### id
**Type**: `string`
**Pattern**: `^[a-z0-9_]+$` (snake_case)
**Description**: Unique identifier for lookup and reference
**Example**: `"oak_dining_table"`, `"king_size_bed"`

#### category
**Type**: `string`
**Allowed Values**: `bedroom`, `kitchen`, `living_room`, `bathroom`, `office`, `outdoor`, `storage`, `decorative`, `functional`
**Description**: Primary category for organization and search

#### bounds
**Type**: `object`
**Required Properties**: `width`, `height`, `depth`

```json
{
  "bounds": {
    "width": 3,   // X-axis (left to right)
    "height": 1,  // Y-axis (bottom to top)
    "depth": 2    // Z-axis (front to back)
  }
}
```

#### placements
**Type**: `array`
**Description**: List of block placement instructions
**Minimum Items**: 1

See [Placement Types](#placement-types) below.

### Optional Fields

#### subcategory
**Type**: `string`
**Description**: Finer classification within category
**Examples**: `"seating"`, `"tables"`, `"storage"`, `"lighting"`

#### tags
**Type**: `array` of `string`
**Description**: Searchable tags for filtering
**Examples**: `["modern", "wood", "large"]`, `["medieval", "stone", "compact"]`

#### origin
**Type**: `object`
**Default**: `{"type": "front_left_bottom", "facing": "north"}`

```json
{
  "origin": {
    "type": "front_left_bottom",  // or "center_bottom", "back_left_bottom"
    "facing": "north"              // or "south", "east", "west"
  }
}
```

#### materials
**Type**: `object`
**Description**: Material requirements with block counts

```json
{
  "materials": {
    "oak_fence": 4,
    "oak_pressure_plate": 6,
    "oak_planks": 3
  }
}
```

#### clearance
**Type**: `object`
**Description**: Recommended space around furniture for access/aesthetics

```json
{
  "clearance": {
    "front": 1,   // Blocks needed in front
    "back": 0,    // Blocks needed behind
    "left": 1,    // Blocks needed on left
    "right": 1,   // Blocks needed on right
    "top": 2      // Blocks needed above
  }
}
```

#### notes
**Type**: `string`
**Description**: Design notes, usage tips, or context
**Example**: `"Simple table design using fence posts as legs. Allows players to walk through."`

#### variants
**Type**: `array`
**Description**: Variations of the furniture (material substitutions, size changes)

```json
{
  "variants": [
    {
      "name": "Spruce Table",
      "id": "simple_spruce_table",
      "changes": "Uses spruce wood instead of oak",
      "material_overrides": {
        "oak_fence": "spruce_fence",
        "oak_pressure_plate": "spruce_pressure_plate"
      }
    }
  ]
}
```

#### source
**Type**: `object`
**Description**: Attribution and source information

```json
{
  "source": {
    "type": "minecraft_wiki",  // or "community", "original"
    "url": "https://minecraft.wiki/w/Tutorials/Furniture"
  }
}
```

## Placement Types

### 1. Block Placement

Place a single block at a specific position.

```json
{
  "type": "block",
  "pos": {"x": 0, "y": 0, "z": 0},
  "block": "oak_fence",
  "state": "[axis=y]",           // Optional: block state
  "nbt": "{CustomName:\"...\"}"  // Optional: NBT data
}
```

**Fields**:
- `pos`: 3D position `{x, y, z}` relative to origin
- `block`: Block ID (with or without `minecraft:` namespace)
- `state` (optional): Block state in bracket notation `[key=value,key2=value2]`
- `nbt` (optional): NBT data string for block entities

**Examples**:
```json
// Simple block
{"type": "block", "pos": {"x": 1, "y": 0, "z": 1}, "block": "stone"}

// Block with state
{"type": "block", "pos": {"x": 0, "y": 0, "z": 0}, "block": "oak_stairs", "state": "[facing=north,half=bottom]"}

// Block entity with NBT
{"type": "block", "pos": {"x": 2, "y": 1, "z": 0}, "block": "chest", "nbt": "{Items:[]}"}
```

### 2. Fill Placement

Fill a rectangular region with blocks.

```json
{
  "type": "fill",
  "from": {"x": 0, "y": 1, "z": 0},
  "to": {"x": 2, "y": 1, "z": 1},
  "block": "oak_planks",
  "state": ""  // Optional
}
```

**Fields**:
- `from`: Starting corner `{x, y, z}`
- `to`: Ending corner `{x, y, z}` (inclusive)
- `block`: Block to fill with
- `state` (optional): Block state

**Example**: Fill a 3x1x2 floor with oak planks
```json
{
  "type": "fill",
  "from": {"x": 0, "y": 0, "z": 0},
  "to": {"x": 2, "y": 0, "z": 1},
  "block": "oak_planks"
}
```

### 3. Line Placement

Place blocks in a line between two points.

```json
{
  "type": "line",
  "from": {"x": 0, "y": 0, "z": 0},
  "to": {"x": 4, "y": 0, "z": 0},
  "block": "iron_bars",
  "state": ""  // Optional
}
```

**Fields**:
- `from`: Starting point `{x, y, z}`
- `to`: Ending point `{x, y, z}`
- `block`: Block for the line
- `state` (optional): Block state

**Example**: Create a railing
```json
{
  "type": "line",
  "from": {"x": 0, "y": 1, "z": 0},
  "to": {"x": 5, "y": 1, "z": 0},
  "block": "oak_fence"
}
```

### 4. Layer Placement

Place a pattern on a horizontal layer (useful for floors, ceilings).

```json
{
  "type": "layer",
  "y": 0,
  "pattern": "50%oak_planks,50%spruce_planks",
  "bounds": {  // Optional
    "from": {"x": 0, "z": 0},
    "to": {"x": 2, "z": 1}
  }
}
```

**Fields**:
- `y`: Y-level for the layer (relative to origin)
- `pattern`: WorldEdit pattern syntax (single block or mixed pattern)
- `bounds` (optional): Restricts layer to specific X, Z range (defaults to full furniture bounds)

**Examples**:
```json
// Simple floor
{"type": "layer", "y": 0, "pattern": "oak_planks"}

// Mixed pattern floor
{"type": "layer", "y": 0, "pattern": "70%oak_planks,20%birch_planks,10%dark_oak_planks"}

// Random wool layer
{"type": "layer", "y": 1, "pattern": "##wool"}
```

## Complete Example: Simple Oak Table

```json
{
  "name": "Simple Oak Table",
  "id": "simple_oak_table",
  "category": "living_room",
  "subcategory": "tables",
  "tags": ["wood", "compact", "dining"],
  "origin": {
    "type": "front_left_bottom",
    "facing": "north"
  },
  "bounds": {
    "width": 3,
    "height": 2,
    "depth": 2
  },
  "placements": [
    {
      "type": "block",
      "pos": {"x": 0, "y": 0, "z": 0},
      "block": "oak_fence",
      "state": "[axis=y]"
    },
    {
      "type": "block",
      "pos": {"x": 2, "y": 0, "z": 0},
      "block": "oak_fence",
      "state": "[axis=y]"
    },
    {
      "type": "block",
      "pos": {"x": 0, "y": 0, "z": 1},
      "block": "oak_fence",
      "state": "[axis=y]"
    },
    {
      "type": "block",
      "pos": {"x": 2, "y": 0, "z": 1},
      "block": "oak_fence",
      "state": "[axis=y]"
    },
    {
      "type": "fill",
      "from": {"x": 0, "y": 1, "z": 0},
      "to": {"x": 2, "y": 1, "z": 1},
      "block": "oak_pressure_plate"
    }
  ],
  "materials": {
    "oak_fence": 4,
    "oak_pressure_plate": 6
  },
  "clearance": {
    "front": 1,
    "back": 1,
    "left": 1,
    "right": 1,
    "top": 2
  },
  "notes": "Simple table design using fence posts as legs and pressure plates as tabletop. Allows players to walk through the table area.",
  "source": {
    "type": "minecraft_wiki",
    "url": "https://minecraft.wiki/w/Tutorials/Furniture"
  }
}
```

### Visualization

```
Top View (Y=1):
     0   1   2   (X)
  0 [P] [P] [P]
  1 [P] [P] [P]
(Z)

Side View (from West, X=0):
     0   1   (Z)
  1 [P] [P]
  0 [F] [F]
(Y)

Legend: [F] = Fence, [P] = Pressure Plate
```

## WorldEdit Command Translation

The placement helper will convert layouts to WorldEdit commands:

### Single Block
```json
{"type": "block", "pos": {"x": 1, "y": 0, "z": 1}, "block": "oak_fence"}
```
→ `//set oak_fence` at absolute position (origin + relative position)

### Fill
```json
{"type": "fill", "from": {"x": 0, "y": 0, "z": 0}, "to": {"x": 2, "y": 1, "z": 1}, "block": "stone"}
```
→ `//pos1 X,Y,Z` then `//pos2 X,Y,Z` then `//set stone`

### Line
```json
{"type": "line", "from": {"x": 0, "y": 0, "z": 0}, "to": {"x": 5, "y": 0, "z": 0}, "block": "fence"}
```
→ `//line fence` between two positions

### Layer
```json
{"type": "layer", "y": 0, "pattern": "oak_planks"}
```
→ `//pos1 X,Y,Z` then `//pos2 X,Y,Z` then `//set oak_planks` for that Y-level

## Best Practices

1. **Always define origin and facing** - Makes rotation predictable
2. **Use bounds accurately** - Should match the actual space occupied
3. **Include clearance data** - Helps AI agents plan room layouts
4. **Document materials** - Enables material estimation
5. **Add tags** - Improves searchability (`["compact", "modern", "wood"]`)
6. **Use fill for regions** - More efficient than individual blocks
7. **Include notes** - Context helps AI understand usage
8. **Specify block states** - Ensures correct orientation (stairs, doors, etc.)

## Adding New Furniture

1. Determine bounding box (width × height × depth)
2. Choose origin point (usually front-left-bottom)
3. Map out block placements relative to (0,0,0)
4. Calculate material counts
5. Add clearance recommendations
6. Tag appropriately for search
7. Validate against schema

## Validation

Use the JSON schema file (`furniture_layout_schema.json`) to validate layouts:

```bash
# Using jsonschema (Python)
pip install jsonschema
python -c "
import json
import jsonschema

with open('furniture_layout_schema.json') as f:
    schema = json.load(f)
with open('your_layout.json') as f:
    layout = json.load(f)

jsonschema.validate(layout, schema)
print('✅ Valid!')
"
```

## Future Enhancements

- Automatic rotation generation (all 4 cardinal directions)
- Pattern templates for common furniture types
- ASCII art previews
- 3D visualization exports
- Material cost calculator
- Space efficiency metrics
