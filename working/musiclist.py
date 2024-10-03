import random
def HipHopSong():
    Music = {
        "Sicko Mode": "https://www.youtube.com/watch?v=6ONRf7h3Mdk",
        "God's Plan": "https://www.youtube.com/watch?v=xpVfcZ0ZcFM",
        "HUMBLE.": "https://www.youtube.com/watch?v=tvTRZJ-4EyI",
        "Old Town Road": "https://www.youtube.com/watch?v=w2OeCwTJu7Q",
        "SAD!": "https://www.youtube.com/watch?v=pgN_Vv3wDik",
        "Bad and Boujee": "https://www.youtube.com/watch?v=S_sogk06K0A",
        "Rockstar": "https://www.youtube.com/watch?v=U6DiQ2Wa9A0",
        "Mask Off": "https://www.youtube.com/watch?v=4nDoJYtC3wQ",
        "Bodak Yellow": "https://www.youtube.com/watch?v=PEGccV-NryU",
        "Money Trees": "https://www.youtube.com/watch?v=U14Zuxh8Lzc",
        "The Box": "https://www.youtube.com/watch?v=UNpOX5hfqDE",
        "Goosebumps": "https://www.youtube.com/watch?v=neH_m2rxA4U",
        "Mo Bamba": "https://www.youtube.com/watch?v=2r5Pta7uF3c",
        "Lucid Dreams": "https://www.youtube.com/watch?v=2TgMs0F5mWc",
        "Antidote": "https://www.youtube.com/watch?v=aDfbYBF9Q9E",
        "Dior": "https://www.youtube.com/watch?v=r-kVsDh3Adk",
        "WAP": "https://www.youtube.com/watch?v=hsm4poTWj2U",
        "Rapstar": "https://www.youtube.com/watch?v=x-8drrAATV0",
        "Laugh Now Cry Later": "https://www.youtube.com/watch?v=3W9TMqNNl6c",
        "What's Poppin": "https://www.youtube.com/watch?v=5rEglvXk7do",
        "Suge": "https://www.youtube.com/watch?v=yEJ6N-swBOI",
        "Highest in the Room": "https://www.youtube.com/watch?v=39Vr0nC-7Mk",
        "Sunflower": "https://www.youtube.com/watch?v=ApXoWvfEYVc",
        "Industry Baby": "https://www.youtube.com/watch?v=4xD2FB_pH_E",
        "Hurricane": "https://www.youtube.com/watch?v=7m5DTdABJ18",
        "Kiss Me More": "https://www.youtube.com/watch?v=0EVlZ4b4n-g",
        "Stay": "https://www.youtube.com/watch?v=kTJczUoc26U",
        "Ski": "https://www.youtube.com/watch?v=22pR5o-jgqI",
        "Big Energy": "https://www.youtube.com/watch?v=0J4D3rzp2gA",
        "First Class": "https://www.youtube.com/watch?v=w34lAohZThI"
    }

    # Pick a random song from the dictionary and return separate title and URL
    def pick_random_song(music_dict):
        # Get a list of all the song titles (keys)
        songs = list(music_dict.keys())
        # Pick a random song title
        random_song = random.choice(songs)
        # Return the song title and its URL separately
        return random_song, music_dict[random_song]

    # Example usage
    song_title, song_url = pick_random_song(Music)
    return song_title, song_url


HipHopSong()



