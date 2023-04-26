import speech_recognition as sr
import pyttsx3
import webbrowser
import time
import subprocess
import threading

from frontend__helpers.popup import show_popup
from utils.utils import speak, wishMe, runProcess, killProcess, song


engine=pyttsx3.init()
r = sr.Recognizer()
mic = sr.Microphone()

# create a new thread for the popup
popup_thread = threading.Thread(target=show_popup)


def takeCommand(r):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.5
        print(r.energy_threshold)
        print("Listening...")
        audio = r.listen(source)

    try:
        statement = r.recognize_google(audio, language='en-in')
        print(f"user said:{statement}\n")

    except Exception as e:
        print(e)
        return "none"
    return statement

wishMe()
speak("Nacho is starting up...")

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
        
        elif 'open code' in statement:
            runProcess('code')

        elif 'close code' in statement:
            killProcess('code')
        
        elif 'open terminal' in statement:
            runProcess('gnome-terminal')
        
        elif 'close terminal' in statement:
            killProcess('gnome-terminal')
        
        elif 'open steam' in statement:
            runProcess('steam')
        
        elif 'close steam' in statement:
            killProcess('steam')
        
        # elif 'play ' in statement and 'on spotify' in statement:
        #     song_name = statement.replace('play ', '').replace(' on spotify', '')
        #     play_song(song_name)

        elif 'open spotify' in statement:
            runProcess('spotify')

        elif 'close spotify' in statement:
            killProcess('spotify')
        
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