# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/SearchHelp.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SearchHelpDialog(object):
    def setupUi(self, SearchHelpDialog):
        SearchHelpDialog.setObjectName("SearchHelpDialog")
        SearchHelpDialog.resize(507, 576)
        SearchHelpDialog.setSizeGripEnabled(True)
        self.helpText = QtWidgets.QTextEdit(SearchHelpDialog)
        self.helpText.setGeometry(QtCore.QRect(14, 12, 481, 509))
        self.helpText.setObjectName("helpText")
        self.buttonBox = QtWidgets.QDialogButtonBox(SearchHelpDialog)
        self.buttonBox.setGeometry(QtCore.QRect(321, 534, 164, 32))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(SearchHelpDialog)
        QtCore.QMetaObject.connectSlotsByName(SearchHelpDialog)

    def retranslateUi(self, SearchHelpDialog):
        _translate = QtCore.QCoreApplication.translate
        SearchHelpDialog.setWindowTitle(_translate("SearchHelpDialog", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SearchHelpDialog = QtWidgets.QDialog()
    ui = Ui_SearchHelpDialog()
    ui.setupUi(SearchHelpDialog)
    SearchHelpDialog.show()
    sys.exit(app.exec_())

