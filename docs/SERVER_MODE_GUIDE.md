# VibeCraft Server Mode Decision Tree

Choose the right configuration for your use case.

## Quick Decision Tree

```
What type of Minecraft server do you have?

├─ Single-Player / Local Testing
│  └─ Go to: [Single-Player Creative Mode](#single-player-creative-mode)
│
├─ Private Server (Friends/Small Group)
│  ├─ Creative Mode
│  │  └─ Go to: [Private Creative Server](#private-creative-server)
│  └─ Survival Mode
│     └─ Go to: [Private Survival Server](#private-survival-server)
│
├─ Public Server (Open to Players)
│  ├─ Creative Plots
│  │  └─ Go to: [Public Creative with Build Plots](#public-creative-with-build-plots)
│  ├─ Survival Server
│  │  └─ Go to: [Public Survival Server](#public-survival-server)
│  └─ Minigame/Event Server
│     └─ Go to: [Event/Minigame Server](#eventminigame-server)
│
└─ Development/Testing
   └─ Go to: [Development Mode](#development-mode)
```

---

## Configuration Profiles

### Single-Player Creative Mode

**Use When**:
- Playing solo in creative mode
- Testing builds locally
- Learning WorldEdit commands

**Recommended Settings**:

```bash
# .env - Single-player creative
VIBECRAFT_RCON_HOST=127.0.0.1
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=[generate secure password]
VIBECRAFT_RCON_TIMEOUT=10

# Safety: Moderate (you have undo!)
VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=true  # Allow //regen, etc.
VIBECRAFT_MAX_COMMAND_LENGTH=1000

# Build area: No limits (entire world available)

# Features: All enabled
VIBECRAFT_ENABLE_VERSION_DETECTION=true
VIBECRAFT_ENABLE_COMMAND_LOGGING=true
```

**Why These Settings**:
- ✅ Dangerous commands allowed (you can always undo)
- ✅ No build constraints (it's your world)
- ✅ Logging enabled (helpful for learning)
- ✅ Local-only connection (secure)

**MCP Client Config**:
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

### Private Creative Server

**Use When**:
- Playing with friends/family
- Small trusted group
- Private creative building

**Recommended Settings**:

```bash
# .env - Private creative server
VIBECRAFT_RCON_HOST=127.0.0.1  # or server IP if remote
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=[generate secure password]
VIBECRAFT_RCON_TIMEOUT=15  # Higher if remote

# Safety: Moderate (trusted users)
VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=true
VIBECRAFT_MAX_COMMAND_LENGTH=1000

# Build area: Optional soft limits
# VIBECRAFT_BUILD_MIN_X=-5000
# VIBECRAFT_BUILD_MAX_X=5000
# VIBECRAFT_BUILD_MIN_Y=-64
# VIBECRAFT_BUILD_MAX_Y=319
# VIBECRAFT_BUILD_MIN_Z=-5000
# VIBECRAFT_BUILD_MAX_Z=5000

# Features
VIBECRAFT_ENABLE_VERSION_DETECTION=true
VIBECRAFT_ENABLE_COMMAND_LOGGING=true
```

**Why These Settings**:
- ✅ Dangerous commands allowed (trusted group)
- ⚠️ Optional soft limits (prevent accidents, not malice)
- ✅ Logging enabled (track who did what)
- ⚠️ Higher timeout for network latency

**Security Notes**:
- Strong RCON password (24+ characters)
- Consider VPN for remote access
- Regular backups recommended

---

### Private Survival Server

**Use When**:
- Private survival world
- Want AI building assistance
- Maintain survival integrity

**Recommended Settings**:

```bash
# .env - Private survival server
VIBECRAFT_RCON_HOST=127.0.0.1
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=[generate secure password]
VIBECRAFT_RCON_TIMEOUT=15

# Safety: Higher (preserve survival experience)
VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=false  # Block //regen, etc.
VIBECRAFT_MAX_COMMAND_LENGTH=500

# Build area: Restrict to designated creative zone
VIBECRAFT_BUILD_MIN_X=10000
VIBECRAFT_BUILD_MAX_X=11000
VIBECRAFT_BUILD_MIN_Y=64
VIBECRAFT_BUILD_MAX_Y=128
VIBECRAFT_BUILD_MIN_Z=10000
VIBECRAFT_BUILD_MAX_Z=11000

# Features
VIBECRAFT_ENABLE_VERSION_DETECTION=true
VIBECRAFT_ENABLE_COMMAND_LOGGING=true
```

**Why These Settings**:
- ❌ Dangerous commands blocked (preserve world)
- ✅ Build area restricted (creative zone only)
- ✅ Stricter safety (avoid mistakes)
- ✅ Logging enabled (audit trail)

**Workflow**:
1. Designate creative building zone (e.g., X=10000-11000)
2. Build structures there with AI
3. Copy to survival world with //copy + //paste
4. Or manually rebuild in survival

---

### Public Creative with Build Plots

**Use When**:
- Public creative server
- Plot-based building system
- Multiple concurrent users

**Recommended Settings**:

```bash
# .env - Public creative server
VIBECRAFT_RCON_HOST=127.0.0.1
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=[generate very secure password]
VIBECRAFT_RCON_TIMEOUT=20

# Safety: Maximum (public server)
VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=false  # Block destructive commands
VIBECRAFT_MAX_COMMAND_LENGTH=500

# Build area: Restrict to creative plot region
VIBECRAFT_BUILD_MIN_X=5000
VIBECRAFT_BUILD_MAX_X=10000
VIBECRAFT_BUILD_MIN_Y=0
VIBECRAFT_BUILD_MAX_Y=256
VIBECRAFT_BUILD_MIN_Z=5000
VIBECRAFT_BUILD_MAX_Z=10000

# Features
VIBECRAFT_ENABLE_VERSION_DETECTION=true
VIBECRAFT_ENABLE_COMMAND_LOGGING=true
```

**Why These Settings**:
- ❌ Dangerous commands BLOCKED (prevent griefing)
- ✅ Strict build area limits (plot region only)
- ✅ Short commands only (reduce abuse)
- ✅ Strong password (public access)

**Additional Recommendations**:
- Use WorldGuard to protect spawn and plots
- Regular automated backups
- Monitor logs for suspicious activity
- Consider per-plot RCON instances (advanced)

---

### Public Survival Server

**Use When**:
- Public survival server
- AI for admin-controlled builds only
- Staff use only

**Recommended Settings**:

```bash
# .env - Public survival server (ADMIN USE ONLY)
VIBECRAFT_RCON_HOST=127.0.0.1
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=[generate very secure password]
VIBECRAFT_RCON_TIMEOUT=20

# Safety: Maximum security
VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=false
VIBECRAFT_MAX_COMMAND_LENGTH=300

# Build area: Restrict to staff build zone
VIBECRAFT_BUILD_MIN_X=50000
VIBECRAFT_BUILD_MAX_X=51000
VIBECRAFT_BUILD_MIN_Y=64
VIBECRAFT_BUILD_MAX_Y=128
VIBECRAFT_BUILD_MIN_Z=50000
VIBECRAFT_BUILD_MAX_Z=51000

# Features
VIBECRAFT_ENABLE_VERSION_DETECTION=true
VIBECRAFT_ENABLE_COMMAND_LOGGING=true
```

**Why These Settings**:
- ❌ Dangerous commands BLOCKED (preserve survival)
- ✅ Very strict limits (isolated build zone)
- ✅ Very short commands (reduce mistakes)
- ✅ ADMIN ONLY access (not for players)

**Security Notes**:
- **CRITICAL**: RCON password is admin-level access
- Don't share with regular players
- Keep .env secure
- Regular security audits

**Use Cases**:
- Building spawn structures
- Creating event arenas
- Admin infrastructure
- Later copy to survival world

---

### Event/Minigame Server

**Use When**:
- Building minigame arenas
- Event preparation
- Temporary structures

**Recommended Settings**:

```bash
# .env - Event/minigame server
VIBECRAFT_RCON_HOST=127.0.0.1
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=[generate secure password]
VIBECRAFT_RCON_TIMEOUT=15

# Safety: Lower during setup, higher during events
VIBECRAFT_ENABLE_SAFETY_CHECKS=true
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=true  # During setup
# VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=false  # During events
VIBECRAFT_MAX_COMMAND_LENGTH=1000

# Build area: Event region
VIBECRAFT_BUILD_MIN_X=0
VIBECRAFT_BUILD_MAX_X=500
VIBECRAFT_BUILD_MIN_Y=0
VIBECRAFT_BUILD_MAX_Y=256
VIBECRAFT_BUILD_MIN_Z=0
VIBECRAFT_BUILD_MAX_Z=500

# Features
VIBECRAFT_ENABLE_VERSION_DETECTION=true
VIBECRAFT_ENABLE_COMMAND_LOGGING=true
```

**Workflow**:
1. **Setup Phase**: Allow dangerous commands, build arenas quickly
2. **Testing Phase**: Switch to safer settings
3. **Event Phase**: Disable dangerous commands, monitor logs
4. **Cleanup Phase**: Re-enable for teardown

**Dynamic Configuration**:
```bash
# Setup: Copy .env.setup → .env
# Events: Copy .env.events → .env
# Restart VibeCraft MCP server after changing
```

---

### Development Mode

**Use When**:
- Testing VibeCraft features
- Developing new tools
- Debugging issues

**Recommended Settings**:

```bash
# .env - Development/testing
VIBECRAFT_RCON_HOST=127.0.0.1
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=dev_password_here  # Simpler for dev
VIBECRAFT_RCON_TIMEOUT=30  # Longer for debugging

# Safety: Minimal (faster testing)
VIBECRAFT_ENABLE_SAFETY_CHECKS=true  # Keep on for realistic testing
VIBECRAFT_ALLOW_DANGEROUS_COMMANDS=true
VIBECRAFT_MAX_COMMAND_LENGTH=10000  # Large for testing

# Build area: No limits

# Features: All enabled, verbose logging
VIBECRAFT_ENABLE_VERSION_DETECTION=true
VIBECRAFT_ENABLE_COMMAND_LOGGING=true
```

**Why These Settings**:
- ✅ All features enabled (test everything)
- ✅ Long commands allowed (test edge cases)
- ✅ Verbose logging (debugging)
- ⚠️ Use test server, not production!

**Best Practices**:
- Use separate test Minecraft server
- Regular snapshots before tests
- Keep production config separate

---

## Switching Modes

### Method 1: Multiple .env Files (Recommended)

Create environment-specific configs:

```bash
cd mcp-server
cp .env .env.production  # Save production config
cp .env .env.development # Save dev config
cp .env .env.events      # Save event config
```

**Switch modes**:
```bash
# Switch to development
cp .env.development .env
# Restart VibeCraft

# Switch to production
cp .env.production .env
# Restart VibeCraft
```

### Method 2: Multiple MCP Server Entries

Configure different modes in MCP client:

```json
{
  "mcpServers": {
    "vibecraft-dev": {
      "env": {
        "VIBECRAFT_ALLOW_DANGEROUS_COMMANDS": "true"
      }
    },
    "vibecraft-prod": {
      "env": {
        "VIBECRAFT_ALLOW_DANGEROUS_COMMANDS": "false",
        "VIBECRAFT_BUILD_MIN_X": "5000",
        "VIBECRAFT_BUILD_MAX_X": "10000"
      }
    }
  }
}
```

Switch by selecting different server in MCP client.

---

## Security by Mode

| Mode | Password Strength | Allow Dangerous | Build Limits | Public Access |
|------|-------------------|-----------------|--------------|---------------|
| Single-Player | Good (16+) | ✅ Yes | ❌ None | ❌ No |
| Private Creative | Strong (20+) | ✅ Yes | ⚠️ Optional | ❌ No |
| Private Survival | Strong (24+) | ❌ No | ✅ Required | ❌ No |
| Public Creative | Very Strong (24+) | ❌ No | ✅ Required | ✅ Yes |
| Public Survival | Very Strong (32+) | ❌ No | ✅ Strict | ⚠️ Admin Only |
| Events | Strong (24+) | ⚠️ Phase-dependent | ✅ Required | ⚠️ Phase-dependent |
| Development | Good (16+) | ✅ Yes | ❌ None | ❌ No |

---

## Related Documentation

- [CONFIGURATION.md](./CONFIGURATION.md) - Detailed configuration reference
- [RCON_PASSWORD_SETUP.md](./RCON_PASSWORD_SETUP.md) - Password security guide
- [README.md](../README.md) - Quick start

---

**Last Updated**: November 9, 2025
