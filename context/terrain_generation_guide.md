# VibeCraft Terrain Generation Guide

## Overview

VibeCraft provides powerful, console-safe terrain generation tools that leverage WorldEdit's noise functions to create realistic landscapes. These tools allow you to generate hills, mountains, valleys, plateaus, and mountain ranges with mathematical precision.

## Available Tools

### 1. generate_terrain

**Purpose**: Create realistic terrain features using pre-tested noise recipes

**Supported Types**:
- `rolling_hills` - Gentle undulating hills (Perlin noise)
- `rugged_mountains` - Sharp peaks and ridges (Ridged Multifractal)
- `valley_network` - Interconnected valleys for rivers (Inverted Perlin)
- `mountain_range` - Linear mountain chain in a direction (Oriented Ridged)
- `plateau` - Flat-topped elevation with rough edges

**Basic Usage**:
```python
generate_terrain(
    type="rolling_hills",
    x1=0, y1=64, z1=0,
    x2=100, y2=80, z2=100,
    scale=18,        # Feature breadth
    amplitude=6      # Height variation
)
```

### 2. texture_terrain

**Purpose**: Apply natural surface materials to terrain based on biome style

**Supported Styles**:
- `temperate` - Grass, moss, dirt (plains/forest)
- `alpine` - Stone, snow, gravel (high altitude)
- `desert` - Sand, sandstone, terracotta (arid)
- `volcanic` - Basalt, magma, blackstone (lava zones)
- `jungle` - Rich soil, podzol, moss (tropical)
- `swamp` - Mud, clay, damp grass (wetlands)

**Basic Usage**:
```python
texture_terrain(
    style="temperate",
    x1=0, y1=64, z1=0,
    x2=100, y2=80, z2=100
)
```

### 3. smooth_terrain

**Purpose**: Post-process terrain to remove blocky appearance

**Basic Usage**:
```python
smooth_terrain(
    x1=0, y1=64, z1=0,
    x2=100, y2=80, z2=100,
    iterations=3    # More = smoother
)
```

## Typical Workflow

### Simple Hills for Village Site

1. **Generate terrain**:
```python
generate_terrain(
    type="rolling_hills",
    x1=0, y1=64, z1=0, x2=100, y2=80, z2=100,
    scale=18, amplitude=6, smooth_iterations=3
)
```

2. **Apply grass texture**:
```python
texture_terrain(
    style="temperate",
    x1=0, y1=64, z1=0, x2=100, y2=80, z2=100
)
```

3. **Done!** You now have gentle grassy hills ready for building.

### Mountain Backdrop for Castle

1. **Generate rugged mountains**:
```python
generate_terrain(
    type="rugged_mountains",
    x1=0, y1=64, z1=0, x2=150, y2=110, z2=100,
    scale=28, amplitude=22, smooth_iterations=2
)
```

2. **Apply alpine texturing**:
```python
texture_terrain(
    style="alpine",
    x1=0, y1=64, z1=0, x2=150, y2=110, z2=100
)
```

3. **Result**: Dramatic snow-capped peaks perfect for a mountain fortress!

### River Valley System

1. **Create valley network**:
```python
generate_terrain(
    type="valley_network",
    x1=0, y1=64, z1=0, x2=150, y2=80, z2=150,
    scale=24, depth=12, smooth_iterations=2
)
```

2. **Apply grass/dirt**:
```python
texture_terrain(
    style="temperate",
    x1=0, y1=64, z1=0, x2=150, y2=80, z2=150
)
```

3. **Add water manually** (use worldedit_region tool):
```python
# Select valley floor areas and fill with water
worldedit_region(command="set water")
```

### Continental Mountain Range

1. **Generate oriented range**:
```python
generate_terrain(
    type="mountain_range",
    x1=0, y1=64, z1=0, x2=200, y2=100, z2=100,
    direction="north-south",  # Runs N-S across the map
    amplitude=24, smooth_iterations=1
)
```

2. **Texture with snow**:
```python
texture_terrain(
    style="alpine",
    x1=0, y1=64, z1=0, x2=200, y2=100, z2=100
)
```

## Parameter Tuning Guide

### Scale (Feature Breadth)

**What it controls**: Horizontal size of terrain features

- **Small (10-15)**: Tight, frequent hills/valleys
- **Medium (18-25)**: Natural-looking variation
- **Large (30-40)**: Broad, sweeping features

**Use smaller scale for**:
- Detailed local terrain
- Compact build areas
- Varied landscapes

**Use larger scale for**:
- Epic vistas
- Distant backdrops
- Gentle rolling plains

### Amplitude (Height Variation)

**What it controls**: Vertical displacement from base terrain

- **Subtle (3-8)**: Gentle slopes, barely noticeable
- **Moderate (10-18)**: Noticeable hills/mountains
- **Dramatic (20-30)**: Extreme elevation changes
- **Maximum (50)**: Safety cap, very steep

**Use lower amplitude for**:
- Farmland
- Village sites
- Subtle variation

**Use higher amplitude for**:
- Mountain ranges
- Dramatic backdrops
- Cliff formations

### Octaves (Detail Level)

**What it controls**: Layers of noise detail

- **Low (3-4)**: Smooth, simple shapes
- **Medium (5)**: Balanced detail
- **High (6+)**: Fine details, complex shapes

**More octaves** = more computation time but richer terrain

### Smooth Iterations (Post-Processing)

**What it controls**: How blocky vs. smooth the result looks

- **Minimal (1-2)**: Preserve sharp features (mountains)
- **Moderate (3)**: Balance detail and smoothness (hills)
- **Heavy (4-5)**: Very smooth, gentle transitions (plains)

**Rule of thumb**:
- Mountains: 1-2 iterations
- Hills: 3 iterations
- Plains: 4+ iterations

## Combining Features

### Layered Complexity

Generate multiple terrain types in sequence for ultra-realistic landscapes:

1. **Base layer**: Gentle hills
```python
generate_terrain(type="rolling_hills", amplitude=6, ...)
```

2. **Add valleys**: Create drainage
```python
generate_terrain(type="valley_network", depth=8, ...)
```

3. **Add plateau**: Elevated feature
```python
generate_terrain(type="plateau", height=12, ...)
```

Result: Complex, varied landscape with multiple elevation zones!

### Height-Based Texturing

Use multiple texturing passes with WorldEdit masks:

1. **Texture base** (all elevations):
```python
texture_terrain(style="temperate", ...)
```

2. **Texture high peaks** (Y > 80):
```python
# Use worldedit_general to set mask
worldedit_general(command="//gmask >y80")
texture_terrain(style="alpine", ...)
worldedit_general(command="//gmask")  # Clear mask
```

Result: Grass in valleys, snow on peaks!

## Best Practices

### Planning

1. **Start small**: Test on 50x50 regions before scaling up
2. **Check coordinates**: Ensure Y range allows for displacement (base Y + amplitude < 320)
3. **Backup**: Use `//copy` on existing terrain before major changes
4. **Location matters**: Generate terrain in flat or void areas for best results

### Execution

1. **Always texture AFTER shaping**: Generate → Smooth → Texture
2. **Use appropriate smooth iterations**: Don't over-smooth mountains
3. **Match texturing to use case**: Alpine for mountains, temperate for valleys
4. **Consider adjacent terrain**: Blend new terrain with existing features

### Optimization

1. **Region size**: Larger = longer operation time
   - Small (50x50): ~5 seconds
   - Medium (100x100): ~20 seconds
   - Large (200x200): ~60+ seconds

2. **Amplitude cap**: Stay under 30 blocks for best results
3. **Seed consistency**: Use same seed for similar terrain across regions
4. **Performance**: Avoid overlapping operations on same region

## Troubleshooting

### "Region too large" Error
**Problem**: Selection exceeds 100,000 blocks
**Solution**: Reduce region size or split into multiple operations

### Terrain looks blocky
**Problem**: Insufficient smoothing
**Solution**: Increase smooth_iterations (try 3-4)

### Terrain too flat
**Problem**: Amplitude too low
**Solution**: Increase amplitude parameter (try 12-18)

### Terrain too extreme
**Problem**: Amplitude too high
**Solution**: Reduce amplitude or increase scale for gentler slopes

### Unnatural patterns
**Problem**: Noise seed creating artifacts
**Solution**: Change seed parameter or adjust octaves/persistence

### Operation timeout
**Problem**: Region too large or server lag
**Solution**: Reduce region size, wait for server resources

## Advanced Techniques

### Custom Seed for Reproducibility

Use explicit seeds to recreate terrain:
```python
generate_terrain(..., seed=42)  # Same seed = same terrain
```

### Directional Ranges

Orient mountain ranges to match your world design:
```python
generate_terrain(
    type="mountain_range",
    direction="northeast-southwest",  # Diagonal range
    ...
)
```

### Conditional Smoothing

Smooth only certain blocks using masks:
```python
smooth_terrain(..., mask="grass_block,dirt")  # Only smooth natural blocks
```

### Erosion Simulation

Simulate water erosion by heavy smoothing in valleys:
```python
# Generate valleys
generate_terrain(type="valley_network", ...)

# Heavy smooth in valley areas (use mask for lower Y)
worldedit_general(command="//gmask <y70")
smooth_terrain(..., iterations=5)
worldedit_general(command="//gmask")
```

## Example Use Cases

### 1. Medieval Village Site
- **Terrain**: Rolling hills (amplitude=6, scale=18)
- **Texture**: Temperate
- **Details**: Gentle slopes for farms, buildings

### 2. Mountain Fortress
- **Terrain**: Rugged mountains (amplitude=22, scale=28)
- **Texture**: Alpine
- **Details**: Dramatic backdrop, natural defenses

### 3. Desert Oasis
- **Terrain**: Plateau (height=15, roughness=0.35)
- **Texture**: Desert
- **Details**: Flat top for settlement, sandy base

### 4. River Canyon
- **Terrain**: Valley network (depth=14, scale=24)
- **Texture**: Temperate
- **Details**: Add water in valleys for river system

### 5. Island Chain
- **Terrain**: Multiple plateaus with low amplitude hills
- **Texture**: Jungle or temperate
- **Details**: Generate several small elevated regions

## Technical Notes

### Noise Functions Used

**Perlin Noise** (`rolling_hills`, `valley_network`):
- Smooth, natural-looking variation
- Good for organic terrain features
- Parameters: frequency, octaves, persistence

**Ridged Multifractal** (`rugged_mountains`, `mountain_range`):
- Sharp-edged, ridge-like features
- Perfect for rocky terrain
- Creates natural-looking peaks

**Smoothstep with Noise** (`plateau`):
- Combines smooth falloff with noise variation
- Creates flat areas with irregular edges
- Good for mesa/plateau formations

### WorldEdit Commands Generated

The tools internally use these WorldEdit commands:

1. **Selection**: `//pos1 X,Y,Z` and `//pos2 X,Y,Z`
2. **Deformation**: `//deform <expression>` (applies noise)
3. **Smoothing**: `//smooth <iterations>`
4. **Texturing**: `//replace <from> <to>` and `//overlay <pattern>`

You can also use these commands directly via `worldedit_region`, `worldedit_selection`, etc. for custom terrain work.

## Safety Features

All terrain generation tools include built-in safety:

1. **Amplitude capping**: Maximum ±50 blocks vertical displacement
2. **Region size limits**: Maximum 100,000 blocks per operation
3. **Coordinate validation**: Ensures operations stay within Minecraft world bounds (-30M to +30M X/Z, -64 to 320 Y)
4. **Error handling**: Clear error messages with recovery suggestions

## When to Use Each Terrain Type

### rolling_hills
- **Best for**: Villages, farms, gentle countryside, open fields
- **Avoid for**: Extreme elevations, confined spaces

### rugged_mountains
- **Best for**: Fortresses, mining operations, dramatic vistas, natural barriers
- **Avoid for**: Flat building sites, low-altitude areas

### valley_network
- **Best for**: River systems, canyon networks, wetlands, drainage patterns
- **Avoid for**: Elevated builds, mountain tops

### mountain_range
- **Best for**: Continental divides, regional borders, oriented backdrops
- **Avoid for**: Circular/radial layouts, uniform terrain

### plateau
- **Best for**: Mesas, elevated settlements, flat-topped mountains, overlooks
- **Avoid for**: Pure flatlands, extreme slopes

## Integration with Other Tools

### With terrain_analyzer

Analyze generated terrain for building suitability:
```python
# 1. Generate terrain
generate_terrain(...)

# 2. Analyze result
terrain_analyzer(x1=..., y1=..., z1=..., x2=..., y2=..., z2=...)

# 3. Review opportunities and hazards
# 4. Adjust as needed
```

### With Building Tools

Use terrain as foundation for structures:
```python
# 1. Generate mountains
generate_terrain(type="rugged_mountains", ...)

# 2. Find flat spot for castle
get_surface_level(x=150, z=200)

# 3. Build structure using building tools
# (calculate_shape, check_symmetry, etc.)
```

### With WorldEdit Region Tools

Combine with manual WorldEdit commands:
```python
# 1. Generate base terrain
generate_terrain(...)

# 2. Add custom features manually
worldedit_region(command="set water")  # Add lake
worldedit_generation(command="sphere stone 10")  # Add boulder
```

## Recipe Reference

Quick reference for common scenarios:

| Use Case | Type | Scale | Amplitude | Smooth | Texture |
|----------|------|-------|-----------|--------|---------|
| Farm fields | rolling_hills | 20 | 4 | 4 | temperate |
| Village hills | rolling_hills | 18 | 6 | 3 | temperate |
| Castle backdrop | rugged_mountains | 28 | 20 | 2 | alpine |
| Mining mountains | rugged_mountains | 25 | 18 | 1 | alpine |
| River valley | valley_network | 24 | 12 | 2 | temperate |
| Canyon | valley_network | 20 | 16 | 2 | desert |
| Mountain range | mountain_range | 30 | 22 | 1 | alpine |
| Desert mesa | plateau | N/A | N/A | 2 | desert |
| Island plateau | plateau | N/A | N/A | 3 | jungle |

## Conclusion

VibeCraft's terrain generation system provides professional-quality landscape creation with simple, intuitive tools. By understanding the parameters and following best practices, you can create stunning, realistic terrain for any Minecraft build.

**Remember the workflow**:
1. Generate → 2. Smooth → 3. Texture → 4. Build!

Happy terraforming! 🏔️
