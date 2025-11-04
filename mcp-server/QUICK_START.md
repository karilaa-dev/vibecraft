# VibeCraft MCP Server - Quick Start

## TL;DR

```bash
cd mcp-server
./run_fastmcp.sh
# Choose option 2 for HTTP/SSE (41 tools, debug logs)
# Choose option 1 for stdio (41 tools, no logs)
```

Then connect Claude to: `http://127.0.0.1:8765/sse`

---

## Two Server Modes

### Mode 1: stdio (Standard)
- **Best for**: Single Claude instance
- **Tools**: All 41 tools ✅
- **Logs**: Hidden (run by Claude)
- **Multiple clients**: ❌ No
- **Command**: `uv run python __main__.py`

### Mode 2: HTTP/SSE (Shared) ⭐ RECOMMENDED
- **Best for**: Multiple Claude instances, debugging
- **Tools**: All 41 tools ✅
- **Logs**: Visible in terminal ✅
- **Multiple clients**: ✅ Yes
- **Command**: `uv run python server_http.py --port 8765`

---

## Running the Server

### Option A: Interactive Script (Easiest)
```bash
cd mcp-server
./run_fastmcp.sh
```

Choose:
- `1` for stdio (single instance, no logs)
- `2` for HTTP/SSE (multi-instance, with logs)

### Option B: Direct Command (HTTP/SSE)
```bash
cd mcp-server
/Users/er/.pyenv/versions/3.11.11/bin/uv run python server_http.py --port 8765
```

### Option C: Convenience Script (HTTP/SSE)
```bash
cd mcp-server
./start-vibecraft.sh
```

---

## Connecting Claude

### Claude Desktop
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "vibecraft": {
      "url": "http://127.0.0.1:8765/sse"
    }
  }
}
```

### Claude Code
Already configured in `.mcp.json` at project root:
```json
{
  "mcpServers": {
    "vibecraft-shared": {
      "transport": "sse",
      "url": "http://127.0.0.1:8765/sse"
    }
  }
}
```

---

## Verifying All Tools Are Available

### Check Server Logs
When server starts, you should see:
```
✅ RCON connected
✅ WorldEdit 7.3.17 detected
🚀 HTTP/SSE Server Ready!
```

### Check Claude
In Claude, you should see **41 tools** available:

**Core Tools (2)**
- `rcon_command` - Generic RCON execution
- `get_server_info` - Server status

**WorldEdit Categories (26)**
- `worldedit_selection` - Define regions
- `worldedit_region` - Modify regions
- `worldedit_generation` - Generate shapes
- `worldedit_clipboard` - Copy/paste
- `worldedit_schematic` - Save/load files
- `worldedit_history` - Undo/redo
- `worldedit_utility` - Fill, drain, etc.
- `worldedit_biome` - Biome management
- `worldedit_brush` - Brush tools
- `worldedit_general` - Session controls
- `worldedit_navigation` - Player movement
- `worldedit_chunk` - Chunk operations
- `worldedit_snapshot` - Backup restore
- `worldedit_scripting` - CraftScripts
- `worldedit_reference` - Help/search
- `worldedit_tools` - Tool binding
- (+ 10 more WorldEdit categories)

**Helper Tools (6)**
- `validate_pattern` - Check patterns
- `validate_mask` - Check masks
- `search_minecraft_item` - Find blocks
- `calculate_region_size` - Block counts
- `get_player_position` - Location detection
- `get_surface_level` - Ground level

**Advanced Tools (7)**
- `terrain_analyzer` - Site analysis
- `furniture_lookup` - 60+ furniture designs
- `calculate_shape` - Perfect circles/spheres
- `calculate_window_spacing` - Architecture
- `check_symmetry` - QA validation
- `analyze_lighting` - Mob spawn prevention
- `validate_structure` - Physics checks

**Total: 41 Tools**

---

## Troubleshooting

### Only seeing 9 tools?
**Problem**: You're running the FastMCP version instead of the HTTP wrapper.

**Solution**:
```bash
# Kill the wrong server
lsof -ti :8765 | xargs kill -9

# Start the correct server
cd mcp-server
./run_fastmcp.sh
# Choose option 2
```

### Server won't start?
**Check 1**: Is Minecraft running?
```bash
lsof -i :25575  # Should show Java process
```

**Check 2**: Is RCON enabled?
```bash
# In server.properties:
enable-rcon=true
rcon.port=25575
rcon.password=your_password
```

**Check 3**: Is password set?
```bash
# In mcp-server/.env:
VIBECRAFT_RCON_PASSWORD=your_password
```

### Connection refused in Claude?
**Check 1**: Is server running?
```bash
lsof -i :8765  # Should show Python process
```

**Check 2**: Is URL correct?
- Should be: `http://127.0.0.1:8765/sse`
- NOT: `http://localhost:8765` (use IP, not hostname)

**Check 3**: Check server logs
Look for:
```
INFO:     Uvicorn running on http://127.0.0.1:8765
```

---

## Server Output (What You Should See)

### Startup
```
🎮 VibeCraft MCP Server - HTTP/SSE Mode
   All 34+ tools available
============================================================

📡 RCON Host: 127.0.0.1:25575
Testing RCON connection...
✅ RCON connected: There are 1 of a max of 10 players online: player1
✅ WorldEdit 7.3.17 detected

============================================================
🚀 HTTP/SSE Server Ready!
============================================================

📡 Server URL: http://127.0.0.1:8765/sse
```

### When Claude Connects
```
INFO:     127.0.0.1:56645 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:56646 - "POST /messages/?session_id=abc123... HTTP/1.1" 202 Accepted
2025-11-01 22:00:33,185 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
```

### When Tool is Called
```
2025-11-01 22:01:45,123 - vibecraft.rcon_manager - INFO - Executing command: //pos1 100,64,100
2025-11-01 22:01:45,234 - vibecraft.rcon_manager - INFO - Response: First position set to (100, 64, 100).
```

---

## Next Steps

1. **Start the server**: `./run_fastmcp.sh` → Option 2
2. **Verify tools**: Check Claude shows 41 tools
3. **Test RCON**: Try `get_server_info` tool
4. **Start building**: Ask Claude to build something!

---

## Additional Resources

- **Full Documentation**: `HTTP_SSE_SOLUTION.md`
- **Setup Guide**: `../docs/COMPLETE_SETUP_GUIDE.md`
- **User Guide**: `../docs/USER_ACTION_GUIDE.md`
- **Claude Instructions**: `../CLAUDE.md`
