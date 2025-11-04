# VibeCraft MCP Configuration Guide

This project includes multiple MCP server configurations for different use cases.

## Available MCP Servers

### 1. `vibecraft` - Standard Server (Default)
- **Type**: stdio transport
- **Use**: Normal Claude Desktop usage
- **Logs**: Hidden (managed by Claude)
- **When to use**: Production work, standard building tasks

### 2. `vibecraft-debug` - Debug Server
- **Type**: stdio transport with visible logging
- **Use**: Debugging MCP communication
- **Logs**: Visible in terminal
- **When to use**: Troubleshooting issues, development

### 3. `vibecraft-shared` - Shared HTTP Server
- **Type**: HTTP/SSE transport
- **Use**: Multiple Claude instances
- **Logs**: Visible in terminal
- **When to use**: Running multiple Claude windows, team collaboration

## Quick Setup

### For Users (Using the project)

1. **Check that `.mcp.json` exists** in project root
2. **Start Minecraft server** with RCON enabled
3. **Configure RCON password**:
   ```bash
   cd mcp-server
   cp .env.example .env
   # Edit .env with your RCON password
   ```
4. **Choose your mode** in Claude Desktop settings

### For Developers (Setting up locally)

1. **Clone the repository**
2. **Install UV** (if not installed):
   ```bash
   pip install uv
   ```
3. **Set up environment**:
   ```bash
   cd mcp-server
   cp .env.example .env
   # Edit .env with your RCON password
   ```
4. **Test the server**:
   ```bash
   ./run_server.sh
   ```

## Configuration Locations

- **Project config** (shared): `.mcp.json` - Defines available servers
- **Environment config** (local): `mcp-server/.env` - Your RCON credentials
- **Claude config** (auto): Claude Desktop will detect `.mcp.json`

## Server Modes

### Standard Mode
```bash
# Claude launches automatically
# No manual action needed
```

### Debug Mode
```bash
cd mcp-server
python3 run_debug.py
# Then connect Claude using vibecraft-debug config
```

### Shared HTTP Mode
```bash
cd mcp-server
/Users/er/.pyenv/versions/3.11.11/bin/uv run python run_shared_server.py
# Server runs at http://127.0.0.1:8765
# Multiple Claude instances can connect
```

## Troubleshooting

### RCON Connection Failed
- Check Minecraft server is running
- Verify `enable-rcon=true` in server.properties
- Check RCON password matches .env file
- Default port is 25575

### MCP Server Not Found
- Ensure `.mcp.json` is in project root
- Restart Claude Desktop after changes
- Check Python/UV installation

### Multiple Claude Instances
- Use `vibecraft-shared` configuration
- Start shared server first
- All instances will share the same server

## Environment Variables

Required:
- `VIBECRAFT_RCON_HOST`: Minecraft server IP (default: 127.0.0.1)
- `VIBECRAFT_RCON_PORT`: RCON port (default: 25575)
- `VIBECRAFT_RCON_PASSWORD`: Your RCON password

Optional:
- `VIBECRAFT_ENABLE_SAFETY_CHECKS`: Enable command validation (default: true)
- `VIBECRAFT_ALLOW_DANGEROUS_COMMANDS`: Allow destructive commands (default: false)
- `VIBECRAFT_ENABLE_COMMAND_LOGGING`: Log all commands (default: true)

## Security Notes

- Never commit `.env` files with passwords
- Use `.env.example` as a template
- RCON passwords should be strong and unique
- Be cautious with `ALLOW_DANGEROUS_COMMANDS`