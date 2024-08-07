# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 100)
        Form.setMinimumSize(QtCore.QSize(400, 100))
        Form.setMaximumSize(QtCore.QSize(400, 100))
        Form.setStyleSheet("")
        self.widget_1 = QtWidgets.QWidget(Form)
        self.widget_1.setGeometry(QtCore.QRect(0, 0, 400, 100))
        self.widget_1.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget_1.setStyleSheet("#widget_1{\n"
"background-color: qlineargradient(spread:pad, x1:0.102273, y1:0.102, x2:1, y2:1, stop:0 rgba(94, 252, 232, 255), stop:1 rgba(115, 110, 254, 255));\n"
"border-radius:20px;\n"
"}")
        self.widget_1.setObjectName("widget_1")
        self.progressBar = QtWidgets.QProgressBar(self.widget_1)
        self.progressBar.setGeometry(QtCore.QRect(160, 70, 201, 8))
        self.progressBar.setMinimumSize(QtCore.QSize(0, 8))
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 8))
        self.progressBar.setStyleSheet("QProgressBar {\n"
"    border:1px solid gray;\n"
"    border-radius:4px;\n"
"}\n"
"QProgressBar::chunk {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(10, 234, 216, 255), stop:1 rgba(72, 100, 234, 255));\n"
"}")
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.widget_1)
        self.label.setGeometry(QtCore.QRect(220, 20, 94, 20))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_6 = QtWidgets.QLabel(self.widget_1)
        self.label_6.setGeometry(QtCore.QRect(31, 20, 91, 61))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.widget_2 = QtWidgets.QWidget(Form)
        self.widget_2.setGeometry(QtCore.QRect(0, 0, 400, 100))
        self.widget_2.setStyleSheet("#widget_2{\n"
"background-color: qlineargradient(spread:pad, x1:0.102273, y1:0.102, x2:1, y2:1, stop:0 rgba(94, 252, 232, 255), stop:1 rgba(115, 110, 254, 255));\n"
"border-radius:20px;\n"
"}")
        self.widget_2.setObjectName("widget_2")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setGeometry(QtCore.QRect(30, 30, 41, 41))
        self.label_2.setStyleSheet("border-image: url(:/icon/Document/Downloads/雷达扫描.png);\n"
"")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setGeometry(QtCore.QRect(90, 35, 291, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.widget_0 = QtWidgets.QWidget(Form)
        self.widget_0.setGeometry(QtCore.QRect(0, 0, 400, 100))
        self.widget_0.setStyleSheet("#widget_0{\n"
"background-color: qlineargradient(spread:pad, x1:0.102273, y1:0.102, x2:1, y2:1, stop:0 rgba(94, 252, 232, 255), stop:1 rgba(115, 110, 254, 255));\n"
"border-radius:20px;\n"
"}")
        self.widget_0.setObjectName("widget_0")
        self.label_7 = QtWidgets.QLabel(self.widget_0)
        self.label_7.setGeometry(QtCore.QRect(20, 16, 70, 70))
        self.label_7.setStyleSheet("")
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.widget_0)
        self.label_8.setGeometry(QtCore.QRect(90, 35, 301, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_8.setObjectName("label_8")
        self.btn = QtWidgets.QPushButton(Form)
        self.btn.setGeometry(QtCore.QRect(370, 5, 25, 25))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        font.setBold(True)
        self.btn.setFont(font)
        self.btn.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    color:white;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: transparent;\n"
"    color:red;\n"
"}")
        self.btn.setObjectName("btn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "上传中..."))
        self.label_3.setText(_translate("Form", "图片上传完毕，10个成功，20个失败。"))
        self.label_8.setText(_translate("Form", "正在扫描，已检测到0个图像文件。"))
        self.btn.setText(_translate("Form", "×"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
