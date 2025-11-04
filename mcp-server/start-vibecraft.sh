#!/bin/bash
# Start VibeCraft MCP Server with HTTP/SSE Support (34+ tools)

cd "$(dirname "$0")"

echo "Starting VibeCraft MCP Server (HTTP/SSE Mode)..."
echo "Server will run at http://127.0.0.1:8765/sse"
echo ""
echo "✨ Features:"
echo "  - ALL 34+ tools from original server"
echo "  - All WorldEdit commands"
echo "  - Terrain analysis & generation"
echo "  - Building tools (symmetry, lighting, validation)"
echo "  - Furniture system with 66+ layouts"
echo "  - Multiple Claude instances can connect"
echo "  - Full debug visibility"
echo ""
echo "Press Ctrl+C to stop"
echo ""

/Users/er/.pyenv/versions/3.11.11/bin/uv run python server_http.py --port 8765
