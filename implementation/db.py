import sqlite3
from typing import Any, Dict, List, Optional


class ValidationError(Exception):
    """Raised when a request is invalid or unsafe."""


class SQLiteAdapter:
    SUPPORTED_OPERATORS = {"eq", "ne", "gt", "lt", "gte", "lte", "like", "in"}
    SUPPORTED_METRICS = {"count", "avg", "sum", "min", "max"}

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def list_tables(self) -> List[str]:
        conn = self.connect()
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        return [row[0] for row in cursor.fetchall()]

    def get_table_schema(self, table: str) -> List[Dict[str, Any]]:
        self._validate_table_exists(table)
        conn = self.connect()
        cursor = conn.execute(f"PRAGMA table_info({table})")
        return [
            {
                "cid": row[0],
                "name": row[1],
                "type": row[2],
                "notnull": bool(row[3]),
                "default_value": row[4],
                "pk": bool(row[5]),
            }
            for row in cursor.fetchall()
        ]

    def _validate_table_exists(self, table: str) -> None:
        if not isinstance(table, str) or not table:
            raise ValidationError("Table name must be a non-empty string")
        if table not in self.list_tables():
            raise ValidationError(
                f"Table '{table}' does not exist. Available tables: {', '.join(self.list_tables())}"
            )

    def _validate_identifier(self, identifier: str) -> None:
        if not isinstance(identifier, str) or not identifier:
            raise ValidationError("Identifier must be a non-empty string")
        if not identifier.replace("_", "").isalnum():
            raise ValidationError(f"Invalid identifier: '{identifier}'")

    def _validate_columns_exist(self, table: str, columns: List[str]) -> None:
        if not columns:
            raise ValidationError("Column list cannot be empty")
        schema = self.get_table_schema(table)
        valid_columns = {col["name"] for col in schema}
        for col in columns:
            if col not in valid_columns:
                raise ValidationError(
                    f"Column '{col}' does not exist in table '{table}'. Available columns: {', '.join(sorted(valid_columns))}"
                )

    def _validate_limit_offset(self, limit: int, offset: int) -> None:
        if not isinstance(limit, int) or limit < 0:
            raise ValidationError("Limit must be a non-negative integer")
        if not isinstance(offset, int) or offset < 0:
            raise ValidationError("Offset must be a non-negative integer")

    def _build_where_clause(
        self, filters: Optional[List[Dict[str, Any]]]
    ) -> tuple[str, List[Any]]:
        if not filters:
            return "", []
        if not isinstance(filters, list):
            raise ValidationError("Filters must be a list of filter objects")

        parts: List[str] = []
        params: List[Any] = []

        for item in filters:
            if not isinstance(item, dict):
                raise ValidationError("Each filter must be an object")
            column = item.get("column")
            operator = item.get("operator", "eq")
            value = item.get("value")

            if not column:
                raise ValidationError("Filter must include a 'column'")
            if operator not in self.SUPPORTED_OPERATORS:
                raise ValidationError(
                    f"Unsupported operator '{operator}'. Supported operators: {', '.join(sorted(self.SUPPORTED_OPERATORS))}"
                )
            self._validate_identifier(column)

            if operator == "eq":
                parts.append(f"{column} = ?")
                params.append(value)
            elif operator == "ne":
                parts.append(f"{column} != ?")
                params.append(value)
            elif operator == "gt":
                parts.append(f"{column} > ?")
                params.append(value)
            elif operator == "lt":
                parts.append(f"{column} < ?")
                params.append(value)
            elif operator == "gte":
                parts.append(f"{column} >= ?")
                params.append(value)
            elif operator == "lte":
                parts.append(f"{column} <= ?")
                params.append(value)
            elif operator == "like":
                parts.append(f"{column} LIKE ?")
                params.append(value)
            elif operator == "in":
                if not isinstance(value, list) or len(value) == 0:
                    raise ValidationError("'in' operator requires a non-empty list value")
                parts.append(f"{column} IN ({','.join(['?'] * len(value))})")
                params.extend(value)

        return " AND ".join(parts), params

    def search(
        self,
        table: str,
        columns: Optional[List[str]] = None,
        filters: Optional[List[Dict[str, Any]]] = None,
        limit: int = 20,
        offset: int = 0,
        order_by: Optional[str] = None,
        descending: bool = False,
    ) -> Dict[str, Any]:
        self._validate_table_exists(table)
        self._validate_limit_offset(limit, offset)

        if columns:
            self._validate_columns_exist(table, columns)
            column_clause = ", ".join(columns)
        else:
            column_clause = "*"

        where_clause, params = self._build_where_clause(filters)
        query = f"SELECT {column_clause} FROM {table}"
        if where_clause:
            query += f" WHERE {where_clause}"

        if order_by:
            self._validate_identifier(order_by)
            self._validate_columns_exist(table, [order_by])
            direction = "DESC" if descending else "ASC"
            query += f" ORDER BY {order_by} {direction}"

        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        conn = self.connect()
        cursor = conn.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]

        count_query = f"SELECT COUNT(*) FROM {table}"
        if where_clause:
            count_query += f" WHERE {where_clause}"
        count_cursor = conn.execute(count_query, params[:-2])
        total_count = count_cursor.fetchone()[0]

        return {
            "rows": rows,
            "total_count": total_count,
            "count": len(rows),
            "limit": limit,
            "offset": offset,
        }

    def insert(self, table: str, values: Dict[str, Any]) -> Dict[str, Any]:
        self._validate_table_exists(table)
        if not isinstance(values, dict) or not values:
            raise ValidationError("Insert values must be a non-empty object")

        columns = list(values.keys())
        self._validate_columns_exist(table, columns)

        column_clause = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))
        query = f"INSERT INTO {table} ({column_clause}) VALUES ({placeholders})"

        conn = self.connect()
        cursor = conn.execute(query, list(values.values()))
        conn.commit()

        row = dict(values)
        if cursor.lastrowid:
            row["id"] = cursor.lastrowid
        return row

    def aggregate(
        self,
        table: str,
        metric: str,
        column: Optional[str] = None,
        filters: Optional[List[Dict[str, Any]]] = None,
        group_by: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        self._validate_table_exists(table)

        metric_lower = metric.lower()
        if metric_lower not in self.SUPPORTED_METRICS:
            raise ValidationError(
                f"Unsupported metric '{metric}'. Supported metrics: {', '.join(sorted(self.SUPPORTED_METRICS))}"
            )

        if metric_lower == "count":
            if column:
                self._validate_identifier(column)
                self._validate_columns_exist(table, [column])
                aggregate_expr = f"COUNT({column})"
            else:
                aggregate_expr = "COUNT(*)"
        else:
            if not column:
                raise ValidationError(f"Metric '{metric}' requires a column")
            self._validate_identifier(column)
            self._validate_columns_exist(table, [column])
            aggregate_expr = f"{metric_lower.upper()}({column})"

        where_clause, params = self._build_where_clause(filters)
        if group_by:
            self._validate_identifier(group_by)
            self._validate_columns_exist(table, [group_by])
            query = f"SELECT {group_by}, {aggregate_expr} AS value FROM {table}"
            if where_clause:
                query += f" WHERE {where_clause}"
            query += f" GROUP BY {group_by}"
        else:
            query = f"SELECT {aggregate_expr} AS value FROM {table}"
            if where_clause:
                query += f" WHERE {where_clause}"

        conn = self.connect()
        cursor = conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
