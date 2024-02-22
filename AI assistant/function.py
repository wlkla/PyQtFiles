from 我的助手 import *

flag_1 = True
flag_2 = True


class Controller(PyQt5.QtCore.QObject):
    ai_message_received = PyQt5.QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.en = Entrance()
        self.chat = Chat()
        self.en.show()
        self.show_history()
        self.en.move(1718, 860)
        self.conversation_history = []
        self.init_chat_window()
        self.ai_message_received.connect(self.display_ai_message)
        self.chat.listWidget.setVerticalScrollMode(PyQt5.QtWidgets.QAbstractItemView.ScrollPerPixel)

    def init_chat_window(self):
        # 入口窗口部分
        self.en.pushButton.clicked.connect(self.chat.show)
        self.chat.move(1500, 470)

        # 聊天窗口部分
        self.chat.pushButton_1.clicked.connect(self.chat.hide)
        self.chat.pushButton_2.clicked.connect(self.change_win)
        self.chat.pushButton_3.clicked.connect(self.chat.hide)
        # self.chat.pushButton_4.clicked.connect(self.chat.close)
        self.chat.message.returnPressed.connect(self.get_reply)
        self.chat.send.clicked.connect(self.get_reply)

    def show_history(self):
        import sqlite3
        import ChatBubble

        conn = sqlite3.connect('history.db')
        c = conn.cursor()
        all_ = c.execute('SELECT MY_MESSAGE,AI_MESSAGE FROM CHAT')
        information = all_.fetchall()
        for item in information:
            my_, ai_ = item
            my_chat_bubble = ChatBubble.ChatBubbleMe(my_, self.chat)
            ai_chat_bubble = ChatBubble.ChatBubbleAi(ai_, self.chat)
            myItem1 = PyQt5.QtWidgets.QListWidgetItem()
            myItem1.setSizeHint(my_chat_bubble.sizeHint())
            self.chat.listWidget.addItem(myItem1)
            self.chat.listWidget.setItemWidget(myItem1, my_chat_bubble)

            myItem2 = PyQt5.QtWidgets.QListWidgetItem()
            myItem2.setSizeHint(ai_chat_bubble.sizeHint())
            self.chat.listWidget.addItem(myItem2)
            self.chat.listWidget.setItemWidget(myItem2, ai_chat_bubble)
        conn.commit()
        conn.close()
        self.chat.listWidget.verticalScrollBar().setValue(self.chat.listWidget.verticalScrollBar().maximum())

    def get_api_key(self):
        from 我的助手 import api_key
        return api_key

    def save_message(self, MY_MESSAGE, AI_MESSAGE):
        import sqlite3
        import datetime
        conn = sqlite3.connect('history.db')
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM CHAT')
        result = c.fetchone()
        if len(result) == 0:
            a = 0
        else:
            row_count = result[0]
            a = row_count
        Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('INSERT INTO CHAT (NUMBER,TIME,MY_MESSAGE,AI_MESSAGE) VALUES (?, ?, ?, ?)', (
            a, Time, MY_MESSAGE, AI_MESSAGE))
        a += 1
        conn.commit()
        conn.close()

    def get_reply(self):
        self.prompt = self.chat.message.text()
        self.chat.message.clear()
        if self.prompt == '':
            PyQt5.QtWidgets.QMessageBox.warning(self.chat, '错误', '消息不能为空！', PyQt5.QtWidgets.QMessageBox.Yes)
            return
        self.conversation_history.append({"role": "user", "content": self.prompt})
        self.display_user_message(self.prompt)
        self.get_answer()

    def display_user_message(self, message):
        import ChatBubble
        my_chat_bubble = ChatBubble.ChatBubbleMe(message, self.chat)
        myItem1 = PyQt5.QtWidgets.QListWidgetItem()
        myItem1.setSizeHint(my_chat_bubble.sizeHint())
        self.chat.listWidget.addItem(myItem1)
        self.chat.listWidget.setItemWidget(myItem1, my_chat_bubble)
        ai_chat_bubble = ChatBubble.ChatBubbleAi('消息生成中...', self.chat)
        myItem2 = PyQt5.QtWidgets.QListWidgetItem()
        myItem2.setSizeHint(ai_chat_bubble.sizeHint())
        self.chat.listWidget.addItem(myItem2)
        self.chat.listWidget.setItemWidget(myItem2, ai_chat_bubble)
        self.chat.listWidget.verticalScrollBar().setValue(self.chat.listWidget.verticalScrollBar().maximum())

    def display_ai_message(self, message):
        import ChatBubble
        self.chat.listWidget.takeItem(self.chat.listWidget.count() - 1)
        ai_chat_bubble = ChatBubble.ChatBubbleAi(message, self.chat)
        myItem2 = PyQt5.QtWidgets.QListWidgetItem()
        myItem2.setSizeHint(ai_chat_bubble.sizeHint())
        self.chat.listWidget.addItem(myItem2)
        self.chat.listWidget.setItemWidget(myItem2, ai_chat_bubble)

    def get_answer(self):
        import threading
        add_thread_2 = threading.Thread(target=self.fetch_answer)
        add_thread_2.start()

    def fetch_answer(self):
        import requests
        api_key = self.get_api_key()
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": self.conversation_history
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            self.chat_result = response_data['choices'][0]['message']['content']
            self.save_message(self.prompt, self.chat_result)
            self.ai_message_received.emit(self.chat_result)
        except requests.exceptions.RequestException as e:
            PyQt5.QtWidgets.QMessageBox.warning(self.chat, '获取回复失败', f'Error during API call:{e}',
                                                PyQt5.QtWidgets.QMessageBox.Yes)
            return

    def change_win(self):
        global flag_1, flag_2
        if flag_1:
            flag_1 = False
            flag_2 = True
            self.chat.set_movable(True)
            self.chat.resize(735, 546)
            self.chat.move(593, 267)
            self.chat.listWidget.clear()
            self.show_history()
            self.chat.pushButton_1.disconnect()
            self.chat.pushButton_2.disconnect()
            self.chat.pushButton_3.disconnect()
            self.chat.pushButton_1.setStyleSheet("QPushButton{\n"
                                                 "background-color: rgb(255, 255, 255, 0);\n"
                                                 "image: url(:/buttom/img/最小化.png);\n"
                                                 "border:0px;\n"
                                                 "}\n"
                                                 "QPushButton:hover{\n"
                                                 "background-color: rgb(220, 220, 220);\n"
                                                 "}")
            self.chat.pushButton_2.setStyleSheet("QPushButton{\n"
                                                 "background-color: rgb(255, 255, 255, 0);\n"
                                                 "image: url(:/buttom/img/缩小.png);\n"
                                                 "border:0px;\n"
                                                 "}\n"
                                                 "QPushButton:hover{\n"
                                                 "background-color: rgb(220, 220, 220);\n"
                                                 "}")
            self.chat.pushButton_3.setStyleSheet("QPushButton{\n"
                                                 "background-color: rgb(255, 255, 255, 0);\n"
                                                 "image: url(:/buttom/img/最大化.png);\n"
                                                 "border:0px;\n"
                                                 "}\n"
                                                 "QPushButton:hover{\n"
                                                 "background-color: rgb(220, 220, 220);\n"
                                                 "}")
            self.chat.pushButton_1.clicked.connect(self.chat.hide)
            self.chat.pushButton_2.clicked.connect(self.change_win)
            self.chat.pushButton_3.clicked.connect(self.change_full)
        else:
            flag_1 = True
            flag_2 = True
            self.chat.set_movable(False)
            self.chat.resize(286, 472)
            self.chat.move(1500, 470)
            self.chat.listWidget.clear()
            self.show_history()
            self.chat.pushButton_1.disconnect()
            self.chat.pushButton_2.disconnect()
            self.chat.pushButton_3.disconnect()
            self.chat.pushButton_1.setStyleSheet("QPushButton{\n"
                                                 "background-color: rgb(255, 255, 255, 0);\n"
                                                 "image: url(:/buttom/img/最小化.png);\n"
                                                 "border:0px;\n"
                                                 "}\n"
                                                 "QPushButton:hover{\n"
                                                 "background-color: rgb(220, 220, 220);\n"
                                                 "}")
            self.chat.pushButton_2.setStyleSheet("QPushButton{\n"
                                                 "background-color: rgb(255, 255, 255, 0);\n"
                                                 "image: url(:/buttom/img/发送至.png);\n"
                                                 "border:0px;\n"
                                                 "}\n"
                                                 "QPushButton:hover{\n"
                                                 "background-color: rgb(220, 220, 220);\n"
                                                 "}")
            self.chat.pushButton_3.setStyleSheet("QPushButton{\n"
                                                 "background-color: rgb(255, 255, 255, 0);\n"
                                                 "image: url(:/buttom/img/关闭.png);\n"
                                                 "border:0px;\n"
                                                 "}\n"
                                                 "QPushButton:hover{\n"
                                                 "background-color:rgb(255, 0, 0);\n"
                                                 "}")
            self.chat.pushButton_1.clicked.connect(self.chat.hide)
            self.chat.pushButton_2.clicked.connect(self.change_win)
            self.chat.pushButton_3.clicked.connect(self.chat.hide)

    def change_full(self):
        global flag_2
        if flag_2:
            flag_2 = False
            self.chat.showFullScreen()
            self.chat.listWidget.clear()
            self.show_history()
            self.chat.pushButton_3.setStyleSheet("QPushButton{\n"
                                                 "background-color: rgb(255, 255, 255, 0);\n"
                                                 "image: url(:/buttom/img/还原.png);\n"
                                                 "border:0px;\n"
                                                 "}\n"
                                                 "QPushButton:hover{\n"
                                                 "background-color: rgb(220, 220, 220);\n"
                                                 "}")
        else:
            flag_2 = True
            self.chat.showNormal()
            self.chat.listWidget.clear()
            self.show_history()
            self.chat.pushButton_3.setStyleSheet("QPushButton{\n"
                                                 "background-color: rgb(255, 255, 255, 0);\n"
                                                 "image: url(:/buttom/img/最大化.png);\n"
                                                 "border:0px;\n"
                                                 "}\n"
                                                 "QPushButton:hover{\n"
                                                 "background-color: rgb(220, 220, 220);\n"
                                                 "}")
