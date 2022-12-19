# -*- coding: utf-8 -*-

# Form implementation generated from reading ui
# file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/GrammarManager.ui'
#
# Created by: PyQt6 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt6 import QtCore, QtWidgets


class Ui_gManager(object):
    def setupUi(self, gManager):
        gManager.setObjectName("gManager")
        gManager.resize(430, 477)
        gManager.setSizeGripEnabled(False)
        self.lexBox = QtWidgets.QGroupBox(gManager)
        self.lexBox.setGeometry(QtCore.QRect(10, 9, 410, 386))
        sizePolicy = QtWidgets.QSizePolicy()
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lexBox.sizePolicy().hasHeightForWidth())
        self.lexBox.setSizePolicy(sizePolicy)
        self.lexBox.setMinimumSize(QtCore.QSize(410, 386))
        self.lexBox.setMaximumSize(QtCore.QSize(410, 386))
        self.lexBox.setTitle("")
        self.lexBox.setObjectName("lexBox")
        self.label = QtWidgets.QLabel(self.lexBox)
        self.label.setGeometry(QtCore.QRect(15, 15, 170, 16))
        self.label.setMinimumSize(QtCore.QSize(170, 16))
        self.label.setMaximumSize(QtCore.QSize(170, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.lexBox)
        self.label_2.setGeometry(QtCore.QRect(15, 186, 170, 16))
        self.label_2.setMinimumSize(QtCore.QSize(170, 16))
        self.label_2.setMaximumSize(QtCore.QSize(170, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.lexBox)
        self.label_3.setGeometry(QtCore.QRect(15, 312, 170, 16))
        self.label_3.setMinimumSize(QtCore.QSize(170, 16))
        self.label_3.setMaximumSize(QtCore.QSize(170, 16))
        self.label_3.setObjectName("label_3")
        self.textEdit = QtWidgets.QTextEdit(self.lexBox)
        self.textEdit.setGeometry(QtCore.QRect(15, 338, 380, 36))
        self.textEdit.setObjectName("textEdit")
        self.groupBox_2 = QtWidgets.QGroupBox(gManager)
        self.groupBox_2.setGeometry(QtCore.QRect(165, 403, 255, 65))
        self.groupBox_2.setMinimumSize(QtCore.QSize(255, 65))
        self.groupBox_2.setMaximumSize(QtCore.QSize(255, 65))
        self.groupBox_2.setStyleSheet("QPushButton {\n"
                                      "    min-width: 76px;\n"
                                      "    min-height: 30px;\n"
                                      "    max-width: 76px;\n"
                                      "    max-height: 30px;\n"
                                      "}")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.Del = QtWidgets.QPushButton(self.groupBox_2)
        self.Del.setGeometry(QtCore.QRect(9, 5, 78, 32))
        self.Del.setObjectName("Del")
        self.Add = QtWidgets.QPushButton(self.groupBox_2)
        self.Add.setGeometry(QtCore.QRect(89, 5, 78, 32))
        self.Add.setObjectName("Add")
        self.Clear = QtWidgets.QPushButton(self.groupBox_2)
        self.Clear.setGeometry(QtCore.QRect(169, 5, 78, 32))
        self.Clear.setObjectName("Clear")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.groupBox_2)
        self.buttonBox.setGeometry(QtCore.QRect(83, 32, 164, 32))
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(gManager)
        QtCore.QMetaObject.connectSlotsByName(gManager)

    def retranslateUi(self, gManager):
        _translate = QtCore.QCoreApplication.translate
        gManager.setWindowTitle(_translate("gManager", "Grammar and cross-references"))
        self.label.setText(_translate("gManager", "Grammatical information:"))
        self.label_2.setText(_translate("gManager", "Alternative forms:"))
        self.label_3.setText(_translate("gManager", "Cross-references:"))
        self.Del.setText(_translate("gManager", "Delete"))
        self.Add.setText(_translate("gManager", "Add"))
        self.Clear.setText(_translate("gManager", "Clear"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    gManager = QtWidgets.QDialog()
    ui = Ui_gManager()
    ui.setupUi(gManager)
    gManager.show()
    sys.exit(app.exec())
