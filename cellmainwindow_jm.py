# -*- coding: utf-8 -*-
import docx, os
import sys
from PyQt5.QtWidgets import *
from TyposSearch.mainwindow_jm import Ui_MainWindow


def readtxt(filename):
    """读取txt"""
    s = ""
    for line in open(filename, "r"):
        s += line
    return s


def readdocx(filename):
    """读取docx"""

    s = ""
    file = docx.Document(filename)
    for para in file.paragraphs:
        s += para.text + "\n"
    return s


def doc2docx(doc_name):
    """
    doc转docx
    """
    try:
        # 首先将doc转换成docx
        from win32com import client
        word = client.Dispatch("Word.Application")
        doc = word.Documents.Open(doc_name)
        newpath = os.path.splitext(doc_name)[0] + '.docx'
        # 使用参数16表示将doc转换成docx
        doc.SaveAs(newpath, 16)
        doc.Close()
        word.Quit()
    except:
        pass
    return doc_name + 'x'


def readfile(fileName):
    """读取文本"""
    Type = ['doc', 'ocx', 'txt']
    if fileName[-3:] not in Type:
        print("无法读取此类型的文本")
    else:
        if fileName[-3:] == 'doc':
            name = doc2docx(fileName)
            return readdocx(name)
        elif fileName[-3:] == 'ocx':
            return readdocx(fileName)
        else:
            return readtxt(fileName)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def openfile_jc(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "C:/",
                                                          "Text/Docx Files (*.txt;*.docx;*.doc);;All Files (*)")

        self.ui.input.clear()  # 清除textEdit以前的内容

        if fileName1 == "":
            print("\n取消选择")
            return

        content = readfile(fileName1)
        print("content: ", content)

        self.ui.input.setText(content)
        # self.ui.lineEdit.setText(fileName1)
        # self.Openfile1.setStatusTip('正在打开+fileName1')

    def savefile_jc(self):
        fileName2, ok2 = QFileDialog.getSaveFileName(self,
                                                     "文件保存",
                                                     "C:/",
                                                     "All Files (*);;Text Files (*.txt)")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

# 激起学习是人工智能领遇最能体现智能的一个分枝!一定会暴发一场革命！
