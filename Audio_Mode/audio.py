import speech_recognition as sr
import time
import pyttsx3
import Helper_Files.nlp as nlp
import Audio_Mode.spotify_integration as spotify
import Helper_Files.global_variables as gv

# Initialize the text-to-speech engine
def initialize_TTS():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 0.6)  # Volume (0.0 to 1.0)
    return engine

def run_TTS(text):
    tts_engine = initialize_TTS()
    tts_engine.say(text)
    tts_engine.runAndWait()

def recognize_speech(recognizer, speech):
    if gv.RECOGNITION_METHOD == "google":
        return recognizer.recognize_google(speech)
    elif gv.RECOGNITION_METHOD == "whisper":
        return recognizer.recognize_whisper(speech, language="english")
    else:
        raise ValueError("Invalid recognition method specified")

def speech_to_command(recognizer, source):
    speech = recognizer.listen(source, phrase_time_limit=5)
    sentence = recognize_speech(recognizer, speech)
    command = nlp.sentence_to_keyword(sentence)
    print(sentence)
    print(command)
    command_status = spotify.command_to_action(command)
    if command_status == "Invalid Command":
        run_TTS("Could not understand. Please try again")
        

def start_audio_mode():
    time.sleep(2)
    run_TTS("Project started in Audio mode")
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index = gv.MICROPHONE_INDEX)
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for Activation Command!")
        while True:
            speech = recognizer.listen(source, phrase_time_limit=4)
            try:
                command = recognize_speech(recognizer, speech)
                print(command)
                if nlp.clean_command(command) == gv.ACTIVATION_COMMAND:
                    print('Listening for Spotify Command')
                    speech_to_command(recognizer, source)
            except sr.UnknownValueError:
                print("Recognition Module could not understand audio")
            except sr.RequestError as e:
                print("Could not raise request", e)
            except Exception as e:
                print(e)

def start_audio_mode_without_activation():
    time.sleep(2)
    run_TTS("Project started in Audio mode without activation keyword")
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index = gv.MICROPHONE_INDEX)
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening!")
        while True:
            speech = recognizer.listen(source, phrase_time_limit=6)
            try:
                sentence = recognize_speech(recognizer, speech)
                command = nlp.sentence_to_keyword(sentence)
                print(sentence)
                print("Command: ", command)
                command_status = spotify.command_to_action(command)
                    
            except sr.UnknownValueError:
                print("Recognition Module could not understand audio")
            except sr.RequestError as e:
                print("Could not raise request", e)
            except Exception as e:
                print(e)