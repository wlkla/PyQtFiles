import os
import random

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QFileDialog, QLabel, QWidget, QHBoxLayout, QScrollArea, QVBoxLayout

from Entrance import mainwindow


class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()

    clicked = pyqtSignal()


class Controller:
    def __init__(self):
        super().__init__()
        self.InitUi()
        self.InitParameter()
        self.InitLayout()
        self.InitFunction()

    def InitParameter(self):
        self.image_folder = None
        self.image_files_to_be_sort = None
        self.image_files_sorted = {}
        self.index = None
        self.image_pair = []
        self.picture_1 = None
        self.sorted_pictures = []
        self.picture_2 = None

    def InitUi(self):
        self.ui = mainwindow()
        self.ui.show()
        self.ui.scrollArea.hide()
        self.ui.horizontalLayout_2 = QHBoxLayout()
        self.ui.scrollArea_1 = QScrollArea(self.ui.widget)
        self.ui.scrollArea_1.setStyleSheet("border:none;")
        self.ui.scrollArea_1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.scrollArea_1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.scrollArea_1.setWidgetResizable(True)
        self.ui.scrollAreaWidgetContents_1 = QWidget()
        self.ui.horizontalLayout_3 = QHBoxLayout(self.ui.scrollAreaWidgetContents_1)
        self.ui.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.ui.scrollArea_1.setWidget(self.ui.scrollAreaWidgetContents_1)
        self.ui.Picture_1 = ClickableLabel(self.ui.scrollAreaWidgetContents_1)
        self.ui.Picture_1.setFixedSize(int((self.ui.width() - 30) / 2), int((self.ui.height() - 350) / 2))
        self.ui.Picture_1.setCursor(QCursor(Qt.PointingHandCursor))
        self.ui.Picture_1.setStyleSheet("QLabel{\n"
                                        "border:15px solid white;\n"
                                        "border-radius:10px;\n"
                                        "}\n"
                                        "QLabel:hover{\n"
                                        "border:15px solid black;\n"
                                        "border-radius:10px;\n"
                                        "}")
        self.ui.horizontalLayout_3.addWidget(self.ui.Picture_1)
        self.ui.scrollArea_2 = QScrollArea()
        self.ui.scrollArea_2.setStyleSheet("border:none;")
        self.ui.scrollArea_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.scrollArea_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.scrollArea_2.setWidgetResizable(True)
        self.ui.scrollAreaWidgetContents_2 = QWidget()
        self.ui.horizontalLayout_5 = QHBoxLayout(self.ui.scrollAreaWidgetContents_2)
        self.ui.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.ui.scrollArea_2.setWidget(self.ui.scrollAreaWidgetContents_2)
        self.ui.Picture_2 = ClickableLabel(self.ui.scrollAreaWidgetContents_2)
        self.ui.Picture_2.setFixedSize(int((self.ui.width() - 30) / 2), int((self.ui.height() - 350) / 2))
        self.ui.Picture_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.ui.Picture_2.setStyleSheet("QLabel{\n"
                                        "border:15px solid white;\n"
                                        "border-radius:10px;\n"
                                        "}\n"
                                        "QLabel:hover{\n"
                                        "border:15px solid black;\n"
                                        "border-radius:10px;\n"
                                        "}")
        self.ui.horizontalLayout_5.addWidget(self.ui.Picture_2)

    def InitLayout(self):
        if self.ui.comboBox.currentIndex() == 0:
            horizontalLayout = QHBoxLayout()
            horizontalLayout.setSpacing(0)
            horizontalLayout.addWidget(self.ui.scrollArea_1)
            horizontalLayout.addWidget(self.ui.scrollArea_2)
            self.ui.horizontalLayout_4.addLayout(horizontalLayout)
        else:
            verticalLayout = QVBoxLayout()
            verticalLayout.setSpacing(0)
            verticalLayout.addWidget(self.ui.scrollArea_1)
            verticalLayout.addWidget(self.ui.scrollArea_2)
            self.ui.horizontalLayout_4.addLayout(verticalLayout)

    def InitFunction(self):
        self.ui.Folder.clicked.connect(self.load_folder_images)
        self.ui.comboBox.currentIndexChanged.connect(self.InitLayout)
        self.ui.radioButton.clicked.connect(self.show_sorted_pictures)
        self.ui.Picture_1.clicked.connect(lambda: self.rank_picture(self.picture_1))
        self.ui.Picture_2.clicked.connect(lambda: self.rank_picture(self.picture_2))

    def load_folder_images(self):  # 获取文件夹图片
        folder = QFileDialog.getExistingDirectory(self.ui, '选择文件夹', 'E:\Picture Files')
        if folder:
            self.ui.Folder.setText(folder)
            self.image_folder = folder
            self.image_files_to_be_sort = [os.path.join(self.image_folder, file) for file in
                                           os.listdir(self.image_folder) if
                                           file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
            for idx, file_path in enumerate(self.image_files_to_be_sort):
                _, file_extension = os.path.splitext(os.path.basename(file_path))
                ex_file = ''
                for i in range(5):
                    ex_file += random.choice('abcdefghijklmnopqrstuvwxyz')
                new_name = f'{ex_file}_{idx + 1}{file_extension}'
                new_path = os.path.join(self.image_folder, new_name)
                os.rename(file_path, new_path)
                self.image_files_to_be_sort[idx] = new_path
            for i in range(len(self.image_files_to_be_sort)):
                for j in range(i + 1, len(self.image_files_to_be_sort)):
                    self.image_pair.append([self.image_files_to_be_sort[i], self.image_files_to_be_sort[j]])
            self.image_files_sorted = {image_path: 0 for image_path in self.image_files_to_be_sort}
            self.sort_picture_pair()

    def load_picture_pair(self, picture_pair):  # 将图片组显示在窗口中
        if self.ui.comboBox.currentIndex() == 0:
            width = int((self.ui.width() - 30) / 2)
            self.ui.Picture_1.setFixedSize(width, int(QPixmap(picture_pair[0]).height() * (
                    width / QPixmap(picture_pair[0]).width())))
            self.ui.Picture_2.setFixedSize(width, int(QPixmap(picture_pair[1]).height() * (
                    width / QPixmap(picture_pair[1]).width())))
        else:
            height = int((self.ui.height() - 350) / 2)
            self.ui.Picture_1.setFixedSize(
                int(QPixmap(picture_pair[0]).width() * (height / QPixmap(picture_pair[0]).height())),
                height)
            self.ui.Picture_2.setFixedSize(
                int(QPixmap(picture_pair[1]).width() * (height / QPixmap(picture_pair[1]).height())),
                height)
        self.ui.Picture_1.setPixmap(QPixmap(picture_pair[0]))
        self.ui.Picture_2.setPixmap(QPixmap(picture_pair[1]))
        self.ui.Picture_1.setScaledContents(True)
        self.ui.Picture_2.setScaledContents(True)
        self.picture_1 = picture_pair[0]
        self.picture_2 = picture_pair[1]
        self.image_pair.pop(self.index)

    def sort_picture_pair(self):  # 对两张图片进行排序
        length = len(self.image_pair)
        self.ui.label_2.setText(str(length))
        if length == 0:
            self.ui.widget.hide()
            self.ui.scrollArea_3.hide()
            self.ui.scrollArea.show()
            self.ui.label.setText("所有图片均已排序，排序如下：")
            sorted_pictures = sorted(self.image_files_sorted.items(), key=lambda x: x[1], reverse=True)
            for i in sorted_pictures:
                picture = QPixmap(i[0])
                width = int((self.ui.width() - 30))
                pictureLabel = QLabel(self.ui.scrollAreaWidgetContents)
                pictureLabel.setFixedSize(width, int(picture.height() * (width / picture.width())))
                pictureLabel.setPixmap(picture)
                pictureLabel.setScaledContents(True)
                pictureLabel.setStyleSheet("QLabel{\n"
                                           "border:15px solid white;\n"
                                           "border-radius:10px;\n"
                                           "}"
                                           "QLabel:hover{\n"
                                           "border:15px solid black;\n"
                                           "border-radius:10px;\n"
                                           "}")
                self.ui.verticalLayout_3.addWidget(pictureLabel)
            self.rename_pictures(sorted_pictures)
        else:
            self.index = random.randint(0, length - 1)
            self.load_picture_pair(self.image_pair[self.index])

    def display_picture_rank(self, sorted_pictures):  # 显示当前排名
        for i in reversed(range(self.ui.horizontalLayout_6.count())):
            self.ui.horizontalLayout_6.itemAt(i).widget().setParent(None)
        for picture in sorted_pictures:
            dock = QLabel(self.ui.scrollArea_3)
            dock.setStyleSheet("QLabel{\n"
                               "border:4px solid white;\n"
                               "border-radius:10px;\n"
                               "}\n"
                               "QLabel:hover{\n"
                               "border:4px solid black;\n"
                               "border-radius:10px;\n"
                               "}")
            dock.setFixedSize(int(QPixmap(picture).width() * (58 / QPixmap(picture).height())), 58)
            dock.setPixmap(QPixmap(picture))
            dock.setScaledContents(True)
            self.ui.horizontalLayout_6.addWidget(dock)

    def show_sorted_pictures(self):  # 显示已排序照片
        if not self.ui.radioButton.isChecked():
            self.ui.scrollArea_3.show()
            self.display_picture_rank(self.sorted_pictures)
        else:
            self.ui.scrollArea_3.hide()

    def rank_picture(self, picture):  # 对所有照片计票
        self.image_files_sorted[picture] += 1
        non_zero_like = {k: v for k, v in self.image_files_sorted.items() if v != 0}
        sorted_pictures = sorted(non_zero_like.items(), key=lambda x: x[1], reverse=True)
        self.sorted_pictures = [k for k, v in sorted_pictures]
        self.show_sorted_pictures()
        self.sort_picture_pair()

    def rename_pictures(self, picture_dict):  # 重命名图片
        for i, (picture_path, _) in enumerate(picture_dict):
            directory = os.path.dirname(picture_path)
            extension = os.path.splitext(picture_path)[1]
            new_picture_path = os.path.join(directory, str(i + 1).zfill(3) + extension)
            os.rename(picture_path, new_picture_path)
