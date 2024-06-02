import os
import configparser
from qframelesswindow import TitleBar
from PyQt5.QtCore import Qt, QRect, QModelIndex, QSize, pyqtSignal, QPoint, QDateTime
from PyQt5.QtGui import QImage, QPainter, QColor, QBrush, QFont, QIcon, QFontMetrics, QMouseEvent, QCursor, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QStyleOptionViewItem, QLabel, QHBoxLayout, QWidget, QSpacerItem, \
    QSizePolicy, QPushButton, QApplication, QInputDialog, QLayout, QStackedWidget
from qfluentwidgets import NavigationWidget, FlipImageDelegate, getFont, CardWidget, IconWidget, BodyLabel, \
    CaptionLabel, FluentIcon, ElevatedCardWidget, PrimaryToolButton, ScrollArea, \
    ImageLabel, CommandBarView, Flyout, FlyoutAnimationType, Action, TransparentToolButton, RoundMenu, FlyoutViewBase, \
    PrimaryPushButton


class AvatarWidget(NavigationWidget):
    def __init__(self, parent=None):
        super().__init__(isSelectable=False, parent=parent)
        self.avatar = QImage('resource/shoko.png').scaled(
            24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)

        if self.isEnter:
            painter.setBrush(QColor(0, 0, 0, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

        painter.setBrush(QBrush(self.avatar))
        painter.translate(8, 6)
        painter.drawEllipse(0, 0, 24, 24)
        painter.translate(-8, -6)

        if not self.isCompacted:
            painter.setPen(Qt.black)
            font = QFont('Segoe UI')
            font.setPixelSize(14)
            painter.setFont(font)
            painter.drawText(QRect(44, 0, 255, 36), Qt.AlignVCenter, 'zhiyiYo')


class CustomFlipItemDelegate(FlipImageDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        super().paint(painter, option, index)
        painter.save()

        painter.setBrush(QColor(0, 0, 0, 100))
        painter.setPen(Qt.NoPen)
        rect = option.rect
        rect = QRect(0, 220, 1960, 40)
        painter.drawRect(rect)

        # draw text
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        picture_bottom_text = config.get('Settings', 'picture_bottom_text')
        painter.setPen(Qt.white)
        painter.setFont(getFont(16, QFont.Bold))
        painter.drawText(rect, Qt.AlignVCenter, picture_bottom_text)

        painter.restore()


class CustomTitleBar(TitleBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(20, 20)
        self.hBoxLayout.insertSpacing(0, 10)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.window().windowIconChanged.connect(self.setIcon)  # type: ignore

        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.titleLabel.setObjectName('titleLabel')
        self.titleLabel.setStyleSheet('font-size: 15px;')
        self.window().windowTitleChanged.connect(self.setTitle)  # type: ignore

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(20, 20))


class AppCard(CardWidget):
    play = pyqtSignal(str)
    likeSignal = pyqtSignal(str)
    deleteSignal = pyqtSignal(str)

    def __init__(self, path, content, style, like, parent=None):
        super().__init__(parent)
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        chat_card_icon = config.get('Settings', 'chat_card_icon')
        audio_card_icon = config.get('Settings', 'audio_card_icon')
        video_card_icon = config.get('Settings', 'video_card_icon')

        self.is_liked = like
        self.path = path
        self.Button = PrimaryToolButton(self)
        self.moreButton = TransparentToolButton(FluentIcon.MORE, self)
        if style == 'audio':
            self.Button.setIcon(FluentIcon.MUSIC)
            self.icon = audio_card_icon
        elif style == 'video':
            self.Button.setIcon(FluentIcon.VIDEO)
            self.icon = video_card_icon
        elif style == 'message':
            self.Button.setIcon(FluentIcon.MESSAGE)
            self.icon = chat_card_icon
        self.Button.clicked.connect(lambda: self.play.emit(path))  # type: ignore
        self.iconWidget = IconWidget(QIcon(self.icon))
        file_name = os.path.basename(path)
        title, _ = os.path.splitext(file_name)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.Button.setFixedWidth(120)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.Button, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(25)

        self.moreButton.setFixedSize(32, 32)
        self.moreButton.clicked.connect(self.onMoreButtonClicked)  # type: ignore

        if self.is_liked:
            self.like_action = Action(FluentIcon.EXPRESSIVE_INPUT_ENTRY, 'UnLike', self)
        else:
            self.like_action = Action(FluentIcon.HEART, 'Like', self)
        self.delete_action = Action(FluentIcon.DELETE, 'Delete', self)

    def onMoreButtonClicked(self):
        menu = RoundMenu(parent=self)
        like_action = self.like_action
        delete_action = self.delete_action
        menu.addAction(like_action)
        menu.addAction(delete_action)

        like_action.triggered.connect(lambda: self.likeSignal.emit(self.path))  # type: ignore
        delete_action.triggered.connect(lambda: self.deleteSignal.emit(self.path))  # type: ignore

        x = (self.moreButton.width() - menu.width()) // 2 + 10
        pos = self.moreButton.mapToGlobal(QPoint(x, self.moreButton.height()))
        menu.exec(pos)

    def updateIconOrText(self, card_style):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        chat_card_icon = config.get('Settings', 'chat_card_icon')
        audio_card_icon = config.get('Settings', 'audio_card_icon')
        video_card_icon = config.get('Settings', 'video_card_icon')
        audio_card_content = config.get('Settings', 'audio_card_content')
        video_card_content = config.get('Settings', 'video_card_content')
        # 根据 style 更新图标
        if card_style == 'audio':
            self.icon = audio_card_icon
            self.contentLabel.setText(audio_card_content)
        elif card_style == 'video':
            self.icon = video_card_icon
            self.contentLabel.setText(video_card_content)
        elif card_style == 'message':
            self.icon = chat_card_icon
        self.iconWidget.setIcon(QIcon(self.icon))


class messageBoxMe(QWidget):
    def __init__(self, content, parent=None):
        super().__init__(parent)
        self.horizontalLayout_5 = QHBoxLayout(self)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.widget = QWidget(self)
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QHBoxLayout(self.widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.ElevatedCardWidget = ElevatedCardWidget(self.widget)
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        my_bubble_color_str = config.get('Settings', 'my_bubble_color')
        my_bubble_color = eval(my_bubble_color_str)
        rgb_color = ', '.join(map(str, my_bubble_color))
        self.ElevatedCardWidget.setStyleSheet(
            "#ElevatedCardWidget{background-color: rgb(%s);}" % rgb_color)
        self.ElevatedCardWidget.setObjectName("ElevatedCardWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.ElevatedCardWidget)
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(self.ElevatedCardWidget)
        self.label.setMinimumSize(QSize(10, 0))
        max_width = 300
        self.label.setMaximumSize(QSize(max_width, 16777215))
        self.label.setStyleSheet("font: 11pt \"微软雅黑\";\n"
                                 "border-radius:5px;\n"
                                 "padding-left:4px;\n"
                                 "background-color: rgb(245, 245, 245);")
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setOpenExternalLinks(True)
        self.label.setText(content)
        self.label.setWordWrap(True)
        font = QFont("微软雅黑", 11)
        font_metrics = QFontMetrics(font)
        text_rect = font_metrics.boundingRect(0, 0, max_width, 16777215, Qt.TextWordWrap, content)
        width = min(text_rect.width() + 15, max_width)
        height = text_rect.height() + 15
        self.widget.setFixedHeight(max(height + 10, 37))
        self.label.setFixedSize(width, height)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.avatar = QLabel(self.ElevatedCardWidget)
        self.avatar.setMinimumSize(QSize(37, 37))
        self.avatar.setMaximumSize(QSize(37, 37))
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        avatar_me = config.get('Settings', 'avatar_me')
        self.avatar.setStyleSheet(f"border-image: url({avatar_me});")
        self.avatar.setText("")
        self.avatar.setObjectName("avatar")
        self.verticalLayout.addWidget(self.avatar)
        spacerItem1 = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addWidget(self.ElevatedCardWidget)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5.addWidget(self.widget)


class messageBoxYou(QWidget):
    def __init__(self, content, parent=None):
        super().__init__(parent)
        self.horizontalLayout_5 = QHBoxLayout(self)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.widget = QWidget(self)
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QHBoxLayout(self.widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ElevatedCardWidget = ElevatedCardWidget(self.widget)
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        other_bubble_color_str = config.get('Settings', 'other_bubble_color')
        other_bubble_color = eval(other_bubble_color_str)
        rgb_color = ', '.join(map(str, other_bubble_color))
        self.ElevatedCardWidget.setStyleSheet(
            "#ElevatedCardWidget{background-color: rgb(%s);}" % rgb_color)
        self.ElevatedCardWidget.setObjectName("ElevatedCardWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.ElevatedCardWidget)
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.avatar = QLabel(self.ElevatedCardWidget)
        self.avatar.setMinimumSize(QSize(37, 37))
        self.avatar.setMaximumSize(QSize(37, 37))
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        avatar_other = config.get('Settings', 'avatar_other')
        self.avatar.setStyleSheet(f"border-image: url({avatar_other});")
        self.avatar.setText("")
        self.avatar.setObjectName("avatar")
        self.verticalLayout.addWidget(self.avatar)
        spacerItem = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.label = QLabel(self.ElevatedCardWidget)
        self.label.setMinimumSize(QSize(10, 0))
        max_width = 300
        self.label.setMaximumSize(QSize(max_width, 16777215))
        self.label.setStyleSheet("font: 11pt \"微软雅黑\";\n"
                                 "border-radius:5px;\n"
                                 "padding-left:4px;\n"
                                 "background-color: rgb(245, 245, 245);")
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setOpenExternalLinks(True)
        self.label.setText(content)
        self.label.setWordWrap(True)
        font = QFont("微软雅黑", 11)
        font_metrics = QFontMetrics(font)
        text_rect = font_metrics.boundingRect(0, 0, max_width, 16777215, Qt.TextWordWrap, content)
        width = min(text_rect.width() + 15, max_width)
        height = text_rect.height() + 15
        self.widget.setFixedHeight(max(height + 10, 37))
        self.label.setFixedSize(width, height)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addWidget(self.ElevatedCardWidget)
        spacerItem1 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5.addWidget(self.widget)


class messageWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(700, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.horizontalLayout_4 = QHBoxLayout(self)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget = QWidget(self)
        self.widget.setStyleSheet("#widget {\n"
                                  "background-color: rgb(255, 255, 255);\n"
                                  "border-radius:15px;\n"
                                  "}")
        self.widget.setObjectName("widget")
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QStackedWidget(self.widget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QWidget()
        self.page.setObjectName("page")
        self.horizontalLayout = QHBoxLayout(self.page)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ScrollArea = ScrollArea(self.page)
        self.ScrollArea.setStyleSheet("border:none;")
        self.ScrollArea.setWidgetResizable(True)
        self.ScrollArea.setObjectName("ScrollArea")
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1164, 387))
        self.scrollAreaWidgetContents.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(30, 10, 30, 10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.ScrollArea)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName("page_2")
        self.horizontalLayout_2 = QHBoxLayout(self.page_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ScrollArea_2 = ScrollArea(self.page_2)
        self.ScrollArea_2.setStyleSheet("border:none;")
        self.ScrollArea_2.setWidgetResizable(True)
        self.ScrollArea_2.setObjectName("ScrollArea_2")
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 1164, 387))
        self.scrollAreaWidgetContents_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.setContentsMargins(30, 10, 30, 10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ScrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_2.addWidget(self.ScrollArea_2)
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout.addWidget(self.stackedWidget)
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setStyleSheet("border:2px solid white;\n"
                                      "background-color: #009faa;\n"
                                      "border-radius:7px;\n"
                                      "padding-left:15px;\n"
                                      "padding-right:15px;\n"
                                      "padding-top:5px;\n"
                                      "padding-bottom:5px;\n"
                                      "margin-left:300px;\n"
                                      "margin-right:300px;\n"
                                      "font: 10pt \\\"微软雅黑\\\";")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_4.addWidget(self.widget)
        self.pushButton.setText('关闭')
        self.pushButton.clicked.connect(self.Close)  # type: ignore
        self.initUi()

    def initUi(self):
        rect = QApplication.desktop().availableGeometry()
        w, h = rect.width(), rect.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            # 如果当前显示的是第一个小部件，就切换到第二个小部件
            if self.stackedWidget.currentIndex() == 0:
                self.stackedWidget.setCurrentIndex(1)
            # 否则，切换到第一个小部件
            else:
                self.stackedWidget.setCurrentIndex(0)

    def Close(self):
        self.close()
        while self.verticalLayout_2.count():
            child = self.verticalLayout_2.takeAt(0)
            # 如果子项是一个widget
            if child.widget():
                child.widget().deleteLater()
        while self.verticalLayout_3.count():
            child = self.verticalLayout_3.takeAt(0)
            # 如果子项是一个widget
            if child.widget():
                child.widget().deleteLater()

class newmsgWin(QWidget):
    fileSaved = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(700, 500)
        self.text = None
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.horizontalLayout_4 = QHBoxLayout(self)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget = QWidget(self)
        self.widget.setStyleSheet("#widget {\n"
                                  "background-color: rgb(255, 255, 255);\n"
                                  "border-radius:15px;\n"
                                  "}")
        self.widget.setObjectName("widget")
        self.horizontalLayout_5 = QHBoxLayout(self.widget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QStackedWidget(self.widget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QWidget()
        self.page.setObjectName("page")
        self.horizontalLayout = QHBoxLayout(self.page)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ScrollArea = ScrollArea(self.page)
        self.ScrollArea.setStyleSheet("border:none;")
        self.ScrollArea.setWidgetResizable(True)
        self.ScrollArea.setObjectName("ScrollArea")
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1164, 387))
        self.scrollAreaWidgetContents.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(30, 10, 30, 10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.ScrollArea)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName("page_2")
        self.horizontalLayout_2 = QHBoxLayout(self.page_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ScrollArea_2 = ScrollArea(self.page_2)
        self.ScrollArea_2.setStyleSheet("border:none;")
        self.ScrollArea_2.setWidgetResizable(True)
        self.ScrollArea_2.setObjectName("ScrollArea_2")
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 1164, 387))
        self.scrollAreaWidgetContents_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.setContentsMargins(30, 10, 30, 10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ScrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_2.addWidget(self.ScrollArea_2)
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout.addWidget(self.stackedWidget)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setStyleSheet("border:2px solid white;\n"
                                      "background-color: #009faa;\n"
                                      "border-radius:7px;\n"
                                      "padding-left:15px;\n"
                                      "padding-right:15px;\n"
                                      "padding-top:5px;\n"
                                      "padding-bottom:5px;\n"
                                      "margin-left:300px;\n"
                                      "font: 10pt \\\"微软雅黑\\\";")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setStyleSheet("border:2px solid white;\n"
                                        "background-color: #009faa;\n"
                                        "border-radius:7px;\n"
                                        "padding-left:15px;\n"
                                        "padding-right:15px;\n"
                                        "padding-top:5px;\n"
                                        "padding-bottom:5px;\n"
                                        "margin-right:300px;\n"
                                        "font: 10pt \\\"微软雅黑\\\";")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.horizontalLayout_4.addWidget(self.widget)
        self.pushButton.setText('保存')
        self.pushButton_2.setText('取消')
        self.pushButton.clicked.connect(self.saveFile)  # type: ignore
        self.pushButton_2.clicked.connect(self.close)  # type: ignore
        self.initUi()

    def initUi(self):
        rect = QApplication.desktop().availableGeometry()
        w, h = rect.width(), rect.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

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

    def saveFile(self):
        current_datetime = QDateTime.currentDateTime()
        default_filename = current_datetime.toString("yyyy-MM-dd-HH-mm")
        filename, ok = QInputDialog.getText(self, '保存文件', '请输入文件名', text=default_filename)
        if ok and filename:
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            base_path = config.get('Settings', 'base_path')
            chat_path = base_path + '/chat'
            file_path = chat_path + '/' + filename + '.txt'
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text)
            self.fileSaved.emit(file_path)  # type: ignore
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            # 如果当前显示的是第一个小部件，就切换到第二个小部件
            if self.stackedWidget.currentIndex() == 0:
                self.stackedWidget.setCurrentIndex(1)
            # 否则，切换到第一个小部件
            else:
                self.stackedWidget.setCurrentIndex(0)


class QL(QWidget):
    likeSignal = pyqtSignal(str)
    deleteSignal = pyqtSignal(str)
    zoomInSignal = pyqtSignal(str)

    def __init__(self, picture, like, parent=None, *args, **kwargs):
        super(QL, self).__init__(parent, *args, **kwargs)
        self.image_label = ImageLabel(self)
        self.picture = picture
        self.is_liked = like
        pixmap = QPixmap(self.picture)
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        waterfall_label_width = config.get('Settings', 'waterfall_label_width')
        width = int(waterfall_label_width)
        self.image_label.setMinimumWidth(width)
        self.image_label.setMinimumHeight(int(width * pixmap.height() / pixmap.width()))
        self.image_label.setStyleSheet(f"image:url({self.picture});")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.clicked.connect(self.showCommandBar)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.image_label)

        if self.is_liked:
            self.like_action = Action(FluentIcon.EXPRESSIVE_INPUT_ENTRY, 'UnLike')
        else:
            self.like_action = Action(FluentIcon.HEART, 'Like')

    def showCommandBar(self):
        view = CommandBarView(self)
        like_action = self.like_action
        zoomIn_action = Action(FluentIcon.ZOOM_IN, 'Zoom In')
        delete_action = Action(FluentIcon.DELETE, 'Delete')
        view.addAction(like_action)
        view.addAction(zoomIn_action)
        view.addAction(delete_action)
        view.resizeToSuitableWidth()
        Flyout.make(view, self.image_label, self, FlyoutAnimationType.FADE_IN)

        like_action.triggered.connect(lambda: self.likeSignal.emit(self.picture))  # type: ignore
        delete_action.triggered.connect(lambda: self.deleteSignal.emit(self.picture))  # type: ignore
        zoomIn_action.triggered.connect(lambda: self.zoomInSignal.emit(self.picture))  # type: ignore

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        ratio = self.width() / self.height()
        height = int(self.width() / ratio)
        return height


class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        margin, _, _, _ = self.getContentsMargins()
        size += QSize(2 * margin, 2 * margin)
        return size

    def doLayout(self, rect, testOnly: bool):
        x = rect.x()
        y = rect.y()
        isAtFisrstRow = True
        item_rects = []

        for i, item in enumerate(self.itemList):
            wid = item.widget()
            style_layoutspacing_h = wid.style().layoutSpacing(QSizePolicy.Frame, QSizePolicy.Frame, Qt.Horizontal)
            spaceX = self.spacing() + style_layoutspacing_h
            style_layoutspacing_v = wid.style().layoutSpacing(QSizePolicy.Frame, QSizePolicy.Frame, Qt.Vertical)
            spaceY = self.spacing() + style_layoutspacing_v
            spaceSide = abs(rect.width() - (rect.width() // wid.width()) * wid.width() - (
                    rect.width() // wid.width() - 1) * spaceX) // 2

            if isAtFisrstRow:
                if len(item_rects) == 0:
                    x += spaceSide
                current_item_rect = QRect(QPoint(x, y), item.sizeHint())
                item_rects.append(current_item_rect)
                if not testOnly:
                    item.setGeometry(current_item_rect)
                next_x = current_item_rect.right() + spaceX
                x = next_x
                if next_x + current_item_rect.width() > rect.right():
                    isAtFisrstRow = False
            else:
                shortest_item_rect = min(item_rects, key=lambda item_rect: item_rect.height())
                x = shortest_item_rect.x()
                y = shortest_item_rect.bottom() + spaceY
                current_item_rect = QRect(QPoint(x, y), item.sizeHint())
                item_rects.remove(shortest_item_rect)
                item_rects.append(QRect(shortest_item_rect.topLeft(), current_item_rect.bottomRight()))
                if not testOnly:
                    item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
        if len(item_rects) > 0:
            return max(item_rects, key=lambda x: x.height()).height()
        else:
            return 0
