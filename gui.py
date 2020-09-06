import sys
import random
from PyQt5 import QtCore, QtWidgets, QtGui
import voice_recog.speech_to_text as vr
import voice_recog.text_to_speech as ts
import words_to_events.word_proccessing as we

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.setMaximumWidth(400) 

        self.button = QtWidgets.QPushButton("Klikni pro coool speech")
        
        self.text = QtWidgets.QLabel("Hello World")
        self.text.setStyleSheet("color: red")
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setWordWrap(True)
        self.setStyleSheet("background-color: yellow;") 

        self.response = QtWidgets.QLabel()
        self.response.setStyleSheet("color: green")
        self.response.setAlignment(QtCore.Qt.AlignCenter)
        self.response.setWordWrap(True)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.response)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.magic)
        
        ts.bag.punched.connect(self.say_punched)
        ts.bag2.punched.connect(self.say_punched2)
        ts.bag.punched.connect(ts.say)
        ts.bag2.punched.connect(ts.say2)

    @QtCore.pyqtSlot(str)
    def say_punched(self, string):
        ''' Give evidence that a bag was punched. '''
        print('Bag was punched.', string)
        self.text.setText(string)

    @QtCore.pyqtSlot(str)
    def say_punched2(self, string):
        ''' Give evidence that a bag was punched. '''
        print('Bag2 was punched.', string)
        self.response.setText(string)
    
    def magic(self):
        self.button.clicked.disconnect(self.magic)
        try:
            said = vr.speech_to_text()
            events = we.find_right_events(said)
            self.response.setText("eventy:"+str(events))
            we.events_to_speaker_and_google_calendar(events)
        except:
            self.button.clicked.connect(self.magic)    

class Info(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.setMaximumWidth(400) 

        self.info = QtWidgets.QLabel()
        self.info = QtWidgets.QLabel("Hello World")
        self.info.setAlignment(QtCore.Qt.AlignCenter)
        self.info.setWordWrap(True)
        self.setStyleSheet("background-color: pink;") 

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.info)
        self.setLayout(self.layout)
        
        ts.bag3.punched.connect(self.say_punched3)

    @QtCore.pyqtSlot(str)
    def say_punched3(self, string):
        ''' Give evidence that a bag was punched. '''
        print('Bag3 was punched.', string)
        self.info.setText(string)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, talks, info):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("ApoLenka")
        layout = QtWidgets.QHBoxLayout()

        layout.addWidget(talks)
        layout.addWidget(info)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    info = Info()
    window = MainWindow(widget, info)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
