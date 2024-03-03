import speech_recognition as sr
import pyautogui
import time
import helper_functions as hf

def speech_to_command(MICROPHONE_INDEX):
    time.sleep(2)
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index = MICROPHONE_INDEX)
    with microphone as source:
        print("Listening!")
        while True:
            speech = recognizer.listen(source, timeout=3)
            try:
                command = recognizer.recognize_google(speech)
                print(command)
                print(hf.command_to_action(command))
            except:
                print("Sorry could not recognize your voice")

MICROPHONE_INDEX = 1
speech_to_command(MICROPHONE_INDEX)
