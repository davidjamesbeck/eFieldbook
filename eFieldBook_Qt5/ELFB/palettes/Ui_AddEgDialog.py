# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/AddEgDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddEg(object):
    def setupUi(self, AddEg):
        AddEg.setObjectName("AddEg")
        AddEg.resize(227, 149)
        AddEg.setSizeGripEnabled(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddEg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AddEg)
        self.label.setMinimumSize(QtCore.QSize(0, 16))
        self.label.setMaximumSize(QtCore.QSize(16777215, 16))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.IDRef = QtWidgets.QLineEdit(AddEg)
        self.IDRef.setMinimumSize(QtCore.QSize(0, 24))
        self.IDRef.setMaximumSize(QtCore.QSize(16777215, 24))
        self.IDRef.setObjectName("IDRef")
        self.verticalLayout.addWidget(self.IDRef)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.checkBox = QtWidgets.QCheckBox(AddEg)
        font = QtGui.QFont()
        font.setItalic(True)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddEg)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddEg)
        QtCore.QMetaObject.connectSlotsByName(AddEg)

    def retranslateUi(self, AddEg):
        _translate = QtCore.QCoreApplication.translate
        AddEg.setWindowTitle(_translate("AddEg", "Add example"))
        self.label.setText(_translate("AddEg", "Enter IDREF"))
        self.IDRef.setToolTip(_translate("AddEg", "Add the ID number of the example to add.\n"
"This can be copied-and-pasted from the\n"
"top left corner of the example viewed in the\n"
"Examples tab."))
        self.checkBox.setToolTip(_translate("AddEg", "check to add the example currently \n"
"visible in the Examples tab"))
        self.checkBox.setText(_translate("AddEg", "Add current example"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddEg = QtWidgets.QDialog()
    ui = Ui_AddEg()
    ui.setupUi(AddEg)
    AddEg.show()
    sys.exit(app.exec_())

