import json
import random
import urllib.parse
import configparser
import urllib.request
from Function import *
from login import Ui_Form as LoginUi_Form
from findPwd import Ui_Form as FindPwdUi_Form
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QMouseEvent, QCursor, QIcon
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QTimer, QEasingCurve, QPropertyAnimation
from qframelesswindow import FramelessWindow, StandardTitleBar


class loginWindow(LoginUi_Form, FramelessWindow):
    toPwdUi = pyqtSignal()
    success = pyqtSignal()
    fail = pyqtSignal()

    code = '@*@*r389r2few[q'
    countdown = 60
    APIUsername, APIPassword = '', ''
    rememberState = False

    def __init__(self, parent=None):
        super(loginWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUi()
        self.initParameter()
        self.timer = QTimer()

        self.startPos = None
        self.labels = [self.label_8, self.label_9, self.label_10, self.label_11]
        self.initPos = [label.pos() for label in self.labels]

        self.timer.timeout.connect(self.updateCountdown)  # type: ignore
        self.EditableComboBox.currentTextChanged.connect(self.resetLabel)
        self.PasswordLineEdit.textChanged.connect(self.resetLabel)

    def initUi(self):
        try:
            with open('user_data.json', 'r') as json_file:
                users = json.load(json_file)
        except:
            users = {}

        self.label_2.hide()
        self.label_3.hide()
        self.label_4.hide()
        self.widget_4.hide()

        self.widget_2.move(17, 170)
        self.widget_3.move(17, 240)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.EditableComboBox.addItems(users.keys())
        self.EditableComboBox.setText('')

        self.setTitleBar(StandardTitleBar(self))
        self.titleBar.raise_()
        self.titleBar.maxBtn.hide()

        rect = QApplication.desktop().availableGeometry()
        w, h = rect.width(), rect.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def initParameter(self):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        self.APIUsername = config.get('Parameter', 'APIUsername')
        self.APIPassword = config.get('Parameter', 'APIPassword')
        self.UVC = config.get('Parameter', 'universal_captcha_code')

    def initLabel(self):
        self.label_2.setText('* 手机号不能为空')
        self.label_3.setText('* 密码不能为空')
        self.label_4.setText('* 验证码错误')
        self.label_2.hide()
        self.label_3.hide()
        self.label_4.hide()

    def enterEvent(self, event):
        self.startPos = event.pos()

    def leaveEvent(self, event):
        self.startPos = None

    def mouseMoveEvent(self, event):
        if self.startPos is None:
            return

        offsetX = event.pos().x() - self.startPos.x()
        offsetY = event.pos().y() - self.startPos.y()

        for i, label in enumerate(self.labels):
            newX = self.initPos[i].x() + int(offsetX * (0.01 * (i + 1)))
            newY = self.initPos[i].y() + int(offsetY * (0.01 * (i + 1)))
            label.move(newX, newY)

    def resetFrame(self):
        self.initLabel()
        self.LineEdit.setText('')
        self.EditableComboBox.setFocus()
        self.EditableComboBox.setText('')
        self.PasswordLineEdit.setText('')

        if self.TransparentToggleToolButton.isChecked():
            self.widget_2.move(17, 140)
            self.widget_3.move(17, 200)
            self.widget_4.show()
            self.PrimaryPushButton.setText('注册并登录')
            self.ElevatedCardWidget_3.hide()
        else:
            self.widget_4.hide()
            self.widget_2.move(17, 170)
            self.widget_3.move(17, 240)
            self.PrimaryPushButton.setText('登录')
            self.ElevatedCardWidget_3.show()

    def sendCode(self):
        try:
            with open('user_data.json', 'r') as json_file:
                users = json.load(json_file)
        except:
            users = {}
        self.code = ''
        mobile = self.EditableComboBox.text()
        if mobile == '':
            self.shake_window(self.EditableComboBox, 10)
            self.label_2.setText('* 手机号不能为空')
            self.label_2.show()
        elif mobile in users:
            self.label_2.setText('* 该手机号已注册')
            self.shake_window(self.EditableComboBox, 10)
            self.label_2.show()
        else:
            self.code = ''.join(str(random.randint(0, 9)) for _ in range(6))
            self.timer.start(1000)
            url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'
            values = {'account': self.APIUsername, 'password': self.APIPassword, 'mobile': mobile,
                      'content': f'您的验证码是：{self.code}。请不要把验证码泄露给其他人。', 'format': 'json', }
            data = urllib.parse.urlencode(values).encode(encoding='UTF8')
            req = urllib.request.Request(url, data)
            response = urllib.request.urlopen(req)
            res = response.read()

    def confirmLogin(self):
        try:
            with open('user_data.json', 'r') as json_file:
                users = json.load(json_file)
        except:
            users = {}
        self.initLabel()
        mobile = self.EditableComboBox.text()
        password = self.PasswordLineEdit.text()
        if self.TransparentToggleToolButton.isChecked():
            code = self.LineEdit.text()
            if mobile == '':  # 手机号为空
                self.shake_window(self.EditableComboBox, 10)
                self.label_2.show()
            elif password == '':  # 密码为空
                self.shake_window(self.PasswordLineEdit, 10)
                self.label_3.show()
            elif code == '':  # 验证码为空
                self.shake_window(self.LineEdit, 10)
                self.label_4.show()
            elif mobile in users:  # 手机号已注册
                self.label_2.setText('* 该手机号已注册')
                self.shake_window(self.EditableComboBox, 10)
                self.label_2.show()
            elif code != self.code and code != self.UVC:  # 验证码不正确
                self.shake_window(self.LineEdit, 10)
                self.label_4.show()
            else:  # 成功注册并登录
                users[mobile] = {"password": password}
                with open('user_data.json', 'w') as json_file:
                    json.dump(users, json_file)
                self.EditableComboBox.addItem(mobile)
                self.success.emit()  # type: ignore
        else:
            if mobile == '':  # 手机号为空
                self.shake_window(self.EditableComboBox, 10)
                self.label_2.show()
            elif password == '':  # 密码为空
                self.shake_window(self.PasswordLineEdit, 10)
                self.label_3.show()
            elif mobile not in users:  # 手机号未注册
                self.shake_window(self.EditableComboBox, 10)
                self.label_2.setText('* 该手机号未注册')
                self.label_2.show()
            elif mobile in users and password == users[mobile]["password"]:  # 账号密码正确，成功登录
                self.success.emit()  # type: ignore
            else:  # 账号或密码错误
                self.shake_window(self.EditableComboBox, 10)
                self.shake_window(self.PasswordLineEdit, 10)
                self.fail.emit()  # type: ignore

    def resetPwd(self):
        self.toPwdUi.emit()  # type: ignore

    def changState(self):
        config = configparser.ConfigParser()
        state = (True if self.CheckBox.isChecked() else False)
        config.read('./config.ini', encoding='utf-8')
        config.set('Settings', 'state', str(state))
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)

    def resetLabel(self):
        import re
        widget = self.sender().objectName()
        text = self.sender().text()
        if widget == 'EditableComboBox':
            if text == '':
                self.shake_window(self.sender(), 10)
                self.label_2.setText('* 手机号不能为空')
                self.label_2.show()
            elif not (re.match(r"^1[35678]\d{9}$", text) and len(text) == 11):
                self.label_2.setText('* 手机号格式不符合要求')
                self.label_2.show()
            else:
                self.label_2.setText('* 手机号不能为空')
                self.label_2.hide()
        elif widget == 'PasswordLineEdit':
            if text == '':
                self.label_3.setText('* 密码不能为空')
                self.shake_window(self.sender(), 10)
                self.label_3.show()
            elif len(text) < 6:
                self.label_3.setText('* 密码长度不能小于6位')
                self.label_3.show()
            else:
                self.label_3.setText('* 密码不能为空')
                self.label_3.hide()

    def updateCountdown(self):
        self.PrimaryPushButton_2.setEnabled(False)
        self.PrimaryPushButton_2.setText(f'{self.countdown}s后重新发送')
        self.countdown -= 1
        if self.countdown == -1:
            self.PrimaryPushButton_2.setEnabled(True)
            self.PrimaryPushButton_2.setText('获取验证码')
            self.countdown = 60
            self.timer.stop()
            return

    def shake_window(self, window, round):
        if round == 0:
            return
        x = 6 * (-1) ** round
        window.move(window.x() + x, window.y())
        QTimer.singleShot(20, lambda: self.shake_window(window, round - 1))


class findPwdWindow(FindPwdUi_Form, QWidget):
    toLogUi = pyqtSignal()
    success = pyqtSignal()

    code = '@*@*r389r2few[q'
    countdown = 60
    APIUsername, APIPassword = '', ''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.initUi()
        self.initParameter()
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateCountdown)  # type: ignore
        self.EditableComboBox.currentTextChanged.connect(self.resetLabel)
        self.PasswordLineEdit.textChanged.connect(self.resetLabel)

    def initUi(self):
        try:
            with open('user_data.json', 'r') as json_file:
                users = json.load(json_file)
        except:
            users = {}

        self.label_2.hide()
        self.label_3.hide()
        self.label_4.hide()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.EditableComboBox.addItems(users.keys())
        self.EditableComboBox.setText('')

        rect = QApplication.desktop().availableGeometry()
        w, h = rect.width(), rect.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def initParameter(self):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        self.APIUsername = config.get('Parameter', 'APIUsername')
        self.APIPassword = config.get('Parameter', 'APIPassword')
        self.UVC = config.get('Parameter', 'universal_captcha_code')

    def initLabel(self):
        self.label_2.setText('* 手机号不能为空')
        self.label_3.setText('* 密码不能为空')
        self.label_4.setText('* 验证码错误')
        self.label_2.hide()
        self.label_3.hide()
        self.label_4.hide()

    def resetLabel(self):
        import re
        widget = self.sender().objectName()
        text = self.sender().text()
        if widget == 'EditableComboBox':
            if text == '':
                self.shake_window(self.sender(), 10)
                self.label_2.setText('* 手机号不能为空')
                self.label_2.show()
            elif not (re.match(r"^1[35678]\d{9}$", text) and len(text) == 11):
                self.label_2.setText('* 手机号格式不符合要求')
                self.label_2.show()
            else:
                self.label_2.setText('* 手机号不能为空')
                self.label_2.hide()
        elif widget == 'PasswordLineEdit':
            if text == '':
                self.label_3.setText('* 密码不能为空')
                self.shake_window(self.sender(), 10)
                self.label_3.show()
            elif len(text) < 6:
                self.label_3.setText('* 密码长度不能小于6位')
                self.label_3.show()
            else:
                self.label_3.setText('* 密码不能为空')
                self.label_3.hide()

    def mouseMoveEvent(self, e: QMouseEvent):
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True
            self.setCursor(QCursor(Qt.ClosedHandCursor))

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None
            self.setCursor(QCursor(Qt.ArrowCursor))

    def return_login(self):
        self.toLogUi.emit()  # type: ignore

    def getCode(self):
        try:
            with open('user_data.json', 'r') as json_file:
                users = json.load(json_file)
        except:
            users = {}
        self.code = ''
        mobile = self.EditableComboBox.text()
        if mobile == '':
            self.shake_window(self.EditableComboBox, 10)
            self.label_2.setText('* 手机号不能为空')
            self.label_2.show()
        elif mobile not in users:
            self.label_2.setText('* 该手机号未注册')
            self.shake_window(self.EditableComboBox, 10)
            self.label_2.show()
        else:
            self.code = ''.join(str(random.randint(0, 9)) for _ in range(6))
            self.timer.start(1000)
            url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'
            values = {
                'account': self.APIUsername,
                'password': self.APIPassword,
                'mobile': mobile,
                'content': f'您的验证码是：{self.code}。请不要把验证码泄露给其他人。',
                'format': 'json',
            }
            data = urllib.parse.urlencode(values).encode(encoding='UTF8')
            req = urllib.request.Request(url, data)
            response = urllib.request.urlopen(req)
            res = response.read()

    def confirmChange(self):
        try:
            with open('user_data.json', 'r') as json_file:
                users = json.load(json_file)
        except:
            users = {}

        self.initLabel()
        mobile = self.EditableComboBox.text()
        password = self.PasswordLineEdit.text()
        code = self.LineEdit.text()
        if mobile == '':  # 手机号为空
            self.shake_window(self.EditableComboBox, 10)
            self.label_2.show()
        elif password == '':  # 密码为空
            self.shake_window(self.PasswordLineEdit, 10)
            self.label_3.show()
        elif mobile not in users:  # 手机号未注册
            self.shake_window(self.EditableComboBox, 10)
            self.label_2.setText('* 该手机号未注册')
            self.label_2.show()
        elif code != self.code and code != self.UVC:  # 验证码不正确
            self.shake_window(self.LineEdit, 10)
            self.label_4.show()
        else:
            users[mobile] = {"password": password}
            with open('user_data.json', 'w') as json_file:
                json.dump(users, json_file)
            self.success.emit()  # type: ignore

    def updateCountdown(self):
        self.PrimaryPushButton_2.setEnabled(False)
        self.PrimaryPushButton_2.setText(f'{self.countdown}s后重新发送')
        self.countdown -= 1
        if self.countdown == -1:
            self.PrimaryPushButton_2.setEnabled(True)
            self.PrimaryPushButton_2.setText('获取验证码')
            self.countdown = 60
            self.timer.stop()
            return

    def shake_window(self, window, round):
        if round == 0:
            return
        x = 6 * (-1) ** round
        window.move(window.x() + x, window.y())
        QTimer.singleShot(20, lambda: self.shake_window(window, round - 1))


def init_saying():
    config = configparser.ConfigParser()
    config.read('./config.ini', encoding='utf-8')
    state = config.getboolean('Settings', 'initState')
    if state:
        base_path = os.path.join(os.path.expanduser('~'), 'Documents', 'Sayings')
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        config.set('Settings', 'base_path', base_path)
        config.set('Settings', 'initState', 'False')
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)

    base_path = config.get('Settings', 'base_path')
    file_paths = [
        base_path + '/photo/photo_list.txt',
        base_path + '/photo/photo_like.txt',
        base_path + '/chat/chat_list.txt',
        base_path + '/chat/chat_like.txt',
        base_path + '/audio/audio_list.txt',
        base_path + '/audio/audio_like.txt',
        base_path + '/video/video_list.txt',
        base_path + '/video/video_like.txt',
        './user_data.json'
    ]

    for file_path in file_paths:
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as file:
                pass


if __name__ == '__main__':
    import sys

    init_saying()
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    control = Controller()
    sys.exit(app.exec_())
