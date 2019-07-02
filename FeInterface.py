# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FeInterface.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FeInterface(object):
    def setupUi(self, FeInterface):
        FeInterface.setObjectName("FeInterface")
        FeInterface.resize(553, 643)
        self.centralwidget = QtWidgets.QWidget(FeInterface)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(488, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(10, 482, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(10, 482, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(488, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMaximumSize(QtCore.QSize(143, 68))
        self.pushButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 1, 1, 1)
        FeInterface.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(FeInterface)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 553, 26))
        self.menubar.setObjectName("menubar")
        FeInterface.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(FeInterface)
        self.statusbar.setObjectName("statusbar")
        FeInterface.setStatusBar(self.statusbar)

        self.retranslateUi(FeInterface)
        self.pushButton.clicked.connect(self.savefile_jc)
        QtCore.QMetaObject.connectSlotsByName(FeInterface)

    def savefile_jc(self):
        try:
            StrText = self.textEdit.toPlainText()
            qS = str(StrText)
            f = open("text.txt", 'a')
            print(qS)
            print(f.write('\n{}'.format(qS)))
            f.close()
        except Exception as e:
            print(e)

    def retranslateUi(self, FeInterface):
        _translate = QtCore.QCoreApplication.translate
        FeInterface.setWindowTitle(_translate("FeInterface", "MainWindow"))
        self.pushButton.setText(_translate("FeInterface", "提交反馈"))
