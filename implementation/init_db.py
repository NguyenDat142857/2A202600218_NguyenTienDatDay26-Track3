import sqlite3
import os

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cohort TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    score REAL DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    credits INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    grade REAL,
    enrolled_date TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    UNIQUE(student_id, course_id)
);
"""

SEED_SQL = """
-- Insert students
INSERT INTO students (name, cohort, email, score) VALUES
    ('Nguyen Van A', 'A1', 'nguyenvana@example.com', 85.5),
    ('Tran Thi B', 'A1', 'tranthib@example.com', 92.0),
    ('Le Van C', 'A2', 'levanc@example.com', 78.5),
    ('Pham Thi D', 'A2', 'phamthid@example.com', 88.0),
    ('Hoang Van E', 'B1', 'hoangvane@example.com', 95.5),
    ('Vo Thi F', 'B1', 'vothif@example.com', 82.0);

-- Insert courses
INSERT INTO courses (code, name, credits) VALUES
    ('CS101', 'Introduction to Computer Science', 3),
    ('CS102', 'Data Structures', 4),
    ('CS201', 'Algorithms', 4),
    ('CS202', 'Database Systems', 3),
    ('CS301', 'Software Engineering', 4);

-- Insert enrollments
INSERT INTO enrollments (student_id, course_id, grade, enrolled_date) VALUES
    (1, 1, 85.0, '2024-01-15'),
    (1, 2, 88.0, '2024-01-15'),
    (2, 1, 92.0, '2024-01-15'),
    (2, 3, 90.0, '2024-01-15'),
    (3, 1, 78.0, '2024-01-16'),
    (3, 2, 80.0, '2024-01-16'),
    (4, 2, 87.0, '2024-01-16'),
    (4, 4, 89.0, '2024-01-16'),
    (5, 3, 95.0, '2024-01-17'),
    (5, 4, 96.0, '2024-01-17'),
    (6, 1, 82.0, '2024-01-17'),
    (6, 5, 84.0, '2024-01-17');
"""


def create_database(db_path: str = "lab.db") -> str:
    """
    Create and initialize the SQLite database.
    
    Args:
        db_path: Path to the database file
        
    Returns:
        Absolute path to the created database
    """
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")

    # Create new database
    conn = sqlite3.connect(db_path)
    
    try:
        # Execute schema SQL
        conn.executescript(SCHEMA_SQL)
        print("Database schema created successfully")
        
        # Execute seed SQL
        conn.executescript(SEED_SQL)
        print("Database seeded successfully")
        
        # Commit changes
        conn.commit()
        
        # Verify data
        cursor = conn.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        cursor = conn.execute("SELECT COUNT(*) FROM courses")
        course_count = cursor.fetchone()[0]
        cursor = conn.execute("SELECT COUNT(*) FROM enrollments")
        enrollment_count = cursor.fetchone()[0]
        
        print(f"\nDatabase initialized with:")
        print(f"  - {student_count} students")
        print(f"  - {course_count} courses")
        print(f"  - {enrollment_count} enrollments")
        
    finally:
        conn.close()
    
    # Return absolute path
    abs_path = os.path.abspath(db_path)
    print(f"\nDatabase created at: {abs_path}")
    return abs_path


if __name__ == "__main__":
    create_database()
