import sys

from PyQt5.QtWidgets import *
from mode import ModeWindow
from sls_select import SLSSelectWindow
from utils.changed_form import Windows

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Windows.window_list["mode"] = ModeWindow()
    Windows.window_list["sls_select"] = SLSSelectWindow()
    Windows.changedWindow(None, "mode")
    app.exec_()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
