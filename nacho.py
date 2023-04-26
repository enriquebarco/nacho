import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import time
import subprocess
import dbus

engine=pyttsx3.init()
r = sr.Recognizer()
mic = sr.Microphone()


def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand(r):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.5
        print("Listening...")
        audio = r.listen(source, timeout=8)

    try:
        statement = r.recognize_google(audio, language='en-in')
        print(f"user said:{statement}\n")

    except Exception as e:
        print(e)
        return "none"
    return statement

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
         speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
    else:
        speak("Good evening!")

def runProcess(process):
    subprocess.run([process])
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

wishMe()
speak("Nacho is ready")

if __name__=='__main__':

    while True:
        statement = takeCommand(r).lower()
        if statement==0:
            continue
        if "goodbye" in statement or "ok bye" in statement or "nacho off" in statement:
            speak ('see you later!')
            break

        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://youtube.com")
            speak("youtube is now open")
            time.sleep(3)
        
            
        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is open now")

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail is open now")
        
        elif 'open slack' in statement:
            runProcess('slack')
        
        elif 'close slack' in statement:
            killProcess('slack')
        
        elif 'open spotify' in statement:
            subprocess.run(['spotify'])

        elif 'close spotify' in statement:
            killProcess('spotify')
        
        elif 'open code' in statement:
            runProcess('code')

        elif 'close code' in statement:
            killProcess('code')
        
        elif 'open terminal' in statement:
            runProcess('gnome-terminal')
        
        elif 'close terminal' in statement:
            killProcess('gnome-terminal')
        
        # elif 'play ' in statement and 'on spotify' in statement:
        #     song_name = statement.replace('play ', '').replace(' on spotify', '')
        #     play_song(song_name)
        
        elif 'play discover weekly on spotify' in statement:
            # Check if Spotify is running
            result = subprocess.run(["pgrep", "spotify"], stdout=subprocess.PIPE)
            if not result.stdout:
                # Spotify is not running, start it
                runProcess('spotify')
            dbus_send = f"dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.OpenUri string:spotify:playlist:37i9dQZEVXcQrLA7FSuSkF"
            subprocess.Popen(dbus_send, shell=True)
            speak("Now playing Discover Weekly on Spotify.")
        
        elif 'play next song' in statement:
            song('next')
        
        elif 'restart song' in statement:
            song('previous')
        
        elif 'pause song' in statement:
            song('pause')
        
        elif 'play song' in statement:
            song('play')