# -*- coding: utf-8 -*-

import cv2
# Form implementation generated from reading ui file 'main-window.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from Preprocesor import Preprocessor
from Recognizer import Recognizer


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.mainwindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelImage = QtWidgets.QLabel(self.centralwidget)
        self.labelImage.setGeometry(QtCore.QRect(5, 0, 790, 480))
        self.labelImage.setText("")
        self.labelImage.setObjectName("labelImage")
        self.pushButtonProcess = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonProcess.setGeometry(QtCore.QRect(680, 510, 111, 32))
        self.pushButtonProcess.setObjectName("pushButtonProcess")
        self.pushButtonProcess.clicked.connect(self.button_process_click)
        self.pushButtonBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonBrowse.setGeometry(QtCore.QRect(570, 510, 111, 32))
        self.pushButtonBrowse.setObjectName("pushButtonBrowse")
        self.pushButtonBrowse.clicked.connect(self.button_browse_click)
        MainWindow.setCentralWidget(self.centralwidget)
        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        # self.menubar.setObjectName("menubar")
        # self.menuHelp = QtWidgets.QMenu(self.menubar)
        # self.menuHelp.setObjectName("menuHelp")
        # MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        # self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.image = None

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Diabetic Retinopathy"))
        self.pushButtonProcess.setText(_translate("MainWindow", "Process"))
        self.pushButtonBrowse.setText(_translate("MainWindow", "Browse"))
        # self.menuHelp.setTitle(_translate("MainWindow", "Help"))

    def button_browse_click(self):
        dlg = QFileDialog()

        if dlg.exec_():
            path = dlg.selectedFiles()[0]
            self.show_image(path)
            # self.image = Image.open(path)
            self.image = cv2.imread(path)

    def show_image(self, path):
        self.labelImage.setScaledContents(True)
        pixmap = QPixmap(path)
        pixmap.scaled(790, 480, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.labelImage.setPixmap(pixmap)
        self.labelImage.show()

    def button_process_click(self):
        preprocessor = Preprocessor()
        labeled_img = preprocessor.process(self.image)
        cv2.imwrite('result_img.png', labeled_img)
        recognizer = Recognizer()
        disease = recognizer.recognize_disease('result_img.png')
        print(disease)
        QMessageBox.about(self.mainwindow, "Predicted Disease", disease)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()    
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
