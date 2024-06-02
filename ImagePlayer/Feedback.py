import smtplib
from email.mime.text import MIMEText
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QMessageBox

sender = 'Your QQ mailbox'
password = 'Your QQ email authorization code'
receivers = ['onebuaaer@gmail.com']


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
        message = MIMEText(f'''用户 {contact_info}的反馈: 
{feedback}''', 'plain', 'utf-8')
        message['Subject'] = '来自ImagePlayer用户的反馈'
        message['From'] = sender
        message['To'] = receivers[0]
        try:
            server = smtplib.SMTP('smtp.qq.com')
            server.login(sender, password)
            server.sendmail(sender, receivers, message.as_string())
            QMessageBox.information(self, '成功', '已成功收到您的反馈，谢谢！')
            server.quit()
        except smtplib.SMTPException as e:
            QMessageBox.information(self, '失败', f'您的反馈发送失败，失败原因为：{e}')
        self.close()
