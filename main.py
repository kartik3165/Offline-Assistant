from tkinter import *
from tkinter import messagebox  # Import messagebox for alerts
import subprocess
import webbrowser
import speech_recognition as sr
import pyttsx3
import os
import json
import threading

# Initialize global variables
command_thread = None
is_listening = False  # Flag to control the thread

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

SONGS_FILE = "songs.json"
SOFTWARE_FILE = "software.json"

def load_assistant_settings():
    with open("settings.json", "r") as file:
        return json.load(file)

def get_assistant_info():
    settings = load_assistant_settings()
    if not settings:
        return None, None
    assistant_name = settings.get("assistant_name", "Unknown Assistant")
    auto_start = settings.get("auto_start", 0)
    return assistant_name, auto_start

name, auto_start_value = get_assistant_info()

if name == "assistant":
    subprocess.Popen(['python', 'gui_setting.py'])

def load_songs():
    try:
        with open(SONGS_FILE, "r") as file:
            songs = json.load(file)
        return songs
    except FileNotFoundError:
        print("The file was not found.")
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return {}

def get_songs():
    songs = load_songs()
    if not songs:
        return None, None
    song_names = list(songs.keys())
    song_links = list(songs.values())
    return song_names, song_links

def load_software():
    try:
        with open(SOFTWARE_FILE, "r") as file:
            software = json.load(file)
        return software
    except FileNotFoundError:
        print("The file was not found.")
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return {}

def get_software():
    software = load_software()
    if not software:
        return None, None
    software_names = list(software.keys())
    software_paths = list(software.values())
    return software_names, software_paths

def find_song_link(song_name):
    song_names, song_links = get_songs()
    if song_names is None:
        return None
    for name, link in zip(song_names, song_links):
        if song_name.lower() in name.lower():
            return link
    return None

def find_software_path(software_name):
    software = load_software()
    for name, path in software.items():
        if software_name.lower() in name.lower():
            return path
    return None

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(command):
    if "f{name}" not in command.lower():
        return  # Ignore commands that don't start with name}
    command = command.lower().replace("f{name}", "").strip()

    if command == "":
        speak("Yes? What can I do for you?")
        command = listen_for_command()

    if "open website" in command:
        site_name = command.removeprefix("open website").strip()
        webbrowser.open(f"https://{site_name}.com")
        speak(f"Opening {site_name}")

    elif "play" in command:
        s_name = command.removeprefix("play ").strip()
        link = find_song_link(s_name)
        if link:
            speak(f"Playing {s_name}")
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {s_name}.")

    elif "open software " in command:
        software_name = command.removeprefix("open software ").strip()
        path = find_software_path(software_name)
        if path:
            speak(f"Opening {software_name}")
            os.startfile(path)
        else:
            speak(f"Sorry, I couldn't find the software {software_name}.")
    else:
        speak("Sorry, I don't know that command.")

def listen_for_command():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for command...")
        try:
            audio = recognizer.listen(source, timeout=7, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.WaitTimeoutError:
            print("No command received within the time limit.")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand you.")
        except sr.RequestError as e:
            print(f"Network error: {e}")
        return None

def show_toast(message):
    toast = Label(root, text=message, bg="black", fg="white", padx=10, pady=5)
    toast.place(relx=0.5, rely=0.5, anchor="center")
    root.after(2000, toast.destroy)

def on_button_click(event):
    global command_thread, is_listening
    if not is_listening:
        is_listening = True
        command_thread = threading.Thread(target=listen_for_commands)
        command_thread.start()
        canvas.itemconfig(oval_id, fill="red")
        canvas.itemconfig(text_id, text="Stop")
    else:
        is_listening = False  # Set the flag to False
        command_thread.join()  # Wait for the thread to finish
        canvas.itemconfig(oval_id, fill="green")
        canvas.itemconfig(text_id, text="StartUp")

def listen_for_commands():
    while is_listening:
        command = listen_for_command()
        if command and "f{name}"in command:
            processCommand(command)

# Menu actions
def update_action():
    webbrowser.open("https://kanbs.blogspot.com/2024/10/offline-personal-assistant-software.html")

def developer_action():
    subprocess.Popen(['python', 'gui_devloper.py'])

def about_action():
    messagebox.showinfo("About Us", "This is a Tkinter application created for testing.")

def settings_action():
    global command_thread, is_listening
    is_listening = False  # Set the flag to False
    command_thread.join()  # Wait for the thread to finish
    canvas.itemconfig(oval_id, fill="green")
    canvas.itemconfig(text_id, text="StartUp")

    subprocess.Popen(['python', 'gui_setting.py'])

# Function to toggle the dropdown menu
def toggle_menu():
    if menu_frame.winfo_ismapped():
        menu_frame.place_forget()
    else:
        menu_frame.place(relx=1.0, rely=0.1, anchor="ne")

# Hide the menu when clicking outside of it
def hide_menu(event):
    if menu_frame.winfo_ismapped() and not menu_frame.winfo_containing(event.x_root, event.y_root):
        menu_frame.place_forget()

# Add text and button to frames
def add_text_and_button(frame, label_text, button_text, button_action):
    inner_frame = Frame(frame, bg=frame.cget("bg"))
    inner_frame.pack(expand=True)
    text_label = Label(inner_frame, text=label_text, bg=inner_frame.cget("bg"), fg="black", font=("Arial", 12, "bold"))
    text_label.pack(pady=10)
    action_button = Button(inner_frame, text=button_text, command=button_action, bg="lightblue", fg="black")
    action_button.pack(pady=10)

def left_button_action():
    subprocess.Popen(['python', 'gui_addSong.py'])

def center_button_action():
    subprocess.Popen(['python', 'gui_addApp.py'])

def right_button_action():
    subprocess.Popen(['python', 'gui_workingGuide.py'])

root = Tk()
root.title("AssistMate v1.0")
root.geometry("850x550")
root.resizable(False, False)
root.configure(bg="#f5f5f5")

# Create top and bottom frames
frame_top = Frame(root, bg="#87CEEB")
frame_bottom = Frame(root, bg="#F0E68C")

frame_top.pack(fill="both", expand=True, side=TOP)
frame_bottom.pack(fill="both", expand=True, side=TOP)

# Set weights to create the 4:6 ratio
root.grid_rowconfigure(0, weight=3)
root.grid_rowconfigure(1, weight=7)

# Create three frames inside the bottom frame
frame_left = Frame(frame_bottom, bg="#FF6347")
frame_center = Frame(frame_bottom, bg="#FFD700")
frame_right = Frame(frame_bottom, bg="#20B2AA")

frame_left.pack(side="left", fill="both", expand=True)
frame_center.pack(side="left", fill="both", expand=True)
frame_right.pack(side="left", fill="both", expand=True)

# Add text label and button to each frame with unique functionality
add_text_and_button(frame_left, "Add your song", "ADD NOW", left_button_action)
add_text_and_button(frame_center, "Add your Apps", "ADD NOW", center_button_action)
add_text_and_button(frame_right, "How it's work", "READ IT", right_button_action)

# Create a canvas for the circular button
canvas = Canvas(frame_top, width=100, height=100, bg="#87CEEB", highlightthickness=0)

# Store oval and text object IDs for later modification
oval_id = canvas.create_oval(10, 10, 90, 90, fill="green", outline="")
text_id = canvas.create_text(50, 50, text="StartUp", fill="white", font=("Arial", 15, "bold"))
canvas.pack(expand=True)

# Bind the click event to the circle
canvas.bind("<Button-1>", on_button_click)

# Create a Menu button
menu_button = Button(frame_top, text="Menu", font=("Arial", 12, "bold"))
menu_button.place(relx=1.0, rely=0.0, anchor="ne")

# Create a dropdown menu in the tab frame
menu_frame = Frame(frame_top, bg="#87CEEB")
Label(menu_frame, text="Update", bg=menu_frame.cget("bg"), font=("Arial", 10), cursor="hand2").pack(pady=5)
Label(menu_frame, text="Developer", bg=menu_frame.cget("bg"), font=("Arial", 10), cursor="hand2").pack(pady=5)
#Label(menu_frame, text="About Us", bg=menu_frame.cget("bg"), font=("Arial", 10), cursor="hand2").pack(pady=5)
Label(menu_frame, text="Settings", bg=menu_frame.cget("bg"), font=("Arial", 10), cursor="hand2").pack(pady=5)

# Bind label click events to actions
menu_frame.children['!label'].bind("<Button-1>", lambda e: update_action())
menu_frame.children['!label2'].bind("<Button-1>", lambda e: developer_action())
#menu_frame.children['!label3'].bind("<Button-1>", lambda e: about_action())
menu_frame.children['!label3'].bind("<Button-1>", lambda e: settings_action())

# Bind the hide menu function to clicks outside the menu
root.bind("<Button-1>", hide_menu)

# Toggle menu button functionality
menu_button.config(command=toggle_menu)

root.mainloop()
