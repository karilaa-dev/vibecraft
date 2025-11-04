#!/bin/bash
# VibeCraft MCP Server Setup Script

set -e

echo "================================================"
echo "🎮 VibeCraft MCP Server Setup"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.10 or higher is required (found: $python_version)"
    exit 1
fi
echo "✅ Python $python_version found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ Pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your RCON password!"
    echo "   nano .env"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

echo "================================================"
echo "✅ VibeCraft MCP Server Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Minecraft server RCON credentials"
echo "   nano .env"
echo ""
echo "2. Ensure your Minecraft server is running with:"
echo "   - WorldEdit installed"
echo "   - RCON enabled in server.properties"
echo ""
echo "3. Test the server:"
echo "   source venv/bin/activate"
echo "   python -m src.vibecraft.server"
echo ""
echo "4. Configure your AI client (Claude Code, etc.)"
echo "   See README.md for integration instructions"
echo ""
echo "================================================"
