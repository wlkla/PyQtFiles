import threading

import pyttsx3
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel, QPushButton


class HoverLabel(QLabel):
    def __init__(self, text, button, parent=None):
        super().__init__(text, parent)
        self.button = button

    def enterEvent(self, event):
        self.button.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        QTimer.singleShot(1000, self.startTimer)
        super().leaveEvent(event)

    def startTimer(self):
        if not self.button.underMouse():
            self.button.hide()


class ChatBubbleAi(QWidget):
    def __init__(self, text, mainwindow):
        super().__init__()
        self.ai_head_pic = QLabel()
        self.ai_head_pic.setFixedSize(35, 35)
        self.ai_head_pic.setStyleSheet("image: url(:/buttom/img/robot.png);")
        self.text_to_speech = QPushButton()
        self.text_to_speech.setFixedSize(20, 20)
        self.text_to_speech.setStyleSheet("border-radius:10px;\n"
                                          "image: url(:/buttom/img/语音ai.png);")
        self.text_to_speech.hide()
        self.text_to_speech.clicked.connect(self.read_text)
        self.label = HoverLabel(text, self.text_to_speech)
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                 "color: black;\n"
                                 "font: 10pt \"黑体\";\n"
                                 "padding: 10px;\n"
                                 "border-radius: 8px;")
        self.label.setCursor(Qt.IBeamCursor)

        layout = QHBoxLayout()
        layout.addWidget(self.ai_head_pic)
        layout.setAlignment(self.ai_head_pic, Qt.AlignTop)
        layout.addWidget(self.label)
        layout.addWidget(self.text_to_speech)
        layout.addStretch()
        self.setLayout(layout)

        self.mainwindow = mainwindow
        self.calculateSize()

    def setMessage(self, text):
        self.message = text
        self.label.setText(self.message)

    def calculateSize(self):
        mainwindow_width = self.mainwindow.width()
        max_width = mainwindow_width * 0.5

        metrics = QFontMetrics(self.label.font())
        text_width = metrics.horizontalAdvance(self.label.text())

        if text_width > max_width:
            self.label.setFixedWidth(int(max_width))
        else:
            self.label.setFixedWidth(int(text_width) + 29)

    def read_text(self):
        thread = threading.Thread(target=self.run_text_to_speech)
        thread.start()

    def run_text_to_speech(self):
        engine = pyttsx3.init()
        engine.say(self.label.text())
        engine.runAndWait()


class ChatBubbleMe(QWidget):
    def __init__(self, text, mainwindow):
        super().__init__()
        self.me_head_pic = QLabel()
        self.me_head_pic.setFixedSize(35, 35)
        self.me_head_pic.setStyleSheet("image: url(:/buttom/img/me.jpg);")
        self.text_to_speech = QPushButton()
        self.text_to_speech.setFixedSize(20, 20)
        self.text_to_speech.setStyleSheet("border-radius:10px;"
                                          "image: url(:/buttom/img/语音me.png);")
        self.text_to_speech.hide()
        self.text_to_speech.clicked.connect(self.read_text)
        self.label = HoverLabel(text, self.text_to_speech)
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setStyleSheet("background-color: rgb(137, 217, 97);\n"
                                 "color: white;\n"
                                 "font: 10pt \"黑体\";\n"
                                 "padding: 10px;\n"
                                 "border-radius: 8px;")
        self.label.setCursor(Qt.IBeamCursor)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.text_to_speech)
        layout.addWidget(self.label)
        layout.addWidget(self.me_head_pic)
        layout.setAlignment(self.me_head_pic, Qt.AlignTop)
        self.setLayout(layout)

        self.mainwindow = mainwindow
        self.calculateSize()

    def setMessage(self, text):
        self.message = text
        self.label.setText(self.message)

    def calculateSize(self):
        mainwindow_width = self.mainwindow.width()
        max_width = mainwindow_width * 0.5

        metrics = QFontMetrics(self.label.font())
        text_width = metrics.horizontalAdvance(self.label.text())

        if text_width > max_width:
            self.label.setFixedWidth(int(max_width))
        else:
            self.label.setFixedWidth(int(text_width) + 29)

    def read_text(self):
        thread = threading.Thread(target=self.run_text_to_speech)
        thread.start()

    def run_text_to_speech(self):
        engine = pyttsx3.init()
        engine.say(self.label.text())
        engine.runAndWait()
