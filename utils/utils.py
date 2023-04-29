from dotenv import load_dotenv
from google.cloud import texttospeech_v1
from frontend__helpers.popup import show_popup

import speech_recognition as sr
import io
import datetime
import subprocess
import dbus
import os
import openai
import pygame
import tkinter as tk

# load enviornmental variables and keys
load_dotenv()
openai.api_key = os.getenv("OPEN_AI_KEY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_credentials.json"

# speech recognition
r = sr.Recognizer()
mic = sr.Microphone()

# text to speech
client = texttospeech_v1.TextToSpeechClient()
voice = texttospeech_v1.VoiceSelectionParams(
    name="en-GB-Standard-B",
    language_code="en-GB",
)
audio_config = texttospeech_v1.AudioConfig(
    audio_encoding=texttospeech_v1.AudioEncoding.MP3,
)

def speak(text):
    # call popup and show the text that is being spoken
    root = tk.Tk()
    show_popup(root, 'Nacho is thinking...')

    # Synthesize the received text into speech
    synthesis_input = texttospeech_v1.SynthesisInput(text=text)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    # Save the received response to an MP3 file
    with open("./nacho.mp3", "wb") as out:
        out.write(response.audio_content)
    
    # Play the saved MP3 file after receiving the response and saving it
    play_audio("./nacho.mp3")

    # kill popup
    root.destroy()

def play_audio(file_path):
    # Initialize the pygame mixer to handle audio playback
    pygame.mixer.init()
    # Load the specified audio file into the mixer
    pygame.mixer.music.load(file_path)
    # Start playing the loaded audio file
    pygame.mixer.music.play()
    # Keep the program running while the audio is still playing
    while pygame.mixer.music.get_busy():
        # Use a clock to keep track of time and control the loop's frequency
        pygame.time.Clock().tick(10)

def engage_AI_conv(newTakeCommand, r):
    speak('attempting to engage conversation...')
    messages = [{"role": "user", "content": "Your name is Nacho, please keep the conversation short and concise. Show me that you understand your role by answering this message saying exactly: Nacho has come out to play, what up with it?"}]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= messages)
    speak(completion.choices[0].message.content)
    while True:
        statement = newTakeCommand(r).lower()
        if statement==0:
            continue
        if 'exit conversation' in statement:
            speak('AI disconnected')
            break
        elif statement is not None and statement != 'none' and (statement.strip() != ''):
            messages.append({"role": "user", "content": statement})
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages= messages)
            speak(completion.choices[0].message.content)
            messages.append({"role": "assistant", "content": completion.choices[0].message.content})
            print(messages)

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
         speak("Good Morning")
    elif hour>=12 and hour<18:
        speak("Good Afternoon...")
    else:
        speak("Good evening...")

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