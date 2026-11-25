
import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path


# ==========================================
# 1. CONFIGURATION
# ==========================================

root = tk.Tk()
root.title("University Course Registration System")
root.geometry("1000x850")
root.minsize(800, 700)

DATA_FILE = Path("registrations.json")


# ==========================================
# 2. DATA VARIABLES
# ==========================================

student_id_var = tk.StringVar()
student_name_var = tk.StringVar()
department_var = tk.StringVar()

semester_var = tk.StringVar()
study_mode_var = tk.StringVar()

email_var = tk.BooleanVar(value=False)
sms_var = tk.BooleanVar(value=False)
announcements_var = tk.BooleanVar(value=False)

priority_var = tk.IntVar(value=5)


# ==========================================
# 3. COURSE DATA
# ==========================================

courses = [
    "Programming Fundamentals",
    "Python Programming",
    "Database Systems",
    "Data Structures",
    "Computer Networks",
    "Operating Systems",
    "Web Development",
    "Software Engineering",
    "Information Systems",
    "System Analysis and Design",
    "Computer Architecture",
    "Artificial Intelligence",
    "Cyber Security",
    "Discrete Mathematics",
    "Mobile Application Development",
    "Data Science"
]


# ==========================================
# 4. HELPER FUNCTIONS
# ==========================================

def load_registrations():
    """Read existing registrations from the JSON file."""

    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        messagebox.showerror(
            "File Error",
            "The registration file has an invalid format."
        )
        return []

    except (json.JSONDecodeError, OSError):
        messagebox.showerror(
            "File Error",
            "Could not read the registration file."
        )
        return []


def save_registration(registration):
    """Save one registration to the JSON file."""

    registrations = load_registrations()

    # Prevent duplicate student registrations
    for item in registrations:
        if item.get("student_id") == registration["student_id"]:
            raise ValueError(
                "This Student ID has already been registered."
            )

    registrations.append(registration)

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            registrations,
            file,
            indent=4,
            ensure_ascii=False
        )


def show_summary(registration):
    """Display registration information in the summary area."""

    summary = f"""
==================================================
             COURSE REGISTRATION SUMMARY
==================================================

STUDENT INFORMATION

Student ID:       {registration['student_id']}
Student Name:     {registration['student_name']}
Department:       {registration['department']}


COURSE INFORMATION

Semester:         {registration['semester']}

Selected Courses:
"""

    for number, course in enumerate(
        registration["courses"], start=1
    ):
        summary += f"  {number}. {course}\n"

    summary += f"""

STUDY INFORMATION

Study Mode:       {registration['study_mode']}
Priority Level:   {registration['priority_level']}/10


COMMUNICATION PREFERENCES

"""

    if registration["preferences"]:
        for preference in registration["preferences"]:
            summary += f"  - {preference}\n"
    else:
        summary += "  No preferences selected.\n"

    summary += """
==================================================
             REGISTRATION COMPLETED
==================================================
"""

    summary_text.config(state=tk.NORMAL)
    summary_text.delete("1.0", tk.END)
    summary_text.insert(tk.END, summary)
    summary_text.config(state=tk.DISABLED)


# ==========================================
# 5. REGISTER FUNCTION
# ==========================================

def register_student():

    # Read student information
    student_id = student_id_var.get().strip()
    student_name = student_name_var.get().strip()
    department = department_var.get()

    # Read selected courses
    selected_indices = course_listbox.curselection()

    selected_courses = [
        course_listbox.get(index)
        for index in selected_indices
    ]

    # Read semester and study mode
    semester = semester_var.get()
    study_mode = study_mode_var.get()

    # Read communication preferences
    preferences = []

    if email_var.get():
        preferences.append("Email")

    if sms_var.get():
        preferences.append("SMS")

    if announcements_var.get():
        preferences.append("Course Announcements")

    # Read priority level
    priority_level = priority_var.get()

    # ======================================
    # VALIDATION
    # ======================================

    if not student_id:
        messagebox.showerror(
            "Validation Error",
            "Please enter the Student ID."
        )
        student_id_entry.focus()
        return

    if not student_name:
        messagebox.showerror(
            "Validation Error",
            "Please enter the Student Name."
        )
        student_name_entry.focus()
        return

    if not department:
        messagebox.showerror(
            "Validation Error",
            "Please select a Department."
        )
        return

    if not selected_courses:
        messagebox.showerror(
            "Validation Error",
            "Please select at least one course."
        )
        return

    if not semester:
        messagebox.showerror(
            "Validation Error",
            "Please select a Semester."
        )
        return

    if not study_mode:
        messagebox.showerror(
            "Validation Error",
            "Please select a Study Mode."
        )
        return

    # ======================================
    # CREATE REGISTRATION DICTIONARY
    # ======================================

    registration = {
        "student_id": student_id,
        "student_name": student_name,
        "department": department,
        "courses": selected_courses,
        "semester": semester,
        "study_mode": study_mode,
        "preferences": preferences,
        "priority_level": priority_level
    }

    # ======================================
    # SAVE REGISTRATION
    # ======================================

    try:
        save_registration(registration)

        show_summary(registration)

        messagebox.showinfo(
            "Registration Successful",
            "Student registration saved successfully!"
        )

    except ValueError as error:
        messagebox.showerror(
            "Registration Error",
            str(error)
        )

    except OSError as error:
        messagebox.showerror(
            "File Error",
            f"Could not save registration:\n{error}"
        )


# ==========================================
# 6. CLEAR FUNCTION
# ==========================================

def clear_form():

    student_id_var.set("")
    student_name_var.set("")
    department_var.set("")

    semester_var.set("")
    study_mode_var.set("")

    course_listbox.selection_clear(0, tk.END)

    email_var.set(False)
    sms_var.set(False)
    announcements_var.set(False)

    priority_var.set(5)

    summary_text.config(state=tk.NORMAL)
    summary_text.delete("1.0", tk.END)
    summary_text.config(state=tk.DISABLED)


# ==========================================
# 7. EXIT FUNCTION
# ==========================================

def exit_application():

    answer = messagebox.askyesno(
        "Exit Application",
        "Are you sure you want to exit?"
    )

    if answer:
        root.destroy()


# ==========================================
# 8. MAIN CONTAINER
# ==========================================

main_frame = ttk.Frame(root, padding=15)
main_frame.pack(fill="both", expand=True)

# Responsive grid configuration
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

main_frame.rowconfigure(2, weight=1)
main_frame.rowconfigure(4, weight=2)


# ==========================================
# 9. TITLE
# ==========================================

title_label = ttk.Label(
    main_frame,
    text="UNIVERSITY COURSE REGISTRATION",
    font=("Arial", 19, "bold"),
    anchor="center"
)

title_label.grid(
    row=0,
    column=0,
    columnspan=2,
    sticky="ew",
    pady=(0, 15)
)


# ==========================================
# 10. STUDENT INFORMATION SECTION
# ==========================================

student_frame = ttk.LabelFrame(
    main_frame,
    text="Student Information",
    padding=12
)

student_frame.grid(
    row=1,
    column=0,
    columnspan=2,
    sticky="ew",
    pady=5
)

student_frame.columnconfigure(1, weight=1)
student_frame.columnconfigure(3, weight=1)


# Student ID
ttk.Label(
    student_frame,
    text="Student ID:"
).grid(row=0, column=0, padx=5, pady=8, sticky="w")

student_id_entry = ttk.Entry(
    student_frame,
    textvariable=student_id_var
)

student_id_entry.grid(
    row=0, column=1,
    padx=5, pady=8,
    sticky="ew"
)


# Student Name
ttk.Label(
    student_frame,
    text="Student Name:"
).grid(row=0, column=2, padx=5, pady=8, sticky="w")

student_name_entry = ttk.Entry(
    student_frame,
    textvariable=student_name_var
)

student_name_entry.grid(
    row=0, column=3,
    padx=5, pady=8,
    sticky="ew"
)


# Department
ttk.Label(
    student_frame,
    text="Department:"
).grid(row=1, column=0, padx=5, pady=8, sticky="w")

department_combo = ttk.Combobox(
    student_frame,
    textvariable=department_var,
    values=[
        "Information Systems",
        "Computer Science",
        "Software Engineering",
        "Information Technology",
        "Cyber Security"
    ],
    state="readonly"
)

department_combo.grid(
    row=1, column=1,
    padx=5, pady=8,
    sticky="ew"
)


# ==========================================
# 11. COURSE SELECTION SECTION
# ==========================================

course_frame = ttk.LabelFrame(
    main_frame,
    text="Course Selection (Multiple Selection)",
    padding=10
)

course_frame.grid(
    row=2,
    column=0,
    sticky="nsew",
    padx=(0, 7),
    pady=5
)

course_frame.columnconfigure(0, weight=1)
course_frame.rowconfigure(0, weight=1)


course_listbox = tk.Listbox(
    course_frame,
    selectmode=tk.MULTIPLE,
    exportselection=False,
    font=("Arial", 10),
    height=12
)

course_listbox.grid(
    row=0,
    column=0,
    sticky="nsew"
)


# Insert courses into Listbox
for course in courses:
    course_listbox.insert(tk.END, course)


# Vertical Scrollbar
course_scrollbar = ttk.Scrollbar(
    course_frame,
    orient="vertical",
    command=course_listbox.yview
)

course_scrollbar.grid(
    row=0,
    column=1,
    sticky="ns"
)

course_listbox.config(
    yscrollcommand=course_scrollbar.set
)


# ==========================================
# 12. REGISTRATION DETAILS SECTION
# ==========================================

details_frame = ttk.LabelFrame(
    main_frame,
    text="Registration Details",
    padding=10
)

details_frame.grid(
    row=2,
    column=1,
    sticky="nsew",
    padx=(7, 0),
    pady=5
)


# Nested Frame: Semester
semester_frame = ttk.LabelFrame(
    details_frame,
    text="Semester",
    padding=8
)

semester_frame.pack(fill="x", pady=5)


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
    state="readonly"
)

semester_combo.pack(fill="x")


# Nested Frame: Study Mode
mode_frame = ttk.LabelFrame(
    details_frame,
    text="Study Mode",
    padding=8
)

mode_frame.pack(fill="x", pady=5)


ttk.Radiobutton(
    mode_frame,
    text="On-Campus",
    variable=study_mode_var,
    value="On-Campus"
).pack(anchor="w")

ttk.Radiobutton(
    mode_frame,
    text="Online",
    variable=study_mode_var,
    value="Online"
).pack(anchor="w")

ttk.Radiobutton(
    mode_frame,
    text="Hybrid",
    variable=study_mode_var,
    value="Hybrid"
).pack(anchor="w")


# Nested Frame: Preferences
preferences_frame = ttk.LabelFrame(
    details_frame,
    text="Communication Preferences",
    padding=8
)

preferences_frame.pack(fill="x", pady=5)


ttk.Checkbutton(
    preferences_frame,
    text="Email Notifications",
    variable=email_var
).pack(anchor="w")

ttk.Checkbutton(
    preferences_frame,
    text="SMS Notifications",
    variable=sms_var
).pack(anchor="w")

ttk.Checkbutton(
    preferences_frame,
    text="Course Announcements",
    variable=announcements_var
).pack(anchor="w")


# Nested Frame: Priority / Experience
priority_frame = ttk.LabelFrame(
    details_frame,
    text="Priority / Experience Level",
    padding=8
)

priority_frame.pack(fill="x", pady=5)


priority_scale = tk.Scale(
    priority_frame,
    from_=1,
    to=10,
    orient="horizontal",
    variable=priority_var,
    showvalue=True
)

priority_scale.pack(fill="x")


# ==========================================
# 13. ACTION AREA
# ==========================================

action_frame = ttk.LabelFrame(
    main_frame,
    text="Actions",
    padding=10
)

action_frame.grid(
    row=3,
    column=0,
    columnspan=2,
    sticky="ew",
    pady=10
)


action_frame.columnconfigure(
    (0, 1, 2),
    weight=1
)


register_button = ttk.Button(
    action_frame,
    text="Register",
    command=register_student
)

register_button.grid(
    row=0, column=0,
    padx=10, pady=5,
    sticky="ew"
)


clear_button = ttk.Button(
    action_frame,
    text="Clear",
    command=clear_form
)

clear_button.grid(
    row=0, column=1,
    padx=10, pady=5,
    sticky="ew"
)


exit_button = ttk.Button(
    action_frame,
    text="Exit",
    command=exit_application
)

exit_button.grid(
    row=0, column=2,
    padx=10, pady=5,
    sticky="ew"
)


# ==========================================
# 14. SUMMARY AREA
# ==========================================

summary_frame = ttk.LabelFrame(
    main_frame,
    text="Registration Summary",
    padding=10
)

summary_frame.grid(
    row=4,
    column=0,
    columnspan=2,
    sticky="nsew",
    pady=5
)

summary_frame.columnconfigure(0, weight=1)
summary_frame.rowconfigure(0, weight=1)


summary_text = tk.Text(
    summary_frame,
    height=12,
    font=("Consolas", 10),
    wrap="word",
    state=tk.DISABLED
)

summary_text.grid(
    row=0,
    column=0,
    sticky="nsew"
)


# Summary Scrollbar
summary_scrollbar = ttk.Scrollbar(
    summary_frame,
    orient="vertical",
    command=summary_text.yview
)

summary_scrollbar.grid(
    row=0,
    column=1,
    sticky="ns"
)

summary_text.config(
    yscrollcommand=summary_scrollbar.set
)


# ==========================================
# 15. START APPLICATION
# ==========================================

root.protocol("WM_DELETE_WINDOW", exit_application)

root.mainloop()
