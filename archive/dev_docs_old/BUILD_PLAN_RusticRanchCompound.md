# BUILD PLAN: Rustic Ranch Compound

## Project Overview

**Project Type**: Multi-building ranch compound
**Style**: Rustic ranch/farmstead
**Location**: In front of player ereidjustpeed
**Player Position**: X=541, Y=-60, Z=-352 (facing North)
**Ground Level**: Y=-61
**Build Direction**: North of player (-Z direction)

## Vision

A complete working ranch compound with authentic rustic aesthetics featuring:
- Main ranch home (residential)
- Functional horse stable with LIVE HORSES
- Garden area with crops
- Ranch elements (paths, fencing, hay bales, water trough)

## Material Palette: Rustic Cottage

**Primary Materials (50%)**:
- `oak_planks` - Main walls, siding
- `spruce_planks` - Variation, trim

**Secondary Materials (25%)**:
- `cobblestone` - Foundation, pathways
- `stone` - Structural accents

**Roofing (20%)**:
- `oak_stairs` - Primary roof material
- `spruce_stairs` - Variation, darker accents

**Accent Materials (5%)**:
- `dark_oak_log` - Corner posts, beams, structural framing
- `stripped_spruce_log` - Decorative timber, porch columns

**Additional Ranch Materials**:
- `oak_fence` - Corral fencing, railings
- `hay_block` - Hay bales, storage
- `water` - Water trough
- `dirt` - Garden plots
- `farmland` - Tilled soil
- `wheat`, `carrots`, `potatoes` - Crops

**Color Scheme**: Warm browns (oak/spruce), gray stone, natural rustic feel

---

## Site Layout

### Build Area Coordinates

**Overall Compound**: 60 blocks × 50 blocks
**Base Coordinates**: X=521 to X=581, Z=-410 to Z=-360, Y=-61 (ground level)

### Building Positions (North of Player)

**Building 1 - Main Ranch Home**:
- Position: X=530, Z=-395 (Northwest sector)
- Footprint: 14×12 blocks
- Height: 2 floors + roof (12 blocks total)
- Orientation: Entrance facing South (toward player)

**Building 2 - Horse Stable**:
- Position: X=555, Z=-395 (Northeast sector)
- Footprint: 18×10 blocks
- Height: 1 floor + roof (8 blocks total)
- Orientation: Entrance facing West (toward home)

**Building 3 - Garden Area**:
- Position: X=530, Z=-375 (South sector, between buildings)
- Footprint: 20×12 blocks (fenced area)
- Height: Ground level (crops + fence)

**Ranch Elements**:
- Paths connecting all buildings
- Corral fence extending from stable
- Water trough near stable
- Hay bale storage area
- Hitching posts

---

## Building 1: Main Ranch Home

### Specifications

**Footprint**: 14 blocks (X) × 12 blocks (Z)
**Base Coordinates**: X=530, Y=-61, Z=-395 to X=544, Y=-61, Z=-383
**Height**: 12 blocks total (Y=-61 to Y=-49)
- Floor 1: Y=-61 to Y=-57 (5 blocks)
- Floor 2: Y=-57 to Y=-53 (4 blocks)
- Roof: Y=-53 to Y=-49 (4 blocks)

### Floor Plan

**First Floor** (Y=-61 to Y=-57):
- Living room: 8×8 blocks (Northwest)
- Kitchen: 6×8 blocks (Northeast)
- Entry/mudroom: 6×4 blocks (South entrance)
- Staircase: 3×4 blocks (center)

**Second Floor** (Y=-57 to Y=-53):
- Master bedroom: 7×8 blocks (North)
- Second bedroom: 7×4 blocks (South)
- Hallway: 3 blocks wide (center)

### Materials

**Foundation & Walls**:
- Floor: `oak_planks` at Y=-61 (flush with ground)
- Exterior walls: `oak_planks` (primary)
- Corner posts: `dark_oak_log` (accent, REQUIRED for contrast)
- Interior walls: `spruce_planks`
- Foundation trim: `cobblestone` (visible below windows)

**Roof**:
- Type: Gable roof (East-West ridge)
- Material: `oak_stairs[facing=north/south,half=bottom]`
- Pitch: Steep (1:1 rise/run)
- Overhang: 2 blocks past walls
- Ridge: `oak_planks` (full blocks at peak)

**Openings**:
- Front door: `oak_door` (2 blocks tall, centered)
- Windows: 2×2 `glass_pane` with `spruce_planks` frames (1 block trim)
- Window spacing: 3 blocks apart (standard rhythm)
- Window height: Y=-58 (eye level, first floor)

**Lighting**:
- Exterior: `lantern` on chains from porch overhang
- Interior: `torch` on walls (every 8 blocks)
- Ceiling: `glowstone` inset in planks (kitchen)

### Key Features

- Front porch: 3 blocks deep, `oak_fence` railing
- Chimney: `cobblestone` 3×3, extends 3 blocks above roof
- Shutters: `oak_trapdoor[facing=east/west]` beside windows
- Flower boxes: `oak_fence` with flowers under windows

---

## Building 2: Horse Stable

### Specifications

**Footprint**: 18 blocks (X) × 10 blocks (Z)
**Base Coordinates**: X=555, Y=-61, Z=-395 to X=573, Y=-61, Z=-385
**Height**: 8 blocks total (Y=-61 to Y=-53)
- Main floor: Y=-61 to Y=-57 (6 blocks ceiling height)
- Roof: Y=-57 to Y=-53 (4 blocks)

### Floor Plan

**Interior Layout**:
- Entry corridor: 3 blocks wide (center, running North-South)
- Horse stalls: 4 stalls, 3×4 blocks each (2 per side)
- Tack room: 4×6 blocks (North end)
- Hay storage: 4×4 blocks (South end)

**Stall Configuration**:
- Stall size: 3 blocks wide × 4 blocks deep
- Stall dividers: `oak_fence` (1 block thick)
- Stall gates: `oak_fence_gate`
- Feeding trough: `cauldron` filled with water
- Bedding: `hay_block` on floor

### Materials

**Structure**:
- Floor: `oak_planks` at Y=-61
- Walls: `spruce_planks` (primary)
- Corner posts: `stripped_spruce_log` (4×4 posts, accent)
- Interior dividers: `oak_fence`
- Foundation: `cobblestone` (visible 1 block)

**Roof**:
- Type: Gable roof (North-South ridge)
- Material: `spruce_stairs[facing=east/west,half=bottom]`
- Pitch: Moderate (1:1)
- Overhang: 1 block
- Ridge: `spruce_planks`

**Openings**:
- Main entrance: Double door 2 blocks wide (West side, facing home)
- Stall doors: `oak_fence_gate` per stall
- Windows: Small 1×2 `glass_pane` with `oak_fence` bars (4 total, high placement)
- Ventilation: Leave 1-block gaps near roof peak (no glass)

**Lighting**:
- Exterior: `lantern` on chains at entrance
- Interior: `torch` on posts (every 6 blocks)
- Stalls: `lantern` hanging from ceiling per stall

### CRITICAL: Live Horses

**MUST spawn actual horses in stalls after construction**:

After stable is complete, execute these commands for each stall:

```
Stall 1 (X=557, Z=-393):
/summon minecraft:horse 557 -60 -393 {Tame:1b,SaddleItem:{id:"minecraft:saddle",Count:1b}}

Stall 2 (X=557, Z=-388):
/summon minecraft:horse 557 -60 -388 {Tame:1b,SaddleItem:{id:"minecraft:saddle",Count:1b}}

Stall 3 (X=570, Z=-393):
/summon minecraft:horse 570 -60 -393 {Tame:1b,SaddleItem:{id:"minecraft:saddle",Count:1b}}

Stall 4 (X=570, Z=-388):
/summon minecraft:horse 570 -60 -388 {Tame:1b,SaddleItem:{id:"minecraft:saddle",Count:1b}}
```

**Horse Variants**: Use different coat colors for variety:
- Add `Variant:0` for white
- Add `Variant:1` for creamy
- Add `Variant:2` for chestnut
- Add `Variant:3` for brown
- Add `Variant:4` for black

### Key Features

- Tack room: `chest` with saddles, `item_frame` with horse armor
- Hay storage: Stack of `hay_block` (3-4 blocks tall)
- Grooming area: `cauldron` with water, `chest` with supplies
- Exterior hitching post: `oak_fence` with `lead` item

---

## Building 3: Garden Area

### Specifications

**Footprint**: 20 blocks (X) × 12 blocks (Z)
**Base Coordinates**: X=530, Y=-61, Z=-375 to X=550, Y=-61, Z=-363
**Height**: Ground level (Y=-61) with fencing Y=-61 to Y=-60

### Layout

**Garden Beds**:
- 4 garden beds, each 4×8 blocks
- Spacing: 2-block paths between beds
- Orientation: North-South rows

**Bed 1 (West)**: X=531-534, Z=-374 to Z=-366
- Crop: `wheat`
- Soil: `farmland` (tilled with water channel)

**Bed 2 (West-Center)**: X=537-540, Z=-374 to Z=-366
- Crop: `carrots`
- Soil: `farmland`

**Bed 3 (East-Center)**: X=543-546, Z=-374 to Z=-366
- Crop: `potatoes`
- Soil: `farmland`

**Bed 4 (East)**: X=549-552, Z=-374 to Z=-366
- Crop: `beetroot`
- Soil: `farmland`

**Irrigation**:
- Water channels: 1 block wide, running through center of each bed
- Water source: `water` blocks at intervals (every 8 blocks hydrates 4-block radius)

### Materials

**Fencing**:
- Perimeter: `oak_fence` (2 blocks tall for climbing protection)
- Gate: `oak_fence_gate` (South side, 2 blocks wide)
- Posts: `oak_fence` every 4 blocks

**Garden Elements**:
- Soil: `farmland` (tilled)
- Paths: `dirt_path` (2 blocks wide)
- Water: `water` source blocks
- Crops: `wheat`, `carrots`, `potatoes`, `beetroot` (fully grown for visual)

**Decorative**:
- Scarecrow: `oak_fence` with `carved_pumpkin` head, `leather_chestplate` on armor stand
- Compost area: `composter` (2-3 blocks)
- Tool storage: `chest` with hoe, seeds
- Flower border: `sunflower`, `poppy` along fence (North side)

---

## Ranch Elements

### Pathways

**Main Path** (South-North, connecting all):
- Width: 3 blocks
- Material: `dirt_path` with `cobblestone` edges
- Route: From player position (Z=-360) → Home → Garden → Stable
- Coordinates: X=540-542 (center line)

**Secondary Paths**:
- Home to Garden: 2 blocks wide, `dirt_path`
- Stable to Garden: 2 blocks wide, `dirt_path`

### Corral Fence

**Extension from Stable**:
- Area: 15×12 blocks (East of stable)
- Coordinates: X=574, Z=-395 to X=589, Z=-383
- Fencing: `oak_fence` (standard height)
- Gate: `oak_fence_gate` (South side, 3 blocks wide for horse passage)
- Interior: Grass blocks, scattered `hay_block`

### Water Trough

**Position**: Outside stable, near entrance
**Coordinates**: X=554, Y=-61, Z=-388
**Design**:
- Base: 3×2 `cobblestone` blocks
- Interior: `water` source blocks (fill)
- Edges: `cobblestone_slab` (top edge)

### Hay Storage

**Position**: North side of stable (exterior)
**Coordinates**: X=564, Y=-61, Z=-397
**Design**:
- Stack: 3×3×3 `hay_block` cube
- Cover: `oak_slab` roof (overhang)
- Access: Open on South side

### Hitching Posts

**Position**: Between home and stable (along main path)
**Coordinates**: X=547, Y=-61, Z=-390
**Design**:
- Posts: 2× `oak_fence` (3 blocks tall)
- Spacing: 4 blocks apart
- Top: `oak_fence` horizontal rail connecting posts
- Leads: `lead` item (decorative, use `/setblock` for lead_knot entity)

---

## Build Sequence & Phasing

### Phase 1: Site Preparation & Foundation (TICKET 1)
**Assigned to**: Shell Engineer
**Dependencies**: None

**Tasks**:
1. Terrain analysis and leveling (if needed)
2. Mark building footprints with temporary blocks
3. Clear vegetation/obstacles in build area
4. Lay main pathway (dirt_path) to mark circulation

**Coordinates for marking**:
- Home: X=530-544, Z=-395 to Z=-383
- Stable: X=555-573, Z=-395 to Z=-385
- Garden: X=530-550, Z=-375 to Z=-363

---

### Phase 2A: Main Ranch Home - Shell (TICKET 2)
**Assigned to**: Shell Engineer
**Dependencies**: Phase 1 complete

**Specifications**:
- Base coordinates: X=530, Y=-61, Z=-395 to X=544, Y=-61, Z=-383
- Floor placement: Y=-61 (flush with ground, `oak_planks`)
- Wall height: First floor Y=-61 to Y=-57 (5 blocks)
- Wall material: `oak_planks` (primary)
- Corner posts: `dark_oak_log` (MUST differ from walls, runs full height)
- Second floor: Y=-57 (floor slab `oak_planks`)
- Second floor walls: Y=-57 to Y=-53 (4 blocks)
- Ceiling: Y=-53 (`oak_planks`)

**WorldEdit Command Sequence**:
```
# First floor
//pos1 530,-61,-395
//pos2 544,-61,-383
//set oak_planks   # Floor at ground level

//pos1 530,-61,-395
//pos2 544,-57,-383
//walls oak_planks  # Exterior walls

# Corner posts (4 corners, full height Y=-61 to Y=-53)
//pos1 530,-61,-395
//pos2 530,-53,-395
//set dark_oak_log  # NW corner

//pos1 544,-61,-395
//pos2 544,-53,-395
//set dark_oak_log  # NE corner

//pos1 530,-61,-383
//pos2 530,-53,-383
//set dark_oak_log  # SW corner

//pos1 544,-61,-383
//pos2 544,-53,-383
//set dark_oak_log  # SE corner

# Second floor slab
//pos1 531,-57,-394
//pos2 543,-57,-384
//set oak_planks

# Second floor walls
//pos1 530,-57,-395
//pos2 544,-53,-383
//walls oak_planks

# Ceiling
//pos1 531,-53,-394
//pos2 543,-53,-384
//set oak_planks
```

**Success Criteria**:
- Floor flush with ground (Y=-61)
- Walls structurally complete (no gaps)
- Corner posts contrasting and visible
- Two distinct floors with ceiling separation
- Ready for window/door openings

---

### Phase 2B: Main Ranch Home - Facade (TICKET 3)
**Assigned to**: Facade Architect
**Dependencies**: Phase 2A complete

**Specifications**:
- Window count: 8 total (4 first floor, 4 second floor)
- Window size: 2×2 `glass_pane`
- Window frame: 1-block `spruce_planks` trim around glass
- Window spacing: 3 blocks apart (standard rhythm)
- Window height: First floor Y=-58, Second floor Y=-55
- Front door: Y=-60 to Y=-59, centered on South wall (Z=-383)
- Door material: `oak_door`
- Door surround: `spruce_planks` frame (1 block)

**Window Positions** (approximate, architect to refine):
- South wall (front): 2 windows first floor, 2 windows second floor
- North wall (back): 1 window first floor, 2 windows second floor
- East/West walls: 1 window each side first floor

**Window Frame Technique**:
1. Cut opening (2×2 for glass)
2. Expand opening by 1 block in all directions
3. Set outer ring to `spruce_planks` (frame)
4. Set inner 2×2 to `glass_pane`

**Additional Details**:
- Shutters: `oak_trapdoor[facing=east/west]` beside each window
- Foundation trim: `cobblestone` visible 1 block below first floor windows
- Porch overhang: 3 blocks deep on South side, `oak_fence` railing

**Success Criteria**:
- All windows have contrasting frames
- Window rhythm is consistent (3-block spacing)
- Door is centered and proportional
- Shutters attached to solid blocks (not floating)
- Foundation trim adds visual weight

---

### Phase 2C: Main Ranch Home - Roofing (TICKET 4)
**Assigned to**: Roofing Specialist
**Dependencies**: Phase 2B complete

**Specifications**:
- Roof type: Gable (East-West ridge)
- Base height: Y=-53 (on top of ceiling)
- Ridge height: Y=-49 (4 blocks rise)
- Material: `oak_stairs[facing=north/south,half=bottom]`
- Pitch: Steep 1:1 (1 block up, 1 block inward per layer)
- Overhang: 2 blocks past walls (extends to X=528-546, Z=-397 to Z=-381)
- Ridge: `oak_planks` full blocks (top center line)

**CRITICAL ROOF CONSTRUCTION**:
- MUST use `analyze_placement_area` before each layer to get proper offset
- Each layer steps UP (Y+1) and INWARD (Z±1 for N/S slopes)
- NEVER stack stairs vertically at same X,Z position

**Layer-by-Layer Build**:

**Layer 1** (Base, Y=-53):
```
# North slope (facing north)
//pos1 528,-53,-397
//pos2 546,-53,-397
//set oak_stairs[facing=north,half=bottom]

# South slope (facing south)
//pos1 528,-53,-381
//pos2 546,-53,-381
//set oak_stairs[facing=south,half=bottom]
```

**Layer 2** (Y=-52, MUST offset inward):
```
# FIRST: analyze_placement_area(center_x=537, center_y=-53, center_z=-389, radius=8, analysis_type="roof_context")
# THEN: Apply offset from analysis (should be Z+1 for north, Z-1 for south)

# North slope (stepped inward to Z=-396)
//pos1 528,-52,-396
//pos2 546,-52,-396
//set oak_stairs[facing=north,half=bottom]

# South slope (stepped inward to Z=-382)
//pos1 528,-52,-382
//pos2 546,-52,-382
//set oak_stairs[facing=south,half=bottom]
```

**Continue layers 3-4 with same offset pattern until ridge**

**Ridge** (Y=-49, center):
```
//pos1 528,-49,-389
//pos2 546,-49,-389
//set oak_planks  # Full blocks at peak
```

**Overhang Extension**:
- Extend stairs 2 blocks past walls on all sides
- Gable ends (East/West): Fill with `oak_planks` in triangular pattern

**Success Criteria**:
- Roof slopes evenly from both sides to ridge
- No vertical stair stacking (each layer offset horizontally)
- 2-block overhang creates shadow line
- Ridge is straight and centered
- Gable ends are filled (no gaps)

---

### Phase 2D: Main Ranch Home - Interior (TICKET 5)
**Assigned to**: Interior Designer
**Dependencies**: Phase 2C complete (roof for lighting context)

**Specifications**:

**First Floor Interior Walls**:
- Kitchen partition: X=537, Z=-394 to Z=-386 (Y=-61 to Y=-56, `spruce_planks`)
- Entryway partition: X=537, Z=-386 to Z=-383 (Y=-61 to Y=-56, `spruce_planks`)
- Staircase enclosure: X=537-539, Z=-389 to Z=-386 (Y=-61 to Y=-56, `oak_fence` open sides)

**Second Floor Interior Walls**:
- Bedroom divider: X=537, Z=-390 to Z=-383 (Y=-57 to Y=-52, `spruce_planks`)
- Hallway: 3 blocks wide, center (X=537-539)

**Furniture Placement**:

CRITICAL: Use `analyze_placement_area` BEFORE placing each furniture item to find exact floor_y/ceiling_y

**Living Room** (First Floor, NW):
- Fireplace: X=531, Z=-393, cobblestone 3×3 (Y=-61 to Y=-59)
- Sofa: X=535-536, Z=-390 (2 `oak_stairs[facing=south]`)
- Coffee table: X=535, Z=-388 (`oak_fence` + `oak_pressure_plate`)
- Bookshelf: X=533-534, Z=-394 (against North wall)
- Rug: `cyan_carpet` 4×4 centered

**Kitchen** (First Floor, NE):
- Counter: L-shape, X=541-543, Z=-394 to Z=-390 (`oak_slab` on `stone`)
- Furnace: X=541, Z=-394 (built into counter)
- Crafting table: X=542, Z=-394
- Chest: X=543, Z=-394 (double chest)
- Sink: `cauldron` with water at X=542, Z=-390

**Master Bedroom** (Second Floor, North):
- Bed: X=541, Z=-393 to Z=-392 (`red_bed`)
- Chest: X=543, Z=-391 (clothing storage)
- Window seat: X=534, Z=-394 (`oak_stairs`)
- Rug: `white_carpet` 4×3

**Second Bedroom** (Second Floor, South):
- Bed: X=541, Z=-385 to Z=-384 (`blue_bed`)
- Chest: X=543, Z=-386
- Desk: X=534, Z=-384 (`oak_fence` + `oak_slab`)

**Staircase**:
- Type: Straight staircase, South to North
- Position: X=537-539, Z=-386 to Z=-390
- Material: `oak_stairs[facing=north]` ascending
- Start: Y=-61 (first floor)
- End: Y=-57 (second floor landing)
- Headroom: 3 blocks above each step

**Lighting**:

MUST verify with `analyze_lighting` after placement:

**First Floor**:
- Living room: 2× `torch` on walls (X=532, Z=-391 and X=540, Z=-391)
- Kitchen: `glowstone` inset in ceiling at X=542, Z=-391 (Y=-56)
- Entryway: `lantern` on chain from ceiling at X=537, Z=-384

**Second Floor**:
- Master bedroom: 1× `lantern` hanging from ceiling (Y=-52)
- Second bedroom: 1× `torch` on wall
- Hallway: 1× `lantern` on chain

**Success Criteria**:
- All furniture placed ON floors (not in floors or floating) using analyze_placement_area
- Lighting verified with analyze_lighting (no dark spots <8 light level)
- Interior walls divide spaces clearly
- Staircase has proper headroom (3 blocks above steps)
- Rooms feel furnished and livable

---

### Phase 3A: Horse Stable - Shell (TICKET 6)
**Assigned to**: Shell Engineer
**Dependencies**: Phase 1 complete

**Specifications**:
- Base coordinates: X=555, Y=-61, Z=-395 to X=573, Y=-61, Z=-385
- Floor: Y=-61 (flush with ground, `oak_planks`)
- Walls: Y=-61 to Y=-57 (6 blocks tall)
- Wall material: `spruce_planks` (primary)
- Corner posts: `stripped_spruce_log` (4×4 posts at corners, accent)
- Ceiling: Y=-57 (`spruce_planks`)

**WorldEdit Command Sequence**:
```
# Floor
//pos1 555,-61,-395
//pos2 573,-61,-385
//set oak_planks

# Walls
//pos1 555,-61,-395
//pos2 573,-57,-385
//walls spruce_planks

# Corner posts (4×4 each)
# NW corner
//pos1 555,-61,-395
//pos2 556,-57,-394
//set stripped_spruce_log

# NE corner
//pos1 571,-61,-395
//pos2 572,-57,-394
//set stripped_spruce_log

# SW corner
//pos1 555,-61,-386
//pos2 556,-57,-385
//set stripped_spruce_log

# SE corner
//pos1 571,-61,-386
//pos2 572,-57,-385
//set stripped_spruce_log

# Ceiling
//pos1 556,-57,-394
//pos2 571,-57,-386
//set spruce_planks
```

**Interior Stall Dividers**:
- Material: `oak_fence` (1 block thick)
- Stall 1-2 divider: X=564, Z=-394 to Z=-388 (Y=-61 to Y=-59)
- Stall 3-4 divider: X=567, Z=-394 to Z=-388 (Y=-61 to Y=-59)
- Center aisle: X=565-566 (3 blocks wide, clear)

**Success Criteria**:
- Floor flush with ground
- Walls 6 blocks tall (barn-style high ceiling)
- Corner posts contrasting and substantial (4×4)
- Stall dividers in place
- Ready for doors and windows

---

### Phase 3B: Horse Stable - Facade & Doors (TICKET 7)
**Assigned to**: Facade Architect
**Dependencies**: Phase 3A complete

**Specifications**:

**Main Entrance** (West wall, facing ranch home):
- Position: X=555, Z=-390 to Z=-389 (centered)
- Size: 2 blocks wide × 3 blocks tall (barn door style)
- Material: `oak_door` (2 adjacent doors for double-wide)
- Surround: `stripped_spruce_log` frame (1 block)

**Stall Gates** (Interior):
- Stall 1: X=558, Z=-393 (`oak_fence_gate`)
- Stall 2: X=558, Z=-388 (`oak_fence_gate`)
- Stall 3: X=569, Z=-393 (`oak_fence_gate`)
- Stall 4: X=569, Z=-388 (`oak_fence_gate`)

**Windows** (High placement for ventilation):
- North wall: 2× windows, 1×2 `glass_pane` with `oak_fence` bars
  - Position: X=561, Z=-395 and X=570, Z=-395 (Y=-55)
- South wall: 2× windows, same style
  - Position: X=561, Z=-385 and X=570, Z=-385 (Y=-55)

**Ventilation Gaps** (Near roof):
- Leave 1-block gaps at Y=-58 (just below ceiling) on East/West gable ends
- No glass, allows airflow

**Success Criteria**:
- Main entrance is wide enough for horse passage (2 blocks)
- Stall gates functional (fence gates open/close)
- Windows provide light but are high (don't interfere with stalls)
- Ventilation gaps present

---

### Phase 3C: Horse Stable - Roofing (TICKET 8)
**Assigned to**: Roofing Specialist
**Dependencies**: Phase 3B complete

**Specifications**:
- Roof type: Gable (North-South ridge)
- Base height: Y=-57 (on ceiling)
- Ridge height: Y=-53 (4 blocks rise)
- Material: `spruce_stairs[facing=east/west,half=bottom]`
- Pitch: Moderate 1:1
- Overhang: 1 block past walls
- Ridge: `spruce_planks` full blocks

**Layer-by-Layer Build** (Use analyze_placement_area before each layer):

**Layer 1** (Y=-57):
```
# East slope
//pos1 554,-57,-395
//pos2 554,-57,-385
//set spruce_stairs[facing=east,half=bottom]

# West slope
//pos1 574,-57,-395
//pos2 574,-57,-385
//set spruce_stairs[facing=west,half=bottom]
```

**Layers 2-4**: Offset inward (X±1 per layer) until ridge at X=564 (center)

**Ridge** (Y=-53):
```
//pos1 564,-53,-395
//pos2 564,-53,-385
//set spruce_planks
```

**Gable Ends** (North/South):
- Fill triangular areas with `spruce_planks`

**Success Criteria**:
- Roof symmetrical, meets at center ridge
- No vertical stacking (proper offset)
- 1-block overhang on East/West sides
- Gable ends closed

---

### Phase 3D: Horse Stable - Interior & Horses (TICKET 9)
**Assigned to**: Interior Designer + Redstone Engineer (for horse spawning)
**Dependencies**: Phase 3C complete

**Stall Furnishings** (Each of 4 stalls):

**Stall 1** (X=557-560, Z=-393 to Z=-390):
- Bedding: `hay_block` on floor (scattered 3-4 blocks)
- Water trough: `cauldron` filled with water at X=559, Z=-393
- Fence gate: X=558, Z=-393 (already placed in Phase 3B)

**Stall 2** (X=557-560, Z=-388 to Z=-385):
- Same configuration, mirrored

**Stall 3** (X=567-570, Z=-393 to Z=-390):
- Same configuration, mirrored

**Stall 4** (X=567-570, Z=-388 to Z=-385):
- Same configuration, mirrored

**Tack Room** (North end, X=557-560, Z=-395 to Z=-394):
- Chest: 2× `chest` at X=558-559, Z=-395 (saddles, horse armor, leads)
- Item frames: 3× `item_frame` on wall with saddle, iron horse armor, lead
- Shelf: `oak_slab` at Y=-58 along North wall

**Hay Storage** (South end, X=567-570, Z=-386 to Z=-385):
- Hay stack: `hay_block` stacked 3×3×3 cube at X=568, Z=-385

**Central Aisle**:
- Grooming area: `cauldron` with water at X=565, Z=-390
- Lantern posts: 2× `oak_fence` with `lantern` on top at X=565, Z=-392 and X=565, Z=-388

**Lighting**:
- Stall lights: 1× `lantern` hanging from ceiling per stall (Y=-56)
- Aisle lights: 2× `torch` on posts at Y=-59
- Entrance: 1× `lantern` on chain outside main door

**CRITICAL: Spawn Live Horses**:

After all furnishings complete, use `rcon_command` to spawn horses:

**Stall 1** (White horse):
```
/summon minecraft:horse 558 -60 -391 {Tame:1b,Variant:0,SaddleItem:{id:"minecraft:saddle",Count:1b}}
```

**Stall 2** (Chestnut horse):
```
/summon minecraft:horse 558 -60 -386 {Tame:1b,Variant:2,SaddleItem:{id:"minecraft:saddle",Count:1b}}
```

**Stall 3** (Brown horse):
```
/summon minecraft:horse 569 -60 -391 {Tame:1b,Variant:3,SaddleItem:{id:"minecraft:saddle",Count:1b}}
```

**Stall 4** (Black horse):
```
/summon minecraft:horse 569 -60 -386 {Tame:1b,Variant:4,SaddleItem:{id:"minecraft:saddle",Count:1b}}
```

**Success Criteria**:
- All 4 stalls have bedding, water, and gates
- Tack room stocked with equipment
- Hay storage visible and accessible
- Lighting adequate (no dark spots)
- **4 LIVE HORSES spawned in stalls** (CRITICAL REQUIREMENT)

---

### Phase 4: Garden Area (TICKET 10)
**Assigned to**: Landscape Artist
**Dependencies**: Phase 1 complete

**Specifications**:
- Base coordinates: X=530, Y=-61, Z=-375 to X=550, Y=-61, Z=-363
- Fencing: `oak_fence` perimeter, 2 blocks tall (Y=-61 to Y=-60)
- Gate: `oak_fence_gate` at X=540, Z=-363 (South side, 2 blocks wide)

**Garden Bed Construction**:

For each bed:
1. Till soil: `farmland` blocks
2. Dig irrigation channel (center line, 1 block wide)
3. Place water source blocks in channel (every 8 blocks)
4. Plant crops (fully grown for visual appeal)

**Bed 1** (X=531-534, Z=-374 to Z=-366):
```
# Till soil
//pos1 531,-61,-374
//pos2 534,-61,-366
//replace dirt farmland

# Water channel (center, Z=-370)
//pos1 531,-61,-370
//pos2 534,-61,-370
//set water

# Plant wheat
//pos1 531,-60,-374
//pos2 534,-60,-366
//replace air wheat[age=7]
```

**Bed 2** (X=537-540, Z=-374 to Z=-366):
- Same process, plant `carrots[age=7]`

**Bed 3** (X=543-546, Z=-374 to Z=-366):
- Same process, plant `potatoes[age=7]`

**Bed 4** (X=549-552, Z=-374 to Z=-366):
- Same process, plant `beetroots[age=3]` (fully grown)

**Paths**:
- Material: `dirt_path`
- Main path: 2 blocks wide, X=535-536, Z=-375 to Z=-363 (North-South center)
- Cross path: 2 blocks wide, Z=-370, X=530 to X=550 (East-West)

**Decorative Elements**:

**Scarecrow** (X=540, Z=-370):
- Base: 2× `oak_fence` vertical (Y=-61 to Y=-59)
- Arms: `oak_fence` horizontal at Y=-59
- Head: `carved_pumpkin` on top at Y=-58
- Body: Armor stand with `leather_chestplate` at Y=-60

**Compost Area** (X=532, Z=-364):
- 2× `composter` blocks
- 1× `chest` with bone meal, seeds

**Tool Storage** (X=548, Z=-364):
- 1× `barrel` (vertical, facing up)
- Item frames with hoe, seeds on nearby fence

**Flower Border** (North edge):
- `sunflower` every 3 blocks along Z=-375 (X=531 to X=549)
- `poppy` scattered between sunflowers

**Success Criteria**:
- All 4 beds tilled, watered, and planted
- Crops fully grown (age=7 or age=3)
- Fencing complete with functional gate
- Paths provide access to all beds
- Decorative elements add charm
- Garden looks productive and well-maintained

---

### Phase 5: Ranch Elements (TICKET 11)
**Assigned to**: Landscape Artist
**Dependencies**: All buildings complete (Phase 2-4)

**Main Pathway**:
- Route: Z=-360 (player start) → Home (Z=-389) → Garden (Z=-370) → Stable (Z=-390)
- Width: 3 blocks (X=540-542)
- Material: Center `dirt_path` (X=541), edges `cobblestone` (X=540, X=542)
- Length: Approximately 50 blocks (Z=-360 to Z=-395)

**Secondary Paths**:

**Home to Garden** (East-West):
- Width: 2 blocks
- Route: X=544 (home East side) to X=530 (garden West gate)
- Material: `dirt_path`
- Coordinates: Z=-378, X=530 to X=544

**Stable to Garden** (Southwest diagonal):
- Width: 2 blocks
- Route: X=555 (stable West) to X=550 (garden East gate)
- Material: `dirt_path`
- Approximate path: Curve from (X=555, Z=-390) to (X=550, Z=-370)

**Corral Fence** (East of stable):

**Area**: X=574 to X=589, Z=-395 to Z=-383 (15×12 blocks)

**Fencing**:
```
# North side
//pos1 574,-61,-395
//pos2 589,-61,-395
//set oak_fence

# South side
//pos1 574,-61,-383
//pos2 589,-61,-383
//set oak_fence

# East side
//pos1 589,-61,-395
//pos2 589,-61,-383
//set oak_fence

# West side (connects to stable)
//pos1 574,-61,-395
//pos2 574,-61,-383
//set oak_fence
```

**Gate**: 3 blocks wide at X=580-582, Z=-383 (South side)
```
//pos1 580,-61,-383
//pos2 582,-61,-383
//replace oak_fence oak_fence_gate
```

**Interior**: Grass blocks with scattered `hay_block` (3-4 blocks total)

**Water Trough** (Outside stable entrance):

**Position**: X=554, Y=-61, Z=-388
**Design**:
```
# Base
//pos1 553,-61,-389
//pos2 555,-61,-388
//set cobblestone

# Hollow interior
//pos1 554,-61,-389
//pos2 554,-61,-388
//set water

# Top edge
//pos1 553,-60,-389
//pos2 555,-60,-388
//set cobblestone_slab[type=top]
```

**Hay Storage** (North exterior of stable):

**Position**: X=564, Y=-61, Z=-397
**Stack**:
```
# Hay cube
//pos1 563,-61,-398
//pos2 565,-61,-396
//set hay_block

//pos1 563,-60,-398
//pos2 565,-60,-396
//set hay_block

//pos1 563,-59,-398
//pos2 565,-59,-396
//set hay_block

# Roof overhang
//pos1 562,-59,-399
//pos2 566,-59,-395
//set oak_slab[type=top]
```

**Hitching Posts** (Along main path, between home and stable):

**Position**: X=547, Y=-61, Z=-390
**Design**:
```
# Post 1
//pos1 546,-61,-390
//pos2 546,-59,-390
//set oak_fence

# Post 2 (4 blocks East)
//pos1 550,-61,-390
//pos2 550,-59,-390
//set oak_fence

# Horizontal rail connecting tops
//pos1 547,-59,-390
//pos2 549,-59,-390
//set oak_fence
```

**Lead decoration** (optional):
- Use `/setblock` for `lead_knot` entities on posts if desired for visual

**Additional Ranch Touches**:
- Lantern lighting: Place `lantern` on chains at key path intersections (every 12 blocks)
- Barrel storage: 2× `barrel` near stable for feed/tools
- Bench: `oak_stairs` facing each other near hitching posts (rest area)

**Success Criteria**:
- All paths connect buildings logically
- Corral provides exercise area for horses (can lead horses out)
- Water trough functional and visible
- Hay storage covered and accessible
- Hitching posts sturdy and decorative
- Compound feels cohesive with circulation and ranch elements

---

### Phase 6: Quality Assurance (TICKET 12)
**Assigned to**: Quality Auditor
**Dependencies**: All phases complete

**Validation Checks**:

**1. Symmetry Check** (Main Home):
```
check_symmetry(
  x1=530, y1=-61, z1=-395,
  x2=544, y2=-49, z2=-383,
  axis="x",  # Check East-West symmetry of gable roof
  tolerance=0
)
```

**2. Structure Validation** (All buildings):
```
# Home
validate_structure(
  x1=530, y1=-61, z1=-395,
  x2=544, y2=-49, z2=-383,
  resolution=1
)

# Stable
validate_structure(
  x1=555, y1=-61, z1=-395,
  x2=573, y2=-53, z2=-385,
  resolution=1
)
```

**3. Lighting Analysis**:
```
# Home interior
analyze_lighting(
  x1=531, y1=-61, z1=-394,
  x2=543, y2=-53, z2=-384,
  resolution=2
)

# Stable interior
analyze_lighting(
  x1=556, y1=-61, z1=-394,
  x2=571, y2=-57, z2=-386,
  resolution=2
)
```

**4. Manual Verification**:
- [ ] 4 live horses present in stable stalls (CRITICAL)
- [ ] All corner posts contrast with walls (dark_oak_log vs oak_planks)
- [ ] All windows have frames (spruce_planks trim)
- [ ] All lights attached to blocks (no floating lanterns/torches)
- [ ] Roofs have proper overhangs (1-2 blocks)
- [ ] Roof stairs not stacked vertically (properly offset)
- [ ] Garden crops fully grown and watered
- [ ] All gates functional (can open/close)
- [ ] Paths connect all buildings
- [ ] Materials consistent with rustic_cottage palette

**5. User Acceptance**:
- Walk through entire compound
- Check sightlines between buildings
- Verify ranch aesthetic cohesion
- Test circulation (can navigate all areas comfortably)
- Confirm all user requirements met:
  - ✅ Main ranch home (residential)
  - ✅ Horse stable (functional with LIVE horses)
  - ✅ Garden area (planted and fenced)
  - ✅ Ranch elements (paths, corral, water trough, hay, hitching posts)

**Success Criteria**:
- All validation checks pass with no critical issues
- 4 live horses verified in stable
- Symmetry within tolerance
- No floating blocks or physics violations
- No dark spots (light level ≥8 everywhere)
- User confirms satisfaction with compound

---

## Coordination Notes

### Checkpoint Reviews

**After Phase 2 (Main Home Complete)**:
- Review home structure, facade, roof, interior
- Verify materials palette consistency
- Check scale and proportions
- Adjust stable/garden if needed based on home success

**After Phase 3 (Stable Complete)**:
- Verify horses spawned correctly (CRITICAL)
- Check stable functionality
- Ensure visual cohesion with home
- Adjust garden scale if needed

**After Phase 5 (All Elements Complete)**:
- Full compound walkthrough
- Check circulation and sightlines
- Verify ranch aesthetic throughout
- Final user approval before QA

### Communication Between Specialists

**Shell Engineer → Facade Architect**:
- Exact wall coordinates for window/door placement
- Corner post positions (avoid cutting into posts with openings)
- Structural integrity notes

**Facade Architect → Roofing Specialist**:
- Final wall top height (roof base)
- Gable end dimensions
- Overhang clearance for windows

**Roofing Specialist → Interior Designer**:
- Ceiling height confirmation
- Light fixture attachment points (beams, ceiling blocks)
- Roof slope angles (affects upper floor spaces)

**Interior Designer → Quality Auditor**:
- Furniture placement coordinates (for validation)
- Lighting placement map (for analyze_lighting)
- Any custom modifications to note

**Landscape Artist → All**:
- Path routing (avoid conflicts with building footprints)
- Grade changes (if terrain leveling needed)
- Exterior decorative elements that attach to buildings

---

## Material Quantities (Estimated)

**Wood**:
- `oak_planks`: ~3,500 blocks (floors, walls, roofs)
- `spruce_planks`: ~2,000 blocks (stable, trim)
- `oak_stairs`: ~800 blocks (roofs, furniture)
- `spruce_stairs`: ~600 blocks (stable roof)
- `dark_oak_log`: ~200 blocks (corner posts)
- `stripped_spruce_log`: ~150 blocks (stable posts)
- `oak_fence`: ~400 blocks (garden, corral, furniture)
- `oak_fence_gate`: ~10 blocks (gates)
- `oak_slab`: ~300 blocks (details, roof)

**Stone**:
- `cobblestone`: ~800 blocks (foundation, chimney, paths, trough)
- `stone`: ~200 blocks (counters, details)

**Functional**:
- `glass_pane`: ~80 blocks (windows)
- `oak_door`: ~6 blocks (doors)
- `torch`: ~40 blocks (lighting)
- `lantern`: ~15 blocks (lighting)
- `chest`: ~8 blocks (storage)
- `cauldron`: ~6 blocks (water, sinks)
- `hay_block`: ~50 blocks (stables, storage, corral)

**Garden**:
- `farmland`: ~120 blocks (tilled soil)
- `dirt_path`: ~200 blocks (pathways)
- `wheat`: ~30 blocks (crops)
- `carrots`: ~30 blocks (crops)
- `potatoes`: ~30 blocks (crops)
- `beetroots`: ~30 blocks (crops)
- `water`: ~30 blocks (irrigation)
- `sunflower`: ~10 blocks (decoration)
- `poppy`: ~10 blocks (decoration)

**Furniture/Decorative**:
- `carpet`: ~50 blocks (rugs)
- `bed`: ~3 blocks (bedrooms)
- `crafting_table`, `furnace`, `composter`, `barrel`: ~10 blocks total
- `carved_pumpkin`: ~1 block (scarecrow)
- `item_frame`: ~10 blocks (displays)

**Horses**: 4 entities (summoned via command)

**Total Estimated Blocks**: ~10,000 blocks

---

## Final Notes

**Critical Success Factors**:
1. **Live Horses** - Must spawn 4 horses in stable (CRITICAL USER REQUIREMENT)
2. **Spatial Awareness** - Use analyze_placement_area before furniture/roof layers
3. **Material Contrast** - Corner posts MUST differ from walls (dark_oak_log vs oak_planks)
4. **Roof Construction** - No vertical stair stacking (offset each layer)
5. **Floor Placement** - Buildings flush with ground (floor at Y=-61, NOT Y=-60)
6. **Cohesive Aesthetic** - Rustic cottage palette throughout (oak/spruce/cobblestone)

**User Expectations**:
- Compound should feel like a working ranch (functional, practical)
- Buildings related through materials, scale, and circulation
- Live horses are centerpiece of stable
- Garden is productive and well-tended
- Ranch elements (paths, corral, hay, water) complete the scene

**Build Duration Estimate**:
- Phase 1 (Prep): 15 minutes
- Phase 2 (Home): 45 minutes
- Phase 3 (Stable): 40 minutes
- Phase 4 (Garden): 20 minutes
- Phase 5 (Elements): 25 minutes
- Phase 6 (QA): 15 minutes
- **Total**: ~2.5-3 hours (for detailed execution)

**Handoff to Executor**:
This plan is complete and ready for execution. Each ticket contains:
- Precise coordinates
- Material specifications
- WorldEdit command sequences
- Success criteria
- Dependencies

Executor should follow phases sequentially, use checkpoints for course correction, and communicate any deviations or issues back to Master Planner for adjustment.

---

**BUILD PLAN APPROVED - READY FOR EXECUTION**
