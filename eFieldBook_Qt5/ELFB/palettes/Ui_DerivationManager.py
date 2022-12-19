# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/DerivationManager.ui'
#
# Created by: PyQt6 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_DerivationManager(object):
    def setupUi(self, DerivationManager):
        DerivationManager.setObjectName("DerivationManager")
        DerivationManager.resize(300, 471)
        DerivationManager.setSizeGripEnabled(True)
        self.groupBox = QtWidgets.QGroupBox(DerivationManager)
        self.groupBox.setGeometry(QtCore.QRect(10, 9, 280, 410))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.lexList = QtWidgets.QListView(self.groupBox)
        self.lexList.setGeometry(QtCore.QRect(9, 9, 262, 392))
        self.lexList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.lexList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lexList.setObjectName("lexList")
        self.buttonBox = QtWidgets.QDialogButtonBox(DerivationManager)
        self.buttonBox.setGeometry(QtCore.QRect(123, 431, 164, 32))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(DerivationManager)
        QtCore.QMetaObject.connectSlotsByName(DerivationManager)

    def retranslateUi(self, DerivationManager):
        _translate = QtCore.QCoreApplication.translate
        DerivationManager.setWindowTitle(_translate("DerivationManager", "Select entry to link to"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DerivationManager = QtWidgets.QDialog()
    ui = Ui_DerivationManager()
    ui.setupUi(DerivationManager)
    DerivationManager.show()
    sys.exit(app.exec())

