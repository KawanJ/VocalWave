import speech_recognition as sr
import time
import spotify_integration as spotify
import global_variables as gv

def speech_to_command(recognizer, source):
    speech = recognizer.listen(source, timeout=5)
    sentence = recognizer.recognize_google(speech)
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
                input = recognizer.recognize_google(speech)
                print(input)
                if input == gv.ACTIVATION_COMMAND:
                    speech_to_command(recognizer, source)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            except:
                print("Unknown Error")
