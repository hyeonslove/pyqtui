import ssl
import cv2

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic.properties import QtGui
import urllib.request

from utils.changed_form import Windows
from utils.pasing import loadCategory, getMovieUrl, getPictureUrl, getExplain
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


def playMovie(window):
    cap = cv2.VideoCapture("temp.mp4")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)

        pixmap = QPixmap(convertToQtFormat)
        pixmap = pixmap.scaledToWidth(900)
        window.lb_video.setPixmap(pixmap)
        cv2.waitKey(20)


def init(window, args):
    word_num = args[0]
    cate_load = loadCategory()
    for idx, key in enumerate(category_metadata):
        category_metadata[key] = cate_load[idx].category
    # getMovieUrl, getPictureUrl, getExplain
    picture_url = getPictureUrl(word_num)
    movie_url = getMovieUrl(word_num)
    body = getExplain(word_num)
    window.lb_word.setText(args[1])
    window.lb_explain.setText(body)

    url = picture_url[0]
    context = ssl._create_unverified_context()
    image = urllib.request.urlopen(url, context=context).read()
    pixmap = QPixmap()
    pixmap.loadFromData(image)
    window.lb_img1.setPixmap(pixmap.scaledToHeight(200, Qt.SmoothTransformation))

    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve(movie_url, "temp.mp4")
    playMovie(window)


class WordWindow(QDialog, QWidget, form_mode):
    def __init__(self):
        super().__init__()

    def __del__(self):
        print()

    def setArgs(self, args):
        self.lb_video.setText("로딩중")
        self.lb_img1.setText("로딩중")
        self.lb_word.setText("로딩중")
        self.lb_explain.setText("로딩중")

        self.load_data_thread = threading.Thread(target=init, args=(self, args,))
        self.load_data_thread.daemon = True
        self.load_data_thread.start()

    def init(self, args=None):
        self.setupUi(self)
        self.setArgs(args)

    def category_button_onClick(self):
        sender = self.sender()
        if self.load_data_thread.is_alive():
            print("데이터를 로딩중입니다.")
            return
        Windows.changedWindow(self, "sls_select", sender.objectName())

    def movie_replay_button_onClick(self):
        sender = self.sender()
        if self.load_data_thread.is_alive():
            print("데이터를 로딩중입니다.")
            return

        self.load_data_thread = threading.Thread(target=playMovie, args=(self,))
        self.load_data_thread.daemon = True
        self.load_data_thread.start()

    def study_button_onClick(self):
        pass

    def mode_button_onClick(self):
        Windows.changedWindow(self, "mode")

    def quiz_button_onClick(self):
        pass
