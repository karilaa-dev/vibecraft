# Minecraft Server Setup Guide with WorldEdit

**Platform:** Linux/macOS
**Minecraft Version:** 1.21.x
**WorldEdit Version:** 7.3.17+
**Server Type:** PaperMC (recommended)

---

## Prerequisites

- Java 21 or higher (required for Minecraft 1.21+)
- At least 2GB RAM available
- Terminal/command line access
- Internet connection for downloads

---

## Step 1: Install Java

### macOS
```bash
# Using Homebrew
brew install openjdk@21

# Add to PATH
echo 'export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify installation
java --version
```

### Linux (Ubuntu/Debian)
```bash
# Install OpenJDK 21
sudo apt update
sudo apt install openjdk-21-jdk

# Verify installation
java --version
```

### Linux (Fedora/RHEL)
```bash
# Install OpenJDK 21
sudo dnf install java-21-openjdk

# Verify installation
java --version
```

---

## Step 2: Download PaperMC Server

```bash
# Create server directory
cd /Users/er/Repos/vibecraft
mkdir minecraft-server
cd minecraft-server

# Download PaperMC 1.21.3 (or latest 1.21.x version)
# Check https://papermc.io/downloads/paper for the latest build number
curl -o paper.jar https://api.papermc.io/v2/projects/paper/versions/1.21.3/builds/latest/downloads/paper-1.21.3.jar

# Alternative: Manual download
# Visit https://papermc.io/downloads/paper
# Download the latest 1.21.x version
```

---

## Step 3: Initial Server Setup

```bash
# Accept EULA
echo "eula=true" > eula.txt

# Create start script
cat > start.sh << 'EOF'
#!/bin/bash
java -Xms2G -Xmx2G -jar paper.jar --nogui
EOF

chmod +x start.sh

# Start server for first time (generates configs)
./start.sh
```

Wait for the server to fully start. You should see "Done!" in the console. Then stop it with `stop` command.

---

## Step 4: Configure RCON

Edit `server.properties`:

```bash
# Open server.properties
nano server.properties

# Set these values:
enable-rcon=true
rcon.password=YOUR_SECURE_PASSWORD_HERE
rcon.port=25575
rcon.broadcast-commands=false

# Optional: Configure server settings
gamemode=creative
difficulty=peaceful
spawn-protection=0
max-players=10
level-type=flat
# For flat world building:
# level-type=flat

# Save and exit (Ctrl+X, then Y, then Enter in nano)
```

**IMPORTANT:** Replace `YOUR_SECURE_PASSWORD_HERE` with a strong password. This will be used by the MCP server.

---

## Step 5: Download and Install WorldEdit

```bash
# Download WorldEdit for Bukkit/Paper
# Check https://dev.bukkit.org/projects/worldedit for latest version
curl -L -o plugins/worldedit.jar https://mediafilez.forgecdn.net/files/5797/655/worldedit-bukkit-7.3.10.jar

# Alternative: Use WorldEdit's official download
# Visit https://worldedit.enginehub.org/en/latest/
# Download the Bukkit version for your Minecraft version
```

---

## Step 6: Configure WorldEdit

```bash
# Start server to generate WorldEdit configs
./start.sh
```

Once server starts, stop it with `stop` command.

```bash
# Edit WorldEdit configuration
nano plugins/WorldEdit/config.yml
```

Key settings to verify:
```yaml
# Allow console commands (important for RCON)
use-scheduler-optimization: true

# Increase limits if needed
limits:
  max-blocks-changed:
    default: 1000000
  max-radius: 1000

# Enable all features
enable-inventory:
  enabled: true
```

---

## Step 7: Operator Permissions

When you first join the server, give yourself operator permissions:

```bash
# From server console:
op YOUR_MINECRAFT_USERNAME

# Or edit ops.json before starting:
echo '[{"uuid":"YOUR_UUID","name":"YOUR_USERNAME","level":4}]' > ops.json
```

You can find your UUID at: https://mcuuid.net/

---

## Step 8: Test RCON Connection

### Using Docker (Reference Implementation Method)
If using the itzg/minecraft-server Docker image:

```bash
docker exec -it mc rcon-cli "list"
```

### Using mcrcon (Native Installation)

Install mcrcon:
```bash
# macOS
brew install mcrcon

# Linux
# From source:
git clone https://github.com/Tiiffi/mcrcon.git
cd mcrcon
make
sudo make install
```

Test connection:
```bash
mcrcon -H localhost -P 25575 -p YOUR_PASSWORD "list"
```

You should see the list of online players (or "There are 0 online players").

---

## Step 9: Test WorldEdit via RCON

```bash
# Set position 1
mcrcon -H localhost -P 25575 -p YOUR_PASSWORD "//pos1 100,64,100"

# Set position 2
mcrcon -H localhost -P 25575 -p YOUR_PASSWORD "//pos2 110,74,110"

# Fill with stone
mcrcon -H localhost -P 25575 -p YOUR_PASSWORD "//set stone"
```

If you're in the game, you should see a 10x10x10 cube of stone appear!

---

## Step 10: Configure Server for Building

### Create a Flat Creative World

Edit `server.properties`:
```properties
level-type=flat
gamemode=creative
generate-structures=false
spawn-monsters=false
spawn-animals=false
```

### Set Specific Spawn Location

From console:
```bash
setworldspawn 0 64 0
```

---

## Step 11: Useful Server Commands

### Starting the Server
```bash
cd /Users/er/Repos/vibecraft/minecraft-server
./start.sh
```

### Stopping the Server
From console:
```bash
stop
```

### Viewing Logs
```bash
# Real-time log viewing
tail -f logs/latest.log

# Search logs for errors
grep ERROR logs/latest.log
```

### Backup World
```bash
# Stop server first!
tar -czf backup-$(date +%Y%m%d).tar.gz world world_nether world_the_end
```

---

## Step 12: Configure Firewall (if needed)

### macOS
```bash
# Allow Minecraft port
# System Settings > Network > Firewall > Options
# Add Java to allowed applications
```

### Linux (UFW)
```bash
# Allow Minecraft and RCON ports
sudo ufw allow 25565/tcp
sudo ufw allow 25575/tcp  # RCON - only if accessing remotely!
sudo ufw reload
```

**Security Note:** RCON port (25575) should NOT be exposed to the internet. Only allow local connections or use SSH tunneling for remote access.

---

## Troubleshooting

### Server Won't Start
- Check Java version: `java --version` (must be 21+)
- Check RAM: Ensure at least 2GB available
- Check logs: `cat logs/latest.log`

### RCON Connection Failed
- Verify `server.properties` has `enable-rcon=true`
- Check password is correct
- Ensure server is fully started ("Done!" message)
- Check firewall isn't blocking port 25575

### WorldEdit Not Working
- Verify plugin loaded: Look for "WorldEdit" in startup logs
- Check permissions: Ensure you're an operator (`op username`)
- Verify correct WorldEdit version for your Minecraft version

### WorldEdit Commands from Console Not Working
- Use comma-separated coordinates: `//pos1 X,Y,Z`
- Some commands require player context:
  ```bash
  execute as @p run //set stone
  ```

---

## Directory Structure

After setup, your directory should look like:
```
minecraft-server/
├── paper.jar
├── start.sh
├── eula.txt
├── server.properties
├── ops.json
├── plugins/
│   ├── worldedit.jar
│   └── WorldEdit/
│       └── config.yml
├── world/
├── logs/
│   └── latest.log
└── ... (other server files)
```

---

## Performance Optimization

### For Building/Creative Servers

Edit `paper-world-defaults.yml`:
```yaml
# Disable unnecessary features
entities:
  spawning:
    all-chunks-are-slime-chunks: false

# Optimize view distance for building
chunks:
  entity-per-chunk-save-limit:
    area_effect_cloud: 0
    arrow: 0

# Disable mob AI
entity-activation-range:
  animals: 0
  monsters: 0
  raiders: 0
  misc: 0
```

### JVM Flags for Better Performance

Update `start.sh`:
```bash
#!/bin/bash
java -Xms2G -Xmx2G \
  -XX:+UseG1GC \
  -XX:+ParallelRefProcEnabled \
  -XX:MaxGCPauseMillis=200 \
  -XX:+UnlockExperimentalVMOptions \
  -XX:+DisableExplicitGC \
  -XX:G1HeapRegionSize=32M \
  -XX:G1NewSizePercent=30 \
  -XX:G1MaxNewSizePercent=40 \
  -jar paper.jar --nogui
```

---

## Next Steps

1. ✅ Server is running with WorldEdit
2. ✅ RCON is configured and tested
3. ➡️ Set up MCP server (see MCP_SERVER_SETUP.md)
4. ➡️ Configure Claude Code integration
5. ➡️ Test VibeCraft with AI building!

---

## Quick Reference

### Essential Commands
```bash
# Start server
./start.sh

# Test RCON
mcrcon -H localhost -P 25575 -p PASSWORD "list"

# Test WorldEdit
mcrcon -H localhost -P 25575 -p PASSWORD "//pos1 0,64,0"

# View logs
tail -f logs/latest.log

# Stop server (from console)
stop
```

### Important Files
- `server.properties` - Server configuration
- `plugins/WorldEdit/config.yml` - WorldEdit settings
- `logs/latest.log` - Server logs
- `ops.json` - Operator permissions

---

**Setup Complete!** Your Minecraft server with WorldEdit is ready for VibeCraft integration.
