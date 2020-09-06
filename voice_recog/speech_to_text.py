import sys, os
import speech_recognition as sr
import voice_recog.text_to_speech as ts


def speech_to_text():
    r = sr.Recognizer()
    mic = sr.Microphone()

    for i in range(3):
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            said = r.recognize_google(audio)
            break
        except:
            ts.bag2.punch("Sorry, I didn't understand you correctly. Could you please repeat it?")
            raise Exception("end")
    else:
        ts.bag2.punch("Sorry, I tried several times and still don't understand you. I give up.")

    print(said)
    ts.bag.punch(said)

    return said
