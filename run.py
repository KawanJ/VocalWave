import speech_recognition as sr
import pyautogui
import time

def speech_to_command():
    time.sleep(5)
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Anything :")
        speech = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(speech)
            if(command == "play" or command == "pause"):
                pyautogui.press('space')
        except:
            print("Sorry could not recognize your voice")

speech_to_command()
