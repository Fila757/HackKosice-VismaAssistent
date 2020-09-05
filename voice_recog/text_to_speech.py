from gtts import gTTS
import os
from playsound import playsound

def say(string):
    tts = gTTS(text=string, lang='en')
    tts.save("good.mp3")
    playsound("good.mp3")
