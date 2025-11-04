#!/bin/bash
# Install dependencies for HTTP/SSE mode

echo "Installing HTTP/SSE dependencies for VibeCraft..."

# Use UV to install in the virtual environment
echo "Using UV to install dependencies..."
/Users/er/.pyenv/versions/3.11.11/bin/uv pip install sse-starlette starlette uvicorn httpx

echo "✅ Dependencies installed!"
echo ""
echo "Now you can run:"
echo "  /Users/er/.pyenv/versions/3.11.11/bin/uv run python run_shared_server.py"