# Rustic Ranch Complex - Implementation Plan V2

**Project**: Complete Rustic Ranch with Multiple Buildings
**Engineer**: Steve (Junior Engineer)
**Date**: 2025-11-02
**Version**: 2.0 (Post-Review)
**Status**: Ready for Final Approval

---

## Executive Summary

Build a complete rustic ranch complex in front of player "ereidjustpeed" with five separate structures connected by paths and fencing. The ranch will include a main house, horse stable, garden area, storage barn, and additional ranch elements with actual horses spawned in the stable.

**Key Changes from V1**:
- Fixed foundation philosophy (Floor Y = Ground Y, no raised foundations)
- Corrected material palette to match rustic_cottage exactly
- Added detailed roof offset specifications with layer-by-layer coordinates
- Expanded validation workflows with specific criteria
- Added complete spatial analysis workflows for furniture placement
- Specified exact lighting positions
- Updated timeline to realistic 3.5-4 hours

---

## 1. Project Overview

### 1.1 Player Context
- **Player**: ereidjustpeed
- **Current Position**: X=561, Y=-60, Z=-316
- **Facing Direction**: East (+X direction)
- **Ground Level**: Y=-60 (surface block at Y=-61)

### 1.2 Build Site Analysis
- **Total Build Area**: 60×40 blocks (X: 560-620, Z: -350 to -310)
- **Ground Level**: Flat terrain at Y=-60 (floor blocks)
- **Terrain Type**: Level ground, suitable for construction
- **Build Orientation**: Buildings arranged east of player, visible from current position

### 1.3 Material Palette (Rustic Cottage Theme)

**CORRECTED**: Based on actual rustic_cottage palette from context/minecraft_material_palettes.json

**Primary (50%): oak_planks**
- Usage: Main house walls, floors, structural elements
- Amount: ~800 blocks
- Alternatives: spruce_planks (for stable/barn variety)

**Secondary (25%): cobblestone**
- Usage: Chimney ONLY (not foundation)
- Amount: ~100 blocks
- Alternatives: stone, andesite, mossy_cobblestone

**Roof (20%): oak_stairs**
- Usage: Main house roof slopes
- Amount: ~200 blocks
- Alternatives: spruce_stairs (for stable/barn variety)

**Accent (5%): stripped_oak_log**
- Usage: Corner posts, structural beams, framing
- Amount: ~150 blocks
- Alternatives: dark_oak_log, stripped_dark_oak_log

**Decorative (NOT in palette)**: hay_block, barrel, lantern, oak_fence, coarse_dirt
- Usage: Ranch-specific details, paths, fencing
- Note: These are functional/decorative, not structural materials

**Material Distribution Notes**:
- Main House: 100% oak palette (oak_planks, oak_stairs, stripped_oak_log)
- Stable: Mix with spruce_planks walls, spruce_stairs roof (variety between buildings)
- Barn: Spruce_planks with oak_log accents
- Consistent use of stripped_oak_log for ALL corner posts

---

## 2. Building Layout Plan

### 2.1 Spatial Organization
```
North (-Z)
    ^
    |
    Garden (570,-340)      Stable (590,-340)
         [15×12]              [12×16]

    House (570,-320)                    Barn (610,-320)
      [9×11]                              [14×18]

    Player (561,-316) -->  East (+X)
```

### 2.2 Building Coordinates & Dimensions

#### Building 1: Main Ranch House
- **Location**: X=570, Z=-320
- **Dimensions**: 9 blocks (X) × 11 blocks (Z) × 5 blocks tall (walls)
- **Total Height**: ~9 blocks (including gabled roof)
- **Footprint**: 9×11 = 99 blocks
- **Floor Y**: -60 (FLUSH with ground, NOT elevated)
- **Roof Overhang**: 1 block on all sides

#### Building 2: Horse Stable
- **Location**: X=590, Z=-340
- **Dimensions**: 12 blocks (X) × 16 blocks (Z) × 6 blocks tall
- **Total Height**: ~10 blocks (including roof)
- **Footprint**: 12×16 = 192 blocks
- **Floor Y**: -60 (FLUSH with ground)
- **Stalls**: 4 individual horse stalls (front half), open area (back half)

#### Building 3: Garden Area
- **Location**: X=570, Z=-340
- **Dimensions**: 15 blocks (X) × 12 blocks (Z) × 1 block tall (fencing)
- **Footprint**: 15×12 = 180 blocks
- **Features**: Oak fence perimeter, tilled farmland, crops, water source

#### Building 4: Storage Barn
- **Location**: X=610, Z=-320
- **Dimensions**: 14 blocks (X) × 18 blocks (Z) × 8 blocks tall
- **Total Height**: ~15 blocks (including roof)
- **Footprint**: 14×18 = 252 blocks
- **Floor Y**: -60 (FLUSH with ground)
- **Roof Overhang**: 1 block on all sides

#### Building 5: Ranch Elements
- **Connecting Paths**: Coarse_dirt paths between buildings (2-3 blocks wide)
- **Fencing**: Oak fence connecting buildings
- **Water Trough**: Cauldron with water near stable
- **Hay Bales**: Scattered around stable and barn
- **Lighting**: Lanterns on fence posts every 8 blocks

---

## 3. Detailed Build Specifications

### 3.1 Building 1: Main Ranch House

#### 3.1.1 Design Philosophy
- **CRITICAL**: Floor Y = Ground Y (-60), building flush with ground, NO raised foundation
- **Style**: Rustic cottage with oak materials
- **Corner Posts**: 1×1 stripped_oak_log[axis=y], full height (Y=-60 to Y=-56)
- **Roof**: Gabled, north-south slope, 1-block overhang, proper horizontal offset

#### 3.1.2 Construction Sequence - CORRECTED

**Step 1: Floor (Y=-60) - FLUSH WITH GROUND**
```
worldedit_selection(command="pos1 570,-60,-320")
worldedit_selection(command="pos2 578,-60,-310")
worldedit_region(command="set oak_planks")
```
- **Block Count**: 99 blocks
- **Note**: Floor REPLACES top layer of ground, building sits FLUSH
- **Verification**: Floor Y = Ground Y = -60 (NOT elevated!)

**Step 2: Walls (Y=-60 to Y=-56) - START AT FLOOR LEVEL**
```
worldedit_selection(command="pos1 570,-60,-320")
worldedit_selection(command="pos2 578,-56,-310")
worldedit_region(command="walls oak_planks")
```
- **Block Count**: ~160 blocks
- **Wall Height**: 5 blocks (Y=-60, -59, -58, -57, -56)
- **Note**: Walls start AT floor level Y=-60, not above it

**Step 3: Corner Posts (Y=-60 to Y=-56) - AFTER WALLS**
```
# Southwest corner (570, -320)
rcon_command(command="fill 570 -60 -320 570 -56 -320 stripped_oak_log[axis=y] replace oak_planks")

# Southeast corner (578, -320)
rcon_command(command="fill 578 -60 -320 578 -56 -320 stripped_oak_log[axis=y] replace oak_planks")

# Northwest corner (570, -310)
rcon_command(command="fill 570 -60 -310 570 -56 -310 stripped_oak_log[axis=y] replace oak_planks")

# Northeast corner (578, -310)
rcon_command(command="fill 578 -60 -310 578 -56 -310 stripped_oak_log[axis=y] replace oak_planks")
```
- **Size**: 1×1 at each corner (4 corners total)
- **Height**: Full wall height (Y=-60 to Y=-56 = 5 blocks tall)
- **Orientation**: [axis=y] for vertical logs
- **Block Count**: 20 blocks (5 blocks × 4 corners)

**Step 4: Door Opening (Y=-60 to Y=-59, front wall) - 2 BLOCKS TALL**
```
# Create opening (2 blocks tall, not 3)
worldedit_selection(command="pos1 574,-60,-320")
worldedit_selection(command="pos2 574,-59,-320")
worldedit_region(command="set air")

# Place door (lower half)
rcon_command(command="setblock 574 -60 -320 oak_door[facing=south,half=lower,hinge=left]")

# Place door (upper half)
rcon_command(command="setblock 574 -59 -320 oak_door[facing=south,half=upper,hinge=left]")
```
- **Position**: X=574 (center of 9-block wall: 570+4=574)
- **Height**: 2 blocks (Y=-60 to Y=-59), NOT 3
- **Facing**: South (into building from player's view)

**Step 5: Windows (Y=-59 to Y=-58) - WITH DETAILED FRAMES**

**North Wall Windows**:
```
# Window 1: X=572, Z=-310
# Create 2×2 glass opening
rcon_command(command="fill 572 -59 -310 573 -58 -310 glass_pane replace oak_planks")

# Frame around window (oak_fence or stripped_oak_log)
# Top frame
rcon_command(command="setblock 571 -57 -310 stripped_oak_log[axis=x]")
rcon_command(command="setblock 572 -57 -310 stripped_oak_log[axis=x]")
rcon_command(command="setblock 573 -57 -310 stripped_oak_log[axis=x]")
rcon_command(command="setblock 574 -57 -310 stripped_oak_log[axis=x]")

# Side frames
rcon_command(command="setblock 571 -59 -310 stripped_oak_log[axis=y]")
rcon_command(command="setblock 571 -58 -310 stripped_oak_log[axis=y]")
rcon_command(command="setblock 574 -59 -310 stripped_oak_log[axis=y]")
rcon_command(command="setblock 574 -58 -310 stripped_oak_log[axis=y]")

# Bottom frame (sill)
rcon_command(command="setblock 571 -60 -310 stripped_oak_log[axis=x]")
rcon_command(command="setblock 572 -60 -310 stripped_oak_log[axis=x]")
rcon_command(command="setblock 573 -60 -310 stripped_oak_log[axis=x]")
rcon_command(command="setblock 574 -60 -310 stripped_oak_log[axis=x]")

# Repeat same pattern for Window 2: X=576, Z=-310
[Same commands with X=576-577 instead of X=572-573]
```

**South Wall Windows**:
```
# Same pattern as north wall but Z=-320
# Window 1: X=572, Z=-320
# Window 2: X=576, Z=-320
[Apply same frame pattern]
```

- **Window Size**: 2×2 glass_pane per window
- **Frame Material**: stripped_oak_log (1-block border around each window)
- **Total Windows**: 4 (2 north, 2 south)
- **Frame Style**: Complete border (top, bottom, sides)

**Step 6: Gabled Roof (Y=-55 to Y=-50) - WITH EXACT OFFSET COORDINATES**

**CRITICAL ROOF RULES**:
- Each layer steps UP by 1 block (Y+1)
- Each layer steps INWARD horizontally by 1 block (Z±1 for north-south slope)
- NEVER stack stairs at same X,Z position
- Roof extends 1 block PAST walls (overhang)
- Use analyze_placement_area before each layer to verify offset

**Building Dimensions**:
- Walls: X=570 to X=578 (9 blocks wide)
- Walls: Z=-320 to Z=-310 (11 blocks deep)
- Roof with overhang: X=569 to X=579 (11 blocks wide, +1 on each side)
- Roof slopes on Z-axis (north-south)

**Roof Layer 1 (Base, Y=-55) - WITH OVERHANG**:
```
# North side (facing north)
worldedit_selection(command="pos1 569,-55,-320")
worldedit_selection(command="pos2 579,-55,-320")
worldedit_region(command="set oak_stairs[facing=north,half=bottom]")

# South side (facing south)
worldedit_selection(command="pos1 569,-55,-310")
worldedit_selection(command="pos2 579,-55,-310")
worldedit_region(command="set oak_stairs[facing=south,half=bottom]")
```
- **X Range**: 569-579 (1 block overhang on each side past walls 570-578)
- **Z Positions**: -320 (north edge), -310 (south edge)
- **Overhang**: 1 block past walls on all sides

**SCAN BEFORE LAYER 2**:
```
analyze_placement_area(
  center_x=574,
  center_y=-55,
  center_z=-315,
  radius=8,
  analysis_type="roof_context"
)
```
Expected return: `{"next_layer_offset": {"x": 0, "y": 1, "z": 1}}`
Interpretation: Step up Y+1, inward Z+1 (north side) and Z-1 (south side)

**Roof Layer 2 (Y=-54, inward Z±1)**:
```
# North side (Z=-320 becomes Z=-319, stepped inward 1 block)
worldedit_selection(command="pos1 569,-54,-319")
worldedit_selection(command="pos2 579,-54,-319")
worldedit_region(command="set oak_stairs[facing=north,half=bottom]")

# South side (Z=-310 becomes Z=-311, stepped inward 1 block)
worldedit_selection(command="pos1 569,-54,-311")
worldedit_selection(command="pos2 579,-54,-311")
worldedit_region(command="set oak_stairs[facing=south,half=bottom]")
```
- **Y**: -54 (up 1 from -55)
- **Z North**: -319 (inward 1 from -320)
- **Z South**: -311 (inward 1 from -310)

**Roof Layer 3 (Y=-53, inward Z±1 again)**:
```
# North side (Z=-319 becomes Z=-318)
worldedit_selection(command="pos1 569,-53,-318")
worldedit_selection(command="pos2 579,-53,-318")
worldedit_region(command="set oak_stairs[facing=north,half=bottom]")

# South side (Z=-311 becomes Z=-312)
worldedit_selection(command="pos1 569,-53,-312")
worldedit_selection(command="pos2 579,-53,-312")
worldedit_region(command="set oak_stairs[facing=south,half=bottom]")
```

**Roof Layer 4 (Y=-52, inward Z±1)**:
```
# North side (Z=-318 becomes Z=-317)
worldedit_selection(command="pos1 569,-52,-317")
worldedit_selection(command="pos2 579,-52,-317")
worldedit_region(command="set oak_stairs[facing=north,half=bottom]")

# South side (Z=-312 becomes Z=-313)
worldedit_selection(command="pos1 569,-52,-313")
worldedit_selection(command="pos2 579,-52,-313")
worldedit_region(command="set oak_stairs[facing=south,half=bottom]")
```

**Roof Layer 5 (Y=-51, inward Z±1)**:
```
# North side (Z=-317 becomes Z=-316)
worldedit_selection(command="pos1 569,-51,-316")
worldedit_selection(command="pos2 579,-51,-316")
worldedit_region(command="set oak_stairs[facing=north,half=bottom]")

# South side (Z=-313 becomes Z=-314)
worldedit_selection(command="pos1 569,-51,-314")
worldedit_selection(command="pos2 579,-51,-314")
worldedit_region(command="set oak_stairs[facing=south,half=bottom]")
```

**Roof Ridge (Y=-50, sides meet) - FULL BLOCKS**:
```
# Ridge at center (Z=-315, where north and south meet)
worldedit_selection(command="pos1 569,-50,-315")
worldedit_selection(command="pos2 579,-50,-315")
worldedit_region(command="set oak_planks")
```
- **Material**: oak_planks (FULL BLOCKS, not stairs!)
- **Position**: Z=-315 (center of 11-block depth)
- **Total Roof Blocks**: ~90 blocks

**Step 7: Chimney (OUTSIDE east wall) - CORRECTED INTEGRATION**

**Design**:
- Position: OUTSIDE east wall (extends from X=578 to X=579-580)
- Footprint: 2×2 blocks
- Height: Through roof to Y=-48 (2 blocks above roof peak)
- Interior fireplace at X=578 (back wall of chimney)

**Interior Fireplace (Y=-60 to Y=-59)**:
```
# Create fireplace opening (inside east wall)
rcon_command(command="fill 578 -60 -315 578 -59 -316 air replace oak_planks")

# Back of fireplace (cobblestone)
rcon_command(command="fill 579 -60 -315 579 -59 -316 cobblestone")

# Fire source (campfire inside fireplace)
rcon_command(command="setblock 578 -60 -315 campfire[lit=true]")
```

**Exterior Chimney Stack (Y=-60 to Y=-48)**:
```
# Chimney exterior walls (2×2 footprint: X=579-580, Z=-315 to -316)
# Build from ground to above roof
rcon_command(command="fill 579 -60 -315 580 -48 -316 cobblestone hollow")
```

**Chimney Cap (Y=-48)**:
```
# Overhang cap with cobblestone_slab
rcon_command(command="fill 578 -48 -314 581 -48 -317 cobblestone_slab[type=top]")
```

**Roof Integration**:
- When building roof layers, EXCLUDE chimney footprint (X=579-580, Z=-315 to -316)
- Chimney passes THROUGH roof layers
- No stairs at chimney location in roof

- **Total Chimney Blocks**: ~60 blocks

#### 3.1.3 Interior Furnishing - WITH SPATIAL ANALYSIS WORKFLOW

**CRITICAL WORKFLOW**: Use analyze_placement_area BEFORE placing ANY furniture

**Bedroom Area (Northwest corner)**:

**1. Bed Placement**:
```
# Step 1: Scan area to find exact floor Y
analyze_placement_area(
  center_x=572,
  center_y=-60,
  center_z=-318,
  radius=3,
  analysis_type="furniture_placement"
)
# Expected return: {"recommended_floor_y": -60, "placement_type": "floor"}

# Step 2: Preview furniture
place_furniture(
  furniture_id="simple_bed",
  origin_x=572,
  origin_y=-60,
  origin_z=-318,
  place_on_surface=true,
  preview_only=true
)
# Review preview output for correctness

# Step 3: Place furniture
place_furniture(
  furniture_id="simple_bed",
  origin_x=572,
  origin_y=-60,
  origin_z=-318,
  place_on_surface=true,
  preview_only=false
)

# Step 4: Validate placement (visual check)
```

**2. Dresser Placement**:
```
analyze_placement_area(
  center_x=577,
  center_y=-60,
  center_z=-318,
  radius=3,
  analysis_type="furniture_placement"
)

place_furniture(
  furniture_id="simple_dresser",
  origin_x=577,
  origin_y=-60,
  origin_z=-318,
  place_on_surface=true,
  preview_only=true
)

place_furniture(
  furniture_id="simple_dresser",
  origin_x=577,
  origin_y=-60,
  origin_z=-318,
  place_on_surface=true,
  preview_only=false
)
```

**Living Area (Southwest corner)**:

**3. Dining Table Placement**:
```
analyze_placement_area(
  center_x=574,
  center_y=-60,
  center_z=-315,
  radius=3,
  analysis_type="furniture_placement"
)

place_furniture(
  furniture_id="simple_dining_table",
  origin_x=574,
  origin_y=-60,
  origin_z=-315,
  place_on_surface=true,
  preview_only=true
)

place_furniture(
  furniture_id="simple_dining_table",
  origin_x=574,
  origin_y=-60,
  origin_z=-315,
  place_on_surface=true,
  preview_only=false
)
```

**4. Bookshelf Placement** (manual):
```
rcon_command(command="setblock 571 -59 -313 bookshelf")
rcon_command(command="setblock 571 -59 -314 bookshelf")
rcon_command(command="setblock 571 -58 -313 bookshelf")
rcon_command(command="setblock 571 -58 -314 bookshelf")
```

#### 3.1.4 Lighting Plan - DETAILED SPECIFICATIONS

**Interior Lighting**:

**1. Ceiling Glowstone (Center)**:
```
# Recessed glowstone in ceiling
rcon_command(command="setblock 574 -56 -315 glowstone")
# Cover with trapdoor for recessed look
rcon_command(command="setblock 574 -55 -315 oak_trapdoor[open=true,facing=north]")
```
- **Position**: X=574, Y=-56, Z=-315 (center of house)
- **Light Level**: 15 (glowstone)

**2. Wall Lanterns (North & South)**:
```
# North wall lantern
rcon_command(command="setblock 574 -57 -310 oak_fence")
rcon_command(command="setblock 574 -58 -310 lantern[hanging=true]")

# South wall lantern
rcon_command(command="setblock 574 -57 -320 oak_fence")
rcon_command(command="setblock 574 -58 -320 lantern[hanging=true]")
```
- **North Position**: X=574, Y=-58, Z=-310
- **South Position**: X=574, Y=-58, Z=-320
- **Light Level**: 15 each

**3. Fireplace Light**:
```
# Campfire already placed in chimney provides light
# Light level 15 at Y=-60, Z=-315
```

**4. Light Level Validation**:
```
analyze_lighting(
  x1=570, y1=-60, z1=-320,
  x2=578, y2=-55, z2=-310,
  resolution=2
)
```
- **Acceptance Criteria**: Average light level ≥10, zero dark spots <8
- **If fails**: Add torches to dark corners, re-run analysis

#### 3.1.5 Validation Gates - MAIN HOUSE

**1. Structural Validation (after walls complete)**:
```
validate_structure(
  x1=570, y1=-60, z1=-320,
  x2=578, y2=-50, z2=-310,
  resolution=1
)
```
- **Acceptance Criteria**:
  - ✓ Zero floating blocks
  - ✓ Zero gravity violations
  - ✓ Zero unsupported regions
- **If fails**: Identify floating blocks, use //undo or manually fix

**2. Roof Validation (after each roof layer)**:
```
# Before each new layer
analyze_placement_area(
  center_x=574,
  center_y=-54,
  center_z=-315,
  radius=8,
  analysis_type="roof_context"
)
# Follow returned offset exactly for next layer
```
- **Check**: Verify next_layer_offset shows UP and INWARD movement
- **Visual Check**: No stairs stacked directly above previous layer

**3. Lighting Analysis (after all lights placed)**:
```
analyze_lighting(
  x1=570, y1=-60, z1=-320,
  x2=578, y2=-55, z2=-310,
  resolution=2
)
```
- **Acceptance Criteria**:
  - ✓ Average light level ≥10
  - ✓ Zero dark spots (<8 light level)
  - ✓ Mob spawn risk: LOW
- **If fails**: Add torches/lanterns to identified dark spots

**4. Symmetry Check (after roof complete)**:
```
check_symmetry(
  x1=570, y1=-60, z1=-320,
  x2=578, y2=-50, z2=-310,
  axis="z",
  tolerance=0
)
```
- **Acceptance Criteria**: Symmetry score ≥95%
- **Note**: House should be symmetric on Z-axis (north/south match)
- **If fails**: Identify asymmetric blocks, manually correct

**5. Floor Level Verification**:
- **Check**: Floor at Y=-60 (same as surrounding ground)
- **Visual**: No visible raised foundation from exterior
- **Result**: Building appears flush with ground

---

### 3.2 Building 2: Horse Stable

#### 3.2.1 Design Specifications - CORRECTED LAYOUT

**Full Stable Layout** (12×16 footprint):
- **Front Half** (Z=-340 to -333, 8 blocks): 4 horse stalls
- **Back Half** (Z=-332 to -325, 8 blocks): Open area for movement, storage, tack
- **Center Aisle**: 3 blocks wide running north-south

**Stall Configuration**:
- **West Stalls** (2 stalls): X=590-593 (4 blocks wide)
- **Center Aisle**: X=594-596 (3 blocks wide)
- **East Stalls** (2 stalls): X=597-601 (5 blocks wide)

**Detailed Stall Dimensions**:
- **Stall 1** (West-North): X=590-593, Z=-340 to -337 (4×4 blocks)
- **Stall 2** (West-South): X=590-593, Z=-336 to -333 (4×4 blocks)
- **Stall 3** (East-North): X=597-600, Z=-340 to -337 (4×4 blocks)
- **Stall 4** (East-South): X=597-600, Z=-336 to -333 (4×4 blocks)

**Open Area**: X=590-601, Z=-332 to -325 (12×8 blocks)
- Feed storage, water trough, equipment, horse movement space

#### 3.2.2 Construction Sequence - CORRECTED

**Step 1: Floor (Y=-60) - FLUSH WITH GROUND**
```
worldedit_selection(command="pos1 590,-60,-340")
worldedit_selection(command="pos2 601,-60,-325")
worldedit_region(command="set coarse_dirt")
```
- **Block Count**: 192 blocks
- **Note**: Floor at ground level Y=-60, NOT elevated

**Step 2: Outer Walls (Y=-60 to Y=-55) - START AT FLOOR**
```
worldedit_selection(command="pos1 590,-60,-340")
worldedit_selection(command="pos2 601,-55,-325")
worldedit_region(command="walls spruce_planks")
```
- **Wall Height**: 6 blocks (Y=-60 to Y=-55)
- **Block Count**: ~220 blocks

**Step 3: Corner Posts (Y=-60 to Y=-55)**
```
# Southwest corner (590, -340)
rcon_command(command="fill 590 -60 -340 590 -55 -340 stripped_oak_log[axis=y] replace spruce_planks")

# Southeast corner (601, -340)
rcon_command(command="fill 601 -60 -340 601 -55 -340 stripped_oak_log[axis=y] replace spruce_planks")

# Northwest corner (590, -325)
rcon_command(command="fill 590 -60 -325 590 -55 -325 stripped_oak_log[axis=y] replace spruce_planks")

# Northeast corner (601, -325)
rcon_command(command="fill 601 -60 -325 601 -55 -325 stripped_oak_log[axis=y] replace spruce_planks")
```
- **Size**: 1×1 at each corner
- **Height**: Full wall height (6 blocks)

**Step 4: Stall Dividers (Y=-60 to Y=-58)**

**West Stall Divider** (between Stall 1 and Stall 2):
```
# Divider at Z=-336 (separating north and south stalls)
rcon_command(command="fill 590 -60 -336 593 -58 -336 oak_fence")
```

**East Stall Divider** (between Stall 3 and Stall 4):
```
# Divider at Z=-336
rcon_command(command="fill 597 -60 -336 600 -58 -336 oak_fence")
```

**Center Aisle Separation**:
```
# West stall gate (between west stalls and aisle)
rcon_command(command="fill 594 -60 -340 594 -58 -333 oak_fence")
# Add gates at each stall
rcon_command(command="setblock 594 -60 -338 oak_fence_gate[facing=east]")
rcon_command(command="setblock 594 -60 -335 oak_fence_gate[facing=east]")

# East stall gate (between east stalls and aisle)
rcon_command(command="fill 596 -60 -340 596 -58 -333 oak_fence")
rcon_command(command="setblock 596 -60 -338 oak_fence_gate[facing=west]")
rcon_command(command="setblock 596 -60 -335 oak_fence_gate[facing=west]")
```

**Step 5: Front Opening (Y=-60 to Y=-54, south wall) - 6 BLOCKS WIDE**
```
# Large opening for horses to enter
worldedit_selection(command="pos1 593,-60,-325")
worldedit_selection(command="pos2 598,-54,-325")
worldedit_region(command="set air")
```
- **Width**: 6 blocks (X=593-598)
- **Height**: 5 blocks (Y=-60 to Y=-54)

**Step 6: Roof (Y=-54 to Y=-48) - GABLED, EAST-WEST SLOPE**

**Note**: Roof slopes on X-axis (east-west), offset pattern uses X±1

**Roof Layer 1 (Y=-54, with 1-block overhang)**:
```
# Walls: X=590-601 (12 blocks)
# Roof with overhang: X=589-602 (14 blocks)

# West side (facing west)
worldedit_selection(command="pos1 589,-54,-340")
worldedit_selection(command="pos2 589,-54,-325")
worldedit_region(command="set spruce_stairs[facing=west,half=bottom]")

# East side (facing east)
worldedit_selection(command="pos1 602,-54,-340")
worldedit_selection(command="pos2 602,-54,-325")
worldedit_region(command="set spruce_stairs[facing=east,half=bottom]")
```

**Roof Layer 2 (Y=-53, inward X±1)**:
```
analyze_placement_area(
  center_x=595,
  center_y=-54,
  center_z=-332,
  radius=8,
  analysis_type="roof_context"
)
# Expected offset: {"x": 1, "y": 1, "z": 0}

# West side (X=589 becomes X=590)
worldedit_selection(command="pos1 590,-53,-340")
worldedit_selection(command="pos2 590,-53,-325")
worldedit_region(command="set spruce_stairs[facing=west,half=bottom]")

# East side (X=602 becomes X=601)
worldedit_selection(command="pos1 601,-53,-340")
worldedit_selection(command="pos2 601,-53,-325")
worldedit_region(command="set spruce_stairs[facing=east,half=bottom]")
```

**Continue layers 3-6 with same X±1 offset pattern until ridge at X=595**

**Roof Ridge (Y=-48, X=595)**:
```
worldedit_selection(command="pos1 595,-48,-340")
worldedit_selection(command="pos2 595,-48,-325")
worldedit_region(command="set spruce_planks")
```

**Step 7: Details**

**Water Trough**:
```
rcon_command(command="setblock 595 -60 -327 cauldron[level=3]")
```

**Hay Bales** (scattered in stalls):
```
rcon_command(command="setblock 591 -60 -338 hay_block")
rcon_command(command="setblock 598 -60 -338 hay_block")
rcon_command(command="setblock 591 -60 -334 hay_block")
rcon_command(command="setblock 598 -60 -334 hay_block")
```

**Lanterns** (on center posts):
```
# Center aisle lighting
rcon_command(command="setblock 595 -57 -338 oak_fence")
rcon_command(command="setblock 595 -58 -338 lantern[hanging=true]")

rcon_command(command="setblock 595 -57 -332 oak_fence")
rcon_command(command="setblock 595 -58 -332 lantern[hanging=true]")
```

#### 3.2.3 Horse Spawning - CORRECTED SYNTAX

**Modern Minecraft Syntax** (1.20+):
```
# Stall 1 (West-North)
rcon_command(command="summon minecraft:horse 591.5 -60 -338.5 {Tame:1b,SaddleItem:{id:\"minecraft:saddle\",Count:1b}}")

# Stall 2 (West-South)
rcon_command(command="summon minecraft:horse 591.5 -60 -334.5 {Tame:1b,SaddleItem:{id:\"minecraft:saddle\",Count:1b}}")

# Stall 3 (East-North)
rcon_command(command="summon minecraft:horse 598.5 -60 -338.5 {Tame:1b,SaddleItem:{id:\"minecraft:saddle\",Count:1b}}")

# Stall 4 (East-South)
rcon_command(command="summon minecraft:horse 598.5 -60 -334.5 {Tame:1b,SaddleItem:{id:\"minecraft:saddle\",Count:1b}}")
```
- **Note**: NO Variant NBT tag (colors are random, more natural)
- **Tame**: 1b (horses are tamed)
- **Saddle**: Each horse has saddle equipped
- **Coordinates**: Center of each stall (.5 for precise placement)

#### 3.2.4 Validation Gates - STABLE

**Structural Validation**:
```
validate_structure(
  x1=590, y1=-60, z1=-340,
  x2=601, y2=-48, z2=-325,
  resolution=1
)
```

**Lighting Analysis**:
```
analyze_lighting(
  x1=590, y1=-60, z1=-340,
  x2=601, y2=-55, z2=-325,
  resolution=2
)
```

**Stall Functionality Check**:
- Visual: Each horse in correct stall
- Gates: All fence gates open/close correctly
- Access: Center aisle clear for movement

---

### 3.3 Building 3: Garden Area

#### 3.3.1 Construction Sequence - CORRECTED WATER PLACEMENT

**Step 1: Perimeter Fence (Y=-60)**
```
# North fence
rcon_command(command="fill 570 -60 -340 584 -60 -340 oak_fence")

# South fence
rcon_command(command="fill 570 -60 -329 584 -60 -329 oak_fence")

# West fence
rcon_command(command="fill 570 -60 -340 570 -60 -329 oak_fence")

# East fence
rcon_command(command="fill 584 -60 -340 584 -60 -329 oak_fence")

# South gate (entrance)
rcon_command(command="setblock 577 -60 -329 oak_fence_gate[facing=south]")
```

**Step 2: Water Source - OPTION A (EFFICIENT)**
```
# Single water source at center (hydrates all farmland within 4 blocks)
rcon_command(command="setblock 577 -61 -334 water")
```
- **Position**: Center of garden (X=577, Z=-334)
- **Hydration**: Covers entire 13×10 interior (4-block radius)
- **Space Saved**: 129 blocks available for crops (vs 120 with channel)

**Alternative - OPTION B (AESTHETIC)**:
```
# Dig channel one block below farmland
worldedit_selection(command="pos1 577,-62,-339")
worldedit_selection(command="pos2 577,-62,-330")
worldedit_region(command="set water")

# Add bridge over channel
rcon_command(command="setblock 577 -61 -334 oak_slab[type=top]")
```
- **Channel**: Y=-62 (one block BELOW farmland at Y=-61)
- **Farmland**: Y=-61 on both sides of channel

**RECOMMENDED**: Use Option A for maximum crop yield

**Step 3: Tilled Farmland (Y=-61)**
```
# Full interior area (13×10) minus water source
worldedit_selection(command="pos1 571,-61,-339")
worldedit_selection(command="pos2 583,-61,-330")
worldedit_region(command="set farmland")

# Replace water source position back to water
rcon_command(command="setblock 577 -61 -334 water")
```
- **Total Farmland**: 129 blocks (130 - 1 water source)

**Step 4: Crop Planting**

**West Section** (X=571-576, wheat and carrots):
```
# Wheat rows (alternating)
rcon_command(command="fill 571 -60 -339 571 -60 -330 wheat[age=7]")
rcon_command(command="fill 573 -60 -339 573 -60 -330 wheat[age=7]")
rcon_command(command="fill 575 -60 -339 575 -60 -330 wheat[age=7]")

# Carrot rows (alternating)
rcon_command(command="fill 572 -60 -339 572 -60 -330 carrots[age=7]")
rcon_command(command="fill 574 -60 -339 574 -60 -330 carrots[age=7]")
rcon_command(command="fill 576 -60 -339 576 -60 -330 carrots[age=7]")
```

**East Section** (X=578-583, potatoes and beetroot):
```
# Potato rows
rcon_command(command="fill 578 -60 -339 578 -60 -330 potatoes[age=7]")
rcon_command(command="fill 580 -60 -339 580 -60 -330 potatoes[age=7]")
rcon_command(command="fill 582 -60 -339 582 -60 -330 potatoes[age=7]")

# Beetroot rows
rcon_command(command="fill 579 -60 -339 579 -60 -330 beetroots[age=3]")
rcon_command(command="fill 581 -60 -339 581 -60 -330 beetroots[age=3]")
rcon_command(command="fill 583 -60 -339 583 -60 -330 beetroots[age=3]")
```
- **Growth Stage**: age=7 (fully grown) for wheat/carrots/potatoes
- **Beetroots**: age=3 (fully grown for beetroots)

**Step 5: Details**

**Scarecrow**:
```
# Armor stand with pumpkin
rcon_command(command="summon armor_stand 584.5 -60 -339.5 {ShowArms:1b,NoGravity:1b,Rotation:[270f,0f]}")
rcon_command(command="replaceitem entity @e[type=armor_stand,limit=1,sort=nearest] armor.head carved_pumpkin")
```

**Compost Bin**:
```
rcon_command(command="setblock 577 -60 -330 composter")
```

**Lighting**:
```
# Corner lanterns
rcon_command(command="setblock 570 -59 -340 lantern[hanging=false]")
rcon_command(command="setblock 584 -59 -340 lantern[hanging=false]")
rcon_command(command="setblock 570 -59 -329 lantern[hanging=false]")
rcon_command(command="setblock 584 -59 -329 lantern[hanging=false]")
```

---

### 3.4 Building 4: Storage Barn

#### 3.4.1 Construction Sequence - CORRECTED

**Step 1: Floor (Y=-60) - FLUSH WITH GROUND**
```
worldedit_selection(command="pos1 610,-60,-320")
worldedit_selection(command="pos2 623,-60,-303")
worldedit_region(command="set coarse_dirt")
```
- **Block Count**: 252 blocks
- **Note**: Floor at Y=-60, NOT elevated

**Step 2: Walls (Y=-60 to Y=-53) - START AT FLOOR**
```
worldedit_selection(command="pos1 610,-60,-320")
worldedit_selection(command="pos2 623,-53,-303")
worldedit_region(command="walls spruce_planks")
```
- **Wall Height**: 8 blocks (Y=-60 to Y=-53)
- **Block Count**: ~350 blocks

**Step 3: Corner Posts (Y=-60 to Y=-53) - 2×2 FOR LARGE BARN**
```
# Southwest corner (2×2)
rcon_command(command="fill 610 -60 -320 611 -53 -319 stripped_oak_log[axis=y] replace spruce_planks")

# Southeast corner (2×2)
rcon_command(command="fill 622 -60 -320 623 -53 -319 stripped_oak_log[axis=y] replace spruce_planks")

# Northwest corner (2×2)
rcon_command(command="fill 610 -60 -304 611 -53 -303 stripped_oak_log[axis=y] replace spruce_planks")

# Northeast corner (2×2)
rcon_command(command="fill 622 -60 -304 623 -53 -303 stripped_oak_log[axis=y] replace spruce_planks")
```
- **Size**: 2×2 at each corner (larger barn needs larger posts)
- **Height**: Full wall height (8 blocks)

**Step 4: Side Beams (Y=-60 to Y=-53) - VERTICAL SUPPORTS**
```
# West wall beams (every 5 blocks)
rcon_command(command="fill 610 -60 -315 610 -53 -315 stripped_oak_log[axis=y] replace spruce_planks")
rcon_command(command="fill 610 -60 -310 610 -53 -310 stripped_oak_log[axis=y] replace spruce_planks")

# East wall beams
rcon_command(command="fill 623 -60 -315 623 -53 -315 stripped_oak_log[axis=y] replace spruce_planks")
rcon_command(command="fill 623 -60 -310 623 -53 -310 stripped_oak_log[axis=y] replace spruce_planks")
```

**Step 5: Large Doors (Y=-60 to Y=-57, front wall)**
```
# 6 blocks wide, 6 blocks tall opening
worldedit_selection(command="pos1 613,-60,-303")
worldedit_selection(command="pos2 618,-57,-303")
worldedit_region(command="set air")
```

**Step 6: Hayloft Floor (Y=-55)**
```
worldedit_selection(command="pos1 611,-55,-319")
worldedit_selection(command="pos2 622,-55,-304")
worldedit_region(command="set oak_planks")
```
- **Block Count**: 132 blocks

**Ladder Access**:
```
# Oak ladder on west wall
rcon_command(command="fill 611 -60 -310 611 -55 -310 oak_ladder[facing=east]")
```

**Step 7: Roof (Y=-52 to Y=-45) - GABLED, WITH OVERHANG**

**Roof runs NORTH-SOUTH** (slopes on Z-axis):
- **Walls**: Z=-320 to Z=-303 (18 blocks deep)
- **Roof with overhang**: Z=-321 to Z=-302 (20 blocks, +1 each side)

**Layer 1 (Y=-52, with overhang)**:
```
# Walls: X=610-623 (14 blocks)
# Roof: X=609-624 (16 blocks, +1 overhang each side)

# North side
worldedit_selection(command="pos1 609,-52,-321")
worldedit_selection(command="pos2 624,-52,-321")
worldedit_region(command="set spruce_stairs[facing=north,half=bottom]")

# South side
worldedit_selection(command="pos1 609,-52,-302")
worldedit_selection(command="pos2 624,-52,-302")
worldedit_region(command="set spruce_stairs[facing=south,half=bottom]")
```

**Layers 2-8**: Follow same Z±1 offset pattern (8 layers total until ridge)

**Ridge** (Y=-45):
```
worldedit_selection(command="pos1 609,-45,-311")
worldedit_selection(command="pos2 624,-45,-311")
worldedit_region(command="set spruce_planks")
```

**Step 8: Storage Details**

**Hay Bales in Loft**:
```
# Random placement (20 bales)
rcon_command(command="setblock 612 -55 -318 hay_block")
rcon_command(command="setblock 615 -55 -317 hay_block")
rcon_command(command="setblock 618 -55 -316 hay_block")
[Continue for 17 more hay blocks at various positions]
```

**Barrels on Ground Floor**:
```
# Along walls
rcon_command(command="fill 611 -60 -319 614 -60 -319 barrel[facing=up]")
rcon_command(command="fill 619 -60 -319 622 -60 -319 barrel[facing=up]")
```

**Chests in Corners**:
```
rcon_command(command="setblock 611 -60 -318 chest[facing=north]")
rcon_command(command="setblock 622 -60 -318 chest[facing=north]")
```

**Lanterns** (ceiling beams):
```
rcon_command(command="setblock 616 -52 -310 oak_fence")
rcon_command(command="setblock 616 -53 -310 lantern[hanging=true]")

rcon_command(command="setblock 616 -52 -315 oak_fence")
rcon_command(command="setblock 616 -53 -315 lantern[hanging=true]")
```

---

### 3.5 Building 5: Ranch Elements

#### 3.5.1 Connecting Paths

**Path Material**: coarse_dirt (3 blocks wide)

**House to Stable** (East path):
```
# X=570-590, Z=-330 to -332
rcon_command(command="fill 570 -60 -332 590 -60 -330 coarse_dirt")
```

**House to Garden** (North path):
```
# X=570-572, Z=-320 to -340
rcon_command(command="fill 570 -60 -340 572 -60 -320 coarse_dirt")
```

**Stable to Barn** (East path):
```
# X=601-610, Z=-330 to -332
rcon_command(command="fill 601 -60 -332 610 -60 -330 coarse_dirt")
```

#### 3.5.2 Perimeter Fencing

**Full Ranch Perimeter**:
```
# North fence (along garden/stable)
rcon_command(command="fill 570 -60 -350 610 -60 -350 oak_fence")

# South fence (along house/barn)
rcon_command(command="fill 570 -60 -300 625 -60 -300 oak_fence")

# West fence
rcon_command(command="fill 560 -60 -350 560 -60 -300 oak_fence")

# East fence
rcon_command(command="fill 625 -60 -350 625 -60 -300 oak_fence")
```

**Gates at Path Intersections**:
```
rcon_command(command="setblock 570 -60 -330 oak_fence_gate[facing=west]")
rcon_command(command="setblock 590 -60 -330 oak_fence_gate[facing=east]")
rcon_command(command="setblock 610 -60 -330 oak_fence_gate[facing=east]")
```

#### 3.5.3 Additional Details

**Lighting** (lanterns every 8 blocks on fence posts):
```
# West fence lights
rcon_command(command="setblock 560 -59 -342 lantern[hanging=false]")
rcon_command(command="setblock 560 -59 -334 lantern[hanging=false]")
rcon_command(command="setblock 560 -59 -326 lantern[hanging=false]")
rcon_command(command="setblock 560 -59 -318 lantern[hanging=false]")
rcon_command(command="setblock 560 -59 -310 lantern[hanging=false]")

[Continue for north, south, east fences]
```

**Hitching Posts** (near stable entrance):
```
rcon_command(command="setblock 592 -60 -326 oak_fence")
rcon_command(command="setblock 598 -60 -326 oak_fence")
```

**Tool Storage** (barrels near barn):
```
rcon_command(command="setblock 610 -60 -304 barrel[facing=west]")
rcon_command(command="setblock 610 -60 -305 barrel[facing=west]")
```

**Scattered Hay Bales**:
```
rcon_command(command="setblock 592 -60 -328 hay_block")
rcon_command(command="setblock 609 -60 -322 hay_block")
[Add 8-10 more in various positions]
```

---

## 4. Implementation Workflow

### 4.1 Build Order (Separate Jobs)

#### Job 1: Main Ranch House (45 minutes)
- Foundation/floor: 5 min
- Walls + corner posts: 8 min
- Door and windows with frames: 5 min
- Roof (6 layers with offset validation): 15 min
- Chimney: 7 min
- Interior furniture (4 pieces with spatial scan): 10 min
- Lighting + validation: 5 min
- Fixes from validation: 5 min (buffer)

#### Job 2: Horse Stable (60 minutes)
- Foundation: 5 min
- Walls + corner posts: 10 min
- Stall dividers (manual fence placement): 15 min
- Roof (7 layers with offset): 15 min
- Details (gates, water trough, hay): 10 min
- Horse spawning (4 horses): 5 min
- Lighting + validation: 5 min
- Fixes: 5 min

#### Job 3: Garden Area (25 minutes)
- Fence perimeter: 8 min
- Farmland prep: 5 min
- Water source: 2 min
- Crop planting (129 blocks): 8 min
- Details (scarecrow, compost): 2 min

#### Job 4: Storage Barn (50 minutes)
- Foundation: 5 min
- Walls + corner posts + beams: 12 min
- Hayloft floor + ladder: 8 min
- Roof (8 layers with offset): 20 min
- Storage details (hay, barrels, chests): 10 min
- Validation: 5 min

#### Job 5: Ranch Elements (30 minutes)
- Paths (coarse_dirt placement): 8 min
- Perimeter fencing: 10 min
- Details (hay, hitching posts, tool storage): 7 min
- Lighting (lanterns on fence posts): 5 min
- Ranch-wide lighting validation: 5 min

**Total Estimated Time**: 210 minutes (3.5 hours)

**Note**: This is realistic for junior engineer with all corrections applied. Add 30-minute buffer for unexpected issues = **4 hours total**.

---

## 5. Quality Assurance

### 5.1 Self-Review Checklist (Before Submission)

**Foundation & Floors**:
- [ ] All floor Y levels = ground Y (Y=-60)
- [ ] No raised foundations visible from exterior
- [ ] Buildings appear flush with ground

**Materials**:
- [ ] Material palette matches rustic_cottage exactly (50/25/20/5)
- [ ] Primary: oak_planks (50%)
- [ ] Secondary: cobblestone (25%, chimney only)
- [ ] Roof: oak_stairs (20%)
- [ ] Accent: stripped_oak_log (5%, corner posts)

**Roof Construction**:
- [ ] All roof layers have explicit coordinates showing offset
- [ ] Each layer steps UP (Y+1) and INWARD (X or Z ±1)
- [ ] No vertical stacking of stairs
- [ ] All roofs have 1-block overhang on all sides
- [ ] Ridge uses FULL BLOCKS (oak_planks/spruce_planks), not stairs

**Structural Details**:
- [ ] All corner posts specified (height, size, material, orientation)
- [ ] Main house: 1×1 corner posts
- [ ] Barn: 2×2 corner posts
- [ ] All corner posts use stripped_oak_log[axis=y]

**Windows & Doors**:
- [ ] All windows have complete frames (stripped_oak_log borders)
- [ ] All doors are 2 blocks tall (not 3)
- [ ] Door block states include facing, half, hinge

**Furniture**:
- [ ] All furniture placement includes analyze_placement_area workflow
- [ ] All furniture previewed before final placement
- [ ] Spatial scan → preview → place sequence for each piece

**Lighting**:
- [ ] All lighting positions specified with exact coordinates
- [ ] All lights attach to blocks (no floating)
- [ ] Sufficient coverage (light level ≥8 throughout)

**Validation**:
- [ ] Structural validation coordinates specified for each building
- [ ] Lighting analysis coordinates specified
- [ ] Symmetry check coordinates specified (where applicable)
- [ ] Acceptance criteria defined for each validation

**Timeline**:
- [ ] Realistic timeline (3.5-4 hours, not 80 minutes)
- [ ] Per-phase breakdown with buffer time

### 5.2 Coordinate Verification Table

| Building | Floor Y | Corner 1 (X,Y,Z) | Corner 2 (X,Y,Z) | Overhang? | Corner Posts |
|----------|---------|------------------|------------------|-----------|--------------|
| Main House | -60 (flush) | 570,-60,-320 | 578,-56,-310 | Yes (1 block) | 1×1, stripped_oak_log[axis=y] |
| Stable | -60 (flush) | 590,-60,-340 | 601,-55,-325 | Yes (1 block) | 1×1, stripped_oak_log[axis=y] |
| Garden | -61 (farmland) | 570,-61,-340 | 584,-60,-329 | N/A | N/A (fence only) |
| Barn | -60 (flush) | 610,-60,-320 | 623,-53,-303 | Yes (1 block) | 2×2, stripped_oak_log[axis=y] |

**Spacing Between Buildings**:
- House to Stable: 12 blocks (adequate)
- House to Barn: 32 blocks (adequate)
- Stable to Barn: 9 blocks (adequate)
- Garden to House: 20 blocks (adequate)

**No Overlaps**: All footprints verified clear

---

## 6. Risk Assessment - UPDATED

### 6.1 Technical Risks

#### Risk 1: Roof Construction Complexity
- **Probability**: Medium
- **Impact**: High (visible from exterior)
- **Mitigation**: Use analyze_placement_area with roof_context before each layer, follow strict offset pattern documented in plan

#### Risk 2: Furniture Placement Errors
- **Probability**: Low (with spatial analysis workflow)
- **Impact**: Medium (interior quality)
- **Mitigation**: ALWAYS use analyze_placement_area before place_furniture, preview_only=true first, follow documented workflow

#### Risk 3: Horse Spawning Issues
- **Probability**: Low
- **Impact**: Medium (missing key feature)
- **Mitigation**: Use modern syntax (no Variant NBT), test spawn in one stall first, verify coordinates

#### Risk 4: Coordinate Calculation Errors
- **Probability**: High (complex multi-building layout)
- **Impact**: High (buildings overlap or misaligned)
- **Mitigation**: Coordinate verification table created, all coordinates pre-calculated, verify with calculate_region_size before building, mark boundaries with temporary blocks

#### Risk 5: Material Palette Inconsistency
- **Probability**: Medium
- **Impact**: Medium (visual inconsistency)
- **Mitigation**: Strict palette documented (50/25/20/5), material choices specified per building, visual check after each building

#### Risk 6: Floor Elevation Errors
- **Probability**: Low (well documented in V2)
- **Impact**: High (violates core principle)
- **Mitigation**: All floor Y levels specified as Y=-60, visual verification after each foundation, check for visible raised base from exterior

---

## 7. Success Metrics

### 7.1 Completion Criteria
- [ ] All 5 buildings constructed
- [ ] All interior spaces furnished
- [ ] All validation gates passed
- [ ] No structural issues (validate_structure: 100% pass)
- [ ] Adequate lighting throughout (analyze_lighting: no dark spots <8)
- [ ] Horses spawned and contained in stalls
- [ ] Garden planted and functional
- [ ] Paths and fencing complete

### 7.2 Quality Metrics
- **Structural validation**: 100% pass (no floating blocks, no gravity violations)
- **Lighting coverage**: 100% (no light level <8, mob spawn risk LOW)
- **Symmetry** (where intended): >95% (main house on Z-axis)
- **Material palette adherence**: 100% (rustic_cottage: 50/25/20/5)
- **Architectural standards**: 100%
  - Corner pillars contrast with walls (✓ stripped_oak_log vs oak_planks/spruce_planks)
  - Window frames (✓ stripped_oak_log borders)
  - Roof overhangs (✓ 1 block on all sides)
  - Roof stairs properly oriented (✓ facing direction + half specified)
  - Lights attached to blocks (✓ no floating lanterns)
  - Floor flush with ground (✓ Y=-60 for all buildings)

### 7.3 User Satisfaction
- Complete rustic ranch as requested
- All buildings distinct and functional
- Cohesive aesthetic throughout (rustic_cottage palette)
- Impressive visual impact (proper proportions, details, lighting)
- No obvious construction errors (no vertical stair stacking, no floating furniture, no elevated foundations)

---

## 8. Dependencies & Prerequisites

### 8.1 Server Requirements
- WorldEdit plugin installed and functional
- RCON access configured
- Permissions for all WorldEdit commands
- Permissions for /summon, /setblock, /fill commands

### 8.2 Resource Availability
- All materials available in creative inventory
- Sufficient WorldEdit history buffer for undo operations
- Server performance adequate for large region operations (up to 252 blocks at once)

### 8.3 Tool Access
- All 46 MCP tools functional
- Pattern libraries loaded (building_patterns.json, terrain_patterns.json)
- Furniture catalog accessible (minecraft_furniture_layouts.json)
- Material palettes loaded (minecraft_material_palettes.json)

---

## 9. Post-Build Documentation

### 9.1 Deliverables
- Screenshot each building from multiple angles (north, south, east, west, aerial)
- Document final coordinates in summary table
- Record actual material usage vs estimates
- Note any deviations from plan with justification
- Capture any custom designs for reuse

### 9.2 Potential Enhancements (Future)
- Add pasture area with more horses
- Expand garden with pumpkin/melon patches
- Add windmill or grain silo
- Create horse training/riding area
- Add ranch signage (hanging signs on posts)
- Add chicken coop near house
- Create storage shed for farming tools

---

## 10. Appendices

### Appendix A: Material Quantities (Updated Estimates)

**Primary Materials**:
- oak_planks: ~800 blocks (main house walls/floors, roof ridges)
- spruce_planks: ~600 blocks (stable/barn walls)
- cobblestone: ~100 blocks (chimney only)
- stripped_oak_log: ~180 blocks (corner posts, window frames, beams)
- oak_stairs: ~200 blocks (main house roof)
- spruce_stairs: ~350 blocks (stable + barn roofs)

**Secondary Materials**:
- glass_pane: ~24 blocks (windows)
- oak_fence: ~250 blocks (stall dividers, garden fence, perimeter)
- oak_fence_gate: ~12 blocks
- coarse_dirt: ~550 blocks (stable/barn floors, paths)
- farmland: ~130 blocks
- hay_block: ~60 blocks

**Decorative Materials**:
- lantern: ~35 blocks
- barrel: ~20 blocks
- cauldron: 1 block
- oak_door: 4 blocks
- oak_ladder: 6 blocks
- chest: 4 blocks
- campfire: 1 block
- composter: 1 block
- glowstone: 1 block
- oak_trapdoor: 1 block

**Entities**:
- Horse: 4 spawns (tamed, saddled)
- Armor stand: 1 (scarecrow)

### Appendix B: Rustic Cottage Palette Reference

**Source**: context/minecraft_material_palettes.json, "rustic_cottage" entry

```json
{
  "primary": {
    "block": "oak_planks",
    "percentage": 50,
    "usage": "Walls, siding, main structure"
  },
  "secondary": {
    "block": "cobblestone",
    "percentage": 25,
    "usage": "Foundation, chimney, lower walls"
  },
  "roof": {
    "block": "oak_stairs",
    "percentage": 20,
    "usage": "Roof slopes, warm wood shingles"
  },
  "accent": {
    "block": "dark_oak_log",
    "percentage": 5,
    "usage": "Corner beams, structural support, decorative framing"
  }
}
```

**Implementation Notes**:
- Primary: oak_planks for main house (50%)
- Secondary: cobblestone ONLY for chimney (25% of total = ~100 blocks)
- Roof: oak_stairs for main house roof (20%)
- Accent: stripped_oak_log for ALL corner posts (5% = ~180 blocks including window frames)
- Variation: spruce_planks/spruce_stairs for stable/barn (variety between buildings while maintaining rustic theme)

### Appendix C: Roof Offset Pattern Reference

**North-South Gabled Roof** (slopes on Z-axis):
- Layer N: Y=base+N, Z_north=start+N, Z_south=end-N
- Offset per layer: UP Y+1, INWARD Z±1
- Example: If Layer 1 at Z=-320 (north), Layer 2 at Z=-319, Layer 3 at Z=-318, etc.

**East-West Gabled Roof** (slopes on X-axis):
- Layer N: Y=base+N, X_west=start+N, X_east=end-N
- Offset per layer: UP Y+1, INWARD X±1
- Example: If Layer 1 at X=589 (west), Layer 2 at X=590, Layer 3 at X=591, etc.

**Always**: Use analyze_placement_area(analysis_type="roof_context") before each layer to verify offset pattern

### Appendix D: Horse Spawn Syntax (Minecraft 1.20+)

**Modern Syntax** (NO Variant NBT):
```
/summon minecraft:horse X Y Z {Tame:1b,SaddleItem:{id:"minecraft:saddle",Count:1b}}
```

**Old Syntax** (1.12-1.19, DEPRECATED):
```
/summon minecraft:horse X Y Z {Variant:0}
```

**Note**: Modern Minecraft randomizes horse colors naturally, no Variant tag needed

### Appendix E: Crop Growth Stages

**All crops use age property**:
- **Wheat, Carrots, Potatoes**: age=0 (planted) to age=7 (fully grown)
- **Beetroots**: age=0 (planted) to age=3 (fully grown)

**Commands**:
```
/setblock X Y Z wheat[age=7]
/setblock X Y Z carrots[age=7]
/setblock X Y Z potatoes[age=7]
/setblock X Y Z beetroots[age=3]
```

---

## 11. Changes from V1

**Critical Fixes Applied**:
1. ✅ Removed cobblestone foundations - Floor Y = Ground Y (Y=-60)
2. ✅ Fixed material palette to match rustic_cottage exactly (50/25/20/5)
3. ✅ Added detailed roof layer coordinates with explicit offset pattern (6 layers for house, 7 for stable, 8 for barn)
4. ✅ Fixed floor Y levels - All buildings flush at Y=-60
5. ✅ Added 1-block roof overhangs on all buildings
6. ✅ Specified corner pillar details (1×1 house/stable, 2×2 barn, stripped_oak_log[axis=y], full height)
7. ✅ Added analyze_placement_area workflows before EVERY furniture piece and roof layer

**High Priority Fixes**:
8. ✅ Complete window frame specifications (block-by-block stripped_oak_log borders)
9. ✅ Fixed door dimensions (2 blocks tall: Y=-60 to Y=-59)
10. ✅ Revised stable stall layout (4 stalls in front half, open area in back half, full 12×16 footprint)
11. ✅ Fixed chimney integration (outside wall at X=579-580, through roof, with interior fireplace)
12. ✅ Optimized garden water (single source at Y=-61 center, or channel at Y=-62)
13. ✅ Added lighting specifications (exact coordinates for each lantern/glowstone with attachment points)
14. ✅ Updated timeline estimates (3.5-4 hours realistic, not 80 minutes)

**Medium Priority Fixes**:
15. ✅ Added roof validation gates (analyze_placement_area before each layer with roof_context)
16. ✅ Expanded validation criteria (specific coordinates, acceptance criteria, failure responses)
17. ✅ Added missing risks (coordinate errors, material drift, floor elevation errors)
18. ✅ Specified all block states (axis=y for logs, facing/half for stairs/doors, level for cauldron)

---

## End of Implementation Plan V2

**Status**: Ready for Final Approval

**Next Steps**:
1. Self-review with checklist above ✅
2. Verify all 18 issues from Cody's review addressed ✅
3. Submit V2 for final approval
4. Upon approval, begin implementation
5. Track progress with todo list
6. Request code review after completion

**Document Version**: 2.0 (Post-Review)
**Review Score Target**: 90-95/100
**Estimated Implementation Time**: 3.5-4 hours

---

**Plan Complete - Ready for Implementation**
