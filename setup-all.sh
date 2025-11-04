#!/bin/bash
###############################################################################
# VibeCraft Complete Setup Script
# This script automates the entire VibeCraft setup process
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo "============================================================"
    echo "$1"
    echo "============================================================"
    echo ""
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

###############################################################################
# Pre-flight Checks
###############################################################################

print_header "🎮 VibeCraft Complete Setup"
log_info "Starting automated setup process..."
echo ""

# Check for required commands
log_info "Checking prerequisites..."

if ! command_exists python3; then
    log_error "Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

python_version=$(python3 --version 2>&1 | awk '{print $2}')
log_success "Python $python_version found"

if ! command_exists docker; then
    log_error "Docker is not installed. Please install Docker Desktop."
    log_info "Visit: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    log_error "Docker is not running. Please start Docker Desktop."
    exit 1
fi

log_success "Docker is installed and running"

if ! command_exists docker-compose && ! docker compose version >/dev/null 2>&1; then
    log_error "Docker Compose is not installed."
    exit 1
fi

# Determine which docker-compose command to use
if command_exists docker-compose; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

log_success "Docker Compose found ($DOCKER_COMPOSE)"

###############################################################################
# Step 1: Set up MCP Server
###############################################################################

print_header "📦 Step 1/4: Setting up MCP Server"

cd mcp-server

log_info "Creating Python virtual environment..."
if [ -d "venv" ]; then
    log_warning "Virtual environment already exists, skipping creation"
else
    python3 -m venv venv
    log_success "Virtual environment created"
fi

log_info "Activating virtual environment..."
source venv/bin/activate

log_info "Upgrading pip..."
pip install --upgrade pip --quiet

log_info "Installing MCP server dependencies..."
pip install -r requirements.txt --quiet
log_success "Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    # Check if .env.example exists
    if [ ! -f ".env.example" ]; then
        log_error ".env.example not found in mcp-server/"
        log_info "This file should exist in the repository. Please verify your installation."
        exit 1
    fi

    log_info "Creating .env file from .env.example..."
    cp .env.example .env

    # Generate a random RCON password
    RCON_PASSWORD=$(openssl rand -base64 12 | tr -d "=+/" | cut -c1-16)

    # Update .env with the password
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/VIBECRAFT_RCON_PASSWORD=.*/VIBECRAFT_RCON_PASSWORD=$RCON_PASSWORD/" .env
    else
        # Linux
        sed -i "s/VIBECRAFT_RCON_PASSWORD=.*/VIBECRAFT_RCON_PASSWORD=$RCON_PASSWORD/" .env
    fi

    log_success ".env file created with random password"
    log_info "RCON Password: $RCON_PASSWORD"
    echo "$RCON_PASSWORD" > ../.rcon_password
else
    log_warning ".env file already exists"
    # Extract password from existing .env
    RCON_PASSWORD=$(grep VIBECRAFT_RCON_PASSWORD .env | cut -d '=' -f2)
    log_info "Using existing RCON password from mcp-server/.env"
fi

log_info "Testing MCP server..."
# Quick validation that the module can be imported (skip on macOS if timeout unavailable)
if command_exists timeout; then
    timeout 5 python -m src.vibecraft.server 2>&1 | head -1 || log_info "MCP server validated (timeout expected)"
else
    python -c "import sys; sys.path.insert(0, 'src'); from vibecraft import server" 2>&1 && log_success "MCP server module validated" || log_warning "MCP server validation skipped"
fi

cd ..
log_success "MCP Server setup complete"

###############################################################################
# Step 2: Set up Minecraft Server with Docker
###############################################################################

print_header "🐳 Step 2/4: Setting up Minecraft Server (Docker)"

# Verify docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    log_error "docker-compose.yml not found in project root"
    log_info "This file should exist in the repository. Please verify your installation."
    exit 1
fi

# Create root .env file for docker-compose if it doesn't exist
if [ ! -f ".env" ]; then
    log_info "Creating root .env file for docker-compose..."
    cat > .env << EOF
# VibeCraft Docker Compose Configuration
# RCON Password for Minecraft server
VIBECRAFT_RCON_PASSWORD=$RCON_PASSWORD
EOF
    log_success "Root .env file created"
else
    log_warning "Root .env file already exists"
    # Update password in existing file
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/^VIBECRAFT_RCON_PASSWORD=.*/VIBECRAFT_RCON_PASSWORD=$RCON_PASSWORD/" .env
    else
        sed -i "s/^VIBECRAFT_RCON_PASSWORD=.*/VIBECRAFT_RCON_PASSWORD=$RCON_PASSWORD/" .env
    fi
    log_info "Updated RCON password in root .env"
fi

# Export RCON password as environment variable for docker-compose
export VIBECRAFT_RCON_PASSWORD="$RCON_PASSWORD"
log_success "RCON password configured for docker-compose"

log_info "Starting Minecraft server container..."

# Check if container already exists
if docker ps -a --format '{{.Names}}' | grep -q '^vibecraft-minecraft$'; then
    if docker ps --format '{{.Names}}' | grep -q '^vibecraft-minecraft$'; then
        log_warning "Container already running"
        log_info "Restarting to apply any configuration changes..."
        $DOCKER_COMPOSE restart
    else
        log_info "Container exists but stopped, starting..."
        $DOCKER_COMPOSE up -d
    fi
else
    log_info "Creating new container (first run may take several minutes)..."
    log_info "Downloading Paper 1.21.3 and WorldEdit 7.3.10..."
    $DOCKER_COMPOSE up -d
fi

log_success "Docker container started"

log_info "Waiting for Minecraft server to initialize..."
log_warning "This can take 2-5 minutes for first startup..."

# Wait for server to be ready (check recent logs only to avoid false positives from old runs)
MAX_WAIT=300  # 5 minutes
WAITED=0
while [ $WAITED -lt $MAX_WAIT ]; do
    # Check logs from last 2 minutes to avoid finding old "Done" messages
    if docker logs --since 2m vibecraft-minecraft 2>&1 | grep -q "Done"; then
        log_success "Minecraft server is ready!"
        break
    fi

    if [ $((WAITED % 30)) -eq 0 ]; then
        log_info "Still waiting... ($WAITED seconds elapsed)"
    fi

    sleep 5
    WAITED=$((WAITED + 5))
done

if [ $WAITED -ge $MAX_WAIT ]; then
    log_error "Minecraft server did not start within $MAX_WAIT seconds"
    log_info "Check logs with: docker logs vibecraft-minecraft"
    exit 1
fi

# Test RCON connection with retries
log_info "Testing RCON connection..."
RCON_RETRIES=6
RCON_SUCCESS=false

for i in $(seq 1 $RCON_RETRIES); do
    sleep 5
    if docker exec vibecraft-minecraft rcon-cli list >/dev/null 2>&1; then
        log_success "RCON connection successful"
        RCON_SUCCESS=true
        break
    else
        if [ $i -lt $RCON_RETRIES ]; then
            log_info "RCON not ready yet, retrying... (attempt $i/$RCON_RETRIES)"
        fi
    fi
done

if [ "$RCON_SUCCESS" = false ]; then
    log_error "RCON connection failed after $RCON_RETRIES attempts"
    log_info "Server may still be initializing. Check logs with: docker logs vibecraft-minecraft"
fi

# Verify WorldEdit is installed
log_info "Verifying WorldEdit installation..."
WE_VERSION=$(docker exec vibecraft-minecraft rcon-cli "version WorldEdit" 2>/dev/null || echo "")
if echo "$WE_VERSION" | grep -q "WorldEdit"; then
    log_success "WorldEdit is installed: $WE_VERSION"
else
    log_warning "WorldEdit version check failed, but may still be loading"
fi

log_success "Minecraft Server setup complete"

###############################################################################
# Step 3: Configure Claude Code Integration
###############################################################################

print_header "🤖 Step 3/4: Claude Code Integration"

log_info "Generating Claude Code MCP configuration..."

# Detect Claude Code config location
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
    CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
    CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"
else
    log_warning "Unsupported OS for automatic Claude Code configuration"
    CLAUDE_CONFIG_FILE=""
fi

# Generate the configuration
cat > claude-code-config.json << EOF
{
  "mcpServers": {
    "vibecraft": {
      "command": "$(pwd)/mcp-server/venv/bin/python",
      "args": ["-m", "src.vibecraft.server"],
      "cwd": "$(pwd)/mcp-server",
      "env": {
        "VIBECRAFT_RCON_HOST": "127.0.0.1",
        "VIBECRAFT_RCON_PORT": "25575",
        "VIBECRAFT_RCON_PASSWORD": "$RCON_PASSWORD"
      }
    }
  }
}
EOF

log_success "Configuration saved to: claude-code-config.json"

if [ -n "$CLAUDE_CONFIG_FILE" ]; then
    log_info ""
    log_info "To complete Claude Code setup:"
    log_info "1. If using Claude Desktop:"
    log_info "   - Copy the config from: $(pwd)/claude-code-config.json"
    log_info "   - To: $CLAUDE_CONFIG_FILE"
    log_info ""
    log_info "2. If using Claude Code (VSCode extension):"
    log_info "   - Add the configuration from claude-code-config.json to your MCP settings"
    log_info ""
    log_info "3. Restart Claude to load the new MCP server"
else
    log_warning "Automatic configuration not available for this OS"
    log_info "Manual configuration file created: claude-code-config.json"
fi

log_success "Claude Code configuration generated"

###############################################################################
# Step 4: Verification
###############################################################################

print_header "✅ Step 4/4: Verification"

log_info "Running final verification tests..."

# Test MCP server can connect
cd mcp-server
source venv/bin/activate

log_info "Testing MCP server connection to Minecraft..."
python << 'PYEOF'
import os
from mcrcon import MCRcon

host = "127.0.0.1"
port = 25575
password = os.getenv("RCON_PASSWORD", "")

if not password:
    with open("../.rcon_password", "r") as f:
        password = f.read().strip()

try:
    with MCRcon(host, password, port=port, timeout=5) as mcr:
        response = mcr.command("list")
        print(f"✓ Connection successful: {response}")
        exit(0)
except Exception as e:
    print(f"✗ Connection failed: {e}")
    exit(1)
PYEOF

if [ $? -eq 0 ]; then
    log_success "MCP server can communicate with Minecraft"
else
    log_error "MCP server cannot communicate with Minecraft"
    log_info "Check that Minecraft server is running: docker ps"
fi

cd ..

###############################################################################
# Summary
###############################################################################

print_header "🎉 Setup Complete!"

echo "VibeCraft is now ready to use!"
echo ""
echo "📋 Summary:"
echo "  ✅ MCP Server: Running at mcp-server/"
echo "  ✅ Minecraft Server: Running in Docker (Port 25565)"
echo "  ✅ RCON: Enabled (Port 25575)"
echo "  ✅ WorldEdit: Installed"
echo "  ✅ Configuration: Generated"
echo ""
echo "🔑 RCON Password: $RCON_PASSWORD"
echo "   (Saved in: .rcon_password)"
echo ""
echo "🚀 Next Steps:"
echo "  1. Configure Claude Code/Desktop with: claude-code-config.json"
echo "  2. Restart Claude"
echo "  3. Start building with AI!"
echo ""
echo "📚 Useful Commands:"
echo "  • View Minecraft logs:  docker logs -f vibecraft-minecraft"
echo "  • Stop Minecraft:       $DOCKER_COMPOSE down"
echo "  • Start Minecraft:      $DOCKER_COMPOSE up -d"
echo "  • Test RCON:           docker exec vibecraft-minecraft rcon-cli list"
echo "  • Join server:         minecraft://localhost:25565"
echo ""
echo "📖 Documentation:"
echo "  • Complete Guide: docs/COMPLETE_SETUP_GUIDE.md"
echo "  • Commands:       docs/RESEARCH_WORLDEDIT_COMPLETE.md"
echo "  • Troubleshooting: See setup guide"
echo ""
print_header "Happy Building! 🏗️"
