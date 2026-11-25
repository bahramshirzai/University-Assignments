
import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Keyboard Event Viewer")
window.geometry("500x350")

# Label for the last key pressed
key_label = tk.Label(
    window,
    text="Last Key Pressed: None",
    font=("Arial", 14, "bold")
)
key_label.pack(pady=15)

# Label for keysym and char
details_label = tk.Label(
    window,
    text="Keysym: None | Character: None",
    font=("Arial", 12)
)
details_label.pack(pady=10)

# Status label
status_label = tk.Label(
    window,
    text="Status: Waiting for keyboard input",
    font=("Arial", 12),
    fg="blue"
)
status_label.pack(pady=10)

# Entry widget
entry_label = tk.Label(
    window,
    text="Type something in the box below:"
)
entry_label.pack(pady=5)

entry = tk.Entry(
    window,
    font=("Arial", 14),
    width=30
)
entry.pack(pady=10)


# Function to handle key presses
def key_pressed(event):
    key_label.config(
        text=f"Last Key Pressed: {event.keysym}"
    )

    details_label.config(
        text=f"Keysym: {event.keysym} | Character: {repr(event.char)}"
    )

    status_label.config(
        text="Status: Key pressed",
        fg="blue"
    )


# Function to clear the display
def clear_display(event):
    key_label.config(text="Last Key Pressed: None")
    details_label.config(text="Keysym: None | Character: None")
    status_label.config(text="Status: Display Cleared", fg="red")


# Function for Ctrl + S
def save_status(event):
    status_label.config(
        text="Status: Saved",
        fg="green"
    )


# Bind keyboard events to the root window
window.bind("<KeyPress>", key_pressed)
window.bind("<Escape>", clear_display)
window.bind("<Control-s>", save_status)
window.bind("<Control-S>", save_status)

# Start the application
window.mainloop()
