# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/SessionDate.ui'
#
# Created by: PyQt6 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt6 import QtCore, QtWidgets


class Ui_SessionDateManager(object):
    def setupUi(self, SessionDateManager):
        SessionDateManager.setObjectName("SessionDateManager")
        SessionDateManager.resize(349, 97)
        SessionDateManager.setSizeGripEnabled(True)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(SessionDateManager)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(SessionDateManager)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(SessionDateManager)
        self.buttonBox.setMinimumSize(QtCore.QSize(164, 32))
        self.buttonBox.setMaximumSize(QtCore.QSize(164, 32))
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(SessionDateManager)
        QtCore.QMetaObject.connectSlotsByName(SessionDateManager)

    def retranslateUi(self, SessionDateManager):
        _translate = QtCore.QCoreApplication.translate
        SessionDateManager.setWindowTitle(_translate("SessionDateManager", "Session Date"))
        SessionDateManager.setToolTip(
            _translate("SessionDateManager", "Choose a date to fill in by default for the remainder of the \n"
                                             "session. Choose “Cancel” to use today’s date instead."))
        self.label.setText(_translate("SessionDateManager", "Set a default a date \n"
                                                            "for the work session."))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    SessionDateManager = QtWidgets.QDialog()
    ui = Ui_SessionDateManager()
    ui.setupUi(SessionDateManager)
    SessionDateManager.show()
    sys.exit(app.exec())
