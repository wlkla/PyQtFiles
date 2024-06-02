from Sayings import *
from MainWindow import *
from qfluentwidgets import InfoBarIcon, InfoBar, InfoBarPosition

from PyQt5.QtGui import QIcon


class Controller:
    def __init__(self):
        super().__init__()
        self.login = loginWindow()
        self.find = findPwdWindow()
        self.main = mainwindow()
        self.InitFunction()

    def InitFunction(self):
        self.Run()
        self.login.toPwdUi.connect(self.PwdUi)
        self.login.success.connect(self.MainUi)
        self.login.fail.connect(self.wrongInfo)
        self.find.toLogUi.connect(self.LogUi)
        self.find.success.connect(self.newPwd)
        self.main.exitUi.connect(self.LogUi)
        self.main.changeIcon.connect(self.changeIcon)

    def Run(self):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        state = config.getboolean('Settings', 'state')
        if state:
            self.main.show()
            self.main.createSubInterface()
            self.main.splashScreen.finish()
            self.login.CheckBox.setChecked(True)
        else:
            self.login.show()

    def show_info_bar(self, parent, title, content, icon):
        info_bar = InfoBar(icon, title, content, position=InfoBarPosition.TOP)
        info_bar.setParent(parent)
        info_bar.show()

    def PwdUi(self):
        self.find.initLabel()
        self.login.close()
        self.find.show()
        self.find.EditableComboBox.setText('')
        self.find.PasswordLineEdit.setText('')
        self.find.LineEdit.setText('')
        self.find.label_2.hide()
        self.find.label_3.hide()
        self.find.label_4.hide()

    def MainUi(self):
        self.login.initLabel()
        self.login.close()
        self.login.timer.stop()
        self.login.countdown = 60
        self.main.show()
        self.main.createSubInterface()
        self.main.splashScreen.finish()
        self.show_info_bar(self.main, '登陆成功', '欢迎回来', InfoBarIcon.SUCCESS)

    def wrongInfo(self):
        self.show_info_bar(self.login, '登陆失败', '账号或密码错误', InfoBarIcon.ERROR)

    def LogUi(self):
        self.find.close()
        self.main.close()
        self.login.show()
        self.login.initLabel()

    def newPwd(self):
        self.find.initLabel()
        self.find.return_login()
        self.show_info_bar(self.login, '修改成功', '请登录', InfoBarIcon.SUCCESS)

    def changeIcon(self, icon):
        self.login.label_5.setStyleSheet(f"border-image: url({icon})")
        self.login.label_6.setStyleSheet(f"border-image: url({icon})")
        self.login.setWindowIcon(QIcon(icon))
        self.find.label_6.setStyleSheet(f"border-image: url({icon})")
        self.find.label_7.setStyleSheet(f"border-image: url({icon})")
        self.find.setWindowIcon(QIcon(icon))
