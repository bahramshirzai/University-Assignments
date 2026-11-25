
import tkinter as tk
from tkinter import ttk


# ==========================================
# 1. MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title("Dynamic Preferences")
root.geometry("550x500")
root.resizable(False, False)


# ==========================================
# 2. CONTROL VARIABLES
# ==========================================

# Notifications enabled or disabled
notifications_var = tk.BooleanVar(value=False)

# Notification frequency
frequency_var = tk.StringVar(value="Daily")

# Notification volume
volume_var = tk.IntVar(value=50)


# ==========================================
# 3. UPDATE WIDGET STATES
# ==========================================

def update_notification_controls():

    if notifications_var.get():

        # Enable the controls
        frequency_combo.config(state="readonly")
        volume_scale.config(state="normal")

    else:

        # Disable the controls
        frequency_combo.config(state="disabled")
        volume_scale.config(state="disabled")

    # Update status after changing states
    update_status()


# ==========================================
# 4. UPDATE STATUS AREA
# ==========================================

def update_status():

    if notifications_var.get():

        notification_status = "Enabled"
        frequency = frequency_var.get()
        volume = volume_var.get()

    else:

        notification_status = "Disabled"
        frequency = "Not available"
        volume = "Not available"

    status = f"""
CURRENT PREFERENCES
----------------------------

Notifications: {notification_status}

Frequency: {frequency}

Volume: {volume}
"""

    status_label.config(text=status)


# ==========================================
# 5. RESET FUNCTION
# ==========================================

def reset_preferences():

    # Restore default values
    notifications_var.set(False)
    frequency_var.set("Daily")
    volume_var.set(50)

    # Restore default widget states
    update_notification_controls()


# ==========================================
# 6. MAIN TITLE
# ==========================================

title_label = ttk.Label(
    root,
    text="Dynamic Notification Preferences",
    font=("Arial", 17, "bold")
)

title_label.pack(pady=20)


# ==========================================
# 7. NOTIFICATION SETTINGS FRAME
# ==========================================

settings_frame = ttk.LabelFrame(
    root,
    text="Notification Settings",
    padding=20
)

settings_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


# Enable Notifications Checkbutton
notification_check = ttk.Checkbutton(
    settings_frame,
    text="Enable Notifications",
    variable=notifications_var,
    command=update_notification_controls
)

notification_check.pack(anchor="w", pady=10)


# ==========================================
# 8. FREQUENCY COMBOBOX
# ==========================================

ttk.Label(
    settings_frame,
    text="Notification Frequency:"
).pack(anchor="w", pady=5)


frequency_combo = ttk.Combobox(
    settings_frame,
    textvariable=frequency_var,
    values=[
        "Immediately",
        "Daily",
        "Weekly",
        "Monthly"
    ],
    state="disabled"
)

frequency_combo.pack(fill="x", pady=5)

# Update status when frequency changes
frequency_combo.bind(
    "<<ComboboxSelected>>",
    lambda event: update_status()
)


# ==========================================
# 9. VOLUME SCALE
# ==========================================

ttk.Label(
    settings_frame,
    text="Notification Volume:"
).pack(anchor="w", pady=10)


volume_scale = tk.Scale(
    settings_frame,
    from_=0,
    to=100,
    orient="horizontal",
    variable=volume_var,
    state="disabled",
    command=lambda value: update_status()
)

volume_scale.pack(fill="x")


# ==========================================
# 10. ACTION BUTTONS
# ==========================================

button_frame = ttk.Frame(root)

button_frame.pack(pady=15)


reset_button = ttk.Button(
    button_frame,
    text="Reset",
    command=reset_preferences
)

reset_button.pack(side="left", padx=10)


exit_button = ttk.Button(
    button_frame,
    text="Exit",
    command=root.destroy
)

exit_button.pack(side="left", padx=10)


# ==========================================
# 11. STATUS AREA
# ==========================================

status_frame = ttk.LabelFrame(
    root,
    text="Current Configuration",
    padding=15
)

status_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)


status_label = ttk.Label(
    status_frame,
    text="",
    font=("Arial", 11),
    justify="left"
)

status_label.pack(anchor="w")


# ==========================================
# 12. INITIAL CONFIGURATION
# ==========================================

update_notification_controls()


# ==========================================
# 13. RUN APPLICATION
# ==========================================

root.mainloop()
