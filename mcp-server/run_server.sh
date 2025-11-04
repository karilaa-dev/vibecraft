#!/bin/bash
# VibeCraft MCP Server Launcher
# Choose how to run the server

echo "======================================="
echo "🎮 VibeCraft MCP Server Launcher"
echo "======================================="
echo ""
echo "Choose server mode:"
echo ""
echo "1) Standard (for Claude Desktop stdio)"
echo "2) Debug (stdio with visible logging)"
echo "3) Shared (HTTP/SSE for multiple clients)"
echo ""
echo -n "Enter choice [1-3]: "

read choice

case $choice in
    1)
        echo "Starting standard server..."
        /Users/er/.pyenv/versions/3.11.11/bin/uv run python -m src.vibecraft.server
        ;;
    2)
        echo "Starting debug server..."
        echo "Use this config in Claude Desktop:"
        echo '  "command": "python3",'
        echo '  "args": ["run_debug.py"],'
        echo ""
        python3 run_debug.py
        ;;
    3)
        echo "Starting shared HTTP/SSE server..."
        # Check if dependencies are installed in venv
        if /Users/er/.pyenv/versions/3.11.11/bin/uv run python -c "import sse_starlette" 2>/dev/null; then
            /Users/er/.pyenv/versions/3.11.11/bin/uv run python run_shared_server.py
        else
            echo ""
            echo "📦 Installing dependencies first..."
            ./install_http_deps.sh
            echo ""
            /Users/er/.pyenv/versions/3.11.11/bin/uv run python run_shared_server.py
        fi
        ;;
    *)
        echo "Invalid choice. Please run again and select 1, 2, or 3."
        exit 1
        ;;
esac