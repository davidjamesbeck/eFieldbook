# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/sorter/ui/mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        MainWindow.resize(578, 663)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.start = QtGui.QListView(self.centralWidget)
        self.start.setGeometry(QtCore.QRect(20, 20, 261, 551))
        self.start.setObjectName(_fromUtf8("start"))
        self.finish = QtGui.QListView(self.centralWidget)
        self.finish.setGeometry(QtCore.QRect(300, 20, 261, 551))
        self.finish.setObjectName(_fromUtf8("finish"))
        self.doSort = QtGui.QPushButton(self.centralWidget)
        self.doSort.setGeometry(QtCore.QRect(420, 600, 110, 32))
        self.doSort.setObjectName(_fromUtf8("doSort"))
        self.sortOrder = QtGui.QPlainTextEdit(self.centralWidget)
        self.sortOrder.setGeometry(QtCore.QRect(20, 580, 391, 71))
        self.sortOrder.setObjectName(_fromUtf8("sortOrder"))
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.doSort.setText(_translate("MainWindow", "Sort", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

