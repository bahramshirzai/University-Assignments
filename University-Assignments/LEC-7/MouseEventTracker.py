
import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Mouse Event Tracker")
window.geometry("600x450")

# Variables to store information
double_click_count = 0

# Create a title label
title_label = tk.Label(
    window,
    text="Mouse Event Tracker",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=10)

# Display mouse coordinates
coordinate_label = tk.Label(
    window,
    text="Mouse Coordinates: X = 0, Y = 0",
    font=("Arial", 12)
)
coordinate_label.pack(pady=5)

# Display mouse actions
action_label = tk.Label(
    window,
    text="Mouse Action: None",
    font=("Arial", 12)
)
action_label.pack(pady=5)

# Display double-click count
count_label = tk.Label(
    window,
    text="Double Clicks: 0",
    font=("Arial", 12)
)
count_label.pack(pady=5)

# Display status
status_label = tk.Label(
    window,
    text="Status: Outside the frame",
    font=("Arial", 12),
    fg="blue"
)
status_label.pack(pady=5)

# Create a large frame
mouse_frame = tk.Frame(
    window,
    width=500,
    height=250,
    bg="lightblue",
    relief="solid",
    borderwidth=2
)
mouse_frame.pack(pady=15)

# Prevent the frame from shrinking
mouse_frame.pack_propagate(False)


# Function for mouse movement
def mouse_motion(event):
    coordinate_label.config(
        text=f"Mouse Coordinates: X = {event.x}, Y = {event.y}"
    )


# Function for left click
def left_click(event):
    action_label.config(text="Mouse Action: Left Click")


# Function for double click
def double_click(event):
    global double_click_count

    double_click_count += 1

    count_label.config(
        text=f"Double Clicks: {double_click_count}"
    )

    action_label.config(text="Mouse Action: Double Click")


# Function when mouse enters the frame
def mouse_enter(event):
    status_label.config(
        text="Status: Mouse is inside the frame",
        fg="green"
    )


# Function when mouse leaves the frame
def mouse_leave(event):
    status_label.config(
        text="Status: Mouse is outside the frame",
        fg="red"
    )


# Bind mouse events to the frame
mouse_frame.bind("<Motion>", mouse_motion)
mouse_frame.bind("<Button-1>", left_click)
mouse_frame.bind("<Double-Button-1>", double_click)
mouse_frame.bind("<Enter>", mouse_enter)
mouse_frame.bind("<Leave>", mouse_leave)


# Run the application
window.mainloop()
