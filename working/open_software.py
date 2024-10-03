import os
import winreg
import re


# Function to get all available drives on the system
def get_all_drives():
    available_drives = []
    for drive_letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        drive = f"{drive_letter}:\\"
        if os.path.exists(drive):
            available_drives.append(drive)
    return available_drives


# Function to scan directories for .exe files in user-specific paths
def scan_user_directories():
    user_dirs = [
        os.path.join("Users", os.getlogin(), "Desktop"),
        os.path.join("Users", os.getlogin(), "Downloads"),
        os.path.join("Users", os.getlogin(), "Documents"),
        os.path.join("Users", os.getlogin(), "AppData\\Local"),
        os.path.join("Users", os.getlogin(), "AppData\\Roaming")
    ]

    external_executables = set()

    drives = get_all_drives()

    for drive in drives:
        for user_dir in user_dirs:
            search_path = os.path.join(drive, user_dir)
            if os.path.exists(search_path):
                for root, dirs, files in os.walk(search_path):
                    for file in files:
                        if file.endswith(".exe"):
                            full_path = os.path.join(root, file)
                            if not is_installer(full_path):  # Check if it's not an installer
                                external_executables.add(full_path)

    return external_executables


# Function to determine if a file is an installer (based on some common installer patterns)
def is_installer(file_path):
    installer_keywords = ["setup", "install", "installer", "config"]
    return any(keyword in file_path.lower() for keyword in installer_keywords)


# Function to retrieve a list of commonly installed software from the Windows Registry
def get_known_software_from_registry():
    known_software = set()
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for reg_path in reg_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                software_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                                install_location, _ = winreg.QueryValueEx(subkey, "InstallLocation")
                                if install_location:
                                    known_software.add((software_name, install_location))
                            except FileNotFoundError:
                                pass
                    except OSError:
                        pass
        except FileNotFoundError:
            pass

    return known_software


# Function to search for software names matching a partial name
def search_software(partial_name, software_list):
    matches = [name for name, _ in software_list if partial_name.lower() in name.lower()]
    return matches


# Function to find executable paths matching the partial name
def find_executables(partial_name, executables):
    matches = [exe for exe in executables if partial_name.lower() in os.path.basename(exe).lower()]
    return matches


# Function to find installed software paths matching the partial name
def find_installed_software_paths(partial_name, installed_software):
    matches = []
    for name, loc in installed_software:
        # Clean up path
        loc = loc.strip().strip('"')
        if os.path.exists(loc):
            try:
                for file_name in os.listdir(loc):
                    if file_name.lower().startswith(partial_name.lower()) and file_name.lower().endswith('.exe'):
                        matches.append(os.path.join(loc, file_name))
            except OSError:
                # Handle cases where loc is not a valid directory
                pass
    return matches


# Function to open the software by its path
def open_software(file_path):
    try:
        os.startfile(file_path)
        print(f"Opening: {file_path}")
    except Exception as e:
        print(f"Failed to open {file_path}: {e}")


# Function to get the best match for an executable file
def get_best_match(partial_name, executables):
    # Remove numeric suffixes and return the best match
    pattern = re.compile(rf"{re.escape(partial_name)}(?:\s*\(\d+\))?\.exe$", re.IGNORECASE)
    matches = [exe for exe in executables if pattern.search(os.path.basename(exe))]

    # If multiple matches, prioritize by exact name match
    if matches:
        matches.sort(key=lambda x: (os.path.basename(x).lower() != f"{partial_name.lower()}.exe", x))
        return matches[0]

    return None


# Function to search and open software
def search_and_open():
    user_executables = scan_user_directories()
    known_software = get_known_software_from_registry()

    while True:
        partial_name = input("Enter partial name to search for software (or type 'exit' to quit): ")
        if partial_name.lower() == 'exit':
            break

        matched_known_software = search_software(partial_name, known_software)
        matched_user_executables = find_executables(partial_name, user_executables)

        if matched_known_software:
            print("Matching installed software (from registry):")
            for software in matched_known_software:
                print(software)

        if matched_user_executables:
            print("Matching external .exe files (from directories):")
            for executable in matched_user_executables:
                print(os.path.basename(executable))

        # Handle installed software
        if len(matched_known_software) == 1:
            # Automatically open the only available installed software
            to_open = matched_known_software[0]
            print(f"Automatically opening the installed software: {to_open}")
            installed_paths = find_installed_software_paths(to_open, known_software)
            if installed_paths:
                for path in installed_paths:
                    if os.path.exists(path):
                        open_software(path)
                        break
            else:
                print("No valid executable found in the installed software paths.")

        else:
            # Prompt to open a specific software
            to_open = input(
                "Enter the exact name of the software you want to open from the list above (without .exe): ")

            # Open installed software from registry
            matching_registry_paths = find_installed_software_paths(to_open, known_software)
            if matching_registry_paths:
                for path in matching_registry_paths:
                    if os.path.exists(path):
                        open_software(path)
                        break  # Stop after opening the first match
                else:
                    print("No valid executable found in the installed software paths.")
            else:
                # Open user-installed .exe files, with a preference for exact name matches
                best_match = get_best_match(to_open, matched_user_executables)
                if best_match:
                    open_software(best_match)
                else:
                    print("No matching executable found to open.")


if __name__ == "__main__":
    search_and_open()
