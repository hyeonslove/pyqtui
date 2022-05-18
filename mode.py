from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from utils.changed_form import Windows

form_mode = uic.loadUiType("./uis/mode.ui")[0]


class ModeWindow(QDialog, QWidget, form_mode):
    def __init__(self):
        super().__init__()


    def __del__(self):
        pass

    def init(self):
        self.setupUi(self)

    def sign_language_study_button_onClick(self):
        Windows.changedWindow(self, "sls_select")

    def word_study_button_onClick(self):
        pass
