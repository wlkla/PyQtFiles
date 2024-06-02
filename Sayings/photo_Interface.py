import random
from PyQt5.QtCore import QTimer

from PyQt5 import sip
from classSet import *
from photo import Ui_Form
from PyQt5.QtWidgets import QWidget, QFileDialog


class photoInterface(Ui_Form, QWidget):
    addPicture = pyqtSignal()

    def __init__(self):
        super(photoInterface, self).__init__()
        self.setupUi(self)
        self.setObjectName('photo')
        self.flow_layout = FlowLayout()
        self.scrollAreaWidgetContents.setLayout(self.flow_layout)
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        photo_list = base_path + '/photo/photo_list.txt'
        photo_like = base_path + '/photo/photo_like.txt'
        try:
            with open(photo_list, 'r', encoding='utf-8') as f:
                images_1 = [(line.strip(), 0) for line in f.readlines()]
            with open(photo_like, 'r', encoding='utf-8') as f:
                images_2 = [(line.strip(), 1) for line in f.readlines()]
            self.images = images_1 + images_2
            random.shuffle(self.images)
            self.importPhoto.clicked.connect(self.addPhoto)
            QTimer.singleShot(0, self.load_next_image)
        except:
            pass

    def load_next_image(self):
        if not self.images:
            return
        image, like_tag = self.images.pop(0)
        image = image.replace('\\', '/')
        if os.path.exists(image):
            q = QL(image, like_tag)
            q.likeSignal.connect(lambda file=image, widget=q: self.likeT(file, widget))
            q.deleteSignal.connect(lambda file=image, widget=q: self.deleteT(file, widget))
            q.zoomInSignal.connect(lambda file=image: self.zoomInT(file))
            self.flow_layout.addWidget(q)
        QTimer.singleShot(0, self.load_next_image)

    def addPhoto(self):
        files, ok = QFileDialog.getOpenFileNames(self, '添加照片', '', "Image Files (*.jpg *.png *.jpeg)")
        if files and ok:
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            base_path = config.get('Settings', 'base_path')
            photo_list = base_path + '/photo/photo_list.txt'
            photo_like = base_path + '/photo/photo_like.txt'
            with open(photo_list, 'r', encoding='utf-8') as f:
                existing_images_1 = [line.strip() for line in f.readlines()]
            with open(photo_like, 'r', encoding='utf-8') as f:
                existing_images_2 = [line.strip() for line in f.readlines()]
            existing_images = existing_images_1 + existing_images_2
            self.images = [(image.replace('\\', '/'), 0) for image in files if image not in existing_images]
            if self.images:
                with open(photo_list, 'a', encoding='utf-8') as f:
                    for image, _ in self.images:
                        f.write(image + '\n')
            QTimer.singleShot(0, self.load_next_image)

    def likeT(self, path, q):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        photo_list = base_path + '/photo/photo_list.txt'
        photo_like = base_path + '/photo/photo_like.txt'
        if q.is_liked:
            q.like_action.setIcon(FluentIcon.HEART)
            q.like_action.setText('Like')
            with open(photo_like, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            with open(photo_like, 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.strip() != path:
                        f.write(line)
            with open(photo_list, 'a', encoding='utf-8') as f:
                f.write(path + '\n')
            q.is_liked = 0
        else:
            q.like_action.setIcon(FluentIcon.EXPRESSIVE_INPUT_ENTRY)
            q.like_action.setText('UnLike')
            with open(photo_like, 'a', encoding='utf-8') as f:
                f.write(path + '\n')
            f.close()
            with open(photo_list, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            with open(photo_list, 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.strip() != path:
                        f.write(line)
            q.is_liked = 1
        try:
            q.like_action.disconnect()
        except:
            pass
        self.update()
        self.addPicture.emit()  # type: ignore

    def deleteT(self, path, q):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        photo_list = base_path + '/photo/photo_list.txt'
        photo_like = base_path + '/photo/photo_like.txt'
        txt = photo_like if q.is_liked else photo_list
        with open(txt, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(txt, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.strip() != path:
                    f.write(line)
        self.addPicture.emit()  # type: ignore

        for i in reversed(range(self.flow_layout.count())):
            widget = self.flow_layout.itemAt(i).widget()
            if widget.picture == path:
                self.flow_layout.removeWidget(widget)
                sip.delete(widget)
                break

    def zoomInT(self, path):
        os.startfile(path)
