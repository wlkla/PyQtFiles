# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tasktwo.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1152, 704)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("*{\n"
"background-color: black;\n"
"color: rgb(255, 255, 255);\n"
"border-radius:4px;\n"
"border:none;\n"
"font: 12pt \"微软雅黑\";\n"
"}\n"
"")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_5.setContentsMargins(0, 2, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.splitter_2 = QtWidgets.QSplitter(self.splitter)
        self.splitter_2.setStyleSheet("border:none;")
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.question = QtWidgets.QTextEdit(self.splitter_2)
        self.question.setEnabled(True)
        self.question.setMaximumSize(QtCore.QSize(16777215, 310))
        self.question.setStyleSheet("border:2px solid white;\n"
"margin-top:5px;\n"
"margin-left:5px;\n"
"margin-right:5px;\n"
"padding:7px;\n"
"border-radius:17px;\n"
"background-color: rgb(0, 0, 0);")
        self.question.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.question.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.question.setOverwriteMode(False)
        self.question.setObjectName("question")
        self.widget_5 = QtWidgets.QWidget(self.splitter_2)
        self.widget_5.setStyleSheet("background-color:transparent;")
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget_5)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("border:2px solid white;\n"
"border-right:none;\n"
"border-top-left-radius:17px;\n"
"border-bottom-left-radius:17px;\n"
"padding:5px;\n"
"margin-left:7px;\n"
"background-color: rgb(0, 0, 0);\n"
"font: 12pt \"微软雅黑\";")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.dataSet = QtWidgets.QComboBox(self.widget_5)
        self.dataSet.setStyleSheet("border:2px solid white;\n"
"border-left:none;\n"
"border-top-right-radius:17px;\n"
"border-bottom-right-radius:17px;\n"
"padding:5px;\n"
"margin-right:7px;\n"
"background-color: rgb(0, 0, 0);")
        self.dataSet.setObjectName("dataSet")
        self.dataSet.addItem("")
        self.dataSet.addItem("")
        self.dataSet.addItem("")
        self.horizontalLayout.addWidget(self.dataSet)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.getData = QtWidgets.QPushButton(self.widget_5)
        self.getData.setStyleSheet("QPushButton {\n"
"border:2px solid white;\n"
"border-radius:17px;\n"
"padding:5px;\n"
"background-color: rgb(0, 0, 0);\n"
"margin-left:7px;\n"
"margin-right:7px;\n"
"}\n"
"QPushButton:pressed {\n"
"padding-left:7px;\n"
"padding-top:7px;\n"
"}")
        self.getData.setObjectName("getData")
        self.verticalLayout.addWidget(self.getData)
        self.widget_6 = QtWidgets.QWidget(self.widget_5)
        self.widget_6.setStyleSheet("border:none;\n"
"background-color:transparent;")
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(10)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem)
        self.dataContent = QtWidgets.QCheckBox(self.widget_6)
        self.dataContent.setMaximumSize(QtCore.QSize(120, 16777215))
        self.dataContent.setStyleSheet("padding:5px;\n"
"margin-left:7px;\n"
"background-color: rgb(0, 0, 0);")
        self.dataContent.setChecked(True)
        self.dataContent.setObjectName("dataContent")
        self.horizontalLayout_10.addWidget(self.dataContent)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem1)
        self.dataShape = QtWidgets.QCheckBox(self.widget_6)
        self.dataShape.setMaximumSize(QtCore.QSize(120, 16777215))
        self.dataShape.setStyleSheet("padding:5px;\n"
"background-color: rgb(0, 0, 0);")
        self.dataShape.setChecked(True)
        self.dataShape.setObjectName("dataShape")
        self.horizontalLayout_10.addWidget(self.dataShape)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem2)
        self.dataType = QtWidgets.QCheckBox(self.widget_6)
        self.dataType.setMaximumSize(QtCore.QSize(120, 16777215))
        self.dataType.setStyleSheet("padding:5px;\n"
"margin-right:7px;\n"
"background-color: rgb(0, 0, 0);")
        self.dataType.setChecked(True)
        self.dataType.setObjectName("dataType")
        self.horizontalLayout_10.addWidget(self.dataType)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem3)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_10)
        self.verticalLayout.addWidget(self.widget_6)
        self.displayData = QtWidgets.QTextBrowser(self.widget_5)
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.displayData.setFont(font)
        self.displayData.setStyleSheet("padding:5px;\n"
"font: italic 12pt \"Cambria\";\n"
"margin:5px;\n"
"border:2px solid white;\n"
"border-radius:17px;\n"
"background-color: rgb(0, 0, 0);")
        self.displayData.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.displayData.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.displayData.setObjectName("displayData")
        self.verticalLayout.addWidget(self.displayData)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_1 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_1.setFont(font)
        self.label_1.setStyleSheet("border:2px solid white;\n"
"border-right:none;\n"
"border-top-left-radius:17px;\n"
"border-bottom-left-radius:17px;\n"
"padding:5px;\n"
"margin-left:7px;\n"
"background-color: rgb(0, 0, 0);\n"
"font: 12pt \"微软雅黑\";")
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName("label_1")
        self.horizontalLayout_3.addWidget(self.label_1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.solutionSet = QtWidgets.QComboBox(self.layoutWidget)
        self.solutionSet.setStyleSheet("border:2px solid white;\n"
"border-left:none;\n"
"border-bottom:none;\n"
"border-top-right-radius:17px;\n"
"padding:5px;\n"
"margin-right:7px;\n"
"background-color: rgb(0, 0, 0);")
        self.solutionSet.setObjectName("solutionSet")
        self.solutionSet.addItem("")
        self.solutionSet.addItem("")
        self.solutionSet.addItem("")
        self.solutionSet.addItem("")
        self.verticalLayout_3.addWidget(self.solutionSet)
        self.stepSet = QtWidgets.QComboBox(self.layoutWidget)
        self.stepSet.setStyleSheet("border:none;\n"
"border-right:2px solid white;\n"
"padding:5px;\n"
"margin-right:7px;\n"
"background-color: rgb(0, 0, 0);")
        self.stepSet.setObjectName("stepSet")
        self.stepSet.addItem("")
        self.stepSet.addItem("")
        self.stepSet.addItem("")
        self.stepSet.addItem("")
        self.verticalLayout_3.addWidget(self.stepSet)
        self.trainSet = QtWidgets.QComboBox(self.layoutWidget)
        self.trainSet.setStyleSheet("border:2px solid white;\n"
"border-left:none;\n"
"border-top:none;\n"
"border-bottom-right-radius:17px;\n"
"padding:5px;\n"
"margin-right:7px;\n"
"background-color: rgb(0, 0, 0);")
        self.trainSet.setObjectName("trainSet")
        self.trainSet.addItem("")
        self.trainSet.addItem("")
        self.verticalLayout_3.addWidget(self.trainSet)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.codeGo = QtWidgets.QPushButton(self.layoutWidget)
        self.codeGo.setStyleSheet("QPushButton {\n"
"border:2px solid white;\n"
"border-radius:17px;\n"
"padding:5px;\n"
"background-color: rgb(0, 0, 0);\n"
"margin-left:7px;\n"
"margin-right:7px;\n"
"}\n"
"QPushButton:pressed {\n"
"padding-left:7px;\n"
"padding-top:7px;\n"
"}")
        self.codeGo.setObjectName("codeGo")
        self.verticalLayout_5.addWidget(self.codeGo)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.valueImage = QtWidgets.QCheckBox(self.layoutWidget)
        self.valueImage.setStyleSheet("margin-bottom:5px;\n"
"background-color: rgb(0, 0, 0);")
        self.valueImage.setChecked(True)
        self.valueImage.setObjectName("valueImage")
        self.horizontalLayout_6.addWidget(self.valueImage)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.declineImage = QtWidgets.QCheckBox(self.layoutWidget)
        self.declineImage.setStyleSheet("margin-bottom:5px;\n"
"background-color: rgb(0, 0, 0);")
        self.declineImage.setChecked(True)
        self.declineImage.setObjectName("declineImage")
        self.horizontalLayout_6.addWidget(self.declineImage)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.gradImage = QtWidgets.QCheckBox(self.layoutWidget)
        self.gradImage.setStyleSheet("margin-bottom:5px;\n"
"background-color: rgb(0, 0, 0);")
        self.gradImage.setChecked(True)
        self.gradImage.setObjectName("gradImage")
        self.horizontalLayout_6.addWidget(self.gradImage)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem7)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.progressBar = QtWidgets.QProgressBar(self.layoutWidget)
        self.progressBar.setStyleSheet("QProgressBar {\n"
"color:black;\n"
"margin-left:7px;\n"
"margin-right:7px;\n"
"border: 2px solid white;\n"
"border-radius: 17px;\n"
"background-color: gray;\n"
"}\n"
"QProgressBar::chunk {\n"
"background-color: white;\n"
"width: 10px;\n"
"margin: 0.5px;\n"
"}")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.scrollArea = QtWidgets.QScrollArea(self.layoutWidget)
        self.scrollArea.setStyleSheet("margin:7px;\n"
"border:2px solid white;\n"
"border-radius:17px;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 560, 421))
        self.scrollAreaWidgetContents.setStyleSheet("border:none;\n"
"margin:0px;")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.verticalLayout_5.addLayout(self.verticalLayout_2)
        self.horizontalLayout_5.addWidget(self.splitter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "最优化"))
        self.question.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'微软雅黑\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\">问题描述：</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\'; font-size:14pt;\">考虑逻辑回归问题：</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/icon/formule.png\" /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\'; font-size:14pt;\">首先，讨论该问题的性质，比如凸、强凸、梯度Lipschitz连续等。进一步，在LIBSVM上的数据集a9a，CINA，ijcnn训练未知参数x.要求用梯度算法、牛顿算法、L-BFGS算法和信赖域算法解决该问题。初始点、线搜索技巧和参数选取不限，鼓励多尝试几种，并用图片和表格尽可能详细汇报。</span></p></body></html>"))
        self.label.setText(_translate("Form", "请选择数据集："))
        self.dataSet.setItemText(0, _translate("Form", "     a9a"))
        self.dataSet.setItemText(1, _translate("Form", "     CINA"))
        self.dataSet.setItemText(2, _translate("Form", "     ijcnn"))
        self.getData.setText(_translate("Form", "获取数据"))
        self.dataContent.setText(_translate("Form", "数据内容"))
        self.dataShape.setText(_translate("Form", "数据形状"))
        self.dataType.setText(_translate("Form", "数据类型"))
        self.displayData.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Cambria\'; font-size:12pt; font-weight:400; font-style:italic;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Bahnschrift Condensed\'; font-size:9pt; font-style:normal;\"><br /></p></body></html>"))
        self.label_1.setText(_translate("Form", "请选择优化算法："))
        self.solutionSet.setItemText(0, _translate("Form", "     梯度算法"))
        self.solutionSet.setItemText(1, _translate("Form", "     牛顿算法"))
        self.solutionSet.setItemText(2, _translate("Form", "     L-BFGS算法"))
        self.solutionSet.setItemText(3, _translate("Form", "     信赖域算法"))
        self.stepSet.setItemText(0, _translate("Form", "     固定步长"))
        self.stepSet.setItemText(1, _translate("Form", "     Armijo线搜索"))
        self.stepSet.setItemText(2, _translate("Form", "     BB步长"))
        self.stepSet.setItemText(3, _translate("Form", "     Wolfe线搜索"))
        self.trainSet.setItemText(0, _translate("Form", "     重新训练"))
        self.trainSet.setItemText(1, _translate("Form", "     导入已有数据"))
        self.codeGo.setText(_translate("Form", "程序，启动！"))
        self.valueImage.setText(_translate("Form", "函数值图像"))
        self.declineImage.setText(_translate("Form", "下降量图像"))
        self.gradImage.setText(_translate("Form", "梯度范数图像"))
import resource_rc
