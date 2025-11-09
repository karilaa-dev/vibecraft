# SYSTEM_PROMPT.md Rename - Complete

**Date**: 2025-11-07
**Issue**: CLAUDE.md was confusing - it's for *using* VibeCraft (building in Minecraft), not for *developing* VibeCraft

---

## Problem

The repository had a file named `CLAUDE.md` that contained system instructions for AI assistants to use VibeCraft as a Minecraft building tool. This was confusing because:

1. **Developers** browsing the repo might think it's instructions for contributing to VibeCraft
2. **Users** might not understand it's meant to be copied for their AI client
3. The name was **too specific** to Claude (works with any MCP-compatible AI)

---

## Solution

**Renamed**: `CLAUDE.md` → `SYSTEM_PROMPT.md`

This makes it clear:
- ✅ It's a system prompt, not code documentation
- ✅ It's for **using** VibeCraft, not developing it
- ✅ Works with any MCP-compatible AI client (not just Claude)

Users copy/link `SYSTEM_PROMPT.md` to `CLAUDE.md` when setting up Claude Code.

---

## Changes Made

### 1. File Renamed ✅
```bash
CLAUDE.md → SYSTEM_PROMPT.md
```

### 2. README.md Updated ✅

**Added**: Clear "System Prompt Setup" section explaining:
- What SYSTEM_PROMPT.md is (for *using* VibeCraft, not developing)
- Works with any MCP-compatible AI client
- Specific instructions for Claude Code: `cp SYSTEM_PROMPT.md CLAUDE.md`

**Updated**: Repository structure and documentation table to reference `SYSTEM_PROMPT.md`

### 3. setup-all.sh Updated ✅

**Added**: System prompt setup reminder in final output
```bash
echo "🚀 Next Steps:"
echo "  2. Set up system prompt (see README.md for your AI client)"
echo "     • Claude Code: cp SYSTEM_PROMPT.md CLAUDE.md"
echo "     • Other clients: See their documentation"
```

**Note**: Does NOT auto-create CLAUDE.md (user's AI client choice, not ours to assume)

### 4. .gitignore Updated ✅

**Added**: `CLAUDE.md` to gitignore
```gitignore
# Auto-generated system prompt (copy of SYSTEM_PROMPT.md)
CLAUDE.md
```

Why: It's auto-generated and users might customize it locally.

### 5. .mcp.json Updated ✅

**Before**:
```json
"claudeInstructions": "CLAUDE.md"
```

**After**:
```json
"systemPrompt": "SYSTEM_PROMPT.md",
"note": "Copy SYSTEM_PROMPT.md to CLAUDE.md when using Claude Code"
```

---

## Files Modified

1. ✅ `CLAUDE.md` → `SYSTEM_PROMPT.md` (renamed)
2. ✅ `README.md` - Added system prompt setup section (3 locations updated)
3. ✅ `setup-all.sh` - Added system prompt setup reminder to output
4. ✅ `.gitignore` - Ignores user-created CLAUDE.md
5. ✅ `.mcp.json` - Updated references
6. ✅ `.github/PULL_REQUEST_TEMPLATE.md` - Updated checklist
7. ✅ `mcp-server/QUICK_START.md` - Updated documentation links

---

## User Experience

### Before (Confusing) ❌
```
Repository structure:
├── CLAUDE.md          ← Is this for using or developing?
├── README.md
└── ...

Developer thinks: "Oh, this must be instructions for coding Claude integration"
User thinks: "Do I need to edit this? Is it specific to Claude only?"
```

### After (Clear) ✅
```
Repository structure:
├── SYSTEM_PROMPT.md   ← Clear: system prompt for AI assistant
├── README.md          ← Explains: copy to CLAUDE.md for Claude Code
└── ...

Developer thinks: "This is the AI system prompt for using VibeCraft"
User thinks: "I copy this to CLAUDE.md for my AI client, setup script does it for me"
```

---

## Setup Flow

**Run setup script**:
```bash
./setup-all.sh
# Sets up MCP server, Minecraft, generates config
# Reminds you to set up system prompt based on your AI client
```

**System prompt setup** (depends on your AI client):
```bash
# Claude Code (VSCode):
cp SYSTEM_PROMPT.md CLAUDE.md

# Claude Desktop, Cursor, other clients:
# Consult your client's documentation for system prompt configuration
```

---

## Benefits

1. ✅ **Clear naming** - No confusion about file purpose
2. ✅ **Works universally** - Not tied to specific AI client name
3. ✅ **User choice** - Doesn't assume which AI client they're using
4. ✅ **Gitignore** - Local customizations not committed
5. ✅ **Professional** - Better first impression for external contributors

---

## Verification

All references updated:
```bash
# Documentation references SYSTEM_PROMPT.md:
✅ README.md references SYSTEM_PROMPT.md (3 locations)
✅ .mcp.json references SYSTEM_PROMPT.md
✅ Repository structure section updated
✅ Documentation table updated
✅ Pull request template updated

# Setup flow:
✅ setup-all.sh reminds users to set up system prompt
✅ .gitignore ignores CLAUDE.md (user-created)
✅ README provides clear instructions per AI client
```

---

**Status**: ✅ Complete - SYSTEM_PROMPT.md is now the canonical system prompt file

**User action**: Manual (based on their AI client choice), not automatic
