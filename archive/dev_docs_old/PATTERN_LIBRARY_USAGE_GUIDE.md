# Pattern Library Usage Guide

## Overview

The VibeCraft Pattern Library provides 70+ searchable, layer-by-layer construction blueprints for building and terrain elements. This guide demonstrates practical workflows for using patterns effectively.

---

## Quick Start

### Search → Get → Build Workflow

**The basic pattern**: Search for patterns, get the one you want, build it layer by layer.

```
1. Search:  building_pattern_lookup(action="search", query="gable oak")
2. Get:     building_pattern_lookup(action="get", pattern_id="gable_oak_medium")
3. Build:   Use layer data to construct with WorldEdit commands
```

---

## Building Patterns

### Example 1: Building a Gable Roof

**Scenario**: You've built a 14×12 building and need to add a roof.

**Step 1: Search for appropriate roofing**
```
building_pattern_lookup(action="search", category="roofing", subcategory="gable")
```

**Result**: Find patterns like:
- `gable_oak_small` (10×5×8) - Too small
- `gable_oak_medium` (14×6×12) - Perfect match!
- `gable_oak_large` (18×8×16) - Too large

**Step 2: Get the pattern details**
```
building_pattern_lookup(action="get", pattern_id="gable_oak_medium")
```

**Result**: Returns complete layer-by-layer construction data:
- 6 layers total
- Layer 0 (Y+0): Eaves with 1-block overhang
- Layer 1-5 (Y+1 to Y+5): Slope progressing to ridge
- Materials: 168 oak_stairs, 12 oak_planks
- Exact block placements with coordinates and orientations

**Step 3: Build layer by layer**

Assume building top at Y=70.

**Layer 0 (Y=70) - Eaves with overhang**:
```
Pattern shows blocks at:
  (0, 0): oak_stairs[facing=north,half=bottom]
  (1, 0): oak_stairs[facing=north,half=bottom]
  ...
  (0, 11): oak_stairs[facing=south,half=bottom]
  (1, 11): oak_stairs[facing=south,half=bottom]
  ...

Build commands (adjust X,Z to your location):
  setblock 100 70 100 oak_stairs[facing=north,half=bottom]
  setblock 101 70 100 oak_stairs[facing=north,half=bottom]
  ...
  setblock 100 70 111 oak_stairs[facing=south,half=bottom]
  setblock 101 70 111 oak_stairs[facing=south,half=bottom]
  ...
```

**Layer 1 (Y=71) - First slope inward**:
```
Pattern shows blocks at:
  (0, 1): oak_stairs[facing=north,half=bottom]
  (1, 1): oak_stairs[facing=north,half=bottom]
  ...

Build commands:
  setblock 100 71 101 oak_stairs[facing=north,half=bottom]
  setblock 101 71 101 oak_stairs[facing=north,half=bottom]
  ...
```

**Continue through all 6 layers**, using the exact coordinates and orientations from the pattern data.

**Result**: A properly constructed gable roof with correct stair orientation, no stacking errors, proper overhang.

---

### Example 2: Adding Windows to a Building

**Scenario**: You have a stone brick building and need to add windows.

**Step 1: Search for window patterns**
```
building_pattern_lookup(action="search", subcategory="windows")
```

**Result**:
- `window_small_1x1_framed` - Single pane with frame
- `window_medium_2x2_framed` - Medium double-high window
- `window_large_3x2_framed` - Large triple-wide window

**Step 2: Get medium window pattern**
```
building_pattern_lookup(action="get", pattern_id="window_medium_2x2_framed")
```

**Result**: Returns:
- Dimensions: 4×3×1 (includes frame)
- Layer 0 (Y+0): Bottom frame with sill
- Layer 1 (Y+1): Glass panes with side frames
- Layer 2 (Y+2): Top frame
- Materials: 10 smooth_stone (frame), 4 glass_pane

**Step 3: Cut opening and build window**

```
# Cut opening in wall (2×2 for glass)
//pos1 105,66,100
//pos2 106,67,100
//set air

# Build frame and glass using pattern layer data
Layer 0 (Y=65): Bottom sill + side frames
  setblock 104 65 100 smooth_stone
  setblock 105 65 100 smooth_stone_slab[type=bottom]  # Sill
  setblock 106 65 100 smooth_stone_slab[type=bottom]  # Sill
  setblock 107 65 100 smooth_stone

Layer 1 (Y=66): Glass with side frames
  setblock 104 66 100 smooth_stone  # Left frame
  setblock 105 66 100 glass_pane
  setblock 106 66 100 glass_pane
  setblock 107 66 100 smooth_stone  # Right frame

Layer 2 (Y=67): Glass with side frames
  setblock 104 67 100 smooth_stone  # Left frame
  setblock 105 67 100 glass_pane
  setblock 106 67 100 glass_pane
  setblock 107 67 100 smooth_stone  # Right frame

Layer 3 (Y=68): Top frame
  setblock 104 68 100 smooth_stone
  setblock 105 68 100 smooth_stone
  setblock 106 68 100 smooth_stone
  setblock 107 68 100 smooth_stone
```

**Result**: Professionally framed window with proper trim, sills, and glass placement.

---

### Example 3: Adding Corner Pillars

**Scenario**: Building lacks structural contrast - all stone_bricks with no pillars.

**Step 1: Search for corner pillar patterns**
```
building_pattern_lookup(action="search", category="corners")
```

**Result**:
- `corner_pillar_1x1_simple` - Basic 1×1 contrasting pillar
- `corner_pillar_2x2_grand` - Large 2×2 for grand buildings
- `corner_pillar_1x1_detailed` - Decorative with capitals

**Step 2: Get simple pillar pattern**
```
building_pattern_lookup(action="get", pattern_id="corner_pillar_1x1_simple")
```

**Result**: Returns:
- Dimensions: 1×10×1 (height varies by building)
- Single column of polished_andesite
- Scale notes: Height should match building height

**Step 3: Replace corner blocks**

```
# Building corners are at:
# (100, 64-74, 100) - NW corner
# (110, 64-74, 100) - NE corner
# (100, 64-74, 110) - SW corner
# (110, 64-74, 110) - SE corner

# Replace each corner column with polished_andesite
//pos1 100,64,100
//pos2 100,74,100
//set polished_andesite

//pos1 110,64,100
//pos2 110,74,100
//set polished_andesite

//pos1 100,64,110
//pos2 100,74,110
//set polished_andesite

//pos1 110,64,110
//pos2 110,74,110
//set polished_andesite
```

**Result**: Building now has contrasting corner pillars providing structural emphasis.

---

## Terrain Patterns

### Example 4: Planting a Forest

**Scenario**: Need to populate a 50×50 area with oak trees.

**Step 1: Search for oak tree patterns**
```
terrain_pattern_lookup(action="search", query="oak tree")
```

**Result**:
- `oak_tree_small` (5×7×5) - Young trees
- `oak_tree_medium` (7×10×7) - Standard mature trees
- `oak_tree_large` (9×14×9) - Ancient trees

**Step 2: Get medium oak tree pattern**
```
terrain_pattern_lookup(action="get", pattern_id="oak_tree_medium")
```

**Result**: Returns:
- 10 layers of construction
- Layer 0: Trunk base (oak_log)
- Layers 1-5: Trunk continuing upward
- Layers 6-9: Canopy with oak_leaves
- Materials: 35 oak_log, 120 oak_leaves
- Placement notes: Space trees 10-15 blocks apart

**Step 3: Place trees across area**

```
# Tree locations (vary by terrain):
# Tree 1: (100, 64, 100)
# Tree 2: (113, 64, 105)
# Tree 3: (108, 65, 118)
# ... etc

For each tree location:
  1. Use get_surface_level(x, z) to find ground Y
  2. Build layers 0-9 from pattern data, starting at surface Y
  3. Adjust trunk height if on slope (add/remove middle layers)

Tree 1 at (100, 64, 100):
  Layer 0 (Y=64): Trunk base
    setblock 100 64 100 oak_log[axis=y]
    setblock 101 64 100 oak_log[axis=y]
    setblock 100 64 101 oak_log[axis=y]
    setblock 101 64 101 oak_log[axis=y]

  Layer 1-5 (Y=65-69): Continue trunk
    (2×2 oak_log column)

  Layer 6-9 (Y=70-73): Canopy
    (Pattern shows oak_leaves in spherical arrangement)
    setblock 98 70 98 oak_leaves
    setblock 99 70 98 oak_leaves
    ... (follow pattern exactly)
```

**Result**: Realistic oak forest with proper spacing, varied heights on slopes, natural canopy.

---

### Example 5: Creating a Path

**Scenario**: Need a path from building to garden (40 blocks away).

**Step 1: Search for path patterns**
```
terrain_pattern_lookup(action="search", subcategory="paths")
```

**Result**:
- `path_cobblestone` - Formal path with edging
- `path_gravel` - Simple gravel trail
- `path_stepping_stones` - Rustic stone path
- `path_dirt` - Natural worn trail

**Step 2: Get cobblestone path pattern**
```
terrain_pattern_lookup(action="get", pattern_id="path_cobblestone")
```

**Result**: Returns:
- Width: 3 blocks (center + edges)
- Layer 0 (Y+0): Cobblestone center, andesite edging
- Repeatable pattern: Extend length as needed
- Materials per 10-block section: 10 cobblestone, 20 andesite

**Step 3: Build path**

```
# Path runs from (100, 64, 100) to (100, 64, 140)

# Pattern shows 3-block width:
# Z-1: andesite edge
# Z+0: cobblestone center
# Z+1: andesite edge

For each segment (every 10 blocks):
  //pos1 99,64,100
  //pos2 99,64,109
  //set andesite

  //pos1 100,64,100
  //pos2 100,64,109
  //set cobblestone

  //pos1 101,64,100
  //pos2 101,64,109
  //set andesite

  (Repeat for next segment starting at Z=110)
```

**Result**: Formal cobblestone path with decorative edging connecting locations.

---

## Advanced Techniques

### Combining Multiple Patterns

**Scenario**: Building a complete cottage with all architectural elements.

**Pattern combination**:
1. Foundation: Solid stone_bricks
2. Walls: Stone_bricks with windows
3. Corner pillars: Polished_andesite
4. Roof: Gable oak roof
5. Door: Grand oak entrance
6. Chimney: Stone chimney

**Workflow**:
```
# 1. Search and get all needed patterns
building_pattern_lookup(action="search", category="roofing")      → Choose roof
building_pattern_lookup(action="search", subcategory="windows")   → Choose windows
building_pattern_lookup(action="search", category="corners")      → Choose pillars
building_pattern_lookup(action="search", subcategory="doors")     → Choose entrance
building_pattern_lookup(action="search", subcategory="chimneys")  → Choose chimney

# 2. Build in order:
#    a. Foundation and walls (solid)
#    b. Add corner pillars (replace corners)
#    c. Cut and frame windows
#    d. Add entrance
#    e. Build roof
#    f. Add chimney

# 3. Each element uses pattern layer data
```

**Result**: Cohesive cottage with all architectural elements properly integrated.

---

### Scaling Patterns

**Scenario**: Pattern is too small/large for your building.

**Check scalability**:
```
building_pattern_lookup(action="get", pattern_id="gable_oak_medium")
```

Look for `scalable: true` and `scale_notes` fields.

**If pattern is scalable**:
- Roofs: Extend base width, add more slope layers
- Windows: Increase frame dimensions, add more glass panes
- Trees: Add trunk layers, expand canopy radius

**Example - Scaling a roof wider**:
```
Original pattern: 14 blocks wide (Layer 0 has 14 stair blocks)
Desired width: 20 blocks

Modification:
  Layer 0: Add 6 more stair blocks (3 per side) for 20 total
  Layer 1-N: Extend inward progression by 3 more layers
  Ridge: Moves up 3 layers (instead of 6 layers, now 9 layers)
```

**Result**: Pattern scaled to fit custom building size while maintaining proper proportions.

---

### Material Variants

**Scenario**: Pattern uses oak but you want spruce.

**Check variants**:
```
building_pattern_lookup(action="get", pattern_id="gable_oak_medium")
```

Look for `variants` field listing alternative patterns:
- `gable_spruce_medium`
- `gable_dark_oak_medium`
- `gable_birch_medium`
- etc.

**Retrieve variant**:
```
building_pattern_lookup(action="get", pattern_id="gable_spruce_medium")
```

**Result**: Same dimensions and construction, different materials.

---

## Common Workflows

### Workflow 1: Building a House from Scratch

```
1. Foundation and walls
   - Build solid structure
   - Leave openings for windows/doors

2. Add architectural elements
   building_pattern_lookup → corner_pillar_1x1_simple
   - Replace corners with contrasting material

3. Frame windows
   building_pattern_lookup → window_medium_2x2_framed
   - Cut openings, add frames and glass

4. Add entrance
   building_pattern_lookup → door_single_oak
   - Build door surround with trim

5. Build roof
   building_pattern_lookup → gable_oak_medium
   - Layer by layer from eaves to ridge

6. Add chimney
   building_pattern_lookup → chimney_stone_medium
   - Build from ground through roof

Result: Complete house with all architectural elements.
```

---

### Workflow 2: Landscaping a Build

```
1. Analyze terrain
   terrain_analyzer → Understand elevation, hazards, opportunities

2. Plant trees
   terrain_pattern_lookup → oak_tree_medium, spruce_tree_large
   - Vary sizes for natural look
   - Space 10-15 blocks apart

3. Add bushes
   terrain_pattern_lookup → bush_leafy, bush_flowering
   - Cluster around tree bases
   - Use as property boundaries

4. Place decorations
   terrain_pattern_lookup → rock_small, fallen_log_oak
   - Add natural elements
   - Break up empty spaces

5. Create paths
   terrain_pattern_lookup → path_cobblestone
   - Connect key locations
   - Follow natural contours

Result: Fully landscaped environment around building.
```

---

### Workflow 3: Renovating a Build

**Scenario**: Existing build lacks architectural quality (no pillars, poor windows, flat roof).

```
1. Assess current state
   - Identify missing elements
   - List needed improvements

2. Add corner pillars
   building_pattern_lookup → corner_pillar_1x1_simple
   - Replace existing corners

3. Upgrade windows
   - Remove bare glass
   building_pattern_lookup → window_medium_2x2_framed
   - Add proper frames and sills

4. Replace roof
   - Remove flat roof
   building_pattern_lookup → gable_oak_medium
   - Build proper pitched roof with overhang

5. Add details
   building_pattern_lookup → chimney_brick_small
   - Enhance with additional elements

Result: Transformed build with professional architectural quality.
```

---

## Tips and Best Practices

### Search Strategies

**1. Start general, refine specific**
```
# Too specific (might miss results):
building_pattern_lookup(action="search", query="medium oak gable roof")

# Better - start broad:
building_pattern_lookup(action="search", category="roofing")
# Then narrow:
building_pattern_lookup(action="search", category="roofing", subcategory="gable")
# Then filter:
building_pattern_lookup(action="search", tags=["oak", "medium"])
```

**2. Use category + subcategory for precision**
```
building_pattern_lookup(action="search", category="facades", subcategory="windows")
terrain_pattern_lookup(action="search", category="vegetation", subcategory="trees")
```

**3. Use tags for style/size filtering**
```
building_pattern_lookup(action="search", tags=["oak", "easy"])
terrain_pattern_lookup(action="search", tags=["large", "natural"])
```

---

### Construction Best Practices

**1. Always read full pattern before building**
- Review all layers
- Check material requirements
- Note special instructions
- Understand Y-offsets

**2. Build layer by layer (don't skip ahead)**
- Complete each layer fully
- Verify orientation before proceeding
- Check symmetry at each level

**3. Adapt to terrain**
- Use get_surface_level for proper Y coordinates
- Adjust for slopes (may need to modify foundation layers)
- Account for underground obstacles

**4. Maintain block state accuracy**
```
# Wrong (random orientation):
//set oak_stairs

# Right (controlled orientation):
setblock 100 70 100 oak_stairs[facing=north,half=bottom]
```

**5. Test first on small scale**
- Build one window before doing all windows
- Try one tree before planting forest
- Verify materials and appearance

---

### Pattern Selection Guidelines

**Roofing**:
- Small (10×5×8): Sheds, small cottages, guard towers
- Medium (14×6×12): Standard houses, barns, shops
- Large (18×8×16): Mansions, halls, large buildings

**Windows**:
- Small (1×1): Guard towers, small structures
- Medium (2×2): Standard residential, most buildings
- Large (3×2): Grand buildings, galleries, public structures

**Trees**:
- Small (5×7×5): Young forests, dense areas, space constraints
- Medium (7×10×7): Standard landscaping, general use
- Large (9×14×9): Focal points, ancient forests, grand landscapes

**Paths**:
- Cobblestone: Formal, town centers, important routes
- Gravel: Casual, rural areas, general paths
- Stepping stones: Rustic, gardens, decorative
- Dirt: Natural, forests, worn trails

---

## Troubleshooting

### "Pattern not found"
- Check spelling of pattern_id
- Use action='search' to find available patterns
- Verify category/subcategory names

### "Wrong size for building"
- Check pattern dimensions in search results
- Look for scalable patterns with scale_notes
- Consider using next size up/down

### "Orientation looks wrong"
- Verify block states exactly match pattern
- Double-check facing direction (north, south, east, west)
- Ensure half parameter is correct (top, bottom)

### "Materials don't match style"
- Check variants field for alternative materials
- Search for same pattern in different material
- Consider manual substitution (oak → spruce, stone_brick → sandstone)

---

## Summary

**Pattern Library Key Benefits**:
1. **Professional quality** - Pre-designed, tested patterns
2. **Exact specifications** - No guessing on block placement
3. **Searchable** - Find patterns by category, style, size
4. **Complete data** - Layer-by-layer with materials and notes
5. **Standardized** - Consistent format across all patterns

**When to Use Patterns**:
- Building any architectural element (roofs, windows, doors, pillars)
- Landscaping (trees, bushes, rocks, paths)
- Learning proper construction techniques
- Ensuring quality and consistency
- Saving time on common elements

**Remember**: Patterns are starting points - adapt them to your specific needs while maintaining their quality standards.

---

**For More Information**:
- Schema documentation: `context/pattern_schema.json`
- Pattern databases: `context/building_patterns_complete.json`, `context/terrain_patterns_complete.json`
- CLAUDE.md: Full pattern system documentation
- Implementation summary: `dev_docs/PATTERN_LIBRARY_IMPLEMENTATION_SUMMARY.md`
