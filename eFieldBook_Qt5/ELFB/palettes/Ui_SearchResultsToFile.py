# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/SearchResultsToFile.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OutPutFormatDialog(object):
    def setupUi(self, OutPutFormatDialog):
        OutPutFormatDialog.setObjectName("OutPutFormatDialog")
        OutPutFormatDialog.resize(329, 178)
        OutPutFormatDialog.setSizeGripEnabled(True)
        self.groupBox = QtWidgets.QGroupBox(OutPutFormatDialog)
        self.groupBox.setGeometry(QtCore.QRect(14, 5, 300, 130))
        self.groupBox.setMinimumSize(QtCore.QSize(300, 130))
        self.groupBox.setMaximumSize(QtCore.QSize(300, 130))
        self.groupBox.setObjectName("groupBox")
        self.HtmlBox = QtWidgets.QCheckBox(self.groupBox)
        self.HtmlBox.setGeometry(QtCore.QRect(13, 31, 86, 20))
        self.HtmlBox.setMinimumSize(QtCore.QSize(86, 20))
        self.HtmlBox.setMaximumSize(QtCore.QSize(86, 20))
        self.HtmlBox.setObjectName("HtmlBox")
        self.TxtBox = QtWidgets.QCheckBox(self.groupBox)
        self.TxtBox.setGeometry(QtCore.QRect(13, 64, 86, 20))
        self.TxtBox.setMinimumSize(QtCore.QSize(86, 20))
        self.TxtBox.setMaximumSize(QtCore.QSize(86, 20))
        self.TxtBox.setObjectName("TxtBox")
        self.customBox = QtWidgets.QCheckBox(self.groupBox)
        self.customBox.setGeometry(QtCore.QRect(13, 98, 86, 20))
        self.customBox.setMinimumSize(QtCore.QSize(86, 20))
        self.customBox.setMaximumSize(QtCore.QSize(86, 20))
        self.customBox.setObjectName("customBox")
        self.formatBox = QtWidgets.QGroupBox(self.groupBox)
        self.formatBox.setGeometry(QtCore.QRect(111, 27, 180, 90))
        self.formatBox.setMinimumSize(QtCore.QSize(180, 90))
        self.formatBox.setMaximumSize(QtCore.QSize(180, 90))
        self.formatBox.setObjectName("formatBox")
        self.comboBox = QtWidgets.QComboBox(self.formatBox)
        self.comboBox.setGeometry(QtCore.QRect(5, 39, 170, 30))
        self.comboBox.setMinimumSize(QtCore.QSize(170, 30))
        self.comboBox.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.buttonBox = QtWidgets.QDialogButtonBox(OutPutFormatDialog)
        self.buttonBox.setGeometry(QtCore.QRect(158, 141, 164, 32))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(OutPutFormatDialog)
        QtCore.QMetaObject.connectSlotsByName(OutPutFormatDialog)

    def retranslateUi(self, OutPutFormatDialog):
        _translate = QtCore.QCoreApplication.translate
        OutPutFormatDialog.setWindowTitle(_translate("OutPutFormatDialog", "Output format"))
        self.groupBox.setTitle(_translate("OutPutFormatDialog", "Select file format:"))
        self.HtmlBox.setText(_translate("OutPutFormatDialog", ".html"))
        self.TxtBox.setText(_translate("OutPutFormatDialog", ".txt"))
        self.customBox.setText(_translate("OutPutFormatDialog", "Custom …"))
        self.formatBox.setTitle(_translate("OutPutFormatDialog", "Custom formats"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OutPutFormatDialog = QtWidgets.QDialog()
    ui = Ui_OutPutFormatDialog()
    ui.setupUi(OutPutFormatDialog)
    OutPutFormatDialog.show()
    sys.exit(app.exec_())

