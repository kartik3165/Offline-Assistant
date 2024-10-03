import json
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
import os

SOFTWARE_FILE = "../software.json"

def load_software():
    """Load existing software data from the JSON file."""
    if os.path.exists(SOFTWARE_FILE):
        try:
            with open(SOFTWARE_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error decoding JSON file.")
            return {}
    return {}

def save_software(software_data):
    """Save updated software data to the JSON file."""
    try:
        with open(SOFTWARE_FILE, "w") as file:
            json.dump(software_data, file, indent=4)
        print(f"Data successfully saved to {SOFTWARE_FILE}.")
    except IOError as e:
        print(f"Error writing to JSON file: {e}")

def select_file():
    """Open a file picker dialog to select a file using PyQt5."""
    app = QApplication(sys.argv)
    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(None, "Select Software Executable", filter="Executable Files (*.exe);;All Files (*)")
    app.exit()  # Exit the application
    return file_path

def add_software():
    """Add a new software entry to the JSON file."""
    print("Loading existing software data...")
    software_data = load_software()

    software_name = input("Enter the software name: ").strip()
    print("Opening file picker dialog...")
    software_path = select_file()

    if software_name and software_path:
        software_data[software_name] = software_path
        save_software(software_data)
        print(f"Software '{software_name}' has been added with path '{software_path}'.")
    else:
        print("Software name and path cannot be empty.")

if __name__ == "__main__":
    add_software()
