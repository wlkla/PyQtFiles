import configparser
import re
import random

from qfluentwidgets import FlyoutView

from classSet import *
from chat import Ui_Form
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QMessageBox


class chatInterface(Ui_Form, QWidget):
    minWin = pyqtSignal()
    norWin = pyqtSignal()
    addChat = pyqtSignal()

    def __init__(self):
        super(chatInterface, self).__init__()
        self.setupUi(self)
        self.setObjectName('chat')
        self.listen_clipboard = False
        self.msgshowWin = messageWindow()
        self.msgWin = newmsgWin()  # type: ignore
        self.msgWin.fileSaved.connect(self.updateFileList)  # type: ignore
        self.importMessage.clicked.connect(self.getNewMessage)
        self.button1.clicked.connect(self.showFlyout)
        self.initChat()

    def initChat(self):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        chat_list = base_path + '/chat/chat_list.txt'
        chat_like = base_path + '/chat/chat_like.txt'
        try:
            with open(chat_list, 'r', encoding='utf-8') as f:
                chat_1 = [(line.strip(), 0) for line in f.readlines()]
            with open(chat_like, 'r', encoding='utf-8') as f:
                chat_2 = [(line.strip(), 1) for line in f.readlines()]
            self.chat = chat_1 + chat_2
            random.shuffle(self.chat)
            QTimer.singleShot(0, self.addMessageCard)
        except:
            pass

    def updateMessageCardIcon(self):
        for i in range(self.verticalLayout_2.count()):
            widget=self.verticalLayout_2.itemAt(i).widget()
            if isinstance(widget, AppCard):
                widget.updateIconOrText('message')

    def getNewMessage(self):
        self.clearLayout(self.msgWin.verticalLayout_2)
        print('hhh')
        self.minWin.emit()  # type: ignore
        print(1)
        clipboard = QApplication.clipboard()
        self.listen_clipboard = True

        def on_clipboard_changed():
            if not self.listen_clipboard:
                return
            text = clipboard.text()
            lines = text.split('\n')
            if len(lines) % 3 == 0 and all(
                    re.match(r'^.*:$', lines[i]) and lines[i + 2] == '' for i in range(0, len(lines), 3)):
                self.norWin.emit()  # type: ignore
                self.msgWin.text = text
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
                last_item_2 = self.msgWin.verticalLayout_2.itemAt(self.msgWin.verticalLayout_2.count() - 1)
                last_item_3 = self.msgWin.verticalLayout_3.itemAt(self.msgWin.verticalLayout_3.count() - 1)
                if isinstance(last_item_2, QSpacerItem):
                    self.msgWin.verticalLayout_2.removeItem(last_item_2)
                if isinstance(last_item_3, QSpacerItem):
                    self.msgWin.verticalLayout_3.removeItem(last_item_3)

                has_scroll_bar = self.msgWin.ScrollArea.verticalScrollBar().isVisible()
                if not has_scroll_bar:
                    spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                    self.msgWin.verticalLayout_2.addItem(spacerItem)
                    self.msgWin.verticalLayout_3.addItem(spacerItem)
                self.msgWin.show()
                self.listen_clipboard = False

        clipboard.dataChanged.connect(on_clipboard_changed)  # type: ignore

    def updateFileList(self, file_path):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        chat_list = base_path + '/chat/chat_list.txt'
        with open(chat_list, 'a', encoding='utf-8') as f:
            f.write(file_path + '\n')
        self.chat = [(file_path, 0)]
        QTimer.singleShot(0, self.addMessageCard)

    def addMessageCard(self):
        if not self.chat:
            return
        chat, like_tag = self.chat.pop(0)
        path = chat.replace('\\', '/')
        try:
            with open(path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            # 获取两个用户
            users = list(set([lines[i].strip().split(':')[0] for i in range(0, len(lines), 3)]))
            [role_1, role_2] = users if len(users) == 2 else users + ['']
            card = AppCard(path, f'{role_1}与{role_2}的聊天记录', 'message', like_tag, self)
            card.likeSignal.connect(lambda file=path, widget=card: self.likeT(file, widget))
            card.deleteSignal.connect(lambda file=path, widget=card: self.deleteT(file, widget))
            # 检查最后一个组件是否是弹簧
            last_item = self.verticalLayout_2.itemAt(self.verticalLayout_2.count() - 1)
            if isinstance(last_item, QSpacerItem):
                self.verticalLayout_2.removeItem(last_item)
            self.verticalLayout_2.addWidget(card, alignment=Qt.AlignTop)
            card.play.connect(lambda: self.addMessageBox(path))
            has_bar = self.ScrollArea.verticalScrollBar().isVisible()
            if not has_bar:
                spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                self.verticalLayout_2.addItem(spacerItem)
        except:
            pass
        QTimer.singleShot(0, self.addMessageCard)

    def addMessageBox(self, path):
        try:
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
                        self.msgshowWin.verticalLayout_2.addWidget(message_box)
                        message_box = messageBoxYou(message)
                        self.msgshowWin.verticalLayout_3.addWidget(message_box)
                    else:
                        message_box = messageBoxYou(message)
                        self.msgshowWin.verticalLayout_2.addWidget(message_box)
                        message_box = messageBoxMe(message)
                        self.msgshowWin.verticalLayout_3.addWidget(message_box)

            # 检查最后一个组件是否是弹簧
            # last_item_2 = self.msgshowWin.verticalLayout_2.itemAt(self.msgshowWin.verticalLayout_2.count() - 1)
            # last_item_3 = self.msgshowWin.verticalLayout_3.itemAt(self.msgshowWin.verticalLayout_3.count() - 1)
            # if isinstance(last_item_2, QSpacerItem):
            #     self.msgshowWin.verticalLayout_2.removeItem(last_item_2)
            # if isinstance(last_item_3, QSpacerItem):
            #     self.msgshowWin.verticalLayout_3.removeItem(last_item_3)
            #
            # has_scroll_bar = self.msgshowWin.ScrollArea.verticalScrollBar().isVisible()
            # if not has_scroll_bar:
            #     spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            #     self.msgshowWin.verticalLayout_2.addItem(spacerItem)
            #     self.msgshowWin.verticalLayout_3.addItem(spacerItem)
            self.msgshowWin.show()
        except:
            QMessageBox.warning(self, '错误', '未定位到文件，可能被移动或改名')

    def likeT(self, path, card):
        try:
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            base_path = config.get('Settings', 'base_path')
            chat_list = base_path + '/chat/chat_list.txt'
            chat_like = base_path + '/chat/chat_like.txt'
            (my_icon, text, file_d, file_a) = (FluentIcon.HEART, 'Like', chat_like, chat_list) if card.is_liked else (
                FluentIcon.EXPRESSIVE_INPUT_ENTRY, 'Unlike', chat_list, chat_like)
            card.like_action.setIcon(my_icon)
            card.like_action.setText(text)
            with open(file_d, 'r', encoding='utf-8') as f:
                likes = f.readlines()
            with open(file_d, 'w', encoding='utf-8') as f:
                for like in likes:
                    like = like.strip()
                    if like != path:
                        f.write(like)
            with open(file_a, 'a', encoding='utf-8') as f:
                f.write(path + '\n')
            card.is_liked = 1 - card.is_liked
            try:
                card.like_action.disconnect()
            except:
                pass
            self.update()
            self.addChat.emit()  # type: ignore
        except:
            pass

    def deleteT(self, path, card):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        chat_list = base_path + '/chat/chat_list.txt'
        chat_like = base_path + '/chat/chat_like.txt'
        txt = chat_like if card.is_liked else chat_list
        with open(txt, 'r', encoding='utf-8') as f:
            likes = f.readlines()
        with open(txt, 'w', encoding='utf-8') as f:
            for like in likes:
                if like.strip() != path:
                    f.write(like)
        self.addChat.emit()  # type: ignore

        for i in reversed(range(self.verticalLayout_2.count())):
            widget = self.verticalLayout_2.itemAt(i).widget()
            if isinstance(widget, AppCard) and widget.path == path:
                self.verticalLayout_2.removeWidget(widget)
                widget.deleteLater()
                break

    def showFlyout(self):
        view = FlyoutView(
            image='./image/introduction.gif',
            title='支持微信消息导入',
            content="打开微信，选择想要保存的聊天记录，点击 ctrl+c 即可，按 shift 键可切换视图。\n注意：每条消息中不可存在换行符，否则无法识别。",
            isClosable=True
        )
        view.widgetLayout.insertSpacing(1, 5)
        view.widgetLayout.addSpacing(5)
        w = Flyout.make(view, self.button1, self)
        view.closed.connect(w.close)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            # 如果子项是一个widget
            if child.widget():
                child.widget().deleteLater()

