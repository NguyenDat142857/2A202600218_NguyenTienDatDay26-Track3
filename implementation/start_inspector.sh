#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="python"
SERVER_PATH="$SCRIPT_DIR/mcp_server.py"
mkdir -p "$SCRIPT_DIR/.npm-cache"
export NPM_CONFIG_CACHE="$SCRIPT_DIR/.npm-cache"
echo "Starting MCP Inspector for SQLite Lab MCP Server..."
echo "Server path: $SERVER_PATH"

npx -y @modelcontextprotocol/inspector "$PYTHON" "$SERVER_PATH"
