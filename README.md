# MCP SQLite Data Server

![MCP Inspector](MCP%20Inspector.png)

---

# Student Information

- **Name:** Nguyen Tien Dat
- **Student ID:** 2A202600218
- **Lab:** FastMCP + SQLite Database Server

---

# Project Overview

This repository implements a production-style Model Context Protocol (MCP) server using FastMCP and SQLite.

The project demonstrates:

- MCP tool development
- MCP resource exposure
- secure SQL execution
- schema validation
- SQLite integration
- MCP client interoperability
- testing and verification workflows

The server exposes a small educational database through secure MCP tools and schema resources.

---

# Included Deliverables

## Main Deliverables

- `implementation/`
  - FastMCP server
  - SQLite adapter
  - validation layer
  - database initialization
  - verification scripts
  - unit tests
  - helper scripts

- `pseudocode/`
  - design notes
  - architecture planning
  - implementation pseudocode

- Documentation
  - `README.md`
  - `QUICKSTART.md`
  - `SUBMISSION.md`
  - `Tips.md`

---

# Features

## MCP Tools

### search

Query rows with:

- filters
- ordering
- pagination
- selected columns

---

### insert

Safely create new records with:

- schema validation
- type checking
- parameterized SQL

---

### aggregate

Compute statistics including:

- `count`
- `avg`
- `sum`
- `min`
- `max`

Supports optional grouping.

---

# MCP Resources

## Full database schema

```txt
schema://database
```

---

## Single table schema

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

# Security Features

The server includes:

- strict table validation
- strict column validation
- supported operator validation
- supported aggregate validation
- parameterized SQL queries
- insert validation
- safe filtering
- structured error handling

Unsafe SQL execution is prevented.

---

# Technology Stack

- Python
- FastMCP
- SQLite
- Pytest

---

# Repository Structure

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

pseudocode/
├── architecture.md
├── search_tool.md
├── insert_tool.md
└── aggregate_tool.md

README.md
QUICKSTART.md
SUBMISSION.md
Tips.md
MCP Inspector.png
```

---

# Installation

## Prerequisites

Install:

- Python 3.8+
- pip
- Node.js + npm

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/VinUni-AI20k/Day26-Track3-MCP-tool-integration.git
```

---

## 2. Navigate to Project

```bash
cd /c/LabVinUni/2A202600218_NguyenTienDatDay26-Track3/implementation
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Initialize Database

Run:

```bash
python init_db.py
```

This creates:

- students table
- courses table
- enrollments table

with sample seed data.

---

# Run Verification

```bash
python verify_server.py
```

This validates:

- search tool
- insert tool
- aggregate tool
- schema resources
- validation logic
- error handling

---

# Start MCP Server

```bash
python mcp_server.py
```

If successful, the server will expose MCP tools and resources.

---

# Run Unit Tests

Using unittest:

```bash
python -m unittest tests/test_server.py -v
```

Or using pytest:

```bash
pytest
```

---

# Database Model

# students

| Column | Type |
|---|---|
| id | INTEGER |
| name | TEXT |
| cohort | TEXT |
| email | TEXT |
| score | REAL |

---

# courses

| Column | Type |
|---|---|
| id | INTEGER |
| code | TEXT |
| name | TEXT |
| credits | INTEGER |

---

# enrollments

| Column | Type |
|---|---|
| id | INTEGER |
| student_id | INTEGER |
| course_id | INTEGER |
| grade | REAL |
| enrolled_date | TEXT |

---

# MCP Tool Examples

# Tool: search

## Search all students

```json
{
  "table": "students"
}
```

---

## Search cohort A1

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
    "name": "Demo Student",
    "cohort": "A3",
    "email": "demo.student@example.com",
    "score": 92.5
  }
}
```

---

## Insert a course

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

| Operator | Description |
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
| avg | average |
| sum | total |
| min | minimum |
| max | maximum |

---

# MCP Resources

## Full schema resource

```txt
schema://database
```

---

## Table schema resources

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

# Start Inspector

## Windows

```bash
start_inspector.bat
```

---

## Linux / Mac

```bash
./start_inspector.sh
```

---

## Manual command

```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```

---

# Gemini CLI Configuration

## Add MCP Server

```bash
gemini mcp add sqlite-lab \
python \
/c/LabVinUni/2A202600218_NguyenTienDatDay26-Track3/implementation/mcp_server.py \
--description "SQLite FastMCP Server" \
--timeout 10000
```

---

## Verify Connection

```bash
gemini mcp list
```

Expected:

```txt
sqlite-lab   Connected
```

---

## Gemini CLI Example

```bash
gemini \
--allowed-mcp-server-names sqlite-lab \
--yolo \
-p "Show all students in cohort A1"
```

---

# Claude Code Configuration

Create `.mcp.json`

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

# Invalid table

```json
{
  "error": "Table 'invalid_table' does not exist"
}
```

---

# Invalid column

```json
{
  "error": "Column 'invalid_col' does not exist in table 'students'"
}
```

---

# Invalid operator

```json
{
  "error": "Unsupported operator 'invalid_op'"
}
```

---

# Invalid metric

```json
{
  "error": "Unsupported metric 'invalid'"
}
```

---

# Empty insert

```json
{
  "error": "Insert values cannot be empty"
}
```

---

# Demo Tasks

This project supports all required rubric demonstrations:

1. Search students in cohort A1
2. Insert a new student
3. Count rows in students table
4. Compute average score by cohort
5. Read full schema resource
6. Read students schema resource
7. Demonstrate invalid request handling

---

# Troubleshooting

# Server does not start

Ensure:

- Python 3.8+ installed
- dependencies installed
- database initialized

Run:

```bash
python init_db.py
```

---

# Inspector Issues

Ensure:

- Node.js installed
- npm installed

Try:

```bash
npm cache clean --force
```

---

# Database Problems

Delete and recreate database:

```bash
rm lab.db
python init_db.py
```

---

# Development Notes

# Add New Tables

1. Update schema in `init_db.py`
2. Add seed data
3. Reinitialize database
4. Update validation logic

---

# Add New MCP Tools

1. Add `@mcp.tool()`
2. Implement validation
3. Add tests
4. Update README

---

# Add New Resources

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
- unit tests
- MCP Inspector support
- Gemini CLI integration
- complete documentation

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
```
