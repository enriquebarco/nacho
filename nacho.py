import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import time

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
        speak("Good Afternoon")
    else:
        speak("Good evening!")

def takeCommand(r):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.5
        print("Listening...")
        audio = r.listen(source, timeout=5)

    try:
        statement = r.recognize_google(audio, language='en-in')
        print(f"user said:{statement}\n")

    except Exception as e:
        print(e)
        return "none"
    return statement

speak("Nacho is ready")
wishMe()

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
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail is open now")
            time.sleep(5)
