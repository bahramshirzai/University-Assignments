
import tkinter as tk


# Create the main window
window = tk.Tk()
window.title("Event-Driven Login Form")
window.geometry("450x350")
window.resizable(False, False)


# -------------------------------
# Helper function: Validate input
# -------------------------------
def validate_login(username, password):
    if username == "" and password == "":
        return False, "Please enter username and password."

    if username == "":
        return False, "Username is required."

    if password == "":
        return False, "Password is required."

    if username == "admin" and password == "12345":
        return True, "Login successful!"

    return False, "Invalid username or password."


# -------------------------------
# Helper function: Clear form
# -------------------------------
def clear_form(event=None):
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    status_label.config(
        text="Form cleared.",
        fg="blue"
    )

    username_entry.focus_set()


# -------------------------------
# Login handler
# -------------------------------
def login(event=None):
    username = username_entry.get()
    password = password_entry.get()

    success, message = validate_login(username, password)

    if success:
        status_label.config(text=message, fg="green")
    else:
        status_label.config(text=message, fg="red")


# -------------------------------
# Focus event functions
# -------------------------------
def username_focus_in(event):
    status_label.config(
        text="Active field: Username",
        fg="blue"
    )


def password_focus_in(event):
    status_label.config(
        text="Active field: Password",
        fg="blue"
    )


def focus_out(event):
    status_label.config(
        text="Focus moved to another field.",
        fg="gray"
    )


# -------------------------------
# GUI Design
# -------------------------------

title_label = tk.Label(
    window,
    text="Login Form",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=15)


# Username
username_label = tk.Label(
    window,
    text="Username:",
    font=("Arial", 12)
)
username_label.pack()

username_entry = tk.Entry(
    window,
    font=("Arial", 12),
    width=30
)
username_entry.pack(pady=5)


# Password
password_label = tk.Label(
    window,
    text="Password:",
    font=("Arial", 12)
)
password_label.pack()

password_entry = tk.Entry(
    window,
    font=("Arial", 12),
    width=30,
    show="*"
)
password_entry.pack(pady=5)


# Login button
login_button = tk.Button(
    window,
    text="Login",
    font=("Arial", 11),
    width=12,
    command=login
)
login_button.pack(pady=10)


# Status label
status_label = tk.Label(
    window,
    text="Please enter your login details.",
    font=("Arial", 10),
    fg="blue"
)
status_label.pack(pady=10)


# -------------------------------
# Bind keyboard and focus events
# -------------------------------

# Pressing Enter calls the same login function
window.bind("<Return>", login)

# Escape clears the form
window.bind("<Escape>", clear_form)

# Focus events for username
username_entry.bind("<FocusIn>", username_focus_in)
username_entry.bind("<FocusOut>", focus_out)

# Focus events for password
password_entry.bind("<FocusIn>", password_focus_in)
password_entry.bind("<FocusOut>", focus_out)


# Set initial focus
username_entry.focus_set()

# Run the application
window.mainloop()
