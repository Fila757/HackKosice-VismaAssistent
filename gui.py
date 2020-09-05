import sys
import random
from PyQt5 import QtCore, QtWidgets, QtGui
import voice_recog.speech_to_text as vr
import words_to_events.word_proccessing as we

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.setMaximumWidth(200) 

        self.button = QtWidgets.QPushButton("Klikni pro coool speech")
        self.text = QtWidgets.QLabel("Hello World")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.response = QtWidgets.QLabel()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.response)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.magic)

    def magic(self):
        said = vr.speech_to_text()
        self.text.setText(said)
        vr.say(said)
        events = we.find_right_events(said)
        self.response.setText("eventy:"+str(events))
        we.events_to_speaker_and_google_calendar(events)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, widget):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("Tutorial")
        self.setCentralWidget(widget)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    window = MainWindow(widget)
    window.resize(800, 600)
    window.show()
    
    sys.exit(app.exec_())
