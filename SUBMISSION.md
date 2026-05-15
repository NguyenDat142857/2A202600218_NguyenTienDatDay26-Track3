# Lab Submission: SQLite MCP Server

## Student Information
- **Name:** 2A202600218_NguyenTienDat
- **Student ID:** 2A202600218
- **Date:** May 2026
- **Lab:** FastMCP + SQLite Database Server

## Project Summary
This repository delivers a complete MCP server implementation using FastMCP and SQLite. It includes secure query tools, schema resources, sample seed data, verification logic, and automated tests.

## Implementation Details

### Database Adapter (`implementation/db.py`)
- Reusable `SQLiteAdapter` class
- Strong validation for tables, columns, filters, and aggregate requests
- Parameterized SQL everywhere
- Safe support for `search`, `insert`, and `aggregate`

### Database Initialization (`implementation/init_db.py`)
- Creates a reproducible schema
- Seeds test-friendly data for students, courses, and enrollments
- Recreates the database cleanly on each run

### MCP Server (`implementation/mcp_server.py`)
- FastMCP server with stdio transport
- MCP tools: `search`, `insert`, `aggregate`
- MCP resources: `schema://database`, `schema://table/{table_name}`
- Friendly JSON responses and validation errors

### Verification (`implementation/verify_server.py`)
- End-to-end verification for schema discovery, search, insert, aggregate, and invalid requests
- Uses a temporary `test_lab.db` database so the main sample data remains intact

### Testing (`implementation/tests/test_server.py`)
- Automated unit tests for core database operations
- Covers valid results and invalid input handling

## Feature Checklist

### MCP Tools
- ✅ `search` with filters, ordering, pagination
- ✅ `insert` with schema validation
- ✅ `aggregate` with count, avg, sum, min, max

### MCP Resources
- ✅ `schema://database`
- ✅ `schema://table/{table_name}`

### Safety
- ✅ Input validation for table names and columns
- ✅ Operator whitelist and metric validation
- ✅ Parameterized SQL
- ✅ Clear error responses for invalid requests

### Verification
- ✅ Verification script included
- ✅ Unit test suite included
- ✅ Demo examples and client setup docs included

## How to Run
```bash
cd implementation
pip install -r requirements.txt
python init_db.py
python verify_server.py
python mcp_server.py
```

## Notes
- The code is structured for readability and reuse
- The implementation is intentionally simple and safe for classroom demos
- Use absolute paths when configuring MCP clients
