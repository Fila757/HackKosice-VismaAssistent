import sys
import speech_recognition as sr
import os

r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    audio = r.listen(source)
    with open("neco.wav", "wb") as file:
        file.write(audio.get_wav_data())
said = r.recognize_google(audio)
print(said)
with open("said.txt","w") as file:
    file.write(said)

os.system("python3 text_to_speech.py")
