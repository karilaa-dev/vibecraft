#!/bin/bash
# Start VibeCraft MCP Server with HTTP/SSE Support (46 tools)

cd "$(dirname "$0")"

# Initialize pyenv if available
if command -v pyenv >/dev/null 2>&1; then
    eval "$(pyenv init -)"
fi

echo "Starting VibeCraft MCP Server (HTTP/SSE Mode)..."
echo "Server will run at http://127.0.0.1:8765/sse"
echo ""
echo "✨ Features:"
echo "  - ALL 46 tools from original server"
echo "  - All WorldEdit commands"
echo "  - Terrain analysis & generation"
echo "  - Building tools (symmetry, lighting, validation)"
echo "  - Furniture system with 66+ layouts"
echo "  - Multiple Claude instances can connect"
echo "  - Full debug visibility"
echo ""
echo "Press Ctrl+C to stop"
echo ""

uv run python server_http.py --port 8765
