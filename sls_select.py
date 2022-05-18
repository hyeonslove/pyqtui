from PyQt5.QtWidgets import *
from PyQt5 import uic
import threading
from utils.pasing import loadCategory, getWord, numOfPages

from utils.changed_form import Windows

form_mode = uic.loadUiType("./uis/sls_select.ui")[0]

cate_data = {
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
    for idx, key in enumerate(cate_data):
        cate_data[key] = cate_load[idx].category

    # 각 카테고리의 최대 페이지를 불러옴
    max_page = numOfPages(cate_data["btn_cate01"])
    window.label_page_cate.setText(str(max_page))

    # 단어들을 불러옴
    word_load = getWord(cate_data["btn_cate01"], 1)

    # 불러온 단어들 데이터로 갱신함.
    for button, word_data in zip(window.word_button_list, word_load):
        window.word_metadata[word_data.mean] = word_data.origin_no
        button.setText(word_data.mean)
        # connect는 최초 한번만 수행하면 됨.
        button.clicked.connect(window.word_button_onClick)


class SLSSelectWindow(QDialog, QWidget, form_mode):
    def __init__(self):
        super().__init__()

    def init(self):
        self.setupUi(self)
        self.load_word_thread = None
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

        for button in self.word_button_list:
            button.setText("로딩중")
        data_loader_thread = threading.Thread(target=init, args=(self,))
        data_loader_thread.daemon = True
        data_loader_thread.start()

    def __del__(self):
        pass

    def next_page_button_onClick(self):
        pass

    def prev_page_button_onClick(self):
        pass

    def category_button_onClick(self):
        if self.load_word_thread is None:
            for button in self.word_button_list:
                button.setText("로딩중")
            sender = self.sender()
            self.load_word_thread = threading.Thread(target=loadWord, args=(self, cate_data[sender.objectName()], 1))
            self.load_word_thread.daemon = True
            self.load_word_thread.start()
        else:
            if not self.load_word_thread.is_alive():
                for button in self.word_button_list:
                    button.setText("로딩중")
                sender = self.sender()
                self.load_word_thread = threading.Thread(target=loadWord,
                                                         args=(self, cate_data[sender.objectName()], 1))
                self.load_word_thread.daemon = True
                self.load_word_thread.start()
            else:
                print("데이터를 로딩중입니다.")

    def word_button_onClick(self):
        print(self.sender().text())

    def study_button_onClick(self):
        pass

    def mode_button_onClick(self):
        Windows.changedWindow(self, "mode")

    def quiz_button_onClick(self):
        pass
