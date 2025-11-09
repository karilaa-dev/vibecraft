<p align="center">
  <img src="assets/vibecraft_logo.png" alt="VibeCraft logo" width="420" />
</p>

# VibeCraft

**AI-Powered WorldEdit for Minecraft**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Minecraft 1.21+](https://img.shields.io/badge/minecraft-1.21+-green.svg)](https://www.minecraft.net/)

> Build ambitious Minecraft creations through natural-language conversations with an AI assistant. VibeCraft connects Claude (and other MCP-aware clients) to WorldEdit over RCON, wrapping the full command surface in tooling designed for safe automation.

---

## Highlights

- 🎯 **Complete WorldEdit Coverage** – 200+ commands exposed as structured tools with guardrails.
- ⚡ **Fast Feedback Loop** – Direct RCON execution with command sanitisation and optional previews.
- 🤖 **AI-Ready Knowledge Base** – Token-optimised context files, specialist agent prompts, and reference workflows.
- 🛠️ **Practical Helpers** – Pattern/furniture placers, schematic management, spatial analysis, and terrain tools.
- 📚 **Documentation-First** – Setup playbooks, troubleshooting guides, and background research kept in-repo.

---

## Quick Start

### Requirements

- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Docker Desktop** with Docker Compose ([Download](https://www.docker.com/products/docker-desktop))
- **MCP-capable AI client**: [Claude Code](https://claude.com/claude-code), [Claude Desktop](https://claude.ai/download), or [Cursor](https://cursor.sh/)

### Installation

```bash
# Replace YOUR-USERNAME with your GitHub username/organization
git clone https://github.com/YOUR-USERNAME/vibecraft.git
cd vibecraft
./setup-all.sh
```

The setup script automatically:
- ✅ Creates Python virtual environment and installs dependencies
- ✅ Downloads and starts PaperMC 1.21.3 + WorldEdit 7.3.17 in Docker
- ✅ Configures RCON and generates secure password
- ✅ Creates Claude configuration file (`claude-code-config.json`)
- ✅ Tests all connections

**Time**: 5-10 minutes (mostly Minecraft server initialization)

### Configure Your AI Client

After `setup-all.sh` completes, you'll see:

```
✅ Setup complete!
RCON Password: XxXxXxXxXxXxXxXx
Configuration saved to: claude-code-config.json
```

#### Claude Desktop (macOS/Linux)

**macOS:**
```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Linux:**
```bash
nano ~/.config/Claude/claude_desktop_config.json
```

Copy the entire content from `claude-code-config.json` into your Claude Desktop configuration. If you have existing `mcpServers`, merge the `vibecraft` entry.

#### Claude Code (VSCode Extension)

1. Open VSCode Settings (Cmd/Ctrl + ,)
2. Search for "MCP"
3. Add server configuration from `claude-code-config.json`
4. Reload VSCode window

**Important:** Restart Claude completely after updating configuration.

#### System Prompt Setup

**What is SYSTEM_PROMPT.md?**
- Contains instructions for your AI assistant to act as a Minecraft building expert
- Teaches the AI how to use VibeCraft's WorldEdit tools effectively
- Works with any MCP-compatible AI client (Claude Code, Claude Desktop, Cursor, etc.)
- **Note**: This is for *using* VibeCraft (building in Minecraft), not for *developing* VibeCraft

**For Claude Code (VSCode Extension):**
```bash
# Copy the system prompt to CLAUDE.md in your project root
cp SYSTEM_PROMPT.md CLAUDE.md
```

**For other AI clients**: Consult your client's documentation on configuring system prompts with MCP servers.

### Verify Setup

Test the connection in Claude:

```
"Can you connect to the Minecraft server?"
"What WorldEdit commands are available?"
"Get server information"
```

If Claude responds with Minecraft server data, you're ready to build! 🎉

---

## Manual Setup

Prefer to configure components yourself? See [`docs/MINECRAFT_SERVER_SETUP.md`](docs/MINECRAFT_SERVER_SETUP.md) for detailed manual setup instructions including:
- Java and PaperMC installation
- WorldEdit plugin setup
- RCON configuration
- MCP server configuration

---

## Repository Structure

- **`mcp-server/`** – Core MCP server (Python package)
- **`context/`** – AI knowledge base (patterns, layouts, materials, guides)
- **`AGENTS/`** – Specialist Claude prompts (architect, planner, QA, etc.)
- **`SYSTEM_PROMPT.md`** – AI assistant instructions for using VibeCraft (copy to `CLAUDE.md` for Claude Code)
- **`docs/`** – Setup guides and references
- **`examples/`** – Example configurations and tutorials
- **`minecraft-data/`** – Docker volume for Minecraft server (world, logs, configs)
- **`scripts/`** – Helper scripts for starting/stopping server
- **`schemas/`** – Pre-built schematics for patterns

### Optional Reference Repos

These directories contain upstream documentation and reference implementations (not required for normal use):

- `reference-worldedit/` – WorldEdit command reference and examples
- `reference-rcon-mcp/` – Example RCON MCP implementations

---

## Features

### WorldEdit Integration

- **200+ commands** exposed as MCP tools
- Selection tools: `//pos1`, `//pos2`, `//expand`, `//contract`
- Building: `//set`, `//replace`, `//walls`, `//faces`
- Shapes: `//sphere`, `//cylinder`, `//pyramid`
- Clipboard: `//copy`, `//paste`, `//rotate`, `//flip`
- Terrain: `//smooth`, `//naturalize`, `//generate`
- History: `//undo`, `//redo`

### Advanced Tools

- **Furniture System** – 60+ pre-designed furniture pieces with automated placement
- **Pattern Library** – 70+ building patterns (roofs, windows, doors, pillars)
- **Building Templates** – Parametric structures (towers, cottages, barns)
- **Terrain Tools** – Analysis, generation, texturing, smoothing
- **Spatial Awareness** – V2 system for precise furniture and roof placement
- **Schematic Library** – Manage and place pre-built structures

### AI Knowledge Base

Files in `context/` provide the AI with:
- **7,662 Minecraft items** – Complete item database with search
- **Furniture catalog** – Build instructions and automated layouts
- **Building patterns** – Roofs, facades, structural elements
- **Terrain patterns** – Trees, rocks, ponds, vegetation
- **Scale reference** – Room dimensions, spacing guidelines
- **WorldEdit recipes** – Common command sequences

---

## Usage Examples

### Basic Building

```
User: "Build a 10x10 stone house with oak door"
Claude: *creates foundation, walls, roof, door using WorldEdit*
```

### Furniture Placement

```
User: "Add a dining table and chairs inside"
Claude: *scans room, places furniture at correct height*
```

### Terrain Shaping

```
User: "Create rolling hills behind the house"
Claude: *analyzes terrain, generates hills with proper texturing*
```

### Complex Structures

```
User: "Build a medieval tower with spiral stairs"
Claude: *uses building template, customizes height and materials*
```

---

## Documentation

| Topic | Reference |
| --- | --- |
| **Setup Guide** | `docs/MINECRAFT_SERVER_SETUP.md` |
| **AI Instructions** | `SYSTEM_PROMPT.md` |
| **Context Files** | `context/README.md` |
| **Examples** | `examples/` |
| **Specialist Agents** | `AGENTS/` |
| **Development History** | `dev_docs/` (gitignored, local only) |

---

## Troubleshooting

### Minecraft Server Won't Start

```bash
# Check Docker status
docker ps

# View logs
docker logs -f vibecraft-minecraft

# Restart server
docker restart vibecraft-minecraft
```

### RCON Connection Failed

```bash
# Test connection
docker exec vibecraft-minecraft rcon-cli list

# Check password
cat .rcon_password

# Verify environment
cat mcp-server/.env
```

### Claude Can't Connect

1. Verify Minecraft server is running: `docker ps`
2. Test RCON: `./scripts/test-connection.sh`
3. Check MCP configuration matches `claude-code-config.json`
4. Restart Claude completely
5. Check Claude logs for connection errors

### Need More Help?

- Check `docs/MINECRAFT_SERVER_SETUP.md` for detailed troubleshooting
- Review logs: `docker logs vibecraft-minecraft`
- Test RCON: `docker exec vibecraft-minecraft rcon-cli list`

---

## Contributing

We welcome contributions! Please review:
- [CONTRIBUTING.md](CONTRIBUTING.md) – Development workflow and standards
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) – Community guidelines

---

## License

This project is licensed under the [MIT License](LICENSE).

---

**Happy building!** 🧱

Need help? Open an issue or check the troubleshooting section above.
