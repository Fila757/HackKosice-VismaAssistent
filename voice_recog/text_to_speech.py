from gtts import gTTS
import os

def say(string):
    tts = gTTS(text=string, lang='en')
    tts.save("good.mp3")
    os.system("vlc good.mp3")
