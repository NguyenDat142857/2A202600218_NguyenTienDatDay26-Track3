# MCP Client Setup Guide

A concise reference for configuring Claude Code, Gemini CLI, and Codex to use the SQLite MCP server.

## Prerequisites
- Python 3.8+ installed
- `fastmcp` installed: `pip install fastmcp`
- Database initialized: `python init_db.py`
- Local server verified: `python verify_server.py`

## Use Absolute Paths
Always use the absolute path to `mcp_server.py`.

Windows PowerShell:
```powershell
cd implementation
python -c "import os; print(os.path.abspath('mcp_server.py'))"
```

Mac/Linux:
```bash
cd implementation
pwd
```

Example:
`C:/LabVinUni/2A202600218_NguyenTienDatDay26-Track3/implementation/mcp_server.py`

## Claude Code

Official docs:
- https://code.claude.com/docs/en/mcp

Example `.mcp.json`:
```json
{
  "mcpServers": {
    "sqlite-lab": {
      "type": "stdio",
      "command": "python",
      "args": ["C:/LabVinUni/2A202600218_NguyenTienDatDay26-Track3/implementation/mcp_server.py"],
      "env": {}
    }
  }
}
```

Tips:
- Restart Claude code after editing config
- Confirm the Python interpreter has `fastmcp`
- Use the server alias `sqlite-lab`

## Gemini CLI

Official docs:
- https://github.com/google/gemini/gemini-cli/blob/main/docs/reference/configuration.md

Register the server:
```bash
gemini mcp add sqlite-lab python C:/LabVinUni/2A202600218_NguyenTienDatDay26-Track3/implementation/mcp_server.py --description "SQLite Lab MCP server" --timeout 10000
```

Verify:
```bash
gemini mcp list
gemini --allowed-mcp-server-names sqlite-lab --yolo -p "Use the sqlite-lab MCP server and show me all students in cohort A1"
```

Tips:
- Use hyphens for the alias
- Increase timeout if needed
- Confirm `python` path matches the environment with `fastmcp`

## Codex

Official docs:
- https://developers.openai.com/learn/docs-mcp

Example `~/.codex/config.toml`:
```toml
[mcp_servers.sqlite_lab]
command = "python"
args = ["C:/LabVinUni/2A202600218_NguyenTienDatDay26-Track3/implementation/mcp_server.py"]
```

Example `AGENTS.md` snippet:
```markdown
# Agent Instructions

Use the `sqlite_lab` MCP server for database schema inspection, record lookup, and aggregate calculations.
```

Verify:
```bash
codex mcp list
```

## MCP Inspector

Windows:
```bash
cd implementation
start_inspector.bat
```

Mac/Linux:
```bash
cd implementation
npx @modelcontextprotocol/inspector python mcp_server.py
```

## Troubleshooting
- `ENOENT`: use the full absolute path
- `ModuleNotFoundError: fastmcp`: run `pip install fastmcp`
- If the server fails, run `python mcp_server.py` directly to inspect the error message

## Quick test
1. Start the server manually:
   ```bash
   python mcp_server.py
   ```
2. If it starts without crashing, the config is likely correct.
3. Use Inspector or an MCP client to connect.
