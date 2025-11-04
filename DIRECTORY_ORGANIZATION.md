# VibeCraft Directory Organization

This document explains the organization of documentation in the VibeCraft project.

## Directory Structure

### `docs/` - Living Documentation (User Guides)

**Purpose:** Documentation that users actively reference for setup, configuration, and usage.

**Contents:**
- `USER_ACTION_GUIDE.md` - Complete user manual with troubleshooting
- `COMPLETE_SETUP_GUIDE.md` - End-to-end setup instructions
- `MINECRAFT_SERVER_SETUP.md` - Server configuration guide

**When to add files here:**
- User-facing guides and instructions
- Setup and configuration documentation
- Troubleshooting guides
- API or usage references
- Operational procedures

### `dev_docs/` - Development Documentation (Reference/Context)

**Purpose:** Historical context, research, planning documents, and development process artifacts.

**Contents:**
- `INSTRUCTIONS.md` - Original project requirements
- `IMPLEMENTATION_PLAN.md` - Steve's detailed implementation plan
- `IMPLEMENTATION_PLAN_REVIEW.md` - Cody's technical review
- `IMPLEMENTATION_COMPLETE.md` - Completion summary
- `RESEARCH_WORLDEDIT_COMPLETE.md` - All 200+ WorldEdit commands research
- `CRITICAL_MISSING_COMMANDS.md` - Ultra-deep analysis findings
- `COMPLETE_ANALYSIS_SUMMARY.md` - Analysis overview

**When to add files here:**
- Planning documents
- Research and analysis
- Implementation reviews
- Development process artifacts
- Historical context
- Technical deep-dives that aren't operational guides

### Root Level

**Purpose:** Key project files and automation scripts.

**Contents:**
- `README.md` - Project overview (stays at root)
- `setup-all.sh` - One-command automated setup
- `docker-compose.yml` - Docker configuration
- `LICENSE`, `.gitignore`, etc. - Standard project files

### `mcp-server/`

**Purpose:** MCP server implementation and its documentation.

**Contents:**
- `src/` - Python source code
- `README.md` - MCP server-specific documentation
- `requirements.txt` - Dependencies
- `.env.example` - Configuration template

### `scripts/`

**Purpose:** Helper scripts for common operations.

**Contents:**
- `start-minecraft.sh` - Start server
- `stop-minecraft.sh` - Stop server
- `test-connection.sh` - Test RCON connection
- `view-logs.sh` - View server logs

## Decision Guidelines

When creating a new markdown file, ask:

### Is it a user guide or operational document?
→ **Put it in `docs/`**
- Will users need this to operate VibeCraft?
- Is it a "how to" guide?
- Does it contain troubleshooting steps?
- Is it reference material for day-to-day use?

### Is it development context or planning?
→ **Put it in `dev_docs/`**
- Is it historical context?
- Was it created during development planning?
- Is it research or analysis?
- Is it a review or retrospective?
- Does it document the development process?

### Examples

**User guides (→ docs/):**
- "How to Set Up VibeCraft"
- "Troubleshooting Common Issues"
- "Command Reference Guide"
- "Configuration Options"
- "API Documentation"

**Development docs (→ dev_docs/):**
- "Requirements Analysis"
- "Implementation Plan"
- "Technical Review"
- "Research: WorldEdit Commands"
- "Architecture Decision Records"
- "Performance Analysis Results"

## Benefits of This Organization

1. **Clear Separation:** Users know where to find operational guides
2. **Historical Context:** Development process is preserved for reference
3. **Easy Maintenance:** Living docs are separate from historical records
4. **Onboarding:** New contributors can understand the development journey
5. **Reduced Clutter:** Main docs folder isn't overwhelmed with planning documents

## Updating Documentation

### When moving files:
1. Update all links in README.md
2. Update links in other documentation files
3. Check for hardcoded paths in code
4. Test that all links work

### When adding new files:
1. Decide: user guide or development context?
2. Place in appropriate directory
3. Add link to README.md in appropriate section
4. Update this guide if creating a new category

---

**Summary:**
- `docs/` = What users need NOW
- `dev_docs/` = How we got here and why
