# Post-Setup Verification Checklist

Verify your VibeCraft installation is working correctly.

## Quick Verification (2 minutes)

Run these tests immediately after setup:

### ✅ 1. Server Starts

```bash
cd mcp-server
uv run python -m src.vibecraft.server
```

**Expected Output**:
```
=============================================================
🎮 VibeCraft MCP Server Starting...
=============================================================
RCON Host: 127.0.0.1:25575
Safety Checks: Enabled
Dangerous Commands: Allowed
Testing RCON connection...
✅ RCON connection successful!
✅ WorldEdit 7.3.0 detected
=============================================================
🚀 VibeCraft MCP Server Ready!
   AI can now build in Minecraft using WorldEdit commands
=============================================================
```

**If you see** ✅ **all green checkmarks → PASS**
**If you see** ❌ **errors → See [Troubleshooting](#troubleshooting)**

---

### ✅ 2. MCP Client Detects Tools

**Claude Code**:
1. Open project in Claude Code
2. Press Cmd+Shift+P (macOS) / Ctrl+Shift+P (Windows/Linux)
3. Type "MCP" → Select "MCP: List Tools"
4. Look for VibeCraft tools

**Expected**: See 52 VibeCraft tools listed:
- rcon_command
- worldedit_selection
- worldedit_region
- ... (49 more)

**If tools appear → PASS**
**If no tools → See [MCP Client Issues](#mcp-client-issues)**

---

### ✅ 3. Basic Command Works

Ask Claude (or your AI):
```
Can you execute this WorldEdit command for me:
//version WorldEdit
```

**Expected Response**:
```
Command executed: //version WorldEdit
Output: WorldEdit version 7.3.0
```

**If command works → PASS**
**If error → See [Command Issues](#command-issues)**

---

## Comprehensive Verification (10 minutes)

Full test suite to verify all components:

### Test 1: Configuration File

**Check**:
```bash
cat mcp-server/.env
```

**Verify**:
- [ ] File exists
- [ ] Contains `VIBECRAFT_RCON_HOST`
- [ ] Contains `VIBECRAFT_RCON_PORT`
- [ ] Contains `VIBECRAFT_RCON_PASSWORD`
- [ ] Password matches Minecraft `server.properties`
- [ ] No extra spaces or quotes around values

**Fix**: See [RCON_PASSWORD_SETUP.md](./RCON_PASSWORD_SETUP.md)

---

### Test 2: Minecraft Server RCON

**Check**:
```bash
# Install mcrcon if not already installed
brew install mcrcon  # macOS
# or: sudo apt-get install mcrcon  # Linux

# Test RCON connection
mcrcon -H 127.0.0.1 -P 25575 -p "your_password" "list"
```

**Expected Output**:
```
There are 1 of a max of 20 players online: YourUsername
```

**Verify**:
- [ ] Connection succeeds
- [ ] Lists current players
- [ ] No "authentication failed" error

**Fix**: See [CONFIGURATION.md § RCON Connection](./CONFIGURATION.md#rcon-connection)

---

### Test 3: WorldEdit Installed

**In Minecraft console** or via mcrcon:
```
/version WorldEdit
```

**Expected Output**:
```
WorldEdit version 7.3.0
```

**Verify**:
- [ ] WorldEdit is installed
- [ ] Version is compatible (7.2+)

**Fix**:
```bash
# Download WorldEdit for your Minecraft version:
# https://dev.bukkit.org/projects/worldedit

# Install in server:
cp WorldEdit-X.X.X.jar server/plugins/
# Restart Minecraft server
```

---

### Test 4: MCP Server Connection

**Run**:
```bash
cd mcp-server
uv run python -m src.vibecraft.server 2>&1 | tee test.log
```

**Expected in test.log**:
```
✅ RCON connection successful!
✅ WorldEdit 7.3.0 detected
🚀 VibeCraft MCP Server Ready!
```

**Verify**:
- [ ] No "Connection refused" errors
- [ ] No "Authentication failed" errors
- [ ] WorldEdit version detected
- [ ] Server reaches "Ready!" state

**Save** `test.log` for troubleshooting if needed

**Fix**: See [Troubleshooting](#troubleshooting)

---

### Test 5: Basic WorldEdit Commands

**Ask Claude/AI**:
```
Execute these WorldEdit commands:

1. Check current position: //pos
2. Set a position: //pos1 100,64,100
3. Create a small test: //set stone
4. Undo: //undo
```

**Expected**:
```
✅ //pos → Returns your current position
✅ //pos1 100,64,100 → "First position set to..."
✅ //set stone → "X blocks changed"
✅ //undo → "Undid X block changes"
```

**Verify**:
- [ ] Position commands work
- [ ] Set command creates blocks in Minecraft
- [ ] Undo reverts changes
- [ ] No permission errors

**Fix**: See [Command Issues](#command-issues)

---

### Test 6: Advanced Tools

**Ask Claude/AI**:
```
1. Search for an item: search_minecraft_item("diamond")
2. Get player position: get_player_position()
3. Get surface level: get_surface_level(x=100, z=100)
```

**Expected**:
```
✅ search_minecraft_item → Lists diamond blocks/items
✅ get_player_position → Returns coordinates, rotation, etc.
✅ get_surface_level → Returns surface Y coordinate
```

**Verify**:
- [ ] Item search returns results
- [ ] Player position includes coordinates
- [ ] Surface level returns valid Y value

**Fix**: See [Advanced Tool Issues](#advanced-tool-issues)

---

### Test 7: Pattern Library

**Ask Claude/AI**:
```
1. Browse patterns: building_pattern_lookup(action="browse")
2. Get a pattern: building_pattern_lookup(action="get", pattern_id="gable_oak_medium")
```

**Expected**:
```
✅ browse → Lists 29 building patterns
✅ get → Returns pattern with layers, materials, dimensions
```

**Verify**:
- [ ] Pattern list appears
- [ ] Pattern retrieval works
- [ ] Pattern includes layer data

**Fix**: Context files missing → Re-run setup

---

### Test 8: Furniture System

**Ask Claude/AI**:
```
1. Search furniture: furniture_lookup(action="search", category="bedroom")
2. Get furniture: furniture_lookup(action="get", furniture_id="simple_bed")
```

**Expected**:
```
✅ search → Lists bedroom furniture
✅ get → Returns furniture with build instructions
```

**Verify**:
- [ ] Furniture categories work
- [ ] Furniture details load
- [ ] Instructions are present

**Fix**: Context files missing → Re-run setup

---

### Test 9: Spatial Awareness

**Ask Claude/AI**:
```
Scan this area:
spatial_awareness_scan(center_x=100, center_y=65, center_z=200, radius=5, detail_level="medium")
```

**Expected**:
```
✅ Returns floor_y, ceiling_y, clearance, recommendations
```

**Verify**:
- [ ] Scan completes without errors
- [ ] Returns floor and ceiling coordinates
- [ ] Provides placement recommendations

**Fix**: RCON timing issues → Increase timeout

---

### Test 10: Terrain Analysis

**Ask Claude/AI**:
```
Analyze this terrain:
terrain_analyzer(x1=0, y1=60, z1=0, x2=100, y2=80, z2=100, resolution=5)
```

**Expected**:
```
✅ Returns elevation, composition, hazards, opportunities
```

**Verify**:
- [ ] Analysis completes (may take 10-30 seconds)
- [ ] Returns terrain type, elevation stats
- [ ] Provides building recommendations

**Fix**: RCON timeout → Increase `VIBECRAFT_RCON_TIMEOUT`

---

## Test Checklist Summary

**Quick Tests** (✅ = Pass):
- [ ] Server starts without errors
- [ ] MCP client shows 52 tools
- [ ] Basic command executes

**Comprehensive Tests**:
- [ ] 1. Configuration file correct
- [ ] 2. RCON connection works
- [ ] 3. WorldEdit installed
- [ ] 4. MCP server connects
- [ ] 5. Basic WorldEdit commands
- [ ] 6. Advanced tools (search, position, surface)
- [ ] 7. Pattern library
- [ ] 8. Furniture system
- [ ] 9. Spatial awareness
- [ ] 10. Terrain analysis

**All 13 tests pass?** → ✅ **Setup verified!**

---

## Troubleshooting

### RCON Connection Failed

**Symptoms**:
```
❌ RCON connection test failed
Connection refused / Authentication failed
```

**Fixes**:

1. **Check Minecraft server running**:
   ```bash
   # Check process
   ps aux | grep java
   # Should show Minecraft server
   ```

2. **Verify RCON enabled** in `server.properties`:
   ```properties
   enable-rcon=true
   rcon.port=25575
   rcon.password=your_password_here
   ```

3. **Restart Minecraft server**:
   ```bash
   # Stop server (in Minecraft console):
   stop
   # Start server again
   ./start.sh
   ```

4. **Test RCON manually**:
   ```bash
   mcrcon -H 127.0.0.1 -P 25575 -p "your_password" "list"
   ```

5. **Check firewall**:
   ```bash
   telnet 127.0.0.1 25575
   # Should connect (Ctrl+C to exit)
   ```

**Still failing?** → [CONFIGURATION.md § Troubleshooting](./CONFIGURATION.md#troubleshooting)

---

### MCP Client Issues

**Symptoms**:
- VibeCraft tools don't appear
- MCP server not starting
- "Failed to start MCP server" error

**Fixes**:

1. **Check MCP config location**:
   - Claude Code: `.claude/mcp.json` in project
   - Claude Desktop: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
   - Cursor: `.cursor/mcp.json` in project

2. **Verify config syntax**:
   ```json
   {
     "mcpServers": {
       "vibecraft": {
         "command": "uv",
         "args": ["run", "python", "-m", "src.vibecraft.server"],
         "cwd": "/absolute/path/to/vibecraft/mcp-server",
         "env": {
           "VIBECRAFT_RCON_HOST": "127.0.0.1",
           "VIBECRAFT_RCON_PORT": "25575",
           "VIBECRAFT_RCON_PASSWORD": "your_password_here"
         }
       }
     }
   }
   ```

3. **Check paths are absolute**:
   ```bash
   # Get absolute path
   cd /path/to/vibecraft/mcp-server
   pwd
   # Copy this path to MCP config "cwd"
   ```

4. **Restart MCP client**:
   - Claude Code: Restart VS Code
   - Claude Desktop: Quit and reopen app
   - Cursor: Restart Cursor

5. **Check MCP server logs**:
   ```bash
   # For Claude Code/Cursor, check VS Code output
   # For Claude Desktop, check system logs
   tail -f ~/Library/Logs/Claude/mcp-*.log  # macOS
   ```

---

### Command Issues

**Symptoms**:
- Commands execute but nothing happens
- "You don't have permission" errors
- Syntax errors

**Fixes**:

1. **Verify operator status**:
   ```bash
   # In Minecraft console:
   /op YourUsername
   ```

2. **Use console syntax** (comma-separated coordinates):
   ```
   ❌ Wrong: //pos1 100 64 100
   ✅ Right: //pos1 100,64,100
   ```

3. **Check WorldEdit permissions**:
   ```bash
   # Check plugins/WorldEdit/config.yml
   # Ensure use-in-creative: true or permissions set
   ```

4. **Test command manually**:
   ```bash
   # Via mcrcon
   mcrcon -H 127.0.0.1 -P 25575 -p "password" "//version WorldEdit"
   ```

---

### Advanced Tool Issues

**Symptoms**:
- search_minecraft_item returns empty
- get_player_position fails
- Pattern/furniture lookup empty

**Fixes**:

1. **Check context files exist**:
   ```bash
   ls -lah context/
   # Should show:
   # minecraft_items_filtered.json
   # building_patterns_complete.json
   # terrain_patterns_complete.json
   # minecraft_furniture_layouts.json
   # etc.
   ```

2. **Re-run setup** (regenerates context):
   ```bash
   ./setup-all.sh
   ```

3. **Check file permissions**:
   ```bash
   chmod -R 644 context/*.json
   ```

---

## Performance Benchmarks

**Normal Performance**:
- Server startup: < 5 seconds
- Basic command: < 1 second
- Pattern lookup: < 1 second
- Spatial scan (medium): 4-6 seconds
- Terrain analysis (100×100): 15-30 seconds

**If slower**:
- Increase `VIBECRAFT_RCON_TIMEOUT`
- Check network latency (for remote servers)
- Reduce terrain analysis resolution

---

## Next Steps

**Setup verified?** ✅

Now:
1. **Read**: [CONFIGURATION.md](./CONFIGURATION.md) - Optimize your settings
2. **Read**: [SERVER_MODE_GUIDE.md](./SERVER_MODE_GUIDE.md) - Choose right mode
3. **Build**: Ask your AI to build something!

**Example prompts**:
```
"Build me a 10×10 stone castle at coordinates 100, 64, 100"
"Create a natural hilly landscape at my current location"
"Place a dining table in this room at X=150, Z=200"
```

---

## Support

**Need help?**
- 🐛 [Report Issues](https://github.com/amenti-labs/vibecraft/issues)
- 💬 [GitHub Discussions](https://github.com/amenti-labs/vibecraft/discussions)
- 📖 [Full Documentation](./README.md)

**Include in bug reports**:
- Output of verification tests
- Server startup log
- MCP client logs
- Minecraft version
- WorldEdit version

---

**Last Updated**: November 9, 2025
