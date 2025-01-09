import webbrowser
import speech_recognition as sr
import pyttsx3
from working.HipHopSong import m
from open_software import search_software, find_executables, find_installed_software_paths, open_software, get_best_match, \
    scan_user_directories, get_known_software_from_registry

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()


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

    if "open " in command:
        # Extract the software name
        software_name = command.removeprefix("open ").strip()

        try:
            # Get available executables and known software
            user_executables = scan_user_directories()
            known_software = get_known_software_from_registry()

            # Search for the software in the installed applications
            matching_installed_software = search_software(software_name, known_software)
            if len(matching_installed_software) == 1:
                # Automatically open the only available installed software
                to_open = matching_installed_software[0]
                print(f"Automatically opening the installed software: {to_open}")
                installed_paths = find_installed_software_paths(to_open, known_software)
                if installed_paths:
                    for path in installed_paths:
                        if os.path.exists(path):
                            open_software(path)
                            return
                else:
                    speak("No valid executable found in the installed software paths.")
                    # Proceed to search user directories if not found in installed software

            # Handle user-installed .exe files or search for a best match
            matched_user_executables = find_executables(software_name, user_executables)
            best_match = get_best_match(software_name, matched_user_executables)

            if best_match:
                open_software(best_match)
            else:
                # If not found, open in the browser
                webbrowser.open(f"https://www.google.com/search?q={software_name}")
                speak(f"Opening search results for {software_name} in your browser.")
        except Exception as e:
            speak(f"An error occurred: {e}")
            print(f"Error processing command '{command}': {e}")

    elif "play random hip-hop song" in command or "play hip-hop song" in command:
        try:
            # Fetch and play a random hip-hop song
            song_title, song_url = m()
            speak(f"Playing {song_title}")
            webbrowser.open(song_url)
        except Exception as e:
            speak(f"An error occurred while trying to play the song: {e}")
            print(f"Error playing song: {e}")

    else:
        speak("Sorry, I don't know that command.")


def listen_for_command():
    """Listen for a command and return it as a string."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        print("Listening for command...")
        try:
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=10)
            command = recognizer.recognize_google(audio)
            print(f"Command received: {command}")  # For debugging
            return command.lower()
        except sr.WaitTimeoutError:
            print("No command received within the time limit.")
            speak("I didn't hear anything. Please try again.")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand you.")
            speak("Sorry, I didn't understand that. Please repeat.")
        except sr.RequestError as e:
            print(f"Network error: {e}")
            speak("There was a network error. Please try again later.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            speak(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    speak("Hi, I'm ready for your commands.")
    while True:
        command = listen_for_command()
        if command and "kartik" in command:  # Only process if "Kartik" is in the command
            processCommand(command)
