import speech_recognition as sr
import pyttsx3
import datetime
import subprocess
import dbus

engine=pyttsx3.init()
r = sr.Recognizer()
mic = sr.Microphone()


def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
         speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon...")
    else:
        speak("Good evening...!")

def runProcess(process):
    subprocess.Popen([process])
    speak(f"{process} is now open")

def killProcess(process):
    out = subprocess.check_output(['pgrep', process])
    pids = out.decode().strip().split('\n')
    for pid in pids:
        subprocess.run(['kill', pid])
    speak(f"{process} has been closed")

# def play_song(song_name):
#     # Connect to the DBus session bus
#     session_bus = dbus.SessionBus()

#     # Get the Spotify DBus service
#     spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")

#     # Get the Spotify interface
#     spotify_interface = dbus.Interface(spotify_bus,"org.mpris.MediaPlayer2.Player")

#     # Search for the song
#     search_results = spotify_bus.Get("org.mpris.MediaPlayer2.Player", "Metadata", dbus_interface="org.freedesktop.DBus.Properties")
#     print(search_results)
#     for key, value in search_results.items():
#         print(song_name)
#         print(value)
#         if song_name.lower() in str(value).lower():
#             song_uri = search_results['xesam:url'][key]
#             break

#     # Play the song
#     dbus_send = f"dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.OpenUri string:{song_uri}"
#     subprocess.Popen(dbus_send, shell=True)

#     # Speak the song name
#     speak(f"Now playing {song_name} on Spotify.")

def song(command):
    # Connect to the DBus session bus
    session_bus = dbus.SessionBus()

    # Get the Spotify DBus service
    spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")

    # Get the Spotify interface
    spotify_interface = dbus.Interface(spotify_bus,"org.mpris.MediaPlayer2.Player")

    # Call the Next method
    if command == 'next':
        spotify_interface.Next()
        speak("Now playing next song on Spotify.")
    elif command == 'previous':
        spotify_interface.Previous()
        speak("Now restarting song on Spotify.")
    elif command == 'pause':
        spotify_interface.Pause()
        speak("Now stopping song on Spotify.")
    elif command == 'play':
        spotify_interface.Play()
        speak("Now playing song on Spotify.")