
import sqlite3

# 1. Create university.db database
conn = sqlite3.connect("university.db")
cursor = conn.cursor()

# 2. Create students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    department TEXT,
    semester INTEGER
)
""")

# 3. Insert at least five students using parameterized queries
students = [
    ("Ahmad", 20, "Computer Science", 2),
    ("Bahram", 21, "Information Systems", 4),
    ("Ali", 22, "Software Engineering", 3),
    ("Omar", 20, "Information Systems", 2),
    ("Yusuf", 23, "Computer Science", 5)
]

cursor.executemany("""
INSERT INTO students (name, age, department, semester)
VALUES (?, ?, ?, ?)
""", students)

conn.commit()

# 4. Display all records
print("\n--- All Students ---")

cursor.execute("SELECT * FROM students")
records = cursor.fetchall()

for student in records:
    print(student)

# 5. Search students by semester
search_semester = 2

print(f"\n--- Students in Semester {search_semester} ---")

cursor.execute(
    "SELECT * FROM students WHERE semester = ?",
    (search_semester,)
)

records = cursor.fetchall()

for student in records:
    print(student)

# 6. Update one student's department
cursor.execute("""
UPDATE students
SET department = ?
WHERE id = ?
""", ("Database Systems", 1))

conn.commit()

print("\nDepartment updated successfully!")

# 7. Delete one record by ID
cursor.execute(
    "DELETE FROM students WHERE id = ?",
    (5,)
)

conn.commit()

print("\nStudent deleted successfully!")

# 8. Print the final table contents
print("\n--- Final Students Table ---")

cursor.execute("SELECT * FROM students")
final_records = cursor.fetchall()

for student in final_records:
    print(student)

# Close database connection
conn.close()
