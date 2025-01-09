import json
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Importing PIL for image handling

# JSON file path
json_file = "settings.json"
INFO_USER = "software.json"

# Create the main window
root = Tk()
root.geometry("850x550")
root.title("Settings")
root.resizable(False, False)
root.configure(bg='lightblue')

# Variables for assistant name and auto start (moved here before load_settings)
assistant_name_var = StringVar()
auto_start_var = IntVar()  # Use IntVar for the checkbox to store 1 or 0

# Function to load settings from JSON
def load_settings():
    try:
        with open(json_file, "r") as file:
            data = json.load(file)
            # Load assistant name or use "assistant" as default
            assistant_name_var.set(data.get("assistant_name", "assistant"))
            # Load auto start value: 1 for checked, 0 for unchecked
            auto_start_var.set(1 if data.get("auto_start", 0) == 1 else 0)
    except FileNotFoundError:
        # If the file doesn't exist, use default values
        assistant_name_var.set("Kartik")
        auto_start_var.set(0)  # Default checkbox to unchecked
    except json.JSONDecodeError:
        # Handle JSON file corruption
        messagebox.showerror("Error", "Error reading settings file. Using default settings.")
        assistant_name_var.set("Kartik")
        auto_start_var.set(0)  # Default checkbox to unchecked

# Function to save settings to JSON
def save_settings_to_json():
    # Save assistant name and auto start value (1 for checked, 0 for unchecked)
    data = {
        "assistant_name": assistant_name_var.get(),
        "auto_start": 1 if auto_start_var.get() == 1 else 0
    }
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)
    print("Settings saved to JSON")
    root.destroy()

# Function to update the assistant name
def update_assistant_name():
    current_name = assistant_name_var.get()
    # Prevent storing the hint text
    if current_name.strip() == "" or current_name == "Enter new name":
        messagebox.showerror("Error", "Assistant name cannot be blank!")
    else:
        assistant_name_label.config(text=f"Current Assistant Name: {current_name}")
        # Hide the entry and update button after successful update
        entry_label.pack_forget()
        entry.pack_forget()
        update_button.pack_forget()
        # Show toast message
        show_toast("Name updated successfully!")
        # Save the updated name to JSON
        save_settings_to_json()

# Function to show the toast message
def show_toast(message):
    toast = Label(root, text=message, bg="black", fg="white", padx=10, pady=5)
    toast.place(relx=0.5, rely=0.5, anchor="center")
    root.after(2000, toast.destroy)  # Toast will disappear after 2 seconds

# Function to get assistant info
def get_assistant_info():
    load_settings()  # Load settings from JSON
    assistant_name = assistant_name_var.get()
    auto_start = auto_start_var.get()
    return assistant_name, auto_start

# Load assistant info and check name
name, auto_start_value = get_assistant_info()

# Display a message box if the assistant name is "assistant"
if name == "assistant":
    # show_toast("Plz enter your assistant name for use ")
    messagebox.showerror("waring","Plz enter your assistant name for use")

# Function to show the entry field for updating assistant name
def show_entry_field():
    entry_label.pack(pady=5)
    entry.pack(pady=5)
    update_button.pack(pady=5)
    assistant_name_var.set("Enter new name")  # Set hint text

# Function to clear the hint when the user starts typing
def on_entry_click(event):
    if assistant_name_var.get() == "Enter new name":
        entry.delete(0, "end")  # Remove the hint when clicked

# Current assistant name label
assistant_name_label = Label(root, text=f"Current Assistant Name: {assistant_name_var.get()}", font=("Arial", 12), bg='lightblue')
assistant_name_label.pack(pady=5)

# Label and entry field to update assistant name (initially hidden)
entry_label = Label(root, text="Update Assistant Name:", font=("Arial", 12), bg='lightblue')
entry = Entry(root, textvariable=assistant_name_var, font=("Arial", 12), bg='white')
entry.insert(0, "Enter new name")  # Add a hint
entry.bind("<FocusIn>", on_entry_click)  # Bind to remove hint on click

update_button = Button(root, text="Update Name", command=update_assistant_name, font=("Arial", 12), bg='lightgreen')

# Button to change name (shows the entry field)
change_name_button = Button(root, text="Change Name", command=show_entry_field, font=("Arial", 12), bg='lightyellow')
change_name_button.pack(pady=5)

# Checkbox for auto app startup
auto_start_checkbox = Checkbutton(root, text="Auto App Startup", variable=auto_start_var, font=("Arial", 12), bg='lightblue', command=save_settings_to_json)
auto_start_checkbox.pack(pady=5)

# Save Settings button (if needed)
save_settings_button = Button(root, text="Save Settings", command=save_settings_to_json, font=("Arial", 12), bg='lightcoral')
save_settings_button.pack(pady=10)

# Load an image and display it at the bottom
try:
    img = Image.open("working/test.png")
    img = img.resize((800, 250), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)

    img_label = Label(root, image=img_tk, bg='lightblue')
    img_label.pack(side=BOTTOM, padx=0, pady=0)
except Exception as e:
    print(f"Error loading image: {e}")

root.mainloop()
