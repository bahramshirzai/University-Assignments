
import tkinter as tk
from tkinter import ttk, messagebox


# =====================================
# 1. MAIN WINDOW
# =====================================

root = tk.Tk()
root.title("Settings Panel")
root.geometry("550x650")
root.resizable(False, False)


# =====================================
# 2. VARIABLES
# =====================================

# Notification Checkbuttons
email_var = tk.BooleanVar(value=True)
sms_var = tk.BooleanVar(value=False)
desktop_var = tk.BooleanVar(value=True)

# Theme Radiobuttons
theme_var = tk.StringVar(value="System")

# Notification volume
volume_var = tk.IntVar(value=50)

# Language Combobox
language_var = tk.StringVar(value="English")


# =====================================
# 3. SAVE SETTINGS FUNCTION
# =====================================

def save_settings():

    email = email_var.get()
    sms = sms_var.get()
    desktop = desktop_var.get()

    theme = theme_var.get()
    volume = volume_var.get()
    language = language_var.get()

    summary = f"""
========== SAVED SETTINGS ==========

NOTIFICATIONS:

Email Notifications: {"Enabled" if email else "Disabled"}

SMS Notifications: {"Enabled" if sms else "Disabled"}

Desktop Notifications: {"Enabled" if desktop else "Disabled"}


THEME:

Selected Theme: {theme}


NOTIFICATION VOLUME:

Volume: {volume}%


LANGUAGE:

Selected Language: {language}

====================================
"""

    summary_label.config(text=summary)

    messagebox.showinfo(
        "Settings Saved",
        "Your settings have been saved successfully!"
    )


# =====================================
# 4. RESET SETTINGS FUNCTION
# =====================================

def reset_settings():

    # Reset Checkbuttons
    email_var.set(True)
    sms_var.set(False)
    desktop_var.set(True)

    # Reset Theme
    theme_var.set("System")

    # Reset Volume
    volume_var.set(50)

    # Reset Language
    language_var.set("English")

    # Clear Summary
    summary_label.config(
        text="Your settings will appear here."
    )

    messagebox.showinfo(
        "Reset",
        "Settings have been reset to default values!"
    )


# =====================================
# 5. WINDOW TITLE
# =====================================

title_label = tk.Label(
    root,
    text="APPLICATION SETTINGS",
    font=("Arial", 20, "bold"),
    fg="#1F4E79"
)

title_label.pack(pady=15)


# =====================================
# 6. NOTIFICATION CHECKBUTTONS
# =====================================

notification_frame = tk.LabelFrame(
    root,
    text="Notification Preferences",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10
)

notification_frame.pack(
    fill="x",
    padx=25,
    pady=10
)


tk.Checkbutton(
    notification_frame,
    text="Email Notifications",
    variable=email_var
).pack(anchor="w", pady=3)


tk.Checkbutton(
    notification_frame,
    text="SMS Notifications",
    variable=sms_var
).pack(anchor="w", pady=3)


tk.Checkbutton(
    notification_frame,
    text="Desktop Notifications",
    variable=desktop_var
).pack(anchor="w", pady=3)


# =====================================
# 7. THEME RADIOBUTTONS
# =====================================

theme_frame = tk.LabelFrame(
    root,
    text="Application Theme",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10
)

theme_frame.pack(
    fill="x",
    padx=25,
    pady=10
)


tk.Radiobutton(
    theme_frame,
    text="Light",
    variable=theme_var,
    value="Light"
).pack(side="left", padx=15)


tk.Radiobutton(
    theme_frame,
    text="Dark",
    variable=theme_var,
    value="Dark"
).pack(side="left", padx=15)


tk.Radiobutton(
    theme_frame,
    text="System",
    variable=theme_var,
    value="System"
).pack(side="left", padx=15)


# =====================================
# 8. NOTIFICATION VOLUME SCALE
# =====================================

volume_frame = tk.LabelFrame(
    root,
    text="Notification Volume",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10
)

volume_frame.pack(
    fill="x",
    padx=25,
    pady=10
)


volume_scale = tk.Scale(
    volume_frame,
    from_=0,
    to=100,
    orient="horizontal",
    variable=volume_var,
    label="Volume Level (%)",
    length=400
)

volume_scale.pack()


# =====================================
# 9. LANGUAGE COMBOBOX
# =====================================

language_frame = tk.LabelFrame(
    root,
    text="Language Settings",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10
)

language_frame.pack(
    fill="x",
    padx=25,
    pady=10
)


tk.Label(
    language_frame,
    text="Select Language:"
).pack(side="left", padx=10)


language_combo = ttk.Combobox(
    language_frame,
    textvariable=language_var,
    values=["English", "Dari", "Pashto", "French", "Arabic"],
    state="readonly",
    width=20
)

language_combo.pack(side="left", padx=10)


# =====================================
# 10. SAVE AND RESET BUTTONS
# =====================================

button_frame = tk.Frame(root)

button_frame.pack(pady=15)


tk.Button(
    button_frame,
    text="Save Settings",
    bg="#198754",
    fg="white",
    width=18,
    command=save_settings
).pack(side="left", padx=10)


tk.Button(
    button_frame,
    text="Reset Settings",
    bg="#DC3545",
    fg="white",
    width=18,
    command=reset_settings
).pack(side="left", padx=10)


# =====================================
# 11. SUMMARY LABEL
# =====================================

summary_frame = tk.LabelFrame(
    root,
    text="Settings Summary",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=10
)

summary_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=10
)


summary_label = tk.Label(
    summary_frame,
    text="Your settings will appear here.",
    font=("Arial", 10),
    justify="left",
    anchor="nw"
)

summary_label.pack(
    fill="both",
    expand=True
)


# =====================================
# 12. RUN APPLICATION
# =====================================

root.mainloop()
