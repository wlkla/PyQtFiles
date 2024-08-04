import io
import os
import sys
import time
import requests
import mimetypes
import pyperclip
import threading
from PIL import Image
from window import Ui_Form
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget

UPLOAD_URL = 'https://telegraph-image-6b4.pages.dev/upload'
GIF_URL = 'https://telegraph-image-6b4.pages.dev/file/9ac35a955f70d75da0165.gif'


class ImageHandler:
    @staticmethod
    def compress_image(file_path, target_size=5 * 1024 * 1024, quality=85, min_quality=65, step=5):
        original_size = os.path.getsize(file_path)

        if original_size <= target_size:
            return file_path

        with Image.open(file_path) as img:
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGB')

            max_dimension = 1920
            if max(img.size) > max_dimension:
                img.thumbnail((max_dimension, max_dimension), Image.LANCZOS)  # type: ignore

            temp_path = os.path.join(os.environ['TEMP'], os.path.basename(file_path))
            _format = 'JPEG' if img.format in ['JPEG', 'JPG'] else 'PNG'

            while quality >= min_quality:
                buffer = io.BytesIO()
                img.save(buffer, format=_format, quality=quality, optimize=True)
                if buffer.tell() <= target_size:
                    with open(temp_path, 'wb') as f:
                        f.write(buffer.getvalue())
                    return temp_path
                quality -= step

        buffer.seek(0)
        with open(temp_path, 'wb') as f:
            f.write(buffer.getvalue())
        return temp_path

    @staticmethod
    def upload_image_to_telegraph(file_path):
        file_path = ImageHandler.compress_image(file_path)
        mime_type = mimetypes.guess_type(file_path)[0]
        with open(file_path, 'rb') as file:
            response = requests.post(UPLOAD_URL, files={'file': (file_path, file, mime_type)})
            if response.status_code == 200:
                return UPLOAD_URL[:-7] + response.json()[0]['src']
        return None


class FileScanner:
    @staticmethod
    def scan_directory(path, _window):
        if os.path.isfile(path):
            return [path]

        image_files = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.jfif', '.pjpeg', '.pjp')):
                    image_files.append(os.path.join(root, file))
                    _window.label_8.setText(f"正在扫描，已检测到{len(image_files)}个图像文件。")
                    time.sleep(0.005)
        return image_files


class UploadManager:
    def __init__(self, _window, path):
        self.window = _window
        self.path = path
        self.image_files = []
        self.successful_links = []
        self.failure_paths = []

    def start_scan(self):
        self.image_files = FileScanner.scan_directory(self.path, self.window)
        total_files = len(self.image_files)

        if total_files == 1:
            self.window.progressBar.setRange(0, 0)
        else:
            self.window.progressBar.setMaximum(total_files)

        if os.path.isfile(self.path):
            self.window.label_8.setText("准备上传文件。")
        else:
            self.window.label_8.setText(f"扫描完成，检测到{total_files}个文件，准备上传。")
            time.sleep(3)

        self.window.widget_1.raise_()
        self.window.btn.raise_()
        self.window.widget_0.hide()

        upload_thread = threading.Thread(target=self.upload_and_handle_result)
        upload_thread.start()

    def upload_and_handle_result(self):
        for i, file_path in enumerate(self.image_files):
            if self.window.stop_threads:
                return

            self.window.set_image_to_label(file_path)

            for _ in range(5):
                try:
                    result = ImageHandler.upload_image_to_telegraph(file_path)
                    if result:
                        self.successful_links.append(result)
                        break
                except Exception as e:
                    print(e)
                    pass
            else:
                self.failure_paths.append(file_path)

            if len(self.image_files) != 1:
                self.window.progressBar.setValue(i + 1)

        self.finish_upload()

    def finish_upload(self):
        self.window.widget_2.raise_()
        self.window.btn.raise_()
        if len(self.failure_paths) == 0 and len(self.successful_links) == 1:
            self.window.label_3.setText("图片上传成功，链接已拷贝至剪切板。")
        else:
            self.window.label_3.setText(
                f"图片上传完毕，{len(self.successful_links)}个成功，{len(self.failure_paths)}个失败。")

        if not self.failure_paths:
            if len(self.successful_links) == 1:
                pyperclip.copy(self.successful_links[0])
            else:
                pyperclip.copy('\n'.join(self.successful_links))
        else:
            pyperclip.copy(
                '上传成功图片链接：\n' + '\n'.join(self.successful_links) +
                '\n上传失败图片路径：\n' + '\n'.join(self.failure_paths))

        time.sleep(3)
        QApplication.instance().quit()


class Window(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.movie = None
        self.stop_threads = None
        self.counter = None
        self.timer = None
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        screen = QDesktopWidget().screenGeometry()
        self.move(screen.width() - 450, 50)
        self.stop_threads = False
        self.counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_label)  # type: ignore
        self.timer.start(500)
        self.btn.clicked.connect(self.close_app)
        self.init_gif()

    def init_gif(self):
        gif_path = get_or_download_gif(GIF_URL)
        if gif_path:
            self.movie = QMovie(gif_path)
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
        QApplication.instance().quit()


def get_or_download_gif(url):
    temp_dir = os.path.join(os.environ['TEMP'], 'telegraph_uploader')
    os.makedirs(temp_dir, exist_ok=True)
    gif_path = os.path.join(temp_dir, 'scan.gif')

    if not os.path.exists(gif_path):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(gif_path, 'wb') as f:
                    f.write(response.content)
            else:
                return None
        except Exception as e:
            print(e)
            return None

    return gif_path


if __name__ == "__main__":
    if len(sys.argv) == 2:
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        app = QApplication(sys.argv)
        window = Window()
        window.show()
        window.widget_0.raise_()
        window.btn.raise_()

        upload_manager = UploadManager(window, sys.argv[1])
        scan_thread = threading.Thread(target=upload_manager.start_scan)
        scan_thread.start()

        sys.exit(app.exec_())
