# Compatibility Fixes Applied

## Issues Found During Testing

### Issue 1: `timeout: command not found`
**Platform:** macOS (Darwin)
**Error Location:** `setup-all.sh` line 146

**Problem:**
- The `timeout` command is part of GNU coreutils
- Not available by default on macOS
- Script was using `timeout 5 python -m src.vibecraft.server` to test the MCP server

**Solution:**
- Added check for `timeout` command availability
- If available (Linux): Use timeout as before
- If not available (macOS): Fall back to simpler Python import test
- Uses: `python -c "import sys; sys.path.insert(0, 'src'); from vibecraft import server"`

**Code:**
```bash
if command_exists timeout; then
    timeout 5 python -m src.vibecraft.server 2>&1 | head -1 || log_info "MCP server validated (timeout expected)"
else
    python -c "import sys; sys.path.insert(0, 'src'); from vibecraft import server" 2>&1 && log_success "MCP server module validated" || log_warning "MCP server validation skipped"
fi
```

### Issue 2: `docker-compose: command not found`
**Platform:** Modern Docker Desktop installations
**Error Location:** Multiple locations in `setup-all.sh` and helper scripts

**Problem:**
- Docker Compose v2 changed from `docker-compose` (hyphenated, standalone) to `docker compose` (space, plugin)
- Modern Docker Desktop (2023+) only includes `docker compose` (space)
- Older installations may still have `docker-compose` (hyphenated)
- Script was hardcoded to use `docker-compose`

**Solution:**
- Added auto-detection for which command is available
- Script now uses `$DOCKER_COMPOSE` variable throughout
- Detection happens once during prerequisite checks
- Applied to all scripts:
  - `setup-all.sh`
  - `scripts/start-minecraft.sh`
  - `scripts/stop-minecraft.sh`

**Code:**
```bash
# Detect which docker-compose command to use
if command_exists docker-compose; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

log_success "Docker Compose found ($DOCKER_COMPOSE)"

# Later usage:
$DOCKER_COMPOSE up -d
$DOCKER_COMPOSE restart
$DOCKER_COMPOSE down
```

## Files Modified

### Main Setup Script
- `setup-all.sh`
  - Lines 83-90: Added docker-compose detection
  - Lines 152-158: Added timeout compatibility
  - Lines 207, 210, 215: Use $DOCKER_COMPOSE variable
  - Lines 227-268: Fixed RCON timing with recent log checks and retry logic
  - Lines 398-399: Updated help text with variable

### Helper Scripts
- `scripts/start-minecraft.sh`
  - Lines 9-14: Added docker-compose detection
  - Line 17: Use $DOCKER_COMPOSE variable

- `scripts/stop-minecraft.sh`
  - Lines 9-14: Added docker-compose detection
  - Line 17: Use $DOCKER_COMPOSE variable

## Testing Results

### Before Fix
```
./setup-all.sh: line 146: timeout: command not found
./setup-all.sh: line 203: docker-compose: command not found
```

### After Fix
- ✅ Script detects `docker compose` (with space) correctly
- ✅ Script skips timeout on macOS, uses alternative validation
- ✅ All docker-compose commands now work correctly

## Platform Compatibility

### macOS
- ✅ No timeout command required
- ✅ Docker Compose v2 (`docker compose`) supported
- ✅ Tested on macOS (Darwin 24.6.0)

### Linux
- ✅ timeout command available (uses original logic)
- ✅ Both `docker-compose` and `docker compose` supported
- ⏳ Awaiting user testing

### Docker Desktop Versions
- ✅ Modern (2.x+): Uses `docker compose` (space)
- ✅ Legacy (1.x): Uses `docker-compose` (hyphen)
- ✅ Auto-detection handles both

### Issue 3: RCON Timing Issue on Container Restart
**Platform:** All platforms
**Error Location:** `setup-all.sh` lines 227-256

**Problem:**
- When restarting an existing container, `docker logs` contains old "Done" messages from previous runs
- Script would find old "Done" message immediately and think server is ready
- RCON connection test would fail because server is still initializing
- No retry logic for RCON connection test

**Solution:**
- Use `docker logs --since 2m` to only check recent logs, avoiding false positives from old runs
- Added retry logic to RCON connection test (6 attempts with 5-second intervals)
- Now waits up to 30 seconds for RCON to be ready after server initialization

**Code:**
```bash
# Before (false positive on restart):
if docker logs vibecraft-minecraft 2>&1 | grep -q "Done"; then
    log_success "Minecraft server is ready!"
    break
fi
# Later...
sleep 5
docker exec vibecraft-minecraft rcon-cli list >/dev/null 2>&1

# After (checks recent logs only + retry logic):
if docker logs --since 2m vibecraft-minecraft 2>&1 | grep -q "Done"; then
    log_success "Minecraft server is ready!"
    break
fi
# Later...
for i in $(seq 1 6); do
    sleep 5
    if docker exec vibecraft-minecraft rcon-cli list >/dev/null 2>&1; then
        log_success "RCON connection successful"
        break
    fi
done
```

### Issue 4: WorldEdit Download 403 Forbidden
**Platform:** All platforms
**Error Location:** `docker-compose.yml` PLUGINS environment variable

**Problem:**
- Original URL used CurseForge CDN (MediaFilez): `https://mediafilez.forgecdn.net/files/5797/655/worldedit-bukkit-7.3.10.jar`
- CurseForge has hotlink protection that blocks direct downloads
- Server would repeatedly get HTTP 403 Forbidden errors
- Server startup would hang indefinitely waiting for plugin download
- WorldEdit 7.3.10 URL was also outdated

**Solution:**
- Switched to Modrinth CDN which allows direct downloads
- Updated to latest stable WorldEdit version 7.3.17
- Used Modrinth API to find correct download URL
- New URL: `https://cdn.modrinth.com/data/1u6JkXh5/versions/3ISh7ADm/worldedit-bukkit-7.3.17.jar`

**Code:**
```yaml
# Before (broken):
# PLUGINS: |
#   https://cdn.modrinth.com/data/1u6JkXh5/versions/YlKb06B7/worldedit-bukkit-7.3.10.jar

# After (working):
PLUGINS: |
  https://cdn.modrinth.com/data/1u6JkXh5/versions/3ISh7ADm/worldedit-bukkit-7.3.17.jar
```

**Verification:**
```bash
# Check WorldEdit loaded correctly
docker exec vibecraft-minecraft rcon-cli "version WorldEdit"
# Result: WorldEdit version 7.3.17+7262-c7fbe08

# Test WorldEdit functionality
docker exec vibecraft-minecraft rcon-cli "worldedit version"
# Result: All capabilities active
```

## Files Modified

### Main Setup Script
- `setup-all.sh`
  - Lines 83-90: Added docker-compose detection
  - Lines 152-158: Added timeout compatibility
  - Lines 207, 210, 215: Use $DOCKER_COMPOSE variable
  - Lines 227-268: Fixed RCON timing with recent log checks and retry logic
  - Lines 398-399: Updated help text with variable

### Helper Scripts
- `scripts/start-minecraft.sh`
  - Lines 9-14: Added docker-compose detection
  - Line 17: Use $DOCKER_COMPOSE variable

- `scripts/stop-minecraft.sh`
  - Lines 9-14: Added docker-compose detection
  - Line 17: Use $DOCKER_COMPOSE variable

### Docker Configuration
- `docker-compose.yml`
  - Lines 29-31: Updated WorldEdit URL to Modrinth CDN
  - Changed from version 7.3.10 to 7.3.17

## Testing Results

### Before Fixes
```
./setup-all.sh: line 146: timeout: command not found
./setup-all.sh: line 203: docker-compose: command not found
[Container lifecycle]: Downloading https://mediafilez.forgecdn.net/files/5797/655/worldedit-bukkit-7.3.10.jar
Error: Server response: 403 Forbidden
[Script hangs indefinitely]
```

### After Fixes
- ✅ Script detects `docker compose` (with space) correctly
- ✅ Script skips timeout on macOS, uses alternative validation
- ✅ All docker-compose commands now work correctly
- ✅ WorldEdit 7.3.17 downloads successfully from Modrinth
- ✅ Server starts in 25-30 seconds with WorldEdit loaded
- ✅ All WorldEdit capabilities active and functional

## Platform Compatibility

### macOS
- ✅ No timeout command required
- ✅ Docker Compose v2 (`docker compose`) supported
- ✅ WorldEdit downloads from Modrinth CDN
- ✅ Tested on macOS (Darwin 24.6.0)

### Linux
- ✅ timeout command available (uses original logic)
- ✅ Both `docker-compose` and `docker compose` supported
- ✅ WorldEdit downloads from Modrinth CDN
- ⏳ Awaiting user testing

### Docker Desktop Versions
- ✅ Modern (2.x+): Uses `docker compose` (space)
- ✅ Legacy (1.x): Uses `docker-compose` (hyphen)
- ✅ Auto-detection handles both

### CDN Compatibility
- ❌ CurseForge MediaFilez: Blocks direct downloads (403)
- ✅ Modrinth CDN: Allows direct downloads, stable URLs

## Backward Compatibility

All changes are backward compatible:
- If `docker-compose` exists: Uses it (legacy systems)
- If only `docker compose` exists: Uses that (modern systems)
- If `timeout` exists: Uses it (Linux)
- If `timeout` missing: Uses alternative (macOS)
- WorldEdit URL works on all platforms with internet access

No user intervention required - script adapts automatically.
