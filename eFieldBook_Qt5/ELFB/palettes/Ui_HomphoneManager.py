# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/HomphoneManager.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        Dialog.setSizeGripEnabled(True)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 250, 358, 43))
        self.layoutWidget.setObjectName("layoutWidget")
        self.hboxlayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setObjectName("hboxlayout")
        self.defaultSelect = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.defaultSelect.setFont(font)
        self.defaultSelect.setObjectName("defaultSelect")
        self.hboxlayout.addWidget(self.defaultSelect)
        spacerItem = QtWidgets.QSpacerItem(131, 31, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.okButton = QtWidgets.QPushButton(self.layoutWidget)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(self.layoutWidget)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout.addWidget(self.cancelButton)
        self.alternativesList = QtWidgets.QListWidget(Dialog)
        self.alternativesList.setGeometry(QtCore.QRect(21, 32, 358, 203))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.alternativesList.setFont(font)
        self.alternativesList.setObjectName("alternativesList")

        self.retranslateUi(Dialog)
        self.okButton.clicked.connect(Dialog.accept)
        self.cancelButton.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Select alternative"))
        self.defaultSelect.setToolTip(_translate("Dialog", "Choose the selected alternative by default, \n"
"don\'t ask about this set again."))
        self.defaultSelect.setText(_translate("Dialog", "Use selection as default"))
        self.okButton.setText(_translate("Dialog", "&OK"))
        self.cancelButton.setText(_translate("Dialog", "&Cancel"))
        self.alternativesList.setToolTip(_translate("Dialog", "Select the correct alternative from the list \n"
"of homphonous entreis in the index."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

