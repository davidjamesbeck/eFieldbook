# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/LinkToLexicon.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EntryManager(object):
    def setupUi(self, EntryManager):
        EntryManager.setObjectName("EntryManager")
        EntryManager.resize(400, 455)
        EntryManager.setSizeGripEnabled(False)
        self.groupBox = QtWidgets.QGroupBox(EntryManager)
        self.groupBox.setGeometry(QtCore.QRect(10, 9, 380, 400))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.lexList = QtWidgets.QTreeWidget(self.groupBox)
        self.lexList.setGeometry(QtCore.QRect(3, 3, 374, 394))
        self.lexList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lexList.setAlternatingRowColors(True)
        self.lexList.setObjectName("lexList")
        self.lexList.headerItem().setText(0, "1")
        self.lexList.header().setVisible(False)
        self.buttonBox = QtWidgets.QDialogButtonBox(EntryManager)
        self.buttonBox.setGeometry(QtCore.QRect(223, 415, 164, 32))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(EntryManager)
        QtCore.QMetaObject.connectSlotsByName(EntryManager)

    def retranslateUi(self, EntryManager):
        _translate = QtCore.QCoreApplication.translate
        EntryManager.setWindowTitle(_translate("EntryManager", "Select lexical entry to link to"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EntryManager = QtWidgets.QDialog()
    ui = Ui_EntryManager()
    ui.setupUi(EntryManager)
    EntryManager.show()
    sys.exit(app.exec_())

