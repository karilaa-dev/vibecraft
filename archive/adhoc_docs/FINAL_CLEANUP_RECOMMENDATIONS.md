# Final Cleanup Recommendations

**Date**: 2025-11-05
**Status**: Optional cleanups for consideration

---

## ✅ Already Clean

Good news! The major cleanup is complete:
- ✅ Dead imports removed
- ✅ Outdated dependencies removed
- ✅ Temporary docs archived
- ✅ GitHub infrastructure created
- ✅ Examples added
- ✅ CHANGELOG created

---

## 🤔 Optional Cleanups (Your Decision)

### 1. Experimental Server Files (Low Priority)

**Found**: Multiple experimental HTTP/SSE server implementations in `mcp-server/`:

```
mcp-server/
├── server_fastmcp_complete.py   (33KB) - FastMCP complete implementation
├── server_fastmcp.py            (11KB) - FastMCP experimental
├── run_shared_server.py         (11KB) - HTTP/SSE shared server
├── run_http.py                  (4KB)  - HTTP runner
├── run_debug.py                 (5KB)  - Debug runner
├── server_http.py               (moved to src/vibecraft/server_http.py)
├── extract_furniture_inventory.py (5KB) - One-time script
└── validate_furniture_layouts.py (5KB)  - One-time script
```

**Context**: These were experiments documented in `HTTP_SSE_SOLUTION.md` to get HTTP/SSE transport working. The main server (`src/vibecraft/server.py`) uses stdio transport and is the primary implementation.

**Options**:

**A. Keep as-is** (if you might use HTTP/SSE in future)
- Pros: Preserved for potential future use
- Cons: Clutters mcp-server/ directory

**B. Archive experimental servers** (recommended if sticking with stdio)
```bash
mkdir -p dev_docs/experimental_servers
mv mcp-server/server_fastmcp*.py dev_docs/experimental_servers/
mv mcp-server/run_shared_server.py dev_docs/experimental_servers/
mv mcp-server/run_http.py dev_docs/experimental_servers/
mv mcp-server/run_debug.py dev_docs/experimental_servers/
mv mcp-server/HTTP_SSE_SOLUTION.md dev_docs/experimental_servers/
```

**C. Delete if never planning HTTP/SSE**
- Only if you're 100% sure you'll never need them

**Recommendation**: **Option B (archive)** - Keeps them for reference but cleans up main directory

---

### 2. One-Time Processing Scripts (Low Priority)

**Found**: Scripts that look like they were used once during development:

```
mcp-server/
├── extract_furniture_inventory.py  - Extracted furniture data
└── validate_furniture_layouts.py   - Validated furniture JSON
```

**Options**:

**A. Archive** (recommended)
```bash
mkdir -p scripts/data_processing
mv mcp-server/extract_furniture_inventory.py scripts/data_processing/
mv mcp-server/validate_furniture_layouts.py scripts/data_processing/
```

**B. Keep** if you regenerate data regularly

**Recommendation**: **Option A (archive)** - Looks like one-time data processing

---

### 3. Temporary Processing Files (Medium Priority)

**Found**: Intermediate data files in root:

```
Root directory:
├── furniture.html                      (366KB) - HTML export of furniture?
├── minecraft_items_filtered_toon.txt   (105KB) - Intermediate TOON processing
└── minecraft_items_filtered.json       (138KB) - ✅ USED BY SERVER (KEEP!)
```

**Status**:
- ✅ `minecraft_items_filtered.json` - **KEEP** (referenced by server.py)
- ❌ `furniture.html` - NOT referenced anywhere
- ❌ `minecraft_items_filtered_toon.txt` - NOT referenced anywhere

**Options**:

**A. Delete unused files** (recommended)
```bash
rm furniture.html
rm minecraft_items_filtered_toon.txt
```

**B. Archive if might need for regeneration**
```bash
mkdir -p dev_docs/data_artifacts
mv furniture.html dev_docs/data_artifacts/
mv minecraft_items_filtered_toon.txt dev_docs/data_artifacts/
```

**Recommendation**: **Option A (delete)** - These look like temporary exports that served their purpose

---

### 4. Shell Scripts in mcp-server/ (Low Priority)

**Found**: Multiple shell scripts for different run modes:

```
mcp-server/
├── install_http_deps.sh   - Installs HTTP dependencies
├── run_fastmcp.sh         - Runs FastMCP server
├── run_server.sh          - Runs main server
├── start-vibecraft.sh     - Starts VibeCraft
├── tail-logs.sh           - Tails log files
└── setup.sh               - Setup script
```

**Status**: These are utilities, generally fine to keep

**Options**:

**A. Keep as-is** (recommended for utilities)

**B. Consolidate** if many are redundant
- Could move HTTP-specific scripts with experimental servers if archiving those

**Recommendation**: **Option A (keep)** - Utilities are useful

---

### 5. Placeholder GitHub URLs (HIGH PRIORITY - Needs Your Input!)

**Found**: `mcp-server/README.md` has placeholder URLs:

```markdown
Line 408-409:
- 🐛 [Report Issues](https://github.com/your-repo/vibecraft/issues)
- 💬 [Discussions](https://github.com/your-repo/vibecraft/discussions)
```

**Action Required**: Replace `your-repo` with actual GitHub organization/username

**This is the ONLY blocking item before public release!**

---

## 📋 Recommended Actions Summary

### High Priority (Do Before Release):
1. ✅ **Replace GitHub URLs** - Need actual repo path

### Medium Priority (Clean Up Nice-to-Have):
2. ✅ **Delete temp files**: `furniture.html`, `minecraft_items_filtered_toon.txt`

### Low Priority (Optional Organization):
3. 🤷 **Archive experimental servers** - If not using HTTP/SSE
4. 🤷 **Archive processing scripts** - If one-time use

---

## 🎯 Quick Cleanup Commands

If you want to do the medium + low priority cleanups:

```bash
# 1. Delete temporary processing files
rm furniture.html minecraft_items_filtered_toon.txt

# 2. Archive experimental servers
mkdir -p dev_docs/experimental_servers
mv mcp-server/server_fastmcp*.py dev_docs/experimental_servers/
mv mcp-server/run_shared_server.py dev_docs/experimental_servers/
mv mcp-server/run_http.py dev_docs/experimental_servers/
mv mcp-server/run_debug.py dev_docs/experimental_servers/
mv mcp-server/HTTP_SSE_SOLUTION.md dev_docs/experimental_servers/

# 3. Archive one-time processing scripts
mkdir -p scripts/data_processing
mv mcp-server/extract_furniture_inventory.py scripts/data_processing/
mv mcp-server/validate_furniture_layouts.py scripts/data_processing/

# 4. Update README.md in archived locations
echo "# Experimental Servers" > dev_docs/experimental_servers/README.md
echo "These are experimental HTTP/SSE implementations. The main server uses stdio transport." >> dev_docs/experimental_servers/README.md

echo "# Data Processing Scripts" > scripts/data_processing/README.md
echo "One-time scripts used to extract and validate furniture/item data." >> scripts/data_processing/README.md
```

**Time**: ~5 minutes

---

## ✅ What's Already Perfect

Don't touch these - they're exactly where they should be:

- ✅ Main server: `mcp-server/src/vibecraft/server.py`
- ✅ Tool modules: `mcp-server/src/vibecraft/tools/`
- ✅ Data files: `minecraft_items_filtered.json` (used by server)
- ✅ Documentation: All `*.md` files properly organized
- ✅ Examples: `examples/` directory
- ✅ GitHub infrastructure: `.github/`
- ✅ Core scripts: `setup-all.sh`, `run_server.sh`, `start-vibecraft.sh`

---

## 🎓 Summary

**Current State**: **98% Clean** ✨

**Remaining**:
- 1 HIGH priority item: Replace GitHub URLs (2 min)
- 2 MEDIUM priority items: Delete temp files (30 sec)
- 3 LOW priority items: Archive experiments (5 min)

**After these**: **100% Production Ready!** 🚀

---

**Generated**: 2025-11-05
**Status**: Final recommendations
**Your Decision Needed**: GitHub URLs, whether to archive experiments
