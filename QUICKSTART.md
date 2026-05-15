# Quick Start

A fast path to run the MCP SQLite server and verify the implementation.

## Prerequisites
- Python 3.8 or higher
- pip package manager
- Node.js / npm for MCP Inspector if you want browser testing

## Install dependencies
```bash
cd implementation
pip install -r requirements.txt
```

## Initialize the database
```bash
python init_db.py
```

Expected output includes:
- `Database schema created successfully`
- `Database seeded successfully`
- summary counts for students, courses, enrollments

## Verify the implementation
```bash
python verify_server.py
```

If verification completes successfully, the core database adapter and query features are working.

## Run the MCP server
```bash
python mcp_server.py
```

The server runs over stdio and can be connected from MCP tools and clients.

## Inspect with MCP Inspector
### Windows
```bash
cd implementation
start_inspector.bat
```

### Mac/Linux
```bash
cd implementation
npx @modelcontextprotocol/inspector python mcp_server.py
```

## Example tool requests
### Search all students
```json
{
  "table": "students"
}
```

### Search students in cohort A1
```json
{
  "table": "students",
  "filters": [
    {"column": "cohort", "operator": "eq", "value": "A1"}
  ]
}
```

### Insert a student
```json
{
  "table": "students",
  "values": {
    "name": "New Student",
    "cohort": "A3",
    "email": "newstudent@example.com",
    "score": 90.0
  }
}
```

### Average score by cohort
```json
{
  "table": "students",
  "metric": "avg",
  "column": "score",
  "group_by": "cohort"
}
```

## Run tests
```bash
cd implementation
python tests/test_server.py -v
```

## Notes
- Use absolute paths for MCP client configuration
- Re-run `python init_db.py` to reset sample data
- The implementation is designed to safely validate requests and reject invalid input
