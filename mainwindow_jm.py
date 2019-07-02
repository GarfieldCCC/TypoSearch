# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow_jm.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

import jieba, re, string, gensim, operator
from pypinyin import lazy_pinyin
from PyQt5 import QtCore, QtGui, QtWidgets
from TyposSearch.FeInterface import Ui_FeInterface
from PyQt5.QtWidgets import *

PATH1 = "Data/jieba.txt"
PATH2 = "Data/cn_dict.txt"
PATH3 = "Data/words.txt"
PATH4 = "Data/pinyin.txt"
PATH5 = "Data/stopwords.txt"

PUNCTUATION_LIST = "["
PUNCTUATION_LIST += string.punctuation
PUNCTUATION_LIST += "。，？：；、｛｝［］‘“”’《》／！％……（）]"

Data_path = "E:/Project/Python/NLP/Gensim/Word2Vec/Model/"
Type = "wiki.model"
model_path = Data_path + Type

model = gensim.models.Word2Vec.load(model_path)


def getPinyin(word):
    p = ""
    for py in lazy_pinyin(word):
        p += str(py)
    return p


def construct_dict(file_path, isPinyin=True, isDictionary=True):
    if isDictionary == True:
        if isPinyin == True:
            word_freq = {}
            with open(file_path, "r", encoding='utf-8') as f:
                for line in f:
                    info = line.split()
                    word = getPinyin(info[0])
                    frequency = info[1]
                    word_freq[word] = frequency
            return word_freq
        else:
            word_freq = {}
            with open(file_path, "r", encoding='utf-8') as f:
                for line in f:
                    info = line.split()
                    word = info[0]
                    frequency = info[1]
                    word_freq[word] = frequency
            return word_freq
    else:
        if isPinyin == True:
            word_freq = []
            with open(file_path, "r", encoding='utf-8') as f:
                for line in f:
                    info = line.split()
                    word = getPinyin(info[0])
                    # frequency = info[1]
                    word_freq.append(word)
            return word_freq
        else:
            word_freq = []
            with open(file_path, "r", encoding='utf-8') as f:
                for line in f:
                    info = line.split()
                    word = info[0]
                    # frequency = info[1]
                    word_freq.append(word)
            return word_freq


NWORDS = construct_dict(PATH1, isPinyin=True, isDictionary=True)


def get_alphabet(file_path):
    alphabet = []
    for py in open(file_path):
        alphabet.append(str(py.strip()))
    return alphabet


alphabet = get_alphabet(PATH4)


def edits1(word):
    word = getPinyin(word)
    n = len(word)
    return set([word[0:i] + word[i + 1:] for i in range(n)] +  # deletion
               [word[0:i] + word[i + 1] + word[i] + word[i + 2:] for i in range(n - 1)] +  # transposition
               [word[0:i] + c + word[i + 1:] for i in range(n) for c in alphabet] +  # alteration
               [word[0:i] + c + word[i:] for i in range(n + 1) for c in alphabet])  # insertion


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)


def known(words): return set(w for w in words if w in NWORDS)


def match_Chinese(word):
    return True if re.match(u'[\u4e00-\u9fa5]', word) != None else False


def correct_pinyin(word):
    candidates = known([getPinyin(word)]) or known(edits1(word)) or known_edits2(word) or [getPinyin(word)]
    return max(candidates, key=lambda w: NWORDS[w])


def cut_sentence(sentence, cut_all):
    jieba_cut = jieba.cut(sentence, cut_all=cut_all)
    return "\t".join(jieba_cut).split("\t")


def correct(py, dictionary):
    if py in dictionary:
        L = dictionary[py]
        num = []
        index = 0
        while index < len(L):
            num.append(L[index + 1])
            index += 2
        m = max(num)
        return L[L.index(m) - 1]
    else:
        return "有问题"


def just_correct(words, dictionary_hanzi, correct_sentence, dictionary_pinyin):
    "初级修改"
    Correct = []
    ori_sentence = ""
    for word in words:
        if match_Chinese(word):
            if word not in PUNCTUATION_LIST:
                if word in dictionary_hanzi:
                    correct_sentence += word
                    ori_sentence += word
                else:
                    correctpinyin = correct_pinyin(word)
                    correct_sentence += "<font color=\"#FF0000\">" + correct(correctpinyin,
                                                                             dictionary_pinyin) + "</font>"
                    ori_sentence += "<font color=\"#FF0001\">" + word + "</font>"
                    Correct.append([word, correct(correctpinyin, dictionary_pinyin)])  # 纠正前，纠正后
            else:
                correct_sentence += word
                ori_sentence += word
        else:
            correct_sentence += word
            ori_sentence += word
    print("\n")
    print(correct_sentence)
    print(Correct)
    return ori_sentence, correct_sentence


def read_pinyin(file_path):
    word_freq = []
    with open(file_path, "r", encoding='utf-8') as f:
        for line in f:
            info = line.split()
            word = getPinyin(info[0])
            word_freq.append(word)
    return word_freq


def read_jiebatxt(file_path):
    wordsdic = construct_dict(file_path, isPinyin=False, isDictionary=True)
    pinyinDic = read_pinyin(file_path)
    pinyindic = set(pinyinDic)
    dictionary = {}
    for word in wordsdic:
        py = getPinyin(word)
        if py in pinyindic:
            l = []
            l.append(word)
            l.append(int(wordsdic[word]))
            if py not in dictionary:
                dictionary[getPinyin(word)] = l
            else:
                dictionary[py].append(word)
                dictionary[py].append(int(wordsdic[word]))
    return dictionary


dictionary_pinyin = read_jiebatxt(PATH1)
dictionary_hanzi = construct_dict(PATH1, isPinyin=False, isDictionary=False)


def loadStopWords(file_path):
    stopwords = []
    for line in open(file_path, encoding='utf-8'):
        stopwords.append(line.strip())
    return stopwords


def get_sentence_words_dic(sentence_list):
    dic = {}
    for item in sentence_list:
        dic[str(item)] = cut_sentence(item, cut_all=True)
    return dic


def remove_space(List):
    "去除空格项"
    l = List
    for i in l:
        if " " in l:
            l.remove(" ")
    return l


def remove_blank(List):
    "去除空项"
    L = []
    for i in List:
        if len(i) != 0:
            L.append(i)
    return L


def seg_sentence(sentence):
    "把句子分割成一句一句的, 并返回列表"
    return re.split(PUNCTUATION_LIST, sentence)


def get_list(sentence):
    return remove_space(remove_blank(seg_sentence(sentence)))


def get_similarity(word, words):
    "返回词语相关性"
    similarity = 0
    for w in words:
        if word != w and word in model and w in model:
            similarity += model.similarity(word, w)
    return similarity / len(words)


def sort(Dictionary):
    "给字典按键值降序排序"
    return sorted(Dictionary.items(), key=operator.itemgetter(0), reverse=True)


def find_index(aim, l):
    for i in range(len(l)):
        if l[i][1] == aim:
            return i
    return -1


def get_abs_between_two_words(word1, word2, l):
    "获取两个词语间的距离"
    return abs(find_index(word1, l) - find_index(word2, l))


def suggest_modify(correct_sentence, dictionary_pinyin):
    "给出建议修改意见"

    res = ""
    stopwords = loadStopWords(PATH5)
    sentence_words_dic = get_sentence_words_dic(get_list(correct_sentence))
    # print(sentence_words_dic)

    for key in sentence_words_dic:
        similarity_dic = {}
        for word in sentence_words_dic[key]:
            if match_Chinese(word) and word not in stopwords:
                pinyin_list = dictionary_pinyin[getPinyin(word)]
                # print(pinyin_list)
                length = len(pinyin_list)
                for i in range(0, length, 2):
                    similarity_dic[get_similarity(pinyin_list[i], sentence_words_dic[key])] = pinyin_list[i]

        sorted_similarity_dic = sort(similarity_dic)
        # print(sorted_similarity_dic)

        dic_len = len(sorted_similarity_dic)

        wrong_word, suggest_word, suggest_sentence = " ", "", ""

        for item in sorted_similarity_dic:
            if item[1] in sentence_words_dic[key]:
                continue
            else:
                suggest_word = item[1]

                for word in sentence_words_dic[key]:
                    if getPinyin(word) == getPinyin(suggest_word) and get_abs_between_two_words(word, suggest_word,
                                                                                                sorted_similarity_dic) > dic_len * 0.24:
                        # 如果找到了一个句子中的词语的拼音和建议修改词语的拼音相同
                        wrong_word = word
                        break

                suggest_sentence = key
                if len(cut_sentence(correct_sentence, cut_all=False)) > 1 and wrong_word != " ":
                    r = "(建议将 " + suggest_sentence + " 中的 " + "<font color=\"#FF0000\">" + wrong_word + "</font>" + " 修改为 " + "<font color=\"#FF0000\">" + suggest_word + "</font>" + ")" + "<br>"
                    # print(r)
                    res += r

                break
    return res


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1093, 726)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(17)
        self.gridLayout.setObjectName("gridLayout")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 4, 1, 1)
        self.input = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.input.setFont(font)
        self.input.setObjectName("input")
        self.gridLayout.addWidget(self.input, 2, 1, 1, 1)
        self.output = QtWidgets.QTextBrowser(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.output.setFont(font)
        self.output.setObjectName("output")
        self.gridLayout.addWidget(self.output, 2, 3, 1, 1)
        self.rectify = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rectify.sizePolicy().hasHeightForWidth())
        self.rectify.setSizePolicy(sizePolicy)
        self.rectify.setMinimumSize(QtCore.QSize(30, 30))
        self.rectify.setMaximumSize(QtCore.QSize(127, 80))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rectify.setFont(font)
        self.rectify.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.rectify.setObjectName("rectify")
        self.gridLayout.addWidget(self.rectify, 3, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(45, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 2, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 6, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 6, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem5 = QtWidgets.QSpacerItem(40, 13, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1093, 26))
        self.menubar.setObjectName("menubar")
        self.function = QtWidgets.QMenu(self.menubar)
        self.function.setObjectName("function")
        MainWindow.setMenuBar(self.menubar)
        self.readdoc = QtWidgets.QAction(MainWindow)
        self.readdoc.setObjectName("readdoc")
        self.userfeedback = QtWidgets.QAction(MainWindow)
        self.userfeedback.setObjectName("userfeedback")
        self.function.addAction(self.readdoc)
        self.function.addAction(self.userfeedback)
        self.menubar.addAction(self.function.menuAction())

        self.retranslateUi(MainWindow)
        self.rectify.clicked.connect(self.on_click)
        self.readdoc.triggered.connect(MainWindow.openfile_jc)
        self.userfeedback.triggered.connect(self.open_FeIterface)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def on_click(self):
        data = self.input.toPlainText()

        correct_sentence = ""
        words = cut_sentence(str(data).strip('\n'), cut_all=False)

        ori_sentence, correct_sentence = just_correct(words, dictionary_hanzi, correct_sentence, dictionary_pinyin)
        sm = suggest_modify(correct_sentence, dictionary_pinyin)

        output = correct_sentence + "<br><br>" + sm
        self.output.setText(output)
        self.input.setText(ori_sentence)
        self.userfeedback.triggered.connect(self.open_FeIterface)

    windowList = []

    def open_FeIterface(self):
        the_window = FeInterface()
        self.windowList.append(the_window)  ##注：没有这句，是不打开另一个主界面的！
        # self.close()
        the_window.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_1.setText(_translate("MainWindow", "原文"))
        self.label_2.setText(_translate("MainWindow", "修改后的结果"))
        self.input.setHtml(_translate("MainWindow",
                                      "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                      "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                      "p, li { white-space: pre-wrap; }\n"
                                      "</style></head><body style=\" font-family:\'宋体\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                      "<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:8pt;\"><br /></p></body></html>"))
        self.output.setHtml(_translate("MainWindow",
                                       "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                       "p, li { white-space: pre-wrap; }\n"
                                       "</style></head><body style=\" font-family:\'宋体\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                       "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:8pt;\"><br /></p></body></html>"))
        self.rectify.setText(_translate("MainWindow", "rectify"))
        self.function.setTitle(_translate("MainWindow", "功能"))
        self.readdoc.setText(_translate("MainWindow", "读取文档"))
        self.userfeedback.setText(_translate("MainWindow", "用户反馈"))


class FeInterface(QMainWindow):
    def __init__(self, parent=None):
        super(FeInterface, self).__init__(parent)
        self.ui = Ui_FeInterface()
        self.ui.setupUi(self)
