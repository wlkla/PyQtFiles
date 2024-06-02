import os
from classSet import *
from home import Ui_Form
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QMessageBox
from qfluentwidgets import HorizontalFlipView


class homeInterface(Ui_Form, QWidget):
    updateSignal = pyqtSignal()

    def __init__(self):
        super(homeInterface, self).__init__()
        self.setupUi(self)
        self.setObjectName('home')
        self.initUi()
        self.msgWin = messageWindow()

    def initUi(self):
        self.flip_View = HorizontalFlipView(self)
        self.flip_View.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self.flip_View.setItemDelegate(CustomFlipItemDelegate(self.flip_View))
        self.flip_View.setBorderRadius(25)
        self.flip_View.setFixedHeight(255)
        self.flip_View.setSpacing(15)
        self.flip_View.currentIndexChanged.connect(self.updateIndex)
        self.verticalLayout_3.addWidget(self.flip_View)

        self.initPhoto()
        self.initChat()
        self.initAudio()
        self.initVideo()

    def initPhoto(self):
        self.images = None
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        photo_like = base_path + '/photo/photo_like.txt'
        try:
            with open(photo_like, 'r', encoding='utf-8') as f:
                self.images = [line.strip() for line in f.readlines()]
                self.images = self.images[-2:] + self.images + self.images[:2]
        except:
            pass
        QTimer.singleShot(0, self.addPhotoCard)

    def initChat(self):
        self.messages = None
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        chat_like = base_path + '/chat/chat_like.txt'
        try:
            with open(chat_like, 'r', encoding='utf-8') as f:
                self.messages = [line.strip() for line in f.readlines()]
        except:
            pass
        QTimer.singleShot(0, self.addMessageCard)

    def initAudio(self):
        self.audios = None
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        audio_like = base_path + '/audio/audio_like.txt'
        try:
            with open(audio_like, 'r', encoding='utf-8') as f:
                self.audios = [line.strip() for line in f.readlines()]
        except:
            pass
        QTimer.singleShot(0, self.addAudioCard)

    def initVideo(self):
        self.videos = None
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        video_like = base_path + '/video/video_like.txt'
        try:
            with open(video_like, 'r', encoding='utf-8') as f:
                self.videos = [line.strip() for line in f.readlines()]
        except:
            pass
        QTimer.singleShot(0, self.addVideoCard)

    def addPhotoCard(self):
        if not self.images:
            return
        image = self.images.pop(0)
        path = image.replace('\\', '/')
        if os.path.exists(path):
            self.flip_View.addImage(path)
        QTimer.singleShot(0, self.addPhotoCard)

    def updateIndex(self, index):
        count = self.flip_View.count()
        if index == 0:
            self.flip_View.setCurrentIndex(count - 2)
        elif index == count - 2:
            self.flip_View.setCurrentIndex(2)

    def addMessageCard(self):
        if not self.messages:
            return
        message = self.messages.pop(0)
        path = message.replace('\\', '/')
        self.addCard('message', path)
        QTimer.singleShot(0, self.addMessageCard)

    def addAudioCard(self):
        if not self.audios:
            return
        audio = self.audios.pop(0)
        path = audio.replace('\\', '/')
        self.addCard('audio', path)
        QTimer.singleShot(0, self.addAudioCard)

    def addVideoCard(self):
        if not self.videos:
            return
        video = self.videos.pop(0)
        path = video.replace('\\', '/')
        self.addCard('video', path)
        QTimer.singleShot(0, self.addVideoCard)

    def addCard(self, style, path):
        role_1, role_2 = '', ''
        try:
            if style == 'message':
                with open(path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                # 获取两个用户
                users = list(set([lines[i].strip().split(':')[0] for i in range(0, len(lines), 3)]))
                [role_1, role_2] = users if len(users) == 2 else users + ['']
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            audio_card_content = config.get('Settings', 'audio_card_content')
            video_card_content = config.get('Settings', 'video_card_content')
            content = {'audio': audio_card_content, 'video': video_card_content,
                       'message': f'{role_1}与{role_2}的聊天记录'}
            scroll = {'audio': self.ScrollArea_3, 'video': self.ScrollArea_4, 'message': self.ScrollArea_5}
            card = AppCard(path, content[style], style, 1)
            card.moreButton.hide()
            dict = {'audio': self.verticalLayout_4, 'video': self.verticalLayout_6, 'message': self.verticalLayout_5}
            layout = dict[style]

            # 检查最后一个组件是否是弹簧
            last_item = layout.itemAt(layout.count() - 1)
            if isinstance(last_item, QSpacerItem):
                layout.removeItem(last_item)

            layout.addWidget(card)
            if style == 'message':
                card.play.connect(lambda file=path: self.addMessageBox(file))
            else:
                card.play.connect(lambda: self.playMedia(path))

            has_bar = scroll[style].verticalScrollBar().isVisible()
            if not has_bar:
                spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                layout.addItem(spacerItem)
        except:
            pass


    def addMessageBox(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # 获取两个用户
        users = list(set([lines[i].strip().split(':')[0] for i in range(0, len(lines), 3)]))
        for i in range(0, len(lines), 3):
            nickname, message = lines[i].strip().split(':')[0], lines[i + 1]
            message = lines[i + 1].strip()
            if message:
                if nickname == users[0]:
                    message_box = messageBoxMe(message)
                    self.msgWin.verticalLayout_2.addWidget(message_box)
                    message_box = messageBoxYou(message)
                    self.msgWin.verticalLayout_3.addWidget(message_box)
                else:
                    message_box = messageBoxYou(message)
                    self.msgWin.verticalLayout_2.addWidget(message_box)
                    message_box = messageBoxMe(message)
                    self.msgWin.verticalLayout_3.addWidget(message_box)

        # 检查最后一个组件是否是弹簧
        # last_item_2 = self.msgWin.verticalLayout_2.itemAt(self.msgWin.verticalLayout_2.count() - 1)
        # last_item_3 = self.msgWin.verticalLayout_3.itemAt(self.msgWin.verticalLayout_3.count() - 1)
        # if isinstance(last_item_2, QSpacerItem):
        #     self.msgWin.verticalLayout_2.removeItem(last_item_2)
        # if isinstance(last_item_3, QSpacerItem):
        #     self.msgWin.verticalLayout_3.removeItem(last_item_3)

        # has_scroll_bar = self.msgWin.ScrollArea.verticalScrollBar().isVisible()
        # if not has_scroll_bar:
        #     spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        #     self.msgWin.verticalLayout_2.addItem(spacerItem)
        #     self.msgWin.verticalLayout_3.addItem(spacerItem)
        self.msgWin.show()

    def likeT(self, path, card, style):
        try:
            my_icon, text, file_d, file_a = '', '', '', ''
            if style == 'audio':
                config = configparser.ConfigParser()
                config.read('./config.ini', encoding='utf-8')
                base_path = config.get('Settings', 'base_path')
                audio_list = base_path + '/audio/audio_list.txt'
                audio_like = base_path + '/audio/audio_like.txt'
                (my_icon, text, file_d, file_a) = (
                    FluentIcon.HEART, 'Like', audio_like, audio_list) if card.is_liked else (
                    FluentIcon.EXPRESSIVE_INPUT_ENTRY, 'Unlike', audio_list, audio_like)
            elif style == 'video':
                config = configparser.ConfigParser()
                config.read('./config.ini', encoding='utf-8')
                base_path = config.get('Settings', 'base_path')
                video_list = base_path + '/video/video_list.txt'
                video_like = base_path + '/video/video_like.txt'
                (my_icon, text, file_d, file_a) = (
                    FluentIcon.HEART, 'Like', video_like, video_list) if card.is_liked else (
                    FluentIcon.EXPRESSIVE_INPUT_ENTRY, 'Unlike', video_list, video_like)
            elif style == 'message':
                config = configparser.ConfigParser()
                config.read('./config.ini', encoding='utf-8')
                base_path = config.get('Settings', 'base_path')
                chat_list = base_path + '/chat/chat_list.txt'
                chat_like = base_path + '/chat/chat_like.txt'
                (my_icon, text, file_d, file_a) = (
                    FluentIcon.HEART, 'Like', chat_like, chat_list) if card.is_liked else (
                    FluentIcon.EXPRESSIVE_INPUT_ENTRY, 'Unlike', chat_list, chat_like)
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
            self.updateSignal.emit()  # type: ignore
            dict = {'audio': self.verticalLayout_4, 'video': self.verticalLayout_6, 'message': self.verticalLayout_5}
            layout = dict[style]
            self.clearLayout(layout)
            if style == 'audio':
                self.initAudio()
            elif style == 'message':
                self.initChat()
            elif style == 'video':
                self.initVideo()
        except:
            pass

    def deleteT(self, path, card, style):
        dict = {'audio': self.verticalLayout_4, 'video': self.verticalLayout_6, 'message': self.verticalLayout_5}
        layout = dict[style]
        txt = ''
        if style == 'audio':
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            base_path = config.get('Settings', 'base_path')
            audio_list = base_path + '/audio/audio_list.txt'
            audio_like = base_path + '/audio/audio_like.txt'
            txt = audio_like if card.is_liked else audio_list
        elif style == 'video':
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            base_path = config.get('Settings', 'base_path')
            video_list = base_path + '/video/video_list.txt'
            video_like = base_path + '/video/video_like.txt'
            txt = video_like if card.is_liked else video_list
        elif style == 'message':
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            base_path = config.get('Settings', 'base_path')
            chat_list = base_path + '/chat/chat_list.txt'
            chat_like = base_path + '/chat/chat_like.txt'
            txt = chat_like if card.is_liked else chat_list

        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, AppCard) and widget.path == path:
                layout.removeWidget(widget)
                widget.deleteLater()
                break
        self.updateSignal.emit()  # type: ignore

        with open(txt, 'r', encoding='utf-8') as f:
            likes = f.readlines()
        with open(txt, 'w', encoding='utf-8') as f:
            for like in likes:
                if like.strip() != path:
                    f.write(like)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def playMedia(self, path):
        try:
            os.startfile(path)
        except:
            QMessageBox.warning(self, '提示', '未定位到文件，可能被移动或改名')
