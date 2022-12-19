# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/DefinitionsManager.ui'
#
# Created by: PyQt6 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1016, 632)
        Dialog.setMinimumSize(QtCore.QSize(531, 100))
        Dialog.setMaximumSize(QtCore.QSize(16777215, 1677215))
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
"\n"
"QToolButton {\n"
"    min-width: 20px;\n"
"    max-width: 20px;\n"
"    min-height: 20px;\n"
"    max-height: 20px;\n"
"     background: #2E9AFE;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background: #F2F2F2;\n"
"    color: #848484;\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    background: #A4A4A4;\n"
"    border: 2px outset #A4A4A4;\n"
"}")
        Dialog.setSizeGripEnabled(False)
        self.lexBox = QtWidgets.QGroupBox(Dialog)
        self.lexBox.setGeometry(QtCore.QRect(13, 10, 466, 579))
        self.lexBox.setTitle("")
        self.lexBox.setObjectName("lexBox")
        self.Kill = QtWidgets.QToolButton(self.lexBox)
        self.Kill.setGeometry(QtCore.QRect(368, 549, 22, 22))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Kill.setFont(font)
        self.Kill.setObjectName("Kill")
        self.New = QtWidgets.QToolButton(self.lexBox)
        self.New.setGeometry(QtCore.QRect(338, 549, 22, 22))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.New.setFont(font)
        self.New.setObjectName("New")
        self.orderEntries = QtWidgets.QSpinBox(self.lexBox)
        self.orderEntries.setGeometry(QtCore.QRect(403, 548, 55, 24))
        self.orderEntries.setMinimumSize(QtCore.QSize(55, 24))
        self.orderEntries.setMaximumSize(QtCore.QSize(55, 24))
        self.orderEntries.setReadOnly(False)
        self.orderEntries.setMaximum(0)
        self.orderEntries.setObjectName("orderEntries")
        self.fieldBox = QtWidgets.QGroupBox(Dialog)
        self.fieldBox.setGeometry(QtCore.QRect(491, 10, 511, 579))
        self.fieldBox.setStyleSheet("")
        self.fieldBox.setTitle("")
        self.fieldBox.setObjectName("fieldBox")
        self.addEgBtn = QtWidgets.QToolButton(self.fieldBox)
        self.addEgBtn.setGeometry(QtCore.QRect(13, 442, 22, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.addEgBtn.setFont(font)
        self.addEgBtn.setObjectName("addEgBtn")
        self.minusEgBtn = QtWidgets.QToolButton(self.fieldBox)
        self.minusEgBtn.setGeometry(QtCore.QRect(40, 442, 22, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.minusEgBtn.setFont(font)
        self.minusEgBtn.setObjectName("minusEgBtn")
        self.diaBox = QtWidgets.QGroupBox(self.fieldBox)
        self.diaBox.setGeometry(QtCore.QRect(10, 10, 490, 128))
        self.diaBox.setStyleSheet("")
        self.diaBox.setTitle("")
        self.diaBox.setObjectName("diaBox")
        self.Part = QtWidgets.QLabel(self.diaBox)
        self.Part.setGeometry(QtCore.QRect(10, 8, 50, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Part.setFont(font)
        self.Part.setObjectName("Part")
        self.Register = QtWidgets.QLabel(self.diaBox)
        self.Register.setGeometry(QtCore.QRect(260, 14, 52, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Register.setFont(font)
        self.Register.setObjectName("Register")
        self.Dialect = QtWidgets.QLabel(self.diaBox)
        self.Dialect.setGeometry(QtCore.QRect(10, 52, 44, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Dialect.setFont(font)
        self.Dialect.setObjectName("Dialect")
        self.AltLabel = QtWidgets.QLabel(self.diaBox)
        self.AltLabel.setGeometry(QtCore.QRect(260, 52, 52, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.AltLabel.setFont(font)
        self.AltLabel.setObjectName("AltLabel")
        self.label = QtWidgets.QLabel(self.diaBox)
        self.label.setGeometry(QtCore.QRect(10, 84, 57, 31))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.diaBox)
        self.label_2.setGeometry(QtCore.QRect(260, 84, 69, 31))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.PLanguage = QtWidgets.QLabel(self.fieldBox)
        self.PLanguage.setGeometry(QtCore.QRect(10, 171, 62, 32))
        self.PLanguage.setObjectName("PLanguage")
        self.SLanguage = QtWidgets.QLabel(self.fieldBox)
        self.SLanguage.setGeometry(QtCore.QRect(10, 250, 65, 32))
        self.SLanguage.setObjectName("SLanguage")
        self.Examples = QtWidgets.QLabel(self.fieldBox)
        self.Examples.setGeometry(QtCore.QRect(10, 420, 57, 16))
        self.Examples.setObjectName("Examples")
        self.switchEgBtn = QtWidgets.QPushButton(self.fieldBox)
        self.switchEgBtn.setGeometry(QtCore.QRect(10, 470, 55, 24))
        self.switchEgBtn.setStyleSheet("")
        self.switchEgBtn.setObjectName("switchEgBtn")
        self.Clear = QtWidgets.QPushButton(self.fieldBox)
        self.Clear.setGeometry(QtCore.QRect(367, 548, 55, 24))
        self.Clear.setObjectName("Clear")
        self.Update = QtWidgets.QPushButton(self.fieldBox)
        self.Update.setGeometry(QtCore.QRect(437, 548, 55, 24))
        self.Update.setObjectName("Update")
        self.SLanguage_2 = QtWidgets.QLabel(self.fieldBox)
        self.SLanguage_2.setGeometry(QtCore.QRect(10, 330, 65, 32))
        self.SLanguage_2.setWordWrap(True)
        self.SLanguage_2.setObjectName("SLanguage_2")
        self.OkayBtn = QtWidgets.QPushButton(Dialog)
        self.OkayBtn.setGeometry(QtCore.QRect(942, 598, 55, 24))
        self.OkayBtn.setDefault(True)
        self.OkayBtn.setObjectName("OkayBtn")
        self.CancelBtn = QtWidgets.QPushButton(Dialog)
        self.CancelBtn.setGeometry(QtCore.QRect(868, 598, 55, 24))
        self.CancelBtn.setObjectName("CancelBtn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Update definitions"))
        self.Kill.setToolTip(_translate("Dialog", "delete selected subentry"))
        self.Kill.setText(_translate("Dialog", "–"))
        self.New.setToolTip(_translate("Dialog", "add new subentry"))
        self.New.setText(_translate("Dialog", "+"))
        self.orderEntries.setToolTip(_translate("Dialog", "move the selected subentry up or down in the list"))
        self.addEgBtn.setToolTip(_translate("Dialog", "add example to selected subentry"))
        self.addEgBtn.setText(_translate("Dialog", "+"))
        self.minusEgBtn.setToolTip(_translate("Dialog", "remove example from selected subentry"))
        self.minusEgBtn.setText(_translate("Dialog", "–"))
        self.Part.setText(_translate("Dialog", "Part of\n"
"Speech"))
        self.Register.setText(_translate("Dialog", "Register"))
        self.Dialect.setText(_translate("Dialog", "Dialect"))
        self.AltLabel.setText(_translate("Dialog", "Alternate"))
        self.label.setText(_translate("Dialog", "Primary Indices"))
        self.label_2.setText(_translate("Dialog", "Secondary Indices"))
        self.PLanguage.setText(_translate("Dialog", "Primary\n"
"language"))
        self.SLanguage.setText(_translate("Dialog", "Secondary\n"
"language"))
        self.Examples.setText(_translate("Dialog", "Examples"))
        self.switchEgBtn.setToolTip(_translate("Dialog", "move example to a different subentry"))
        self.switchEgBtn.setText(_translate("Dialog", "Switch"))
        self.Clear.setToolTip(_translate("Dialog", "clear all fields"))
        self.Clear.setText(_translate("Dialog", "Clear"))
        self.Update.setToolTip(_translate("Dialog", "update selected subentry\n"
"in the database"))
        self.Update.setText(_translate("Dialog", "Update"))
        self.SLanguage_2.setText(_translate("Dialog", "Context and Usage"))
        self.OkayBtn.setToolTip(_translate("Dialog", "close window and update the database"))
        self.OkayBtn.setText(_translate("Dialog", "Okay"))
        self.CancelBtn.setToolTip(_translate("Dialog", "close window without updating database"))
        self.CancelBtn.setText(_translate("Dialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())

