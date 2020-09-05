from gtts import gTTS
import os
with open("said.txt", "r") as file:
    said = file.read()
tts = gTTS(text=said, lang='en')
tts.save("good.mp3")
os.system("vlc good.mp3")
