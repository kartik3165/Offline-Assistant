import json
import os


# File where songs will be saved
SONGS_FILE = "songs.json"

# Function to load songs from the JSON file
def load_songs():
    if os.path.exists(SONGS_FILE):
        with open(SONGS_FILE, "r") as f:
            return json.load(f)
    return {}

# Function to save songs to the JSON file
def save_songs(songs):
    with open(SONGS_FILE, "w") as f:
        json.dump(songs, f, indent=4)

# Function to display the list of songs
def display_songs(songs):
    if not songs:
        print("No songs in the list.")
    else:
        print("\nSong List:")
        for name, link in songs.items():
            print(f"{name}: {link}")

# Function to add a song
def add_song(songs):
    song_name = input("\nEnter song name: ")
    song_link = input("Enter song link: ")

    if song_name and song_link:
        songs[song_name] = song_link
        save_songs(songs)
        print(f"\nAdded: {song_name}")
    else:
        print("\nPlease provide both song name and song link.")

# Function to delete a song
def delete_song(songs):
    display_songs(songs)
    if not songs:
        return

    song_name = input("\nEnter the name of the song to delete: ")
    if song_name in songs:
        del songs[song_name]
        save_songs(songs)
        print(f"\nDeleted: {song_name}")
    else:
        print("\nSong not found.")

# Function to search for a song by name
def search_song(songs):
    song_name = processCommand(c)
    if song_name in songs:
        print(f"\nFound: {song_name}: {songs[song_name]}")
    else:
        print("\nSong not found.")

# Main function with options to add, delete, search, or view songs
def main():
    songs = load_songs()  # Load existing songs

    while True:
        print("\nOptions:")
        print("1. View song list")
        print("2. Add a song")
        print("3. Delete a song")
        print("4. Search for a song")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            display_songs(songs)
        elif choice == "2":
            add_song(songs)
        elif choice == "3":
            delete_song(songs)
        elif choice == "4":
            search_song(songs)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")

# Start the program
main()
