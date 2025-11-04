#!/bin/bash
# Stop Minecraft server

# Load environment variables from .env if it exists
if [ -f "../.env" ]; then
    export $(cat ../.env | grep -v '^#' | xargs)
fi

# Detect docker-compose command
if command -v docker-compose >/dev/null 2>&1; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

echo "Stopping Minecraft server..."
$DOCKER_COMPOSE -f ../docker-compose.yml down

echo "Minecraft server stopped."
