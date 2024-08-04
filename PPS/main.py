from function import *
from packages import *


class MainWindow(Ui_Form, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    control = Controller()
    sys.exit(app.exec_())
