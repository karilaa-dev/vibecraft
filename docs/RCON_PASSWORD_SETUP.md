# RCON Password Setup and Management

Secure guide for setting up and managing RCON passwords for VibeCraft.

## Table of Contents

- [Quick Setup](#quick-setup)
- [Security Best Practices](#security-best-practices)
- [Password Generation](#password-generation)
- [Updating Passwords](#updating-passwords)
- [Troubleshooting](#troubleshooting)

---

## Quick Setup

### Step 1: Generate Secure Password

Generate a strong random password (recommended: 16-32 characters):

**macOS/Linux**:
```bash
# Generate 24-character random password
openssl rand -base64 24

# Alternative: using /dev/urandom
cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9!@#$%^&*' | fold -w 24 | head -n 1
```

**Windows (PowerShell)**:
```powershell
# Generate 24-character random password
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 24 | % {[char]$_})
```

**Online** (if no CLI available):
- Visit: https://bitwarden.com/password-generator/
- Settings: 24 characters, include letters, numbers, symbols
- ⚠️ **WARNING**: Only use trusted password generators

**Example Output**:
```
k3Jx9mP2nQ7wR8sL4tF6vY1h
```

### Step 2: Set Password in Minecraft Server

Edit `server.properties` in your Minecraft server directory:

```properties
# Enable RCON
enable-rcon=true

# Set RCON port (default: 25575)
rcon.port=25575

# Set the password you generated
rcon.password=k3Jx9mP2nQ7wR8sL4tF6vY1h
```

**Important**:
- No quotes around the password
- No spaces before/after `=`
- Must be on a single line

### Step 3: Restart Minecraft Server

```bash
# Stop server gracefully
# In Minecraft console, type:
stop

# Wait for server to fully stop, then start again
./start.sh  # or however you start your server
```

### Step 4: Configure VibeCraft

Add password to `mcp-server/.env`:

```bash
VIBECRAFT_RCON_HOST=127.0.0.1
VIBECRAFT_RCON_PORT=25575
VIBECRAFT_RCON_PASSWORD=k3Jx9mP2nQ7wR8sL4tF6vY1h
```

**OR** add to MCP client configuration:

```json
{
  "mcpServers": {
    "vibecraft": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.vibecraft.server"],
      "cwd": "/path/to/vibecraft/mcp-server",
      "env": {
        "VIBECRAFT_RCON_HOST": "127.0.0.1",
        "VIBECRAFT_RCON_PORT": "25575",
        "VIBECRAFT_RCON_PASSWORD": "k3Jx9mP2nQ7wR8sL4tF6vY1h"
      }
    }
  }
}
```

### Step 5: Test Connection

```bash
cd mcp-server
uv run python -m src.vibecraft.server
```

**Expected Output**:
```
Testing RCON connection...
✅ RCON connection successful!
✅ WorldEdit 7.3.0 detected
🚀 VibeCraft MCP Server Ready!
```

---

## Security Best Practices

### ✅ DO

1. **Use Strong Passwords**
   - Minimum 16 characters
   - Include uppercase, lowercase, numbers, symbols
   - Generate randomly (don't create manually)

2. **Store Securely**
   - Use `.env` file (add to `.gitignore`)
   - Use password managers (1Password, Bitwarden, LastPass)
   - Encrypt backups containing passwords

3. **Limit Access**
   - Don't share RCON passwords
   - Use different passwords for different servers
   - Rotate passwords periodically (every 3-6 months)

4. **Protect `.env` Files**
   - Add `.env` to `.gitignore`
   - Never commit to version control
   - Set file permissions: `chmod 600 .env`

5. **Use Network Security**
   - Bind RCON to `127.0.0.1` (local only) when possible
   - Use firewall rules to restrict RCON port access
   - Consider SSH tunnels for remote connections

### ❌ DON'T

1. **Don't Use Weak Passwords**
   - ❌ "minecraft"
   - ❌ "password123"
   - ❌ "admin"
   - ❌ Short passwords (<16 characters)

2. **Don't Expose Passwords**
   - ❌ Commit `.env` to git
   - ❌ Share in screenshots
   - ❌ Include in logs
   - ❌ Paste in public chat/forums

3. **Don't Reuse Passwords**
   - ❌ Same password for multiple servers
   - ❌ Same password as other services

4. **Don't Leave Defaults**
   - ❌ Keep the example password from tutorials
   - ❌ Skip password setup ("I'll do it later")

---

## Password Generation

### Recommended Methods

#### Method 1: OpenSSL (Most Secure)

```bash
# 24-character base64 password
openssl rand -base64 24
# Output: k3Jx9mP2nQ7wR8sL4tF6vY1h

# 32-character base64 password (extra secure)
openssl rand -base64 32
# Output: k3Jx9mP2nQ7wR8sL4tF6vY1hN9mK2pL7qR6s
```

#### Method 2: /dev/urandom (Linux/macOS)

```bash
# Alphanumeric + symbols
cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9!@#$%^&*()_+-=' | fold -w 24 | head -n 1

# Alphanumeric only (safer for config files)
cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 24 | head -n 1
```

#### Method 3: Python

```bash
python3 -c "import secrets, string; print(''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(24)))"
```

#### Method 4: Password Manager

Use built-in password generator from:
- 1Password: Settings → Password Generator → 24 characters
- Bitwarden: Tools → Password Generator → 24 characters
- LastPass: Generate → 24 characters

### Password Strength

| Length | Strength | Use Case |
|--------|----------|----------|
| 8-12 | Weak | ❌ Not recommended |
| 13-15 | Moderate | ⚠️ Minimum acceptable |
| 16-23 | Strong | ✅ Good for local servers |
| 24-31 | Very Strong | ✅ Recommended for all servers |
| 32+ | Maximum | ✅ Best for public/remote servers |

---

## Updating Passwords

### When to Update

**Scheduled Rotation** (Recommended):
- Every 3-6 months for routine security
- Set calendar reminder

**Immediate Update Required**:
- Password exposed (screenshot, log, chat)
- Unauthorized access detected
- Staff member leaves with access
- Server compromise suspected

### Update Procedure

#### Step 1: Generate New Password

```bash
openssl rand -base64 24
```

Save to password manager immediately.

#### Step 2: Update Minecraft Server

1. Stop Minecraft server:
   ```bash
   # In Minecraft console:
   stop
   ```

2. Edit `server.properties`:
   ```properties
   rcon.password=NEW_PASSWORD_HERE
   ```

3. Start Minecraft server:
   ```bash
   ./start.sh
   ```

#### Step 3: Update VibeCraft

Update `mcp-server/.env`:
```bash
VIBECRAFT_RCON_PASSWORD=NEW_PASSWORD_HERE
```

**OR** update MCP client config and restart client.

#### Step 4: Test New Password

```bash
cd mcp-server
uv run python -m src.vibecraft.server
```

Verify "✅ RCON connection successful!"

#### Step 5: Update All Instances

If you have multiple configurations:
- Claude Code → `.claude/mcp.json`
- Claude Desktop → `claude_desktop_config.json`
- Cursor → `.cursor/mcp.json`
- Any scripts/automation

---

## Troubleshooting

### Authentication Failed

**Error**: "RCON authentication failed"

**Solutions**:

1. **Verify Password Matches**:
   ```bash
   # Check Minecraft server.properties
   grep rcon.password server.properties

   # Check VibeCraft .env
   grep VIBECRAFT_RCON_PASSWORD mcp-server/.env

   # Passwords must match exactly (case-sensitive)
   ```

2. **Check for Hidden Characters**:
   - No spaces before/after password
   - No quotes around password
   - No line breaks in password
   - Copy-paste carefully to avoid hidden characters

3. **Test with mcrcon**:
   ```bash
   # Install mcrcon
   brew install mcrcon  # macOS
   # or: sudo apt-get install mcrcon  # Linux

   # Test connection
   mcrcon -H 127.0.0.1 -P 25575 -p "YOUR_PASSWORD" "list"
   ```

4. **Restart Both Servers**:
   ```bash
   # Restart Minecraft server
   stop
   ./start.sh

   # Restart VibeCraft/MCP client
   # (restart Claude Code/Desktop/Cursor)
   ```

### Password Contains Special Characters

**Problem**: Password with `#`, `"`, `'`, or other special characters causes issues

**Solutions**:

1. **Avoid Problematic Characters in Passwords**:
   ```bash
   # Generate alphanumeric-only password
   openssl rand -base64 24 | tr -d '+/='
   ```

2. **Quote Password in MCP Config** (if needed):
   ```json
   "VIBECRAFT_RCON_PASSWORD": "password-with-special-chars"
   ```

3. **Escape Characters in .env** (if needed):
   ```bash
   # If password has #
   VIBECRAFT_RCON_PASSWORD=pass#word  # OK
   # If password has spaces (not recommended)
   VIBECRAFT_RCON_PASSWORD="pass word"  # Quote it
   ```

### Connection Refused

**Error**: "Connection refused" or "Failed to connect"

**Not a password issue!** See [CONFIGURATION.md](./CONFIGURATION.md#rcon-connection-failed) for connection troubleshooting.

### Password in Logs

**Problem**: Accidentally logged password (in terminal, screenshot, git commit)

**Immediate Actions**:

1. **Change Password Immediately**:
   ```bash
   openssl rand -base64 24  # Generate new password
   # Update server.properties and .env
   # Restart both servers
   ```

2. **Remove from Git History** (if committed):
   ```bash
   # WARNING: Rewrites history, coordinate with team
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch mcp-server/.env" \
     --prune-empty --tag-name-filter cat -- --all

   # Force push (use with caution!)
   git push origin --force --all
   ```

3. **Rotate All Affected Credentials**:
   - RCON password
   - Any other passwords in same file/commit

4. **Review Security**:
   - Add `.env` to `.gitignore`
   - Audit what else might be exposed
   - Consider full security review

---

## Multi-Server Setup

### Different Password Per Server

**Recommended**: Use unique passwords for each server.

**server1 `server.properties`**:
```properties
rcon.password=server1_k3Jx9mP2nQ7wR8sL
```

**server2 `server.properties`**:
```properties
rcon.password=server2_L4tF6vY1hN9mK2pL
```

**MCP Config**:
```json
{
  "mcpServers": {
    "vibecraft-server1": {
      "env": {
        "VIBECRAFT_RCON_PASSWORD": "server1_k3Jx9mP2nQ7wR8sL"
      }
    },
    "vibecraft-server2": {
      "env": {
        "VIBECRAFT_RCON_PASSWORD": "server2_L4tF6vY1hN9mK2pL"
      }
    }
  }
}
```

### Password Management Tools

**1Password**:
```
Item: VibeCraft RCON - Creative Server
Username: rcon
Password: [generated]
Notes: Minecraft server at 192.168.1.100:25575
```

**Bitwarden**:
```
Name: VibeCraft RCON Creative
Username: rcon
Password: [generated]
Notes: server.properties and mcp-server/.env
```

---

## Related Documentation

- [CONFIGURATION.md](./CONFIGURATION.md) - Complete configuration guide
- [README.md](../README.md) - Quick start
- [Minecraft RCON Docs](https://wiki.vg/RCON) - RCON protocol details

---

**Security Notice**: RCON provides administrative access to your Minecraft server. Treat RCON passwords with the same care as root/admin passwords.

**Last Updated**: November 9, 2025
