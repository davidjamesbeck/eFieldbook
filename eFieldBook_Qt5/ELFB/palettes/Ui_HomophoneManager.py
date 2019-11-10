# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/HomophoneManager.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(382, 307)
        Dialog.setStyleSheet("QPushButton {\n"
"    background: white;\n"
"    color: black;\n"
"    border: 0px solid black;\n"
"    border-radius: 4px;\n"
"    padding: 0 0 0 0;\n"
"    margin: 0 0 0 0;\n"
"    min-height: 24px;\n"
"    max-height: 24px;\n"
"    min-width: 55px;\n"
"    max-width: 55px;\n"
"    font-size: 11pts;\n"
"}\n"
"\n"
"QPushButton:default {\n"
"    background: #2E9AFE;\n"
"    color: white;\n"
"}\n"
"")
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.line = QtWidgets.QPlainTextEdit(Dialog)
        self.line.setMinimumSize(QtCore.QSize(358, 30))
        self.line.setMaximumSize(QtCore.QSize(358, 30))
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.alternativesList = QtWidgets.QListWidget(Dialog)
        self.alternativesList.setMinimumSize(QtCore.QSize(358, 150))
        self.alternativesList.setMaximumSize(QtCore.QSize(358, 150))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.alternativesList.setFont(font)
        self.alternativesList.setObjectName("alternativesList")
        self.verticalLayout.addWidget(self.alternativesList)
        self.gloss = QtWidgets.QPlainTextEdit(Dialog)
        self.gloss.setMinimumSize(QtCore.QSize(358, 30))
        self.gloss.setMaximumSize(QtCore.QSize(358, 30))
        self.gloss.setObjectName("gloss")
        self.verticalLayout.addWidget(self.gloss)
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.defaultSelect = QtWidgets.QCheckBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.defaultSelect.setFont(font)
        self.defaultSelect.setObjectName("defaultSelect")
        self.hboxlayout.addWidget(self.defaultSelect)
        spacerItem1 = QtWidgets.QSpacerItem(131, 31, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout.addWidget(self.cancelButton)
        self.okButton = QtWidgets.QPushButton(Dialog)
        self.okButton.setDefault(True)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)
        self.verticalLayout.addLayout(self.hboxlayout)

        self.retranslateUi(Dialog)
        self.okButton.clicked.connect(Dialog.accept)
        self.cancelButton.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Select alternative"))
        self.alternativesList.setToolTip(_translate("Dialog", "Select the correct alternative from the list \n"
"of homphonous entreis in the index."))
        self.defaultSelect.setToolTip(_translate("Dialog", "Choose the selected alternative by default, \n"
"don\'t ask about this set again."))
        self.defaultSelect.setText(_translate("Dialog", "Use selection as default"))
        self.cancelButton.setText(_translate("Dialog", "&Cancel"))
        self.okButton.setText(_translate("Dialog", "&OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

