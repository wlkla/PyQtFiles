import os
import re
import sys
import json
import time
import plyer
import shutil
import win32api
import tempfile
import winerror
import threading
import win32event
import resource_rc
from PyQt5.QtGui import QIcon, QPixmap
from watchdog.observers import Observer
from winotify import Notification, audio
from watchdog.events import FileSystemEventHandler
from PyQt5.QtCore import QDateTime, Qt, QTimer, QObject, pyqtSignal, QRect, QPropertyAnimation, QEasingCurve, QPoint, \
    QCoreApplication
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QListWidget, QFileDialog, QTextEdit, QSystemTrayIcon, QMenu, QAction, QLineEdit, QLabel,
                             QComboBox, QMessageBox, QSpinBox)

# 设置文件夹默认保存位置
default_path = os.path.join(os.environ['APPDATA'], 'FolderMonitor')
settings_file = os.path.join(default_path, "settings.json")
animationList = [("QEasingCurve.InOutExpo", QEasingCurve.InOutExpo),
                 ("QEasingCurve.InExpo", QEasingCurve.InExpo),
                 ("QEasingCurve.OutExpo", QEasingCurve.OutExpo),
                 ("QEasingCurve.InOutCirc", QEasingCurve.InOutCirc),
                 ("QEasingCurve.InCirc", QEasingCurve.InCirc),
                 ("QEasingCurve.OutCirc", QEasingCurve.OutCirc),
                 ("QEasingCurve.InOutSine", QEasingCurve.InOutSine),
                 ("QEasingCurve.InSine", QEasingCurve.InSine),
                 ("QEasingCurve.OutSine", QEasingCurve.OutSine),
                 ("QEasingCurve.InOutQuint", QEasingCurve.InOutQuint),
                 ("QEasingCurve.InQuint", QEasingCurve.InQuint),
                 ("QEasingCurve.OutQuint", QEasingCurve.OutQuint),
                 ("QEasingCurve.InOutQuart", QEasingCurve.InOutQuart),
                 ("QEasingCurve.InQuart", QEasingCurve.InQuart),
                 ("QEasingCurve.OutQuart", QEasingCurve.OutQuart),
                 ("QEasingCurve.InOutCubic", QEasingCurve.InOutCubic),
                 ("QEasingCurve.InCubic", QEasingCurve.InCubic),
                 ("QEasingCurve.OutCubic", QEasingCurve.OutCubic),
                 ("QEasingCurve.InOutQuad", QEasingCurve.InOutQuad),
                 ("QEasingCurve.InQuad", QEasingCurve.InQuad),
                 ("QEasingCurve.OutQuad", QEasingCurve.OutQuad)]
default_qss = '''
/*软件中提供以下图标/图片：01.png、02.png、03.png、04.png、05.png、06.png、07.png、08.png、09.png、10.png、add.png、delete.png、export.png、clear.png、monitor.png*/
/*使用方式为：background-image/border-image: url(:/img/xxx.png);*/

#addButton {
    color: white;
    border: none;
    padding: 10px 0;
    border-radius: 10px;
    image: url(:/img/add.png);
    background-color: #4CAF50;
}

#adjustButton {
    color: white;
    border: none;
    padding: 7px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    background-color: #4CAF50;
}

#animationtypeCombo {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#animationtypeLabel {
    color: #333333;
    font: 12pt "方正姚体";
}

#animationLabel {
    color: #333333;
    font: 12pt "方正姚体";
}

#animationX {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#animationY {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#applyButton {
    color: white;
    border: none;
    padding: 15px;
    border-radius: 10px;
    font: 10pt "方正姚体";
    background-color: #4CAF50;
}

#app_nameLabel {
    color: #333333;
    font: 12pt "方正姚体";
}

#app_nameX {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#app_nameY {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#cancelButton {
    color: white;
    border: none;
    padding: 7px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    background-color: red;
}

#clearButton {
    border: none;
    padding: 10px 0;
    border-radius: 10px;
    background-color: red;
    image: url(:/img/clear.png);
}

#closebuttonLabel {
    color: #333333;
    font: 12pt "方正姚体";
}

#closebuttonX {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#closebuttonY {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#doubleclickCombo {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#doubleclickLabel {
    color: #333333;
    font: 12pt "方正姚体";
}

#exportButton {
    border: none;
    padding: 10px 0;
    border-radius: 10px;
    image: url(:/img/export.png);
    background-color: #4CAF50;
}

#folderList {
    color: white;
    padding: 10px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-image: url(:/img/08.png);
}

#iconLabel {
    color: #333333;
    font: 12pt "方正姚体";
}

#iconX {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#iconY {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#icon_2Label {
    color: #333333;
    font: 12pt "方正姚体";
}

#icon_2X {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#icon_2Y {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#logText {
    color: white;
    padding: 10px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-image: url(:/img/08.png);
}

#mainWindow {
    background-color: #f0f0f0;
}

#messagesizeLabel {
    color: #333333;
    font: 12pt "方正姚体";
}

#messagesizeWidth {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#messagesizeHeight {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#messageLabel {
    color: #333333;
    font: 12pt "方正姚体";
}

#messageX {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#messageY {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#notificationCombo {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#notificationLabel {
    color: #333333;
    font: 12pt "方正姚体";
}

#qssCombo {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#qssEdit {
    color: white;
    padding: 10px;
    border-radius: 10px;
    font: 13pt "方正姚体";
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-image: url(:/img/05.png);
}

#qssLabel {
    padding: 5px 0;
    color: #333333;
    font: 12pt "方正姚体";
}

#removeButton {
    color: white;
    border: none;
    padding: 10px 0;
    border-radius: 10px;
    background-color: red;
    image: url(:/img/delete.png);
}

#screensizeHeight {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#screensizeLabel {
    color: #333333;
    font: 12pt "方正姚体";
}

#screensizeWidth {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#searchBar {
    padding: 5px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#singleclickCombo {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#singleclickLabel {
    color: #333333;
    font: 12pt "方正姚体";
}


#startupCombo {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#startupLabel {
    color: #333333;
    font: 12pt "方正姚体";
}

#storageButton {
    color: white;
    border: none;
    padding: 7px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    background-color: #4CAF50;
}

#storageLabel {
    color: #333333;
    font: 12pt "方正姚体";
}

#storageLine {
    color: gray;
    padding: 5px 15px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#tabWidget {
    background-color: #ffffff;
    border: 2px solid black;
}

#testButton{
    color: white;
    border: none;
    max-width: 80px;
    padding: 7px 0;
    border-radius: 10px;
    font: 12pt "方正姚体";
    background-color: #4CAF50;
}

#titleLabel {
    color: #333333;
    font: 12pt "方正姚体";
}

#titleX {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

#titleY {
    color: gray;
    padding: 5px 20px;
    border-radius: 10px;
    font: 12pt "方正姚体";
    border: 1px solid #cccccc;
}

QListWidget::Item {
    padding-top:4px;
    padding-bottom:4px;
}

QListWidget::Item:hover {
    color: black;
}

QListWidget::item:selected {
    background: rgba(159, 237, 249, 0.7);
}

QListWidget::item:selected:!active {
    background: rgba(159, 237, 249, 0.2);
}

QTabWidget::pane {
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
    border: 1px solid #C2C7CB;
    background: white;
}

QTabBar::tab {
    margin-right: 2px;
    background: white;
    font: 13pt "方正姚体";
    border: 1px solid #C4C4C3;
    border-bottom-color: #C2C7CB;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    min-width: 12ex;
    min-height: 6ex;
}

QTabBar::tab:!selected {
    color: gray;
    margin-top: 2px;
}

QTabBar::tab:selected {
    background: white;
    border-color: #9B9B9B;
    border-bottom-color: white;
}

QTabBar::tab:hover {
    margin-top: 0;
}
'''


def create_default_storage():
    if not os.path.exists(default_path):
        os.makedirs(default_path)
    return default_path


def open_folder(item):
    os.startfile(item.text())


class CustomListWidget(QListWidget):
    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.clearSelection()


class ObserverManager(threading.Thread):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.daemon = True

    def run(self):
        while True:
            for folder, observer in self.app.observers.items():
                if not observer.is_alive():
                    self.app.start_observer(folder)
            time.sleep(5)


class Notice(QWidget):
    def __init__(self, title, message):
        super().__init__()
        desktop = QApplication.desktop()
        self.screen_geometry = desktop.availableGeometry()

        notice_data_file = os.path.join(os.environ['APPDATA'], 'FolderMonitor', "noticeData.json")
        if os.path.exists(notice_data_file):
            with open(notice_data_file, "r") as f:
                self.notice_data = json.load(f)
        else:
            self.notice_data = {
                "screenSize": {"width": 500, "height": 178},
                "icon": {"x": 20, "y": 60},
                "icon_2": {"x": 15, "y": 15},
                "title": {"x": 110, "y": 60},
                "message": {"x": 110, "y": 82},
                "messagesize": {"width": 325, "height": 70},
                "app_name": {"x": 50, "y": 15},
                "closebutton": {"x": 430, "y": 15},
                "animation": {"x": self.screen_geometry.width() - 510, "y": self.screen_geometry.height() - 188},
                "animationtype": "QEasingCurce.InOutQuad"
            }

        self.setGeometry(self.screen_geometry.width() + self.width() + 30, self.notice_data["animation"]["y"],
                         self.notice_data["screenSize"]["width"], self.notice_data["screenSize"]["height"])
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QWidget(self)
        self.widget.setStyleSheet("#widget{background-color: rgba(230, 230, 230, 240);}")
        self.widget.setObjectName("widget")
        self.icon = QLabel(self.widget)
        self.icon.setGeometry(QRect(self.notice_data["icon"]["x"], self.notice_data["icon"]["y"], 71, 61))
        self.icon.setStyleSheet("image: url(:/img/monitor.png);")
        self.icon.setObjectName("icon")
        self.title = QLabel(self.widget)
        self.title.setText(title)
        self.title.setGeometry(QRect(self.notice_data["title"]["x"], self.notice_data["title"]["y"], 251, 21))
        self.title.setStyleSheet("font:700 12pt \"微软雅黑\";")
        self.title.setObjectName("title")
        self.message = QLabel(self.widget)
        self.message.setText(message)
        self.message.setGeometry(
            QRect(self.notice_data["message"]["x"], self.notice_data["message"]["y"],
                  self.notice_data["messagesize"]["width"], self.notice_data["messagesize"]["height"]))
        self.message.setStyleSheet("color:gray;font:11pt \"微软雅黑\";")
        self.message.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.message.setWordWrap(True)
        self.message.setObjectName("message")
        self.app_name = QLabel(self.widget)
        self.app_name.setText("文件夹监视器")
        self.app_name.setGeometry(QRect(self.notice_data["app_name"]["x"], self.notice_data["app_name"]["y"], 141, 31))
        self.app_name.setStyleSheet("font:10pt \"微软雅黑\";")
        self.app_name.setObjectName("app_name")
        self.closebutton = QPushButton(self.widget)
        self.closebutton.setText("×")
        self.closebutton.setGeometry(
            QRect(self.notice_data["closebutton"]["x"], self.notice_data["closebutton"]["y"], 31, 24))
        self.closebutton.setStyleSheet("QPushButton{background:transparent;color:gray;font:16pt \"微软雅黑\";}\n"
                                       "QPushButton:hover{color:black;}")
        self.closebutton.setObjectName("closebutton")
        self.closebutton.clicked.connect(self.close)  # type: ignore
        self.icon_2 = QLabel(self.widget)
        self.icon_2.setGeometry(QRect(self.notice_data["icon_2"]["x"], self.notice_data["icon_2"]["y"], 20, 31))
        self.icon_2.setStyleSheet("image: url(:/img/monitor.png);")
        self.icon_2.setObjectName("icon_2")
        self.horizontalLayout.addWidget(self.widget)

        self.animation = QPropertyAnimation(self, b"pos")
        name = QEasingCurve.InCirc
        for animationtype, animationname in animationList:
            if animationtype == self.notice_data["animationtype"]:
                name = animationname
                break
        self.animation.setEasingCurve(name)
        self.animation.setDuration(500)

    def show_animation(self):
        start_pos = QPoint(self.screen_geometry.width() + self.width() + 30, self.pos().y())
        end_pos = QPoint(self.notice_data["animation"]["x"], self.pos().y())
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.show()
        self.animation.start()

    def hide_animation(self):
        start_pos = QPoint(self.notice_data["animation"]["x"], self.notice_data["animation"]["y"])
        end_pos = QPoint(self.screen_geometry.width() + self.width() + 30, self.pos().y())
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.finished.connect(self.hide)  # type: ignore
        self.animation.start()


class NotificationManager(QObject):
    show_message_signal = pyqtSignal(str, str)

    def __init__(self, app, icon):
        super().__init__()
        self.app = app
        self.icon = icon
        self.notification_type = "系统通知2（可能无效）"
        self.winotify = Notification(app_id="文件夹监视器", title="", msg="", icon=self.icon)
        self.winotify.set_audio(audio.Default, loop=False)
        self.notice = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.close_notice)  # type: ignore
        self.show_message_signal.connect(self.show_notice)  # type: ignore

    def show_notification(self, title, message):
        if self.notification_type == "系统通知1（可能无效）":
            plyer.notification.notify(title=title, message=message, app_icon=self.icon, timeout=1)
        elif self.notification_type == "系统通知2（可能无效）":
            self.winotify.title = title
            self.winotify.msg = message
            self.winotify.icon = self.icon
            self.winotify.show()
            self.winotify.duration = "short"
        elif self.notification_type == "软件通知":
            self.show_message_signal.emit(title, message)  # type: ignore

    def show_notice(self, title, message):
        if not self.notice:
            self.notice = Notice(title, message)
        else:
            self.notice.title.setText(title)
            self.notice.message.setText(message)
        self.notice.show_animation()
        self.timer.start(3000)

    def close_notice(self):
        if self.notice:
            self.notice.hide_animation()
            self.notice = None
        self.timer.stop()


class FolderHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app

    def on_created(self, event):
        path, _ = os.path.split(event.src_path)
        self.app.log_change(path, "created")

    def on_deleted(self, event):
        path, _ = os.path.split(event.src_path)
        self.app.log_change(path, "deleted")

    def on_moved(self, event):
        path, _ = os.path.split(event.src_path)
        self.app.log_change(path, "modified")


class FolderScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_variables()
        self.init_ui()
        self.setup_system_tray()
        self.load_settings()
        self.load_notice_data()
        self.scan_results_file = os.path.join(self.storage_path, "scanResults.json")
        self.load_folders()
        self.load_log()
        self.load_qss()

        if self.startup_option == "前台启动":
            self.show()
        else:
            self.hide()

        self.setup_watchdog()
        self.observer_manager.start()

    # Initialization methods
    def init_variables(self):
        # Initialize all instance variables here
        self.observers = {}
        self.folder_list = []
        self.qss_cache = None
        self.testNotice = None
        self.storage_path = ""
        self.last_scan_results = {}
        self.startup_option = "前台启动"
        self.single_click_action = "无"
        self.handler = FolderHandler(self)
        self.double_click_action = "打开软件界面"
        self.observer_manager = ObserverManager(self)
        self.temp_icon_path = self.save_icon_to_temp()
        self.notification_manager = NotificationManager(self, self.temp_icon_path)

    def init_ui(self):
        self.set_window_properties()
        main_widget = QWidget()
        main_widget.setObjectName("main_widget")
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.tabWidget = QTabWidget()
        self.tabWidget.setObjectName("tabWidget")
        main_layout.addWidget(self.tabWidget)

        self.create_scan_tab()
        self.create_log_tab()
        self.create_notice_tab()
        self.create_settings_tab()

    def set_window_properties(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/img/monitor.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle("文件夹监视器")
        self.setGeometry(100, 100, 800, 600)
        self.setObjectName("mainWindow")

    def setup_watchdog(self):
        for folder in self.folder_list:
            self.start_observer(folder)

    def start_observer(self, folder):
        if folder not in self.observers or not self.observers[folder].is_alive():
            observer = Observer()
            observer.schedule(self.handler, folder, recursive=False)
            observer.start()
            self.observers[folder] = observer

    def stop_observer(self, folder):
        if folder in self.observers:
            self.observers[folder].stop()
            self.observers[folder].join()
            del self.observers[folder]

    # UI creation methods
    def create_scan_tab(self):
        scan_tab = QWidget()
        layout = QVBoxLayout()

        self.searchBar = QLineEdit()
        self.searchBar.setObjectName("searchBar")
        self.searchBar.setPlaceholderText("搜索文件夹...")
        self.searchBar.textChanged.connect(self.filter_folders)  # type: ignore
        layout.addWidget(self.searchBar)

        self.folderList = CustomListWidget()
        self.folderList.setObjectName("folderList")
        self.folderList.itemDoubleClicked.connect(open_folder)  # type: ignore
        self.folderList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.folderList.setDragDropMode(QListWidget.InternalMove)
        self.folderList.model().rowsMoved.connect(self.update_folder_order)  # type: ignore
        layout.addWidget(self.folderList)

        button_layout = QHBoxLayout()
        self.addButton = QPushButton()
        self.addButton.setObjectName("addButton")
        self.addButton.clicked.connect(self.add_folder)  # type: ignore
        self.removeButton = QPushButton()
        self.removeButton.setObjectName("removeButton")
        self.removeButton.clicked.connect(self.remove_folder)  # type: ignore
        button_layout.addWidget(self.addButton)
        button_layout.addWidget(self.removeButton)

        layout.addLayout(button_layout)
        scan_tab.setLayout(layout)
        self.tabWidget.addTab(scan_tab, "扫描")

    def create_log_tab(self):
        log_tab = QWidget()
        layout = QVBoxLayout()

        self.logText = QTextEdit()
        self.logText.setObjectName("logText")
        self.logText.setReadOnly(True)
        self.logText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.logText)

        button_layout = QHBoxLayout()
        self.exportButton = QPushButton()
        self.exportButton.setObjectName("exportButton")
        self.exportButton.clicked.connect(self.export_log)  # type: ignore
        self.clearButton = QPushButton()
        self.clearButton.setObjectName("clearButton")
        self.clearButton.clicked.connect(self.clear_log)  # type: ignore
        button_layout.addWidget(self.exportButton)
        button_layout.addWidget(self.clearButton)

        layout.addLayout(button_layout)
        log_tab.setLayout(layout)
        self.tabWidget.addTab(log_tab, "日志")

    def create_settings_tab(self):
        settings_tab = QWidget()
        layout = QVBoxLayout()

        storage_layout = QHBoxLayout()
        storageLabel = QLabel("文件保存位置：")
        storageLabel.setObjectName("storageLabel")
        self.storageLine = QLineEdit()
        self.storageLine.setObjectName("storageLine")
        self.storageLine.setReadOnly(True)
        self.storageButton = QPushButton("浏览")
        self.storageButton.setObjectName("storageButton")
        self.storageButton.clicked.connect(self.select_storage_location)  # type: ignore
        storage_layout.addWidget(storageLabel)
        storage_layout.addWidget(self.storageLine)
        storage_layout.addWidget(self.storageButton)
        layout.addLayout(storage_layout)

        notification_layout = QHBoxLayout()
        notificationLabel = QLabel("选择通知方式：")
        notificationLabel.setObjectName("notificationLabel")
        self.notificationCombo = QComboBox()
        self.notificationCombo.setObjectName("notificationCombo")
        self.notificationCombo.addItems(["不通知", "系统通知1（可能无效）", "系统通知2（可能无效）", "软件通知"])
        self.notificationCombo.setCurrentText(self.notification_manager.notification_type)
        self.notificationCombo.currentTextChanged.connect(self.update_notification_type)  # type: ignore

        self.test_notification_button = QPushButton("测试")
        self.test_notification_button.setObjectName("testButton")
        self.test_notification_button.clicked.connect(self.test_notification)  # type: ignore

        notification_layout.addWidget(notificationLabel)
        notification_layout.addWidget(self.notificationCombo)
        notification_layout.addWidget(self.test_notification_button)
        layout.addLayout(notification_layout)

        # Add single click action setting
        single_click_layout = QHBoxLayout()
        singleclickLabel = QLabel("单击托盘图标动作：")
        singleclickLabel.setObjectName("singleclickLabel")
        self.singleclickCombo = QComboBox()
        self.singleclickCombo.setObjectName("singleclickCombo")
        self.singleclickCombo.addItems(["无", "打开软件界面", "退出软件"])
        self.singleclickCombo.setCurrentText(self.single_click_action)
        self.singleclickCombo.currentTextChanged.connect(self.update_single_click_action)  # type: ignore
        single_click_layout.addWidget(singleclickLabel)
        single_click_layout.addWidget(self.singleclickCombo)
        layout.addLayout(single_click_layout)

        # Add double click action setting
        double_click_layout = QHBoxLayout()
        doubleclickLabel = QLabel("双击托盘图标动作：")
        doubleclickLabel.setObjectName("doubleclickLabel")
        self.doubleclickCombo = QComboBox()
        self.doubleclickCombo.setObjectName("doubleclickCombo")
        self.doubleclickCombo.addItems(["无", "打开软件界面", "退出软件"])
        self.doubleclickCombo.setCurrentText(self.double_click_action)
        self.doubleclickCombo.currentTextChanged.connect(self.update_double_click_action)  # type: ignore
        double_click_layout.addWidget(doubleclickLabel)
        double_click_layout.addWidget(self.doubleclickCombo)
        layout.addLayout(double_click_layout)

        startup_layout = QHBoxLayout()
        startupLabel = QLabel("启动选项：")
        startupLabel.setObjectName("startupLabel")
        self.startupCombo = QComboBox()
        self.startupCombo.setObjectName("startupCombo")
        self.startupCombo.addItems(["前台启动", "后台启动"])
        self.startupCombo.setCurrentText(self.startup_option)
        self.startupCombo.currentTextChanged.connect(self.update_startup_option)  # type: ignore
        startup_layout.addWidget(startupLabel)
        startup_layout.addWidget(self.startupCombo)
        layout.addLayout(startup_layout)

        qssLabel = QLabel("编辑组件QSS：")
        qssLabel.setObjectName("qssLabel")
        layout.addWidget(qssLabel)

        self.qssCombo = QComboBox()
        self.qssCombo.setObjectName("qssCombo")
        widgetList = [
            "<<----请选择一个组件---->>", "All QSS", "addButton", "adjustButton", "animationtypeCombo",
            "animationtypeLabel", "animationLabel", "animationX", "animationY", "applyButton", "app_nameLabel",
            "app_nameX", "app_nameY", "cancelButton", "clearButton", "closebuttonLabel", "closebuttonX", "closebuttonY",
            "doubleclickCombo", "doubleclickLabel", "exportButton", "folderList", "iconLabel", "iconX", "iconY",
            "logText", "mainWindow", "messageLabel", "messageX", "messageY", "notificationCombo", "notificationLabel",
            "removeButton", "screensizeHeight", "screensizeLabel", "screensizeWidth", "searchBar", "singleclickCombo",
            "singleclickLabel", "startupLabel", "startupCombo", "storageButton", "storageLabel", "storageLine",
            "testButton", "titleLabel", "titleX", "titleY", "qssCombo", "qssEdit", "qssLabel"]
        self.qssCombo.addItems(widgetList)
        self.qssCombo.currentTextChanged.connect(self.update_qssEdit)  # type: ignore
        layout.addWidget(self.qssCombo)

        self.qssEdit = QTextEdit()
        self.qssEdit.setObjectName("qssEdit")
        self.qssEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.qssEdit)

        self.applyButton = QPushButton("应用QSS")
        self.applyButton.setObjectName("applyButton")
        self.applyButton.clicked.connect(self.apply_qss)  # type: ignore
        layout.addWidget(self.applyButton)

        settings_tab.setLayout(layout)
        self.tabWidget.addTab(settings_tab, "设置")

    def create_notice_tab(self):
        self.notice_tab = QWidget()
        layout = QVBoxLayout()

        self.notice_label = QLabel("❗❗❗通知界面可能无法适配不同分辨率电脑，手动调节或许更加美观😘")
        self.notice_label.setStyleSheet("font:12pt '方正姚体'")
        self.notice_label.setObjectName("notice_label")
        self.notice_label.setFixedHeight(40)
        layout.addWidget(self.notice_label)

        self.noticeWidget = []

        screenSizeLayout = QHBoxLayout()
        self.screensizeLabel = QLabel("通知界面大小：")
        self.screensizeLabel.setObjectName("screensizeLabel")
        self.screensizeWidth = QSpinBox()
        self.screensizeWidth.setEnabled(False)
        self.noticeWidget.append(self.screensizeWidth)
        self.screensizeWidth.setObjectName("screensizeWidth")
        self.screensizeWidth.valueChanged.connect(self.updateNotice)  # type: ignore
        self.screensizeHeight = QSpinBox()
        self.screensizeHeight.setEnabled(False)
        self.noticeWidget.append(self.screensizeHeight)
        self.screensizeHeight.setObjectName("screensizeHeight")
        self.screensizeHeight.valueChanged.connect(self.updateNotice)  # type:ignore
        screenSizeLayout.addWidget(self.screensizeLabel)
        screenSizeLayout.addWidget(self.screensizeWidth)
        screenSizeLayout.addWidget(self.screensizeHeight)
        layout.addLayout(screenSizeLayout)

        components = [
            ("app_name", "软件名称位置："),
            ("icon_2", "小图标位置："),
            ("icon", "图标位置："),
            ("title", "标题位置："),
            ("closebutton", "关闭按钮位置："),
            ("message", "消息位置：")
        ]

        for name, label_text in components:
            component_layout = QHBoxLayout()
            setattr(self, f"{name}Label", QLabel(label_text))
            label = getattr(self, f"{name}Label")
            label.setObjectName(f"{name}Label")
            component_layout.addWidget(label)

            for axis in ['X', 'Y']:
                spin_box = QSpinBox()
                spin_box.setObjectName(f"{name}{axis}")
                spin_box.valueChanged.connect(self.updateNotice)  # type: ignore
                spin_box.setEnabled(False)
                self.noticeWidget.append(spin_box)
                setattr(self, f"{name}{axis}", spin_box)
                component_layout.addWidget(spin_box)

            layout.addLayout(component_layout)

        messagesizeLayout = QHBoxLayout()
        self.messagesizeLabel = QLabel("消息框大小：")
        self.messagesizeLabel.setObjectName("messagesizeLabel")
        self.messagesizeWidth = QSpinBox()
        self.messagesizeWidth.setObjectName("messagesizeWidth")
        self.messagesizeWidth.setEnabled(False)
        self.messagesizeWidth.valueChanged.connect(self.updateNotice)  # type: ignore
        self.noticeWidget.append(self.messagesizeWidth)
        self.messagesizeHeight = QSpinBox()
        self.messagesizeHeight.setObjectName("messagesizeHeight")
        self.messagesizeHeight.setEnabled(False)
        self.messagesizeHeight.valueChanged.connect(self.updateNotice)  # type: ignore
        self.noticeWidget.append(self.messagesizeHeight)
        messagesizeLayout.addWidget(self.messagesizeLabel)
        messagesizeLayout.addWidget(self.messagesizeWidth)
        messagesizeLayout.addWidget(self.messagesizeHeight)
        layout.addLayout(messagesizeLayout)

        animationLayout = QHBoxLayout()
        self.animationLabel = QLabel("弹窗动画结束位置：")
        self.animationLabel.setObjectName("animationLabel")
        self.animationX = QSpinBox()
        self.animationX.setObjectName("animationX")
        self.animationX.setEnabled(False)
        self.animationX.valueChanged.connect(self.updateNotice)  # type: ignore
        self.noticeWidget.append(self.animationX)
        self.animationY = QSpinBox()
        self.animationY.setObjectName("animationY")
        self.animationY.setEnabled(False)
        self.animationY.valueChanged.connect(self.updateNotice)  # type: ignore
        self.noticeWidget.append(self.animationY)
        animationLayout.addWidget(self.animationLabel)
        animationLayout.addWidget(self.animationX)
        animationLayout.addWidget(self.animationY)
        layout.addLayout(animationLayout)

        animationtypeLayout = QHBoxLayout()
        self.animationtypeLabel = QLabel("请选择弹出动画曲线：")
        self.animationtypeLabel.setObjectName("animationtypeLabel")
        self.animationtypeCombo = QComboBox()
        self.animationtypeCombo.setObjectName("animationtypeCombo")

        for animationname, animationtype in animationList:
            self.animationtypeCombo.addItem(animationname)
        self.animationtypeCombo.setEnabled(False)
        self.animationtypeCombo.currentIndexChanged.connect(self.showNotice)  # type: ignore
        animationtypeLayout.addWidget(self.animationtypeLabel)
        animationtypeLayout.addWidget(self.animationtypeCombo)
        layout.addLayout(animationtypeLayout)

        buttonLayout = QHBoxLayout()
        self.adjustButton = QPushButton("调整")
        self.adjustButton.setObjectName("adjustButton")
        self.cancelButton = QPushButton("取消")
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.hide()
        self.adjustButton.clicked.connect(self.toggle_notice_adjustment)  # type: ignore
        self.cancelButton.clicked.connect(self.cancel_notice_adjustment)  # type:ignore
        buttonLayout.addWidget(self.adjustButton)
        buttonLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonLayout)

        self.notice_tab.setLayout(layout)
        self.tabWidget.addTab(self.notice_tab, "通知")
        for spinBox in self.noticeWidget:
            spinBox.setMaximum(5000)

    def showNotice(self):
        if self.testNotice:
            animationType = self.animationtypeCombo.currentText()
            name = QEasingCurve.InCirc
            for animationtype, animationname in animationList:
                if animationtype == animationType:
                    name = animationname
                    break
            self.testNotice.animation.setEasingCurve(name)
            self.testNotice.show_animation()

    def updateNotice(self):
        if hasattr(self, 'testNotice'):
            if self.testNotice:
                if self.sender().objectName() == "animationtypeCombo":
                    self.testNotice.show_animation()
                else:
                    self.testNotice.setGeometry(self.animationX.value(), self.animationY.value(),
                                                self.screensizeWidth.value(), self.screensizeHeight.value())
                    self.testNotice.icon.move(self.iconX.value(), self.iconY.value())
                    self.testNotice.icon_2.move(self.icon_2X.value(), self.icon_2Y.value())
                    self.testNotice.title.move(self.titleX.value(), self.titleY.value())
                    self.testNotice.message.setGeometry(self.messageX.value(), self.messageY.value(),
                                                        self.messagesizeWidth.value(), self.messagesizeHeight.value())
                    self.testNotice.app_name.move(self.app_nameX.value(), self.app_nameY.value())
                    self.testNotice.closebutton.move(self.closebuttonX.value(), self.closebuttonY.value())

    def toggle_notice_adjustment(self):
        if self.adjustButton.text() == "调整":
            for spinBox in self.noticeWidget:
                spinBox.setEnabled(True)
            self.animationtypeCombo.setEnabled(True)
            self.adjustButton.setText("确认")
            self.cancelButton.show()
            self.testNotice = Notice("调整通知页面", "请修改参数调整各个组件的位置")
            self.testNotice.message.setStyleSheet("background: rgb(199, 224, 255);color:gray;font:11pt \"微软雅黑\";")
            self.testNotice.show_animation()
        else:
            for spinBox in self.noticeWidget:
                spinBox.setEnabled(False)
            self.animationtypeCombo.setEnabled(False)
            self.adjustButton.setText("调整")
            self.cancelButton.hide()
            self.testNotice.hide_animation()
            self.testNotice = None
            self.save_notice_data()

    def cancel_notice_adjustment(self):
        self.load_notice_data()
        self.cancelButton.hide()
        self.toggle_notice_adjustment()

    def update_folder_order(self):
        new_order = [self.folderList.item(i).text() for i in range(self.folderList.count())]
        self.folder_list = new_order
        self.save_folders()

    # click methods
    def update_single_click_action(self, action):
        self.single_click_action = action
        self.save_settings()

    def update_double_click_action(self, action):
        self.double_click_action = action
        self.save_settings()

    # startup methods
    def update_startup_option(self, option):
        self.startup_option = option
        self.save_settings()

    # System tray methods
    def setup_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/img/monitor.png"), QIcon.Normal, QIcon.Off)
        self.tray_icon.setIcon(icon)

        tray_menu = QMenu()
        show_action = QAction("显示", self)
        quit_action = QAction("退出", self)
        show_action.triggered.connect(self.show)  # type: ignore
        quit_action.triggered.connect(QApplication.instance().quit)  # type: ignore
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)  # type: ignore
        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Single click
            self.handle_tray_action(self.single_click_action)
        elif reason == QSystemTrayIcon.DoubleClick:  # Double click
            self.handle_tray_action(self.double_click_action)

    def handle_tray_action(self, action):
        if action == "打开软件界面":
            self.show()
        elif action == "退出软件":
            QApplication.instance().quit()

    def show(self):
        super().show()
        for folder, observer in self.observers.items():
            if not observer.is_alive():
                self.start_observer(folder)

    def closeEvent(self, event):
        if self.testNotice:
            self.toggle_notice_adjustment()
        event.ignore()
        self.hide()

        self.notification_manager.show_notification("缩小", "软件已缩小至托盘图标")

        for observer in self.observers.values():
            if not observer.is_alive():
                observer.start()

    # Folder management methods
    def filter_folders(self):
        search_text = self.searchBar.text().lower()
        for i in range(self.folderList.count()):
            item = self.folderList.item(i)
            item.setHidden(search_text not in item.text().lower())

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择监视文件夹")
        if folder and folder not in self.folder_list:
            self.folder_list.append(folder)
            self.folderList.addItem(folder)
            self.start_observer(folder)
            self.save_folders()
            self.log_action(f"Added folder: {folder}")

    def remove_folder(self):
        current_item = self.folderList.currentItem()
        if current_item:
            folder = current_item.text()
            self.folder_list.remove(folder)
            self.folderList.takeItem(self.folderList.row(current_item))
            self.stop_observer(folder)
            self.save_folders()
            self.log_action(f"Removed folder: {folder}")

    def remove_missing_folder(self, folder):
        self.folder_list.remove(folder)
        for i in range(self.folderList.count()):
            if self.folderList.item(i).text() == folder:
                self.folderList.takeItem(i)
                break
        if folder in self.last_scan_results:
            del self.last_scan_results[folder]
        self.save_folders()
        self.log_action(f"Removed missing folder: {folder}")

    # Logging methods
    def log_change(self, path, action):
        current_files = set([filename for filename in os.listdir(path)])
        scan_results = self.load_scan_results()
        last_files = set(scan_results.get(path, []))
        files = []

        if action == "created":
            new_file = current_files - last_files
            files.append(new_file)
            for file in new_file:
                self.log_action(f"Created in {path}: {file}")
        elif action == "deleted":
            deleted_file = last_files - current_files
            files.append(deleted_file)
            for file in deleted_file:
                self.log_action(f"Deleted from {path}: {file}")
        elif action == "modified":
            group = current_files & last_files
            old_files = list(last_files - group)[0]
            new_files = list(current_files - group)[0]
            files.append(old_files)
            files.append(new_files)
            self.log_action(f"Modified in {path}: {old_files}->{new_files}")

        scan_results[path] = list(current_files)
        self.save_scan_results(scan_results)
        self.show_notification(action, path, files)

    def save_icon_to_temp(self):
        icon = QIcon(":/img/monitor.png")
        pixmap = icon.pixmap(256, 256)

        temp_file = tempfile.NamedTemporaryFile(suffix='.ico', delete=False)
        temp_file_path = temp_file.name
        temp_file.close()

        pixmap.save(temp_file_path, "ICO")

        return temp_file_path

    def update_notification_type(self, notification_type):
        if notification_type == "软件通知":
            self.tabWidget.setTabVisible(self.tabWidget.indexOf(self.notice_tab), True)
        else:
            self.tabWidget.setTabVisible(self.tabWidget.indexOf(self.notice_tab), False)
        self.notification_manager.notification_type = notification_type
        self.save_settings()

    def test_notification(self):
        try:
            self.notification_manager.show_notification("测试通知", "这是一条测试通知消息")
        except Exception as e:
            self.log_action(f"Message sending failed: {e}")

    def show_notification(self, action, path, files):
        dict = {"created": "创建", "deleted": "删除", "modified": "修改"}
        if len(files) == 1:
            message = f"{path}： {list(files[0])[0]}被{dict[action]}".replace("\\", "/")
        else:
            message = f"{path}：{files[0]}被重命名为{files[1]}"
        try:
            self.notification_manager.show_notification(dict[action], message)
        except Exception as e:
            self.log_action(f"Message sending failed: {e}")

    def export_log(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "导出日志", "", "Text Files (*.txt)")
        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.logText.toPlainText())

    def clear_log(self):
        self.logText.clear()
        self.save_log()

    def log_action(self, message):
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        log_entry = f"{timestamp} - {message}\n"
        self.logText.append(log_entry)

        # 限制日志条目数量
        max_log_entries = 1000
        current_text = self.logText.toPlainText().split('\n')
        if len(current_text) > max_log_entries:
            self.logText.setPlainText('\n'.join(current_text[-max_log_entries:]))

        self.save_log()

    # Settings methods
    def select_storage_location(self):
        new_storage_path = QFileDialog.getExistingDirectory(self, "选择存储路径")
        if new_storage_path:
            if self.storage_path:
                self.move_files_to_new_location(new_storage_path)
            self.storage_path = new_storage_path
            self.storageLine.setText(new_storage_path)
            self.save_settings()
            self.load_folders()
            self.load_log()
            self.load_qss()

    def move_files_to_new_location(self, new_path):
        files_to_move = ['style.qss', 'log.txt', 'folders.json']
        for file in files_to_move:
            old_file_path = os.path.join(self.storage_path, file)
            new_file_path = os.path.join(new_path, file)
            if os.path.exists(old_file_path):
                try:
                    shutil.move(old_file_path, new_file_path)
                except Exception as e:
                    QMessageBox.warning(self, "File Move Error", f"Error moving {file}: {str(e)}")

    def save_settings(self):
        settings = {
            "storage_path": self.storage_path,
            "single_click_action": self.single_click_action,
            "double_click_action": self.double_click_action,
            "notification_type": self.notification_manager.notification_type,
            "startup_option": self.startup_option
        }
        try:
            with open(settings_file, "w") as f:
                json.dump(settings, f)
        except Exception as e:
            self.log_action(f"Error saving settings: {str(e)}")

    def load_settings(self):
        if not os.path.exists(settings_file):
            default_storage = create_default_storage()

            default_settings = {
                "storage_path": default_storage,
                "single_click_action": "无",
                "double_click_action": "打开软件界面",
                "notification_type": "系统通知1（可能无效）",
                "startup_option": "前台启动"
            }

            with open(settings_file, "w") as f:
                json.dump(default_settings, f)

            self.storage_path = default_storage
            self.single_click_action = "无"
            self.double_click_action = "打开软件界面"
            self.notification_manager.notification_type = "系统通知1（可能无效）"
            self.startup_option = "前台启动"
        else:
            try:
                with open(settings_file, "r") as f:
                    settings = json.load(f)
                    self.storage_path = settings.get("storage_path", "")
                    self.single_click_action = settings.get("single_click_action", "无")
                    self.double_click_action = settings.get("double_click_action", "打开软件界面")
                    self.notification_manager.notification_type = settings.get("notification_type",
                                                                               "系统通知1（可能无效）")
                    self.startup_option = settings.get("startup_option", "前台启动")
            except Exception as e:
                self.log_action(f"Error loading settings: {str(e)}")
                self.storage_path = create_default_storage()
                self.single_click_action = "无"
                self.double_click_action = "打开软件界面"
                self.notification_manager.notification_type = "系统通知1（可能无效）"
                self.startup_option = "前台启动"

        self.storageLine.setText(self.storage_path)
        self.singleclickCombo.setCurrentText(self.single_click_action)
        self.doubleclickCombo.setCurrentText(self.double_click_action)
        self.notificationCombo.setCurrentText(self.notification_manager.notification_type)
        self.update_notification_type(self.notification_manager.notification_type)
        self.startupCombo.setCurrentText(self.startup_option)

    def load_notice_data(self):
        desktop = QApplication.desktop()
        self.screen_geometry = desktop.availableGeometry()
        notice_data_file = os.path.join(self.storage_path, "noticeData.json")
        if not os.path.exists(notice_data_file):
            default_data = {
                "screenSize": {"width": 500, "height": 178},
                "icon": {"x": 20, "y": 60},
                "icon_2": {"x": 15, "y": 15},
                "title": {"x": 110, "y": 60},
                "message": {"x": 110, "y": 82},
                "messagesize": {"width": 325, "height": 70},
                "app_name": {"x": 50, "y": 15},
                "closebutton": {"x": 430, "y": 15},
                "animation": {"x": self.screen_geometry.width() - 510, "y": self.screen_geometry.height() - 188},
                "animationtype": "QEasingCurve.InOutExpo"
            }
            with open(notice_data_file, "w") as f:
                json.dump(default_data, f)
        else:
            with open(notice_data_file, "r") as f:
                default_data = json.load(f)

        self.screensizeWidth.setValue(default_data["screenSize"]["width"])
        self.screensizeHeight.setValue(default_data["screenSize"]["height"])
        self.iconX.setValue(default_data["icon"]["x"])
        self.iconY.setValue(default_data["icon"]["y"])
        self.icon_2X.setValue(default_data["icon_2"]["x"])
        self.icon_2Y.setValue(default_data["icon_2"]["y"])
        self.titleX.setValue(default_data["title"]["x"])
        self.titleY.setValue(default_data["title"]["y"])
        self.messageX.setValue(default_data["message"]["x"])
        self.messageY.setValue(default_data["message"]["y"])
        self.app_nameX.setValue(default_data["app_name"]["x"])
        self.app_nameY.setValue(default_data["app_name"]["y"])
        self.messagesizeWidth.setValue(default_data["messagesize"]["width"])
        self.messagesizeHeight.setValue(default_data["messagesize"]["height"])
        self.closebuttonX.setValue(default_data["closebutton"]["x"])
        self.closebuttonY.setValue(default_data["closebutton"]["y"])
        self.animationX.setValue(default_data["animation"]["x"])
        self.animationY.setValue(default_data["animation"]["y"])
        self.animationtypeCombo.setCurrentText(default_data["animationtype"])

    def save_notice_data(self):
        notice_data = {
            "screenSize": {"width": self.screensizeWidth.value(), "height": self.screensizeHeight.value()},
            "icon": {"x": self.iconX.value(), "y": self.iconY.value()},
            "icon_2": {"x": self.icon_2X.value(), "y": self.icon_2Y.value()},
            "title": {"x": self.titleX.value(), "y": self.titleY.value()},
            "message": {"x": self.messageX.value(), "y": self.messageY.value()},
            "messagesize": {"width": self.messagesizeWidth.value(), "height": self.messagesizeHeight.value()},
            "app_name": {"x": self.app_nameX.value(), "y": self.app_nameY.value()},
            "closebutton": {"x": self.closebuttonX.value(), "y": self.closebuttonY.value()},
            "animation": {"x": self.animationX.value(), "y": self.animationY.value()},
            "animationtype": self.animationtypeCombo.currentText()
        }
        notice_data_file = os.path.join(self.storage_path, "noticeData.json")
        with open(notice_data_file, "w") as f:
            json.dump(notice_data, f)

    # File management methods
    def save_folders(self):
        if not self.storage_path:
            self.log_action("Error: No storage path set. Cannot save folders.")
            return
        try:
            folders_file = os.path.join(self.storage_path, "folders.json")
            with open(folders_file, "w") as f:
                json.dump(self.folder_list, f)
        except Exception as e:
            self.log_action(f"Error saving folders: {str(e)}")

    def load_folders(self):
        if not self.storage_path:
            self.log_action("Error: No storage path set. Cannot load folders.")
            return
        try:
            folders_file = os.path.join(self.storage_path, "folders.json")
            with open(folders_file, "r") as f:
                self.folder_list = json.load(f)
                self.folderList.clear()
                self.folderList.addItems(self.folder_list)
                self.update_scan_results()
        except FileNotFoundError:
            pass
        except Exception as e:
            self.log_action(f"Error loading folders: {str(e)}")

    def update_scan_results(self):
        scan_results = self.load_scan_results()
        for folder in self.folder_list:
            if os.path.exists(folder):
                scan_results[folder] = list(os.listdir(folder))
            else:
                self.log_action(f"Warning: Folder not found: {folder}")
                if folder in scan_results:
                    del scan_results[folder]
        self.save_scan_results(scan_results)

    def load_scan_results(self):
        try:
            with open(self.scan_results_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            self.log_action("Error: Scan results file is corrupted. Creating a new one.")
            return {}

    def save_scan_results(self, scan_results):
        with open(self.scan_results_file, "w") as f:
            json.dump(scan_results, f)

    def save_log(self):
        if not self.storage_path:
            self.log_action("Error: No storage path set. Cannot save log.")
            return
        try:
            log_file = os.path.join(self.storage_path, "log.txt")
            with open(log_file, "w") as f:
                f.write(self.logText.toPlainText())
        except Exception as e:
            self.log_action(f"Error saving log: {str(e)}")

    def load_log(self):
        if not self.storage_path:
            self.log_action("Error: No storage path set. Cannot load log.")
            return
        try:
            log_file = os.path.join(self.storage_path, "log.txt")
            with open(log_file, "r") as f:
                self.logText.setPlainText(f.read())
        except FileNotFoundError:
            pass
        except Exception as e:
            self.log_action(f"Error loading log: {str(e)}")

    # QSS methods
    def update_qssEdit(self, component_name):
        if component_name == "<<----请选择一个组件---->>":
            qss_content = ""
        elif component_name == "All QSS":
            qss_content = self.load_all_qss()
        else:
            qss_content = self.load_component_qss(component_name)
        self.qssEdit.setPlainText(qss_content)

    def load_all_qss(self):
        qss_file_path = os.path.join(self.storage_path, "style.qss")
        try:
            with open(qss_file_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return "No QSS file found."

    def apply_qss(self):
        component_name = self.qssCombo.currentText()
        qss_content = self.qssEdit.toPlainText()

        if component_name == "<<----请选择一个组件---->>":
            pass
        elif component_name == "All QSS":
            self.save_all_qss(qss_content)
        else:
            self.save_component_qss(component_name, qss_content)

        self.qss_cache = None
        self.load_qss()

    def load_component_qss(self, component_name):
        qss_file_path = os.path.join(self.storage_path, "style.qss")
        try:
            with open(qss_file_path, "r") as f:
                qss_content = f.read()
                pattern = re.compile(rf'#{re.escape(component_name)}(?:\s*{{[^}}]*}}|\s*:[^{{]+{{[^}}]*}})+')
                matches = pattern.findall(qss_content)
                if matches:
                    return '\n\n'.join(matches)
        except FileNotFoundError:
            pass
        return f"#{component_name} {{\n\n}}"

    def save_all_qss(self, qss_content):
        qss_file_path = os.path.join(self.storage_path, "style.qss")
        with open(qss_file_path, "w") as f:
            f.write(qss_content)

    def save_component_qss(self, component_name, qss_content):
        qss_file_path = os.path.join(self.storage_path, "style.qss")
        try:
            with open(qss_file_path, "r") as f:
                full_qss_content = f.read()

            pattern = re.compile(rf'(#{re.escape(component_name)}(?:\s*{{[^}}]*}}|\s*:[^{{]+{{[^}}]*}})+)')
            if pattern.search(full_qss_content):
                new_qss_content = pattern.sub(qss_content, full_qss_content)
            else:
                new_qss_content = full_qss_content + "\n\n" + qss_content

            with open(qss_file_path, "w") as f:
                f.write(new_qss_content)
        except FileNotFoundError:
            with open(qss_file_path, "w") as f:
                f.write(qss_content)

    def load_qss(self):
        qss_file_path = os.path.join(self.storage_path, "style.qss")
        if self.qss_cache is None:
            try:
                with open(qss_file_path, "r") as f:
                    self.qss_cache = f.read()
            except FileNotFoundError:
                self.qss_cache = default_qss
                with open(qss_file_path, "w") as f:
                    f.write(default_qss)
        self.setStyleSheet(self.qss_cache)


if __name__ == "__main__":
    mutex_name = "FolderScannerApp_Mutex"
    mutex = win32event.CreateMutex(None, False, mutex_name)
    last_error = win32api.GetLastError()  # type: ignore

    if last_error == winerror.ERROR_ALREADY_EXISTS:
        mutex = None
        sys.exit(0)

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = FolderScannerApp()

    exit_code = app.exec_()

    if mutex:
        win32api.CloseHandle(mutex)  # type: ignore

    sys.exit(exit_code)
