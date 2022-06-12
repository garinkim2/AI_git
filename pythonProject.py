import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
import numpy as np
import platform

import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps



def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path('flowrate.ui')  # 여기에 ui파일명 입력
form_class = uic.loadUiType(form)[0]

form_second = resource_path('secondwindow_flowrate.ui')
form_secondwindow = uic.loadUiType(form_second)[0]



class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label_2.setGeometry(10, 60, 192, 192)
        self.comboBox.addItems(["14G"])             # 14G = 1.82mm(ID)
        self.comboBox.addItems(["17G"])             # 17G = 1.23mm(ID)
        self.comboBox.addItems(["21G"])             # 21G = 0.50mm(ID)
        self.MLmodel = None                         # self.인식모델을 의미
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('File')

        self.guide = QLabel('helloworld')
        self.guide.move(40,50)
        self.guide.adjustSize()


        file_add_model_menu = QAction('모델 불러오기', self)
        file_add_model_menu.setShortcut('Ctrl + L')
        file_add_model_menu.triggered.connect(self.loadModel)
        filemenu.addAction(file_add_model_menu)



    # 여기에 시그널-슬롯 연결 설정 및 함수 설정.

    def btn_file_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', '', 'All File(*);; Image File(*.png *.jpg')
        if fname[0]:
            # QPixmap 객체
            pixmap = QPixmap(fname[0])
            pixmap2 = pixmap.scaled(192, 192)
            self.label_2.setPixmap(pixmap2)



    def comb_nozzle_diameter(self):

        global nozzle_ID
        global nozzle_Dia
        nozzle_ID = self.comboBox.currentIndex()
        nozzle_name = self.comboBox.currentText()
        # self.comboBox.setText(nozzle_name)
        if nozzle_ID == 1:
            nozzle_Dia = 1.82
        if nozzle_ID == 2 :
            nozzle_Dia = 1.23
        if nozzle_ID == 3 :
            nozzle_Dia = 0.50


    def loadModel(self):                    # 파일에서 인식모델을 가져와 사용
        global model
        try:
            modelfile, _ = QFileDialog.getOpenFileName(self, 'add model', '')       ## model file 경로
            insert_fname = QFileInfo(modelfile).fileName()
            self.MLmodel = load_model('insert_fname')
            if modelfile:

                self.MLmodel = load_model('insert_fname')
                self.guide.setText('모델 추가 완료!')

        except:
            self.guide.setText('모델 파일 형식이 아닙니다.')

            print(self.MLmodel)

    def btn_main_to_second(self):
        self.hide()

        self.second = secondwindow()
        self.second.exec()
        self.show()

        # define image
        image = Image.open(fname[0])
        image = image.resize((128, 128))
        image = np.array(image)
        #  x.append(image)
        #   y.append(i - 1)


class secondwindow(QDialog, QWidget, form_secondwindow):
    def __init__(self):
        super(secondwindow, self).__init__()
        self.initUi()
        self.show()



    def initUi(self):
        self.setupUi(self)

    def btn_second_to_main(self):
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()