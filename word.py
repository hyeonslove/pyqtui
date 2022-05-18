from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from utils.changed_form import Windows
from utils.pasing import loadCategory
import threading

form_mode = uic.loadUiType("./uis/word.ui")[0]

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


def init(window):
    cate_load = loadCategory()
    for idx, key in enumerate(category_metadata):
        category_metadata[key] = cate_load[idx].category


class WordWindow(QDialog, QWidget, form_mode):
    def __init__(self):
        super().__init__()

    def __del__(self):
        print()

    def init(self, args=None):
        self.setupUi(self)

        self.load_data_thread = threading.Thread(target=init, args=(self,))
        self.load_data_thread.daemon = True
        self.load_data_thread.start()

    def category_button_onClick(self):
        sender = self.sender()
        if self.load_data_thread.is_alive():
            print("데이터를 로딩중입니다.")
            return
        Windows.changedWindow(self, "sls_select", sender.objectName())

    def study_button_onClick(self):
        pass

    def mode_button_onClick(self):
        Windows.changedWindow(self, "mode")

    def quiz_button_onClick(self):
        pass
