#!/bin/bash
# Script to tail the latest VibeCraft MCP server log

LOG_DIR="./logs"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Find the most recent log file
LATEST_LOG=$(ls -t "$LOG_DIR"/vibecraft_*.log 2>/dev/null | head -n1)

if [ -z "$LATEST_LOG" ]; then
    echo "No log files found in $LOG_DIR"
    echo "Waiting for VibeCraft server to start and create logs..."

    # Wait for a log file to appear
    while [ -z "$LATEST_LOG" ]; do
        sleep 1
        LATEST_LOG=$(ls -t "$LOG_DIR"/vibecraft_*.log 2>/dev/null | head -n1)
    done
fi

echo "Tailing log file: $LATEST_LOG"
echo "============================================"
tail -f "$LATEST_LOG"