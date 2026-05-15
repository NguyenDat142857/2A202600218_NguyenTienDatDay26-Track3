# MCP Client Tips

A short reference to connect the SQLite MCP server from popular MCP clients.

## Key advice
- Use absolute paths for the Python executable and server file
- Install `fastmcp` into the same Python interpreter you will run the server with
- Reinitialize the database with `python init_db.py` when you want a clean sample dataset
- Always verify the server with `python verify_server.py` before client integration

## Claude Code

Anthropic MCP docs:
- https://code.claude.com/docs/en/mcp

Example `.mcp.json` for project-local configuration:
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
- Use absolute paths to avoid `ENOENT` errors
- If Claude fails to start the server, confirm `python --version`
- Test resource access with `@sqlite-lab:schema://database`

## Gemini CLI

Gemini MCP docs:
- https://github.com/google/gemini/gemini-cli/blob/main/docs/reference/configuration.md

Add the server:
```bash
gemini mcp add sqlite-lab python C:/LabVinUni/2A202600218_NguyenTienDatDay26-Track3/implementation/mcp_server.py --description "SQLite Lab MCP server" --timeout 10000
```

Verify:
```bash
gemini mcp list
gemini --allowed-mcp-server-names sqlite-lab --yolo -p "Use the sqlite-lab MCP server and show me all students in cohort A1"
```

Tips:
- Use hyphens instead of underscores for the server alias
- If the server shows as disconnected, increase the timeout and check the path
- Confirm `fastmcp` is installed in the selected Python interpreter

## Codex

OpenAI Codex MCP docs:
- https://developers.openai.com/learn/docs-mcp

Example `~/.codex/config.toml`:
```toml
[mcp_servers.sqlite_lab]
command = "python"
args = ["C:/LabVinUni/2A202600218_NguyenTienDatDay26-Track3/implementation/mcp_server.py"]
```

Project instructions in `AGENTS.md`:
```markdown
Use the `sqlite_lab` MCP server for tasks that require database schema, record lookup, or aggregate calculations.
```

## MCP Inspector

Use Inspector to browse tools and resources in a browser.

### Windows
```bash
cd implementation
start_inspector.bat
```

### Linux / Mac
```bash
cd implementation
npx @modelcontextprotocol/inspector python mcp_server.py
```

Checklist:
- Tools appear: `search`, `insert`, `aggregate`
- Resources appear: `schema://database`, `schema://table/{table_name}`
- Valid search returns rows
- Invalid request returns a clear validation error

