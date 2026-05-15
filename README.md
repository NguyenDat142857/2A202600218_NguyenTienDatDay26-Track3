# MCP SQLite Data Server
Ảnh kết quả ![MCP Inspector](<MCP Inspector.png>)
## Student
- **Name:** 2A202600218_NguyenTienDat
- **Student ID:** 2A202600218
- **Lab:** FastMCP + SQLite Database Server

## Project Overview
This repository implements a polished Model Context Protocol server using FastMCP and SQLite. It exposes a small education dataset through three secure MCP tools and two schema resources.

## Included Deliverables
- `implementation/`: server implementation, database adapter, verification script, unit tests, and helper scripts
- `pseudocode/`: design notes and pseudocode for the main features
- `README.md`, `QUICKSTART.md`, `SUBMISSION.md`, `Tips.md`: clean documentation for setup and grading

## Features
- `search`: query rows with filters, ordering, pagination, and selected columns
- `insert`: create records safely with schema validation
- `aggregate`: compute `count`, `avg`, `sum`, `min`, `max` with optional grouping
- `schema://database`: full database schema resource
- `schema://table/{table_name}`: per-table schema resource
- secure input validation and parameterized SQL execution
- sample dataset with students, courses, and enrollments
- verification script and unit tests

## Quick Start
```bash
cd implementation
pip install -r requirements.txt
python init_db.py
python verify_server.py
python mcp_server.py
```

## Run the Server
- Start the server with: `python mcp_server.py`
- Inspect the server using `start_inspector.bat` on Windows or `npx @modelcontextprotocol/inspector python mcp_server.py`
- Connect any MCP-aware client to call the tools and resources

## Core Files
- `implementation/mcp_server.py`: MCP server entry point
- `implementation/db.py`: SQLite adapter with validation and query execution
- `implementation/init_db.py`: schema creation and sample seeding
- `implementation/verify_server.py`: verification script
- `implementation/tests/test_server.py`: unit tests
- `implementation/CLIENT_SETUP.md`: client configuration examples
- `implementation/demo_examples.md`: demo-ready tool examples

## Data Model
### students
- `id`, `name`, `cohort`, `email`, `score`

### courses
- `id`, `code`, `name`, `credits`

### enrollments
- `id`, `student_id`, `course_id`, `grade`, `enrolled_date`

## Example Requests
### Search all students
```json
{
  "table": "students"
}
```

### Search cohort A1
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
    "name": "Demo Student",
    "cohort": "A3",
    "email": "demo.student@example.com",
    "score": 92.5
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

## Resources
- `schema://database`
- `schema://table/students`
- `schema://table/courses`
- `schema://table/enrollments`

## Notes
- Re-run `python init_db.py` to reset seed data
- Use absolute paths for MCP client configs
- Validate the server locally before client integration

## Documentation
See `implementation/README.md` for more details, usage examples, and troubleshooting.
