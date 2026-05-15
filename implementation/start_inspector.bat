@echo off
REM Start MCP Inspector for SQLite Lab MCP Server
REM This script starts the MCP Inspector to test the server

echo Starting MCP Inspector for SQLite Lab MCP Server...
echo.

REM Get the absolute path to the current directory
set SCRIPT_DIR=%~dp0
set PYTHON_PATH=python
set SERVER_PATH=%SCRIPT_DIR%mcp_server.py

echo Server path: %SERVER_PATH%
echo.

REM Create npm cache directory if it doesn't exist
if not exist "%SCRIPT_DIR%.npm-cache" mkdir "%SCRIPT_DIR%.npm-cache"

REM Set npm cache location
set NPM_CONFIG_CACHE=%SCRIPT_DIR%.npm-cache

echo Running Inspector...
echo Press Ctrl+C to stop
echo.

npx -y @modelcontextprotocol/inspector %PYTHON_PATH% %SERVER_PATH%
