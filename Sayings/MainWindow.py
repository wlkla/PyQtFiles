import random
from classSet import *
from PyQt5.QtCore import QEventLoop, QTimer
from qframelesswindow import FramelessWindow
from PyQt5.QtWidgets import QApplication, QStackedWidget
from mySplashScreen import SplashScreen as MySplashScreen
from qfluentwidgets import NavigationInterface, NavigationItemPosition, qrouter, MessageBox

from home_Interface import homeInterface
from chat_Interface import chatInterface
from photo_Interface import photoInterface
from audio_Interface import audioInterface
from video_Interface import videoInterface
from setting_Interface import settingInterface


class mainwindow(FramelessWindow):
    exitUi = pyqtSignal()
    changeIcon = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.resize(1100, 750)
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        app_name = config.get('Settings', 'app_name')
        app_icon = config.get('Settings', 'app_icon')
        try:
            poems = list(config['Poems'].values())
            selected_poem = random.choice(poems)
        except:
            selected_poem = '欢迎使用Sayings'
        self.splashScreen = MySplashScreen(QIcon(app_icon), app_name, selected_poem, self)
        self.splashScreen.setIconSize(QSize(204, 204))

        self.setTitleBar(CustomTitleBar(self))
        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True, showReturnButton=True)
        self.stackWidget = QStackedWidget(self)

        self.homeInterface = homeInterface()
        self.photoInterface = photoInterface()
        self.chatInterface = chatInterface()
        self.audioInterface = audioInterface()
        self.videoInterface = videoInterface()
        self.settingInterface = settingInterface()

        self.chatInterface.minWin.connect(self.hide)
        self.chatInterface.norWin.connect(self.showNormal)

        self.initLayout()
        self.initFunction()
        self.initNavigation()
        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)
        self.titleBar.raise_()
        self.navigationInterface.displayModeChanged.connect(self.titleBar.raise_)

    def initFunction(self):
        self.homeInterface.photo.clicked.connect(self.openRelativeUi)
        self.homeInterface.chat.clicked.connect(self.openRelativeUi)
        self.homeInterface.audio.clicked.connect(self.openRelativeUi)
        self.homeInterface.video.clicked.connect(self.openRelativeUi)

        self.homeInterface.updateSignal.connect(self.updateAll)
        self.photoInterface.addPicture.connect(self.addLikedPicture)
        self.chatInterface.addChat.connect(self.addLikedChat)
        self.audioInterface.addAudio.connect(self.addLikedAudio)
        self.videoInterface.addVideo.connect(self.addLikedVideo)
        self.settingInterface.updateName.connect(self.updateName)
        self.settingInterface.updateText.connect(self.updateText)
        self.settingInterface.updateIcon.connect(self.updateIcon)
        self.settingInterface.updateCard.connect(self.updateCard)
        self.settingInterface.updateChat.connect(self.updateChat)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, '主页')
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.photoInterface, FluentIcon.PHOTO, '照片')
        self.addSubInterface(self.chatInterface, FluentIcon.CHAT, '聊天')
        self.addSubInterface(self.audioInterface, FluentIcon.MUSIC_FOLDER, '音频')
        self.addSubInterface(self.videoInterface, FluentIcon.VIDEO, '视频')
        self.navigationInterface.addItem(
            routeKey='avatar',
            icon=FluentIcon.CLOSE,
            text='退出',
            onClick=self.returnLogin,
            position=NavigationItemPosition.BOTTOM,
        )
        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, '设置',
                             position=NavigationItemPosition.BOTTOM)
        qrouter.setDefaultRouteKey(self.stackWidget, self.homeInterface.objectName())
        self.navigationInterface.setExpandWidth(100)
        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)  # type: ignore
        self.stackWidget.setCurrentIndex(0)

    def initWindow(self):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        app_icon = config.get('Settings', 'app_icon')
        app_name = config.get('Settings', 'app_name')
        self.setWindowTitle('  ' + app_name)
        self.setWindowIcon(QIcon(app_icon))
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        rect = QApplication.desktop().availableGeometry()
        w, h = rect.width(), rect.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def addLikedPicture(self):
        self.homeInterface.flip_View.clear()
        self.homeInterface.initPhoto()

    def addLikedChat(self):
        self.clearLayout(self.homeInterface.verticalLayout_5)
        self.homeInterface.initChat()

    def addLikedAudio(self):
        self.clearLayout(self.homeInterface.verticalLayout_4)
        self.homeInterface.initAudio()

    def addLikedVideo(self):
        self.clearLayout(self.homeInterface.verticalLayout_6)
        self.homeInterface.initVideo()

    def updateAll(self):
        self.photoInterface.update()
        self.chatInterface.update()
        self.audioInterface.update()
        self.videoInterface.update()

    def updateName(self, title):
        self.setWindowTitle('  ' + title)

    def updateText(self):
        self.homeInterface.flip_View.update()

    def updateIcon(self, icon):
        self.changeIcon.emit(icon)  # type: ignore
        self.setWindowIcon(QIcon(icon))

    def updateChat(self):
        self.clearLayout(self.chatInterface.verticalLayout_2)
        self.chatInterface.initChat()
        self.addLikedChat()

    def updateCard(self, style):
        layout = ''
        if style == 'audio':
            layout = self.homeInterface.verticalLayout_4
            self.audioInterface.updateAudioCardIcon()
        elif style == 'video':
            layout = self.homeInterface.verticalLayout_6
            self.videoInterface.updateVideoCardIcon()
        elif style == 'message':
            layout = self.homeInterface.verticalLayout_5
            self.chatInterface.updateMessageCardIcon()
        for i in range(layout.count()):  # type: ignore
            widget = layout.itemAt(i).widget()
            if isinstance(widget, AppCard):
                widget.updateIconOrText(style)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def openRelativeUi(self):
        text = self.sender().text()
        if text == 'photo':
            self.stackWidget.setCurrentIndex(1)
        elif text == 'chat':
            self.stackWidget.setCurrentIndex(2)
        elif text == 'audio':
            self.stackWidget.setCurrentIndex(3)
        elif text == 'video':
            self.stackWidget.setCurrentIndex(4)

    def createSubInterface(self):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        duration = config.get('Settings', 'duration')
        self.resize(1100, 750)
        # self.splashScreen.show()
        loop = QEventLoop(self)
        QTimer.singleShot(int(duration), loop.quit)
        loop.exec()

    def returnLogin(self):
        w = MessageBox('退出', '你确定要退出吗？', self)
        w.cancelButton.setText('取消')
        w.yesButton.setText('退出')
        if w.exec():
            self.close()
            self.exitUi.emit()  # type: ignore

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP):
        self.stackWidget.addWidget(interface)

        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text
        )

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())
        qrouter.push(self.stackWidget, widget.objectName())

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width() - 46, self.titleBar.height())
