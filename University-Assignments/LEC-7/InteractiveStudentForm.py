
import tkinter as tk
from tkinter import messagebox
import csv
import os


# Create main window
window = tk.Tk()
window.title("Interactive Student Form")
window.geometry("500x500")
window.resizable(False, False)


# Store field information
fields = {}
after_id = None


# -------------------------------
# Helper 1: Display status message
# -------------------------------
def show_message(message, color="blue", temporary=False):
    global after_id

    # Cancel previous scheduled message
    if after_id is not None:
        window.after_cancel(after_id)
        after_id = None

    status_label.config(text=message, fg=color)

    # Clear temporary message after 3 seconds
    if temporary:
        after_id = window.after(3000, clear_message)


def clear_message():
    global after_id

    status_label.config(text="")
    after_id = None


# -------------------------------
# Helper 2: Validate one field
# -------------------------------
def validate_field(field_name):
    value = fields[field_name].get().strip()

    if value == "":
        show_message(f"{field_name} is required!", "red")
        return False

    if field_name == "Email" and "@" not in value:
        show_message("Please enter a valid email address.", "red")
        return False

    return True


# -------------------------------
# Helper 3: Validate all fields
# -------------------------------
def validate_form():
    for field_name in fields:
        if not validate_field(field_name):
            fields[field_name].focus_set()
            return False

    return True


# -------------------------------
# Helper 4: Get student data
# -------------------------------
def get_student_data():
    return {
        "Name": fields["Name"].get().strip(),
        "Student ID": fields["Student ID"].get().strip(),
        "Email": fields["Email"].get().strip(),
        "Course": fields["Course"].get().strip()
    }


# -------------------------------
# Helper 5: Save student data
# -------------------------------
def save_student():
    if not validate_form():
        return

    student = get_student_data()

    file_exists = os.path.isfile("students.csv")

    try:
        with open("students.csv", "a", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["Name", "Student ID", "Email", "Course"]
            )

            # Write headings if file is new or empty
            if not file_exists or os.path.getsize("students.csv") == 0:
                writer.writeheader()

            writer.writerow(student)

        show_message(
            "Student information saved successfully!",
            "green",
            temporary=True
        )

    except OSError as error:
        show_message(f"Error saving file: {error}", "red")


# -------------------------------
# Helper 6: Clear form
# -------------------------------
def clear_form():
    for entry in fields.values():
        entry.delete(0, tk.END)

    show_message("Form cleared.", "blue")
    fields["Name"].focus_set()


# -------------------------------
# Event handler: FocusOut
# -------------------------------
def focus_out(event):
    field_name = event.widget.field_name
    validate_field(field_name)


# -------------------------------
# Event handler: Enter
# -------------------------------
def enter_pressed(event):
    current_widget = window.focus_get()

    field_names = list(fields.keys())
    current_index = field_names.index(current_widget.field_name)

    # Move to the next field
    if current_index < len(field_names) - 1:
        next_field = fields[field_names[current_index + 1]]
        next_field.focus_set()

    # Submit on the last field
    else:
        save_student()

    return "break"


# -------------------------------
# Event handler: Ctrl + S
# -------------------------------
def save_shortcut(event):
    save_student()
    return "break"


# -------------------------------
# Event handler: Escape
# -------------------------------
def escape_pressed(event):
    clear_form()
    return "break"


# -------------------------------
# Window close handler
# -------------------------------
def close_window():
    answer = messagebox.askyesno(
        "Exit Application",
        "Are you sure you want to close the student form?"
    )

    if answer:
        window.destroy()


# -------------------------------
# GUI Design
# -------------------------------

title = tk.Label(
    window,
    text="Student Registration Form",
    font=("Arial", 18, "bold")
)
title.pack(pady=20)


# Create labels and entry widgets
field_names = ["Name", "Student ID", "Email", "Course"]

for field_name in field_names:

    label = tk.Label(
        window,
        text=field_name + ":",
        font=("Arial", 11)
    )
    label.pack()

    entry = tk.Entry(
        window,
        font=("Arial", 11),
        width=35
    )
    entry.pack(pady=5)

    # Store the Entry widget
    fields[field_name] = entry

    # Store the field name in the widget
    entry.field_name = field_name

    # Bind FocusOut event
    entry.bind("<FocusOut>", focus_out)

    # Bind Enter event
    entry.bind("<Return>", enter_pressed)


# Save button
save_button = tk.Button(
    window,
    text="Save Student",
    font=("Arial", 11, "bold"),
    width=15,
    command=save_student
)
save_button.pack(pady=15)


# Status label
status_label = tk.Label(
    window,
    text="Enter student information.",
    font=("Arial", 10)
)
status_label.pack(pady=5)


# Keyboard shortcuts
window.bind("<Control-s>", save_shortcut)
window.bind("<Control-S>", save_shortcut)
window.bind("<Escape>", escape_pressed)


# Handle window close button
window.protocol("WM_DELETE_WINDOW", close_window)


# Initial keyboard focus
fields["Name"].focus_set()


# Start application
window.mainloop()
