#!/bin/bash
# View Minecraft server logs

echo "Showing Minecraft server logs..."
echo "Press Ctrl+C to exit"
echo ""

docker logs -f vibecraft-minecraft
