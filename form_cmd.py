# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form_cmd.ui'
#
# Created: Fri Mar 28 15:05:52 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(349, 611)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Consolas"))
        MainWindow.setFont(font)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.frame_2 = QtGui.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(311, 43))
        self.frame_2.setMaximumSize(QtCore.QSize(311, 43))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.l_mode = QtGui.QLabel(self.frame_2)
        self.l_mode.setGeometry(QtCore.QRect(10, 10, 281, 23))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.l_mode.setFont(font)
        self.l_mode.setObjectName(_fromUtf8("l_mode"))
        self.verticalLayout_3.addWidget(self.frame_2)
        self.f_democracy = QtGui.QFrame(self.frame)
        self.f_democracy.setMinimumSize(QtCore.QSize(311, 0))
        self.f_democracy.setFrameShape(QtGui.QFrame.StyledPanel)
        self.f_democracy.setFrameShadow(QtGui.QFrame.Raised)
        self.f_democracy.setObjectName(_fromUtf8("f_democracy"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.f_democracy)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.l_democracy = QtGui.QLabel(self.f_democracy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.l_democracy.setFont(font)
        self.l_democracy.setObjectName(_fromUtf8("l_democracy"))
        self.verticalLayout_2.addWidget(self.l_democracy)
        self.verticalLayout_3.addWidget(self.f_democracy)
        self.f_anarchy = QtGui.QFrame(self.frame)
        self.f_anarchy.setMinimumSize(QtCore.QSize(311, 0))
        self.f_anarchy.setFrameShape(QtGui.QFrame.StyledPanel)
        self.f_anarchy.setFrameShadow(QtGui.QFrame.Raised)
        self.f_anarchy.setObjectName(_fromUtf8("f_anarchy"))
        self.verticalLayout = QtGui.QVBoxLayout(self.f_anarchy)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.l_anarchy = QtGui.QLabel(self.f_anarchy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.l_anarchy.setFont(font)
        self.l_anarchy.setObjectName(_fromUtf8("l_anarchy"))
        self.verticalLayout.addWidget(self.l_anarchy)
        self.verticalLayout_3.addWidget(self.f_anarchy)
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 349, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Commands", None))
        self.l_mode.setText(_translate("MainWindow", "Mode", None))
        self.l_democracy.setText(_translate("MainWindow", "Democracy cmds", None))
        self.l_anarchy.setText(_translate("MainWindow", "All cmds", None))

