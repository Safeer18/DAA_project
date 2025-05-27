import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 170)
tts_engine.setProperty('volume', 1.0)

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen_command():
    with sr.Microphone() as source:
        speak("Listening...")
        print("[Voice] 🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"[Voice] ✅ Heard: {command}")
            return command
        except sr.UnknownValueError:
            print("[Voice] ❌ Could not understand audio")
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError as e:
            print(f"[Voice] ❌ Recognition error: {e}")
            speak("Speech recognition failed.")
            return ""
