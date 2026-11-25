
import tkinter as tk
from tkinter import ttk, messagebox


# =====================================
# 1. MAIN WINDOW
# =====================================

root = tk.Tk()
root.title("Course Selection System")
root.geometry("550x600")
root.resizable(False, False)


# =====================================
# 2. COURSE LIST
# =====================================

courses = [
    "Programming Fundamentals",
    "Database Systems",
    "Computer Networks",
    "Data Structures",
    "Web Development",
    "Operating Systems",
    "Information Systems",
    "Software Engineering",
    "Python Programming",
    "Computer Architecture",
    "Artificial Intelligence",
    "Cyber Security",
    "Discrete Mathematics",
    "System Analysis and Design"
]


# =====================================
# 3. TITLE
# =====================================

title_label = tk.Label(
    root,
    text="COURSE SELECTION SYSTEM",
    font=("Arial", 19, "bold"),
    fg="#1F4E79"
)

title_label.pack(pady=15)


# =====================================
# 4. COURSE SELECTION FRAME
# =====================================

course_frame = tk.LabelFrame(
    root,
    text="Select Your Courses",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10
)

course_frame.pack(
    fill="x",
    padx=25,
    pady=10
)


# =====================================
# 5. LISTBOX WITH MULTIPLE SELECTION
# =====================================

list_frame = tk.Frame(course_frame)
list_frame.pack()


course_listbox = tk.Listbox(
    list_frame,
    width=45,
    height=10,
    selectmode=tk.MULTIPLE,
    font=("Arial", 11),
    exportselection=False
)

course_listbox.pack(side=tk.LEFT)


# Add courses to Listbox
for course in courses:
    course_listbox.insert(tk.END, course)


# =====================================
# 6. VERTICAL SCROLLBAR
# =====================================

scrollbar = tk.Scrollbar(
    list_frame,
    orient=tk.VERTICAL,
    command=course_listbox.yview
)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

course_listbox.config(
    yscrollcommand=scrollbar.set
)


# =====================================
# 7. SEMESTER COMBOBOX
# =====================================

semester_frame = tk.LabelFrame(
    root,
    text="Select Semester",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10
)

semester_frame.pack(
    fill="x",
    padx=25,
    pady=10
)


semester_var = tk.StringVar(value="Semester 1")


tk.Label(
    semester_frame,
    text="Semester:"
).pack(side=tk.LEFT, padx=10)


semester_combo = ttk.Combobox(
    semester_frame,
    textvariable=semester_var,
    values=[
        "Semester 1",
        "Semester 2",
        "Semester 3",
        "Semester 4",
        "Semester 5",
        "Semester 6",
        "Semester 7",
        "Semester 8"
    ],
    state="readonly",
    width=20
)

semester_combo.pack(side=tk.LEFT, padx=10)


# =====================================
# 8. SELECTED COURSE COUNTER
# =====================================

count_label = tk.Label(
    root,
    text="Selected Courses: 0",
    font=("Arial", 11, "bold"),
    fg="blue"
)

count_label.pack(pady=10)


# =====================================
# 9. LISTBOX SELECT EVENT
# =====================================

def update_count(event):

    selected = course_listbox.curselection()

    count_label.config(
        text=f"Selected Courses: {len(selected)}"
    )


course_listbox.bind(
    "<<ListboxSelect>>",
    update_count
)


# =====================================
# 10. DISPLAY SELECTED COURSES
# =====================================

def display_selection():

    selected_indices = course_listbox.curselection()

    selected_semester = semester_var.get()

    if not selected_indices:
        messagebox.showwarning(
            "No Selection",
            "Please select at least one course!"
        )
        return

    selected_courses = [
        course_listbox.get(index)
        for index in selected_indices
    ]

    result = "SELECTED COURSES\n\n"

    result += f"Semester: {selected_semester}\n\n"

    for number, course in enumerate(selected_courses, start=1):
        result += f"{number}. {course}\n"

    result += f"\nTotal Courses: {len(selected_courses)}"

    messagebox.showinfo(
        "Course Selection Result",
        result
    )


# =====================================
# 11. CLEAR SELECTION
# =====================================

def clear_selection():

    course_listbox.selection_clear(0, tk.END)

    count_label.config(
        text="Selected Courses: 0"
    )


# =====================================
# 12. BUTTONS
# =====================================

button_frame = tk.Frame(root)

button_frame.pack(pady=15)


tk.Button(
    button_frame,
    text="Display Selection",
    bg="#198754",
    fg="white",
    width=18,
    command=display_selection
).pack(side=tk.LEFT, padx=10)


tk.Button(
    button_frame,
    text="Clear Selection",
    bg="#DC3545",
    fg="white",
    width=18,
    command=clear_selection
).pack(side=tk.LEFT, padx=10)


# =====================================
# 13. RUN APPLICATION
# =====================================

root.mainloop()
