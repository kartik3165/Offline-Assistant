from tkinter import *
from tkinter import ttk, messagebox
import json
import os


def load_songs():
    if os.path.exists('songs.json'):
        with open('songs.json', 'r') as f:
            try:
                songs = json.load(f)
                for song_name, song_link in songs.items():
                    song_table.insert("", END, values=(song_name, song_link))
            except json.JSONDecodeError:
                show_toast("Error loading songs from JSON. File might be corrupted.")


def add_song():
    song_name = song_name_entry.get()
    song_link = song_link_entry.get()

    if song_name and song_link:
        song_table.insert("", END, values=(song_name, song_link))
        save_song(song_name, song_link)
        song_name_entry.delete(0, END)
        song_link_entry.delete(0, END)
    else:
        show_toast("Please enter both song name and song link.")


def save_song(name, link):
    if os.path.exists('songs.json'):
        with open('songs.json', 'r') as f:
            songs = json.load(f)
    else:
        songs = {}

    songs[name] = link

    with open('songs.json', 'w') as f:
        json.dump(songs, f, indent=4)


def delete_song(song_name):
    if os.path.exists('songs.json'):
        with open('songs.json', 'r') as f:
            songs = json.load(f)

        if song_name in songs:
            del songs[song_name]

        with open('songs.json', 'w') as f:
            json.dump(songs, f, indent=4)


def on_delete_click(event):
    selected_item = song_table.selection()
    if selected_item:
        item_values = song_table.item(selected_item, "values")
        song_name = item_values[0]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{song_name}'?")
        if confirm:
            delete_song(song_name)
            song_table.delete(selected_item)


def show_toast(message):
    toast = Label(root, text=message, bg="black", fg="white", padx=10, pady=5)
    toast.place(relx=0.5, rely=0.5, anchor="center")
    root.after(2000, toast.destroy)


def delete_button_click(event):
    item = song_table.identify_row(event.y)
    if item:
        item_values = song_table.item(item, "values")
        song_name = item_values[0]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{song_name}'?")
        if confirm:
            delete_song(song_name)
            song_table.delete(item)


def search_songs(event):
    search_query = search_entry.get().lower()
    for item in song_table.get_children():
        song_table.delete(item)

    if os.path.exists('songs.json'):
        with open('songs.json', 'r') as f:
            try:
                songs = json.load(f)
                for song_name, song_link in songs.items():
                    if search_query in song_name.lower():
                        song_table.insert("", END, values=(song_name, song_link))
            except json.JSONDecodeError:
                show_toast("Error loading songs from JSON. File might be corrupted.")


def on_tab_click():
    show_toast("Tab clicked!")


root = Tk()
root.geometry("850x550")
root.resizable(False, False)

frame_top = Frame(root, bg="lightblue")
frame_bottom = Frame(root, bg="lightgreen")

frame_top.pack(fill="x", expand=False)
frame_bottom.pack(fill="both", expand=True)

# Add title label in the top frame
title_label = Label(frame_top, text="Song List", font=("Arial", 24), bg="lightblue")
title_label.pack(pady=10)

# # Create a tab in the top left corner
# tab_button = Button(frame_top, text="Tab", command=on_tab_click)
# tab_button.pack(side=LEFT, padx=(10, 0),anchor = NW)

# Create a search bar
search_frame = Frame(frame_top, bg="lightblue")
search_frame.pack(pady=10)

search_label = Label(search_frame, text="Search Song:", bg="lightblue")
search_label.pack(side=LEFT)

search_entry = Entry(search_frame, width=30)
search_entry.pack(side=LEFT, padx=5)

search_entry.bind("<KeyRelease>", search_songs)

# Create a Treeview to display songs in a table format
columns = ("Song Name", "Song Link")
song_table = ttk.Treeview(frame_bottom, columns=columns, show='headings', height=15)
song_table.heading("Song Name", text="Song Name")
song_table.heading("Song Link", text="Song Link")
song_table.pack(fill=BOTH, expand=True, padx=20, pady=10)

# Bind the double click event to delete button click
song_table.bind("<Double-1>", delete_button_click)

# Create entry fields and button to add a new song
add_song_frame = Frame(frame_bottom, bg="lightgreen")
add_song_frame.pack(pady=10)

song_name_label = Label(add_song_frame, text="Song Name:", bg="lightgreen")
song_name_label.grid(row=0, column=0, padx=5, sticky=W)

song_name_entry = Entry(add_song_frame, width=30)
song_name_entry.grid(row=0, column=1, padx=5)

song_link_label = Label(add_song_frame, text="Song Link:", bg="lightgreen")
song_link_label.grid(row=1, column=0, padx=5, sticky=W)

song_link_entry = Entry(add_song_frame, width=30)
song_link_entry.grid(row=1, column=1, padx=5)

add_song_button = Button(add_song_frame, text="Add Song", command=add_song)
add_song_button.grid(row=2, columnspan=2, pady=10)

load_songs()  # Load songs from the JSON file when the app starts

root.mainloop()
