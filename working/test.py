from tkinter import *
import subprocess
import webbrowser
import speech_recognition as sr
import pyttsx3
import os
import json
import threading

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

SONGS_FILE = "songs.json"
SOFTWARE_FILE = "software.json"

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
        print("Loaded software data:", software)  # Debugging line
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
    """Find the link for the given song name."""
    song_names, song_links = get_songs()
    if song_names is None:
        return None
    for name, link in zip(song_names, song_links):
        if song_name.lower() in name.lower():
            return link
    return None

def find_software_path(software_name):
    """Find the path for the given software name."""
    software = load_software()
    for name, path in software.items():
        print(f"Checking software: {name}")  # Debugging line
        print(f"Comparing with: {software_name}")  # Debugging line
        if software_name.lower() in name.lower():
            print(f"Found path: {path}")  # Debugging line
            return path
    return None

def speak(text):
    """Speak the provided text using pyttsx3."""
    engine.say(text)
    engine.runAndWait()

def processCommand(command):
    """Process the recognized command and perform the appropriate action."""
    if "kartik" not in command.lower():
        return  # Ignore commands that don't start with "Kartik"

    command = command.lower().replace("kartik", "").strip()  # Remove "Kartik" and process the rest

    if command == "":  # If only "Kartik" was spoken
        speak("Yes? What can I do for you?")
        command = listen_for_command()  # Listen again for the actual command

    if "open website" in command:
        # Extract the website name and open it
        site_name = command.removeprefix("open website").strip()
        webbrowser.open(f"https://{site_name}.com")
        speak(f"Opening {site_name}")

    elif "play" in command:
        # Extract the song name and find the link
        s_name = command.removeprefix("play ").strip()
        link = find_song_link(s_name)
        if link:
            speak(f"Playing {s_name}")
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {s_name}.")

    elif "open software " in command:
        # Extract the software name and find the path
        software_name = command.removeprefix("open software ").strip()
        path = find_software_path(software_name)
        if path:
            speak(f"Opening {software_name}")
            os.startfile(path)  # Use os.startfile to open the software
        else:
            speak(f"Sorry, I couldn't find the software {software_name}.")

    else:
        speak("Sorry, I don't know that command.")

def listen_for_command():
    """Listen for a command and return it as a string."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
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
    speak("Hi, I'm ready for your commands.")
    command_thread = threading.Thread(target=listen_for_commands)
    command_thread.start()

def listen_for_commands():
    while True:
        command = listen_for_command()
        if command and "kartik" in command:  # Only process if "Kartik" is in the command
            processCommand(command)

# Menu actions
def update_action():
    show_toast("Update selected!")

def developer_action():
    show_toast("Developer selected!")

def settings_action():
    subprocess.Popen(['python', 'gui_setting.py'])

# Function to toggle the dropdown menu
def toggle_menu():
    if menu_frame.winfo_ismapped():  # Check if the menu is currently displayed
        menu_frame.place_forget()  # Hide the menu
    else:
        menu_frame.place(relx=1.0, rely=0.1, anchor="ne")  # Show the menu

# Add text and button to frames
def add_text_and_button(frame, label_text, button_text, button_action):
    # Create a frame to hold the text label and button
    inner_frame = Frame(frame, bg=frame.cget("bg"))
    inner_frame.pack(expand=True)  # Center the inner frame

    # Text label
    text_label = Label(inner_frame, text=label_text, bg=inner_frame.cget("bg"), fg="white")
    text_label.pack(pady=10)  # Add some vertical padding

    # Action button with the passed action
    action_button = Button(inner_frame, text=button_text, command=button_action)
    action_button.pack(pady=10)  # Add some vertical padding

# Different actions for each button
def left_button_action():
    subprocess.Popen(['python', 'gui_addSong.py'])

def center_button_action():
    subprocess.Popen(['python', 'gui_addApp.py'])

def right_button_action():
    show_toast("Right frame button clicked!")

root = Tk()
root.geometry("850x550")
root.resizable(False, False)

# Create top and bottom frames
frame_top = Frame(root, bg="lightblue")
frame_bottom = Frame(root, bg="lightgreen")

frame_top.pack(fill="both", expand=True, side=TOP)
frame_bottom.pack(fill="both", expand=True, side=TOP)

# Set weights to create the 4:6 ratio
root.grid_rowconfigure(0, weight=3)  # Top frame weight
root.grid_rowconfigure(1, weight=7)  # Bottom frame weight

# Create three frames inside the bottom frame
frame_left = Frame(frame_bottom, bg="red")
frame_center = Frame(frame_bottom, bg="yellow")
frame_right = Frame(frame_bottom, bg="blue")

frame_left.pack(side="left", fill="both", expand=True)
frame_center.pack(side="left", fill="both", expand=True)
frame_right.pack(side="left", fill="both", expand=True)

# Add text label and button to each frame with unique functionality
add_text_and_button(frame_left, "Add you favourite song", "ADD NOW", left_button_action)
add_text_and_button(frame_center, "Add your favourite software", "ADD NOW", center_button_action)
add_text_and_button(frame_right, "Right Frame", "Right Button", right_button_action)

# Create a canvas for the circular button
canvas = Canvas(frame_top, width=100, height=100, bg="lightblue", highlightthickness=0)
canvas.create_oval(10, 10, 90, 90, fill="blue", outline="")
canvas.create_text(50, 50, text="Click Me", fill="white", font=("Arial", 10, "bold"))

canvas.pack(expand=True)

# Bind the click event to the circle
canvas.bind("<Button-1>", on_button_click)

# Create a frame for the tab in the top right corner
tab_frame = Frame(frame_top, bg="lightgrey", padx=10, pady=5)
tab_button = Button(tab_frame, text="Menu", command=toggle_menu)
tab_button.pack()

# Pack the tab frame to the top right
tab_frame.place(relx=1.0, rely=0.0, anchor="ne")

# Create a dropdown menu frame
menu_frame = Frame(frame_top, bg="white", bd=1, relief="raised")
menu_frame.place(relx=1.0, rely=0.1, anchor="ne")  # Initially hidden

# Add buttons for the menu options with their respective actions
update_button = Button(menu_frame, text="Update", command=update_action, bg="white")
update_button.pack(fill='x')  # Fill the button to occupy the full width

developer_button = Button(menu_frame, text="Developer", command=developer_action, bg="white")
developer_button.pack(fill='x')

settings_button = Button(menu_frame, text="Settings", command=settings_action, bg="white")
settings_button.pack(fill='x')

root.mainloop()


