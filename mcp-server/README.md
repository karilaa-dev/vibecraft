# VibeCraft MCP Server

**AI-Powered WorldEdit for Minecraft**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

VibeCraft is a Model Context Protocol (MCP) server that exposes ALL WorldEdit commands to AI assistants like Claude, enabling AI-powered building in Minecraft.

## Features

- 🎯 **Complete WorldEdit Coverage** - All 200+ WorldEdit commands accessible
- 🔒 **Safety First** - Command validation, sanitization, and coordinate bounds checking
- 🛠️ **Hybrid Tool Approach** - Generic RCON + Categorized WorldEdit + Helper utilities
- 📚 **Comprehensive Documentation** - Built-in guides for patterns, masks, expressions
- 🔌 **Easy Integration** - Works with Claude Code, Claude Desktop, Cursor, and other MCP clients
- ⚡ **RCON-Based** - Simple setup, no custom Minecraft plugins required

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Minecraft server with WorldEdit and RCON enabled
- Claude Code, Claude Desktop, or another MCP-compatible client

### Installation

```bash
# Clone the repository
cd /Users/er/Repos/vibecraft/mcp-server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR: venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the `mcp-server` directory:

```bash
# RCON Connection
VIBECRAFT_RCON_HOST=127.0.0.1
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=your_rcon_password_here
VIBECRAFT_RCON_TIMEOUT=10

# Safety Settings
VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=true
VIBECRAFT_MAX_COMMAND_LENGTH=1000

# Optional: Build Area Constraints
# VIBECRAFT_BUILD_MIN_X=0
# VIBECRAFT_BUILD_MAX_X=1000
# VIBECRAFT_BUILD_MIN_Y=-64
# VIBECRAFT_BUILD_MAX_Y=319
# VIBECRAFT_BUILD_MIN_Z=0
# VIBECRAFT_BUILD_MAX_Z=1000

# Feature Flags
VIBECRAFT_ENABLE_VERSION_DETECTION=true
VIBECRAFT_ENABLE_COMMAND_LOGGING=true
```

### Test the Server

```bash
# Activate virtual environment if not already active
source venv/bin/activate

# Run the server directly (for testing)
python -m src.vibecraft.server
```

The server will connect to your Minecraft server and verify WorldEdit is installed.

## Integrating with AI Clients

### Claude Code

Add to your Claude Code MCP configuration:

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
        "VIBECRAFT_RCON_PASSWORD": "your_password_here"
      }
    }
  }
}
```

Restart Claude Code. You should now see VibeCraft tools available!

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

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
        "VIBECRAFT_RCON_PASSWORD": "your_password_here"
      }
    }
  }
}
```

Restart Claude Desktop.

### Cursor

Edit `.cursor/mcp.json` in your project:

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
        "VIBECRAFT_RCON_PASSWORD": "your_password_here"
      }
    }
  }
}
```

## Available Tools

VibeCraft provides three tiers of tools:

### Tier 1: Generic RCON
- `rcon_command` - Execute any Minecraft/WorldEdit command

### Tier 2: Categorized WorldEdit Commands
- `worldedit_selection` - Define and manipulate regions
- `worldedit_region` - Modify selected regions (set, replace, walls, etc.)
- `worldedit_generation` - Generate shapes (spheres, cylinders, pyramids)
- `worldedit_clipboard` - Copy, cut, paste operations
- `worldedit_schematic` - Save/load structures
- `worldedit_history` - Undo/redo changes
- `worldedit_utility` - Fill, drain, remove, environment commands
- `worldedit_biome` - View and modify biomes
- `worldedit_brush` - Brush-based editing (requires player)
- `worldedit_general` - Session options, limits, side-effects, and overrides
- `worldedit_navigation` - Movement commands that usually need player context
- `worldedit_chunk` - Chunk diagnostics and deletion commands
- `worldedit_snapshot` - Snapshot selection and restoration
- `worldedit_scripting` - CraftScript execution helpers
- `worldedit_reference` - Search and help index commands
- `worldedit_tools` - Tool binding, super pickaxe, and brush configuration

### Tier 3: Helper Utilities
- `validate_pattern` - Validate WorldEdit patterns
- `validate_mask` - Validate WorldEdit masks
- `get_server_info` - Get server status and info
- `calculate_region_size` - Calculate region dimensions and block count

## Example Usage with AI

Once configured, you can ask Claude (or your AI assistant):

```
"Build a stone castle at coordinates 100, 64, 100. Make it 30x20x30 blocks."

"Create a hollow sphere of glass with a 15 block radius at 200, 80, 200."

"Replace all dirt in the region from (0,60,0) to (50,70,50) with grass blocks."

"Copy the structure at (100,64,100) to (100,64,110) and paste it at (300,64,300)."
```

The AI will use VibeCraft tools to execute appropriate WorldEdit commands!

## Documentation Resources

VibeCraft provides built-in documentation resources that AI can access:

- `vibecraft://guide/patterns` - WorldEdit pattern syntax
- `vibecraft://guide/masks` - WorldEdit mask syntax
- `vibecraft://guide/expressions` - WorldEdit expression syntax
- `vibecraft://guide/coordinates` - Coordinate system guide
- `vibecraft://guide/workflows` - Common building workflows
- `vibecraft://guide/player-context` - Player context commands info

## Safety Features

- **Command Sanitization** - Blocks command injection, control characters
- **Dangerous Command Controls** - Optional restrictions via config (default allows all)
- **Coordinate Bounds** - Optional restrictions on build area
- **Player Context Warnings** - Warns about commands that need player interaction
- **Command Logging** - Track all executed commands

## Troubleshooting

### RCON Connection Failed

**Problem:** "Failed to connect to Minecraft server"

**Solutions:**
1. Verify Minecraft server is running
2. Check `server.properties` has `enable-rcon=true`
3. Verify RCON password matches
4. Ensure no firewall blocking port 25575
5. Test with `mcrcon` CLI tool

### WorldEdit Commands Not Working

**Problem:** Commands execute but nothing happens

**Solutions:**
1. Verify WorldEdit is installed: `/version WorldEdit`
2. Check you have operator permissions
3. Use comma-separated coordinates from console: `//pos1 X,Y,Z`
4. Some commands require player context - use alternatives

### Commands Blocked by Safety

**Problem:** "Potentially dangerous command blocked" (only when you've set `VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=false`)

**Solutions:**
- Review command to ensure it's safe
- Re-enable dangerous commands with `VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=true`
- Use coordinate bounds to limit build area

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=src/vibecraft --cov-report=html
```

### Code Quality

```bash
# Format code
black src/

# Lint code
ruff check src/

# Type checking
mypy src/
```

## Architecture

```
VibeCraft MCP Server
├── Configuration Management (config.py)
├── RCON Connection Manager (rcon_manager.py)
├── Command Sanitization (sanitizer.py)
├── Documentation Resources (resources.py)
└── MCP Server Implementation (server.py)
    ├── Tier 1: Generic RCON Tool
    ├── Tier 2: Categorized WorldEdit Tools (16 tools)
    └── Tier 3: Helper Utilities (4 tools)
```

## Limitations

- **RCON-Based**: Some commands requiring player context won't work from console
- **No Schematic Browsing**: File system access depends on server permissions
- **Async Operations**: Large operations may timeout (increase `RCON_TIMEOUT`)
- **Version Detection**: Automatic but may fail on some server configurations

## Roadmap

Future enhancements planned:
- [ ] Custom Minecraft plugin for direct WorldEdit API access
- [ ] WebSocket support for real-time feedback
- [ ] Schematic preview and validation
- [ ] Build queue management for large operations
- [ ] Multi-server support
- [ ] Web UI for monitoring and management

## Contributing

Contributions welcome! Please see our contributing guidelines.

## License

MIT License - see LICENSE file for details

## Credits

- WorldEdit by EngineHub
- MCP SDK by Anthropic
- mcrcon library by Tiiffi

## Support

- 📖 [Full Documentation](../docs/)
- 🐛 [Report Issues](https://github.com/your-repo/vibecraft/issues)
- 💬 [Discussions](https://github.com/your-repo/vibecraft/discussions)

---

**Built with ❤️ for the Minecraft and AI communities**
