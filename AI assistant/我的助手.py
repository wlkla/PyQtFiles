import PyQt5

from entrance import Ui_Form as entrance_ui
from chat import Ui_MainWindow as chat_ui

from function import *


def read_api_key():
    with open("config.ini", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("api_key"):
                key, value = line.split("=")
                return value
    return None


def save_api_key(new_api_key):
    with open("config.ini", "r+", encoding="utf-8") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith("api_key"):
                key, value = line.split("=")
                new_line = key + "=" + new_api_key + "\n"
                lines[i] = new_line
                break
        f.seek(0)
        f.writelines(lines)


api_key = read_api_key()


class Entrance(PyQt5.QtWidgets.QMainWindow, entrance_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(
            PyQt5.QtCore.Qt.FramelessWindowHint | PyQt5.QtCore.Qt.WindowStaysOnTopHint | PyQt5.QtCore.Qt.Tool)
        self.setAttribute(PyQt5.QtCore.Qt.WA_TranslucentBackground)

        # 创建 QSystemTrayIcon 对象与图标
        self.tray_icon = PyQt5.QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(PyQt5.QtGui.QIcon("img/机器人俯视.ico"))
        tray_menu = PyQt5.QtWidgets.QMenu()
        quit_action = PyQt5.QtWidgets.QAction("退出", self)
        quit_action.triggered.connect(PyQt5.QtWidgets.QApplication.instance().quit)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip("AI助手")
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.show_window)
        self.movie = PyQt5.QtGui.QMovie('img/ROBOT.gif')
        self.label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.movie.frameChanged.connect(self.adjust_label_size)
        self.movie.start()

    def adjust_label_size(self):
        frame = self.movie.currentPixmap()
        self.label.setPixmap(frame)
        self.label.setFixedSize(frame.width(), frame.height())

    def mousePressEvent(self, event):
        if event.button() == PyQt5.QtCore.Qt.RightButton:
            # Create a QMenu instance and add an action to hide the window
            menu = PyQt5.QtWidgets.QMenu(self)
            hide_action = menu.addAction("隐藏")
            # Connect the action to a slot that hides the window
            hide_action.triggered.connect(self.hide)
            # Add a new action to change the api_key
            change_api_key_action = menu.addAction("修改api_key")
            # Connect the action to a slot that pops up an input box
            change_api_key_action.triggered.connect(self.change_api_key)
            # Show the menu at the cursor position
            menu.exec_(event.globalPos())

    def show_window(self, reason):
        # Check if the reason is a double click on the tray icon
        if reason == PyQt5.QtWidgets.QSystemTrayIcon.DoubleClick:
            # Show the window and raise it to the front
            self.show()
            self.raise_()

    def change_api_key(self):
        # Pop up an input box to let the user enter a new api_key
        new_api_key, ok = PyQt5.QtWidgets.QInputDialog.getText(self, "修改api_key", "请输入新的api_key：")
        if ok:
            # Update the global variable
            global api_key
            api_key = new_api_key
            # Save the new api_key to a config file or a database
            save_api_key(new_api_key)


class Chat(PyQt5.QtWidgets.QMainWindow, chat_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(
            PyQt5.QtCore.Qt.FramelessWindowHint | PyQt5.QtCore.Qt.WindowStaysOnTopHint | PyQt5.QtCore.Qt.Tool)
        self.setAttribute(PyQt5.QtCore.Qt.WA_TranslucentBackground)

        # 给 self.movable 赋一个初始值，比如 False
        self.movable = False

    def set_movable(self, movable):
        # 设置一个属性来记录是否允许移动窗口
        self.movable = movable

    def mousePressEvent(self, event):
        if event.button() == PyQt5.QtCore.Qt.LeftButton:
            super().mousePressEvent(event)
            # 只有当 self.movable 为 True 时，才记录鼠标位置
            if self.movable:
                self.start_x = event.x()
                self.start_y = event.y()

    def mouseReleaseEvent(self, event):
        if self.movable:
            self.start_x = None
            self.start_y = None

    def mouseMoveEvent(self, event):
        try:
            super().mouseMoveEvent(event)
            # 只有当 self.movable 为 True 时，才计算并移动窗口位置
            if self.movable:
                dis_x = event.x() - self.start_x
                dis_y = event.y() - self.start_y
                self.move(self.x() + dis_x, self.y() + dis_y)
        except:
            pass


if __name__ == "__main__":
    import sys
    import PyQt5

    PyQt5.QtCore.QCoreApplication.setAttribute(PyQt5.QtCore.Qt.AA_EnableHighDpiScaling)
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    control = Controller()
    sys.exit(app.exec_())
