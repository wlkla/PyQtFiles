from video import Ui_Form
import random
from classSet import *
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox

from PyQt5.QtCore import pyqtSignal, QTimer


class videoInterface(Ui_Form, QWidget):
    addVideo = pyqtSignal()

    def __init__(self):
        super(videoInterface, self).__init__()
        self.setupUi(self)
        self.setObjectName('video')
        self.initVideo()
        self.importVideo.clicked.connect(self.addnewVideo)  # type: ignore

    def initVideo(self):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        video_list = base_path + '/video/video_list.txt'
        video_like = base_path + '/video/video_like.txt'
        try:
            with open(video_list, 'r', encoding='utf-8') as f:
                video_1 = [(line.strip(), 0) for line in f.readlines()]
            with open(video_like, 'r', encoding='utf-8') as f:
                video_2 = [(line.strip(), 1) for line in f.readlines()]
            self.videos = video_1 + video_2
            random.shuffle(self.videos)
            QTimer.singleShot(0, self.addVideoCard)
        except:
            pass

    def updateVideoCardIcon(self):
        for i in range(self.verticalLayout_2.count()):
            widget = self.verticalLayout_2.itemAt(i).widget()
            if isinstance(widget, AppCard):
                widget.updateIconOrText('video')

    def addVideoCard(self):
        if not self.videos:
            return
        video, like_tag = self.videos.pop(0)
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        video_card_content = config.get('Settings', 'video_card_content')
        path = video.replace('\\', '/')
        card = AppCard(path, video_card_content, 'video', like_tag, self)
        card.likeSignal.connect(lambda file=path, widget=card: self.likeT(file, widget))
        card.deleteSignal.connect(lambda file=path, widget=card: self.deleteT(file, widget))

        # 检查最后一个组件是否是弹簧
        last_item = self.verticalLayout_2.itemAt(self.verticalLayout_2.count() - 1)
        if isinstance(last_item, QSpacerItem):
            self.verticalLayout_2.removeItem(last_item)

        self.verticalLayout_2.addWidget(card, alignment=Qt.AlignTop)
        card.play.connect(lambda: self.playVideo(path))

        has_bar = self.ScrollArea.verticalScrollBar().isVisible()
        if not has_bar:
            spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.verticalLayout_2.addItem(spacerItem)

        QTimer.singleShot(0, self.addVideoCard)

    def addnewVideo(self):
        files, ok = QFileDialog.getOpenFileNames(self, '添加视频', '', "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv)")
        if files and ok:
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            base_path = config.get('Settings', 'base_path')
            video_list = base_path + '/video/video_list.txt'
            video_like = base_path + '/video/video_like.txt'
            with open(video_list, 'r', encoding='utf-8') as f:
                existing_video_1 = [line.strip() for line in f.readlines()]
            with open(video_like, 'r', encoding='utf-8') as f:
                existing_video_2 = [line.strip() for line in f.readlines()]
            existing_videos = existing_video_1 + existing_video_2
            self.videos = [(video.replace('\\', '/'), 0) for video in files if video not in existing_videos]
            if self.videos:
                with open(video_list, 'a', encoding='utf-8') as f:
                    for video, _ in self.videos:
                        f.write(video + '\n')
            QTimer.singleShot(0, self.addVideoCard)

    def likeT(self, path, card):
        try:
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            base_path = config.get('Settings', 'base_path')
            video_list = base_path + '/video/video_list.txt'
            video_like = base_path + '/video/video_like.txt'
            (my_icon, text, file_d, file_a) = (
                FluentIcon.HEART, 'Like', video_like, video_list) if card.is_liked else (
                FluentIcon.EXPRESSIVE_INPUT_ENTRY, 'Unlike', video_list, video_like)

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
            self.addVideo.emit()  # type: ignore
        except:
            pass

    def deleteT(self, path, card):
        for i in reversed(range(self.verticalLayout_2.count())):
            widget = self.verticalLayout_2.itemAt(i).widget()
            if isinstance(widget, AppCard) and widget.path == path:
                self.verticalLayout_2.removeWidget(widget)
                widget.deleteLater()
                break

        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        video_list = base_path + '/video/video_list.txt'
        video_like = base_path + '/video/video_like.txt'
        txt = video_like if card.is_liked else video_list
        with open(txt, 'r', encoding='utf-8') as f:
            likes = f.readlines()
        with open(txt, 'w', encoding='utf-8') as f:
            for like in likes:
                if like.strip() != path:
                    f.write(like)
        self.addVideo.emit()  # type: ignore

    def playVideo(self, path):
        try:
            os.startfile(path)
        except:
            QMessageBox.warning(self, '提示', '未定位到文件，可能被移动或改名')
