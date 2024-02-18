import speech_recognition as sr

def get_audio(MICROPHONE_INDEX):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index = MICROPHONE_INDEX)
    with microphone as source:
        print("Listening!")
        speech = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(speech)
            print(command)

            with open("audio.wav", "wb") as file:
                file.write(speech.get_wav_data())
            print("Audio saved to audio.wav")
        except:
            print("Sorry could not recognize your voice")

MICROPHONE_INDEX = 2
get_audio(MICROPHONE_INDEX)