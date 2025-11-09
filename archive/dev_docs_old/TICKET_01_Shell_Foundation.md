# TICKET 01: Foundation & Shell Structure
**Phase**: 1 of 6
**Assigned to**: Shell Engineer
**Dependencies**: None (first phase)
**Status**: Ready for execution

---

## Objective
Build the structural foundation and exterior shell for the Florida beach home:
- Elevated foundation platform (Y=64)
- Exterior walls (4 blocks tall, white_concrete)
- Interior floor (birch_planks)
- Room division walls
- Door and window openings marked

---

## Specifications

### Foundation Platform
- **Material**: `smooth_sandstone`
- **Level**: Y=64
- **Dimensions**: 14 blocks (X) × 18 blocks (Z)
- **Coordinates**: X 246→260, Z -36→-18

### Exterior Walls
- **Material**: `white_concrete`
- **Height**: 4 blocks (Y=65 to Y=68)
- **Thickness**: 1 block
- **Style**: Clean, modern beach home

### Interior Floor
- **Material**: `birch_planks`
- **Level**: Y=65
- **Coverage**: Inside exterior walls only (not under walls)

### Room Divisions
1. **Living/Bedroom Divider**:
   - North-South wall at X=253
   - From Z=-35 to Z=-27 (8 blocks long)
   - Height: Y=65 to Y=68
   - Material: `white_concrete`
   - **Door opening**: 1-block wide at Z=-30 (Y=65-66)

2. **Kitchen Partition**:
   - East-West wall at Z=-26
   - From X=247 to X=259 (12 blocks long)
   - Height: Y=65 to Y=68
   - Material: `white_concrete`
   - **Opening**: 3-block wide gap at X=250-252 (open floor plan)

### Wall Openings (marked for future phases)

**South Wall (Front, Porch Wall)** - Z=-36:
- Main entrance: 1-block wide at X=253 (Y=65-66) - **SET TO AIR**

**East Wall (Bedroom)** - X=260:
- Window 1: 2×2 at Z=-32 to -30, Y=66-67 - **SET TO AIR**
- Window 2: 2×2 at Z=-24 to -22, Y=66-67 - **SET TO AIR**

**West Wall (Living Room)** - X=246:
- Window 1: 3×2 at Z=-34 to -31, Y=66-67 - **SET TO AIR**
- Window 2: 3×2 at Z=-26 to -23, Y=66-67 - **SET TO AIR**

**North Wall (Kitchen)** - Z=-18:
- Window 1: 2×2 at X=252-254, Y=66-67 - **SET TO AIR**

---

## WorldEdit Command Sequence

### Step 1: Foundation Platform (smooth_sandstone)
```
//pos1 246,64,-36
//pos2 260,64,-18
//set smooth_sandstone
```
**Expected result**: 14×18 sandy foundation slab at Y=64

---

### Step 2: Exterior Walls - Shell Only (hollow box)
```
//pos1 246,65,-36
//pos2 260,68,-18
//walls white_concrete
```
**Expected result**: 4-block tall hollow rectangular shell (no roof/floor)

---

### Step 3: Interior Floor (birch_planks)
```
//pos1 247,65,-35
//pos2 259,65,-19
//set birch_planks
```
**Expected result**: Birch wood flooring inside the exterior walls

---

### Step 4: Living/Bedroom Divider Wall (North-South)
```
//pos1 253,65,-35
//pos2 253,68,-27
//set white_concrete
```
**Expected result**: Interior wall separating living room (West) from bedroom (East)

---

### Step 5: Bedroom Doorway (opening in divider wall)
```
//pos1 253,65,-30
//pos2 253,66,-30
//set air
```
**Expected result**: 1×2 doorway connecting living room to bedroom

---

### Step 6: Kitchen Partition Wall (East-West, with opening)
```
//pos1 247,65,-26
//pos2 249,68,-26
//set white_concrete
```
**Expected result**: Western section of kitchen wall

```
//pos1 253,65,-26
//pos2 259,68,-26
//set white_concrete
```
**Expected result**: Eastern section of kitchen wall (3-block gap left for open floor plan)

---

### Step 7: Front Door Opening (South wall, main entrance)
```
//pos1 253,65,-36
//pos2 253,66,-36
//set air
```
**Expected result**: 1×2 entrance opening in front wall

---

### Step 8: East Wall Windows (Bedroom side)

**Window 1** (North window):
```
//pos1 260,66,-32
//pos2 260,67,-30
//set air
```
**Expected result**: 2×2 window opening (will be glazed in Phase 2)

**Window 2** (South window):
```
//pos1 260,66,-24
//pos2 260,67,-22
//set air
```
**Expected result**: 2×2 window opening

---

### Step 9: West Wall Windows (Living room side)

**Window 1** (South window, wide):
```
//pos1 246,66,-34
//pos2 246,67,-31
//set air
```
**Expected result**: 3×2 wide window opening (coastal style)

**Window 2** (North window, wide):
```
//pos1 246,66,-26
//pos2 246,67,-23
//set air
```
**Expected result**: 3×2 wide window opening

---

### Step 10: North Wall Window (Kitchen)

**Window 1** (centered above future counters):
```
//pos1 252,66,-18
//pos2 254,67,-18
//set air
```
**Expected result**: 2×2 kitchen window opening

---

### Step 11: Covered Porch Floor (extends South from front wall)
```
//pos1 246,65,-39
//pos2 260,65,-36
//set birch_planks
```
**Expected result**: 14×3 porch floor extending South (same level as interior)

---

## Verification Checklist

After completing all commands, verify:

- [ ] Foundation platform: 14×18 smooth_sandstone at Y=64
- [ ] Exterior walls: 4 blocks tall (Y=65-68), white_concrete
- [ ] Interior floor: Birch_planks at Y=65 (inside walls)
- [ ] Living/Bedroom divider: North-South wall at X=253 with 1×2 door
- [ ] Kitchen partition: East-West wall at Z=-26 with 3-block opening
- [ ] Front door: 1×2 opening at X=253, Z=-36
- [ ] East windows: Two 2×2 openings at proper positions
- [ ] West windows: Two 3×2 openings at proper positions
- [ ] North window: One 2×2 opening centered
- [ ] Porch floor: 14×3 birch_planks extending South

**Block count estimate**: ~850 blocks
- Foundation: 252 blocks
- Walls: ~500 blocks
- Floor: ~200 blocks

---

## Success Criteria

✅ Foundation platform complete and level
✅ Exterior walls 4 blocks tall, clean white_concrete
✅ All window openings cut at Y=66-67 (eye level)
✅ Door openings cut at Y=65-66 (proper height)
✅ Interior divider walls with proper openings
✅ Porch floor extends South from front wall
✅ Ready for Phase 2 (Facade Architect to add windows/trim)

---

## Notes for Executor

1. **Coordinate format**: Remember comma-separated (e.g., `//pos1 246,64,-36`)
2. **Work order**: Foundation → Walls → Floor → Divisions → Openings → Porch
3. **Undo available**: Use `//undo` if any mistakes occur
4. **Size check**: Use `//size` after selections to verify dimensions
5. **Visual check**: Walk through structure to confirm room sizes feel right

---

## Handoff to Phase 2

Once complete, report:
- Total blocks placed
- Any deviations from plan
- Structural integrity confirmed
- Ready for Facade Architect (Phase 2: Windows, doors, trim, porch details)

**Shell Engineer**: Ready to execute ✓
