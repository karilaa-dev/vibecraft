# Roofing Guidance Added to CLAUDE.md

## Summary

Added comprehensive roofing best practices section to CLAUDE.md to guide AI agents in building proper Minecraft roofs with correct stair orientation and layering.

## Location

**File:** `/Users/er/Repos/vibecraft/CLAUDE.md`
**Section:** "Common Task Patterns" → "Building Roofs"
**Lines:** 367-497 (130 lines of guidance)

## User Requirements Implemented

### ✅ 1. Use Stairs, Normal Blocks, and Half Slabs
```markdown
**Materials to Use:**
- **Stairs** (oak_stairs, stone_brick_stairs, etc.) - Primary roofing material
- **Slabs** (oak_slab, stone_brick_slab, etc.) - For half-height layers and transitions
- **Full blocks** (planks, bricks, etc.) - For flat roof sections or ridges
```

### ✅ 2. Careful About Rotation and Orientation
```markdown
⚠️ **Stair Orientation:**
- Every stair block has a **facing direction** and **half** (top/bottom)
- Block states: `oak_stairs[facing=north,half=bottom]`
- **NEVER** place stairs randomly - always specify orientation
- Stairs should face outward on roof slopes

**Orientation Guide:**
- `facing=north` → High side points north, slopes down to south
- `facing=south` → High side points south, slopes down to north
- `facing=east` → High side points east, slopes down to west
- `facing=west` → High side points west, slopes down to east

**Half Guide:**
- `half=bottom` → Normal stairs (top surface slopes)
- `half=top` → Inverted/upside-down stairs (bottom surface slopes)
```

### ✅ 3. No Step Blocks Covered Up
```markdown
⚠️ **NO Hidden Stairs:**
- **NEVER** cover up stair blocks with full blocks above them
- Stairs are visible elements - if covered, use full blocks instead
- Exception: Slabs can sit on top of upside-down stairs for detailing
```

### ✅ 4. No Step Blocks Directly on Top of Each Other
```markdown
⚠️ **NO Stacking Stairs:**
- **NEVER** place stair blocks directly on top of each other
- Stacked stairs create visual glitches and look unnatural
- Use full blocks or slabs between stair layers if needed
- Each stair layer should be offset horizontally
```

## Section Contents

### 1. Critical Rules (3 Major Warnings)
- **Stair Orientation** - Always specify facing and half
- **NO Stacking Stairs** - Never place stairs vertically at same X,Z
- **NO Hidden Stairs** - Don't cover stairs with full blocks

### 2. Example Gable Roof Walkthrough
Step-by-step guide showing:
- Roof base placement
- First stair layer with correct orientation
- Second stair layer offset inward
- Continuing to ridge
- Ridge cap with full blocks

### 3. Common Roof Types
- **Gable Roof** - Triangle profile, two sloped sides
- **Hip Roof** - Four sloped sides, complex corners
- **Flat Roof** - Modern style with slabs
- **Mansard Roof** - Steep lower slope, flat upper section

### 4. Orientation Reference Guide
Detailed explanation of:
- **facing** parameter (which direction high side points)
- **half** parameter (top vs bottom orientation)
- Examples for all 8 combinations

### 5. Block State Examples
```
oak_stairs[facing=north,half=bottom]
stone_brick_stairs[facing=east,half=top]
spruce_stairs[facing=south,half=bottom]
```

### 6. Using setblock for Precise Control
When WorldEdit isn't precise enough, use individual setblock commands:
```
setblock 100 71 100 oak_stairs[facing=north,half=bottom]
```

### 7. Common Mistakes Section (❌ vs ✅)
Four critical comparisons:
- ❌ Random stairs vs ✅ Controlled block states
- ❌ Stacked stairs vs ✅ Horizontal offset
- ❌ Covered stairs vs ✅ Exposed or full blocks
- ❌ Mixed stair types vs ✅ Consistent materials

### 8. Pro Tips (6 Best Practices)
1. Test orientation first with single block
2. Work symmetrically
3. Check from all angles
4. Use clipboard for mirroring
5. Layer by layer approach
6. Ridge caps with full blocks/slabs

## Why This Matters

### Problem: AI Makes Common Roofing Mistakes
Without guidance, AI agents would:
- Place stairs with random orientation (looks chaotic)
- Stack stairs vertically (visual glitches)
- Cover stairs unnecessarily (wasted blocks)
- Mix orientations randomly (broken appearance)

### Solution: Clear Rules and Examples
With this section, AI agents now:
- Always specify block states for stairs
- Understand facing and half parameters
- Know to offset stair layers horizontally
- Use appropriate materials for each roof element

## Visual Examples in Guide

### Gable Roof Pattern
```
Layer 5 (Ridge):    [====]         (full blocks)
Layer 4:         [/      \]        (stairs inward)
Layer 3:       [/          \]      (stairs inward)
Layer 2:     [/              \]    (stairs inward)
Layer 1:   [/                  \]  (stairs from wall)
Base:    [____________________]    (wall top)
```

Each layer steps inward by 1 block and up by 1 block.

### Stair Orientation Example (North-facing roof edge)
```
All facing=north, half=bottom:
[↗][↗][↗][↗][↗]  ← High side points north (back)
                   Slopes down to south (front)
```

## Integration with Existing Content

**Fits perfectly after "Complex Building" and before "Tool Selection Guide"**

The progression now flows:
1. Building a Simple Structure
2. Creating Terrain
3. Complex Building
4. **Building Roofs** ← NEW
5. Tool Selection Guide

## Testing Recommendations

### Test Scenarios for AI Agents:

1. **Simple Gable Roof**
   - Request: "Build a gable roof on this 10×10 building"
   - Expected: Properly oriented stairs, no stacking, clean ridge

2. **Hip Roof**
   - Request: "Add a hip roof to this house"
   - Expected: All four sides slope correctly, corners handled

3. **Flat Roof with Trim**
   - Request: "Build a modern flat roof with decorative trim"
   - Expected: Slabs for flat section, stairs for edge trim

4. **Complex Roof with Multiple Sections**
   - Request: "Build a roof with different height sections"
   - Expected: Each section oriented correctly, transitions smooth

## Benefits to Users

### For AI Agents:
- Clear rules prevent common mistakes
- Examples show correct implementation
- Block state syntax reference always available
- Pro tips help with complex roofs

### For Users:
- Better-looking roofs automatically
- No visual glitches from stacked stairs
- Proper material usage (no hidden blocks)
- Consistent quality across all builds

## Future Enhancements

Potential additions to consider:
1. **Roof pitch calculator** - Determine optimal rise/run ratios
2. **Overhang guidelines** - How far to extend beyond walls
3. **Dormer windows** - How to integrate into sloped roofs
4. **Roof trim patterns** - Decorative edge techniques
5. **Material combinations** - Which blocks work well together

## Documentation Files

This guidance is now part of:
- **CLAUDE.md** - Primary AI agent instructions
- **dev_docs/ROOFING_GUIDANCE_ADDED.md** - This implementation summary

## Statistics

- **130 lines** of comprehensive roofing guidance
- **3 critical rules** highlighted with warnings
- **4 common roof types** documented
- **6 pro tips** for best practices
- **8 block state examples** provided
- **1 complete gable roof walkthrough** with step-by-step commands

---

**Status:** ✅ Complete and integrated into CLAUDE.md
**Impact:** High - Prevents common roofing mistakes, ensures quality builds
**Date:** October 31, 2025
