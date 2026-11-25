
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
import re


# ==========================================
# 1. DATABASE INITIALIZATION
# ==========================================

conn = sqlite3.connect("students.db")
conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department TEXT NOT NULL,
    semester INTEGER NOT NULL CHECK(semester > 0)
)
""")

conn.commit()


# ==========================================
# 2. MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title("Student Management System")
root.geometry("1000x700")
root.minsize(850, 600)

selected_id = None


# ==========================================
# 3. VALIDATION FUNCTION
# ==========================================

def validate_input():

    name = name_entry.get().strip()
    email = email_entry.get().strip()
    department = department_entry.get().strip()
    semester = semester_entry.get().strip()

    if not name or not email or not department or not semester:
        messagebox.showerror(
            "Validation Error",
            "All fields are required!"
        )
        return None

    # Check email format
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        messagebox.showerror(
            "Validation Error",
            "Please enter a valid email address!"
        )
        return None

    # Check semester
    try:
        semester = int(semester)

        if semester < 1:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Validation Error",
            "Semester must be a positive integer!"
        )
        return None

    return name, email, department, semester


# ==========================================
# 4. CLEAR FORM
# ==========================================

def clear_form():

    global selected_id

    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)
    semester_entry.delete(0, tk.END)

    selected_id = None

    for item in student_tree.selection():
        student_tree.selection_remove(item)


# ==========================================
# 5. DISPLAY / REFRESH STUDENTS
# ==========================================

def refresh_students(search=""):

    # Remove old records
    for item in student_tree.get_children():
        student_tree.delete(item)

    try:
        cursor.execute("""
            SELECT id, name, email, department, semester
            FROM students
            WHERE name LIKE ?
            ORDER BY id DESC
        """, ('%' + search + '%',))

        records = cursor.fetchall()

        for student in records:
            student_tree.insert(
                "",
                tk.END,
                values=student
            )

        status_label.config(
            text=f"Total displayed students: {len(records)}"
        )

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


# ==========================================
# 6. CREATE / ADD STUDENT
# ==========================================

def add_student():

    data = validate_input()

    if data is None:
        return

    try:
        # Transaction: commit on success,
        # rollback automatically on failure
        with conn:

            conn.execute("""
                INSERT INTO students
                (name, email, department, semester)
                VALUES (?, ?, ?, ?)
            """, data)

        messagebox.showinfo(
            "Success",
            "Student added successfully!"
        )

        clear_form()
        search_entry.delete(0, tk.END)
        refresh_students()

    except sqlite3.IntegrityError as e:

        if "UNIQUE constraint failed" in str(e):
            messagebox.showerror(
                "Duplicate Email",
                "This email address already exists!"
            )
        else:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


# ==========================================
# 7. SELECT STUDENT
# ==========================================

def select_student(event):

    global selected_id

    selection = student_tree.selection()

    if not selection:
        return

    student = student_tree.item(selection[0], "values")

    selected_id = int(student[0])

    clear_form_fields()

    name_entry.insert(0, student[1])
    email_entry.insert(0, student[2])
    department_entry.insert(0, student[3])
    semester_entry.insert(0, student[4])


# Helper function
def clear_form_fields():

    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)
    semester_entry.delete(0, tk.END)


# ==========================================
# 8. UPDATE STUDENT
# ==========================================

def update_student():

    if selected_id is None:
        messagebox.showwarning(
            "Selection Required",
            "Please select a student first!"
        )
        return

    data = validate_input()

    if data is None:
        return

    try:
        with conn:

            cursor.execute("""
                UPDATE students
                SET name = ?,
                    email = ?,
                    department = ?,
                    semester = ?
                WHERE id = ?
            """, (*data, selected_id))

            if cursor.rowcount == 0:
                raise ValueError("Student record no longer exists.")

        messagebox.showinfo(
            "Success",
            "Student updated successfully!"
        )

        clear_form()
        refresh_students(search_entry.get().strip())

    except sqlite3.IntegrityError as e:

        if "UNIQUE constraint failed" in str(e):
            messagebox.showerror(
                "Duplicate Email",
                "Another student already uses this email!"
            )
        else:
            messagebox.showerror("Database Error", str(e))

    except (sqlite3.Error, ValueError) as e:
        messagebox.showerror("Update Error", str(e))


# ==========================================
# 9. DELETE STUDENT
# ==========================================

def delete_student():

    if selected_id is None:
        messagebox.showwarning(
            "Selection Required",
            "Please select a student first!"
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Deletion",
        "Are you sure you want to delete this student?"
    )

    if not confirm:
        return

    try:
        with conn:

            cursor.execute("""
                DELETE FROM students
                WHERE id = ?
            """, (selected_id,))

            if cursor.rowcount == 0:
                raise ValueError("Student record no longer exists.")

        messagebox.showinfo(
            "Success",
            "Student deleted successfully!"
        )

        clear_form()
        refresh_students(search_entry.get().strip())

    except (sqlite3.Error, ValueError) as e:
        messagebox.showerror("Delete Error", str(e))


# ==========================================
# 10. SEARCH STUDENT
# ==========================================

def search_student():

    search_text = search_entry.get().strip()

    clear_form()

    refresh_students(search_text)


def show_all_students():

    search_entry.delete(0, tk.END)
    clear_form()
    refresh_students()


# ==========================================
# 11. EXPORT TO CSV
# ==========================================

def export_csv():

    selection = student_tree.selection()

    if selection:

        records = [
            student_tree.item(item, "values")
            for item in selection
        ]

    else:

        confirm = messagebox.askyesno(
            "Export Records",
            "No students selected.\nExport all students instead?"
        )

        if not confirm:
            return

        try:
            cursor.execute("""
                SELECT id, name, email, department, semester
                FROM students
                ORDER BY id
            """)

            records = cursor.fetchall()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            return

    if not records:
        messagebox.showwarning(
            "No Records",
            "There are no records to export!"
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        initialfile="students.csv"
    )

    if not file_path:
        return

    try:
        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "ID",
                "Name",
                "Email",
                "Department",
                "Semester"
            ])

            writer.writerows(records)

        messagebox.showinfo(
            "Export Successful",
            f"{len(records)} record(s) exported successfully!"
        )

    except (OSError, csv.Error) as e:
        messagebox.showerror("Export Error", str(e))


# ==========================================
# 12. GUI DESIGN - TITLE
# ==========================================

title_label = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    fg="#1F4E79"
)

title_label.pack(pady=15)


# ==========================================
# 13. STUDENT FORM
# ==========================================

form_frame = tk.LabelFrame(
    root,
    text="Student Information",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=15
)

form_frame.pack(fill="x", padx=25, pady=10)


# Name
tk.Label(form_frame, text="Name:").grid(
    row=0, column=0, padx=10, pady=8, sticky="w"
)

name_entry = tk.Entry(form_frame, width=35)
name_entry.grid(row=0, column=1, padx=10, pady=8)


# Email
tk.Label(form_frame, text="Email:").grid(
    row=0, column=2, padx=10, pady=8, sticky="w"
)

email_entry = tk.Entry(form_frame, width=35)
email_entry.grid(row=0, column=3, padx=10, pady=8)


# Department
tk.Label(form_frame, text="Department:").grid(
    row=1, column=0, padx=10, pady=8, sticky="w"
)

department_entry = tk.Entry(form_frame, width=35)
department_entry.grid(row=1, column=1, padx=10, pady=8)


# Semester
tk.Label(form_frame, text="Semester:").grid(
    row=1, column=2, padx=10, pady=8, sticky="w"
)

semester_entry = tk.Entry(form_frame, width=35)
semester_entry.grid(row=1, column=3, padx=10, pady=8)


# ==========================================
# 14. CRUD BUTTONS
# ==========================================

button_frame = tk.LabelFrame(
    root,
    text="Student Operations",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=10
)

button_frame.pack(fill="x", padx=25, pady=10)


tk.Button(
    button_frame,
    text="Add Student",
    width=16,
    bg="#198754",
    fg="white",
    command=add_student
).grid(row=0, column=0, padx=10, pady=5)


tk.Button(
    button_frame,
    text="Update Student",
    width=16,
    bg="#0D6EFD",
    fg="white",
    command=update_student
).grid(row=0, column=1, padx=10, pady=5)


tk.Button(
    button_frame,
    text="Delete Student",
    width=16,
    bg="#DC3545",
    fg="white",
    command=delete_student
).grid(row=0, column=2, padx=10, pady=5)


tk.Button(
    button_frame,
    text="Clear Form",
    width=16,
    command=clear_form
).grid(row=0, column=3, padx=10, pady=5)


# ==========================================
# 15. SEARCH SECTION
# ==========================================

search_frame = tk.LabelFrame(
    root,
    text="Search Students",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=10
)

search_frame.pack(fill="x", padx=25, pady=10)


tk.Label(
    search_frame,
    text="Search by Name:"
).grid(row=0, column=0, padx=10)


search_entry = tk.Entry(search_frame, width=35)
search_entry.grid(row=0, column=1, padx=10)

search_entry.bind(
    "<Return>",
    lambda event: search_student()
)


tk.Button(
    search_frame,
    text="Search",
    width=12,
    command=search_student
).grid(row=0, column=2, padx=5)


tk.Button(
    search_frame,
    text="Show All",
    width=12,
    command=show_all_students
).grid(row=0, column=3, padx=5)


tk.Button(
    search_frame,
    text="Export CSV",
    width=12,
    command=export_csv
).grid(row=0, column=4, padx=5)


# ==========================================
# 16. STUDENT RECORDS TABLE
# ==========================================

table_frame = tk.LabelFrame(
    root,
    text="Student Records",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=10
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=10
)


columns = (
    "ID",
    "Name",
    "Email",
    "Department",
    "Semester"
)

student_tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="extended"
)


# Column headings
for column in columns:
    student_tree.heading(column, text=column)
    student_tree.column(column, width=150, anchor="center")


student_tree.column("ID", width=50)
student_tree.column("Semester", width=90)


# Scrollbar
scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=student_tree.yview
)

student_tree.configure(
    yscrollcommand=scrollbar.set
)

student_tree.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(side="right", fill="y")


# Select a record
student_tree.bind(
    "<<TreeviewSelect>>",
    select_student
)


# ==========================================
# 17. STATUS BAR
# ==========================================

status_label = tk.Label(
    root,
    text="Total displayed students: 0",
    anchor="w",
    font=("Arial", 10),
    fg="gray"
)

status_label.pack(fill="x", padx=25, pady=5)


# ==========================================
# 18. APPLICATION STARTUP
# ==========================================

refresh_students()

root.protocol(
    "WM_DELETE_WINDOW",
    lambda: close_application()
)


def close_application():

    conn.close()
    root.destroy()


root.mainloop()
