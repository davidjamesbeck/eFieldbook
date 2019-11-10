# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/AddTextLine.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(400, 135)
        Dialog.setMinimumSize(QtCore.QSize(400, 0))
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.newLine = QtWidgets.QPlainTextEdit(Dialog)
        self.newLine.setMinimumSize(QtCore.QSize(360, 28))
        self.newLine.setMaximumSize(QtCore.QSize(16777215, 28))
        self.newLine.setObjectName("newLine")
        self.verticalLayout.addWidget(self.newLine)
        self.newGloss = QtWidgets.QPlainTextEdit(Dialog)
        self.newGloss.setMinimumSize(QtCore.QSize(360, 28))
        self.newGloss.setMaximumSize(QtCore.QSize(16777215, 28))
        self.newGloss.setObjectName("newGloss")
        self.verticalLayout.addWidget(self.newGloss)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(40, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.parsingBox = QtWidgets.QCheckBox(Dialog)
        self.parsingBox.setMinimumSize(QtCore.QSize(110, 0))
        self.parsingBox.setMaximumSize(QtCore.QSize(110, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.parsingBox.setFont(font)
        self.parsingBox.setObjectName("parsingBox")
        self.horizontalLayout.addWidget(self.parsingBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setMinimumSize(QtCore.QSize(164, 32))
        self.buttonBox.setMaximumSize(QtCore.QSize(164, 32))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add New Line"))
        self.newLine.setToolTip(_translate("Dialog", "new line"))
        self.newGloss.setToolTip(_translate("Dialog", "new gloss (optional if line is unparseable)"))
        self.parsingBox.setToolTip(_translate("Dialog", "check this box if the line is not a parseable\n"
"line in the target language (e.g., it is spoken\n"
"in the contact language, it is an interjectiion,\n"
"etc.). For interlocutors other than the main \n"
"narrator, a change of speaker, etc., add the\n"
"initials plus a colon and a space to the gloss."))
        self.parsingBox.setText(_translate("Dialog", "unparseable?"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
