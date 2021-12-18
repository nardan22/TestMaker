# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'startpage.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 640)
        MainWindow.setMinimumSize(QtCore.QSize(480, 640))
        MainWindow.setMaximumSize(QtCore.QSize(480, 640))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QPushButton {\n"
"    background-color: #0A2A49;\n"
"    border-radius: 25px;\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"     background-color: #0E3459;\n"
" }\n"
"\n"
"QPushButton:pressed {\n"
"     background-color: #0A2A49;\n"
" }\n"
"\n"
"QPushButton:disabled {\n"
"     background-color: #1F4971;\n"
"    color: grey;\n"
" }")
        self.centralwidget.setObjectName("centralwidget")
        self.newTestBtn = QtWidgets.QPushButton(self.centralwidget)
        self.newTestBtn.setGeometry(QtCore.QRect(65, 130, 350, 50))
        self.newTestBtn.setMinimumSize(QtCore.QSize(350, 50))
        self.newTestBtn.setMaximumSize(QtCore.QSize(350, 50))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.newTestBtn.setFont(font)
        self.newTestBtn.setStyleSheet("")
        self.newTestBtn.setInputMethodHints(QtCore.Qt.ImhNone)
        self.newTestBtn.setObjectName("newTestBtn")
        self.existingTestsBtn = QtWidgets.QPushButton(self.centralwidget)
        self.existingTestsBtn.setGeometry(QtCore.QRect(65, 230, 350, 50))
        self.existingTestsBtn.setMinimumSize(QtCore.QSize(350, 50))
        self.existingTestsBtn.setMaximumSize(QtCore.QSize(350, 50))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.existingTestsBtn.setFont(font)
        self.existingTestsBtn.setStyleSheet("")
        self.existingTestsBtn.setInputMethodHints(QtCore.Qt.ImhNone)
        self.existingTestsBtn.setObjectName("existingTestsBtn")
        self.closeBtn = QtWidgets.QPushButton(self.centralwidget)
        self.closeBtn.setGeometry(QtCore.QRect(65, 470, 350, 50))
        self.closeBtn.setMinimumSize(QtCore.QSize(350, 50))
        self.closeBtn.setMaximumSize(QtCore.QSize(350, 50))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.closeBtn.setFont(font)
        self.closeBtn.setStyleSheet("")
        self.closeBtn.setInputMethodHints(QtCore.Qt.ImhNone)
        self.closeBtn.setObjectName("closeBtn")
        self.fileConditionsBtn = QtWidgets.QPushButton(self.centralwidget)
        self.fileConditionsBtn.setGeometry(QtCore.QRect(60, 320, 350, 50))
        self.fileConditionsBtn.setMinimumSize(QtCore.QSize(350, 50))
        self.fileConditionsBtn.setMaximumSize(QtCore.QSize(350, 50))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.fileConditionsBtn.setFont(font)
        self.fileConditionsBtn.setStyleSheet("QPushButton {\n"
"    background-color: #C22A13;\n"
"    border-radius: 25px;\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"     background-color: #D7331A;\n"
" }\n"
"\n"
"QPushButton:pressed {\n"
"     background-color: #C22A13;\n"
" }\n"
"\n"
"QPushButton:disabled {\n"
"     background-color: #E15D48;\n"
"    color: grey;\n"
" }")
        self.fileConditionsBtn.setInputMethodHints(QtCore.Qt.ImhNone)
        self.fileConditionsBtn.setObjectName("fileConditionsBtn")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Test Generator"))
        self.newTestBtn.setText(_translate("MainWindow", "Добавить новый тест"))
        self.existingTestsBtn.setText(_translate("MainWindow", "Пройти тест"))
        self.closeBtn.setText(_translate("MainWindow", "Закрыть"))
        self.fileConditionsBtn.setText(_translate("MainWindow", "Требования к файлу"))
