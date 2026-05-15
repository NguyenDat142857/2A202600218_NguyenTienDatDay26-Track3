# Demo Examples for SQLite MCP Server

A ready-to-run demo guide showing how to use the MCP tools and resources from this project.

## Setup
1. Initialize the database:
```bash
cd implementation
python init_db.py
```
2. Start the MCP server in one terminal:
```bash
python mcp_server.py
```
3. In another terminal, use Inspector or any MCP client to call tools.

## Search Demo

### 1. Search all students
- Tool: `search`
- Request:
```json
{
  "table": "students"
}
```
- Expected result: all rows in `students`, pagination metadata, and `total_count`.

### 2. Filter by cohort
- Tool: `search`
- Request:
```json
{
  "table": "students",
  "filters": [
    {"column": "cohort", "operator": "eq", "value": "A1"}
  ]
}
```
- Expected result: only students in cohort `A1`.

### 3. Order results by score
- Tool: `search`
- Request:
```json
{
  "table": "students",
  "order_by": "score",
  "descending": true,
  "limit": 3
}
```
- Expected result: top 3 students by score.

### 4. Pagination example
- Tool: `search`
- Page 1:
```json
{
  "table": "students",
  "limit": 2,
  "offset": 0
}
```
- Page 2:
```json
{
  "table": "students",
  "limit": 2,
  "offset": 2
}
```
- Expected result: different sets of rows across pages.

### 5. Select specific columns
- Tool: `search`
- Request:
```json
{
  "table": "students",
  "columns": ["name", "cohort", "score"]
}
```
- Expected result: only the requested columns appear in the response.

## Insert Demo

### 1. Insert a student
- Tool: `insert`
- Request:
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
- Expected result: inserted record with generated `id`.

### 2. Insert a course
- Tool: `insert`
- Request:
```json
{
  "table": "courses",
  "values": {
    "code": "CS999",
    "name": "Machine Learning",
    "credits": 4
  }
}
```
- Expected result: new course row is created.

### 3. Insert an enrollment
- Tool: `insert`
- Request:
```json
{
  "table": "enrollments",
  "values": {
    "student_id": 1,
    "course_id": 5,
    "grade": 88.5,
    "enrolled_date": "2024-02-01"
  }
}
```
- Expected result: new enrollment row with an `id`.

## Aggregate Demo

### 1. Count students
- Tool: `aggregate`
- Request:
```json
{
  "table": "students",
  "metric": "count"
}
```
- Expected result: `value` equals the number of students.

### 2. Average score
- Tool: `aggregate`
- Request:
```json
{
  "table": "students",
  "metric": "avg",
  "column": "score"
}
```
- Expected result: average student score.

### 3. Average score by cohort
- Tool: `aggregate`
- Request:
```json
{
  "table": "students",
  "metric": "avg",
  "column": "score",
  "group_by": "cohort"
}
```
- Expected result: average score grouped by each cohort.

### 4. Maximum score
- Tool: `aggregate`
- Request:
```json
{
  "table": "students",
  "metric": "max",
  "column": "score"
}
```
- Expected result: highest score value in the table.

## Schema Resource Demo

### 1. Full database schema
- Resource: `schema://database`
- Expected result: JSON snapshot of all tables and columns.

### 2. Table schema
- Resource: `schema://table/students`
- Expected result: JSON metadata for the `students` table.

## Error demo

### 1. Invalid table
- Request:
```json
{
  "table": "unknown_table"
}
```
- Expected result: validation error describing valid table names.

### 2. Invalid operator
- Request:
```json
{
  "table": "students",
  "filters": [{"column": "score", "operator": "wrong", "value": 80}]
}
```
- Expected result: error listing supported operators.

**Expected Result:**
- Returns maximum score: 95.5 (Hoang Van E)

### Example 3.5: Minimum Score
**Tool:** `aggregate`

**Parameters:**
```json
{
  "table": "students",
  "metric": "min",
  "column": "score"
}
```

**Expected Result:**
- Returns minimum score: 78.5 (Le Van C)

### Example 3.6: Sum of Credits
**Tool:** `aggregate`

**Parameters:**
```json
{
  "table": "courses",
  "metric": "sum",
  "column": "credits"
}
```

**Expected Result:**
- Returns total credits: 18 (3+4+4+3+4)

### Example 3.7: Count Students per Cohort
**Tool:** `aggregate`

**Parameters:**
```json
{
  "table": "students",
  "metric": "count",
  "group_by": "cohort"
}
```

**Expected Result:**
- A1: 2 students
- A2: 2 students
- B1: 2 students

### Example 3.8: Count with Filter
**Tool:** `aggregate`

**Parameters:**
```json
{
  "table": "students",
  "metric": "count",
  "filters": [
    {
      "column": "score",
      "operator": "gte",
      "value": 85
    }
  ]
}
```

**Expected Result:**
- Returns count of students with score >= 85
- Should be 4 students

## Demo 4: Resources

### Example 4.1: Get Full Database Schema
**Resource:** `schema://database`

**Expected Result:**
- JSON with all tables and their columns
- Shows structure of students, courses, and enrollments tables
- Includes column types, constraints, and primary keys

### Example 4.2: Get Students Table Schema
**Resource:** `schema://table/students`

**Expected Result:**
- JSON with students table structure
- Shows 5 columns: id, name, cohort, email, score
- Includes data types and constraints

### Example 4.3: Get Courses Table Schema
**Resource:** `schema://table/courses`

**Expected Result:**
- JSON with courses table structure
- Shows 4 columns: id, code, name, credits

### Example 4.4: Get Enrollments Table Schema
**Resource:** `schema://table/enrollments`

**Expected Result:**
- JSON with enrollments table structure
- Shows foreign key relationships

## Demo 5: Error Handling

### Example 5.1: Invalid Table Name
**Tool:** `search`

**Parameters:**
```json
{
  "table": "invalid_table"
}
```

**Expected Result:**
- Error message: "Table 'invalid_table' does not exist"
- Lists available tables: students, courses, enrollments

### Example 5.2: Invalid Column Name
**Tool:** `search`

**Parameters:**
```json
{
  "table": "students",
  "columns": ["invalid_column"]
}
```

**Expected Result:**
- Error message: "Column 'invalid_column' does not exist in table 'students'"
- Lists available columns

### Example 5.3: Invalid Operator
**Tool:** `search`

**Parameters:**
```json
{
  "table": "students",
  "filters": [
    {
      "column": "name",
      "operator": "invalid_op",
      "value": "test"
    }
  ]
}
```

**Expected Result:**
- Error message: "Unsupported operator 'invalid_op'"
- Lists supported operators: eq, ne, gt, lt, gte, lte, like, in

### Example 5.4: Invalid Metric
**Tool:** `aggregate`

**Parameters:**
```json
{
  "table": "students",
  "metric": "invalid_metric"
}
```

**Expected Result:**
- Error message: "Unsupported metric 'invalid_metric'"
- Lists supported metrics: count, avg, sum, min, max

### Example 5.5: Empty Insert
**Tool:** `insert`

**Parameters:**
```json
{
  "table": "students",
  "values": {}
}
```

**Expected Result:**
- Error message: "Insert values cannot be empty"

### Example 5.6: Missing Required Column
**Tool:** `insert`

**Parameters:**
```json
{
  "table": "students",
  "values": {
    "name": "Test"
  }
}
```

**Expected Result:**
- Database constraint error (missing required fields)

### Example 5.7: Invalid Table in Resource
**Resource:** `schema://table/invalid_table`

**Expected Result:**
- Error message: "Table 'invalid_table' does not exist"

## Demo 6: Complex Queries

### Example 6.1: Multiple Filters
**Tool:** `search`

**Parameters:**
```json
{
  "table": "students",
  "filters": [
    {
      "column": "cohort",
      "operator": "eq",
      "value": "A1"
    },
    {
      "column": "score",
      "operator": "gte",
      "value": 90
    }
  ]
}
```

**Expected Result:**
- Returns students in cohort A1 with score >= 90
- Should return Tran Thi B (92.0)

### Example 6.2: LIKE Operator
**Tool:** `search`

**Parameters:**
```json
{
  "table": "students",
  "filters": [
    {
      "column": "name",
      "operator": "like",
      "value": "%Van%"
    }
  ]
}
```

**Expected Result:**
- Returns students with "Van" in their name
- Nguyen Van A, Le Van C, Hoang Van E

### Example 6.3: IN Operator
**Tool:** `search`

**Parameters:**
```json
{
  "table": "students",
  "filters": [
    {
      "column": "cohort",
      "operator": "in",
      "value": ["A1", "B1"]
    }
  ]
}
```

**Expected Result:**
- Returns students in cohorts A1 or B1
- Should return 4 students

## Testing Workflow

1. **Start with Resources**
   - Get database schema to understand structure
   - Get individual table schemas

2. **Test Search**
   - Basic search (all records)
   - Filtered search
   - Ordered search
   - Paginated search

3. **Test Insert**
   - Insert valid records
   - Try invalid inserts to see error handling

4. **Test Aggregate**
   - Simple aggregates (count, avg, sum, min, max)
   - Grouped aggregates
   - Filtered aggregates

5. **Test Error Handling**
   - Invalid table names
   - Invalid column names
   - Invalid operators
   - Invalid metrics
   - Empty inserts

## Tips for Demo

1. Start with simple examples and build up complexity
2. Show both successful operations and error handling
3. Demonstrate the safety features (validation, parameterized queries)
4. Use the Inspector UI to show tool schemas and resource URIs
5. Show how pagination works with different offset values
6. Demonstrate the GROUP BY functionality with aggregates
7. Show how filters can be combined for complex queries

## Expected Outcomes

After running all demos, you should have demonstrated:

- ✅ All three tools work correctly
- ✅ Both resources are accessible
- ✅ Input validation prevents invalid requests
- ✅ Error messages are clear and helpful
- ✅ Complex queries with multiple filters work
- ✅ Pagination works correctly
- ✅ Aggregates with grouping work
- ✅ The server handles edge cases gracefully
