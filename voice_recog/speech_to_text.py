import sys
import speech_recognition as sr
import os
import voice_recog.text_to_speech as ts

def speech_to_text():
    r = sr.Recognizer()
    mic = sr.Microphone()

    while(True):
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                with open("neco.wav", "wb") as file:
                    file.write(audio.get_wav_data())
            said = r.recognize_google(audio)
            break
        except:
            ts.bag2.punch("Sorry, I didn't understand you correctly. Could you please repeat it?")
        
    
    print(said)
    ts.bag.punch(said)
    return said
