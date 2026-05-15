#!/usr/bin/env python3
"""
Verification script for the MCP SQLite server.
"""

import os
from db import SQLiteAdapter, ValidationError
from init_db import create_database


def print_section(title: str) -> None:
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_result(name: str, success: bool, details: str = "") -> None:
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"{status}: {name}")
    if details:
        print(f"  {details}")


def main() -> None:
    print_section("SQLite MCP Server Verification")
    db_path = os.path.join(os.path.dirname(__file__), "test_lab.db")
    if os.path.exists(db_path):
        os.remove(db_path)

    create_database(db_path)
    adapter = SQLiteAdapter(db_path)

    print_section("Table and schema checks")
    try:
        tables = adapter.list_tables()
        print_result("List tables", True, f"Found: {', '.join(tables)}")
        assert set(["students", "courses", "enrollments"]).issubset(set(tables))
    except Exception as exc:
        print_result("List tables", False, str(exc))

    try:
        schema = adapter.get_table_schema("students")
        names = [column["name"] for column in schema]
        print_result("Students schema", True, f"Columns: {', '.join(names)}")
    except Exception as exc:
        print_result("Students schema", False, str(exc))

    print_section("Search tests")
    try:
        result = adapter.search("students")
        print_result("Search all students", True, f"Rows: {result['count']}")
    except Exception as exc:
        print_result("Search all students", False, str(exc))

    try:
        result = adapter.search(
            "students",
            filters=[{"column": "cohort", "operator": "eq", "value": "A1"}],
        )
        print_result("Search cohort A1", True, f"Matches: {result['count']}")
    except Exception as exc:
        print_result("Search cohort A1", False, str(exc))

    print_section("Insert tests")
    try:
        row = adapter.insert(
            "students",
            {
                "name": "Verification Student",
                "cohort": "A3",
                "email": "verification@example.com",
                "score": 93.0,
            },
        )
        print_result("Insert student", True, f"ID: {row.get('id')}")
    except Exception as exc:
        print_result("Insert student", False, str(exc))

    print_section("Aggregate tests")
    try:
        count = adapter.aggregate("students", "count")
        print_result("Count students", True, f"Count: {count[0]['value']}")
    except Exception as exc:
        print_result("Count students", False, str(exc))

    try:
        avg_score = adapter.aggregate("students", "avg", column="score")
        print_result("Average score", True, f"Average: {avg_score[0]['value']:.2f}")
    except Exception as exc:
        print_result("Average score", False, str(exc))

    try:
        grouped = adapter.aggregate("students", "avg", column="score", group_by="cohort")
        print_result("Average score by cohort", True, f"Cohorts: {len(grouped)}")
    except Exception as exc:
        print_result("Average score by cohort", False, str(exc))

    print_section("Validation tests")
    try:
        adapter.search("invalid_table")
        print_result("Invalid table detection", False, "Expected ValidationError")
    except ValidationError as exc:
        print_result("Invalid table detection", True, str(exc))

    try:
        adapter.search("students", columns=["invalid_column"])
        print_result("Invalid column detection", False, "Expected ValidationError")
    except ValidationError as exc:
        print_result("Invalid column detection", True, str(exc))

    try:
        adapter.search(
            "students",
            filters=[{"column": "name", "operator": "wrong", "value": "test"}],
        )
        print_result("Invalid operator detection", False, "Expected ValidationError")
    except ValidationError as exc:
        print_result("Invalid operator detection", True, str(exc))

    try:
        adapter.aggregate("students", "invalid_metric")
        print_result("Invalid metric detection", False, "Expected ValidationError")
    except ValidationError as exc:
        print_result("Invalid metric detection", True, str(exc))

    try:
        adapter.insert("students", {})
        print_result("Invalid insert detection", False, "Expected ValidationError")
    except ValidationError as exc:
        print_result("Invalid insert detection", True, str(exc))

    adapter.close()
    print_section("Verification complete")
    print(f"Database used for verification: {db_path}")


if __name__ == "__main__":
    main()
