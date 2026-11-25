
import tkinter as tk
from tkinter import ttk
import sqlite3


# ==================================
# 1. DATABASE CONNECTION
# ==================================

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department TEXT NOT NULL,
    semester INTEGER NOT NULL
)
""")

conn.commit()


# ==================================
# 2. DATABASE LOGIC
# ==================================

def search_students(search_term=""):

    if search_term == "":
        cursor.execute("""
            SELECT * FROM students
            ORDER BY id
        """)
    else:
        cursor.execute("""
            SELECT * FROM students
            WHERE name LIKE ?
            ORDER BY id
        """, ('%' + search_term + '%',))

    return cursor.fetchall()


# ==================================
# 3. REFRESH STUDENT LIST
# ==================================

def display_students(search_term=""):

    # Clear old records
    for item in student_tree.get_children():
        student_tree.delete(item)

    # Get matching records from database
    records = search_students(search_term)

    # Display new records
    for student in records:
        student_tree.insert(
            "",
            tk.END,
            values=student
        )


# ==================================
# 4. SEARCH HANDLER
# ==================================

def search_handler(event):

    # Read current search text
    search_term = search_entry.get().strip()

    # Refresh student list
    display_students(search_term)


# ==================================
# 5. MAIN WINDOW
# ==================================

root = tk.Tk()
root.title("Student Management System")
root.geometry("800x500")


# ==================================
# 6. SEARCH ENTRY
# ==================================

search_frame = tk.Frame(root)
search_frame.pack(pady=15)

tk.Label(
    search_frame,
    text="Search Student:",
    font=("Arial", 12)
).pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(
    search_frame,
    width=35,
    font=("Arial", 12)
)

search_entry.pack(side=tk.LEFT, padx=5)


# Bind KeyRelease event
search_entry.bind(
    "<KeyRelease>",
    search_handler
)


# ==================================
# 7. STUDENT TABLE
# ==================================

columns = (
    "ID",
    "Name",
    "Email",
    "Department",
    "Semester"
)

student_tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

for column in columns:
    student_tree.heading(column, text=column)
    student_tree.column(column, width=140)

student_tree.pack(
    fill=tk.BOTH,
    expand=True,
    padx=15,
    pady=10
)


# ==================================
# 8. LOAD ALL STUDENTS
# ==================================

display_students()


# ==================================
# 9. RUN APPLICATION
# ==================================

root.mainloop()

conn.close()
