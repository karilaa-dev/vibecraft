# VibeCraft User Action Guide

Complete step-by-step guide for setting up and running VibeCraft.

## Quick Start (Recommended)

If you want to get started quickly with automated setup:

```bash
# From the vibecraft directory
./setup-all.sh
```

This will automatically:
- Verify prerequisites (Python 3.10+, Docker)
- Set up the MCP server with virtual environment
- Download and configure Minecraft server (PaperMC 1.21.3)
- Install WorldEdit plugin (7.3.10)
- Generate RCON password
- Create Claude Code configuration
- Test all connections

**Time estimate:** 5-10 minutes (mostly waiting for Minecraft server initialization)

Then skip to [Step 4: Configure Claude Code](#step-4-configure-claude-code)

---

## Prerequisites

Before starting, ensure you have:

### Required Software

1. **Python 3.10 or higher**
   - Check: `python3 --version`
   - Download: https://www.python.org/downloads/

2. **Docker Desktop**
   - Check: `docker --version` and `docker info`
   - Download: https://www.docker.com/products/docker-desktop
   - **Important:** Docker Desktop must be running

3. **Docker Compose**
   - Usually included with Docker Desktop
   - Check: `docker-compose --version` or `docker compose version`

4. **Git** (optional, for cloning repositories)
   - Check: `git --version`

### System Requirements

- **Disk Space:** ~2GB free (Minecraft server + world data)
- **RAM:** 4GB minimum, 8GB recommended
- **OS:** macOS, Linux, or Windows with WSL2

---

## Option 1: Automated Setup (Recommended)

### Step 1: Run the Setup Script

```bash
cd /Users/er/Repos/vibecraft
./setup-all.sh
```

### Step 2: Monitor the Setup Process

The script will output colored progress messages:

- **[INFO]** (Blue) - Informational messages
- **[SUCCESS]** (Green) - Successful steps
- **[WARNING]** (Yellow) - Non-critical issues
- **[ERROR]** (Red) - Critical failures

**Expected timeline:**
- Prerequisites check: 5 seconds
- MCP server setup: 30 seconds
- Minecraft server first start: 2-5 minutes
- RCON testing: 10 seconds
- Configuration generation: 5 seconds

### Step 3: Save Your RCON Password

At the end of setup, you'll see:

```
RCON Password: XxXxXxXxXxXxXxXx
(Saved in: .rcon_password)
```

This password is automatically configured in:
- `mcp-server/.env`
- `docker-compose.yml`
- `claude-code-config.json`

**You don't need to copy it manually**, but keep the `.rcon_password` file safe.

### Step 4: Configure Claude Code

The setup script creates `claude-code-config.json` with your complete configuration.

#### For Claude Desktop (macOS/Linux)

**macOS:**
```bash
# Configuration location
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```bash
# Configuration location
~/.config/Claude/claude_desktop_config.json
```

**Steps:**
1. Open the configuration file (create if it doesn't exist)
2. Copy the entire content from `claude-code-config.json`
3. If you have existing `mcpServers`, add the `vibecraft` entry to the existing object
4. Save and restart Claude Desktop

**Example merged configuration:**
```json
{
  "mcpServers": {
    "existing-server": {
      "command": "...",
      "args": ["..."]
    },
    "vibecraft": {
      "command": "/Users/er/Repos/vibecraft/mcp-server/venv/bin/python",
      "args": ["-m", "src.vibecraft.server"],
      "cwd": "/Users/er/Repos/vibecraft/mcp-server",
      "env": {
        "VIBECRAFT_RCON_HOST": "127.0.0.1",
        "VIBECRAFT_RCON_PORT": "25575",
        "VIBECRAFT_RCON_PASSWORD": "your_generated_password_here"
      }
    }
  }
}
```

#### For Claude Code (VSCode Extension)

1. Open VSCode settings
2. Search for "MCP"
3. Add the server configuration from `claude-code-config.json`
4. Restart VSCode

### Step 5: Restart Claude

**Important:** Claude must be completely restarted to load the new MCP server.

- **Desktop:** Quit and reopen the application
- **VSCode:** Reload the window or restart VSCode

### Step 6: Verify the Setup

#### Test Minecraft Server

```bash
# View logs
docker logs -f vibecraft-minecraft

# Should see "Done" indicating server is ready
```

#### Test RCON Connection

```bash
# Run test script
./scripts/test-connection.sh

# Or manually
docker exec vibecraft-minecraft rcon-cli list
```

Expected output: `There are 0 of a max of 20 players online:`

#### Test MCP Server in Claude

In Claude, try asking:
- "Can you connect to the Minecraft server?"
- "What WorldEdit commands are available?"
- "Get server information"

If Claude can respond with Minecraft server data, setup is complete!

---

## Option 2: Manual Setup (Advanced)

If you prefer manual setup or the automated script fails:

### Step 1: Set Up MCP Server

```bash
cd mcp-server

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Generate RCON password
openssl rand -base64 12 | tr -d "=+/" | cut -c1-16

# Edit .env and set VIBECRAFT_RCON_PASSWORD to the generated password
nano .env  # or your preferred editor
```

### Step 2: Set Up Minecraft Server with Docker

```bash
cd ..  # Back to vibecraft root

# Edit docker-compose.yml
# Replace 'vibecraft_rcon_password_change_me' with your generated password
nano docker-compose.yml

# Start the server
docker-compose up -d

# Wait for server to initialize (2-5 minutes)
docker logs -f vibecraft-minecraft
# Press Ctrl+C when you see "Done"
```

### Step 3: Test RCON Connection

```bash
# Test connection
docker exec vibecraft-minecraft rcon-cli list

# Test WorldEdit
docker exec vibecraft-minecraft rcon-cli "version WorldEdit"
```

### Step 4: Create Claude Code Configuration

Create `claude-code-config.json` in the project root:

```json
{
  "mcpServers": {
    "vibecraft": {
      "command": "/absolute/path/to/vibecraft/mcp-server/venv/bin/python",
      "args": ["-m", "src.vibecraft.server"],
      "cwd": "/absolute/path/to/vibecraft/mcp-server",
      "env": {
        "VIBECRAFT_RCON_HOST": "127.0.0.1",
        "VIBECRAFT_RCON_PORT": "25575",
        "VIBECRAFT_RCON_PASSWORD": "your_generated_password_here"
      }
    }
  }
}
```

**Important:** Replace `/absolute/path/to/vibecraft` with your actual path.

### Step 5: Configure Claude Code

Follow the same steps as in [Automated Setup - Step 4](#step-4-configure-claude-code)

---

## Daily Usage

### Starting VibeCraft

```bash
# Start Minecraft server
./scripts/start-minecraft.sh

# Or manually
docker-compose up -d
```

### Stopping VibeCraft

```bash
# Stop Minecraft server
./scripts/stop-minecraft.sh

# Or manually
docker-compose down
```

### Viewing Logs

```bash
# View server logs
./scripts/view-logs.sh

# Or manually
docker logs -f vibecraft-minecraft
```

### Testing Connection

```bash
# Test RCON connection
./scripts/test-connection.sh

# Or manually
docker exec vibecraft-minecraft rcon-cli list
```

---

## Connecting to Minecraft

### In Minecraft Client

1. Open Minecraft (Java Edition 1.21.3)
2. Click "Multiplayer"
3. Click "Add Server"
4. Enter:
   - **Server Name:** VibeCraft
   - **Server Address:** `localhost:25565`
5. Click "Done"
6. Join the server

**Note:** The server is in creative mode with a flat world for easy building.

### Using RCON Directly

```bash
# Execute any command
docker exec vibecraft-minecraft rcon-cli "command here"

# Examples
docker exec vibecraft-minecraft rcon-cli "time set day"
docker exec vibecraft-minecraft rcon-cli "weather clear"
docker exec vibecraft-minecraft rcon-cli "//pos1"
```

---

## Using VibeCraft with Claude

### Available Tools

Once configured, Claude has access to these tools:

1. **rcon_command** - Execute any Minecraft command
2. **worldedit_selection** - Define and manipulate selections
3. **worldedit_region** - Modify selected regions
4. **worldedit_generation** - Generate shapes and terrain
5. **worldedit_clipboard** - Copy, cut, paste operations
6. **worldedit_schematic** - Save and load schematics
7. **worldedit_history** - Undo/redo operations
8. **worldedit_utility** - Navigation and utility commands
9. **worldedit_biome** - Change biomes
10. **worldedit_brush** - Configure brushes
11. **validate_pattern** - Validate WorldEdit patterns
12. **validate_mask** - Validate WorldEdit masks
13. **get_server_info** - Get server information
14. **calculate_region_size** - Calculate region sizes

### Example Requests

Try asking Claude:

**Basic Operations:**
- "Set my selection from 100,64,100 to 120,80,120 and fill it with stone"
- "Create a sphere of radius 10 made of glass at 0,70,0"
- "Copy the selected region and paste it 50 blocks north"

**Advanced Operations:**
- "Create a smooth stone pyramid of height 20"
- "Replace all dirt in the selection with a pattern of 70% grass and 30% stone"
- "Generate a forest in a 50 block radius around 200,64,200"

**Information Requests:**
- "What patterns can I use in WorldEdit?"
- "How do I create a hollow cylinder?"
- "Show me the documentation for masks"

### Important Limitations

**Commands Requiring Player Interaction:**
- Brushes (except configuration commands like /mask, /size)
- Navigation commands (//ascend, //descend, //thru)
- Tool commands (//wand, //tool)

**Workarounds:**
- For brushes: Configure from console, use in-game
- For navigation: Use teleport commands instead
- For regions: Use coordinate-based selection (//pos1, //pos2)

---

## Troubleshooting

### Minecraft Server Won't Start

**Check Docker is running:**
```bash
docker info
```

**Check logs:**
```bash
docker logs vibecraft-minecraft
```

**Common issues:**
- Port 25565 already in use: Stop other Minecraft servers
- Port 25575 (RCON) in use: Check for other RCON servers
- Insufficient memory: Increase Docker memory allocation in Docker Desktop

**Fix:**
```bash
# Stop everything
docker-compose down

# Remove container (preserves world data)
docker rm vibecraft-minecraft

# Start fresh
docker-compose up -d
```

### RCON Connection Failed

**Check password matches:**
```bash
# Check MCP server .env
cat mcp-server/.env | grep VIBECRAFT_RCON_PASSWORD

# Check docker-compose.yml
cat docker-compose.yml | grep RCON_PASSWORD

# Check Claude Code config
cat claude-code-config.json | grep VIBECRAFT_RCON_PASSWORD
```

**Passwords must match** in all three files.

**Test RCON manually:**
```bash
docker exec vibecraft-minecraft rcon-cli list
```

If this fails, RCON is not configured correctly.

**Fix:**
```bash
# Regenerate password
openssl rand -base64 12 | tr -d "=+/" | cut -c1-16

# Update all three files with the new password
# Then restart
docker-compose down
docker-compose up -d
```

### MCP Server Not Connecting

**Test MCP server manually:**
```bash
cd mcp-server
source venv/bin/activate
python -m src.vibecraft.server
```

Should show: `Server running on stdio`

Press Ctrl+C to stop.

**Check Claude Code configuration:**
```bash
# macOS
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Linux
cat ~/.config/Claude/claude_desktop_config.json
```

**Verify paths are absolute** (not relative).

**Restart Claude** completely after any config changes.

### WorldEdit Commands Not Working

**Check WorldEdit is installed:**
```bash
docker exec vibecraft-minecraft rcon-cli "version WorldEdit"
```

Should show: `WorldEdit version 7.3.10...`

**Check plugin loaded:**
```bash
docker exec vibecraft-minecraft rcon-cli "plugins"
```

Should list WorldEdit in green.

**If WorldEdit is missing:**
```bash
# Check logs for plugin load errors
docker logs vibecraft-minecraft | grep -i worldedit

# Restart server
docker-compose restart
```

### Claude Can't Execute Commands

**Verify MCP server is connected:**
Ask Claude: "Can you list the available tools?"

Should see worldedit_* tools listed.

**Check RCON from MCP server:**
```bash
cd mcp-server
source venv/bin/activate
python << 'EOF'
import os
from mcrcon import MCRcon

# Load password from .env
from dotenv import load_dotenv
load_dotenv()

password = os.getenv("VIBECRAFT_RCON_PASSWORD")
print(f"Using password: {password}")

try:
    with MCRcon("127.0.0.1", password, port=25575) as mcr:
        response = mcr.command("list")
        print(f"Success: {response}")
except Exception as e:
    print(f"Failed: {e}")
EOF
```

### World Data Corruption

**World data is persisted** in the `minecraft-data/` directory (bind mount).

**To reset the world:**
```bash
# Stop server
docker-compose down

# Remove world data
rm -rf minecraft-data/

# Start fresh (will recreate with new world)
docker-compose up -d
```

**To backup the world:**
```bash
# Create backup
tar czf world-backup-$(date +%Y%m%d-%H%M%S).tar.gz minecraft-data/

# Or backup just the world folder
cd minecraft-data
tar czf ../world-backup-$(date +%Y%m%d-%H%M%S).tar.gz world/
cd ..
```

**To restore a backup:**
```bash
# Stop server
docker-compose down

# Remove current data
rm -rf minecraft-data/

# Restore backup
tar xzf world-backup-YYYYMMDD-HHMMSS.tar.gz

# Start server
docker-compose up -d
```

---

## Configuration Reference

### Environment Variables (mcp-server/.env)

```bash
# RCON connection
VIBECRAFT_RCON_HOST=127.0.0.1
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=your_password_here

# Safety settings
VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=true
# Set to false to re-enable blocking commands like //delchunks

# Coordinate bounds (prevent excessive operations)
VIBECRAFT_MAX_COORDINATE=100000
VIBECRAFT_MIN_COORDINATE=-100000
VIBECRAFT_MAX_REGION_SIZE=1000000

# Performance
VIBECRAFT_RCON_TIMEOUT=10
```

### Docker Compose Configuration

Edit `docker-compose.yml` to customize:

- Minecraft version (VERSION)
- RCON password (RCON_PASSWORD)
- Server properties (LEVEL, GAMEMODE, etc.)
- Plugin URLs

### MCP Server Features

Edit `mcp-server/src/vibecraft/config.py` to enable/disable:

- Safety checks
- Dangerous command blocking
- Coordinate validation
- Command sanitization

---

## Useful Commands

### Docker Management

```bash
# View all containers
docker ps -a

# View logs
docker logs vibecraft-minecraft

# Follow logs
docker logs -f vibecraft-minecraft

# Execute command in container
docker exec vibecraft-minecraft <command>

# Shell access
docker exec -it vibecraft-minecraft /bin/bash

# Restart container
docker-compose restart

# Rebuild and restart
docker-compose up -d --build
```

### Minecraft Server Management

```bash
# List players
docker exec vibecraft-minecraft rcon-cli list

# Set time
docker exec vibecraft-minecraft rcon-cli "time set day"

# Set weather
docker exec vibecraft-minecraft rcon-cli "weather clear"

# Teleport player
docker exec vibecraft-minecraft rcon-cli "tp PlayerName 0 64 0"

# Give item
docker exec vibecraft-minecraft rcon-cli "give PlayerName diamond 64"

# Server properties
docker exec vibecraft-minecraft cat /data/server.properties
```

### WorldEdit Commands

```bash
# Get info
docker exec vibecraft-minecraft rcon-cli "//version"
docker exec vibecraft-minecraft rcon-cli "version WorldEdit"

# Selection
docker exec vibecraft-minecraft rcon-cli "//pos1 0,64,0"
docker exec vibecraft-minecraft rcon-cli "//pos2 10,74,10"
docker exec vibecraft-minecraft rcon-cli "//size"

# Region operations
docker exec vibecraft-minecraft rcon-cli "//set stone"
docker exec vibecraft-minecraft rcon-cli "//replace dirt grass_block"

# Generation
docker exec vibecraft-minecraft rcon-cli "//sphere glass 10"
docker exec vibecraft-minecraft rcon-cli "//pyramid stone 20"

# Clipboard
docker exec vibecraft-minecraft rcon-cli "//copy"
docker exec vibecraft-minecraft rcon-cli "//paste"

# History
docker exec vibecraft-minecraft rcon-cli "//undo"
docker exec vibecraft-minecraft rcon-cli "//redo"
```

---

## Next Steps

1. **Test the setup** - Follow Step 6 in automated setup
2. **Join the server** - Connect with Minecraft client
3. **Try commands** - Ask Claude to build something
4. **Read documentation:**
   - WorldEdit commands: `docs/RESEARCH_WORLDEDIT_COMPLETE.md`
   - Implementation details: `docs/COMPLETE_SETUP_GUIDE.md`
   - Missing commands analysis: `docs/CRITICAL_MISSING_COMMANDS.md`

## Support

For issues:

1. Check this troubleshooting guide
2. Review logs: `docker logs vibecraft-minecraft`
3. Check MCP server logs (if running in console)
4. Verify all passwords match in `.env`, `docker-compose.yml`, and `claude-code-config.json`

## Security Notes

**For POC/Development Only:**

- RCON password is stored in plaintext
- No authentication on Minecraft server
- Server is exposed on localhost only
- Docker container has broad permissions

**For Production:**

- Use environment variables instead of hardcoded passwords
- Enable Minecraft authentication
- Use firewall rules
- Implement proper secret management
- Run Docker with restricted permissions
- Use VPN or SSH tunnel for remote access

---

**Happy Building!**
