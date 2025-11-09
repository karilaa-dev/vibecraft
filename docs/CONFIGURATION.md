# VibeCraft Configuration Guide

Complete reference for configuring VibeCraft MCP server.

## Table of Contents

- [Configuration File Location](#configuration-file-location)
- [Environment Variables Reference](#environment-variables-reference)
- [Configuration Categories](#configuration-categories)
  - [RCON Connection](#rcon-connection)
  - [Safety Settings](#safety-settings)
  - [Build Area Constraints](#build-area-constraints)
  - [Feature Flags](#feature-flags)
- [MCP Client Configuration](#mcp-client-configuration)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)

---

## Configuration File Location

VibeCraft uses environment variables loaded from a `.env` file.

**Location**: `/path/to/vibecraft/mcp-server/.env`

Create this file if it doesn't exist:
```bash
cd mcp-server
cp .env.example .env  # If you have an example file
# OR create from scratch:
touch .env
```

---

## Environment Variables Reference

### Quick Reference Table

| Variable | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `VIBECRAFT_RCON_HOST` | string | `127.0.0.1` | Yes | Minecraft server hostname |
| `VIBECRAFT_RCON_PORT` | integer | `25575` | Yes | RCON port |
| `VIBECRAFT_RCON_PASSWORD` | string | - | Yes | RCON password |
| `VIBECRAFT_RCON_TIMEOUT` | integer | `10` | No | RCON connection timeout (seconds) |
| `VIBECRAFT_ENABLE_SAFETY_CHECKS` | boolean | `true` | No | Enable command validation |
| `VIBECRAFT_ALLOW_DANGEROUS_COMMANDS` | boolean | `true` | No | Allow potentially destructive commands |
| `VIBECRAFT_MAX_COMMAND_LENGTH` | integer | `1000` | No | Maximum command length |
| `VIBECRAFT_BUILD_MIN_X` | integer | - | No | Minimum X coordinate for builds |
| `VIBECRAFT_BUILD_MAX_X` | integer | - | No | Maximum X coordinate for builds |
| `VIBECRAFT_BUILD_MIN_Y` | integer | - | No | Minimum Y coordinate for builds |
| `VIBECRAFT_BUILD_MAX_Y` | integer | - | No | Maximum Y coordinate for builds |
| `VIBECRAFT_BUILD_MIN_Z` | integer | - | No | Minimum Z coordinate for builds |
| `VIBECRAFT_BUILD_MAX_Z` | integer | - | No | Maximum Z coordinate for builds |
| `VIBECRAFT_ENABLE_VERSION_DETECTION` | boolean | `true` | No | Auto-detect WorldEdit version |
| `VIBECRAFT_ENABLE_COMMAND_LOGGING` | boolean | `true` | No | Log all executed commands |

---

## Configuration Categories

### RCON Connection

Configure connection to your Minecraft server's RCON interface.

```bash
# RCON Connection
VIBECRAFT_RCON_HOST=127.0.0.1      # Server IP (use 127.0.0.1 for local)
VIBECRAFT_RCON_PORT=25575          # RCON port (default: 25575)
VIBECRAFT_RCON_PASSWORD=your_password_here  # Password from server.properties
VIBECRAFT_RCON_TIMEOUT=10          # Timeout in seconds
```

**Setup Checklist**:
1. ✅ Enable RCON in Minecraft `server.properties`:
   ```properties
   enable-rcon=true
   rcon.port=25575
   rcon.password=your_secure_password
   ```
2. ✅ Restart Minecraft server
3. ✅ Copy `rcon.password` to VibeCraft `.env`
4. ✅ Test connection: `uv run python -m src.vibecraft.server`

**Common Issues**:
- **Connection refused** → Check `enable-rcon=true` in server.properties
- **Authentication failed** → Verify password matches exactly
- **Timeout** → Increase `VIBECRAFT_RCON_TIMEOUT` or check network

---

### Safety Settings

Control command validation and safety checks.

```bash
# Safety Settings
VIBECRAFT_ENABLE_SAFETY_CHECKS=true      # Enable input validation
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=true  # Allow //regen, //delchunks, etc.
VIBECRAFT_MAX_COMMAND_LENGTH=1000        # Max characters per command
```

**Safety Levels**:

**Maximum Safety** (Recommended for public servers):
```bash
VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=false
VIBECRAFT_MAX_COMMAND_LENGTH=500
VIBECRAFT_BUILD_MIN_X=0
VIBECRAFT_BUILD_MAX_X=1000
VIBECRAFT_BUILD_MIN_Y=0
VIBECRAFT_BUILD_MAX_Y=256
VIBECRAFT_BUILD_MIN_Z=0
VIBECRAFT_BUILD_MAX_Z=1000
```

**Moderate Safety** (Default):
```bash
VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=true  # AI can use //regen, //delchunks
VIBECRAFT_MAX_COMMAND_LENGTH=1000
# No build area constraints
```

**No Safety** (Development/testing only):
```bash
VIBECRAFT_ENABLE_SAFETY_CHECKS=false
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=true
VIBECRAFT_MAX_COMMAND_LENGTH=10000
```

---

### Build Area Constraints

Optional: Restrict builds to a specific region.

```bash
# Optional: Build Area Constraints
VIBECRAFT_BUILD_MIN_X=0
VIBECRAFT_BUILD_MAX_X=1000
VIBECRAFT_BUILD_MIN_Y=-64    # Minecraft 1.18+ bedrock level
VIBECRAFT_BUILD_MAX_Y=319    # Minecraft 1.18+ build limit
VIBECRAFT_BUILD_MIN_Z=0
VIBECRAFT_BUILD_MAX_Z=1000
```

**When to Use**:
- ✅ Public servers (prevent builds in wrong area)
- ✅ Protected regions (keep AI builds in designated zone)
- ✅ Testing (limit scope of experiments)

**When NOT to Use**:
- ❌ Single-player worlds
- ❌ Private servers with trusted AI operators
- ❌ Creative mode testing

**Example Scenarios**:

**Spawn Protection**:
```bash
# Keep builds away from spawn (0,0)
VIBECRAFT_BUILD_MIN_X=500
VIBECRAFT_BUILD_MAX_X=2000
VIBECRAFT_BUILD_MIN_Z=500
VIBECRAFT_BUILD_MAX_Z=2000
```

**Creative Plot**:
```bash
# Restrict to a 256x256 plot
VIBECRAFT_BUILD_MIN_X=1000
VIBECRAFT_BUILD_MAX_X=1256
VIBECRAFT_BUILD_MIN_Y=64
VIBECRAFT_BUILD_MAX_Y=128
VIBECRAFT_BUILD_MIN_Z=1000
VIBECRAFT_BUILD_MAX_Z=1256
```

---

### Feature Flags

Enable/disable optional features.

```bash
# Feature Flags
VIBECRAFT_ENABLE_VERSION_DETECTION=true  # Auto-detect WorldEdit version
VIBECRAFT_ENABLE_COMMAND_LOGGING=true    # Log commands to file
```

**Version Detection**:
- Detects WorldEdit version on startup
- Helps diagnose compatibility issues
- Minimal performance impact

**Command Logging**:
- Logs all executed commands to `logs/vibecraft_*.log`
- Useful for debugging and auditing
- Slight performance overhead

---

## MCP Client Configuration

Configure VibeCraft in your MCP client (Claude Code, Claude Desktop, Cursor).

### Claude Code

**Location**: `.claude/mcp.json` in your project

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

**Important**:
- Use **absolute paths** for `cwd`
- Include RCON credentials in `env` (overrides .env file)
- Restart Claude Code after changes

### Claude Desktop

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

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

Restart Claude Desktop after editing.

### Cursor

**Location**: `.cursor/mcp.json` in your project

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

---

## Advanced Configuration

### Multiple Servers

Connect to different Minecraft servers by creating multiple MCP server entries:

```json
{
  "mcpServers": {
    "vibecraft-creative": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.vibecraft.server"],
      "cwd": "/path/to/vibecraft/mcp-server",
      "env": {
        "VIBECRAFT_RCON_HOST": "127.0.0.1",
        "VIBECRAFT_RCON_PORT": "25575",
        "VIBECRAFT_RCON_PASSWORD": "creative_password"
      }
    },
    "vibecraft-survival": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.vibecraft.server"],
      "cwd": "/path/to/vibecraft/mcp-server",
      "env": {
        "VIBECRAFT_RCON_HOST": "192.168.1.100",
        "VIBECRAFT_RCON_PORT": "25576",
        "VIBECRAFT_RCON_PASSWORD": "survival_password"
      }
    }
  }
}
```

### Remote Servers

Connect to remote Minecraft servers:

```bash
# .env for remote server
VIBECRAFT_RCON_HOST=mc.example.com    # Domain or IP
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=remote_password
VIBECRAFT_RCON_TIMEOUT=30             # Longer timeout for network latency
```

**Security Considerations**:
- Use secure RCON passwords (16+ characters, random)
- Consider firewall rules (only allow specific IPs)
- Use SSH tunnel for extra security:
  ```bash
  ssh -L 25575:localhost:25575 user@mc.example.com
  # Then connect to 127.0.0.1:25575 in VibeCraft
  ```

### Custom Python Environment

Use a specific Python version or virtualenv:

```json
{
  "mcpServers": {
    "vibecraft": {
      "command": "/usr/bin/python3.11",  // Specific Python
      "args": ["-m", "src.vibecraft.server"],
      "cwd": "/path/to/vibecraft/mcp-server",
      "env": {
        // ... RCON config
      }
    }
  }
}
```

---

## Troubleshooting

### Configuration Not Loading

**Problem**: Changes to `.env` not taking effect

**Solutions**:
1. Restart MCP client (Claude Code/Desktop/Cursor)
2. Check `.env` file is in `mcp-server/` directory (not project root)
3. Verify no syntax errors in `.env` (no quotes, no spaces around `=`)
4. Check MCP client config overrides (client `env` takes precedence)

### RCON Connection Failed

**Problem**: "Failed to connect to Minecraft server"

**Debug Steps**:
```bash
# 1. Verify Minecraft server is running
# Check server logs

# 2. Test RCON with mcrcon tool
brew install mcrcon  # macOS
# or: apt-get install mcrcon  # Linux
mcrcon -H 127.0.0.1 -P 25575 -p your_password "list"

# 3. Check server.properties
grep rcon server.properties
# Should show:
# enable-rcon=true
# rcon.port=25575
# rcon.password=your_password

# 4. Check firewall
telnet 127.0.0.1 25575
# Should connect (Ctrl+C to exit)
```

### Commands Not Working

**Problem**: Commands execute but nothing happens in Minecraft

**Solutions**:
1. Verify WorldEdit is installed: `/version WorldEdit` in Minecraft
2. Check you have operator permissions: `/op YourUsername`
3. Use console-compatible syntax: `//pos1 X,Y,Z` (comma-separated!)
4. Some commands require player context (use alternatives from docs)

### Permission Errors

**Problem**: "You don't have permission to use this command"

**Solutions**:
1. Give yourself operator status: `/op YourUsername`
2. Check WorldEdit permissions in `plugins/WorldEdit/config.yml`
3. Verify RCON user has admin privileges

---

## Configuration Best Practices

### Security

✅ **DO**:
- Use strong RCON passwords (16+ random characters)
- Keep `.env` out of version control (add to `.gitignore`)
- Use environment-specific `.env` files (.env.local, .env.production)
- Rotate RCON passwords periodically
- Use build area constraints on public servers

❌ **DON'T**:
- Commit `.env` to git
- Share RCON passwords in screenshots/logs
- Use default passwords (change from "minecraft")
- Disable safety checks on public servers

### Performance

✅ **DO**:
- Use local connections when possible (127.0.0.1)
- Set reasonable timeouts (10-30 seconds)
- Enable command logging for debugging

❌ **DON'T**:
- Use very short timeouts (< 5 seconds) for remote servers
- Disable version detection (minimal overhead)

### Development vs Production

**Development**:
```bash
# Liberal settings for testing
VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=true
VIBECRAFT_ENABLE_COMMAND_LOGGING=true
# No build constraints
```

**Production**:
```bash
# Strict settings for public server
VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=false
VIBECRAFT_MAX_COMMAND_LENGTH=500
VIBECRAFT_BUILD_MIN_X=1000
VIBECRAFT_BUILD_MAX_X=2000
# ... full build area constraints
VIBECRAFT_ENABLE_COMMAND_LOGGING=true
```

---

## Example Configurations

### Single-Player Creative

```bash
# .env - Single-player creative (local)
VIBECRAFT_RCON_HOST=127.0.0.1
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=creative_mode_password
VIBECRAFT_RCON_TIMEOUT=10

VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=true  # Allow //regen, etc.
VIBECRAFT_MAX_COMMAND_LENGTH=1000

# No build constraints (entire world available)

VIBECRAFT_ENABLE_VERSION_DETECTION=true
VIBECRAFT_ENABLE_COMMAND_LOGGING=true
```

### Public Creative Server

```bash
# .env - Public server with build plots
VIBECRAFT_RCON_HOST=127.0.0.1
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=super_secure_random_password_here
VIBECRAFT_RCON_TIMEOUT=15

VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=false  # Block //regen, //delchunks
VIBECRAFT_MAX_COMMAND_LENGTH=500

# Restrict to creative build area (plot system)
VIBECRAFT_BUILD_MIN_X=5000
VIBECRAFT_BUILD_MAX_X=10000
VIBECRAFT_BUILD_MIN_Y=0
VIBECRAFT_BUILD_MAX_Y=256
VIBECRAFT_BUILD_MIN_Z=5000
VIBECRAFT_BUILD_MAX_Z=10000

VIBECRAFT_ENABLE_VERSION_DETECTION=true
VIBECRAFT_ENABLE_COMMAND_LOGGING=true
```

### Remote Development Server

```bash
# .env - Remote server over internet
VIBECRAFT_RCON_HOST=mc.example.com
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=remote_dev_password
VIBECRAFT_RCON_TIMEOUT=30  # Higher for network latency

VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=true
VIBECRAFT_MAX_COMMAND_LENGTH=1000

# No build constraints

VIBECRAFT_ENABLE_VERSION_DETECTION=true
VIBECRAFT_ENABLE_COMMAND_LOGGING=true
```

---

## Related Documentation

- [README.md](../README.md) - Quick start guide
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Development setup
- [RCON Password Setup](./RCON_PASSWORD_SETUP.md) - Secure password management

---

**Last Updated**: November 9, 2025
**Version**: 1.0.0
