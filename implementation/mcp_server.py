#!/usr/bin/env python3
"""
FastMCP server for the MCP SQLite database lab.
"""

import json
import os
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

from db import SQLiteAdapter, ValidationError
from init_db import create_database

ROOT_DIR = os.path.dirname(__file__)
DB_PATH = os.environ.get("LAB_DB_PATH", os.path.join(ROOT_DIR, "lab.db"))

if not os.path.exists(DB_PATH):
    print(f"Database not found at {DB_PATH}. Creating sample database...")
    create_database(DB_PATH)

mcp = FastMCP("2A202600218_NguyenTienDat SQLite MCP Server")
adapter = SQLiteAdapter(DB_PATH)


def _json_error(message: str) -> str:
    return json.dumps({"error": message}, indent=2)


@mcp.tool(name="search", description="Search rows in a table with filters, ordering, and pagination.")
def search(
    table: str,
    filters: Optional[List[Dict[str, Any]]] = None,
    columns: Optional[List[str]] = None,
    limit: int = 20,
    offset: int = 0,
    order_by: Optional[str] = None,
    descending: bool = False
) -> str:
    try:
        result = adapter.search(
            table=table,
            columns=columns,
            filters=filters,
            limit=limit,
            offset=offset,
            order_by=order_by,
            descending=descending,
        )
        return json.dumps(result, indent=2)
    except ValidationError as exc:
        return _json_error(str(exc))
    except Exception as exc:
        return _json_error(f"Unexpected error: {exc}")


@mcp.tool(name="insert", description="Insert a new row into a supported table.")
def insert(table: str, values: Dict[str, Any]) -> str:
    try:
        row = adapter.insert(table=table, values=values)
        return json.dumps({"success": True, "inserted": row}, indent=2)
    except ValidationError as exc:
        return _json_error(str(exc))
    except Exception as exc:
        return _json_error(f"Unexpected error: {exc}")


@mcp.tool(name="aggregate", description="Run an aggregate query against a table.")
def aggregate(
    table: str,
    metric: str,
    column: Optional[str] = None,
    filters: Optional[List[Dict[str, Any]]] = None,
    group_by: Optional[str] = None,
) -> str:
    try:
        result = adapter.aggregate(
            table=table,
            metric=metric,
            column=column,
            filters=filters,
            group_by=group_by,
        )
        return json.dumps({"metric": metric, "results": result}, indent=2)
    except ValidationError as exc:
        return _json_error(str(exc))
    except Exception as exc:
        return _json_error(f"Unexpected error: {exc}")


@mcp.resource("schema://database")
def database_schema() -> str:
    try:
        tables = adapter.list_tables()
        schema: Dict[str, Any] = {}
        for table in tables:
            schema[table] = adapter.get_table_schema(table)
        return json.dumps({"database": DB_PATH, "tables": schema}, indent=2)
    except Exception as exc:
        return _json_error(f"Failed to load schema: {exc}")


@mcp.resource("schema://table/{table_name}")
def table_schema(table_name: str) -> str:
    try:
        schema = adapter.get_table_schema(table_name)
        return json.dumps({"table": table_name, "columns": schema}, indent=2)
    except ValidationError as exc:
        return _json_error(str(exc))
    except Exception as exc:
        return _json_error(f"Failed to load table schema: {exc}")


if __name__ == "__main__":
    print(f"Starting MCP SQLite server using database: {DB_PATH}")
    mcp.run()
