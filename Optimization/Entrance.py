from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from Function import *
from UI import Ui_Form


class mainwindow(Ui_Form, QWidget):
    resized = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resized.emit()


if __name__ == '__main__':
    import sys
    from PyQt5.QtCore import QCoreApplication, Qt
    from PyQt5.QtWidgets import QApplication

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    controll = Controller()
    sys.exit(app.exec_())
