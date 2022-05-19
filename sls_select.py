from PyQt5.QtWidgets import *
from PyQt5 import uic
import threading
from utils.pasing import loadCategory, getWord, numOfPages

from utils.changed_form import Windows

form_mode = uic.loadUiType("./uis/sls_select.ui")[0]

category_metadata = {
    "btn_cate01": "",
    "btn_cate02": "",
    "btn_cate03": "",
    "btn_cate04": "",
    "btn_cate05": "",
    "btn_cate06": "",
    "btn_cate07": "",
    "btn_cate08": "",
    "btn_cate09": "",
    "btn_cate10": "",
    "btn_cate11": "",
    "btn_cate12": "",
    "btn_cate13": "",
    "btn_cate14": "",
    "btn_cate15": "",
    "btn_cate16": ""
}


def loadWord(window, cate_num, page):
    # 각 카테고리의 최대 페이지를 불러옴
    max_page = numOfPages(cate_num)
    window.label_page_cate.setText(str(max_page))

    # 단어들을 불러옴
    word_load = getWord(cate_num, page)

    # 불러온 단어들을 데이터로 갱신함
    for button, word_data in zip(window.word_button_list, word_load):
        window.word_metadata[word_data.mean] = word_data.origin_no
        button.setText(word_data.mean)


def init(window):
    cate_load = loadCategory()
    for idx, key in enumerate(category_metadata):
        category_metadata[key] = cate_load[idx].category

    # 각 카테고리의 최대 페이지를 불러옴
    max_page = numOfPages(category_metadata["btn_cate01"])
    window.label_page_cate.setText(str(max_page))

    # 단어들을 불러옴
    word_load = getWord(category_metadata["btn_cate01"], 1)

    # 불러온 단어들 데이터로 갱신함.
    for button, word_data in zip(window.word_button_list, word_load):
        window.word_metadata[word_data.mean] = word_data.origin_no
        button.setText(word_data.mean)
        # connect는 최초 한번만 수행하면 됨.
        button.clicked.connect(window.word_button_onClick)


class SLSSelectWindow(QDialog, QWidget, form_mode):
    def __init__(self):
        super().__init__()

    def init(self, args=None):
        self.setupUi(self)
        if args is None:
            self.load_word_thread = self.load_word_thread = threading.Thread(target=loadWord,
                                                                             args=(
                                                                                 self, category_metadata["btn_cate01"],
                                                                                 1))
        else:
            self.load_word_thread = self.load_word_thread = threading.Thread(target=loadWord,
                                                                             args=(
                                                                                 self, category_metadata[args],
                                                                                 1))
        self.word_metadata = {}
        self.word_button_list = [
            self.btn_word01,
            self.btn_word02,
            self.btn_word03,
            self.btn_word04,
            self.btn_word05,
            self.btn_word06,
            self.btn_word07,
            self.btn_word08,
            self.btn_word09,
            self.btn_word10
        ]
        self.cate_num = "btn_cate01"
        for button in self.word_button_list:
            button.setText("로딩중")
        self.load_word_thread = threading.Thread(target=init, args=(self,))
        self.load_word_thread.daemon = True
        self.load_word_thread.start()

    def __del__(self):
        pass

    def setArgs(self, args):
        for button in self.word_button_list:
            button.setText("로딩중")
        self.load_word_thread = self.load_word_thread = threading.Thread(target=loadWord,
                                                                         args=(
                                                                             self, category_metadata[args],
                                                                             1))
        self.cate_num = args
        self.load_word_thread.daemon = True
        self.load_word_thread.start()

    def next_page_button_onClick(self):
        sender = self.sender()
        if not self.load_word_thread.is_alive():
            if int(self.label_page.text()) + 1 >= int(self.label_page_cate.text()):
                print("불러올 페이지가 없습니다.")
                return
            next_page = int(self.label_page.text()) + 1
            self.label_page.setText(str(next_page))
            for button in self.word_button_list:
                button.setText("로딩중")
            self.load_word_thread = threading.Thread(target=loadWord,
                                                     args=(self, category_metadata[self.cate_num], next_page))
            self.load_word_thread.daemon = True
            self.load_word_thread.start()
        else:
            print("데이터를 로딩중입니다.")

    def prev_page_button_onClick(self):
        sender = self.sender()
        if not self.load_word_thread.is_alive():
            if int(self.label_page.text()) - 1 <= 0:
                print("불러올 페이지가 없습니다.")
                return
            prev_page = int(self.label_page.text()) - 1
            self.label_page.setText(str(prev_page))
            for button in self.word_button_list:
                button.setText("로딩중")
            self.load_word_thread = threading.Thread(target=loadWord,
                                                     args=(self, category_metadata[self.cate_num], prev_page))
            self.load_word_thread.daemon = True
            self.load_word_thread.start()
        else:
            print("데이터를 로딩중입니다.")

    def category_button_onClick(self):
        sender = self.sender()
        if not self.load_word_thread.is_alive():
            for button in self.word_button_list:
                button.setText("로딩중")
            self.label_page.setText("1")
            self.cate_num = sender.objectName()
            self.load_word_thread = threading.Thread(target=loadWord,
                                                     args=(self, category_metadata[sender.objectName()], 1))
            self.load_word_thread.daemon = True
            self.load_word_thread.start()
        else:
            print("데이터를 로딩중입니다.")

    def word_button_onClick(self):
        sender = self.sender()
        if sender.text() == "로딩중":
            print("데이터를 로딩중입니다.")
            return
        Windows.changedWindow(self, "word", (self.word_metadata[sender.text()], sender.text()))

    def study_button_onClick(self):
        pass

    def mode_button_onClick(self):
        if self.load_word_thread.is_alive():
            print("데이터를 로딩중입니다")
            return
        Windows.changedWindow(self, "mode")

    def quiz_button_onClick(self):
        if self.load_word_thread.is_alive():
            print("데이터를 로딩중입니다")
            return
        Windows.changedWindow(self, "sls_quiz", True)
