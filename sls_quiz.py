from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *
from PyQt5 import uic
import threading
import time
from keras.models import Sequential
from keras.layers import LSTM, Dense
import cv2
import random
from sld.configs import Config
from sld.mediapipes import MediaPipe
from utils.pasing import loadCategory, getWord, numOfPages
import numpy as np
from utils.changed_form import Windows

form_mode = uic.loadUiType("./uis/sls_quiz.ui")[0]


def init(window):
    window.mp = MediaPipe(detection_option=["pose", "lh", "rh"])

    window.result_arr = Config.get_action_num()
    window.model = Sequential()
    window.model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(Config.SEQUENCE_LENGTH, 258)))
    window.model.add(LSTM(128, return_sequences=True, activation='relu'))
    window.model.add(LSTM(64, return_sequences=False, activation='relu'))
    window.model.add(Dense(64, activation='relu'))
    window.model.add(Dense(32, activation='relu'))
    window.model.add(Dense(window.result_arr.shape[0], activation='softmax'))
    window.model.load_weights("cjw27_100.h5")

    sequence = 0

    window.cap = cv2.VideoCapture(0)
    window.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)  # 1280
    window.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)  # 720
    start = time.time()
    while window.isPlay:
        ret, frame = window.cap.read()
        image, result = window.mp.mediapipe_detection(frame)
        window.mp.draw_styled_landmarks(image, result)
        remain = time.time() - start
        if remain > Config.WAIT_TIME:
            if not window.isStart:
                start = time.time()
                continue
            print('start')
            sequences = []
            st = time.time()
            for idx in range(Config.SEQUENCE_LENGTH):
                ret, frame = window.cap.read()
                image, result = window.mp.mediapipe_detection(frame)
                window.mp.draw_styled_landmarks(image, result)
                keypoints = window.mp.extract_keypoints(result)
                sequences.append(keypoints)
                cv2.putText(image, 'capture %d frame' % (idx), (100, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5, cv2.LINE_AA)

                img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap(convertToQtFormat)
                pixmap = pixmap.scaledToWidth(800)
                window.lb_camera.setPixmap(pixmap)  # scaledToHeight(200, Qt.SmoothTransformation)
                # cv2.imshow("utils", image)
                cv2.waitKey(2)
            print(time.time() - st)
            res = window.model.predict(np.expand_dims(sequences, axis=0))[0]
            print("per : " + str(res[np.argmax(res)]) + "\nRes : " +
                  str(Config.get_action_name(window.result_arr[np.argmax(res)])))
            if str(Config.get_action_name(window.result_arr[np.argmax(res)])) == window.lb_question.text():
                if int(window.lb_page.text()) + 1 >= 6:
                    window.isStart = False
                    window.isPlay = False
                    break
                window.lb_page.setText(str(int(window.lb_page.text()) + 1))
                window.lb_question.setText(window.quiz_word[int(window.lb_page.text()) - 1][1])
            sequence += 1
            start = time.time()
        else:
            cv2.putText(image, '%d wait %.2f sec ' % (sequence, Config.WAIT_TIME - remain), (100, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5, cv2.LINE_AA)
        # cv2.imshow("utils", image)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(convertToQtFormat)
        pixmap = pixmap.scaledToWidth(800)
        window.lb_camera.setPixmap(pixmap)  # scaledToHeight(200, Qt.SmoothTransformation)
        cv2.waitKey(1)


class SLSQuizWindow(QDialog, QWidget, form_mode):
    def __init__(self):
        super().__init__()

    def init(self, args=None):
        self.setupUi(self)
        self.isPlay = True
        self.isStart = False
        self.lb_camera.setText("로딩중")
        self.quiz_word = random.sample(Config.get_action()[1:], 5)
        self.init_thread = threading.Thread(target=init, args=(self,))
        self.init_thread.daemon = True
        self.init_thread.start()

    def setArgs(self, args):
        self.lb_camera.setText("로딩중")
        self.btn_pass.setText("시작")
        self.lb_page.setText("1")
        self.lb_question.setText("로딩중")
        self.isPlay = True
        self.isStart = False
        self.quiz_word = random.sample(Config.get_action()[1:], 5)
        if args is not None:
            self.init_thread = threading.Thread(target=init, args=(self,))
            self.init_thread.daemon = True
            self.init_thread.start()

    def start_button_onClick(self):
        if not self.isStart:
            self.isStart = True
            self.btn_pass.setText("다음")
            self.lb_question.setText(self.quiz_word[int(self.lb_page.text()) - 1][1])
        else:
            if int(self.lb_page.text()) + 1 >= 6:
                self.isStart = False
                self.isPlay = False
                return
            self.lb_page.setText(str(int(self.lb_page.text()) + 1))
            self.lb_question.setText(self.quiz_word[int(self.lb_page.text()) - 1][1])

    def study_button_onClick(self):
        if self.init_thread.is_alive():
            self.isPlay = False
            print("데이터를 로딩중입니다.")
            return
        Windows.changedWindow(self, "sls_select")

    def mode_button_onClick(self):
        if self.init_thread.is_alive():
            self.isPlay = False
            print("데이터를 로딩중입니다.")
            return
        Windows.changedWindow(self, "mode")

    def result_button_onClick(self):
        if self.init_thread.is_alive():
            print("데이터를 로딩중입니다")
            return
