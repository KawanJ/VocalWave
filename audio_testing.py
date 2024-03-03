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
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except:
            print("Unknown Error")

MICROPHONE_INDEX = 1
get_audio(MICROPHONE_INDEX)