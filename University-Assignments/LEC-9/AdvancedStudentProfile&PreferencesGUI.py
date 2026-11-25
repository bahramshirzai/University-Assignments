
import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path


# ==========================================
# 1. MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title("Advanced Student Profile & Preferences")
root.geometry("950x850")
root.minsize(750, 700)

DATA_FILE = Path("student_profiles.json")


# ==========================================
# 2. CONTROL VARIABLES
# ==========================================

student_id_var = tk.StringVar()
name_var = tk.StringVar()
email_var = tk.StringVar()

department_var = tk.StringVar()

study_mode_var = tk.StringVar(value="")

email_notifications_var = tk.BooleanVar(value=False)
sms_notifications_var = tk.BooleanVar(value=False)
announcements_var = tk.BooleanVar(value=False)

experience_var = tk.IntVar(value=5)


# ==========================================
# 3. PROGRAMMING SKILLS
# ==========================================

programming_skills = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "HTML & CSS",
    "SQL",
    "PHP",
    "C#",
    "Dart",
    "React",
    "Node.js",
    "Machine Learning",
    "Data Science",
    "Cyber Security"
]


# ==========================================
# 4. GET FORM DATA
# ==========================================

def get_form_data():

    selected_indices = skills_listbox.curselection()

    selected_skills = [
        skills_listbox.get(index)
        for index in selected_indices
    ]

    preferences = []

    if email_notifications_var.get():
        preferences.append("Email Notifications")

    if sms_notifications_var.get():
        preferences.append("SMS Notifications")

    if announcements_var.get():
        preferences.append("Course Announcements")

    student_data = {
        "student_id": student_id_var.get().strip(),
        "name": name_var.get().strip(),
        "email": email_var.get().strip(),
        "department": department_var.get(),
        "study_mode": study_mode_var.get(),
        "preferences": preferences,
        "experience": experience_var.get(),
        "skills": selected_skills
    }

    return student_data


# ==========================================
# 5. VALIDATION FUNCTION
# ==========================================

def validate_form(data):

    if not data["student_id"]:
        messagebox.showerror(
            "Validation Error",
            "Please enter the Student ID."
        )
        student_id_entry.focus()
        return False

    if not data["name"]:
        messagebox.showerror(
            "Validation Error",
            "Please enter the Student Name."
        )
        name_entry.focus()
        return False

    if not data["email"]:
        messagebox.showerror(
            "Validation Error",
            "Please enter the Email Address."
        )
        email_entry.focus()
        return False

    # Basic email format validation
    if "@" not in data["email"] or "." not in data["email"].split("@")[-1]:
        messagebox.showerror(
            "Validation Error",
            "Please enter a valid Email Address."
        )
        email_entry.focus()
        return False

    if not data["department"]:
        messagebox.showerror(
            "Validation Error",
            "Please select a Department."
        )
        return False

    if not data["study_mode"]:
        messagebox.showerror(
            "Validation Error",
            "Please select a Study Mode."
        )
        return False

    if not data["preferences"]:
        messagebox.showerror(
            "Validation Error",
            "Please select at least one preference."
        )
        return False

    if not data["skills"]:
        messagebox.showerror(
            "Validation Error",
            "Please select at least one programming skill."
        )
        return False

    return True


# ==========================================
# 6. DISPLAY FORMATTED SUMMARY
# ==========================================

def display_summary(data):

    summary = f"""
==================================================
             STUDENT PROFILE SUMMARY
==================================================

STUDENT INFORMATION

Student ID:       {data['student_id']}
Student Name:     {data['name']}
Email Address:    {data['email']}
Department:       {data['department']}


STUDY PREFERENCES

Study Mode:       {data['study_mode']}

Programming Experience: {data['experience']}/10


COMMUNICATION PREFERENCES
"""

    for preference in data["preferences"]:
        summary += f"\n  - {preference}"

    summary += "\n\nPROGRAMMING SKILLS\n"

    for number, skill in enumerate(data["skills"], start=1):
        summary += f"\n  {number}. {skill}"

    summary += """

==================================================
               END OF PROFILE
==================================================
"""

    summary_text.config(state=tk.NORMAL)
    summary_text.delete("1.0", tk.END)
    summary_text.insert(tk.END, summary)
    summary_text.config(state=tk.DISABLED)


# ==========================================
# 7. SAVE FUNCTION
# ==========================================

def save_profile():

    data = get_form_data()

    # Validate all required information
    if not validate_form(data):
        return

    try:
        # Load existing profiles
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as file:
                profiles = json.load(file)

            if not isinstance(profiles, list):
                raise ValueError("Invalid profile file format.")

        else:
            profiles = []

        # Check duplicate student ID
        for profile in profiles:
            if profile.get("student_id") == data["student_id"]:
                messagebox.showerror(
                    "Duplicate Student",
                    "This Student ID already exists."
                )
                return

        # Add new profile
        profiles.append(data)

        # Save to JSON file
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                profiles,
                file,
                indent=4,
                ensure_ascii=False
            )

        # Display summary
        display_summary(data)

        messagebox.showinfo(
            "Success",
            "Student profile saved successfully!"
        )

    except json.JSONDecodeError:
        messagebox.showerror(
            "File Error",
            "The existing JSON file contains invalid data."
        )

    except (OSError, ValueError) as error:
        messagebox.showerror(
            "Save Error",
            f"Could not save the profile:\n{error}"
        )


# ==========================================
# 8. CLEAR / RESET FUNCTION
# ==========================================

def reset_form():

    student_id_var.set("")
    name_var.set("")
    email_var.set("")

    department_var.set("")

    study_mode_var.set("")

    email_notifications_var.set(False)
    sms_notifications_var.set(False)
    announcements_var.set(False)

    experience_var.set(5)

    skills_listbox.selection_clear(0, tk.END)

    summary_text.config(state=tk.NORMAL)
    summary_text.delete("1.0", tk.END)
    summary_text.config(state=tk.DISABLED)


# ==========================================
# 9. EXIT FUNCTION
# ==========================================

def exit_application():

    answer = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if answer:
        root.destroy()


# ==========================================
# 10. MAIN CONTAINER
# ==========================================

main_frame = ttk.Frame(root, padding=15)
main_frame.grid(
    row=0,
    column=0,
    sticky="nsew"
)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Responsive two-column layout
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

main_frame.rowconfigure(2, weight=1)
main_frame.rowconfigure(4, weight=2)


# ==========================================
# 11. TITLE
# ==========================================

title_label = ttk.Label(
    main_frame,
    text="ADVANCED STUDENT PROFILE & PREFERENCES",
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
# 12. STUDENT INFORMATION LABELFRAME
# ==========================================

student_frame = ttk.LabelFrame(
    main_frame,
    text="1. Student Information",
    padding=15
)

student_frame.grid(
    row=1,
    column=0,
    columnspan=2,
    sticky="ew",
    pady=8
)

# Responsive columns inside the frame
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
    row=0,
    column=1,
    padx=5,
    pady=8,
    sticky="ew"
)


# Student Name
ttk.Label(
    student_frame,
    text="Student Name:"
).grid(row=0, column=2, padx=5, pady=8, sticky="w")

name_entry = ttk.Entry(
    student_frame,
    textvariable=name_var
)

name_entry.grid(
    row=0,
    column=3,
    padx=5,
    pady=8,
    sticky="ew"
)


# Email
ttk.Label(
    student_frame,
    text="Email Address:"
).grid(row=1, column=0, padx=5, pady=8, sticky="w")

email_entry = ttk.Entry(
    student_frame,
    textvariable=email_var
)

email_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=8,
    sticky="ew"
)


# Department Combobox
ttk.Label(
    student_frame,
    text="Department:"
).grid(row=1, column=2, padx=5, pady=8, sticky="w")

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
    row=1,
    column=3,
    padx=5,
    pady=8,
    sticky="ew"
)


# ==========================================
# 13. STUDY PREFERENCES LABELFRAME
# ==========================================

preferences_frame = ttk.LabelFrame(
    main_frame,
    text="2. Study Preferences",
    padding=12
)

preferences_frame.grid(
    row=2,
    column=0,
    sticky="nsew",
    padx=(0, 7),
    pady=8
)


# Study Mode
mode_frame = ttk.LabelFrame(
    preferences_frame,
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


# Communication Preferences
communication_frame = ttk.LabelFrame(
    preferences_frame,
    text="Communication Preferences",
    padding=8
)

communication_frame.pack(fill="x", pady=5)


ttk.Checkbutton(
    communication_frame,
    text="Email Notifications",
    variable=email_notifications_var
).pack(anchor="w")

ttk.Checkbutton(
    communication_frame,
    text="SMS Notifications",
    variable=sms_notifications_var
).pack(anchor="w")

ttk.Checkbutton(
    communication_frame,
    text="Course Announcements",
    variable=announcements_var
).pack(anchor="w")


# Programming Experience Scale
experience_frame = ttk.LabelFrame(
    preferences_frame,
    text="Programming Experience (1-10)",
    padding=8
)

experience_frame.pack(fill="x", pady=5)


experience_scale = tk.Scale(
    experience_frame,
    from_=1,
    to=10,
    orient="horizontal",
    variable=experience_var,
    showvalue=True
)

experience_scale.pack(fill="x")


# ==========================================
# 14. SKILLS LABELFRAME
# ==========================================

skills_frame = ttk.LabelFrame(
    main_frame,
    text="3. Programming Skills (Multiple Selection)",
    padding=12
)

skills_frame.grid(
    row=2,
    column=1,
    sticky="nsew",
    padx=(7, 0),
    pady=8
)

skills_frame.columnconfigure(0, weight=1)
skills_frame.rowconfigure(0, weight=1)


# Listbox
skills_listbox = tk.Listbox(
    skills_frame,
    selectmode=tk.MULTIPLE,
    exportselection=False,
    height=12,
    font=("Arial", 10)
)

skills_listbox.grid(
    row=0,
    column=0,
    sticky="nsew"
)


# Insert skills
for skill in programming_skills:
    skills_listbox.insert(tk.END, skill)


# Scrollbar
skills_scrollbar = ttk.Scrollbar(
    skills_frame,
    orient="vertical",
    command=skills_listbox.yview
)

skills_scrollbar.grid(
    row=0,
    column=1,
    sticky="ns"
)

skills_listbox.config(
    yscrollcommand=skills_scrollbar.set
)


# ==========================================
# 15. ACTION AREA
# ==========================================

action_frame = ttk.LabelFrame(
    main_frame,
    text="4. Actions",
    padding=12
)

action_frame.grid(
    row=3,
    column=0,
    columnspan=2,
    sticky="ew",
    pady=8
)

for column in range(3):
    action_frame.columnconfigure(column, weight=1)


ttk.Button(
    action_frame,
    text="Save Profile",
    command=save_profile
).grid(
    row=0,
    column=0,
    padx=10,
    pady=5,
    sticky="ew"
)


ttk.Button(
    action_frame,
    text="Clear / Reset",
    command=reset_form
).grid(
    row=0,
    column=1,
    padx=10,
    pady=5,
    sticky="ew"
)


ttk.Button(
    action_frame,
    text="Exit",
    command=exit_application
).grid(
    row=0,
    column=2,
    padx=10,
    pady=5,
    sticky="ew"
)


# ==========================================
# 16. SUMMARY LABELFRAME
# ==========================================

summary_frame = ttk.LabelFrame(
    main_frame,
    text="5. Student Profile Summary",
    padding=10
)

summary_frame.grid(
    row=4,
    column=0,
    columnspan=2,
    sticky="nsew",
    pady=8
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
# 17. START APPLICATION
# ==========================================

root.protocol("WM_DELETE_WINDOW", exit_application)

root.mainloop()
