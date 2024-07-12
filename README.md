# Notii-fy Music Player App

Notii-fy is a simple music player application built with Python and Tkinter. It allows users to play MP3 files from a specified folder, with basic playback controls and song details display. Additionally, it supports voice commands to play specific songs by their names.

![Notii-fy Music Player App](demo.png)

## Features

- **Play/Pause Controls:** Play, pause, and skip to the next or previous track.
- **Song Details Display:** Shows the currently playing song name and artist.
- **Album Art Display:** Displays album art if available in the MP3 file's ID3 tags.
- **Voice Command Support:** Play specific songs by their names using voice commands.

## Technologies Used

- Python
- Tkinter (GUI toolkit)
- Pygame (for music playback)
- Mutagen (for reading MP3 metadata)
- PIL (Python Imaging Library, for displaying album art)
- SpeechRecognition (for voice command recognition)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/notii-fy.git
   cd notii-fy
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the application:
   ```bash
   python main.py

## Usage

- Launch the application by running main.py.
- Choose a folder containing your MP3 files using the "Choose Folder" button.
- Click on the "▶ Play" button to start playing music from the selected folder.
- Use the playback control buttons (▶ Play, ❚❚ Pause, ▶▶ Next, ◀ Previous, ↺ Replay) to control playback.
- To play a specific song, say its name clearly using the voice command feature.
- The currently playing song name and artist are displayed, along with album art if available.

## Voice Command Setup

- Ensure your microphone is connected and configured properly on your system.
- Voice commands are recognized using the speech_recognition library.
- Speak clearly and say the name of the song you want to play to control playback.
