
import tkinter as tk
from tkinter import ttk, messagebox


# ==========================================
# 1. MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title("Student Preferences Form")
root.geometry("650x800")
root.resizable(False, False)


# ==========================================
# 2. VARIABLES
# ==========================================

# Study Mode
study_mode_var = tk.StringVar(value="")

# Communication Preferences
email_var = tk.BooleanVar(value=False)
sms_var = tk.BooleanVar(value=False)
phone_var = tk.BooleanVar(value=False)

# Programming Experience
experience_var = tk.IntVar(value=1)

# Department
department_var = tk.StringVar(value="")


# ==========================================
# 3. DISPLAY SUMMARY FUNCTION
# ==========================================

def submit_form():

    # Get student name
    student_name = name_entry.get().strip()

    # Get department
    department = department_var.get()

    # Get study mode
    study_mode = study_mode_var.get()

    # Get communication preferences
    communication = []

    if email_var.get():
        communication.append("Email")

    if sms_var.get():
        communication.append("SMS")

    if phone_var.get():
        communication.append("Phone")

    # Get programming experience
    experience = experience_var.get()

    # Get selected skills
    selected_indices = skills_listbox.curselection()

    selected_skills = [
        skills_listbox.get(index)
        for index in selected_indices
    ]

    # ==================================
    # VALIDATION
    # ==================================

    if not student_name:
        messagebox.showerror(
            "Validation Error",
            "Please enter your name!"
        )
        name_entry.focus()
        return

    if not department:
        messagebox.showerror(
            "Validation Error",
            "Please select a department!"
        )
        return

    if not study_mode:
        messagebox.showerror(
            "Validation Error",
            "Please select a study mode!"
        )
        return

    if not communication:
        messagebox.showerror(
            "Validation Error",
            "Please select at least one communication preference!"
        )
        return

    if not selected_skills:
        messagebox.showerror(
            "Validation Error",
            "Please select at least one programming skill!"
        )
        return

    # ==================================
    # STRUCTURED SUMMARY
    # ==================================

    summary = f"""
====================================
       STUDENT PREFERENCES
====================================

STUDENT INFORMATION

Name: {student_name}

Department: {department}


STUDY INFORMATION

Study Mode: {study_mode}

Programming Experience: {experience}/10


COMMUNICATION PREFERENCES

{", ".join(communication)}


PROGRAMMING SKILLS

"""

    for number, skill in enumerate(selected_skills, start=1):
        summary += f"{number}. {skill}\n"

    summary += """
====================================
       END OF SUMMARY
====================================
"""

    # Display summary in Text widget
    summary_text.config(state=tk.NORMAL)
    summary_text.delete("1.0", tk.END)
    summary_text.insert(tk.END, summary)
    summary_text.config(state=tk.DISABLED)

    messagebox.showinfo(
        "Success",
        "Student preferences submitted successfully!"
    )


# ==========================================
# 4. RESET FORM FUNCTION
# ==========================================

def reset_form():

    name_entry.delete(0, tk.END)

    department_var.set("")
    study_mode_var.set("")

    email_var.set(False)
    sms_var.set(False)
    phone_var.set(False)

    experience_var.set(1)

    skills_listbox.selection_clear(0, tk.END)

    summary_text.config(state=tk.NORMAL)
    summary_text.delete("1.0", tk.END)
    summary_text.config(state=tk.DISABLED)


# ==========================================
# 5. MAIN TITLE
# ==========================================

title_label = tk.Label(
    root,
    text="STUDENT PREFERENCES FORM",
    font=("Arial", 20, "bold"),
    fg="#1F4E79"
)

title_label.pack(pady=15)


# ==========================================
# 6. STUDENT INFORMATION
# ==========================================

student_frame = tk.LabelFrame(
    root,
    text="Student Information",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10
)

student_frame.pack(
    fill="x",
    padx=25,
    pady=8
)


# Student Name
tk.Label(
    student_frame,
    text="Student Name:"
).grid(row=0, column=0, padx=10, pady=8, sticky="w")


name_entry = tk.Entry(
    student_frame,
    width=40
)

name_entry.grid(row=0, column=1, padx=10, pady=8)


# Department Combobox
tk.Label(
    student_frame,
    text="Department:"
).grid(row=1, column=0, padx=10, pady=8, sticky="w")


department_combo = ttk.Combobox(
    student_frame,
    textvariable=department_var,
    values=[
        "Computer Science",
        "Information Systems",
        "Software Engineering",
        "Information Technology",
        "Cyber Security"
    ],
    state="readonly",
    width=37
)

department_combo.grid(row=1, column=1, padx=10, pady=8)


# ==========================================
# 7. STUDY MODE RADIOBUTTONS
# ==========================================

study_frame = tk.LabelFrame(
    root,
    text="Study Mode",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10
)

study_frame.pack(
    fill="x",
    padx=25,
    pady=8
)


tk.Radiobutton(
    study_frame,
    text="On-Campus",
    variable=study_mode_var,
    value="On-Campus"
).pack(side="left", padx=15)


tk.Radiobutton(
    study_frame,
    text="Online",
    variable=study_mode_var,
    value="Online"
).pack(side="left", padx=15)


tk.Radiobutton(
    study_frame,
    text="Hybrid",
    variable=study_mode_var,
    value="Hybrid"
).pack(side="left", padx=15)


# ==========================================
# 8. COMMUNICATION CHECKBUTTONS
# ==========================================

communication_frame = tk.LabelFrame(
    root,
    text="Communication Preferences",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10
)

communication_frame.pack(
    fill="x",
    padx=25,
    pady=8
)


tk.Checkbutton(
    communication_frame,
    text="Email",
    variable=email_var
).pack(side="left", padx=15)


tk.Checkbutton(
    communication_frame,
    text="SMS",
    variable=sms_var
).pack(side="left", padx=15)


tk.Checkbutton(
    communication_frame,
    text="Phone",
    variable=phone_var
).pack(side="left", padx=15)


# ==========================================
# 9. PROGRAMMING EXPERIENCE SCALE
# ==========================================

experience_frame = tk.LabelFrame(
    root,
    text="Programming Experience",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10
)

experience_frame.pack(
    fill="x",
    padx=25,
    pady=8
)


tk.Label(
    experience_frame,
    text="Experience Level (1-10):"
).pack(anchor="w")


experience_scale = tk.Scale(
    experience_frame,
    from_=1,
    to=10,
    orient="horizontal",
    variable=experience_var,
    length=450
)

experience_scale.pack()


# ==========================================
# 10. PROGRAMMING SKILLS LISTBOX
# ==========================================

skills_frame = tk.LabelFrame(
    root,
    text="Programming Skills (Select Multiple)",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10
)

skills_frame.pack(
    fill="x",
    padx=25,
    pady=8
)


skills = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "HTML & CSS",
    "SQL",
    "PHP",
    "C#",
    "Dart",
    "React"
]


skills_listbox = tk.Listbox(
    skills_frame,
    selectmode=tk.MULTIPLE,
    height=5,
    width=45,
    exportselection=False
)

skills_listbox.pack(side="left", padx=10)


# Add skills
for skill in skills:
    skills_listbox.insert(tk.END, skill)


# Scrollbar
skills_scrollbar = tk.Scrollbar(
    skills_frame,
    orient="vertical",
    command=skills_listbox.yview
)

skills_scrollbar.pack(side="left", fill="y")

skills_listbox.config(
    yscrollcommand=skills_scrollbar.set
)


# ==========================================
# 11. SUBMIT AND RESET BUTTONS
# ==========================================

button_frame = tk.Frame(root)

button_frame.pack(pady=12)


tk.Button(
    button_frame,
    text="Submit Preferences",
    bg="#198754",
    fg="white",
    width=20,
    command=submit_form
).pack(side="left", padx=10)


tk.Button(
    button_frame,
    text="Reset Form",
    bg="#DC3545",
    fg="white",
    width=20,
    command=reset_form
).pack(side="left", padx=10)


# ==========================================
# 12. SUMMARY TEXT AREA
# ==========================================

summary_frame = tk.LabelFrame(
    root,
    text="Student Preferences Summary",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=10
)

summary_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=8
)


summary_text = tk.Text(
    summary_frame,
    height=9,
    width=65,
    font=("Courier New", 9),
    state=tk.DISABLED
)

summary_text.pack(
    fill="both",
    expand=True
)


# ==========================================
# 13. RUN APPLICATION
# ==========================================

root.mainloop()
