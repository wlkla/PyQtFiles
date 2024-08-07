# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(515, 1500)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(10, 50, 10, 20)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ScrollArea = ScrollArea(self.widget)
        self.ScrollArea.setStyleSheet("border:none;")
        self.ScrollArea.setWidgetResizable(True)
        self.ScrollArea.setObjectName("ScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 477, 1444))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setStyleSheet("#groupBox {\n"
"    font: 12pt \"微软雅黑\";\n"
"}")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_8.addItem(spacerItem)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.CardWidget = CardWidget(self.groupBox)
        self.CardWidget.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.CardWidget.setObjectName("CardWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.CardWidget)
        self.horizontalLayout_3.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.StrongBodyLabel = StrongBodyLabel(self.CardWidget)
        self.StrongBodyLabel.setObjectName("StrongBodyLabel")
        self.horizontalLayout_2.addWidget(self.StrongBodyLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.LineEdit = LineEdit(self.CardWidget)
        self.LineEdit.setMaximumSize(QtCore.QSize(200, 33))
        self.LineEdit.setText("")
        self.LineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.LineEdit.setObjectName("LineEdit")
        self.horizontalLayout_2.addWidget(self.LineEdit)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_7.addWidget(self.CardWidget)
        self.CardWidget_2 = CardWidget(self.groupBox)
        self.CardWidget_2.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_2.setObjectName("CardWidget_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.CardWidget_2)
        self.horizontalLayout_5.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.StrongBodyLabel_2 = StrongBodyLabel(self.CardWidget_2)
        self.StrongBodyLabel_2.setObjectName("StrongBodyLabel_2")
        self.verticalLayout_2.addWidget(self.StrongBodyLabel_2)
        self.CaptionLabel = CaptionLabel(self.CardWidget_2)
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.verticalLayout_2.addWidget(self.CaptionLabel)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.PushButton = PushButton(self.CardWidget_2)
        self.PushButton.setObjectName("PushButton")
        self.horizontalLayout_4.addWidget(self.PushButton)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.verticalLayout_7.addWidget(self.CardWidget_2)
        self.CardWidget_3 = CardWidget(self.groupBox)
        self.CardWidget_3.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_3.setObjectName("CardWidget_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.CardWidget_3)
        self.horizontalLayout_6.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.StrongBodyLabel_3 = StrongBodyLabel(self.CardWidget_3)
        self.StrongBodyLabel_3.setObjectName("StrongBodyLabel_3")
        self.verticalLayout_3.addWidget(self.StrongBodyLabel_3)
        self.CaptionLabel_2 = CaptionLabel(self.CardWidget_3)
        self.CaptionLabel_2.setObjectName("CaptionLabel_2")
        self.verticalLayout_3.addWidget(self.CaptionLabel_2)
        self.horizontalLayout_7.addLayout(self.verticalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.PushButton_2 = PushButton(self.CardWidget_3)
        self.PushButton_2.setObjectName("PushButton_2")
        self.horizontalLayout_7.addWidget(self.PushButton_2)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_7)
        self.verticalLayout_7.addWidget(self.CardWidget_3)
        self.verticalLayout_8.addLayout(self.verticalLayout_7)
        self.verticalLayout_13.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setStyleSheet("#groupBox_3 {\n"
"    font: 12pt \"微软雅黑\";\n"
"}")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        spacerItem4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_10.addItem(spacerItem4)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.CardWidget_11 = CardWidget(self.groupBox_3)
        self.CardWidget_11.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_11.setObjectName("CardWidget_11")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout(self.CardWidget_11)
        self.horizontalLayout_22.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.StrongBodyLabel_11 = StrongBodyLabel(self.CardWidget_11)
        self.StrongBodyLabel_11.setObjectName("StrongBodyLabel_11")
        self.horizontalLayout_23.addWidget(self.StrongBodyLabel_11)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_23.addItem(spacerItem5)
        self.CompactSpinBox_2 = CompactSpinBox(self.CardWidget_11)
        self.CompactSpinBox_2.setMinimum(3000)
        self.CompactSpinBox_2.setMaximum(10000)
        self.CompactSpinBox_2.setSingleStep(100)
        self.CompactSpinBox_2.setProperty("value", 3000)
        self.CompactSpinBox_2.setObjectName("CompactSpinBox_2")
        self.horizontalLayout_23.addWidget(self.CompactSpinBox_2)
        self.horizontalLayout_22.addLayout(self.horizontalLayout_23)
        self.verticalLayout_9.addWidget(self.CardWidget_11)
        self.CardWidget_12 = CardWidget(self.groupBox_3)
        self.CardWidget_12.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_12.setObjectName("CardWidget_12")
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout(self.CardWidget_12)
        self.horizontalLayout_24.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.StrongBodyLabel_12 = StrongBodyLabel(self.CardWidget_12)
        self.StrongBodyLabel_12.setObjectName("StrongBodyLabel_12")
        self.horizontalLayout_25.addWidget(self.StrongBodyLabel_12)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_25.addItem(spacerItem6)
        self.horizontalLayout_24.addLayout(self.horizontalLayout_25)
        self.verticalLayout_9.addWidget(self.CardWidget_12)
        self.CardWidget_13 = CardWidget(self.groupBox_3)
        self.CardWidget_13.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_13.setObjectName("CardWidget_13")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout(self.CardWidget_13)
        self.horizontalLayout_26.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.StrongBodyLabel_13 = StrongBodyLabel(self.CardWidget_13)
        self.StrongBodyLabel_13.setObjectName("StrongBodyLabel_13")
        self.horizontalLayout_27.addWidget(self.StrongBodyLabel_13)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_27.addItem(spacerItem7)
        self.horizontalLayout_26.addLayout(self.horizontalLayout_27)
        self.verticalLayout_9.addWidget(self.CardWidget_13)
        self.verticalLayout_10.addLayout(self.verticalLayout_9)
        self.verticalLayout_13.addWidget(self.groupBox_3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setStyleSheet("#groupBox_2 {\n"
"    font: 12pt \"微软雅黑\";\n"
"}")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        spacerItem8 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_11.addItem(spacerItem8)
        self.CardWidget_4 = CardWidget(self.groupBox_2)
        self.CardWidget_4.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_4.setObjectName("CardWidget_4")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.CardWidget_4)
        self.horizontalLayout_8.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.StrongBodyLabel_4 = StrongBodyLabel(self.CardWidget_4)
        self.StrongBodyLabel_4.setObjectName("StrongBodyLabel_4")
        self.verticalLayout_4.addWidget(self.StrongBodyLabel_4)
        self.CaptionLabel_3 = CaptionLabel(self.CardWidget_4)
        self.CaptionLabel_3.setObjectName("CaptionLabel_3")
        self.verticalLayout_4.addWidget(self.CaptionLabel_3)
        self.horizontalLayout_9.addLayout(self.verticalLayout_4)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem9)
        self.PushButton_3 = PushButton(self.CardWidget_4)
        self.PushButton_3.setObjectName("PushButton_3")
        self.horizontalLayout_9.addWidget(self.PushButton_3)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_9)
        self.verticalLayout_11.addWidget(self.CardWidget_4)
        self.CardWidget_5 = CardWidget(self.groupBox_2)
        self.CardWidget_5.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_5.setObjectName("CardWidget_5")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.CardWidget_5)
        self.horizontalLayout_10.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.StrongBodyLabel_5 = StrongBodyLabel(self.CardWidget_5)
        self.StrongBodyLabel_5.setObjectName("StrongBodyLabel_5")
        self.verticalLayout_5.addWidget(self.StrongBodyLabel_5)
        self.CaptionLabel_4 = CaptionLabel(self.CardWidget_5)
        self.CaptionLabel_4.setObjectName("CaptionLabel_4")
        self.verticalLayout_5.addWidget(self.CaptionLabel_4)
        self.horizontalLayout_11.addLayout(self.verticalLayout_5)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem10)
        self.PushButton_4 = PushButton(self.CardWidget_5)
        self.PushButton_4.setObjectName("PushButton_4")
        self.horizontalLayout_11.addWidget(self.PushButton_4)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_11)
        self.verticalLayout_11.addWidget(self.CardWidget_5)
        self.CardWidget_6 = CardWidget(self.groupBox_2)
        self.CardWidget_6.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_6.setObjectName("CardWidget_6")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.CardWidget_6)
        self.horizontalLayout_12.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.StrongBodyLabel_6 = StrongBodyLabel(self.CardWidget_6)
        self.StrongBodyLabel_6.setObjectName("StrongBodyLabel_6")
        self.verticalLayout_6.addWidget(self.StrongBodyLabel_6)
        self.CaptionLabel_5 = CaptionLabel(self.CardWidget_6)
        self.CaptionLabel_5.setObjectName("CaptionLabel_5")
        self.verticalLayout_6.addWidget(self.CaptionLabel_5)
        self.horizontalLayout_13.addLayout(self.verticalLayout_6)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem11)
        self.PushButton_5 = PushButton(self.CardWidget_6)
        self.PushButton_5.setObjectName("PushButton_5")
        self.horizontalLayout_13.addWidget(self.PushButton_5)
        self.horizontalLayout_12.addLayout(self.horizontalLayout_13)
        self.verticalLayout_11.addWidget(self.CardWidget_6)
        self.CardWidget_7 = CardWidget(self.groupBox_2)
        self.CardWidget_7.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_7.setObjectName("CardWidget_7")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.CardWidget_7)
        self.horizontalLayout_14.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.StrongBodyLabel_7 = StrongBodyLabel(self.CardWidget_7)
        self.StrongBodyLabel_7.setObjectName("StrongBodyLabel_7")
        self.horizontalLayout_15.addWidget(self.StrongBodyLabel_7)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem12)
        self.LineEdit_2 = LineEdit(self.CardWidget_7)
        self.LineEdit_2.setMaximumSize(QtCore.QSize(200, 33))
        self.LineEdit_2.setText("")
        self.LineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.LineEdit_2.setObjectName("LineEdit_2")
        self.horizontalLayout_15.addWidget(self.LineEdit_2)
        self.horizontalLayout_14.addLayout(self.horizontalLayout_15)
        self.verticalLayout_11.addWidget(self.CardWidget_7)
        self.CardWidget_16 = CardWidget(self.groupBox_2)
        self.CardWidget_16.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_16.setObjectName("CardWidget_16")
        self.horizontalLayout_36 = QtWidgets.QHBoxLayout(self.CardWidget_16)
        self.horizontalLayout_36.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_36.setObjectName("horizontalLayout_36")
        self.horizontalLayout_37 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_37.setObjectName("horizontalLayout_37")
        self.StrongBodyLabel_18 = StrongBodyLabel(self.CardWidget_16)
        self.StrongBodyLabel_18.setObjectName("StrongBodyLabel_18")
        self.horizontalLayout_37.addWidget(self.StrongBodyLabel_18)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_37.addItem(spacerItem13)
        self.LineEdit_3 = LineEdit(self.CardWidget_16)
        self.LineEdit_3.setMaximumSize(QtCore.QSize(200, 33))
        self.LineEdit_3.setText("")
        self.LineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.LineEdit_3.setObjectName("LineEdit_3")
        self.horizontalLayout_37.addWidget(self.LineEdit_3)
        self.horizontalLayout_36.addLayout(self.horizontalLayout_37)
        self.verticalLayout_11.addWidget(self.CardWidget_16)
        self.CardWidget_17 = CardWidget(self.groupBox_2)
        self.CardWidget_17.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_17.setObjectName("CardWidget_17")
        self.horizontalLayout_38 = QtWidgets.QHBoxLayout(self.CardWidget_17)
        self.horizontalLayout_38.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_38.setObjectName("horizontalLayout_38")
        self.horizontalLayout_39 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_39.setObjectName("horizontalLayout_39")
        self.StrongBodyLabel_19 = StrongBodyLabel(self.CardWidget_17)
        self.StrongBodyLabel_19.setObjectName("StrongBodyLabel_19")
        self.horizontalLayout_39.addWidget(self.StrongBodyLabel_19)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_39.addItem(spacerItem14)
        self.LineEdit_4 = LineEdit(self.CardWidget_17)
        self.LineEdit_4.setMaximumSize(QtCore.QSize(200, 33))
        self.LineEdit_4.setText("")
        self.LineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        self.LineEdit_4.setObjectName("LineEdit_4")
        self.horizontalLayout_39.addWidget(self.LineEdit_4)
        self.horizontalLayout_38.addLayout(self.horizontalLayout_39)
        self.verticalLayout_11.addWidget(self.CardWidget_17)
        self.CardWidget_14 = CardWidget(self.groupBox_2)
        self.CardWidget_14.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_14.setObjectName("CardWidget_14")
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout(self.CardWidget_14)
        self.horizontalLayout_28.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.StrongBodyLabel_14 = StrongBodyLabel(self.CardWidget_14)
        self.StrongBodyLabel_14.setObjectName("StrongBodyLabel_14")
        self.verticalLayout_15.addWidget(self.StrongBodyLabel_14)
        self.CaptionLabel_6 = CaptionLabel(self.CardWidget_14)
        self.CaptionLabel_6.setObjectName("CaptionLabel_6")
        self.verticalLayout_15.addWidget(self.CaptionLabel_6)
        self.horizontalLayout_29.addLayout(self.verticalLayout_15)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_29.addItem(spacerItem15)
        self.PushButton_10 = PushButton(self.CardWidget_14)
        self.PushButton_10.setObjectName("PushButton_10")
        self.horizontalLayout_29.addWidget(self.PushButton_10)
        self.horizontalLayout_28.addLayout(self.horizontalLayout_29)
        self.verticalLayout_11.addWidget(self.CardWidget_14)
        self.CardWidget_15 = CardWidget(self.groupBox_2)
        self.CardWidget_15.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_15.setObjectName("CardWidget_15")
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout(self.CardWidget_15)
        self.horizontalLayout_30.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.StrongBodyLabel_15 = StrongBodyLabel(self.CardWidget_15)
        self.StrongBodyLabel_15.setObjectName("StrongBodyLabel_15")
        self.verticalLayout_16.addWidget(self.StrongBodyLabel_15)
        self.CaptionLabel_7 = CaptionLabel(self.CardWidget_15)
        self.CaptionLabel_7.setObjectName("CaptionLabel_7")
        self.verticalLayout_16.addWidget(self.CaptionLabel_7)
        self.horizontalLayout_31.addLayout(self.verticalLayout_16)
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_31.addItem(spacerItem16)
        self.PushButton_11 = PushButton(self.CardWidget_15)
        self.PushButton_11.setObjectName("PushButton_11")
        self.horizontalLayout_31.addWidget(self.PushButton_11)
        self.horizontalLayout_30.addLayout(self.horizontalLayout_31)
        self.verticalLayout_11.addWidget(self.CardWidget_15)
        self.CardWidget_8 = CardWidget(self.groupBox_2)
        self.CardWidget_8.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_8.setObjectName("CardWidget_8")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.CardWidget_8)
        self.horizontalLayout_16.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.StrongBodyLabel_8 = StrongBodyLabel(self.CardWidget_8)
        self.StrongBodyLabel_8.setObjectName("StrongBodyLabel_8")
        self.horizontalLayout_17.addWidget(self.StrongBodyLabel_8)
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem17)
        self.horizontalLayout_16.addLayout(self.horizontalLayout_17)
        self.verticalLayout_11.addWidget(self.CardWidget_8)
        self.CardWidget_9 = CardWidget(self.groupBox_2)
        self.CardWidget_9.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_9.setObjectName("CardWidget_9")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.CardWidget_9)
        self.horizontalLayout_18.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.StrongBodyLabel_9 = StrongBodyLabel(self.CardWidget_9)
        self.StrongBodyLabel_9.setObjectName("StrongBodyLabel_9")
        self.horizontalLayout_19.addWidget(self.StrongBodyLabel_9)
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem18)
        self.horizontalLayout_18.addLayout(self.horizontalLayout_19)
        self.verticalLayout_11.addWidget(self.CardWidget_9)
        self.CardWidget_10 = CardWidget(self.groupBox_2)
        self.CardWidget_10.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_10.setObjectName("CardWidget_10")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(self.CardWidget_10)
        self.horizontalLayout_20.setContentsMargins(40, -1, 40, -1)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.StrongBodyLabel_10 = StrongBodyLabel(self.CardWidget_10)
        self.StrongBodyLabel_10.setObjectName("StrongBodyLabel_10")
        self.horizontalLayout_21.addWidget(self.StrongBodyLabel_10)
        self.pushButton = QtWidgets.QPushButton(self.CardWidget_10)
        self.pushButton.setMinimumSize(QtCore.QSize(14, 14))
        self.pushButton.setStyleSheet("border-radius:7px;\n"
"background-color: rgb(232, 232, 232);")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_21.addWidget(self.pushButton)
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_21.addItem(spacerItem19)
        self.CompactSpinBox = CompactSpinBox(self.CardWidget_10)
        self.CompactSpinBox.setMinimum(200)
        self.CompactSpinBox.setMaximum(350)
        self.CompactSpinBox.setSingleStep(10)
        self.CompactSpinBox.setProperty("value", 300)
        self.CompactSpinBox.setObjectName("CompactSpinBox")
        self.horizontalLayout_21.addWidget(self.CompactSpinBox)
        self.horizontalLayout_20.addLayout(self.horizontalLayout_21)
        self.verticalLayout_11.addWidget(self.CardWidget_10)
        self.verticalLayout_12.addLayout(self.verticalLayout_11)
        self.verticalLayout_13.addWidget(self.groupBox_2)
        self.verticalLayout_14.addLayout(self.verticalLayout_13)
        self.ScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.ScrollArea)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "软件设置"))
        self.StrongBodyLabel.setText(_translate("Form", "软件名称"))
        self.StrongBodyLabel_2.setText(_translate("Form", "软件图标"))
        self.CaptionLabel.setText(_translate("Form", "Caption label"))
        self.PushButton.setText(_translate("Form", "选取图标"))
        self.StrongBodyLabel_3.setText(_translate("Form", "保存文件路径"))
        self.CaptionLabel_2.setText(_translate("Form", "Caption label"))
        self.PushButton_2.setText(_translate("Form", "选择文件夹"))
        self.groupBox_3.setTitle(_translate("Form", "启动界面设置"))
        self.StrongBodyLabel_11.setText(_translate("Form", "持续时间(ms)"))
        self.StrongBodyLabel_12.setText(_translate("Form", "线条颜色"))
        self.StrongBodyLabel_13.setText(_translate("Form", "圆点颜色"))
        self.groupBox_2.setTitle(_translate("Form", "卡片设置"))
        self.StrongBodyLabel_4.setText(_translate("Form", "聊天卡片图标"))
        self.CaptionLabel_3.setText(_translate("Form", "Caption label"))
        self.PushButton_3.setText(_translate("Form", "选取图标"))
        self.StrongBodyLabel_5.setText(_translate("Form", "音频卡片图标"))
        self.CaptionLabel_4.setText(_translate("Form", "Caption label"))
        self.PushButton_4.setText(_translate("Form", "选取图标"))
        self.StrongBodyLabel_6.setText(_translate("Form", "视频卡片图标"))
        self.CaptionLabel_5.setText(_translate("Form", "Caption label"))
        self.PushButton_5.setText(_translate("Form", "选取图标"))
        self.StrongBodyLabel_7.setText(_translate("Form", "图片卡片底部文字"))
        self.StrongBodyLabel_18.setText(_translate("Form", "音频卡片底部文字"))
        self.StrongBodyLabel_19.setText(_translate("Form", "视频卡片底部文字"))
        self.StrongBodyLabel_14.setText(_translate("Form", "己方聊天框头像"))
        self.CaptionLabel_6.setText(_translate("Form", "Caption label"))
        self.PushButton_10.setText(_translate("Form", "选取图标"))
        self.StrongBodyLabel_15.setText(_translate("Form", "对方聊天框头像"))
        self.CaptionLabel_7.setText(_translate("Form", "Caption label"))
        self.PushButton_11.setText(_translate("Form", "选取图标"))
        self.StrongBodyLabel_8.setText(_translate("Form", "己方聊天框颜色设置"))
        self.StrongBodyLabel_9.setText(_translate("Form", "对方聊天框颜色设置"))
        self.StrongBodyLabel_10.setText(_translate("Form", "瀑布流卡片宽度"))
        self.pushButton.setToolTip(_translate("Form", "该修改需要重启生效"))
        self.pushButton.setText(_translate("Form", "?"))
from qfluentwidgets import CaptionLabel, CardWidget, CompactSpinBox, LineEdit, PushButton, ScrollArea, StrongBodyLabel
