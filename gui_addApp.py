from tkinter import *
from tkinter import ttk, messagebox, filedialog
import json
import os


def load_software():
    if os.path.exists('software.json'):
        with open('software.json', 'r') as f:
            try:
                software = json.load(f)
                for software_name, software_path in software.items():
                    software_table.insert("", END, values=(software_name, software_path))
            except json.JSONDecodeError:
                show_toast("Error loading software from JSON. File might be corrupted.")


def add_software():
    software_name = software_name_entry.get()
    software_path = software_path_entry.get()

    if software_name and software_path:
        software_table.insert("", END, values=(software_name, software_path))
        save_software(software_name, software_path)
        software_name_entry.delete(0, END)
        software_path_entry.delete(0, END)
    else:
        show_toast("Please enter both software name and select a software path.")


def save_software(name, path):
    if os.path.exists('software.json'):
        with open('software.json', 'r') as f:
            software = json.load(f)
    else:
        software = {}

    software[name] = path

    with open('software.json', 'w') as f:
        json.dump(software, f, indent=4)


def delete_software(software_name):
    if os.path.exists('software.json'):
        with open('software.json', 'r') as f:
            software = json.load(f)

        if software_name in software:
            del software[software_name]

        with open('software.json', 'w') as f:
            json.dump(software, f, indent=4)


def on_delete_click(event):
    selected_item = software_table.selection()
    if selected_item:
        item_values = software_table.item(selected_item, "values")
        software_name = item_values[0]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{software_name}'?")
        if confirm:
            delete_software(software_name)
            software_table.delete(selected_item)


def show_toast(message):
    toast = Label(root, text=message, bg="black", fg="white", padx=10, pady=5)
    toast.place(relx=0.5, rely=0.5, anchor="center")
    root.after(2000, toast.destroy)


def delete_button_click(event):
    item = software_table.identify_row(event.y)
    if item:
        item_values = software_table.item(item, "values")
        software_name = item_values[0]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{software_name}'?")
        if confirm:
            delete_software(software_name)
            software_table.delete(item)


def search_software(event):
    search_query = search_entry.get().lower()
    for item in software_table.get_children():
        software_table.delete(item)

    if os.path.exists('software.json'):
        with open('software.json', 'r') as f:
            try:
                software = json.load(f)
                for software_name, software_path in software.items():
                    if search_query in software_name.lower():
                        software_table.insert("", END, values=(software_name, software_path))
            except json.JSONDecodeError:
                show_toast("Error loading software from JSON. File might be corrupted.")


def select_file():
    file_path = filedialog.askopenfilename(title="Select Software")
    if file_path:
        software_path_entry.delete(0, END)
        software_path_entry.insert(0, file_path)
        show_toast("Software path selected!")  # Show toast after selecting the file


def on_home_click():
    show_toast("Home clicked!")  # Show toast for Home button click


# Set up the main window
root = Tk()
root.geometry("850x600")
root.resizable(False, False)

frame_top = Frame(root, bg="lightblue")
frame_bottom = Frame(root, bg="lightgreen")

frame_top.pack(fill="x", expand=False)
frame_bottom.pack(fill="both", expand=True)

# Add title label in the top frame
title_label = Label(frame_top, text="Software List", font=("Arial", 24), bg="lightblue")
title_label.pack(pady=10)

# Create a Home tab button
# home_button = Button(frame_top, text="Home", command=on_home_click)
# home_button.pack(side=LEFT, padx=(10, 0), anchor=NW)

# Create a search bar
search_frame = Frame(frame_top, bg="lightblue")
search_frame.pack(pady=10)

search_label = Label(search_frame, text="Search Software:", bg="lightblue")
search_label.pack(side=LEFT)

search_entry = Entry(search_frame, width=30)
search_entry.pack(side=LEFT, padx=5)

search_entry.bind("<KeyRelease>", search_software)

# Create a Treeview to display software in a table format
columns = ("Software Name", "Software Path")
software_table = ttk.Treeview(frame_bottom, columns=columns, show='headings', height=15)
software_table.heading("Software Name", text="Software Name")
software_table.heading("Software Path", text="Software Path")
software_table.pack(fill=BOTH, expand=True, padx=20, pady=10)

# Bind the double click event to delete button click
software_table.bind("<Double-1>", delete_button_click)

# Create entry fields and button to add a new software
add_software_frame = Frame(frame_bottom, bg="lightgreen")
add_software_frame.pack(pady=10)

# Configure grid weights for full-width entry fields
add_software_frame.grid_columnconfigure(0, weight=1)  # For Software Name
add_software_frame.grid_columnconfigure(1, weight=1)  # For Software Path
add_software_frame.grid_columnconfigure(2, weight=0)  # For Browse button

software_name_label = Label(add_software_frame, text="Software Name:", bg="lightgreen")
software_name_label.grid(row=0, column=0, padx=5, sticky=W)

software_name_entry = Entry(add_software_frame, width=30)
software_name_entry.grid(row=0, column=1, padx=5, sticky="ew")  # Full width

# Browse button for software name
# browse_button = Button(add_software_frame, text="Browse", command=select_file)
# browse_button.grid(row=0, column=2, padx=5)

software_path_label = Label(add_software_frame, text="Software Path:", bg="lightgreen")
software_path_label.grid(row=1, column=0, padx=5, sticky=W)

software_path_entry = Entry(add_software_frame, width=30)
software_path_entry.grid(row=1, column=1, padx=5, sticky="ew")  # Full width

# Button to open file picker for software path
select_button = Button(add_software_frame, text="Browse", command=select_file)
select_button.grid(row=1, column=2, padx=5)

add_software_button = Button(add_software_frame, text="Add Software", command=add_software)
add_software_button.grid(row=2, columnspan=3, pady=10)

load_software()  # Load software from the JSON file when the app starts

root.mainloop()
