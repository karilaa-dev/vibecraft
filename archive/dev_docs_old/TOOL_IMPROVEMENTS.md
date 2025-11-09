# VibeCraft Tool Improvements

## Analysis: Why Claude May Not Use Tools Effectively

### Current Strengths ✅
1. Tool descriptions have examples
2. Parameter schemas are clear
3. Resources are comprehensive
4. Safety features documented

### Identified Gaps ❌
1. **No workflow context** - Tools exist in isolation
2. **No decision guidance** - When to use which tool unclear
3. **Resource discoverability** - Claude may not know to check resources
4. **Single-step focus** - Multi-step patterns not explicit
5. **No anti-patterns** - What NOT to do isn't clear

## Solution: Hybrid Approach

### 1. System Prompt (CLAUDE.md) ✅ COMPLETED
**Purpose**: Provide high-level context and workflow

**Benefits**:
- Defines role clearly
- Shows common task patterns
- Explains tool selection strategy
- Guides multi-step building
- Zero code changes needed

**Cost**: ~1500 tokens per session (loaded once)

**Created**: `/Users/er/Repos/vibecraft/CLAUDE.md`

### 2. Enhanced Tool Descriptions (RECOMMENDED NEXT)
**Purpose**: Improve individual tool usage

**Key Improvements Needed**:

#### A. Add Workflow Context to Each Tool
```python
# Example: worldedit_selection
description="""WorldEdit Selection Commands - Define your build area.

⭐ TYPICAL WORKFLOW:
1. Use this tool FIRST to define your building area
2. Then use worldedit_region or worldedit_generation to modify
3. Finally verify with //size or get_server_info

🔗 RELATED TOOLS:
- After selection → worldedit_region (modify blocks)
- After selection → worldedit_generation (create shapes)
- To verify → worldedit_selection //size

[rest of description...]
"""
```

#### B. Add Multi-Step Examples
```python
# Example: worldedit_region
description="""...

📋 MULTI-STEP EXAMPLES:

Building a house:
1. worldedit_selection: //pos1 100,64,100
2. worldedit_selection: //pos2 120,74,120
3. worldedit_region: //walls stone_bricks
4. worldedit_region: //faces oak_planks

Creating terrain:
1. worldedit_selection: //pos1 0,64,0 → //pos2 100,100,100
2. worldedit_generation: //generate stone y<70
3. worldedit_region: //smooth 3
4. worldedit_region: //naturalize

[rest of description...]
"""
```

#### C. Add Decision Guidance
```python
# Example: rcon_command
description="""...

⚙️ WHEN TO USE THIS TOOL:
✅ Custom commands not covered by other tools
✅ Minecraft server commands (time, weather, gamemode)
✅ Testing new WorldEdit commands
✅ Direct control needed

❌ DON'T USE THIS TOOL FOR:
❌ Basic WorldEdit - use specialized tools (better descriptions)
❌ Pattern validation - use validate_pattern tool
❌ Server info - use get_server_info tool

[rest of description...]
"""
```

#### D. Add Resource Hints
```python
# Example: worldedit_region
description="""...

📚 SYNTAX HELP:
- Complex patterns? Check resource: vibecraft://patterns
- Need masks? Check resource: vibecraft://masks
- Using expressions? Check resource: vibecraft://expressions

Examples of when to check resources:
- Before: //set 50%stone,30%dirt → Check patterns resource
- Before: //replace #existing stone → Check masks resource
- Before: //generate stone y<64 → Check expressions resource

[rest of description...]
"""
```

### 3. Additional Recommended Improvements

#### A. Helper Tool Enhancement
Make helper tools more discoverable:

```python
Tool(
    name="validate_pattern",
    description="""Validate a WorldEdit pattern before using it in large operations.

⭐ USE THIS BEFORE BIG OPERATIONS!

When to use:
- Before //set on large selection (>1000 blocks)
- When using complex patterns (percentages, categories)
- If unsure about pattern syntax

Example workflow:
1. validate_pattern "50%stone,30%dirt,20%grass_block"
2. If valid → worldedit_region //set 50%stone,30%dirt,20%grass_block
3. If invalid → Check vibecraft://patterns resource

This saves you from //undo on massive mistakes!
""",
    [rest...]
)
```

#### B. Add "Getting Started" Resource
New resource that provides quick-start guide:

```python
GETTING_STARTED_GUIDE = """# VibeCraft Quick Start

## First Time Using WorldEdit?

### 3-Step Process for Any Build:
1. **SELECT** - Define the area (worldedit_selection)
2. **MODIFY** - Change blocks (worldedit_region or worldedit_generation)
3. **VERIFY** - Check results (get_server_info or //size)

### Your First Structure:
1. //pos1 100,64,100       (worldedit_selection)
2. //pos2 110,74,110       (worldedit_selection)
3. //set stone_bricks      (worldedit_region)
4. //size                  (worldedit_selection - verify)

Done! You just built a 10x10x10 cube.

### Common Mistakes to Avoid:
❌ Using spaces in coordinates: //pos1 100 64 100 (WRONG)
✅ Use commas: //pos1 100,64,100 (CORRECT)

❌ Forgetting to set selection before //set (ERROR)
✅ Always //pos1 and //pos2 first

❌ Not checking pattern syntax (WASTED TIME)
✅ Use validate_pattern or check resources

### Need Help?
- Pattern syntax → vibecraft://patterns
- Mask syntax → vibecraft://masks
- All coordinates → vibecraft://coordinates
"""
```

## Implementation Priority

### Phase 1: Zero-Code (COMPLETED ✅)
- [x] Create CLAUDE.md with role context and workflow
- [x] Document tool usage patterns
- [x] Provide decision tree for tool selection

### Phase 2: Tool Description Enhancements (RECOMMENDED)
- [ ] Add workflow context to each tool (⭐ FIRST)
- [ ] Add multi-step examples (⭐ NEXT)
- [ ] Add resource hints to relevant tools
- [ ] Add decision guidance (when to use/not use)

### Phase 3: Code Improvements (OPTIONAL)
- [ ] Add "getting started" resource
- [ ] Enhance helper tool descriptions
- [ ] Consider renaming tools for clarity
- [ ] Add tool relationship metadata

## Expected Impact

### With CLAUDE.md Only (Current State)
- ✅ Better understanding of role and capabilities
- ✅ Clear workflow patterns for common tasks
- ✅ Tool selection guidance
- ⚠️ Still requires Claude to discover tool relationships
- **Estimated Improvement**: 40-50%

### With Enhanced Tool Descriptions (Recommended)
- ✅ All above benefits
- ✅ Workflow context in every tool
- ✅ Multi-step examples readily available
- ✅ Resource hints at point of use
- ✅ Clear decision guidance per tool
- **Estimated Improvement**: 70-80%

### With Full Implementation (Optional)
- ✅ All above benefits
- ✅ Beginner-friendly quick start
- ✅ Tool relationships explicit
- ✅ Perfect for any AI model
- **Estimated Improvement**: 90%+

## Recommendation

**Start with CLAUDE.md (Done)**, then if Claude still struggles, enhance tool descriptions in Phase 2.

The beauty of CLAUDE.md is:
- Zero code changes
- No reinstall needed
- Easy to iterate
- Immediate effect
- User can customize it

Tool description improvements are more permanent and scalable, but require code changes and testing.

## Testing Strategy

1. **Test with CLAUDE.md first** (current state)
2. **Observe which tools Claude struggles with**
3. **Enhance those specific tool descriptions**
4. **Iterate based on real usage patterns**

This data-driven approach ensures we optimize where it matters most.
