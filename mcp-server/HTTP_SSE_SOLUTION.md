# VibeCraft HTTP/SSE Server - Tool Parity Solution

## Problem

When running VibeCraft MCP server with HTTP/SSE transport using FastMCP, only 9 tools were exposed instead of the full 41 tools available in the original stdio server.

## Root Cause

FastMCP uses a different tool registration system than the official `mcp` package. The decorator-based approach in FastMCP (`@mcp.tool()`) doesn't properly expose all tools defined in the original `vibecraft.server` module.

## Solution

Created `server_http.py` which:
1. Imports the original `app` from `vibecraft.server` (with all 41 tools)
2. Wraps it with HTTP/SSE transport using `mcp.server.sse.SseServerTransport`
3. Maintains 100% tool parity with the stdio server

## File Comparison

### ❌ FastMCP Approach (9 tools only)
- File: `server_fastmcp.py`
- Uses: `from fastmcp import FastMCP`
- Registration: `@mcp.tool()` decorators
- Result: Only 9 tools exposed

### ✅ HTTP Wrapper Approach (ALL 41 tools)
- File: `server_http.py`
- Uses: Official `mcp` package with SSE transport
- Registration: Imports original `app` with `@app.list_tools()` handler
- Result: All 41 tools exposed

## Usage

### Quick Start
```bash
cd mcp-server
./run_fastmcp.sh
# Choose option 2 for HTTP/SSE mode
```

### Manual Start
```bash
cd mcp-server
/Users/er/.pyenv/versions/3.11.11/bin/uv run python server_http.py --port 8765
```

### Add to Claude Desktop
```json
{
  "mcpServers": {
    "vibecraft-shared": {
      "url": "http://127.0.0.1:8765/sse"
    }
  }
}
```

### Add to Claude Code (Project Config)
Already configured in `.mcp.json`:
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

## Features

✅ **All 41 Tools Available**
- Generic RCON command
- 26 WorldEdit command categories
- 8 helper/validation tools
- 6 advanced building tools

✅ **Multiple Client Support**
- Multiple Claude Desktop instances can connect
- Multiple Claude Code instances can connect
- All share the same RCON connection pool

✅ **Debug Visibility**
- All MCP communication logged to console
- RCON command execution logged
- Tool invocation logged
- Easy troubleshooting

✅ **No Code Duplication**
- Reuses original server code
- Single source of truth for tool definitions
- Automatic updates when original server changes

## Technical Details

### How It Works

1. **Import Original App**
   ```python
   from vibecraft.server import app
   ```
   This imports the complete MCP Server instance with all decorators already applied.

2. **Create SSE Transport**
   ```python
   from mcp.server.sse import SseServerTransport
   sse = SseServerTransport("/messages")
   ```

3. **Connect Streams**
   ```python
   async with sse.connect_sse(...) as streams:
       await app.run(streams[0], streams[1], ...)
   ```

4. **Serve via HTTP**
   ```python
   starlette_app = Starlette(routes=[
       Route("/sse", handle_sse, methods=["GET"]),
       Route("/messages", handle_messages, methods=["POST"]),
   ])
   ```

### Why This Works

The MCP Server class (`app`) already has:
- All tool handlers registered via `@app.list_tools()`
- Tool execution via `@app.call_tool()`
- Request handlers for MCP protocol

By importing `app` and wrapping it with SSE transport, we get:
- 100% of original functionality
- HTTP/SSE transport benefits
- No tool registration code needed

### Logging Added

The `server_http.py` includes enhanced logging:
- Startup: Shows tool count inspection
- Connection: Logs when Claude connects
- Requests: Logs all MCP messages
- Responses: Can log tool lists (when handler wrapper is enabled)

## Comparison: stdio vs HTTP/SSE

| Feature | stdio (original) | HTTP/SSE (wrapper) |
|---------|------------------|-------------------|
| Tools Available | 41 | 41 |
| Multiple Clients | ❌ No | ✅ Yes |
| Debug Logs Visible | ❌ No | ✅ Yes |
| Auto-Launch | ✅ Yes | ⚠️ Manual |
| Performance | Fast | Fast |
| Complexity | Low | Low |

## Maintenance

When adding new tools to `vibecraft.server`:
1. Add tool to `@app.list_tools()` in `src/vibecraft/server.py`
2. Add handler to `@app.call_tool()` in same file
3. No changes needed to `server_http.py` - it automatically inherits new tools

## Troubleshooting

### Only seeing 9 tools?
- Make sure you're running `server_http.py`, not `server_fastmcp.py`
- Check the startup logs for "WRAPPING list_tools TO LOG RESPONSE"
- Verify the server URL is `http://127.0.0.1:8765/sse`

### Connection refused?
- Ensure server is running: `lsof -i :8765`
- Check RCON is enabled in Minecraft server
- Verify RCON password in `.env` file

### Server crashes on startup?
- Check Minecraft server is running
- Verify RCON connection works: `telnet localhost 25575`
- Check logs in `mcp-server/logs/`

## Future Improvements

Potential enhancements:
- [ ] Auto-launch option (background process)
- [ ] Health check endpoint
- [ ] Metrics/statistics endpoint
- [ ] WebSocket transport option
- [ ] Multi-server RCON pooling

## Credits

- Original MCP Server: `src/vibecraft/server.py`
- HTTP/SSE Wrapper: `server_http.py`
- Transport: `mcp.server.sse.SseServerTransport` from official `mcp` package
