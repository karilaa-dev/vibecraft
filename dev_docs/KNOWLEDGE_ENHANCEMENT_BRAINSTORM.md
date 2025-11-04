# VibeCraft Knowledge Enhancement Brainstorm

## The Goal
Give Claude the knowledge of an experienced Minecraft builder, not just a WorldEdit operator.

## Current State
✅ WorldEdit command knowledge (200+ commands)
✅ Pattern/mask/expression syntax
✅ Tool usage workflows
❌ Block properties and aesthetics
❌ Building design patterns
❌ Architectural knowledge
❌ Material combinations
❌ Scale and proportion guidance

---

## Category 1: Block Database 🧱

### A. Basic Block Properties
```json
{
  "blocks": {
    "oak_planks": {
      "category": "building_blocks",
      "material": "wood",
      "color": "tan/brown",
      "transparency": "opaque",
      "blast_resistance": 3.0,
      "hardness": 2.0,
      "tool_required": "axe",
      "renewable": true,
      "flammable": true,
      "variants": ["oak", "spruce", "birch", "jungle", "acacia", "dark_oak"],
      "use_cases": ["walls", "floors", "roofs", "furniture"],
      "pairs_well_with": ["stone_bricks", "cobblestone", "glass", "oak_stairs"],
      "common_in": ["houses", "cabins", "medieval_builds"]
    }
  }
}
```

**Benefits**:
- Claude knows which blocks are flammable
- Can suggest non-flammable alternatives
- Understands tool requirements
- Knows what "pairs well" aesthetically

### B. Block Color Palette
```yaml
# Organized by color for aesthetic building
colors:
  whites:
    - quartz_block: "pure white, smooth"
    - white_concrete: "pure white, flat"
    - white_wool: "pure white, soft texture"
    - bone_block: "off-white, ribbed"
    - birch_planks: "cream/tan, wood grain"

  grays:
    - stone_bricks: "medium gray, structured"
    - andesite: "gray, speckled"
    - cobblestone: "rough gray, rustic"
    - gray_concrete: "smooth gray, modern"

  browns:
    - oak_planks: "tan brown, warm"
    - dark_oak_planks: "deep brown, rich"
    - spruce_planks: "orange brown, cozy"
```

**Benefits**:
- Claude can create color palettes
- "Build in gray and white" → knows which blocks
- Better aesthetic decisions

### C. Block Texture Families
```yaml
texture_groups:
  smooth:
    - concrete (all colors)
    - quartz_block
    - terracotta (glazed variants)
    - purpur_block

  rough:
    - cobblestone
    - andesite
    - stone
    - netherrack

  patterned:
    - bricks
    - nether_bricks
    - prismarine
    - end_stone_bricks
```

**Benefits**:
- Mix/match complementary textures
- Avoid texture clashing
- Create cohesive designs

---

## Category 2: Building Pattern Library 🏗️

### A. Common Structure Patterns
```yaml
patterns:
  walls:
    basic_wall:
      description: "Simple wall with no detail"
      command: "//walls <material>"

    detailed_wall:
      description: "Wall with depth and texture"
      steps:
        - "//walls stone_bricks"
        - "//replace stone_bricks 20%cobblestone,80%stone_bricks"
        - "Add window cutouts with //set air"

    medieval_wall:
      description: "Thick wall with battlements"
      steps:
        - "//walls cobblestone (2 blocks thick)"
        - "//faces stone_bricks (cap top)"
        - "Create crenellations with alternating blocks"

  roofs:
    flat_roof:
      materials: ["concrete", "terracotta", "planks"]
      slope: "0 degrees"
      style: "modern"

    gabled_roof:
      materials: ["stairs", "slabs"]
      slope: "45 degrees"
      style: "traditional"
      steps:
        - "Build up center spine"
        - "//stack outward with stairs"
        - "Cap with slabs"

    dome_roof:
      command: "//hsphere <material> <radius>"
      materials: ["quartz", "terracotta", "prismarine"]
      style: "grand/religious"
```

**Benefits**:
- Claude knows multiple ways to build common structures
- Can suggest appropriate style for context
- Has step-by-step templates

### B. Architectural Styles
```yaml
styles:
  medieval:
    materials:
      primary: ["cobblestone", "stone_bricks", "oak_planks"]
      accent: ["dark_oak", "spruce", "andesite"]
      roofing: ["oak_stairs", "spruce_stairs", "cobblestone"]
    features:
      - "Thick walls (2+ blocks)"
      - "Small windows"
      - "Steep roofs"
      - "Towers and battlements"
      - "Asymmetrical layouts"
    typical_blocks:
      walls: "cobblestone, stone_bricks"
      floors: "stone_bricks, oak_planks"
      roofs: "oak_stairs, cobblestone_stairs"
      details: "fences, iron_bars, lanterns"

  modern:
    materials:
      primary: ["white_concrete", "gray_concrete", "glass"]
      accent: ["black_concrete", "quartz"]
      roofing: ["concrete (flat)", "quartz_slabs"]
    features:
      - "Clean lines"
      - "Large windows"
      - "Flat or minimal slope roofs"
      - "Geometric shapes"
      - "Symmetrical layouts"
    typical_blocks:
      walls: "white_concrete, glass_panes"
      floors: "gray_concrete, quartz"
      roofs: "gray_concrete, quartz_slabs"
      details: "sea_lanterns, iron_trapdoors"
```

**Benefits**:
- "Build a medieval castle" → Claude knows exactly which blocks
- Maintains style consistency
- Suggests appropriate details

### C. Scale and Proportion Guidelines
```yaml
proportions:
  residential:
    ceiling_height: "3-4 blocks (comfortable)"
    door_height: "2 blocks (standard)"
    window_height: "1-2 blocks"
    room_sizes:
      small: "5x5 to 7x7"
      medium: "8x8 to 12x12"
      large: "13x13+"

  grand_structures:
    ceiling_height: "6-10 blocks (imposing)"
    door_height: "3-4 blocks (grand entrance)"
    window_height: "3-5 blocks (tall windows)"
    room_sizes:
      hall: "20x30+"
      throne_room: "30x40+"

  walls:
    exterior_residential: "1 block thick"
    exterior_fortress: "2-3 blocks thick"
    interior: "1 block thick"
```

**Benefits**:
- Buildings feel properly scaled
- Avoids tiny cramped houses
- Knows when to go grand vs. cozy

---

## Category 3: Building Techniques 🛠️

### A. Detailing Methods
```yaml
techniques:
  depth_and_shadow:
    description: "Create visual interest through depth"
    methods:
      - name: "Inset windows"
        how: "Set windows back 1 block from wall face"
        effect: "Creates shadows, more realistic"

      - name: "Layered walls"
        how: "Use stairs/slabs to create protrusions"
        effect: "Breaks up flat surfaces"

      - name: "Column details"
        how: "Use full blocks flanked by stairs"
        effect: "3D column appearance"

  texture_mixing:
    description: "Combine similar blocks for organic feel"
    ratios:
      subtle: "90% primary, 10% accent"
      moderate: "70% primary, 30% accent"
      heavy: "50/50 mix or more variation"
    examples:
      stone_wall: "80%stone_bricks,15%cobblestone,5%andesite"
      wooden_floor: "70%oak_planks,30%birch_planks"
      medieval_path: "60%cobblestone,30%stone,10%gravel"
```

**Benefits**:
- Creates more interesting, organic builds
- Knows specific ratios that work well
- Can add details automatically

### B. Landscaping Integration
```yaml
landscaping:
  terrain_blending:
    description: "Make builds feel natural in environment"
    techniques:
      - "Use local blocks at foundation"
      - "Gradual transition from stone to grass"
      - "Match biome vegetation"

  garden_patterns:
    formal:
      layout: "Symmetrical, geometric"
      materials: ["hedges (leaves)", "stone_bricks", "water"]

    natural:
      layout: "Organic, curved paths"
      materials: ["flowers", "grass", "coarse_dirt", "gravel"]
```

**Benefits**:
- Buildings don't look "dropped in"
- Can create surroundings
- Knows appropriate vegetation

### C. Interior Design Patterns
```yaml
interiors:
  furniture_patterns:
    table:
      - "fence posts + pressure plate on top"
      - "stair blocks (facing each other)"

    chair:
      - "single stair block"
      - "stair + signs for arms"

    bed:
      - "actual bed blocks"
      - "wool + trapdoors for custom beds"

    kitchen:
      - "furnace + smoker + brewing stand"
      - "cauldron for sink"
      - "trapdoors for cabinets"

  lighting_rules:
    spacing: "Every 8-12 blocks for even lighting"
    hidden_methods:
      - "Glowstone under carpet"
      - "Sea lanterns in floor"
      - "Lanterns on chains"
    decorative:
      - "Chandeliers (fences + lanterns)"
      - "Wall sconces (trapdoor + lantern)"
```

**Benefits**:
- Can furnish interiors
- Proper lighting distribution
- Knows multiple furniture styles

---

## Category 4: Advanced Knowledge 🎓

### A. Biome-Appropriate Building
```yaml
biomes:
  plains:
    natural_materials: ["oak", "grass", "dirt", "stone"]
    suggested_styles: ["farmhouse", "village", "windmill"]

  desert:
    natural_materials: ["sandstone", "terracotta", "sand"]
    suggested_styles: ["pueblo", "egyptian", "arabian"]
    palette: ["sandstone", "smooth_sandstone", "orange_terracotta"]

  snowy_tundra:
    natural_materials: ["spruce", "snow", "ice", "stone"]
    suggested_styles: ["cabin", "nordic", "igloo"]
    palette: ["spruce_planks", "stone_bricks", "snow", "ice"]
```

**Benefits**:
- Builds fit their environment
- Uses locally available materials
- Culturally appropriate styles

### B. Redstone Integration Points
```yaml
redstone_ready:
  doors:
    space_needed: "3 blocks (door + 2 for redstone)"
    mechanisms: ["pressure plate", "button", "lever", "tripwire"]

  lighting:
    automatic: "Daylight sensor circuits"
    manual: "Lever-controlled"

  hidden_entrances:
    piston_door: "2x2 area, 4 blocks depth needed"
    trapdoor: "1x1, minimal space"
```

**Benefits**:
- Leaves room for redstone
- Can suggest automation
- Knows space requirements

### C. Mega-Build Planning
```yaml
mega_builds:
  planning:
    - "Start with outline/foundation"
    - "Build in sections/modules"
    - "Use reference points every 64 blocks"

  organization:
    - "Mark corners with distinct blocks"
    - "Use different materials for measurement"
    - "Save progress as schematics"

  efficiency:
    - "Use //stack for repetitive elements"
    - "Create clipboard library of common parts"
    - "Mirror for symmetrical builds"
```

**Benefits**:
- Can guide large projects
- Knows how to organize huge builds
- Suggests efficient workflows

---

## Category 5: Material Constraints 📊

### A. Resource Availability
```yaml
materials:
  easy_to_gather:
    - dirt
    - cobblestone
    - wood (any)
    - sand
    - gravel

  moderate_effort:
    - iron
    - bricks
    - terracotta
    - quartz

  difficult_to_gather:
    - diamond_blocks
    - netherite_blocks
    - beacon
    - shulker_boxes

  survival_friendly_builds:
    prefer: ["cobblestone", "wood", "stone_bricks", "glass"]
    avoid: ["diamond_blocks", "emerald_blocks", "netherite"]
```

**Benefits**:
- Suggests realistic materials for survival
- Knows what's easily renewable
- Can optimize for resource availability

### B. Performance Considerations
```yaml
performance:
  entity_heavy:
    avoid_excess:
      - item_frames
      - armor_stands
      - hoppers
      - redstone_torches

  light_calculations:
    - "Avoid rapid light level changes"
    - "Use consistent light sources"

  chunk_boundaries:
    - "Avoid building across many chunks"
    - "Redstone may break at boundaries"
```

**Benefits**:
- Creates performant builds
- Knows Minecraft technical limits
- Suggests optimizations

---

## Implementation Ideas

### Format 1: Resource Files (Best for Large Datasets)
```
vibecraft://blocks         - Complete block database
vibecraft://palettes       - Color-organized block lists
vibecraft://styles         - Architectural style guides
vibecraft://techniques     - Building technique library
vibecraft://proportions    - Scale and sizing guides
```

**Pros**:
- Well-organized
- Easy to update
- Can be very comprehensive
- Queryable by Claude

**Cons**:
- Takes tokens when accessed
- Need to prompt Claude to check them

### Format 2: Enhanced CLAUDE.md Sections
Add sections to existing CLAUDE.md:
```markdown
## Block Knowledge
[Curated essential info about common blocks]

## Building Patterns
[Common structure templates]

## Style Guides
[Medieval, modern, etc. quick reference]
```

**Pros**:
- Always loaded
- Zero additional queries
- Integrated with workflow

**Cons**:
- Token cost every session
- Limited space (want to keep CLAUDE.md focused)

### Format 3: Hybrid Approach (RECOMMENDED)
```markdown
CLAUDE.md:
- Core workflow
- Most common blocks (top 50)
- Essential patterns (5-10)
- Quick style guide

Resources:
- vibecraft://blocks (full database)
- vibecraft://patterns (complete library)
- vibecraft://styles (detailed guides)
```

**Pros**:
- Best of both worlds
- Essentials always available
- Deep knowledge on-demand

**Cons**:
- Requires curation (what's "essential"?)

---

## Prioritization

### Tier 1: Highest Impact (Do First)
1. **Common Block Palette** (~50 most-used blocks with colors/uses)
2. **Basic Building Patterns** (walls, roofs, floors)
3. **Style Guide** (Medieval, Modern, Rustic, Fantasy)
4. **Proportion Guidelines** (room sizes, heights, wall thickness)

**Why**: Covers 90% of building scenarios with minimal content.

### Tier 2: High Value (Do Second)
1. **Texture Families** (which blocks work together)
2. **Detailing Techniques** (how to make builds interesting)
3. **Biome-Appropriate Materials** (builds that fit environment)
4. **Interior Furniture Patterns**

**Why**: Elevates builds from basic to professional.

### Tier 3: Nice to Have (Do Later)
1. **Complete Block Database** (all 1000+ blocks)
2. **Advanced Redstone Integration**
3. **Mega-Build Planning**
4. **Performance Optimization**

**Why**: Specialized knowledge for advanced use cases.

---

## Sample Implementation: Essential Blocks

```yaml
# vibecraft://essential-blocks or add to CLAUDE.md

essential_blocks:
  # BUILDING FOUNDATIONS
  stone_blocks:
    - name: cobblestone
      use: "Rustic builds, foundations, medieval"
      color: "gray"
      pairs: ["stone_bricks", "andesite", "oak_planks"]

    - name: stone_bricks
      use: "Refined builds, formal structures"
      color: "gray"
      pairs: ["cobblestone", "oak_planks", "glass"]

  # WOOD VARIETIES
  woods:
    - name: oak_planks
      use: "Default wood, versatile, warm"
      color: "tan/brown"
      variants: ["oak_stairs", "oak_slabs", "oak_fence"]

    - name: dark_oak_planks
      use: "Rich, elegant, formal"
      color: "dark_brown"
      variants: ["dark_oak_stairs", "dark_oak_slabs"]

  # MODERN MATERIALS
  concrete:
    - name: white_concrete
      use: "Modern builds, clean aesthetic"
      color: "pure_white"
      pairs: ["gray_concrete", "glass", "black_concrete"]

    - name: gray_concrete
      use: "Modern builds, neutral base"
      color: "gray"
      pairs: ["white_concrete", "glass"]

  # DECORATIVE
  glass:
    - name: glass
      use: "Windows, modern walls"
      color: "transparent"
      variants: ["glass_panes", "stained_glass (16 colors)"]
```

---

## Creative Ideas

### 1. Building "Recipes"
Like cooking recipes but for structures:
```yaml
recipes:
  small_house:
    difficulty: beginner
    size: "10x10x8"
    materials:
      - oak_planks: "~400 blocks"
      - cobblestone: "~200 blocks"
      - glass_panes: "~50 blocks"
    steps:
      1. "Create 10x10 cobblestone foundation"
      2. "Build oak_planks walls, 6 blocks high"
      3. "Add glass_pane windows (2 blocks high)"
      4. "Create gabled roof with oak_stairs"
      5. "Add door and details"
    worldedit_commands:
      - "//pos1 0,64,0"
      - "//pos2 10,64,10"
      - "//set cobblestone"
      # [etc.]
```

### 2. "Build Vocabulary"
Common Minecraft building terms:
```yaml
vocabulary:
  crenellation: "Battlements - alternating high/low on castle walls"
  gable: "Triangular wall section on peaked roof"
  corbel: "Supporting structure that projects from wall"
  lintel: "Horizontal beam over door/window"
```

### 3. Problem-Solving Database
```yaml
problems:
  - issue: "Build looks flat and boring"
    solutions:
      - "Add depth: inset windows 1 block"
      - "Mix textures: 80/20 primary/accent ratio"
      - "Add protrusions: use stairs/slabs for details"

  - issue: "Rooms feel cramped"
    solutions:
      - "Increase ceiling to 4+ blocks"
      - "Widen doorways"
      - "Use lighter colored blocks"
```

### 4. Inspiration Gallery
Reference existing builds:
```yaml
gallery:
  - name: "Classic Medieval Castle"
    style: medieval
    key_features:
      - "Thick cobblestone walls"
      - "Corner towers with conical roofs"
      - "Central keep"
      - "Drawbridge entrance"
    materials: ["cobblestone", "stone_bricks", "oak", "spruce"]

  - name: "Modern Villa"
    style: modern
    key_features:
      - "Clean white concrete exterior"
      - "Floor-to-ceiling glass windows"
      - "Flat roof with garden"
      - "Geometric shapes"
    materials: ["white_concrete", "glass", "gray_concrete"]
```

---

## Recommendation

**Start with Tier 1 + Hybrid Approach**:

1. **Add to CLAUDE.md** (always loaded):
   - Top 30-50 blocks with uses and color info
   - 5-10 essential building patterns
   - Quick style guide (Medieval, Modern, Rustic basics)
   - Basic proportion rules

2. **Create Resources** (on-demand):
   - `vibecraft://blocks` - Full block database
   - `vibecraft://patterns` - Complete pattern library
   - `vibecraft://styles` - Detailed style guides
   - `vibecraft://techniques` - Advanced methods

3. **Prompt Claude to check resources** when:
   - User asks about specific blocks
   - Building in a particular style
   - Needs advanced techniques

This gives Claude essential knowledge immediately while keeping comprehensive references available!

Would you like me to start implementing any of these? I'd suggest starting with the essential blocks list for CLAUDE.md!
