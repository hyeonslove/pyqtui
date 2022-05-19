import sys

from PyQt5.QtWidgets import *
from mode import ModeWindow
from sls_quiz import SLSQuizWindow
from sls_select import SLSSelectWindow
from utils.changed_form import Windows
from word import WordWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Windows.window_list["mode"] = ModeWindow()
    Windows.window_list["sls_select"] = SLSSelectWindow()
    Windows.window_list["word"] = WordWindow()
    Windows.window_list["sls_quiz"] = SLSQuizWindow()
    Windows.changedWindow(None, "mode")
    app.exec_()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
