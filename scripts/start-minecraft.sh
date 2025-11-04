#!/bin/bash
# Start Minecraft server

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

echo "Starting Minecraft server..."
$DOCKER_COMPOSE -f ../docker-compose.yml up -d

echo "Waiting for server to be ready..."
sleep 10

echo "Server status:"
docker ps | grep vibecraft-minecraft

echo ""
echo "Minecraft server is starting!"
echo "View logs with: docker logs -f vibecraft-minecraft"
echo "Join at: localhost:25565"
