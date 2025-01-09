import webbrowser
import speech_recognition as sr
import pyttsx3
import os
import json

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

SONGS_FILE = "../songs.json"
SOFTWARE_FILE = "../software.json"

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

if __name__ == "__main__":

    speak("Hi, I'm ready for your commands.")
    while True:
        command = listen_for_command()
        if command and "kartik" in command:  # Only process if "Kartik" is in the command
            processCommand(command)
