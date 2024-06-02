import os
import sys
import time
import requests
import mimetypes
import pyperclip
import threading

from PIL import Image
from PyQt5.QtGui import QPixmap, QMovie

from window import Ui_Form
from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QMessageBox

url = 'https://telegraph-image-6b4.pages.dev/upload'


class Window(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setupUi(self)
        screen = QDesktopWidget().screenGeometry()
        width = screen.width()
        self.move(width - 450, 50)
        self.stop_threads = False
        self.counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_label)  # type: ignore
        self.timer.start(500)
        self.btn.clicked.connect(self.close_app)

        self.movie = QMovie(r'D:\Application\scan.gif')
        self.label_7.setMovie(self.movie)
        self.label_7.setScaledContents(True)
        self.movie.start()

    def update_label(self):
        self.label.setText('上传中' + '.' * (self.counter % 4))
        self.counter += 1

    def set_image_to_label(self, file_path):
        pixmap = QPixmap(file_path)
        picture_width = pixmap.width()
        picture_height = pixmap.height()
        label_width = self.label_6.width()
        label_height = self.label_6.height()
        if label_width / picture_width * picture_height < label_height:
            pixmap = pixmap.scaled(label_width, int(label_width / picture_width * picture_height),
                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            pixmap = pixmap.scaled(int(label_height / picture_height * picture_width), label_height,
                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_6.setPixmap(pixmap)
        self.label_6.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

    def close_app(self):
        self.close()
        self.stop_threads = True
        app.quit()


def compress_image(file_path):
    o_size = os.path.getsize(file_path) / 1024 / 1024
    if o_size < 5:
        return file_path

    picture = Image.open(file_path)
    temp_path = os.path.join(os.environ['TEMP'], os.path.basename(file_path))
    picture.save(temp_path, "JPEG", quality=90)

    return temp_path


def upload_image_to_telegraph(file_path):
    file_path = compress_image(file_path)
    mime_type = mimetypes.guess_type(file_path)[0]
    with open(file_path, 'rb') as file:
        response = requests.post(url, files={'file': (file_path, file, mime_type)})

        if response.status_code == 200:
            return url[:-7] + response.json()[0]['src']
        else:
            return None


def scan_directory(directory, window):
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_files.append(os.path.join(root, file))
                window.label_8.setText(f"正在扫描，已检测到{len(image_files)}个图像文件。")
                time.sleep(0.005)
    return image_files


if __name__ == "__main__":
    if len(sys.argv) == 2:
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        app = QApplication(sys.argv)
        window = Window()
        window.show()
        window.widget_0.raise_()
        window.btn.raise_()
        directory = sys.argv[1]


        def start_scan():
            image_files = scan_directory(directory, window)
            total_files = len(image_files)
            window.progressBar.setMaximum(total_files)
            window.label_8.setText(f"扫描完成，检测到{total_files}个文件，准备上传。")
            time.sleep(3)
            window.widget_1.raise_()
            window.btn.raise_()

            def upload_and_handle_result():
                success = 0
                fail = 0
                successful_links = []
                failure_paths = []
                for i, file_path in enumerate(image_files):
                    if window.stop_threads:
                        return
                    ans = ''
                    for _ in range(5):  # 最多尝试上传5次
                        try:
                            window.set_image_to_label(file_path)
                            ans = upload_image_to_telegraph(file_path)
                            if ans:  # 如果上传成功，跳出循环
                                break
                        except:
                            ans = ''
                    if ans:
                        success += 1
                        successful_links.append(ans)
                    else:
                        fail += 1
                        failure_paths.append(file_path)
                    window.progressBar.setValue(i + 1)
                window.widget_2.raise_()
                window.btn.raise_()
                window.label_3.setText(f"图片上传完毕，{success}个成功，{fail}个失败。")
                if len(failure_paths) == 0:
                    pyperclip.copy('上传成功图片链接：\n' + '\n'.join(successful_links))
                else:
                    pyperclip.copy(
                        '上传成功图片链接：\n' + '\n'.join(successful_links) + '\n上传失败图片路径：\n' + '\n'.join(
                            failure_paths))
                time.sleep(3)
                app.quit()

            upload_thread = threading.Thread(target=upload_and_handle_result)
            upload_thread.start()


        scan_thread = threading.Thread(target=start_scan)
        scan_thread.start()

        sys.exit(app.exec_())
