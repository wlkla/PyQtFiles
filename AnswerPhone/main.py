import sys
import cv2
import time
import numpy as np
import pyautogui
from PIL import ImageGrab, Image
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QSpinBox, \
    QDoubleSpinBox, QMessageBox, QMenu, QAction, QSystemTrayIcon
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal

# Global variables for image paths and interval
image_path_1_1 = None
image_path_1_2 = None
image_path_2_1 = None
image_path_2_2 = None
image_path_3 = None
interval = 5
delay_after_click = 0.2  # Default delay after clicking


def capture_screen():
    try:
        screen = ImageGrab.grab()
        screen_np = np.array(screen)
        return screen_np
    except Exception as e:
        # 返回一个全白的图片
        return np.ones((1080, 1920, 3), dtype=np.uint8) * 255


def find_and_click(image_paths_to_find, image_paths_to_click, screen_image_np, threshold=0.9, delay_after_click=0.2):
    found = False
    for image_path in image_paths_to_find:
        template = cv2.imread(image_path, 0)
        screen_image = cv2.cvtColor(screen_image_np, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(screen_image, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        if len(loc[0]) > 0:
            found = True
            for pt in zip(*loc[::-1]):
                center_x, center_y = pt[0] + template.shape[1] // 2, pt[1] + template.shape[0] // 2
                pyautogui.moveTo(center_x, center_y, duration=0.2)
                pyautogui.click()
                break
            time.sleep(delay_after_click)
            screen_image_np = capture_screen()
            screen_image = cv2.cvtColor(screen_image_np, cv2.COLOR_BGR2GRAY)

            if image_paths_to_click:
                for image_path_to_click in image_paths_to_click:
                    template_click = cv2.imread(image_path_to_click, 0)
                    res_click = cv2.matchTemplate(screen_image, template_click, cv2.TM_CCOEFF_NORMED)
                    loc_click = np.where(res_click >= threshold)
                    if len(loc_click[0]) > 0:
                        for pt_click in zip(*loc_click[::-1]):
                            center_x_click, center_y_click = pt_click[0] + template_click.shape[1] // 2, pt_click[1] + \
                                                             template_click.shape[0] // 2
                            pyautogui.moveTo(center_x_click, center_y_click, duration=0.2)
                            pyautogui.click()
                            break
                        if image_path in [image_path_1_2]:
                            # 群聊，点击后再次截图并点击 image_path_3
                            time.sleep(delay_after_click)
                            screen_image_np = capture_screen()
                            screen_image = cv2.cvtColor(screen_image_np, cv2.COLOR_BGR2GRAY)
                            if image_path_3:
                                template_image_path_3 = cv2.imread(image_path_3, 0)
                                res_image_path_3 = cv2.matchTemplate(screen_image, template_image_path_3,
                                                                     cv2.TM_CCOEFF_NORMED)
                                loc_image_path_3 = np.where(res_image_path_3 >= threshold)
                                if len(loc_image_path_3[0]) > 0:
                                    for pt_image_path_3 in zip(*loc_image_path_3[::-1]):
                                        center_x_image_path_3, center_y_image_path_3 = pt_image_path_3[0] + \
                                                                                       template_image_path_3.shape[
                                                                                           1] // 2, pt_image_path_3[1] + \
                                                                                       template_image_path_3.shape[
                                                                                           0] // 2
                                        pyautogui.moveTo(center_x_image_path_3, center_y_image_path_3, duration=0.2)
                                        pyautogui.click()
                                        break
                            return True
                        return True
            return False
    return False


class ImageFinderThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, image_paths_to_find, image_paths_to_click, interval, delay_after_click):
        super().__init__()
        self.image_paths_to_find = image_paths_to_find
        self.image_paths_to_click = image_paths_to_click
        self.interval = interval
        self.delay_after_click = delay_after_click
        self.running = True

    def run(self):
        while self.running:
            screen_image_np = capture_screen()
            if not find_and_click(self.image_paths_to_find, self.image_paths_to_click, screen_image_np,
                                  delay_after_click=self.delay_after_click):
                self.update_signal.emit("未发现有新电话")
            else:
                self.update_signal.emit("成功接听电话")
            time.sleep(self.interval)

    def stop(self):
        self.running = False


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = '微信电话接听'
        self.setWindowIcon(QIcon('icon.ico'))
        self.image_paths_to_find = []
        self.image_paths_to_click = []
        self.interval = interval
        self.delay_after_click = delay_after_click
        self.finder_thread = None
        self.tray_icon = None
        self.tray_menu = None
        self.initUI()
        self.setupTrayIcon()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 400, 350)
        layout = QVBoxLayout()

        self.label1 = QLabel('选择私聊视频接听按钮截图:')
        layout.addWidget(self.label1)

        self.btn1 = QPushButton('选择私聊视频接听按钮截图', self)
        self.btn1.setToolTip('选择私聊视频接听按钮截图')
        self.btn1.clicked.connect(self.open_file_dialog_1_1)
        layout.addWidget(self.btn1)

        self.label2 = QLabel('选择群聊视频接听按钮截图:')
        layout.addWidget(self.label2)

        self.btn2 = QPushButton('选择群聊视频接听按钮截图', self)
        self.btn2.setToolTip('选择群聊视频接听按钮截图')
        self.btn2.clicked.connect(self.open_file_dialog_1_2)
        layout.addWidget(self.btn2)

        self.label3 = QLabel('选择私聊全屏按钮截图:')
        layout.addWidget(self.label3)

        self.btn_click_image_2_1 = QPushButton('选择私聊全屏按钮截图', self)
        self.btn_click_image_2_1.setToolTip('选择私聊全屏按钮截图')
        self.btn_click_image_2_1.clicked.connect(self.open_file_dialog_click_2_1)
        layout.addWidget(self.btn_click_image_2_1)

        self.label4 = QLabel('选择群聊全屏按钮截图:')
        layout.addWidget(self.label4)

        self.btn_click_image_2_2 = QPushButton('选择群聊全屏按钮截图', self)
        self.btn_click_image_2_2.setToolTip('选择群聊全屏按钮截图')
        self.btn_click_image_2_2.clicked.connect(self.open_file_dialog_click_2_2)
        layout.addWidget(self.btn_click_image_2_2)

        self.label5 = QLabel('选择开启摄像头截图:')
        layout.addWidget(self.label5)

        self.btn_click_image_3 = QPushButton('选择开启摄像头截图', self)
        self.btn_click_image_3.setToolTip('选择开启摄像头截图')
        self.btn_click_image_3.clicked.connect(self.open_file_dialog_click_3)
        layout.addWidget(self.btn_click_image_3)

        self.label6 = QLabel('设置检查电话时间间隔:')
        layout.addWidget(self.label6)

        self.spinbox = QSpinBox(self)
        self.spinbox.setValue(self.interval)
        self.spinbox.setMinimum(1)
        layout.addWidget(self.spinbox)

        self.label8 = QLabel('设置接听后全屏间隔（秒）:')
        layout.addWidget(self.label8)

        self.double_spinbox = QDoubleSpinBox(self)
        self.double_spinbox.setValue(self.delay_after_click)
        self.double_spinbox.setMinimum(0.0)
        self.double_spinbox.setSingleStep(0.1)
        layout.addWidget(self.double_spinbox)

        self.btn_start_stop = QPushButton('开始', self)
        self.btn_start_stop.clicked.connect(self.toggle_finding)
        layout.addWidget(self.btn_start_stop)

        self.status_label = QLabel('状态: 空闲')
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def closeEvent(self, event):
        if self.tray_icon.isVisible():
            self.hide()  # 隐藏窗口
            event.ignore()  # 忽略关闭事件
        else:
            event.accept()  # 允许关闭事件

    def setupTrayIcon(self):
        self.tray_icon = QSystemTrayIcon(QIcon('icon.ico'), self)
        self.tray_icon.show()
        self.tray_menu = QMenu()

        restore_action = QAction('显示主窗口', self)
        restore_action.triggered.connect(self.show_window)
        self.tray_menu.addAction(restore_action)

        quit_action = QAction('退出', self)
        quit_action.triggered.connect(self.quit_application)
        self.tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.onTrayIconActivated)
        self.tray_icon.show()

    def open_file_dialog_1_1(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "选择私聊视频接听按钮截图", "",
                                              "图片文件 (*.png *.jpg *.jpeg *.bmp)",
                                              options=options)
        if file:
            global image_path_1_1
            image_path_1_1 = file
            self.btn1.setText('私聊视频接听按钮截图已选择')
            self.btn1.setToolTip('重新选择私聊视频接听按钮截图')

    def open_file_dialog_1_2(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "选择群聊视频接听按钮截图", "",
                                              "图片文件 (*.png *.jpg *.jpeg *.bmp)",
                                              options=options)
        if file:
            global image_path_1_2
            image_path_1_2 = file
            self.btn2.setText('群聊视频接听按钮截图已选择')
            self.btn2.setToolTip('重新选择私聊视频接听按钮截图')

    def open_file_dialog_click_2_1(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "选择私聊全屏按钮截图", "", "图片文件 (*.png *.jpg *.jpeg *.bmp)",
                                              options=options)
        if file:
            global image_path_2_1
            image_path_2_1 = file
            self.btn_click_image_2_1.setText('私聊全屏按钮截图已选择')
            self.btn_click_image_2_1.setToolTip('重新选择私聊全屏按钮截图')

    def open_file_dialog_click_2_2(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "选择群聊全屏按钮截图", "", "图片文件 (*.png *.jpg *.jpeg *.bmp)",
                                              options=options)
        if file:
            global image_path_2_2
            image_path_2_2 = file
            self.btn_click_image_2_2.setText('私聊全屏按钮截图已选择')
            self.btn_click_image_2_2.setToolTip('重新选择私聊全屏按钮截图')

    def open_file_dialog_click_3(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "选择开启摄像头截图", "", "图片文件 (*.png *.jpg *.jpeg *.bmp)",
                                              options=options)
        if file:
            global image_path_3
            image_path_3 = file
            self.btn_click_image_3.setText('开启摄像头截图已选择')
            self.btn_click_image_3.setToolTip('重新选择开启摄像头截图')

    def toggle_finding(self):
        if self.finder_thread is None or not self.finder_thread.isRunning():
            self.interval = self.spinbox.value()
            self.delay_after_click = self.double_spinbox.value()
            image_paths_to_find = [image_path_1_1, image_path_1_2]
            image_paths_to_click = [image_path_2_1, image_path_2_2]
            if None in image_paths_to_find or None in image_paths_to_click:
                QMessageBox.warning(self, '警告', '请确保所有图片都已选择')
                return

            # 禁用所有选择按钮和输入框
            self.btn1.setEnabled(False)
            self.btn2.setEnabled(False)
            self.btn_click_image_2_1.setEnabled(False)
            self.btn_click_image_2_2.setEnabled(False)
            self.btn_click_image_3.setEnabled(False)
            self.spinbox.setEnabled(False)
            self.double_spinbox.setEnabled(False)

            self.finder_thread = ImageFinderThread(image_paths_to_find, image_paths_to_click, self.interval,
                                                   self.delay_after_click)
            self.finder_thread.update_signal.connect(self.update_status)
            self.finder_thread.start()
            self.btn_start_stop.setText('停止')
        else:
            self.finder_thread.stop()
            self.finder_thread.wait()
            self.finder_thread = None

            # 启用所有选择按钮和输入框
            self.btn1.setEnabled(True)
            self.btn2.setEnabled(True)
            self.btn_click_image_2_1.setEnabled(True)
            self.btn_click_image_2_2.setEnabled(True)
            self.btn_click_image_3.setEnabled(True)
            self.spinbox.setEnabled(True)
            self.double_spinbox.setEnabled(True)

            self.btn_start_stop.setText('开始')

    def update_status(self, message):
        self.status_label.setText(f'状态: {message}')

    def show_window(self):
        self.show()
        self.activateWindow()

    def quit_application(self):
        QApplication.quit()

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
