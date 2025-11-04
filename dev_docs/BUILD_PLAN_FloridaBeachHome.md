# BUILD PLAN: Florida Beach-Style Home

## Project Overview
**Style**: Florida beach home architecture - coastal, airy, light-filled
**Location**: X=246, Z=-36, Y=64 (ground level foundation)
**Orientation**: Front faces South (player facing ~177°)
**Size**: Modest, realistic Minecraft home - 14x18 block footprint
**Total Height**: 9 blocks (foundation to roof peak)

## Design Philosophy
Florida beach homes emphasize:
- **Light & Airy**: Large windows, white/cream palette, natural light
- **Indoor/Outdoor Living**: Covered porch (lanai), open floor plan
- **Coastal Materials**: White concrete, birch wood, light blues, sandy tones
- **Low-Pitch Roof**: Hip roof typical of Florida architecture (hurricane resistance)
- **Elevated Foundation**: 1-block raised foundation (coastal flooding adaptation)

## Footprint & Coordinates
**Base Coordinates**: 246,64,-36 (Southwest corner)
**Dimensions**: 14 blocks (East-West) x 18 blocks (North-South)
**Full extent**: X 246→260, Y 64→73, Z -36→-18

### Orientation (Front faces South where player is looking)
- **South side** (Z=-36): Main entrance, covered porch, primary facade
- **North side** (Z=-18): Rear, kitchen access, utility
- **East side** (X=260): Bedroom windows
- **West side** (X=246): Living room windows

## Floor Plan (14x18 blocks)

```
North (Z=-18) ←

   ┌─────────────────────┐
   │    Kitchen/Dining   │  6x8 blocks
   │      (North)        │
   ├──────────┬──────────┤
   │  Bedroom │ Living   │  Bedroom: 6x5
   │   East   │  Room    │  Living: 8x5
   │   6x5    │  8x5     │
   └──────────┴──────────┘
   └───────────────────┘
      Covered Porch 14x3

→ South (Z=-36) MAIN ENTRANCE
  (Player facing direction)
```

### Room Breakdown (following minecraft_scale_reference.txt)
1. **Covered Porch/Lanai** (Z=-36 to -33): 14x3 blocks, 3-block ceiling height
2. **Living Room** (West side): 8x5 blocks, 4-block ceiling (airy, tall)
3. **Bedroom** (East side): 6x5 blocks, 3-block ceiling (comfortable)
4. **Kitchen/Dining** (North end): 6x8 blocks, 3-block ceiling (open to living)
5. **Circulation**: 2-block wide internal passages

## Materials Palette (Minecraft 1.21.3)

### Primary Structure
- **Foundation**: `smooth_sandstone` (sandy, coastal tone)
- **Main Walls**: `white_concrete` (clean, modern Florida look)
- **Accent Walls**: `birch_planks` (warm wood accents)
- **Roof**: `birch_stairs` + `birch_slab` (light wood, low pitch)

### Windows & Doors
- **Windows**: `white_stained_glass_pane` (large coastal windows)
- **Main Door**: `birch_door` (light wood entrance)
- **Window Frames**: `birch_planks` (trim detail)

### Interior
- **Flooring**: `birch_planks` (warm hardwood throughout)
- **Ceiling**: `white_concrete` (continues exterior, reflects light)
- **Interior Walls**: `white_concrete` (open, bright)

### Accents & Details
- **Porch Posts**: `birch_fence` (light wood columns)
- **Railings**: `birch_fence` (porch perimeter)
- **Lighting**: `sea_lantern` (coastal theme) + `lantern` (hanging fixtures)
- **Furniture Base**: `birch_stairs`, `white_carpet`, `light_blue_carpet`

### Landscape
- **Pathways**: `sandstone` and `sand`
- **Beach Grass**: `tall_grass`, `fern`
- **Tropical**: `jungle_sapling` (palm-like trees)
- **Ground Cover**: `sand` blending into natural terrain

## Build Sequence (6 Phases + QA)

### Phase 1: Foundation & Shell Structure
**Assigned to**: Shell Engineer
**Dependencies**: None (first phase)

**Specifications**:
- Foundation slab at Y=64: smooth_sandstone (14x18)
- Exterior walls Y=65-68: white_concrete (4 blocks tall)
- Interior floor Y=65: birch_planks (inside walls only)
- Wall openings marked (doors, large window positions)
- Load-bearing structure: exterior walls are 1 block thick

**Key Coordinates**:
- Southwest corner: 246,64,-36
- Northeast corner: 260,64,-18
- Wall height: Y=65 to Y=68 (4 blocks)

**Room Divisions**:
- Living/Bedroom divider wall: X=253 (North-South wall)
- Kitchen partition: Z=-26 (East-West wall with 2-block opening)

---

### Phase 2: Exterior Facade & Windows
**Assigned to**: Facade Architect
**Dependencies**: Phase 1 complete (shell structure exists)

**Specifications**:
- **South Facade** (Front, Z=-36):
  - Main entrance: 1x2 birch_door at center (X=253, Y=65-66)
  - No windows on porch wall (porch provides coverage)
  - Birch_planks accent trim around door

- **East Wall** (Bedroom side, X=260):
  - Two 2x2 windows with white_stained_glass_pane
  - Window positions: Y=66-67 (eye level)
  - Spacing: 3 blocks apart (standard rhythm)
  - Birch_planks frames (1 block border)

- **West Wall** (Living room, X=246):
  - Two 3x2 windows (wide, coastal style)
  - Window positions: Y=66-67
  - Birch_planks frames

- **North Wall** (Kitchen, Z=-18):
  - One 2x2 window above counters
  - Position: Y=66-67, centered
  - Birch_planks frame

- **Porch Construction** (Z=-36 to -33):
  - Roof support posts: birch_fence at corners and midpoints
  - Floor: birch_planks (continuous from interior)
  - Railings: birch_fence (1 block height) on South, East, West edges
  - Ceiling: white_concrete at Y=68

**Color Gradient**: Clean white_concrete with birch_planks accents (10% coverage)

---

### Phase 3: Roofing
**Assigned to**: Roofing Specialist
**Dependencies**: Phase 2 complete (facade finished)

**Roof Type**: Hip roof (all four sides slope) - classic Florida style
**Pitch**: Shallow (3:12 rise/run = gentle slope)
**Materials**: birch_stairs (slopes) + birch_slab (edges)

**Specifications**:
- Roof base level: Y=69 (top of walls)
- Hip roof slopes inward from all four sides
- Peak height: Y=73 (4 blocks above wall top = 9 total height)
- Overhang: 1 block on all sides (creates shadow line)
- Ridge runs East-West at center (Z=-27)

**Construction Notes**:
- Use birch_stairs facing inward for slopes
- Corners create hip lines (diagonal slopes)
- birch_slab for edge details and ridge caps
- No skylights (traditional Florida design)

**Coordinates**:
- Roof extends: X 245→261, Z -37→-17 (1 block overhang)
- Peak ridge: Z=-27, Y=73

---

### Phase 4: Interior Design
**Assigned to**: Interior Designer
**Dependencies**: Phase 3 complete (roof protects interior work)

**Specifications**:

**Living Room** (West section, 8x5 blocks):
- Floor: birch_planks (already placed in Phase 1)
- Ceiling height: 4 blocks (Y=65 to Y=68, airy feel)
- Furniture:
  - L-shaped sofa: 3 birch_stairs (West wall) + 2 birch_stairs (South wall)
  - Coffee table: 2 birch_fence + white_carpet (center)
  - Lighting: 2 sea_lantern embedded in ceiling (Y=68)
- Decor: White_carpet area rug (4x3), light_blue_carpet accents

**Bedroom** (East section, 6x5 blocks):
- Floor: birch_planks
- Ceiling height: 3 blocks (Y=65 to Y=67, comfortable)
- Furniture:
  - Bed: white_bed or light_blue_bed (East wall, 2 blocks long)
  - Side table: birch_fence + birch_slab (1 block clearance)
  - Storage: double chest (North wall)
  - Lighting: 1 lantern hanging from ceiling
- Decor: Light_blue_carpet beside bed

**Kitchen/Dining** (North section, 6x8 blocks):
- Floor: birch_planks
- Ceiling height: 3 blocks (Y=65 to Y=67)
- Kitchen area (West half):
  - Counters: birch_slab on stone blocks (L-shape, 3-block runs)
  - Furnace + crafting table built into counters
  - Double chest storage
  - Lighting: 2 lanterns above work area
- Dining area (East half):
  - Table: 3 birch_fence + birch_pressure_plate (3x2 table)
  - Chairs: 4 birch_stairs facing table
  - Lighting: 1 sea_lantern centered above table

**Covered Porch** (South, 14x3 blocks):
- Floor: birch_planks (continuous flow)
- Ceiling: white_concrete at Y=68 (covered)
- Furniture:
  - 2 birch_stairs (seating facing outward)
  - Decorative plants in pots (1-2 jungle_sapling in flower_pot)
- Lighting: 2 lanterns hanging from ceiling (Y=68)

**Lighting Strategy** (spawn-safe, every 8 blocks):
- Living room: 2 sea_lantern (ceiling-mounted)
- Bedroom: 1 lantern (hanging)
- Kitchen: 2 lanterns (task lighting)
- Dining: 1 sea_lantern (centerpiece)
- Porch: 2 lanterns (ambient)
- Total: 8 light sources across 252 m² = well-lit

**Circulation**:
- 2-block wide passage from porch → living room (double door or wide opening)
- Open connection living room → kitchen (no door, 3-block opening)
- Bedroom door: 1x2 birch_door from living room

---

### Phase 5: Landscape & Coastal Integration
**Assigned to**: Landscape Artist
**Dependencies**: Phase 4 complete (building finished)

**Specifications**:

**Immediate Perimeter** (5-block radius):
- **South (Front)**:
  - Pathway: 3-block wide sandstone path from porch to beach
  - Length: 8 blocks South (Z=-36 to -44)
  - Edges: sand borders (1 block wide)
  - Beach grass: tall_grass scattered (5-7 placements)

- **East & West Sides**:
  - Ground cover: sand and sandstone mix (natural transition)
  - Beach vegetation: tall_grass, fern (sparse, windswept look)
  - 2-3 jungle_sapling (palm-like trees, 8 blocks from house)

- **North (Rear)**:
  - Utility area: sandstone patio (4x4)
  - Beach grass: tall_grass clusters
  - Compost/storage area (barrel, chest)

**Extended Landscape** (10-block radius):
- Terrain grading: Gentle slope toward beach (if needed)
- Palm grove: 3-4 jungle_sapling (East side, 10-15 blocks away)
- Beach grass patches: tall_grass, fern (scattered naturally)
- Sand dunes: Small sand mounds (1-2 blocks high) with grass

**Coastal Elements**:
- Seashell decor: white_concrete or bone_block (small accents)
- Driftwood: stripped_birch_log (horizontal placement, 1-2 pieces)
- Beach path lighting: 4 lanterns on birch_fence posts (pathway edges)

**Biome Blending**:
- Transition natural terrain to sandy beach aesthetic
- Preserve existing features where possible
- Add sand gradually (don't cover everything)

**Coordinates**:
- Landscaping zone: X 236→270, Z -46→-8 (30x38 area)
- Primary focus: 10-block radius from house center

---

### Phase 6: Quality Audit & Final Review
**Assigned to**: Quality Auditor
**Dependencies**: Phase 5 complete (all construction finished)

**Review Checklist**:

1. **Scale Verification** (minecraft_scale_reference.txt compliance):
   - [ ] Living room 8x5 = 40 m² (comfortable range ✓)
   - [ ] Bedroom 6x5 = 30 m² (comfortable range ✓)
   - [ ] Kitchen 6x8 = 48 m² (spacious range ✓)
   - [ ] Ceiling heights: 3-4 blocks (comfortable ✓)
   - [ ] Porch depth: 3 blocks (usable ✓)
   - [ ] Door clearances: 2 blocks tall (✓)
   - [ ] Window placement: Y=66-67 (eye level ✓)
   - [ ] Furniture clearances: 1-2 blocks (✓)

2. **Florida Beach Style Compliance**:
   - [ ] Color palette: White, birch, light blue (coastal ✓)
   - [ ] Large windows: 15-20% wall coverage (modern ✓)
   - [ ] Open floor plan: Living→Kitchen flow (✓)
   - [ ] Covered porch: 14x3 lanai (✓)
   - [ ] Low-pitch hip roof: Florida style (✓)
   - [ ] Light, airy aesthetic (✓)

3. **Detail Quality**:
   - [ ] Window frames: Birch trim present (✓)
   - [ ] Door trim: Accent details (✓)
   - [ ] Furniture: Properly scaled and placed (✓)
   - [ ] Lighting: 8 sources, spawn-safe coverage (✓)
   - [ ] Landscape: Palm trees, beach grass, pathways (✓)
   - [ ] Porch details: Posts, railings, seating (✓)

4. **Symmetry & Proportion**:
   - [ ] Facade balanced (windows evenly spaced)
   - [ ] Roof symmetrical (hip roof, 4-way slopes)
   - [ ] Interior layout logical (flow, circulation)
   - [ ] Exterior/interior color harmony

5. **Block Count Sanity Check**:
   - Foundation: ~252 blocks (14x18)
   - Walls: ~800 blocks (perimeter walls, 4 tall)
   - Roof: ~350 blocks (hip roof with overhang)
   - Interior: ~400 blocks (floors, furniture, details)
   - Landscape: ~200 blocks (paths, vegetation)
   - **Total estimate**: ~2,000 blocks (modest, detailed home ✓)

6. **User Specification Compliance**:
   - [ ] Location: X=246, Z=-36, Y=64 (✓)
   - [ ] Orientation: Front South (~177°) (✓)
   - [ ] Scale: Real, livable, NOT too large (✓)
   - [ ] Style: Florida beach home (✓)
   - [ ] Detail level: Highly detailed (✓)

**Final Walkthrough**:
- Visual inspection from all four sides
- Interior navigation test (circulation)
- Lighting check (no dark corners)
- Style consistency (coastal aesthetic throughout)

**Sign-off**: If all checkboxes pass → Project complete ✓

---

## Checkpoint Protocol

**After Phase 1 (Shell)**: Verify foundation dimensions, wall heights, room divisions
**After Phase 3 (Exterior+Roof)**: Confirm facade appearance, roof slope, overall silhouette
**After Phase 4 (Interior)**: Check furniture placement, lighting, circulation flow
**After Phase 5 (Landscape)**: Verify coastal integration, pathway quality, vegetation
**After Phase 6 (QA)**: Final approval before project close

---

## WorldEdit Command Summary

### Critical Syntax Reminder
⚠️ **CONSOLE COORDINATES**: Use comma-separated format: `//pos1 X,Y,Z`

### Typical Command Sequences (by Phase)

**Phase 1 - Foundation**:
```
//pos1 246,64,-36
//pos2 260,64,-18
//set smooth_sandstone
```

**Phase 1 - Exterior Walls**:
```
//pos1 246,65,-36
//pos2 260,68,-18
//walls white_concrete
```

**Phase 2 - Windows**:
```
//pos1 [X],[Y],[Z]
//pos2 [X+width],[Y+height],[Z]
//set white_stained_glass_pane
```

**Phase 3 - Roof**:
```
//pos1 245,69,-37
//pos2 261,73,-17
[Specialized hip roof construction with birch_stairs]
```

**Phase 4 - Interior**:
```
//pos1 247,65,-35
//pos2 259,65,-19
//set birch_planks (interior flooring)
[Furniture placement with individual blocks]
```

**Phase 5 - Pathways**:
```
//pos1 246,64,-37
//pos2 260,64,-44
//set sandstone (pathway pattern)
```

---

## Expected Timeline

- **Phase 1**: Foundation & Shell - 50 blocks, 5 minutes
- **Phase 2**: Facade & Windows - 100 blocks, 10 minutes
- **Phase 3**: Roofing - 350 blocks, 15 minutes
- **Phase 4**: Interior - 400 blocks, 20 minutes
- **Phase 5**: Landscape - 200 blocks, 15 minutes
- **Phase 6**: QA Review - 5 minutes

**Total**: ~70 minutes for complete, highly detailed Florida beach home

---

## Notes for Execution

1. **Always verify coordinates** before large //set operations
2. **Use //undo** if mistakes occur (WorldEdit history available)
3. **Work incrementally**: Complete each room/section before moving on
4. **Reference scale guide**: Keep minecraft_scale_reference.txt proportions
5. **Lighting last**: Add sea_lanterns and lanterns after walls/roof complete
6. **Landscape integration**: Blend with existing terrain, don't bulldoze everything

---

**Master Planner Sign-off**: Build plan complete and ready for execution.
**Next Step**: Delegate Phase 1 (Foundation & Shell) to Shell Engineer.
