import sys
import speech_recognition as sr
import os
from text_to_speech import say

r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    audio = r.listen(source)
    with open("neco.wav", "wb") as file:
        file.write(audio.get_wav_data())
said = r.recognize_google(audio)
print(said)
say(said)
