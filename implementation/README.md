# SQLite MCP Server

A production-ready Model Context Protocol (MCP) server built with FastMCP and SQLite.

This project demonstrates how to build secure MCP tools and resources with proper validation, safe SQL execution, and MCP client integration.

---

# Student Information

- **Name:** Nguyen Tien Dat
- **Student ID:** 2A202600218
- **Repository:** Day26-Track3-MCP-tool-integration

---

# Features

## MCP Tools

This server exposes 3 MCP tools:

### 1. search
Query rows from database tables with:

- filters
- ordering
- pagination
- column selection

### 2. insert
Insert validated rows into database tables.

### 3. aggregate
Compute statistics such as:

- count
- avg
- sum
- min
- max

---

## MCP Resources

### Full database schema

```txt
schema://database
```

### Single table schema

```txt
schema://table/{table_name}
```

Examples:

```txt
schema://table/students
schema://table/courses
schema://table/enrollments
```

---

# Security and Validation

The server includes:

- table validation
- column validation
- operator validation
- aggregate validation
- parameterized SQL queries
- insert validation
- safe filtering
- clear error handling

Unsafe SQL execution is prevented by strict validation.

---

# Tech Stack

- Python
- FastMCP
- SQLite
- Pytest

---

# Project Structure

```txt
implementation/
├── db.py
├── init_db.py
├── mcp_server.py
├── verify_server.py
├── requirements.txt
├── start_inspector.bat
├── start_inspector.sh
├── CLIENT_SETUP.md
├── demo_examples.md
├── README.md
│
├── tests/
│   └── test_server.py
│
└── lab.db
```

---

# Installation

## Prerequisites

- Python 3.8+
- pip
- Node.js (for MCP Inspector)

---

# Setup

## 1. Clone repository

```bash
git clone https://github.com/VinUni-AI20k/Day26-Track3-MCP-tool-integration.git
```

---

## 2. Move into implementation folder

```bash
cd /c/LabVinUni/2A202600218_NguyenTienDatDay26-Track3/implementation
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Initialize Database

```bash
python init_db.py
```

This creates:

- students table
- courses table
- enrollments table

with seed data.

---

# Run MCP Server

```bash
python mcp_server.py
```

If successful, the MCP server will start and expose tools/resources.

---

# Verify Implementation

Run:

```bash
python verify_server.py
```

This verifies:

- search tool
- insert tool
- aggregate tool
- schema resources
- validation handling

---

# Run Tests

```bash
python -m unittest tests/test_server.py -v
```

or:

```bash
pytest
```

---

# Database Schema

## students

| Column | Type |
|---|---|
| id | INTEGER |
| name | TEXT |
| cohort | TEXT |
| email | TEXT |
| score | REAL |

---

## courses

| Column | Type |
|---|---|
| id | INTEGER |
| code | TEXT |
| name | TEXT |
| credits | INTEGER |

---

## enrollments

| Column | Type |
|---|---|
| id | INTEGER |
| student_id | INTEGER |
| course_id | INTEGER |
| grade | REAL |
| enrolled_date | TEXT |

---

# MCP Tool Usage Examples

# Tool: search

## Search all students

```json
{
  "table": "students"
}
```

---

## Search students in cohort A1

```json
{
  "table": "students",
  "filters": [
    {
      "column": "cohort",
      "operator": "eq",
      "value": "A1"
    }
  ]
}
```

---

## Search students with score >= 85

```json
{
  "table": "students",
  "filters": [
    {
      "column": "score",
      "operator": "gte",
      "value": 85
    }
  ]
}
```

---

# Tool: insert

## Insert a new student

```json
{
  "table": "students",
  "values": {
    "name": "New Student",
    "cohort": "A3",
    "email": "newstudent@example.com",
    "score": 88.5
  }
}
```

---

## Insert a new course

```json
{
  "table": "courses",
  "values": {
    "code": "CS999",
    "name": "Advanced Topics",
    "credits": 4
  }
}
```

---

# Tool: aggregate

## Count all students

```json
{
  "table": "students",
  "metric": "count"
}
```

---

## Average score by cohort

```json
{
  "table": "students",
  "metric": "avg",
  "column": "score",
  "group_by": "cohort"
}
```

---

## Maximum score

```json
{
  "table": "students",
  "metric": "max",
  "column": "score"
}
```

---

## Count students in cohort A1

```json
{
  "table": "students",
  "metric": "count",
  "filters": [
    {
      "column": "cohort",
      "operator": "eq",
      "value": "A1"
    }
  ]
}
```

---

# Supported Filter Operators

| Operator | Meaning |
|---|---|
| eq | equal |
| ne | not equal |
| gt | greater than |
| lt | less than |
| gte | greater than or equal |
| lte | less than or equal |
| like | SQL LIKE |
| in | value in list |

---

# Supported Aggregate Metrics

| Metric | Description |
|---|---|
| count | count rows |
| avg | average value |
| sum | total value |
| min | minimum value |
| max | maximum value |

---

# MCP Resources

## Full database schema

```txt
schema://database
```

---

## Specific table schema

```txt
schema://table/students
schema://table/courses
schema://table/enrollments
```

---

# MCP Inspector

## Install Inspector

```bash
npm install -g @modelcontextprotocol/inspector
```

---

## Start Inspector

### Windows

```bash
start_inspector.bat
```

### Linux / Mac

```bash
./start_inspector.sh
```

### Manual command

```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```

---

# Gemini CLI Configuration

## Add MCP server

```bash
gemini mcp add sqlite-lab \
python \
/c/LabVinUni/2A202600218_NguyenTienDatDay26-Track3/implementation/mcp_server.py \
--description "SQLite FastMCP Server" \
--timeout 10000
```

---

## Verify connection

```bash
gemini mcp list
```

Expected result:

```txt
sqlite-lab  Connected
```

---

## Example Gemini CLI test

```bash
gemini \
--allowed-mcp-server-names sqlite-lab \
--yolo \
-p "Show all students in cohort A1"
```

---

# Claude Code Configuration

Create `.mcp.json`:

```json
{
  "mcpServers": {
    "sqlite-lab": {
      "type": "stdio",
      "command": "python",
      "args": [
        "/c/LabVinUni/2A202600218_NguyenTienDatDay26-Track3/implementation/mcp_server.py"
      ]
    }
  }
}
```

---

# Codex Configuration

Edit:

```txt
~/.codex/config.toml
```

Add:

```toml
[mcp_servers.sqlite_lab]
command = "python"
args = ["/c/LabVinUni/2A202600218_NguyenTienDatDay26-Track3/implementation/mcp_server.py"]
```

---

# Error Handling Examples

## Invalid table

```json
{
  "error": "Table 'invalid_table' does not exist. Available tables: students, courses, enrollments"
}
```

---

## Invalid column

```json
{
  "error": "Column 'invalid_col' does not exist in table 'students'"
}
```

---

## Invalid operator

```json
{
  "error": "Unsupported operator 'invalid_op'"
}
```

---

## Invalid metric

```json
{
  "error": "Unsupported metric 'invalid'"
}
```

---

## Empty insert

```json
{
  "error": "Insert values cannot be empty"
}
```

---

# Demo Tasks

The following demo tasks are supported:

1. Search all students in cohort A1
2. Insert a new student
3. Count rows in students table
4. Compute average score by cohort
5. Read full schema resource
6. Read students schema resource
7. Show invalid request handling

---

# Troubleshooting

## Server does not start

Ensure:

- Python 3.8+ installed
- dependencies installed
- database initialized

Run:

```bash
python init_db.py
```

---

## Inspector issues

Ensure:

- Node.js installed
- npm installed

Try:

```bash
npm cache clean --force
```

---

## Database issues

Delete database and recreate:

```bash
rm lab.db
python init_db.py
```

---

# Development Notes

## Adding new tables

1. Update schema in `init_db.py`
2. Add seed data
3. Reinitialize database
4. Update validation logic

---

## Adding new MCP tools

1. Add `@mcp.tool()`
2. Implement validation
3. Add tests
4. Update README

---

## Adding new resources

1. Add `@mcp.resource()`
2. Return schema/data
3. Verify with Inspector

---

# Deliverables Checklist

- FastMCP server
- SQLite database
- search tool
- insert tool
- aggregate tool
- schema resources
- validation and error handling
- verification script
- tests
- Inspector support
- Gemini CLI integration
- README documentation

---

# References

- FastMCP Documentation  
  https://gofastmcp.com/

- MCP Specification  
  https://modelcontextprotocol.io/

- MCP Inspector  
  https://modelcontextprotocol.io/docs/tools/inspector

---

# Author

Nguyen Tien Dat  
Student ID: 2A202600218