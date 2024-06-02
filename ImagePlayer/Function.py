import os
import json
import webbrowser
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt, QPoint, QRect, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QFileDialog, QLabel, QMessageBox, QListWidget, QListWidgetItem, QDialog, QVBoxLayout, \
    QProgressDialog, QApplication
from Entrance import mainwindow
from Feedback import FeedbackDialog


class Controller:
    def __init__(self):
        super().__init__()
        self.InitUi()
        self.InitParameter()
        self.InitFunction()

    def InitUi(self):
        self.ui = mainwindow()
        self.ui.show()
        self.ui.horizontalSlider.hide()
        self.ui.resized.connect(self.handleResizeEvent)
        self.ui.esc.connect(self.ui.showNormal)

    def InitParameter(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.play)
        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.Carousel)
        self.image_index = 0
        self.image = []
        self.labels = []

    def InitFunction(self):
        self.ui.pushButton.clicked.connect(self.selectFolder)
        self.ui.pushButton_2.clicked.connect(self.timerStart)
        self.ui.pushButton_3.clicked.connect(self.clear)
        self.ui.pushButton_4.clicked.connect(self.history)
        self.ui.pushButton_5.clicked.connect(self.feedback)
        self.ui.pushButton_6.clicked.connect(self.seecode)
        self.ui.pushButton_7.clicked.connect(self.Fullscreen)
        self.ui.horizontalSlider.valueChanged.connect(self.play_timer.stop)
        self.animation_up = QPropertyAnimation(self.ui.widget_4, b"geometry")
        self.animation_down = QPropertyAnimation(self.ui.widget_4, b"geometry")
        self.ui.dockWidget.enterEvent = self.dockWidgetEnterEvent
        self.ui.dockWidget.leaveEvent = self.dockWidgetLeaveEvent

    def selectFolder(self):
        folder = QFileDialog.getExistingDirectory(self.ui, '选择文件夹', 'E:\Picture Files')
        if folder:
            self.ui.lineEdit.setText(folder)
            self.image_folder = folder
            self.image = [os.path.join(self.image_folder, file) for file in os.listdir(self.image_folder) if
                          file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
            self.timer.start(2)

            history = []
            history_file = 'history.json'
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    history = json.load(f)
            history.append(folder)
            with open(history_file, 'w') as f:
                json.dump(history, f)

    def play(self):
        progress_dialog = QProgressDialog("正在加载图片...", "取消", 0, len(self.image), self.ui)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()

        for self.image_index in range(len(self.image)):
            if progress_dialog.wasCanceled():
                break

            if self.ui.isFullScreen():
                height = 1050
            else:
                height = int((self.ui.height() - 200))
            label = QLabel()
            label.setScaledContents(True)
            picture = QPixmap(self.image[self.image_index])
            label.setPixmap(picture)
            label.setStyleSheet("QLabel{\n"
                                "border:15px solid white;\n"
                                "border-radius:10px;\n"
                                "}\n"
                                "QLabel:hover{\n"
                                "border:15px solid black;\n"
                                "border-radius:10px;\n"
                                "}")
            label.setFixedSize(int(picture.width() * (height / picture.height())), height)
            self.ui.horizontalLayout_5.addWidget(label)
            self.labels.append(label)

            progress_dialog.setValue(self.image_index + 1)
            QApplication.processEvents()

        if self.image_index == len(self.image) - 1:
            QMessageBox.information(self.ui, '完成', '图片读取完成！')
            self.timer.stop()

    def handleResizeEvent(self):
        if self.ui.isFullScreen():
            height = 1050
            self.ui.widget.hide()
            self.ui.widget_4.move(0, 0)
            self.ui.dockWidget.setFloating(True)
            self.ui.dockWidget.setFixedSize(350, 51)
            self.ui.dockWidget.setWindowTitle('功能区')
        else:
            self.ui.widget.show()
            self.ui.dockWidget.setFixedHeight(84)
            self.ui.dockWidget.setMinimumWidth(0)
            self.ui.dockWidget.setWindowTitle('')
            self.ui.dockWidget.setMaximumWidth(16777215)
            self.ui.dockWidget.setFloating(False)
            dock_width = self.ui.dockWidget.width()
            widget_width = self.ui.widget_4.width()
            new_x = max((dock_width - widget_width) // 2, 0)
            height = int((self.ui.height() - 200))
            self.ui.widget_4.setGeometry(new_x, 64, widget_width, 51)

        for label in self.labels:
            picture = label.pixmap()
            label.setFixedSize(int(picture.width() * (height / picture.height())), height)

    def timerStart(self):
        if self.play_timer.isActive():
            self.play_timer.stop()
            self.ui.horizontalSlider.hide()
        else:
            self.ui.horizontalSlider.show()
            self.play_timer.start(3)

    def Carousel(self):
        bar = self.ui.scrollArea.horizontalScrollBar()
        bar.setSliderPosition(bar.sliderPosition() + int(self.ui.horizontalSlider.value() * 0.1) + 1)

    def clear(self):
        self.ui.lineEdit.clear()
        for label in self.labels:
            self.ui.horizontalLayout_5.removeWidget(label)
            label.deleteLater()
        self.labels.clear()
        self.image.clear()
        self.image_index = 0

    def history(self):
        # 从文件中读取历史记录
        history = []
        history_file = 'history.json'
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)

        # 创建一个新的窗口来显示历史记录
        dialog = QDialog(self.ui)
        dialog.setWindowTitle('历史记录')
        layout = QVBoxLayout(dialog)

        list_widget = QListWidget(dialog)
        for folder in history:
            item = QListWidgetItem(folder)
            list_widget.addItem(item)
        list_widget.itemDoubleClicked.connect(self.useFolder)

        layout.addWidget(list_widget)
        dialog.setLayout(layout)
        dialog.exec_()

    def useFolder(self, item):
        self.clear()
        folder = item.text()
        self.ui.lineEdit.setText(folder)
        self.image_folder = folder
        self.image = [os.path.join(self.image_folder, file) for file in os.listdir(self.image_folder) if
                      file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
        self.timer.start(2)
        item.listWidget().window().close()

    def feedback(self):
        dialog = FeedbackDialog(self.ui)
        dialog.exec_()

    def seecode(self):
        webbrowser.open('https://github.com/wlkla/pictureplayer/tree/main')

    def dockWidgetEnterEvent(self, event):
        self.moveWidget4FromOutside()

    def dockWidgetLeaveEvent(self, event):
        self.moveWidget4ToOutside()

    def moveWidget4FromOutside(self):
        x = self.ui.widget_4.x()
        width = self.ui.widget_4.width()
        target_rect = QRect(x, 0, width, 51)

        self.animation_up.setStartValue(QRect(x, 64, width, 51))
        self.animation_up.setEndValue(target_rect)
        self.animation_up.setDuration(500)
        self.animation_up.setEasingCurve(QEasingCurve.OutCubic)
        self.animation_up.start()

    def moveWidget4ToOutside(self):
        x = self.ui.widget_4.x()
        width = self.ui.widget_4.width()
        target_rect = QRect(x, 64, width, 51)

        self.animation_down.setStartValue(QRect(x, 0, width, 51))
        self.animation_down.setEndValue(target_rect)
        self.animation_down.setDuration(500)
        self.animation_down.setEasingCurve(QEasingCurve.OutCubic)
        self.animation_down.start()

    def Fullscreen(self):
        if self.ui.isFullScreen():
            self.ui.showNormal()
        else:
            self.ui.showFullScreen()
