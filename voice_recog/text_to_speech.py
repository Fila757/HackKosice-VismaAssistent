from gtts import gTTS
import os, sys
from playsound import playsound
from PyQt5 import QtCore

class PunchingBag(QtCore.QObject):
    ''' Represents a punching bag; when you punch it, it
        emits a signal that indicates that it was punched. '''
    punched = QtCore.pyqtSignal(str)

    def __init__(self):
        # Initialize the PunchingBag as a QObject
        QtCore.QObject.__init__(self)

    def punch(self, string):
        ''' Punch the bag '''
        self.punched.emit(string)

@QtCore.pyqtSlot(str)
def say(string):
    tts = gTTS(text=string, lang='en')
    tts.save("good.mp3")
    playsound("good.mp3")

@QtCore.pyqtSlot(str)
def say2(string):
    tts = gTTS(text=string, lang='en-uk')
    tts.save("good.mp3")
    playsound("good.mp3")

bag = PunchingBag()
bag2 = PunchingBag()
bag3 = PunchingBag()
