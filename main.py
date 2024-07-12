import os
import random
import tkinter as tk
import threading
import speech_recognition as sr
from tkinter import filedialog
import io
from PIL import Image, ImageTk
from pygame import mixer
from mutagen.mp3 import MP3

class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notii-fy")
        self.root.configure(bg="#191414")
        self.root.geometry("400x500")
        self.main_frame = tk.Frame(root, bg="#121212")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Initialize mixer
        mixer.init()

        # Initialize variables
        self.folder_path = tk.StringVar()
        self.current_song_index = 0
        self.current_song_name = tk.StringVar()
        self.current_song_artist = tk.StringVar()

        # Placeholder image for album art
        self.placeholder_image = ImageTk.PhotoImage(Image.open("placeholder_image.jpg"))

        # Create UI elements
        self.create_widgets()

        # Set default folder path to "Songs" folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.folder_path.set(os.path.join(script_dir, "Songs"))

        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()

    def create_widgets(self):
        # Heading
        heading_label = tk.Label(
            self.main_frame,
            text="Notii-fy?",
            bg="#191414",
            fg="#1DB954",
            font=("Arial", 20, "bold"),
        )
        heading_label.pack(pady=10)

        # Placeholder image above buttons
        self.default_image_label = tk.Label(self.main_frame, bg="#121212", image=self.placeholder_image)
        self.default_image_label.pack(pady=10)

        # Play, Pause, Next buttons in the same line
        button_frame = tk.Frame(self.main_frame, bg="#121212")
        button_frame.pack(pady=5)

        # Play button
        play_button = tk.Button(
            button_frame,
            text="▶ Play",
            command=self.play,
            bg="#1DB954",
            fg="#ffffff",
            font=("Arial", 12),
        )
        play_button.pack(side="left", padx=5)

        # Pause button
        pause_button = tk.Button(
            button_frame,
            text="❚❚ Pause",
            command=self.pause,
            bg="#1DB954",
            fg="#ffffff",
            font=("Arial", 12),
        )
        pause_button.pack(side="left", padx=5)

        # Next button
        next_button = tk.Button(
            button_frame,
            text="▶▶ Next",
            command=self.next_song,
            bg="#1DB954",
            fg="#ffffff",
            font=("Arial", 12),
        )
        next_button.pack(side="left", padx=5)

        # Button frame for Previous and Replay buttons
        button_frame2 = tk.Frame(self.main_frame, bg="#121212")
        button_frame2.pack(pady=5)

        # Previous button
        previous_button = tk.Button(
            button_frame2,
            text="◀ Previous",
            command=self.previous_song,
            bg="#1DB954",
            fg="#ffffff",
            font=("Arial", 12),
        )
        previous_button.pack(side="left", padx=5)

        # Replay button
        replay_button = tk.Button(
            button_frame2,
            text="↺ Replay",
            command=self.replay_song,
            bg="#1DB954",
            fg="#ffffff",
            font=("Arial", 12),
        )
        replay_button.pack(side="left", padx=5)

        # Currently playing label
        self.current_song_label = tk.Label(
            self.main_frame,
            textvariable=self.current_song_name,
            bg="#121212",
            fg="#1DB954",
            font=("Arial", 14, "bold"),
        )
        self.current_song_label.pack(pady=10)

        # Song artist label
        self.current_artist_label = tk.Label(
            self.main_frame,
            textvariable=self.current_song_artist,
            bg="#121212",
            fg="#1DB954",
            font=("Arial", 12),
        )
        self.current_artist_label.pack(pady=5)

        # Album art label
        self.album_art_label = tk.Label(self.main_frame, bg="#121212")
        self.album_art_label.pack(pady=10)

    def play(self):
        folder_path = self.folder_path.get()
        if folder_path:
            mp3_files = [file for file in os.listdir(folder_path) if file.endswith(".mp3")]
            random.shuffle(mp3_files)
            self.play_song(folder_path, mp3_files[self.current_song_index])

    def play_song(self, folder_path, mp3_file):
        mixer.music.load(os.path.join(folder_path, mp3_file))
        mixer.music.play()
        self.current_song_name.set(mp3_file)
        self.get_song_details(folder_path, mp3_file)

    def get_song_details(self, folder_path, mp3_file):
        audio = MP3(os.path.join(folder_path, mp3_file))
        try:
            artist = audio["TPE1"].text[0]  # Extract artist from ID3 tags
        except KeyError:
            artist = "Unknown Artist"
        self.current_song_artist.set(artist)

        # Fetch album art (if available) and display it
        if "APIC:" in audio.tags:
            album_art = audio.tags["APIC:"].data
            img = ImageTk.PhotoImage(Image.open(io.BytesIO(album_art)))
            self.placeholder_image = img
            self.album_art_label.config(image=img)
            self.default_image_label.config(image=img)

    def pause(self):
        mixer.music.pause()

    def next_song(self):
        folder_path = self.folder_path.get()
        if folder_path:
            mp3_files = [file for file in os.listdir(folder_path) if file.endswith(".mp3")]
            self.current_song_index = (self.current_song_index + 1) % len(mp3_files)
            self.play_song(folder_path, mp3_files[self.current_song_index])

    def previous_song(self):
        folder_path = self.folder_path.get()
        if folder_path:
            mp3_files = [file for file in os.listdir(folder_path) if file.endswith(".mp3")]
            self.current_song_index = (self.current_song_index - 1) % len(mp3_files)
            self.play_song(folder_path, mp3_files[self.current_song_index])

    def replay_song(self):
        folder_path = self.folder_path.get()
        if folder_path:
            mp3_files = [file for file in os.listdir(folder_path) if file.endswith(".mp3")]
            self.play_song(folder_path, mp3_files[self.current_song_index])

    def quit(self):
        mixer.music.stop()
        mixer.quit()
        self.root.destroy()

    def voice_command(self):
        while True:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)

            try:
                command = self.recognizer.recognize_google(audio).lower()
                print("Command:", command)
                if "play" in command:
                    song_name = command.split("play")[-1].strip()
                    self.play_specified_song(song_name)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Error with the speech recognition service; {0}".format(e))

    def play_specified_song(self, song_name):
        folder_path = self.folder_path.get()
        if folder_path:
            mp3_files = [file for file in os.listdir(folder_path) if file.lower() == (song_name + ".mp3").lower()]
            if mp3_files:
                self.play_song(folder_path, mp3_files[0])
            else:
                print(f"Could not find {song_name}.mp3 in the specified folder.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)

    # Start listening for voice commands in a separate thread
    voice_thread = threading.Thread(target=app.voice_command)
    voice_thread.daemon = True  # Make sure the thread exits when the main program exits
    voice_thread.start()

    root.mainloop()
