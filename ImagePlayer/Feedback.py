from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTextEdit, QPushButton


class FeedbackDialog(QDialog):
    def __init__(self, parent=None):
        super(FeedbackDialog, self).__init__(parent)
        self.setWindowTitle('反馈')

        self.layout = QVBoxLayout(self)

        self.contact_info = QLineEdit(self)
        self.contact_info.setPlaceholderText('请输入您的联系方式')
        self.layout.addWidget(self.contact_info)

        self.feedback = QTextEdit(self)
        self.feedback.setPlaceholderText('请输入您的反馈')
        self.layout.addWidget(self.feedback)

        self.submit_button = QPushButton('提交', self)
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

        self.cancel_button = QPushButton('取消', self)
        self.cancel_button.clicked.connect(self.close)
        self.layout.addWidget(self.cancel_button)

    def submit(self):
        contact_info = self.contact_info.text()
        feedback = self.feedback.toPlainText()
        # 在这里处理用户的联系方式和反馈，例如发送到服务器或保存到文件
        print(f'联系方式: {contact_info}, 反馈: {feedback}')
        self.close()
