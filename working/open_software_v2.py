import speech_recognition as sr
import subprocess
import os

# Define application mappings directly in the script
app_mappings = {
    "brave": {
        "display_name": "Brave",
        "executable_names": ["brave.exe"]
    },
    "chrome": {
        "display_name": "Chrome",
        "executable_names": ["chrome.exe"]
    },
    "firefox": {
        "display_name": "Firefox",
        "executable_names": ["firefox.exe"]
    },
    "notepad": {
        "display_name": "Notepad",
        "executable_names": ["notepad.exe"]
    }
}

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized command: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Sorry, there was an issue with the request.")
    return None

def find_executable(name, executable_names, search_paths):
    for search_path in search_paths:
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if file.lower() in (name.lower() for name in executable_names):
                    return os.path.join(root, file)
    return None

def open_application(command, app_mappings):
    # Define common and additional directories to search
    common_paths = [
        "C:\\Program Files",
        "C:\\Program Files (x86)",
        "C:\\Users\\Public\\Desktop",
        "C:\\Users\\%USERNAME%\\Desktop",
        "D:\\",  # Add other drive letters if necessary
        "E:\\",
        # Add more paths if needed
    ]

    for app_key, app_info in app_mappings.items():
        if app_info['display_name'].lower() in command:
            path = find_executable(app_key, app_info['executable_names'], common_paths)
            if path:
                subprocess.Popen(path)
                print(f"Opening {app_info['display_name']}...")
                return
            else:
                print(f"Executable not found for {app_info['display_name']} in common paths.")
                return
    print("Application not found.")

if __name__ == "__main__":
    command = recognize_speech()
    if command:
        open_application(command, app_mappings)
