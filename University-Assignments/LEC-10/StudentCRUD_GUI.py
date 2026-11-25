
import tkinter as tk
from tkinter import ttk, messagebox
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
# 2. MAIN WINDOW
# ==================================

root = tk.Tk()
root.title("Student Management System")
root.geometry("850x600")
root.resizable(False, False)


# Selected student ID
selected_id = None


# ==================================
# 3. FUNCTIONS
# ==================================

# Clear input fields
def clear_fields():
    global selected_id

    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)
    semester_entry.delete(0, tk.END)

    selected_id = None


# Display students
def display_students(search=""):

    student_list.delete(0, tk.END)

    cursor.execute("""
    SELECT * FROM students
    WHERE name LIKE ?
    ORDER BY id
    """, ('%' + search + '%',))

    records = cursor.fetchall()

    for student in records:
        student_list.insert(
            tk.END,
            f"ID: {student[0]} | Name: {student[1]} | "
            f"Email: {student[2]} | Department: {student[3]} | "
            f"Semester: {student[4]}"
        )


# Add new student
def add_student():

    name = name_entry.get().strip()
    email = email_entry.get().strip()
    department = department_entry.get().strip()
    semester = semester_entry.get().strip()

    # Required field validation
    if not name or not email or not department or not semester:
        messagebox.showerror("Error", "All fields are required!")
        return

    # Semester validation
    if not semester.isdigit() or int(semester) < 1:
        messagebox.showerror("Error", "Semester must be a positive number!")
        return

    try:
        cursor.execute("""
        INSERT INTO students (name, email, department, semester)
        VALUES (?, ?, ?, ?)
        """, (name, email, department, int(semester)))

        conn.commit()

        messagebox.showinfo("Success", "Student added successfully!")

        clear_fields()
        display_students()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "This email already exists!")


# Select student from Listbox
def select_student(event):

    global selected_id

    selection = student_list.curselection()

    if not selection:
        return

    selected_text = student_list.get(selection[0])

    selected_id = int(selected_text.split("|")[0].replace("ID:", "").strip())

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (selected_id,)
    )

    student = cursor.fetchone()

    if student:

        clear_form_only()

        name_entry.insert(0, student[1])
        email_entry.insert(0, student[2])
        department_entry.insert(0, student[3])
        semester_entry.insert(0, student[4])


# Clear form without removing selected ID
def clear_form_only():

    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)
    semester_entry.delete(0, tk.END)


# Update selected student
def update_student():

    if selected_id is None:
        messagebox.showerror("Error", "Please select a student first!")
        return

    name = name_entry.get().strip()
    email = email_entry.get().strip()
    department = department_entry.get().strip()
    semester = semester_entry.get().strip()

    if not name or not email or not department or not semester:
        messagebox.showerror("Error", "All fields are required!")
        return

    if not semester.isdigit() or int(semester) < 1:
        messagebox.showerror("Error", "Invalid semester!")
        return

    try:
        cursor.execute("""
        UPDATE students
        SET name = ?, email = ?, department = ?, semester = ?
        WHERE id = ?
        """, (name, email, department, int(semester), selected_id))

        conn.commit()

        messagebox.showinfo("Success", "Student updated successfully!")

        clear_fields()
        display_students()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "This email already exists!")


# Delete selected student
def delete_student():

    if selected_id is None:
        messagebox.showerror("Error", "Please select a student first!")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if confirm:

        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (selected_id,)
        )

        conn.commit()

        messagebox.showinfo("Success", "Student deleted successfully!")

        clear_fields()
        display_students()


# Search students by name
def search_student():

    search_text = search_entry.get().strip()

    display_students(search_text)


# ==================================
# 4. GUI DESIGN
# ==================================

title_label = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold"),
    fg="blue"
)

title_label.pack(pady=15)


# Form Frame
form_frame = tk.Frame(root)
form_frame.pack(pady=10)


# Name
tk.Label(form_frame, text="Name:", font=("Arial", 11)).grid(
    row=0, column=0, padx=10, pady=8, sticky="w"
)

name_entry = tk.Entry(form_frame, width=35)
name_entry.grid(row=0, column=1, padx=10, pady=8)


# Email
tk.Label(form_frame, text="Email:", font=("Arial", 11)).grid(
    row=1, column=0, padx=10, pady=8, sticky="w"
)

email_entry = tk.Entry(form_frame, width=35)
email_entry.grid(row=1, column=1, padx=10, pady=8)


# Department
tk.Label(form_frame, text="Department:", font=("Arial", 11)).grid(
    row=2, column=0, padx=10, pady=8, sticky="w"
)

department_entry = tk.Entry(form_frame, width=35)
department_entry.grid(row=2, column=1, padx=10, pady=8)


# Semester
tk.Label(form_frame, text="Semester:", font=("Arial", 11)).grid(
    row=3, column=0, padx=10, pady=8, sticky="w"
)

semester_entry = tk.Entry(form_frame, width=35)
semester_entry.grid(row=3, column=1, padx=10, pady=8)


# ==================================
# 5. BUTTONS
# ==================================

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(
    button_frame, text="Add Student",
    width=15, bg="green", fg="white",
    command=add_student
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame, text="Update",
    width=15, bg="blue", fg="white",
    command=update_student
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame, text="Delete",
    width=15, bg="red", fg="white",
    command=delete_student
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame, text="Clear",
    width=15, command=clear_fields
).grid(row=0, column=3, padx=5)


# ==================================
# 6. SEARCH SECTION
# ==================================

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(
    search_frame,
    text="Search by Name:",
    font=("Arial", 11)
).grid(row=0, column=0, padx=5)

search_entry = tk.Entry(search_frame, width=30)
search_entry.grid(row=0, column=1, padx=5)

tk.Button(
    search_frame,
    text="Search",
    command=search_student
).grid(row=0, column=2, padx=5)

tk.Button(
    search_frame,
    text="Show All",
    command=lambda: display_students()
).grid(row=0, column=3, padx=5)


# ==================================
# 7. STUDENT LISTBOX
# ==================================

list_frame = tk.Frame(root)
list_frame.pack(pady=10)

tk.Label(
    list_frame,
    text="Student Records (Select a student to edit):",
    font=("Arial", 12, "bold")
).pack(pady=5)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

student_list = tk.Listbox(
    list_frame,
    width=105,
    height=12,
    font=("Arial", 9),
    yscrollcommand=scrollbar.set
)

student_list.pack(side=tk.LEFT)

scrollbar.config(command=student_list.yview)

student_list.bind("<<ListboxSelect>>", select_student)


# ==================================
# 8. LOAD RECORDS AND RUN GUI
# ==================================

display_students()

root.mainloop()


# Close database connection after GUI closes
conn.close()
