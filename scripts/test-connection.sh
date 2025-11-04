#!/bin/bash
# Test RCON connection

echo "Testing RCON connection..."
echo ""

# Test with docker rcon-cli
echo "Test 1: List players"
docker exec vibecraft-minecraft rcon-cli list

echo ""
echo "Test 2: Check WorldEdit version"
docker exec vibecraft-minecraft rcon-cli "version WorldEdit"

echo ""
echo "Test 3: WorldEdit test command"
docker exec vibecraft-minecraft rcon-cli "//calc 2+2"

echo ""
echo "✅ All tests complete!"
