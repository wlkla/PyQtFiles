import os
import sys
import glob
import pickle
import tempfile
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileDialog, QLabel, QVBoxLayout, QWidget, QApplication


def load_xor_values():
    user_home = os.path.expanduser('~')
    _file_path = os.path.join(user_home, "AppData\\Roaming\\DatFileViewer\\xor_values.pkl")
    if os.path.exists(_file_path):
        with open(_file_path, "rb") as file:
            return pickle.load(file)
    return []


class DatFileViewer(QWidget):
    def __init__(self, _file_path=None):
        super().__init__()
        self.initUI()
        self.pressed = None
        self.origin = None
        self.label = None
        self.layout = None
        self.current_pixmap = None
        self.xor_values = load_xor_values()
        self.scale_factor = 1.0
        self.file_list = []
        self.current_file_index = 0

        if _file_path:
            self.file_list = sorted(glob.glob(os.path.join(os.path.dirname(_file_path), '*.dat')))
            self.current_file_index = self.file_list.index(_file_path)
            self.decodeAndDisplayImage(_file_path)

    def initUI(self):
        self.setWindowTitle('DAT File Viewer')
        self.setWindowIcon(QIcon("D:/Document/Downloads/时间序列频率转换-选中.ico"))
        self.layout = QVBoxLayout()
        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # type: ignore
        self.showFullScreen()

    def wheelEvent(self, event):
        degrees = event.angleDelta().y() / 8
        steps = degrees / 15
        if steps > 0:
            self.scale_factor *= 1.0 + steps / 10.0
        else:
            self.scale_factor /= 1.0 - steps / 10.0
        self.displayImage()

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.pressed = True
        self.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))  # type: ignore

    def mouseMoveEvent(self, event):
        if self.pressed:
            x = event.x()
            y = event.y()
            x_diff = x - self.origin.x()
            y_diff = y - self.origin.y()
            self.origin = QPoint(x, y)
            self.label.move(self.label.pos() + QPoint(x_diff, y_diff))

    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))  # type: ignore

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:  # type: ignore
            self.close()
        elif event.key() == QtCore.Qt.Key_Right:  # type: ignore
            self.current_file_index = (self.current_file_index + 1) % len(self.file_list)
            self.decodeAndDisplayImage(self.file_list[self.current_file_index])
        elif event.key() == QtCore.Qt.Key_Left:  # type: ignore
            self.current_file_index = (self.current_file_index - 1) % len(self.file_list)
            self.decodeAndDisplayImage(self.file_list[self.current_file_index])
        elif event.key() == QtCore.Qt.Key_S and event.modifiers() & QtCore.Qt.ControlModifier:  # type: ignore
            self.saveImage()

    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "DAT Files (*.dat);;All Files (*)", options=options)
        if fileName:
            self.decodeAndDisplayImage(fileName)

    def decodeAndDisplayImage(self, _file_path):
        if self.xor_values:
            for xor_value in self.xor_values:
                if self.tryDecode(_file_path, xor_value):
                    return

        with open(_file_path, "rb") as file:
            first_four_bytes = file.read(2)

        hex_value = int.from_bytes(first_four_bytes, byteorder='big')
        xor_result = hex_value ^ 0xffd8
        xor_value = xor_result & 0xff

        if self.tryDecode(_file_path, xor_value):
            self.xor_values.append(xor_value)
            self.save_xor_values()
            return

        for possible_xor_value in range(256):
            if self.tryDecode(_file_path, possible_xor_value):
                self.xor_values.append(possible_xor_value)
                self.save_xor_values()
                return

        self.label.setText("Failed to decode image.")

    def tryDecode(self, _file_path, xor_value):
        temp_dir = tempfile.gettempdir()
        target_path = os.path.join(temp_dir, "decoded_image.png")

        with open(_file_path, "rb") as dat_read, open(target_path, "wb") as png_write:
            for now in dat_read:
                for nowByte in now:
                    newByte = nowByte ^ xor_value
                    png_write.write(bytes([newByte]))

        self.current_pixmap = QPixmap(target_path)
        if not self.current_pixmap.isNull():
            self.displayImage()
            return True
        return False

    def displayImage(self):
        if self.current_pixmap:
            self.label.setPixmap(
                self.current_pixmap.scaled(self.scale_factor * self.label.size(),
                                           QtCore.Qt.KeepAspectRatio,  # type: ignore
                                           QtCore.Qt.SmoothTransformation))  # type: ignore
            self.label.setAlignment(QtCore.Qt.AlignCenter)  # type: ignore
        else:
            self.label.setText("Failed to load image.")
        self.label.setAlignment(QtCore.Qt.AlignCenter)  # type: ignore

    def save_xor_values(self):
        user_home = os.path.expanduser('~')
        directory = os.path.join(user_home, "AppData\\Roaming\\DatFileViewer")
        os.makedirs(directory, exist_ok=True)
        _file_path = os.path.join(directory, "xor_values.pkl")
        with open(_file_path, "wb") as file:
            pickle.dump(self.xor_values, file)

    def saveImage(self):
        if self.current_pixmap:
            options = QFileDialog.Options()
            default_path = os.path.join(os.path.expanduser('~'),
                                        os.path.basename(self.file_list[self.current_file_index]).replace('.dat',
                                                                                                          '.png'))
            fileName, _ = QFileDialog.getSaveFileName(self, "保存图片", default_path,
                                                      "PNG Files (*.png);;All Files (*)", options=options)
            if fileName:
                self.current_pixmap.save(fileName, "PNG")


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # type: ignore
    app = QApplication(sys.argv)
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    viewer = DatFileViewer(file_path)
    viewer.show()
    sys.exit(app.exec_())
