# Minecraft Architectural Patterns Reference

## Purpose

This document provides comprehensive guidance on proper Minecraft building techniques, material usage, and architectural conventions. Use this to ensure builds follow best practices and avoid common mistakes.

---

## Building Anatomy: Essential Elements

Every well-designed Minecraft structure includes these key elements:

### 1. Foundation & Structure
- **Foundation blocks** - Base layer, often different material than walls
- **Corner pillars** - Vertical columns at building corners (contrasting material)
- **Structural supports** - Interior columns for large spaces
- **Floor** - Ground level, often wood planks or stone

### 2. Walls & Surfaces
- **Primary walls** - Main exterior material
- **Trim** - Contrasting material around windows/doors
- **Texture variation** - Mix of similar blocks (e.g., stone + stone bricks + andesite)

### 3. Roof System
- **Roof structure** - Stairs and slabs forming the roof shape
- **Roof cap/ridge** - Top edge, often full blocks or different material
- **Overhang** - Roof extends beyond walls (1 block minimum)
- **Gutter/trim** - Edge detail under overhang

### 4. Openings
- **Windows** - Glass panes with surrounding frame/trim
- **Doors** - Entrance with trim or different material surround
- **Window sills** - Slabs or stairs below windows (exterior)
- **Lintels** - Support blocks above openings

### 5. Lighting
- **Ceiling lights** - Attached to ceiling blocks (NOT floating)
- **Wall sconces** - Attached to walls
- **Floor lamps** - On ground or on fence posts
- **Exterior lighting** - On walls or posts, proper spacing (8-12 blocks)

### 6. Details & Decoration
- **Trim bands** - Horizontal lines of contrasting material
- **Cornices** - Decorative ledge at roofline
- **Buttresses** - Exterior support structures (decorative or functional)
- **Varied depth** - Not all walls flat (recesses, protrusions)

---

## Material Role System

**CRITICAL**: Every build should use materials with defined roles for visual interest and realism.

### Primary Material (60-70% of build)
**Purpose**: Main walls, bulk of structure
**Examples**:
- Stone bricks (castles, fortresses)
- Oak planks (wooden houses)
- Sandstone (desert buildings)
- Bricks (urban buildings)

### Structural Material (10-15% of build)
**Purpose**: Corner pillars, floor columns, structural emphasis
**MUST be different from primary material**

**Rules**:
- ⚠️ **ALWAYS use contrasting material for corner pillars**
- Pillars should be 1x1 or 2x2 at building corners
- Interior columns in large rooms (every 6-8 blocks)
- Different color/texture family from primary

**Examples**:
- Primary: Stone bricks → Structural: Polished andesite or deepslate
- Primary: Oak planks → Structural: Stripped oak logs or dark oak
- Primary: Sandstone → Structural: Smooth sandstone or cut red sandstone
- Primary: Bricks → Structural: Stone bricks or polished granite

### Trim Material (10-15% of build)
**Purpose**: Window frames, door surrounds, decorative bands

**Rules**:
- Frame windows with 1-block border of contrasting material
- Surround doors with trim (sides + top)
- Create horizontal bands at floor levels (multi-story buildings)
- Use slabs/stairs for dimensional trim

**Examples**:
- Primary: Stone bricks → Trim: Smooth stone or cobblestone
- Primary: Oak planks → Trim: Spruce planks or stripped logs
- Primary: Sandstone → Trim: Chiseled sandstone or terracotta

### Detail Material (5-10% of build)
**Purpose**: Accents, decorative elements, final touches

**Examples**:
- Buttons, trapdoors (shutters on windows)
- Fences (railings, window bars)
- Slabs (window sills, ledges)
- Carpets, banners, paintings (interior)

---

## Critical Pattern: Corner Pillars

**THE RULE**: ⚠️ Every building MUST have contrasting corner pillars

### Why Corner Pillars Matter
- Define the vertical edges of the structure
- Add visual interest and depth
- Suggest structural support (realistic architecture)
- Break up monotonous walls

### How to Build Corner Pillars

**Small Buildings (1-2 stories)**:
```
Plan View (top-down):

P = Pillar block (contrasting material)
W = Wall block (primary material)

Corner:
P W W W
W . . .
W . . .
W . . .

Vertical (side view):
P P P P P P (floor to roof)
```

**Large Buildings (3+ stories)**:
```
Plan View:

P P W W W
P P . . .
W . . . .
W . . . .

2x2 pillar at corner for larger structures
```

**Example Material Combinations**:
```
Building: Stone brick castle
→ Corners: Polished andesite pillars (1x1)
→ Walls: Stone bricks
→ Trim: Smooth stone around windows

Building: Wooden house
→ Corners: Stripped oak log pillars (1x1)
→ Walls: Oak planks
→ Trim: Spruce planks around windows

Building: Desert temple
→ Corners: Smooth sandstone pillars (2x2)
→ Walls: Sandstone
→ Trim: Chiseled sandstone bands
```

### Interior Pillars

**When to use**:
- Rooms wider than 10 blocks
- Great halls, throne rooms, churches
- Multi-story atriums

**Placement**:
- Every 6-8 blocks in large rooms
- Aligned in rows (creates colonnade)
- Same material as corner pillars

---

## Critical Pattern: Ceiling Lights

**THE RULE**: ⚠️ Lights MUST be attached to solid blocks - NEVER floating mid-air

### Proper Light Fixture Construction

**Flush Ceiling Light** (simplest):
```
Top view:
C C C C C (ceiling blocks)
C L L L C (L = light source)
C C C C C

Side view:
C C C C C (ceiling solid blocks)
L L L L L (lights attached BELOW ceiling)
. . . . . (air - room below)
```

**Lantern on Ceiling**:
```
Side view:
C C C C C (ceiling blocks - wood planks, stone, etc.)
| | | | | (chains - attached to ceiling above)
L L L L L (lanterns hanging from chains)
. . . . . (air)

Place: 1. Ceiling block, 2. Chain below, 3. Lantern below chain
```

**Glowstone Inset** (cleanest):
```
Side view:
C C C G C C (G = glowstone, C = ceiling blocks)
. . . . . . (air)

Glowstone is INSIDE the ceiling, flush with bottom surface
```

**Torch Sconce on Wall**:
```
Side view:
W W W W W (wall)
    T     (torch attached to wall)
. . . . . (air)

NEVER place torch floating in mid-air
```

**Chandelier (Advanced)**:
```
Side view:
C C C C C (ceiling)
    F     (fence post hanging from ceiling)
    F     (more fence)
  L F L   (lanterns attached to sides of fence)
    F
  L   L   (more lanterns)

Uses fence posts as structure, lanterns attached to fence sides
```

### Bad Examples (NEVER DO THIS)

❌ **Floating Lantern**:
```
C C C C C (ceiling)
. . . . . (air)
. . L . . (lantern floating - NO SUPPORT)
. . . . . (air)
```

❌ **Torch in Mid-Air**:
```
W W W W W (wall)
. . T . . (torch floating away from wall)
. . . . . (air)
```

### Light Spacing

**Interior Ceiling Lights**:
- Every 6-8 blocks (prevents mob spawning)
- Symmetrical placement (centered in rooms)
- Consider architectural rhythm (match window spacing)

**Exterior Wall Lights**:
- Every 8-12 blocks along walls
- Near entrances (both sides of door)
- Corner emphasis (lights at building corners)

---

## Critical Pattern: Slab Usage

**THE RULE**: ⚠️ Use slabs for slopes, low-pitch roofs, and dimensional details

### When to Use Slabs vs. Stairs vs. Full Blocks

**Slabs (Half-Blocks)**:
- ✅ Low-pitch roofs (1:2 slope or less)
- ✅ Gradual slopes and ramps
- ✅ Horizontal ledges and trim
- ✅ Window sills (exterior)
- ✅ Furniture (tables, counters)
- ✅ Path borders and curbs

**Stairs**:
- ✅ Medium-pitch roofs (1:1 slope)
- ✅ Steep roofs (steeper than 1:1)
- ✅ Actual stairs/steps
- ✅ Roof edges and cornices
- ✅ Chair backs

**Full Blocks**:
- ✅ Walls, floors, ceilings
- ✅ Flat roofs
- ✅ Roof ridges/caps
- ✅ Structural elements

### Slab Roof Construction (Low Pitch)

**Gable Roof with Slabs** (1:2 slope):
```
Side view (cross-section):

R R R R R R R R R (ridge - full blocks)
S S S S S S S S   (slabs - one step down per 2 blocks horizontal)
  S S S S S S     (slabs continuing slope)
    S S S S       (slabs)
W W W S S W W W   (walls with slab overhang)

S = slab (top half)
W = wall
R = ridge (full blocks)
```

**Steps to build**:
1. Build walls
2. Place ridge (center line of roof)
3. Place slabs stepping down from ridge
4. Each slab layer extends 1 block outward horizontally
5. Every 2 blocks horizontal = 1 block down vertical
6. Overhang extends 1 block past walls

**Slab Roof Example** (side view):
```
Layer 0 (ridge): oak_slab[type=top] at Y=10
Layer 1: oak_slab[type=top] at Y=9 (2 blocks out from ridge)
Layer 2: oak_slab[type=top] at Y=8 (4 blocks out from ridge)
Layer 3: oak_slab[type=top] at Y=7 (6 blocks out from ridge - overhang)
Wall: at Y=7
```

### Slab vs. Stair Roof Decision

**Use Slabs When**:
- Low-pitch aesthetic (barn, modern, Asian-inspired)
- Wide buildings (slope would be too steep with stairs)
- Gradual, gentle roof
- Building is 1-story and roof shouldn't dominate

**Use Stairs When**:
- Traditional peaked roof
- Medieval/fantasy buildings
- Multi-story buildings
- Steep pitch desired (faster runoff appearance)

**Example Comparison**:

Stair roof (1:1 slope - steep):
```
      S (ridge)
    S   S
  S       S
W           W (walls)
```

Slab roof (1:2 slope - gentle):
```
      F F F (ridge - full blocks)
    s s s s (slabs)
  s s     s s
W             W (walls)
```

### Slab Window Sills (Exterior)

**Purpose**: Add depth and detail to facades

**Construction**:
```
Side view (exterior wall):

W W W W W (wall above window)
G G G G G (glass panes - window)
W W W W W (wall below window)
  s s s   (slabs extending out below window - sill)
W W W W W (wall continues down)

s = slab (bottom half) extending 1 block out
```

**Details**:
- Slabs extend 1 block outward from wall
- Use bottom-half slabs (`[type=bottom]`)
- Material can match window trim or wall
- Every window should have a sill (exterior only)

### Slab Horizontal Trim Bands

**Purpose**: Break up tall walls, mark floor levels

**Construction**:
```
Front view (exterior):

W W W W W W W (wall - floor 2)
s s s s s s s (slab band - marks floor 1/2 boundary)
W W W W W W W (wall - floor 1)

s = slab (top half) protruding from wall
```

**Usage**:
- Multi-story buildings
- Between each floor (exterior)
- Creates visual rhythm
- Use contrasting material (trim color)

---

## Common Mistakes to Avoid

### 1. ❌ Floating Blocks

**Problem**: Blocks with no attachment point (especially lights, decorations)

**Examples of Floating Blocks**:
- Lanterns in mid-air
- Torches not on walls/floors/ceilings
- Decoration blocks floating
- Signs not attached to surfaces

**Solution**: ALWAYS attach blocks to solid surfaces
```
✅ CORRECT: Lantern hanging from ceiling chain
❌ WRONG: Lantern in middle of room with no support
```

### 2. ❌ No Corner Pillars

**Problem**: All walls use same material, no structural emphasis

**Example**:
```
❌ WRONG (all stone bricks):
S S S S S
S . . . S
S . . . S
S S S S S

✅ CORRECT (corner pillars):
P S S S P
S . . . S
S . . . S
P S S S P

P = Polished andesite pillar
S = Stone brick wall
```

**Solution**: Use contrasting material for corner pillars (1x1 minimum)

### 3. ❌ All Stairs for Roofs

**Problem**: Using stairs for every roof, even when slabs would look better

**When it's wrong**:
- Low-pitch roof on wide building → Too steep with stairs
- Modern or barn aesthetic → Slabs give gentler slope
- 1-story building with steep stairs roof → Roof dominates, looks odd

**Solution**: Use slabs for low-pitch roofs (1:2 slope), stairs for traditional peaked roofs (1:1 slope)

### 4. ❌ No Material Variation

**Problem**: Entire build is one material (all oak planks, all stone bricks)

**Example**:
```
❌ WRONG:
Oak planks: walls, floor, ceiling, pillars, trim, roof

✅ CORRECT:
Oak planks: walls (primary)
Stripped oak logs: corner pillars (structural)
Spruce planks: trim around windows (trim)
Oak slabs: roof (roof system)
```

**Solution**: Use material role system (primary, structural, trim, detail)

### 5. ❌ Windows Without Frames

**Problem**: Glass panes placed directly in walls with no trim

**Example**:
```
❌ WRONG:
W W W W W
W G G G W
W W W W W

W = wall, G = glass, no distinction

✅ CORRECT:
W W W W W
W T T T W
W T G T W
W T T T W
W W W W W

T = trim material framing glass
```

**Solution**: Always frame windows with 1-block border of contrasting material

### 6. ❌ Flat Roofs on All Buildings

**Problem**: No roof variation, everything is flat

**Solution**: Use variety
- Gable roofs (triangular, most common)
- Hip roofs (four sloped sides)
- Gambrel roofs (barn-style, two slopes per side)
- Mansard roofs (steep lower slope, flat upper)
- Flat roofs (only for modern or desert buildings)

### 7. ❌ No Overhangs

**Problem**: Roof edges align exactly with walls (no overhang)

**Solution**: Extend roof 1-2 blocks past walls
- Protects walls (realistic)
- Adds depth and shadow
- Makes roof visually distinct from walls

### 8. ❌ Symmetry Violations

**Problem**: Asymmetric buildings without intentional asymmetry

**Examples**:
- Windows not aligned
- Door off-center when should be centered
- One side has feature other doesn't

**Solution**:
- Intentional symmetry: Mirror both sides exactly
- Intentional asymmetry: Clear design reason (tower on one side, etc.)
- Use `check_symmetry` tool to verify

---

## Building Checklist

### Pre-Build Planning

✅ **Material Palette Defined**:
- [ ] Primary material chosen (walls)
- [ ] Structural material chosen (pillars, columns) - MUST be different
- [ ] Trim material chosen (windows, doors)
- [ ] Detail materials selected

✅ **Dimensions Planned**:
- [ ] Foundation size determined
- [ ] Room sizes appropriate (see minecraft_scale_reference.txt)
- [ ] Ceiling heights comfortable (3 blocks minimum)

✅ **Location Validated**:
- [ ] Terrain analyzed (use terrain_analyzer)
- [ ] Ground level determined (use get_surface_level)
- [ ] Orientation decided (front faces cardinal direction)

### During Construction

✅ **Structural Elements**:
- [ ] Foundation laid (different material or same as walls)
- [ ] Corner pillars placed (CONTRASTING MATERIAL, 1x1 minimum)
- [ ] Interior columns in large rooms (every 6-8 blocks)
- [ ] Walls built with primary material
- [ ] Floor installed (planks, stone, etc.)

✅ **Openings**:
- [ ] Windows have trim/frames (contrasting material)
- [ ] Doors have trim surrounds
- [ ] Window sills added (slabs, exterior)
- [ ] Lintels above openings (if needed)

✅ **Roof System**:
- [ ] Roof type appropriate (gable, hip, flat, etc.)
- [ ] Slabs used for low-pitch roofs, stairs for steep
- [ ] Roof overhangs 1-2 blocks past walls
- [ ] Ridge capped with full blocks or different material
- [ ] Roof material complements walls

✅ **Lighting**:
- [ ] Ceiling lights attached to ceiling blocks (NOT floating)
- [ ] Wall lights attached to walls
- [ ] Exterior lights spaced every 8-12 blocks
- [ ] Light level adequate (no dark spots < 8)

✅ **Details**:
- [ ] Trim bands added (if multi-story)
- [ ] Texture variation in walls (mix similar blocks)
- [ ] Depth variation (not all walls flat)
- [ ] Decorative elements appropriate

### Post-Build Validation

✅ **Quality Checks**:
- [ ] No floating blocks (use validate_structure tool)
- [ ] Symmetry correct (use check_symmetry tool)
- [ ] Lighting adequate (use analyze_lighting tool)
- [ ] Corner pillars present and contrasting
- [ ] Material roles followed (primary, structural, trim)

✅ **Final Polish**:
- [ ] Add interior furniture (use furniture_lookup)
- [ ] Landscape integration (paths, gardens)
- [ ] Exterior lighting complete
- [ ] Signage or banners (if applicable)

---

## Material Combination Reference

### Stone-Based Buildings

**Castle / Fortress**:
- Primary: Stone bricks
- Structural: Polished andesite or deepslate bricks
- Trim: Smooth stone or cobblestone
- Detail: Stone buttons, iron bars

**Medieval Manor**:
- Primary: Stone bricks (60%) + Cobblestone (20%) mix
- Structural: Dark oak logs (corner pillars)
- Trim: Stripped dark oak logs
- Detail: Oak trapdoors (shutters)

**Stone Cottage**:
- Primary: Cobblestone + stone mix
- Structural: Stone bricks (corners)
- Trim: Smooth stone
- Roof: Stone brick slabs
- Detail: Wooden trapdoors, flower pots

### Wood-Based Buildings

**Oak House (Traditional)**:
- Primary: Oak planks
- Structural: Stripped oak logs or dark oak logs
- Trim: Spruce planks or stripped oak
- Roof: Oak stairs or dark oak stairs
- Detail: Oak fences, trapdoors

**Spruce Cabin**:
- Primary: Spruce planks
- Structural: Stripped spruce logs
- Trim: Dark oak planks
- Roof: Spruce stairs
- Detail: Spruce trapdoors, lanterns

**Bamboo/Jungle House**:
- Primary: Bamboo planks
- Structural: Stripped bamboo (corners)
- Trim: Jungle planks
- Roof: Bamboo slabs (low pitch)
- Detail: Bamboo fences, paper lanterns

### Desert Buildings

**Sandstone Temple**:
- Primary: Sandstone (60%) + Smooth sandstone (20%)
- Structural: Cut sandstone or smooth sandstone (2x2 pillars)
- Trim: Chiseled sandstone
- Detail: Terracotta accents, gold blocks

**Desert House**:
- Primary: Sandstone
- Structural: Smooth sandstone
- Trim: Cut red sandstone
- Roof: Smooth sandstone slabs (flat or low pitch)
- Detail: Terracotta, cactus decorations

### Modern Buildings

**Modern House**:
- Primary: Quartz blocks or white concrete
- Structural: Smooth stone or polished andesite
- Trim: Black concrete or gray concrete
- Roof: Flat (quartz slabs)
- Detail: Glass panes (large windows), iron bars

**Industrial Building**:
- Primary: Stone bricks + andesite mix
- Structural: Polished andesite
- Trim: Iron blocks or dark oak planks
- Roof: Flat or low-pitch (andesite slabs)
- Detail: Iron bars, chains, lanterns

---

## Advanced Patterns

### Texture Mixing (Natural Variation)

**Purpose**: Avoid monotonous walls by mixing similar materials

**Example - Stone Castle Walls**:
```
Instead of 100% stone bricks:
70% stone bricks
20% andesite
10% cobblestone

Random distribution creates natural texture
```

**How to apply**:
```
Use WorldEdit patterns:
//set 70%stone_bricks,20%andesite,10%cobblestone
```

**Material Families** (safe to mix):
- Stone: stone, andesite, diorite, granite, cobblestone, stone bricks
- Wood: planks, logs, stripped logs (within same wood type)
- Sandstone: sandstone, smooth sandstone, cut sandstone, chiseled sandstone
- Nether: netherrack, nether bricks, red nether bricks, blackstone

### Depth Variation

**Purpose**: Create visual interest by varying wall depth

**Techniques**:
```
1. Recessed windows (glass 1 block behind wall surface)
2. Protruding trim (slabs, stairs extending from wall)
3. Buttresses (columns extending outward)
4. Balconies (platforms extending from upper floors)
5. Archways (recessed entryways)
```

**Example - Recessed Window**:
```
Side view (cross-section):

W W W W W (wall outer surface)
  G G G   (glass set back 1 block)
W W W W W (wall behind window)

Creates shadow and depth
```

### Roof Combinations

**Gambrel Roof** (barn-style):
```
Uses stairs (steep lower) + slabs (gentle upper)

Cross-section:
        F F F (ridge)
      S S S S (slabs - gentle upper slope)
    T       T (stairs - steep lower slope)
  T           T (stairs)
W               W (walls)

T = stairs (steep), S = slabs (gentle), F = full blocks
```

**Hip Roof** (four sloped sides):
```
Top view:

    S S S (slabs/stairs)
  S       S
S           S
  S       S
    S S S

All four sides slope toward center
More complex but elegant
```

---

## Block State Reference

### Slabs

**Types**:
- `[type=top]` - Upper half of block
- `[type=bottom]` - Lower half of block (default)
- `[type=double]` - Full block (two slabs)

**Usage**:
- Roofs: `[type=top]` (water runs off top surface)
- Window sills: `[type=bottom]` (extends out from wall)
- Ledges/trim: `[type=top]` or `[type=bottom]` depending on position

### Stairs

**Orientation**:
- `[facing=north/south/east/west]` - Which direction high side points
- `[half=top/bottom]` - Normal (bottom) or inverted (top)
- `[shape=straight/inner_left/inner_right/outer_left/outer_right]` - Auto-set by neighbors

**Roof Usage**:
- `[half=bottom]` - Normal roofs (climb upward)
- `[half=top]` - Underside details or inverted roofs

**Critical**: ALWAYS specify orientation for roofs
```
✅ CORRECT: oak_stairs[facing=north,half=bottom]
❌ WRONG: oak_stairs (random orientation)
```

### Fences & Walls

**Connection Rules**:
- Fences connect to adjacent fences, solid blocks
- Walls connect to adjacent walls, solid blocks
- Useful for: railings, window bars, fence posts

**Light Fixture Usage**:
- Fence post → Place lantern on top or sides
- Creates vertical support for hanging lights

---

## Putting It All Together: Example Build

**Medieval Stone House with All Patterns**

**Materials**:
- Primary: Stone bricks (walls)
- Structural: Polished andesite (corner pillars, 1x1)
- Trim: Smooth stone (windows, door)
- Roof: Stone brick stairs
- Detail: Oak trapdoors (shutters), lanterns

**Features**:
1. ✅ Corner pillars (polished andesite, contrasting)
2. ✅ Window frames (smooth stone trim around glass)
3. ✅ Window sills (stone brick slabs extending outward)
4. ✅ Gable roof (stone brick stairs, 1:1 slope)
5. ✅ Roof overhang (1 block past walls)
6. ✅ Ceiling lights (lanterns hanging from chains attached to ceiling)
7. ✅ Exterior wall lights (lanterns on walls every 8 blocks)
8. ✅ Door surround (smooth stone trim)
9. ✅ Texture mixing (stone bricks + andesite 80/20 in walls)
10. ✅ Depth variation (recessed windows, slab sills)

**Result**: Professional-quality build following all architectural conventions!

---

## Quick Reference: Material Contrast

**Light + Dark**:
- Oak planks (light) + dark oak planks (dark)
- Sandstone (light) + terracotta (dark)
- Quartz (light) + black concrete (dark)

**Smooth + Textured**:
- Stone bricks (textured) + smooth stone (smooth)
- Cobblestone (textured) + stone bricks (semi-smooth)

**Warm + Cool**:
- Oak/spruce (warm wood) + stone (cool)
- Sandstone (warm) + prismarine (cool)

**Natural + Processed**:
- Oak logs (natural) + oak planks (processed)
- Stone (natural) + stone bricks (processed)

---

**Use this reference for EVERY build to ensure quality, realism, and proper Minecraft architectural conventions!**
