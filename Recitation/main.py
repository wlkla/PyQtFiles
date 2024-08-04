import sys
import json
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QComboBox, QPushButton, QLabel, QLineEdit)
from PyQt5.QtCore import Qt


class QuestionViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 读取JSON文件
        with open('questions.json', 'r', encoding='utf-8') as file:
            self.data = json.load(file)

        self.setWindowTitle('期末复习')
        self.setObjectName("Form")
        self.setWindowIcon(QIcon('D:/Document/Pictures/ico/vmde.ico'))
        self.setStyleSheet(
            """#Form{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(105, 255, 151, 
            255), stop:1 rgba(0, 228, 255, 255));}""")
        self.current_chapter = '全部章节'
        self.current_importance = '全部重要程度'
        self.current_familiarity = '全部熟悉程度'
        self.questions = []
        self.current_question_index = 0
        self.showing_answer = False

        # 创建下拉选框
        self.chapter_combo = QComboBox()
        self.importance_combo = QComboBox()
        self.familiarity_combo = QComboBox()

        self.chapter_combo.addItem('全部章节')
        for chapter in self.data['chapters']:
            self.chapter_combo.addItem(chapter['chapterTitle'])

        self.importance_combo.addItem('全部重要程度')
        self.importance_combo.addItem('重要')
        self.importance_combo.addItem('不重要')

        self.familiarity_combo.addItem('全部熟悉程度')
        self.familiarity_combo.addItem('熟悉')
        self.familiarity_combo.addItem('模糊')
        self.familiarity_combo.addItem('不会')

        # 连接信号和槽
        self.chapter_combo.currentIndexChanged.connect(self.updateQuestions)  # type: ignore
        self.importance_combo.currentIndexChanged.connect(self.updateQuestions)  # type: ignore
        self.familiarity_combo.currentIndexChanged.connect(self.updateQuestions)  # type: ignore

        self.chapter_combo.setFixedSize(300, 60)
        self.importance_combo.setFixedSize(300, 60)
        self.familiarity_combo.setFixedSize(300, 60)

        # 设置下拉框样式
        self.chapter_combo.setStyleSheet("""
            QComboBox{
                background-color: transparent;
                border: 2px solid white;
                color: white;
                border-radius: 30px;
                font: 18pt "华文新魏";
                padding-left: 80px;
            }
            QComboBox:hover {
                background-color: rgba(255, 255, 255, 100)
            }            
            QComboBox QAbstractItemView {
                outline: 0px;
                color: black;
                background-color: white;
                selection-background-color:red;
            }
            QComboBox::drop-down 
            {
                border:none;
            }
            QComboBox::down-arrow {
                padding: 0px 10px 0px 0px;
                image: url(:/icon/Document/Downloads/down.png);
            }
            QComboBox QAbstractScrollArea QScrollBar:vertical {
                width: 4px;
                background-color: transparent;
            }
            QComboBox QAbstractScrollArea QScrollBar::handle:vertical {
                border-radius: 2px;
                background: red;
                height: 10px;
            }
            QComboBox QAbstractScrollArea QScrollBar::handle:vertical:hover {
                background: black;
            }
        """)
        self.importance_combo.setStyleSheet("""
            QComboBox{
                background-color: transparent;
                border: 2px solid white;
                color: white;
                border-radius: 30px;
                font: 18pt "华文新魏";
                padding-left: 80px;
            }
            QComboBox:hover {
                background-color: rgba(255, 255, 255, 100)
            }
            QComboBox QAbstractItemView {
                outline: 0px;
                color: black;
                background-color: white;
                selection-background-color:orange;
            }
            QComboBox::drop-down 
            {
                border:none;
            }
            QComboBox::down-arrow {
                padding: 0px 10px 0px 0px;
                image: url(:/icon/Document/Downloads/down.png);
            }            
            QComboBox QAbstractScrollArea QScrollBar:vertical {
                width: 4px;
                background-color: transparent;
            }
            QComboBox QAbstractScrollArea QScrollBar::handle:vertical {
                border-radius: 2px;
                background: orange;
                height: 10px;
            }
            QComboBox QAbstractScrollArea QScrollBar::handle:vertical:hover {
                background: black;
            }
        """)
        self.familiarity_combo.setStyleSheet("""
            QComboBox{
                background-color: transparent;
                border: 2px solid white;
                color: white;
                border-radius: 30px;
                font: 18pt "华文新魏";
                padding-left: 80px;
            }
            QComboBox:hover {
                background-color: rgba(255, 255, 255, 100)
            }            
            QComboBox QAbstractItemView {
                outline: 0px;
                color: black;
                background-color: white;
                selection-background-color:green;
            }
            QComboBox::drop-down 
            {
                border:none;
            }
            QComboBox::down-arrow {
                padding: 0px 10px 0px 0px;
                image: url(:/icon/Document/Downloads/down.png);
            }            
            QComboBox QAbstractScrollArea QScrollBar:vertical {
                width: 4px;
                background-color: transparent;
            }
            QComboBox QAbstractScrollArea QScrollBar::handle:vertical {
                border-radius: 2px;
                background: green;
                height: 10px;
            }
            QComboBox QAbstractScrollArea QScrollBar::handle:vertical:hover {
                background: black;
            }
        """)

        # 搜索按钮
        self.search_button = QPushButton("展开搜索")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("输入搜索内容...")
        self.search_box.hide()

        self.search_button.clicked.connect(self.toggleSearchBox)  # type: ignore
        self.search_box.textChanged.connect(self.searchQuestions)  # type: ignore

        self.search_button.setFixedSize(150, 60)
        self.search_box.setFixedSize(400, 60)

        self.search_button.setStyleSheet("""
                    QPushButton {
                        border-radius: 30px;
                        border: 2px solid white;
                        background-color: transparent;
                        color: white;
                        font: 15pt "黑体";
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 100);
                    }
                """)
        self.search_box.setStyleSheet("""
                            QLineEdit {
                                padding-left: 20px;
                                border-radius: 30px;
                                border: 2px solid white;
                                background-color: transparent;
                                color: white;
                                font: 15pt "黑体";
                            }
                            QLineEdit:hover {
                                background-color: rgba(255, 255, 255, 100);
                            }
                        """)

        # 创建按钮
        self.prev_button = QPushButton('<<')
        self.next_button = QPushButton('>>')
        self.familiar_button = QPushButton('熟悉')
        self.fuzzy_button = QPushButton('模糊')
        self.not_familiar_button = QPushButton('不会')

        self.prev_button.clicked.connect(self.showPrevQuestion)  # type: ignore
        self.next_button.clicked.connect(self.showNextQuestion)  # type: ignore
        self.familiar_button.clicked.connect(lambda: self.setFamiliarity('熟悉'))  # type: ignore
        self.fuzzy_button.clicked.connect(lambda: self.setFamiliarity('模糊'))  # type: ignore
        self.not_familiar_button.clicked.connect(lambda: self.setFamiliarity('不会'))  # type: ignore

        # 设置按钮样式
        self.prev_button.setFixedSize(60, 60)
        self.next_button.setFixedSize(60, 60)
        self.familiar_button.setFixedSize(200, 60)
        self.fuzzy_button.setFixedSize(200, 60)
        self.not_familiar_button.setFixedSize(200, 60)
        self.prev_button.setStyleSheet("""
            QPushButton {
                border-radius: 30px;
                border: 2px solid white;
                background-color: transparent;
                color: white;
                font: 15pt "黑体";
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 100);
            }
        """)
        self.next_button.setStyleSheet("""
            QPushButton {
                border-radius: 30px;
                border: 2px solid white;
                background-color: transparent;
                color: white;
                font: 15pt "黑体";
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 100);
            }
        """)
        self.familiar_button.setStyleSheet("""
            QPushButton{
                background-color: transparent;
                color: white;
                border-radius: 30px;
                font: 18pt "华文新魏";
                border:2px solid white;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 100);
            }
        """)
        self.fuzzy_button.setStyleSheet("""
            QPushButton{
                background-color: transparent;
                color: white;
                border-radius: 30px;
                font: 18pt "华文新魏";
                border:2px solid white;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 100);
            }
        """)
        self.not_familiar_button.setStyleSheet("""
            QPushButton{
                background-color: transparent;
                color: white;
                border-radius: 30px;
                font: 18pt "华文新魏";
                border:2px solid white;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 100);
            }
        """)

        # 创建问题显示区域
        self.font_size = 40
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)  # type: ignore
        self.question_label.setStyleSheet(
            f"""font: {self.font_size}pt "新宋体";border:2px solid white;border-radius:20px;color:white;""")
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.mouseDoubleClickEvent = self.toggleAnswer

        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.addWidget(self.chapter_combo)
        top_layout.addWidget(self.importance_combo)
        top_layout.addWidget(self.familiarity_combo)
        top_layout.addWidget(self.search_box)
        top_layout.addWidget(self.search_button)
        top_widget.setFixedHeight(75)

        middle_widget = QWidget()
        middle_layout = QHBoxLayout(middle_widget)
        middle_layout.addWidget(self.prev_button)
        middle_layout.addWidget(self.question_label)
        middle_layout.addWidget(self.next_button)
        middle_widget.setFixedHeight(800)

        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_layout.addWidget(self.not_familiar_button)
        bottom_layout.addWidget(self.fuzzy_button)
        bottom_layout.addWidget(self.familiar_button)
        bottom_widget.setFixedHeight(75)

        main_layout = QVBoxLayout()
        main_layout.addWidget(top_widget)
        main_layout.addWidget(middle_widget)
        main_layout.addWidget(bottom_widget)

        self.setLayout(main_layout)
        self.updateQuestions()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.showPrevQuestion()
        elif event.key() == Qt.Key_Right:
            self.showNextQuestion()
        elif event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
            self.toggleAnswer(event)

    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        if angle > 0:
            self.font_size += 1
        else:
            self.font_size -= 1
        self.showQuestion()

    def updateQuestions(self):
        self.current_chapter = self.chapter_combo.currentText()
        self.current_importance = self.importance_combo.currentText()
        self.current_familiarity = self.familiarity_combo.currentText()

        self.questions = []

        for chapter in self.data['chapters']:
            if self.current_chapter != '全部章节' and chapter['chapterTitle'] != self.current_chapter:
                continue

            if self.current_importance in ['全部重要程度', '重要']:
                self.questions.extend(chapter['importantQuestions'])
            if self.current_importance in ['全部重要程度', '不重要']:
                self.questions.extend(chapter['unimportantQuestions'])

        if self.current_familiarity != '全部熟悉程度':
            self.questions = [q for q in self.questions if q['familiarity'] == self.current_familiarity]

        # 保持当前问题索引在有效范围内
        if self.current_question_index >= len(self.questions):
            self.current_question_index = len(self.questions) - 1

        if self.questions:
            self.showQuestion()
        else:
            self.question_label.setText('没有找到匹配的问题')

    def showQuestion(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            question_text = question['question']
            self.question_label.setText(question_text)
            self.showing_answer = False

            # 根据熟悉程度设置文本颜色
            familiarity = question['familiarity']
            if familiarity == '不会':
                self.question_label.setStyleSheet(
                    f"""font: {self.font_size}pt "新宋体";border:2px solid white;border-radius:20px;color:white;""")
                self.setStyleSheet(
                    """#Form{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(238, 9, 121, 255), stop:1 rgba(255, 106, 0, 255));}""")
            elif familiarity == '模糊':
                self.question_label.setStyleSheet(
                    f"""font: {self.font_size}pt "新宋体";border:2px solid white;border-radius:20px;color:white;""")
                self.setStyleSheet(
                    """#Form{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(252, 227, 138, 255), stop:1 rgba(243, 129, 129, 255));}""")
            elif familiarity == '熟悉':
                self.question_label.setStyleSheet(
                    f"""font: {self.font_size}pt "新宋体";border:2px solid white;border-radius:20px;color:white;""")
                self.setStyleSheet(
                    """#Form{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(105, 255, 151, 255), stop:1 rgba(0, 228, 255, 255));}""")

    def showPrevQuestion(self):
        if self.questions:
            self.current_question_index = (self.current_question_index - 1) % len(self.questions)
            self.showQuestion()

    def showNextQuestion(self):
        if self.questions:
            self.current_question_index = (self.current_question_index + 1) % len(self.questions)
            self.showQuestion()

    def setFamiliarity(self, level):
        if self.questions:
            self.questions[self.current_question_index]['familiarity'] = level
            self.saveData()
            self.updateQuestions()

    def saveData(self):
        with open('questions.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def toggleAnswer(self, event):
        if self.questions:
            question = self.questions[self.current_question_index]
            if self.showing_answer:
                self.question_label.setText(question['question'])
            else:
                self.question_label.setText(question['answer'])
            self.showing_answer = not self.showing_answer

    def toggleSearchBox(self):
        if self.search_box.isVisible():
            self.search_box.hide()
            self.search_button.setText("展开搜索")
            self.updateQuestions()
            self.search_box.clear()
        else:
            self.search_box.show()
            self.search_button.setText("关闭搜索")

    def searchQuestions(self, text):
        if text:
            self.questions = [q for q in self.questions if text.lower() in q['question'].lower()]
            if len(self.questions) == 0:
                self.question_label.setText('没有找到匹配的问题')
            else:
                self.current_question_index = 0
                self.showQuestion()
        else:
            self.questions = []
            self.updateQuestions()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # type: ignore
    viewer = QuestionViewer()
    viewer.show()
    sys.exit(app.exec_())
