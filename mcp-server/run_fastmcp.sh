#!/bin/bash
# Run VibeCraft MCP Server

echo "Starting VibeCraft MCP Server..."
echo ""
echo "Choose mode:"
echo "1) Standard (stdio) - For single Claude instance"
echo "2) Shared (HTTP/SSE) - For multiple Claude instances with debug visibility (ALL 41 TOOLS)"
echo ""
read -p "Enter choice [1-2]: " choice

case $choice in
    1)
        echo "Starting stdio server..."
        /Users/er/.pyenv/versions/3.11.11/bin/uv run python __main__.py
        ;;
    2)
        echo "Starting HTTP/SSE server at http://127.0.0.1:8765/sse"
        echo "✨ ALL 41 TOOLS AVAILABLE ✨"
        echo "You can see all debug output here!"
        echo ""
        /Users/er/.pyenv/versions/3.11.11/bin/uv run python server_http.py --port 8765
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac