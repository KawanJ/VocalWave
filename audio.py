import speech_recognition as sr
import time
import spotify_integration as spotify
import global_variables as gv

def recognize_speech(recognizer, speech):
    if gv.RECOGNITION_METHOD == "google":
        return recognizer.recognize_google(speech)
    elif gv.RECOGNITION_METHOD == "whisper":
        return recognizer.recognize_whisper(speech, language="english")
    else:
        raise ValueError("Invalid recognition method specified")

def speech_to_command(recognizer, source):
    speech = recognizer.listen(source, timeout=5)
    sentence = recognize_speech(recognizer, speech)
    print(sentence)
    print(spotify.command_to_action(sentence))

def start_audio_mode():
    time.sleep(2)
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index = gv.MICROPHONE_INDEX)
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening!")
        while True:
            speech = recognizer.listen(source, phrase_time_limit=3, timeout=3)
            try:
                input = recognize_speech(recognizer, speech)
                print(input)
                if input == gv.ACTIVATION_COMMAND:
                    speech_to_command(recognizer, source)
            except sr.UnknownValueError:
                print("Recognition Module could not understand audio")
            except sr.RequestError as e:
                print("Could not raise request", e)
            except Exception as e:
                print(e)

def start_audio_mode_without_activation():
    time.sleep(2)
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index = gv.MICROPHONE_INDEX)
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening!")
        while True:
            speech = recognizer.listen(source, phrase_time_limit=5, timeout=5)
            try:
                sentence = recognize_speech(recognizer, speech)
                print(sentence)
                print(spotify.command_to_action(sentence))
            except sr.UnknownValueError:
                print("Recognition Module could not understand audio")
            except sr.RequestError as e:
                print("Could not raise request", e)
            except Exception as e:
                print(e)