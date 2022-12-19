# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/NewLexDialog.ui'
#
# Created by: PyQt6 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_NewLexDialog(object):
    def setupUi(self, NewLexDialog):
        NewLexDialog.setObjectName("NewLexDialog")
        NewLexDialog.resize(400, 350)
        NewLexDialog.setMinimumSize(QtCore.QSize(400, 350))
        NewLexDialog.setMaximumSize(QtCore.QSize(400, 350))
        NewLexDialog.setSizeGripEnabled(False)
        self.explanation = QtWidgets.QLabel(NewLexDialog)
        self.explanation.setGeometry(QtCore.QRect(35, 10, 330, 35))
        self.explanation.setObjectName("explanation")
        self.groupBox = QtWidgets.QGroupBox(NewLexDialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 55, 380, 85))
        self.groupBox.setMinimumSize(QtCore.QSize(380, 85))
        self.groupBox.setMaximumSize(QtCore.QSize(380, 85))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(26, 26, 234, 16))
        self.label.setObjectName("label")
        self.speakerCode = QtWidgets.QComboBox(self.groupBox)
        self.speakerCode.setGeometry(QtCore.QRect(23, 46, 240, 30))
        self.speakerCode.setMinimumSize(QtCore.QSize(240, 30))
        self.speakerCode.setMaximumSize(QtCore.QSize(240, 30))
        self.speakerCode.setObjectName("speakerCode")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(281, 26, 71, 16))
        self.label_2.setObjectName("label_2")
        self.researcherCode = QtWidgets.QComboBox(self.groupBox)
        self.researcherCode.setGeometry(QtCore.QRect(278, 46, 77, 30))
        self.researcherCode.setMinimumSize(QtCore.QSize(77, 30))
        self.researcherCode.setMaximumSize(QtCore.QSize(77, 30))
        self.researcherCode.setObjectName("researcherCode")
        self.groupBox_2 = QtWidgets.QGroupBox(NewLexDialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 150, 380, 142))
        self.groupBox_2.setMinimumSize(QtCore.QSize(380, 142))
        self.groupBox_2.setMaximumSize(QtCore.QSize(380, 142))
        self.groupBox_2.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(48, 89, 34, 16))
        self.label_4.setMinimumSize(QtCore.QSize(34, 0))
        self.label_4.setMaximumSize(QtCore.QSize(34, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.entryWord = QtWidgets.QTextEdit(self.groupBox_2)
        self.entryWord.setGeometry(QtCore.QRect(90, 29, 280, 30))
        self.entryWord.setMinimumSize(QtCore.QSize(280, 30))
        self.entryWord.setMaximumSize(QtCore.QSize(280, 30))
        self.entryWord.setObjectName("entryWord")
        self.gloss = QtWidgets.QTextEdit(self.groupBox_2)
        self.gloss.setGeometry(QtCore.QRect(90, 70, 280, 60))
        self.gloss.setMinimumSize(QtCore.QSize(280, 60))
        self.gloss.setMaximumSize(QtCore.QSize(280, 60))
        self.gloss.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.gloss.setObjectName("gloss")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(17, 37, 65, 16))
        self.label_3.setMinimumSize(QtCore.QSize(65, 0))
        self.label_3.setMaximumSize(QtCore.QSize(65, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.buttonBox = QtWidgets.QDialogButtonBox(NewLexDialog)
        self.buttonBox.setGeometry(QtCore.QRect(224, 306, 164, 32))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(NewLexDialog)
        QtCore.QMetaObject.connectSlotsByName(NewLexDialog)

    def retranslateUi(self, NewLexDialog):
        _translate = QtCore.QCoreApplication.translate
        NewLexDialog.setWindowTitle(_translate("NewLexDialog", "New lexical entry"))
        self.explanation.setText(_translate("NewLexDialog", "Provide the information required to start a new entry.\n"
"Additional information can be added in the tab view."))
        self.groupBox.setTitle(_translate("NewLexDialog", "Metadata"))
        self.label.setText(_translate("NewLexDialog", "Speaker"))
        self.label_2.setText(_translate("NewLexDialog", "Researcher"))
        self.groupBox_2.setTitle(_translate("NewLexDialog", "Headword and definition"))
        self.label_4.setText(_translate("NewLexDialog", "Gloss"))
        self.label_3.setText(_translate("NewLexDialog", "Headword"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NewLexDialog = QtWidgets.QDialog()
    ui = Ui_NewLexDialog()
    ui.setupUi(NewLexDialog)
    NewLexDialog.show()
    sys.exit(app.exec())

