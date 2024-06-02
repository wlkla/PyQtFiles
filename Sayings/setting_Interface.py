import configparser
import os
import shutil

from qfluentwidgets import ColorPickerButton

from setting import Ui_Form

from PyQt5.QtWidgets import QWidget, QFileDialog

from PyQt5.QtGui import QColor

from PyQt5.QtCore import pyqtSignal


class settingInterface(Ui_Form, QWidget):
    updateName = pyqtSignal(str)
    updateText = pyqtSignal()
    updateIcon = pyqtSignal(str)
    updateCard = pyqtSignal(str)
    updateChat = pyqtSignal()

    def __init__(self):
        super(settingInterface, self).__init__()
        self.setupUi(self)
        self.setObjectName('setting')
        self.initUi()
        self.initFunction()

    def initUi(self):
        self.PushButton_8 = ColorPickerButton(QColor(156, 217, 249), '线条颜色', self.CardWidget_12)
        self.PushButton_8.setObjectName("PushButton_8")
        self.horizontalLayout_25.addWidget(self.PushButton_8)
        self.PushButton_9 = ColorPickerButton(QColor(156, 217, 249), '圆点颜色', self.CardWidget_13)
        self.PushButton_9.setObjectName("PushButton_9")
        self.horizontalLayout_27.addWidget(self.PushButton_9)
        self.PushButton_6 = ColorPickerButton(QColor(255, 170, 0), '聊天框颜色', self.CardWidget_8)
        self.PushButton_6.setObjectName("PushButton_6")
        self.horizontalLayout_17.addWidget(self.PushButton_6)
        self.PushButton_7 = ColorPickerButton(QColor(0, 170, 255), '聊天框颜色', self.CardWidget_9)
        self.PushButton_7.setObjectName("PushButton_7")
        self.horizontalLayout_19.addWidget(self.PushButton_7)

        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        self.app_name = config.get('Settings', 'app_name')
        self.app_icon = config.get('Settings', 'app_icon')
        self.chat_card_icon = config.get('Settings', 'chat_card_icon')
        self.audio_card_icon = config.get('Settings', 'audio_card_icon')
        self.video_card_icon = config.get('Settings', 'video_card_icon')
        self.base_path = config.get('Settings', 'base_path')
        self.picture_bottom_text = config.get('Settings', 'picture_bottom_text')
        self.audio_card_content = config.get('Settings', 'audio_card_content')
        self.video_card_content = config.get('Settings', 'video_card_content')
        self.my_bubble_color = config.get('Settings', 'my_bubble_color')
        self.other_bubble_color = config.get('Settings', 'other_bubble_color')
        self.waterfall_label_width = config.get('Settings', 'waterfall_label_width')
        self.duration = config.get('Settings', 'duration')
        self.line_color = config.get('Settings', 'line_color')
        self.circle_color = config.get('Settings', 'circle_color')
        self.avatar_me = config.get('Settings', 'avatar_me')
        self.avatar_other = config.get('Settings', 'avatar_other')

        self.LineEdit.setText(self.app_name)
        self.LineEdit_2.setText(self.picture_bottom_text)
        self.LineEdit_3.setText(self.audio_card_content)
        self.LineEdit_4.setText(self.video_card_content)
        self.CaptionLabel.setText(self.app_icon)
        self.CaptionLabel_2.setText(self.base_path)
        self.CaptionLabel_3.setText(self.chat_card_icon)
        self.CaptionLabel_4.setText(self.audio_card_icon)
        self.CaptionLabel_5.setText(self.video_card_icon)
        self.CaptionLabel_6.setText(self.avatar_me)
        self.CaptionLabel_7.setText(self.avatar_other)
        self.CompactSpinBox.setValue(int(self.waterfall_label_width))
        self.CompactSpinBox_2.setValue(int(self.duration))
        self.PushButton_8.setColor(QColor(*eval(self.line_color)))
        self.PushButton_9.setColor(QColor(*eval(self.circle_color)))
        self.PushButton_6.setColor(QColor(*eval(self.my_bubble_color)))
        self.PushButton_7.setColor(QColor(*eval(self.other_bubble_color)))

    def initFunction(self):
        self.LineEdit.editingFinished.connect(self.saveAppname)
        self.LineEdit_2.editingFinished.connect(self.savePictureBottomText)
        self.LineEdit_3.editingFinished.connect(self.saveAudioCardContent)
        self.LineEdit_4.editingFinished.connect(self.saveVideoCardContent)
        self.PushButton.clicked.connect(self.setAppIcon)
        self.PushButton_2.clicked.connect(self.choseFolder)
        self.PushButton_3.clicked.connect(self.choseChatCardIcon)
        self.PushButton_4.clicked.connect(self.choseAudioCardIcon)
        self.PushButton_5.clicked.connect(self.choseVideoCardIcon)
        self.PushButton_6.colorChanged.connect(self.saveMyBubbleColor)
        self.PushButton_7.colorChanged.connect(self.saveOtherBubbleColor)
        self.PushButton_8.colorChanged.connect(self.saveLineColor)
        self.PushButton_9.colorChanged.connect(self.saveCircleColor)
        self.PushButton_10.clicked.connect(self.choseAvatarMe)
        self.PushButton_11.clicked.connect(self.choseAvatarOther)
        self.CompactSpinBox.valueChanged.connect(self.saveWaterfallLabelWidth)
        self.CompactSpinBox_2.valueChanged.connect(self.saveDuration)

    def saveAppname(self):
        app_name = self.LineEdit.text()
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        config.set('Settings', 'app_name', app_name)
        with open('config.ini', 'w', encoding='utf-8') as f:
            config.write(f)

        self.updateName.emit(app_name)  # type: ignore

    def savePictureBottomText(self):
        picture_bottom_text = self.LineEdit_2.text()
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        config.set('Settings', 'picture_bottom_text', picture_bottom_text)
        with open('config.ini', 'w', encoding='utf-8') as f:
            config.write(f)

        self.updateText.emit()  # type: ignore

    def saveAudioCardContent(self):
        audio_card_content = self.LineEdit_3.text()
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        config.set('Settings', 'audio_card_content', audio_card_content)
        with open('config.ini', 'w', encoding='utf-8') as f:
            config.write(f)
        self.updateCard.emit('audio')  # type: ignore

    def saveVideoCardContent(self):
        video_card_content = self.LineEdit_4.text()
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        config.set('Settings', 'video_card_content', video_card_content)
        with open('config.ini', 'w', encoding='utf-8') as f:
            config.write(f)
        self.updateCard.emit('video')  # type: ignore

    def setAppIcon(self):
        app_icon, ok = QFileDialog.getOpenFileName(self, '选择图标', '', '图标文件(*.ico *.png *.jpg *.jpeg)')
        if ok:
            self.CaptionLabel.setText(app_icon)
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            config.set('Settings', 'app_icon', app_icon)
            with open('config.ini', 'w', encoding='utf-8') as f:
                config.write(f)

            self.updateIcon.emit(app_icon)  # type: ignore

    def choseFolder(self):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        base_path = config.get('Settings', 'base_path')
        new_path = QFileDialog.getExistingDirectory(self, "选择新的存储位置")
        if new_path:
            self.CaptionLabel_2.setText(new_path)
            for filename in os.listdir(base_path):
                shutil.move(os.path.join(base_path, filename), new_path)
            config.set('Settings', 'base_path', new_path)
            with open('config.ini', 'w', encoding='utf-8') as configfile:
                config.write(configfile)
            for file_name in ['chat_list.txt', 'chat_like.txt']:
                file_path = os.path.join(new_path, 'chat', file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                with open(file_path, 'w', encoding='utf-8') as file:
                    for line in lines:
                        new_line = line.replace(base_path, new_path)
                        file.write(new_line)
            self.updateChat.emit()  # type: ignore

    def choseChatCardIcon(self):
        chat_icon, ok = QFileDialog.getOpenFileName(self, '选择图标', '', '图标文件(*.ico *.png *.jpg *.jpeg)')
        if ok:
            self.CaptionLabel_3.setText(chat_icon)
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            config.set('Settings', 'chat_card_icon', chat_icon)
            with open('config.ini', 'w', encoding='utf-8') as f:
                config.write(f)

            self.updateCard.emit('message')  # type: ignore

    def choseAudioCardIcon(self):
        audio_icon, ok = QFileDialog.getOpenFileName(self, '选择图标', '', '图标文件(*.ico *.png *.jpg *.jpeg)')
        if ok:
            self.CaptionLabel_4.setText(audio_icon)
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            config.set('Settings', 'audio_card_icon', audio_icon)
            with open('config.ini', 'w', encoding='utf-8') as f:
                config.write(f)

            self.updateCard.emit('audio')  # type: ignore

    def choseVideoCardIcon(self):
        video_icon, ok = QFileDialog.getOpenFileName(self, '选择图标', '', '图标文件(*.ico *.png *.jpg *.jpeg)')
        if ok:
            self.CaptionLabel_5.setText(video_icon)
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            config.set('Settings', 'video_card_icon', video_icon)
            with open('config.ini', 'w', encoding='utf-8') as f:
                config.write(f)

            self.updateCard.emit('video')  # type: ignore

    def saveMyBubbleColor(self):
        r, g, b, _ = self.PushButton_6.color.getRgb()
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        config.set('Settings', 'my_bubble_color', str((r, g, b)))
        with open('config.ini', 'w', encoding='utf-8') as f:
            config.write(f)

    def saveOtherBubbleColor(self):
        r, g, b, _ = self.PushButton_7.color.getRgb()
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        config.set('Settings', 'other_bubble_color', str((r, g, b)))
        with open('config.ini', 'w', encoding='utf-8') as f:
            config.write(f)

    def saveLineColor(self):
        r, g, b, _ = self.PushButton_8.color.getRgb()
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        config.set('Settings', 'line_color', str((r, g, b)))
        with open('config.ini', 'w', encoding='utf-8') as f:
            config.write(f)

    def saveCircleColor(self):
        r, g, b, _ = self.PushButton_9.color.getRgb()
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        config.set('Settings', 'circle_color', str((r, g, b)))
        with open('config.ini', 'w', encoding='utf-8') as f:
            config.write(f)

    def choseAvatarMe(self):
        avatar_me, ok = QFileDialog.getOpenFileName(self, '选择头像', '', '图片文件(*.png *.jpg *.jpeg)')
        if ok:
            self.CaptionLabel_6.setText(avatar_me)
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            config.set('Settings', 'avatar_me', avatar_me)
            with open('config.ini', 'w', encoding='utf-8') as f:
                config.write(f)

    def choseAvatarOther(self):
        avatar_other, ok = QFileDialog.getOpenFileName(self, '选择头像', '', '图片文件(*.png *.jpg *.jpeg)')
        if ok:
            self.CaptionLabel_7.setText(avatar_other)
            config = configparser.ConfigParser()
            config.read('./config.ini', encoding='utf-8')
            config.set('Settings', 'avatar_other', avatar_other)
            with open('config.ini', 'w', encoding='utf-8') as f:
                config.write(f)

    def saveWaterfallLabelWidth(self):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        config.set('Settings', 'waterfall_label_width', str(self.CompactSpinBox.value()))
        with open('config.ini', 'w', encoding='utf-8') as f:
            config.write(f)

    def saveDuration(self):
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        config.set('Settings', 'duration', str(self.CompactSpinBox_2.value()))
        with open('config.ini', 'w', encoding='utf-8') as f:
            config.write(f)
