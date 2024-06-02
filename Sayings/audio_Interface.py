import random
from classSet import *
from audio import Ui_Form
import configparser
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox

from PyQt5.QtCore import pyqtSignal, QTimer


class audioInterface(Ui_Form, QWidget):
    addAudio = pyqtSignal()

    def __init__(self):
        super(audioInterface, self).__init__()
        self.setupUi(self)
        self.setObjectName('audio')
        self.initAudio()
        self.importAudio.clicked.connect(self.addnewAudio)  # type: ignore

    def initAudio(self):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        audio_list = base_path + '/audio/audio_list.txt'
        audio_like = base_path + '/audio/audio_like.txt'
        try:
            with open(audio_list, 'r', encoding='utf-8') as f:
                audio_1 = [(line.strip(), 0) for line in f.readlines()]
            with open(audio_like, 'r', encoding='utf-8') as f:
                audio_2 = [(line.strip(), 1) for line in f.readlines()]
            self.audios = audio_1 + audio_2
            random.shuffle(self.audios)
            QTimer.singleShot(0, self.addAudioCard)
        except:
            pass

    def updateAudioCardIcon(self):
        for i in range(self.verticalLayout_3.count()):
            widget=self.verticalLayout_3.itemAt(i).widget()
            if isinstance(widget,AppCard):
                widget.updateIconOrText('audio')

    def addAudioCard(self):
        if not self.audios:
            return
        audio, like_tag = self.audios.pop(0)
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        audio_card_content = config.get('Settings', 'audio_card_content')
        path = audio.replace('\\', '/')
        card = AppCard(path, audio_card_content, 'audio', like_tag, self)
        card.likeSignal.connect(lambda file=path, widget=card: self.likeT(file, widget))
        card.deleteSignal.connect(lambda file=path, widget=card: self.deleteT(file, widget))

        # 检查最后一个组件是否是弹簧
        last_item = self.verticalLayout_3.itemAt(self.verticalLayout_3.count() - 1)
        if isinstance(last_item, QSpacerItem):
            self.verticalLayout_3.removeItem(last_item)

        self.verticalLayout_3.addWidget(card, alignment=Qt.AlignTop)
        card.play.connect(lambda: self.playAudio(path))

        has_bar = self.ScrollArea.verticalScrollBar().isVisible()
        if not has_bar:
            spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.verticalLayout_3.addItem(spacerItem)

        QTimer.singleShot(0, self.addAudioCard)

    def addnewAudio(self):
        files, ok = QFileDialog.getOpenFileNames(self, '音频文件', '', "Audio Files (*.mp3 *.wav *.ogg *.flac)")
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        audio_list = base_path + '/audio/audio_list.txt'
        if files and ok:
            audio_like = base_path + '/audio/audio_like.txt'
            with open(audio_list, 'r', encoding='utf-8') as f:
                existing_audio_1 = [line.strip() for line in f.readlines()]
            with open(audio_like, 'r', encoding='utf-8') as f:
                existing_audio_2 = [line.strip() for line in f.readlines()]
            existing_audios = existing_audio_1 + existing_audio_2
            self.audios = [(audio.replace('\\', '/'), 0) for audio in files if audio not in existing_audios]
            if self.audios:
                with open(audio_list, 'a', encoding='utf-8') as f:
                    for audio, _ in self.audios:
                        f.write(audio + '\n')
            QTimer.singleShot(0, self.addAudioCard)

    def likeT(self, path, card):
        try:
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            base_path = config.get('Settings', 'base_path')
            audio_list = base_path + '/audio/audio_list.txt'
            audio_like = base_path + '/audio/audio_like.txt'
            (my_icon, text, file_d, file_a) = (
                FluentIcon.HEART, 'Like', audio_like, audio_list) if card.is_liked else (
                FluentIcon.EXPRESSIVE_INPUT_ENTRY, 'Unlike', audio_list, audio_like)
            card.like_action.setIcon(my_icon)
            card.like_action.setText(text)
            with open(file_d, 'r', encoding='utf-8') as f:
                likes = f.readlines()
            with open(file_d, 'w', encoding='utf-8') as f:
                for like in likes:
                    if like.strip() != path:
                        f.write(like)
            with open(file_a, 'a', encoding='utf-8') as f:
                f.write(path + '\n')
            card.is_liked = 1 - card.is_liked
            try:
                card.like_action.disconnect()
            except:
                pass
            self.update()
            self.addAudio.emit()  # type: ignore
        except:
            pass

    def deleteT(self, path, card):
        for i in reversed(range(self.verticalLayout_3.count())):
            widget = self.verticalLayout_3.itemAt(i).widget()
            if isinstance(widget, AppCard) and widget.path == path:
                self.verticalLayout_3.removeWidget(widget)
                widget.deleteLater()
                break
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        audio_list = base_path + '/audio/audio_list.txt'
        audio_like = base_path + '/audio/audio_like.txt'
        txt = audio_like if card.is_liked else audio_list
        with open(txt, 'r', encoding='utf-8') as f:
            likes = f.readlines()
        with open(txt, 'w', encoding='utf-8') as f:
            for like in likes:
                if like.strip() != path:
                    f.write(like)
        self.addAudio.emit()  # type: ignore

    def playAudio(self, path):
        try:
            os.startfile(path, 'open')
        except:
            QMessageBox.warning(self, '提示', '未定位到文件，可能被移动或改名')
