import pyttsx3
import os
import json


if __name__ == "__main__":
    '''while True:
        c = str(input("word :"))
        if c.lower() == "e":
            break
        speak(c)
        
'''
SOFTWARE_FILE = "../software.json"

def speak(text):
    """Speak the provided text using pyttsx3."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def load_software():

        with open(SOFTWARE_FILE, "r") as file:
            software = json.load(file)
        print("Loaded software data:", software)  # Debugging line
        return software


def get_software():
    software = load_software()
    if not software:
        return None, None

    software_names = list(software.keys())
    software_paths = list(software.values())

    return software_names, software_paths

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

def open_software(path):
    """Open the software at the specified path."""
    try:
        os.startfile(path)  # Windows specific
        print(f"Opening software at {path}")
    except Exception as e:
        print(f"Failed to open software: {e}")

SOFTWARE_FILE = "../software.json"

software_name = "brave"
path = find_software_path(software_name)
if path:
    open_software(path)
else:
    print(f"{software_name} not found")
