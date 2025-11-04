# VibeCraft

**AI-Powered WorldEdit for Minecraft**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Minecraft 1.21+](https://img.shields.io/badge/minecraft-1.21+-green.svg)](https://www.minecraft.net/)
[![Status: Complete](https://img.shields.io/badge/Status-Complete%20%26%20Operational-brightgreen.svg)](SETUP_COMPLETE.md)

> Build amazing Minecraft structures using natural language through AI assistants like Claude!

**Project Status:** ✅ Complete and fully operational! See [SETUP_COMPLETE.md](SETUP_COMPLETE.md) for details.

VibeCraft is a proof-of-concept that enables AI-powered building in Minecraft by exposing WorldEdit's powerful editing functions through a Model Context Protocol (MCP) server.

## ✨ Features

- 🎯 **Complete WorldEdit Integration** - All 200+ commands accessible to AI
- 🤖 **Natural Language Building** - "Build a castle" instead of memorizing commands
- 🔒 **Safety First** - Command validation, sanitization, and coordinate bounds
- 📚 **Comprehensive Documentation** - Built-in guides for patterns, masks, and expressions
- 🛠️ **Easy Setup** - No custom plugins required, uses standard RCON
- ⚡ **Fast** - Direct RCON communication for instant building
- 🧱 **Automated Placement** - `place_furniture` and `place_building_pattern` convert blueprints into structures instantly
- 🗂️ **Workflow Coordinator** - Phase gating with recorded validations keeps complex projects on track

## 🎮 Quick Start

### What You'll Need

1. **Minecraft Server** (PaperMC 1.21.x recommended)
2. **WorldEdit Plugin** (7.3.17+)
3. **Python 3.10+**
4. **AI Client** (Claude Code, Claude Desktop, or Cursor)

### Installation (5-10 Minutes)

**Option 1: Automated Setup (Recommended)**
```bash
# 1. Clone the repository
git clone <repository-url>
cd vibecraft

# 2. Run one-command setup
./setup-all.sh

# 3. Configure Claude Code (see output for instructions)
# 4. Start building!
```

**Option 2: Manual Setup**
```bash
# Follow the detailed guide
See docs/USER_ACTION_GUIDE.md for step-by-step instructions
```

See [User Action Guide](docs/USER_ACTION_GUIDE.md) for complete manual with troubleshooting.

## 🏗️ Example Usage

Once configured, simply ask your AI assistant:

```
"Build a stone castle at coordinates 100, 64, 100.
Make it 50x30x50 blocks with towers at each corner."
```

```
"Create a modern house with glass walls, oak floors,
and a swimming pool at coordinates 200, 64, 200."
```

```
"Generate a natural-looking mountain terrain from (0,64,0) to (100,100,100)."
```

The AI will automatically:
1. Set appropriate region selections
2. Use WorldEdit commands to build
3. Handle complex multi-step constructions
4. Provide feedback on progress

## 📖 Documentation

### User Guides (Living Documentation)
- **[User Action Guide](docs/USER_ACTION_GUIDE.md)** - Complete manual with troubleshooting
- **[Complete Setup Guide](docs/COMPLETE_SETUP_GUIDE.md)** - End-to-end setup instructions
- **[Minecraft Server Setup](docs/MINECRAFT_SERVER_SETUP.md)** - Server configuration guide
- **[MCP Server README](mcp-server/README.md)** - MCP server documentation

### Development Documentation (Reference/Context)
- **[Research: WorldEdit Commands](dev_docs/RESEARCH_WORLDEDIT_COMPLETE.md)** - All 200+ commands documented
- **[Implementation Plan](dev_docs/IMPLEMENTATION_PLAN.md)** - Steve's detailed implementation plan
- **[Implementation Review](dev_docs/IMPLEMENTATION_PLAN_REVIEW.md)** - Cody's technical review
- **[Critical Missing Commands](dev_docs/CRITICAL_MISSING_COMMANDS.md)** - Ultra-deep analysis findings
- **[Complete Analysis Summary](dev_docs/COMPLETE_ANALYSIS_SUMMARY.md)** - Analysis overview
- **[Implementation Complete](dev_docs/IMPLEMENTATION_COMPLETE.md)** - Completion summary
- **[Original Requirements](dev_docs/INSTRUCTIONS.md)** - Project specifications

## 🏛️ Architecture

```
┌─────────────────┐
│   AI Assistant  │  (Claude, etc.)
│  (Natural Lang) │
└────────┬────────┘
         │ MCP Protocol
┌────────▼────────┐
│  VibeCraft MCP  │
│     Server      │
│  (Python + MCP) │
└────────┬────────┘
         │ RCON
┌────────▼────────┐
│   Minecraft     │
│  Server + WE    │
└─────────────────┘
```

### Components

1. **MCP Server** (`mcp-server/`)
   - RCON connection manager
   - Command sanitization and validation
   - 21 tools (generic, categorized, helpers)
   - 6 documentation resources

2. **Minecraft Server** (`minecraft-server/`)
   - PaperMC 1.21.x
   - WorldEdit 7.3.17+
   - RCON enabled

3. **Documentation** (`docs/`)
   - Setup guides
   - Command references
   - Implementation plans

## 🛠️ Available Tools

### Tier 1: Generic RCON
- `rcon_command` - Execute any command

### Tier 2: WorldEdit Categories (16 tools)
- `worldedit_selection` - Region selection
- `worldedit_region` - Modify regions
- `worldedit_generation` - Generate shapes
- `worldedit_clipboard` - Copy/paste
- `worldedit_schematic` - File operations
- `worldedit_history` - Undo/redo
- `worldedit_utility` - Utilities
- `worldedit_biome` - Biome operations
- `worldedit_brush` - Brush tools
- `worldedit_general` - Global settings & session management
- `worldedit_navigation` - Movement commands
- `worldedit_chunk` - Chunk analysis & deletion
- `worldedit_snapshot` - Snapshot restore workflows
- `worldedit_scripting` - CraftScript execution
- `worldedit_reference` - Search and help commands
- `worldedit_tools` - Tool binding and super pickaxe control

### Tier 3: Helpers (4 tools)
- `validate_pattern` - Check patterns
- `validate_mask` - Check masks
- `get_server_info` - Server status
- `calculate_region_size` - Size calculations

## 🔒 Safety Features

- **Command Sanitization** - Prevents injection attacks
- **Dangerous Command Controls** - Optional restrictions via config (default allows all)
- **Coordinate Bounds** - Restrict building area
- **Player Context Warnings** - Alerts about commands needing player
- **Operation Logging** - Track all commands

## 📋 Project Structure

```
vibecraft/
├── README.md                    # This file
├── setup-all.sh                # One-command automated setup
├── docker-compose.yml          # Automated Minecraft server setup
│
├── docs/                       # Living Documentation (User Guides)
│   ├── USER_ACTION_GUIDE.md           # Complete user manual
│   ├── COMPLETE_SETUP_GUIDE.md        # End-to-end setup
│   └── MINECRAFT_SERVER_SETUP.md      # Server configuration
│
├── dev_docs/                   # Development Documentation (Context/Reference)
│   ├── INSTRUCTIONS.md                # Original project requirements
│   ├── IMPLEMENTATION_PLAN.md         # Steve's implementation plan
│   ├── IMPLEMENTATION_PLAN_REVIEW.md  # Cody's technical review
│   ├── IMPLEMENTATION_COMPLETE.md     # Completion summary
│   ├── RESEARCH_WORLDEDIT_COMPLETE.md # All 200+ WorldEdit commands
│   ├── CRITICAL_MISSING_COMMANDS.md   # Ultra-deep analysis findings
│   └── COMPLETE_ANALYSIS_SUMMARY.md   # Analysis overview
│
├── mcp-server/                 # MCP Server Implementation
│   ├── src/vibecraft/
│   │   ├── server.py                  # Main MCP server (21 tools)
│   │   ├── config.py                  # Configuration management
│   │   ├── rcon_manager.py            # RCON connection handling
│   │   ├── sanitizer.py               # Command validation & security
│   │   └── resources.py               # Documentation resources
│   ├── requirements.txt               # Python dependencies
│   ├── .env.example                   # Environment template
│   └── README.md                      # MCP server documentation
│
├── scripts/                    # Helper Scripts
│   ├── start-minecraft.sh             # Start server
│   ├── stop-minecraft.sh              # Stop server
│   ├── test-connection.sh             # Test RCON
│   └── view-logs.sh                   # View server logs
│
└── reference-*/                # Reference Implementations (cloned repos)
    ├── reference-rcon-mcp/            # RCON MCP reference
    └── reference-worldedit/           # WorldEdit source code
```

## 🚀 Getting Started

### Quick Start (Automated Setup - Recommended)

1. Run `./setup-all.sh` (handles everything automatically)
2. Configure Claude Code with generated `claude-code-config.json`
3. Restart Claude
4. Start building with natural language!

**Time:** 5-10 minutes (mostly waiting for Minecraft server initialization)

### Manual Setup (Advanced Users)

Follow the [User Action Guide](docs/USER_ACTION_GUIDE.md) for detailed step-by-step instructions.

## 📝 Configuration

### MCP Server Configuration (`.env`)

```bash
# RCON Connection
VIBECRAFT_RCON_HOST=127.0.0.1
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=your_password

# Safety Settings
VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=true
# Set to false to block //delchunks, //regen, etc.

# Optional: Build Area Restrictions
VIBECRAFT_BUILD_MIN_X=0
VIBECRAFT_BUILD_MAX_X=1000
# ... (Y and Z coordinates)
```

### AI Client Configuration

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "vibecraft": {
      "command": "python",
      "args": ["-m", "src.vibecraft.server"],
      "cwd": "/path/to/vibecraft/mcp-server",
      "env": {
        "VIBECRAFT_RCON_HOST": "127.0.0.1",
        "VIBECRAFT_RCON_PORT": "25575",
        "VIBECRAFT_RCON_PASSWORD": "your_password"
      }
    }
  }
}
```

## 🔍 Examples

### Simple Cube

```
AI: "Create a 10x10x10 stone cube at 100, 64, 100"

Commands executed:
1. //pos1 100,64,100
2. //pos2 110,74,110
3. //set stone

Result: ✅ Stone cube created
```

### Complex House

```
AI: "Build a modern house at 200, 64, 200 with glass walls and oak floors"

Commands executed:
1. //pos1 200,64,200
2. //pos2 215,70,215
3. //set oak_planks      (floor)
4. //walls glass         (walls)
5. //pos1 200,70,200
6. //pos2 215,70,215
7. //set oak_stairs      (roof)

Result: ✅ Modern house with glass walls created
```

### Terrain Generation

```
AI: "Create a natural hill at 0,64,0"

Commands executed:
1. //pos1 -20,64,-20
2. //pos2 20,80,20
3. //generate stone (20-sqrt((x)^2+(z)^2))*0.3+y-64<5
4. //smooth 3
5. //replace >stone grass_block

Result: ✅ Natural hill with grass on top created
```

## 🎯 Use Cases

### Creative Building
- Rapid prototyping of structures
- Large-scale terrain modification
- Complex architectural designs

### Education
- Teaching programming concepts
- Learning coordinate systems
- Understanding 3D geometry

### Game Development
- Quick map creation
- Testing game mechanics
- Prototyping level designs

### Art & Creativity
- Pixel art in 3D
- Sculptures and statues
- Detailed decorations

## 🐛 Troubleshooting

### Common Issues

**RCON Connection Failed**
- Ensure Minecraft server is running
- Verify RCON enabled in `server.properties`
- Check password matches

**WorldEdit Commands Not Working**
- Verify WorldEdit plugin is loaded
- Check operator permissions
- Use comma-separated coordinates from console

**AI Can't See Tools**
- Verify MCP configuration is correct
- Check absolute paths (for Claude Desktop)
- Restart AI client

See [Complete Setup Guide](docs/COMPLETE_SETUP_GUIDE.md#troubleshooting) for more solutions.

## 📊 Development Status

**🎉 Project Complete and Production-Ready!**

See [SETUP_COMPLETE.md](SETUP_COMPLETE.md) for verification tests and detailed status.

### Completed ✅
- [x] WorldEdit command research (200+ commands)
- [x] MCP server implementation (21 tools, 6 resources)
- [x] RCON connection manager
- [x] Command sanitization and validation
- [x] All 21 tools implemented and tested
- [x] Documentation resources
- [x] Setup automation (one-command setup)
- [x] Comprehensive documentation
- [x] Cross-platform compatibility (macOS + Linux)
- [x] Docker Compose v1 and v2 support
- [x] WorldEdit 7.3.17 integration verified
- [x] End-to-end testing completed
- [x] All compatibility issues resolved

### Available for User Testing ✅
- [x] Complete setup verified on macOS (Darwin 24.6.0)
- [ ] Awaiting Linux user testing (all fixes applied)

### Future Enhancements 🔮
- [ ] Custom Minecraft plugin for direct API access
- [ ] WebSocket support for real-time feedback
- [ ] Schematic preview and validation
- [ ] Build queue management
- [ ] Multi-server support
- [ ] Web UI for monitoring

## 🤝 Contributing

Contributions welcome! Areas we'd love help with:
- Testing on different platforms
- Additional documentation and examples
- Bug reports and fixes
- Feature suggestions

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Credits

- **WorldEdit** by EngineHub - The powerful editing tool
- **MCP SDK** by Anthropic - Model Context Protocol
- **mcrcon** by Tiiffi - Python RCON library
- **PaperMC** - High-performance Minecraft server

## 📞 Support

- 📖 [Documentation](docs/)
- 🐛 [Report Issues](https://github.com/your-repo/vibecraft/issues)
- 💬 [Discussions](https://github.com/your-repo/vibecraft/discussions)

---

## 🎓 Team

**Research & Planning:**
- Comprehensive WorldEdit documentation and command mapping
- Architecture design and technology selection

**Engineering Team:**
- **Steve** (Junior Engineer) - Implementation planning
- **Cody** (Senior Engineer) - Technical review and architecture validation

**Implementation:**
- MCP server with complete WorldEdit integration
- Safety features and validation
- Documentation and guides

---

**Built with ❤️ for the Minecraft and AI communities**

*Start building amazing structures with just your words!* 🏗️✨

---

## Quick Links

### User Guides
- [User Action Guide](docs/USER_ACTION_GUIDE.md) - Complete manual with troubleshooting
- [Complete Setup Guide](docs/COMPLETE_SETUP_GUIDE.md) - End-to-end setup
- [Minecraft Server Setup](docs/MINECRAFT_SERVER_SETUP.md) - Server configuration
- [MCP Server Docs](mcp-server/README.md) - MCP server documentation

### Development Reference
- [WorldEdit Command Reference](dev_docs/RESEARCH_WORLDEDIT_COMPLETE.md) - All 200+ commands
- [Implementation Plan](dev_docs/IMPLEMENTATION_PLAN.md) - Steve's plan
- [Technical Review](dev_docs/IMPLEMENTATION_PLAN_REVIEW.md) - Cody's review
- [Critical Missing Commands](dev_docs/CRITICAL_MISSING_COMMANDS.md) - Ultra-deep analysis
- [Original Requirements](dev_docs/INSTRUCTIONS.md) - Project specs
