# VibeCraft Complete Setup Guide

**End-to-End Instructions for AI-Powered Building in Minecraft**

This guide walks you through the complete setup process, from Minecraft server to AI integration.

---

## Overview

VibeCraft consists of three components:
1. **Minecraft Server** with WorldEdit plugin
2. **VibeCraft MCP Server** (RCON bridge)
3. **AI Client** (Claude Code, Claude Desktop, or Cursor)

**Estimated Setup Time:** 30-60 minutes

---

## Part 1: Minecraft Server Setup

Follow the detailed guide at: `docs/MINECRAFT_SERVER_SETUP.md`

**Quick Checklist:**
- [ ] Java 21+ installed
- [ ] PaperMC 1.21.x downloaded
- [ ] Server started and EULA accepted
- [ ] RCON enabled in server.properties
- [ ] WorldEdit 7.3+ installed in plugins/
- [ ] Operator permissions granted
- [ ] RCON connection tested with mcrcon

**Test Command:**
```bash
mcrcon -H localhost -P 25575 -p YOUR_PASSWORD "list"
```

---

## Part 2: VibeCraft MCP Server Setup

### Step 1: Navigate to MCP Server Directory

```bash
cd /Users/er/Repos/vibecraft/mcp-server
```

### Step 2: Run Setup Script

```bash
./setup.sh
```

This will:
- Verify Python 3.10+ is installed
- Create virtual environment
- Install dependencies
- Create `.env` file from template

### Step 3: Configure Environment

Edit `.env` file with your settings:

```bash
nano .env
```

**Critical Settings:**
```bash
VIBECRAFT_RCON_HOST=127.0.0.1
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=your_actual_rcon_password_here
```

**Optional Safety Settings:**
```bash
# Restrict build area (coordinates)
VIBECRAFT_BUILD_MIN_X=0
VIBECRAFT_BUILD_MAX_X=500
VIBECRAFT_BUILD_MIN_Y=-64
VIBECRAFT_BUILD_MAX_Y=319
VIBECRAFT_BUILD_MIN_Z=0
VIBECRAFT_BUILD_MAX_Z=500
```

Save and exit (Ctrl+X, Y, Enter).

### Step 4: Test MCP Server

```bash
# Activate virtual environment
source venv/bin/activate

# Run server
python -m src.vibecraft.server
```

**Expected Output:**
```
============================================================
🎮 VibeCraft MCP Server Starting...
============================================================
RCON Host: 127.0.0.1:25575
Safety Checks: Enabled
Dangerous Commands: Blocked
Testing RCON connection...
✅ RCON connection successful!
✅ WorldEdit 7.3.10 detected
============================================================
🚀 VibeCraft MCP Server Ready!
   AI can now build in Minecraft using WorldEdit commands
============================================================
```

If successful, press Ctrl+C to stop the test. The server is ready!

**Troubleshooting:**
- **Connection refused**: Minecraft server not running
- **Authentication failed**: Wrong RCON password
- **WorldEdit not detected**: Plugin not installed or loaded

---

## Part 3: AI Client Integration

Choose your AI client and follow the appropriate instructions:

### Option A: Claude Code

**Location:** Claude Code MCP settings

1. Open Claude Code settings
2. Navigate to MCP Servers configuration
3. Add VibeCraft server:

```json
{
  "mcpServers": {
    "vibecraft": {
      "command": "python",
      "args": ["-m", "src.vibecraft.server"],
      "cwd": "/Users/er/Repos/vibecraft/mcp-server",
      "env": {
        "VIBECRAFT_RCON_HOST": "127.0.0.1",
        "VIBECRAFT_RCON_PORT": "25575",
        "VIBECRAFT_RCON_PASSWORD": "YOUR_PASSWORD_HERE"
      }
    }
  }
}
```

4. Restart Claude Code
5. Verify tools appear in available tools list

### Option B: Claude Desktop

**Location:** `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

1. Edit configuration file:

```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. Add VibeCraft server:

```json
{
  "mcpServers": {
    "vibecraft": {
      "command": "/Users/er/Repos/vibecraft/mcp-server/venv/bin/python",
      "args": ["-m", "src.vibecraft.server"],
      "cwd": "/Users/er/Repos/vibecraft/mcp-server",
      "env": {
        "VIBECRAFT_RCON_HOST": "127.0.0.1",
        "VIBECRAFT_RCON_PORT": "25575",
        "VIBECRAFT_RCON_PASSWORD": "YOUR_PASSWORD_HERE"
      }
    }
  }
}
```

**Note:** Use full path to Python in venv for Claude Desktop!

3. Restart Claude Desktop
4. Check that VibeCraft tools are available

### Option C: Cursor

**Location:** `.cursor/mcp.json` in your project

1. Create/edit `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "vibecraft": {
      "command": "python",
      "args": ["-m", "src.vibecraft.server"],
      "cwd": "/Users/er/Repos/vibecraft/mcp-server",
      "env": {
        "VIBECRAFT_RCON_HOST": "127.0.0.1",
        "VIBECRAFT_RCON_PORT": "25575",
        "VIBECRAFT_RCON_PASSWORD": "YOUR_PASSWORD_HERE"
      }
    }
  }
}
```

2. Restart Cursor
3. Verify VibeCraft tools appear

---

## Part 4: Testing the Complete System

### Test 1: Server Information

Ask your AI:
```
"Get information about the Minecraft server"
```

AI should use `get_server_info` tool and return server details.

### Test 2: Simple Build

Ask your AI:
```
"Create a 10x10x10 cube of stone at coordinates 100, 64, 100"
```

AI should:
1. Use `worldedit_selection` to set pos1 and pos2
2. Use `worldedit_region` to fill with stone
3. Confirm completion

**Verify in Minecraft:** Join your server and teleport to 100, 64, 100. You should see a stone cube!

```bash
/tp @p 100 64 100
```

### Test 3: Complex Structure

Ask your AI:
```
"Build a small house at 200, 64, 200. Use oak planks for walls, stone bricks for floor, and oak stairs for the roof. Make it 10x8x10 blocks."
```

AI should:
1. Set the region
2. Create floor with stone bricks
3. Create walls with oak planks
4. Make it hollow
5. Add roof with stairs

**Verify in Minecraft:** The house should appear at the coordinates!

### Test 4: Undo/Redo

Ask your AI:
```
"Undo the last build"
```

The structure should disappear (WorldEdit undo).

```
"Redo it"
```

The structure should reappear!

---

## Part 5: Understanding Available Tools

VibeCraft provides 14 tools organized in 3 tiers:

### Tier 1: Generic RCON (1 tool)
- `rcon_command` - Execute any command

### Tier 2: WorldEdit Categories (9 tools)
- `worldedit_selection` - Region selection
- `worldedit_region` - Region modifications
- `worldedit_generation` - Shape generation
- `worldedit_clipboard` - Copy/paste
- `worldedit_schematic` - File operations
- `worldedit_history` - Undo/redo
- `worldedit_utility` - Utilities
- `worldedit_biome` - Biome operations
- `worldedit_brush` - Brush tools

### Tier 3: Helpers (4 tools)
- `validate_pattern` - Check pattern syntax
- `validate_mask` - Check mask syntax
- `get_server_info` - Server status
- `calculate_region_size` - Size calculations

### Documentation Resources (6 resources)
- Pattern syntax guide
- Mask syntax guide
- Expression syntax guide
- Coordinate system guide
- Common workflows
- Player context warnings

---

## Part 6: Best Practices for AI Building

### 1. Always Set Positions First

```
"Set position 1 to 100, 64, 100 and position 2 to 120, 80, 120"
```

### 2. Use Appropriate Tools

For simple blocks:
```
"Fill the region with stone"  → worldedit_region
```

For shapes:
```
"Create a sphere of glass with radius 10"  → worldedit_generation
```

### 3. Work in Phases

Complex builds:
```
1. "Create the foundation"
2. "Build the walls"
3. "Add the roof"
4. "Add details and decorations"
```

### 4. Use Undo if Needed

```
"That doesn't look right, undo it and try again"
```

### 5. Save Good Structures

```
"Copy this structure and save it as 'my_house'"
```

---

## Part 7: Safety and Limits

### Command Safety

VibeCraft now allows all WorldEdit commands, including high-impact actions:
- `//regen` - World regeneration
- `//delchunks` - Chunk deletion
- `/stop` - Server stop
- Large limits (>1M blocks)

**Need stricter safety?** Set `VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=false` to restore blocking.

### Coordinate Bounds

Restrict building area in `.env`:
```bash
VIBECRAFT_BUILD_MIN_X=0
VIBECRAFT_BUILD_MAX_X=1000
...
```

Commands outside bounds will be rejected.

### Operation Limits

WorldEdit has built-in limits:
- Default: 1,000,000 blocks per operation
- Configurable in WorldEdit config

For large operations, AI should break into smaller chunks.

---

## Part 8: Troubleshooting

### Problem: "RCON connection failed"

**Cause:** Server not reachable

**Solutions:**
1. Ensure Minecraft server is running
2. Verify RCON password in `.env`
3. Check `server.properties` has `enable-rcon=true`
4. Test with `mcrcon` CLI tool

### Problem: "WorldEdit not detected"

**Cause:** Plugin not loaded

**Solutions:**
1. Check `plugins/` directory has `worldedit.jar`
2. Restart Minecraft server
3. Run `/version WorldEdit` in-game to verify
4. Check server logs for errors

### Problem: "Command executed but nothing happened"

**Cause:** Player context or syntax error

**Solutions:**
1. Use comma-separated coordinates: `//pos1 100,64,100`
2. Check command syntax in WorldEdit docs
3. Some commands need player - use alternatives
4. Verify you're an operator: `/op yourusername`

### Problem: "Permission denied" errors

**Cause:** Not an operator or insufficient permissions

**Solutions:**
1. Give yourself operator: `/op yourusername`
2. Check `ops.json` file
3. Verify WorldEdit permissions in config

### Problem: AI tools not appearing

**Cause:** MCP server not connected

**Solutions:**
1. Check MCP configuration file is correct
2. Verify paths are absolute (for Claude Desktop)
3. Check AI client logs for errors
4. Restart AI client
5. Test MCP server runs standalone

---

## Part 9: Advanced Configuration

### Custom Build Zones

Define multiple zones with different permissions:
```bash
# Zone 1: Spawn area (protected)
VIBECRAFT_BUILD_MIN_X=-100
VIBECRAFT_BUILD_MAX_X=100
...

# Zone 2: Creative area (full access)
# Use separate configuration or disable bounds
```

### Performance Tuning

For large operations:
```bash
# Increase timeout
VIBECRAFT_RCON_TIMEOUT=30

# WorldEdit config (plugins/WorldEdit/config.yml)
limits:
  max-blocks-changed:
    default: 5000000
```

### Logging and Debugging

Enable detailed logging:
```bash
VIBECRAFT_ENABLE_COMMAND_LOGGING=true
```

View logs in terminal where MCP server runs.

---

## Part 10: Next Steps

### Learn WorldEdit

Read documentation:
- `docs/RESEARCH_WORLDEDIT_COMPLETE.md` - Complete command reference
- https://worldedit.enginehub.org/ - Official docs

### Experiment with Patterns

Try different patterns:
```
"Set the region to 50% stone, 30% cobblestone, 20% andesite"
"Replace all stone with random wool colors"
"Fill with oak stairs facing north"
```

### Build Complex Structures

Challenge the AI:
```
"Build a medieval castle with towers and walls"
"Create a modern house with glass walls and a pool"
"Generate a natural-looking mountain terrain"
```

### Save Your Creations

```
"Copy this structure and save it as 'my_awesome_build'"
```

Later:
```
"Load 'my_awesome_build' and paste it at coordinates X, Y, Z"
```

---

## Appendix A: Command Reference Quick Sheet

### Selection
```
//pos1 X,Y,Z     - Set corner 1
//pos2 X,Y,Z     - Set corner 2
//expand <amt>   - Expand selection
//size           - Get selection info
```

### Region Operations
```
//set <pattern>           - Fill with pattern
//replace <from> <to>     - Replace blocks
//walls <pattern>         - Build walls
//hollow                  - Hollow out
//move <distance> <dir>   - Move contents
//stack <count> <dir>     - Stack/repeat
```

### Shapes
```
//sphere <pattern> <radius>       - Sphere
//cyl <pattern> <radius> [height] - Cylinder
//pyramid <pattern> <size>        - Pyramid
```

### Clipboard
```
//copy          - Copy selection
//cut           - Cut selection
//paste         - Paste
//rotate <deg>  - Rotate
//flip [dir]    - Flip
```

### History
```
//undo [times]  - Undo
//redo [times]  - Redo
```

---

## Appendix B: Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `VIBECRAFT_RCON_HOST` | 127.0.0.1 | RCON host |
| `VIBECRAFT_RCON_PORT` | 25575 | RCON port |
| `VIBECRAFT_RCON_PASSWORD` | minecraft | RCON password |
| `VIBECRAFT_RCON_TIMEOUT` | 10 | Command timeout (seconds) |
| `VIBECRAFT_ENABLE_SAFETY_CHECKS` | true | Enable validation |
| `VIBECRAFT_ALLOW_DANGEROUS_COMMANDS` | true | Allow risky commands (set false to block) |
| `VIBECRAFT_MAX_COMMAND_LENGTH` | 1000 | Max command length |
| `VIBECRAFT_BUILD_MIN_X` | None | Min X coordinate |
| `VIBECRAFT_BUILD_MAX_X` | None | Max X coordinate |
| `VIBECRAFT_BUILD_MIN_Y` | None | Min Y coordinate |
| `VIBECRAFT_BUILD_MAX_Y` | None | Max Y coordinate |
| `VIBECRAFT_BUILD_MIN_Z` | None | Min Z coordinate |
| `VIBECRAFT_BUILD_MAX_Z` | None | Max Z coordinate |
| `VIBECRAFT_ENABLE_VERSION_DETECTION` | true | Detect WorldEdit version |
| `VIBECRAFT_ENABLE_COMMAND_LOGGING` | true | Log commands |

---

## Appendix C: File Locations

### macOS
```
Claude Desktop Config: ~/Library/Application Support/Claude/claude_desktop_config.json
Minecraft Server: /Users/er/Repos/vibecraft/minecraft-server/
MCP Server: /Users/er/Repos/vibecraft/mcp-server/
```

### Linux
```
Claude Desktop Config: ~/.config/Claude/claude_desktop_config.json
Minecraft Server: /path/to/vibecraft/minecraft-server/
MCP Server: /path/to/vibecraft/mcp-server/
```

---

## Support

- 📚 Documentation: `docs/` directory
- 🐛 Issues: Report problems with detailed logs
- 💡 Examples: See `docs/RESEARCH_WORLDEDIT_COMPLETE.md`

---

**Congratulations! 🎉**

You now have a fully functional AI-powered building system for Minecraft. Start creating amazing structures with just natural language commands!

**Happy Building! 🏗️**
