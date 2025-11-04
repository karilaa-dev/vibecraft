# Setup Script Issues Analysis

Comprehensive analysis of setup-all.sh and related files.

## Critical Issues

### 1. Docker Compose File Modified Destructively ⚠️ HIGH PRIORITY

**Location:** `setup-all.sh` lines 150-155

```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/vibecraft_rcon_password_change_me/$RCON_PASSWORD/g" docker-compose.yml
else
    sed -i "s/vibecraft_rcon_password_change_me/$RCON_PASSWORD/g" docker-compose.yml
fi
```

**Problem:**
- If script is run multiple times, second run fails (placeholder already replaced)
- Script is not idempotent
- No way to restore original docker-compose.yml
- User can't easily change password later

**Impact:** Script cannot be safely re-run

**Solutions:**
1. Use `.env` file with docker-compose (RECOMMENDED)
2. Create `docker-compose.override.yml` with password
3. Keep original `docker-compose.yml.template` and generate `docker-compose.yml`
4. Use environment variable substitution in docker-compose.yml

**Recommended Fix:**
Use environment variable in docker-compose.yml:
```yaml
RCON_PASSWORD: "${VIBECRAFT_RCON_PASSWORD:-minecraft}"
```
Then export the variable before running docker-compose.

### 2. Volume Name Inconsistency ⚠️ MEDIUM PRIORITY

**Location:** `docker-compose.yml` line 37 vs `docs/USER_ACTION_GUIDE.md` lines 559-583

**Problem:**
- docker-compose.yml uses bind mount: `./minecraft-data:/data`
- USER_ACTION_GUIDE.md refers to named volume: `vibecraft-world`
- Backup/restore instructions won't work

**Impact:** User confusion, backup instructions incorrect

**Solution:** Update USER_ACTION_GUIDE.md to match actual implementation (bind mount)

### 3. No Container State Check ⚠️ MEDIUM PRIORITY

**Location:** `setup-all.sh` line 160

```bash
docker-compose up -d
```

**Problem:**
- Doesn't check if container is already running
- Doesn't check if old container exists but stopped
- Could cause conflicts or unexpected behavior

**Impact:** Confusing errors if run multiple times

**Solution:** Check and handle existing containers:
```bash
if docker ps -a --format '{{.Names}}' | grep -q '^vibecraft-minecraft$'; then
    log_info "Container already exists, checking status..."
    if docker ps --format '{{.Names}}' | grep -q '^vibecraft-minecraft$'; then
        log_success "Container already running"
    else
        log_info "Starting existing container..."
        docker-compose up -d
    fi
else
    log_info "Creating new container..."
    docker-compose up -d
fi
```

### 4. MCP Server .env.example Not Verified ⚠️ LOW PRIORITY

**Location:** `setup-all.sh` line 112

```bash
if [ ! -f ".env" ]; then
    log_info "Creating .env file..."
    cp .env.example .env
```

**Problem:**
- Doesn't check if .env.example exists before copying
- Will fail with confusing error if file missing

**Impact:** Cryptic error message

**Solution:**
```bash
if [ ! -f ".env" ]; then
    if [ ! -f ".env.example" ]; then
        log_error ".env.example not found in mcp-server/"
        exit 1
    fi
    log_info "Creating .env file..."
    cp .env.example .env
```

## Non-Critical Issues

### 5. Password Mismatch Not Detected ℹ️ INFO

**Location:** `setup-all.sh` lines 131-136

**Problem:**
- If .env already exists with different password than docker-compose.yml, they'll be out of sync
- Script extracts password from .env but doesn't verify it matches docker-compose.yml

**Impact:** Connection failures that are hard to debug

**Solution:** Add validation to ensure passwords match across all files

### 6. Claude Code Config Not Auto-Installed ℹ️ INFO

**Location:** `setup-all.sh` lines 254-269

**Problem:**
- Generates config file but requires manual installation
- Could be confusing for users

**Impact:** Extra manual step required

**Solution:** Could offer to automatically merge config (advanced, risky)
**Better:** Current approach is actually safer, keep as-is

### 7. No Cleanup on Failure ℹ️ INFO

**Location:** Entire script

**Problem:**
- If script fails partway through, leaves system in inconsistent state
- No rollback mechanism
- Uses `set -e` which exits immediately but doesn't cleanup

**Impact:** Manual cleanup required after failure

**Solution:** Add trap handler:
```bash
cleanup() {
    if [ $? -ne 0 ]; then
        log_error "Setup failed. Partial installation may exist."
        log_info "To clean up: docker-compose down; rm -rf mcp-server/venv"
    fi
}
trap cleanup EXIT
```

### 8. Hardcoded Paths in Generated Config ℹ️ INFO

**Location:** `setup-all.sh` lines 236-251

**Problem:**
- Uses `$(pwd)` to generate absolute paths
- If user moves project directory, config breaks

**Impact:** Config needs regeneration if project moved

**Solution:** Document this limitation (already done in guides)

## Documentation Issues

### 9. Volume Backup Instructions Incorrect ⚠️ MEDIUM PRIORITY

**Location:** `docs/USER_ACTION_GUIDE.md` lines 559-590

**Problem:**
- Instructions reference `vibecraft-world` volume
- Actual implementation uses `./minecraft-data` bind mount
- Backup commands won't work

**Solution:** Update documentation:
```bash
# Backup (bind mount version)
tar czf world-backup-$(date +%Y%m%d-%H%M%S).tar.gz minecraft-data/

# Restore (bind mount version)
docker-compose down
rm -rf minecraft-data
tar xzf world-backup-YYYYMMDD-HHMMSS.tar.gz
docker-compose up -d
```

### 10. Setup Script Not Mentioned in All Docs ℹ️ INFO

**Location:** Various docs

**Problem:**
- Some documentation still references manual setup as primary method
- setup-all.sh should be featured more prominently

**Solution:** Update docs to emphasize automated setup

## Verification Needed

### 11. Test Script on Clean System

**Items to verify:**
- [ ] Fresh Ubuntu installation
- [ ] Fresh macOS installation
- [ ] With Docker already running
- [ ] With Docker not running
- [ ] With partial installation (venv exists)
- [ ] With full installation (run twice)
- [ ] With wrong Python version
- [ ] Without Docker installed

### 12. Test Generated Config

**Items to verify:**
- [ ] Claude Desktop on macOS
- [ ] Claude Desktop on Linux
- [ ] Claude Code VSCode extension
- [ ] Config with existing mcpServers
- [ ] Config as only MCP server

## Priority Summary

### Must Fix (Before User Testing)
1. **Docker compose password injection** - Makes script non-idempotent
2. **Volume documentation mismatch** - Breaks backup instructions

### Should Fix (Before Release)
3. Container state checking
4. .env.example existence check
5. Password sync validation

### Nice to Have
6. Auto-install Claude config (risky, maybe skip)
7. Cleanup on failure trap
8. Comprehensive error messages

## Recommended Action Plan

1. **Immediate:**
   - Fix docker-compose password handling (use environment variables)
   - Fix volume documentation in USER_ACTION_GUIDE.md

2. **Before user testing:**
   - Add container state checking
   - Add .env.example validation
   - Test on clean systems

3. **Polish:**
   - Add failure cleanup trap
   - Improve error messages
   - Add password sync validation
