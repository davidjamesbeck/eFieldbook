# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/RecordBrowser.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(250, 168)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setStyleSheet("QPushButton {\n"
"     border: 0px solid black;\n"
"     border-radius: 4px;\n"
"     min-width: 50px;\n"
"     min-height: 18px;\n"
"     max-width: 76px;\n"
"     max-height: 24px;\n"
"     background: #6698FF;\n"
"     color: white;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"     border: 2px solid black;\n"
"     border-radius: 8px;\n"
"}\n"
"\n"
"")
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.PrevBtn = QtWidgets.QToolButton(Dialog)
        self.PrevBtn.setGeometry(QtCore.QRect(15, 15, 40, 40))
        self.PrevBtn.setAutoFillBackground(False)
        self.PrevBtn.setText("")
        self.PrevBtn.setObjectName("PrevBtn")
        self.NextBtn = QtWidgets.QToolButton(Dialog)
        self.NextBtn.setGeometry(QtCore.QRect(85, 15, 40, 40))
        self.NextBtn.setAutoFillBackground(False)
        self.NextBtn.setText("")
        self.NextBtn.setObjectName("NextBtn")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(15, 56, 218, 40))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(15, 90, 226, 67))
        self.groupBox.setStyleSheet("QToolButton {\n"
"    background: transparent;\n"
"     min-width: 32px;\n"
"     min-height: 32px;\n"
"     max-width: 32px;\n"
"     max-height: 32px;\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    border: 3px red;\n"
"}")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Select = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.Select.setFont(font)
        self.Select.setObjectName("Select")
        self.horizontalLayout.addWidget(self.Select)
        self.NewList = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.NewList.setFont(font)
        self.NewList.setStyleSheet("")
        self.NewList.setObjectName("NewList")
        self.horizontalLayout.addWidget(self.NewList)
        self.Save = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.Save.setFont(font)
        self.Save.setStyleSheet("")
        self.Save.setObjectName("Save")
        self.horizontalLayout.addWidget(self.Save)
        self.Discard = QtWidgets.QPushButton(Dialog)
        self.Discard.setGeometry(QtCore.QRect(155, 22, 76, 24))
        self.Discard.setStyleSheet("")
        self.Discard.setObjectName("Discard")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Browse results"))
        Dialog.setToolTip(_translate("Dialog", "<html><head/><body><p>This palette allows you to step back and forth through search results. Use the <span style=\" font-weight:600;\">Scratchpad</span> to make lists of examples of special interest. The <span style=\" font-weight:600;\">Discard</span> button will remove resuts from the Results field on the Search tab.</p></body></html>"))
        self.PrevBtn.setToolTip(_translate("Dialog", "Go backwards."))
        self.NextBtn.setToolTip(_translate("Dialog", "Go forwards."))
        self.groupBox.setToolTip(_translate("Dialog", "Builds a list of earmarked examples from the search results\n"
"that are especially interesting or that you want to set aside for\n"
"some purpose or another. Scratchpads can be saved to a file\n"
"or converted into a Dataset."))
        self.groupBox.setTitle(_translate("Dialog", "Scratchpad"))
        self.Select.setToolTip(_translate("Dialog", "Add this example to scratchpad."))
        self.Select.setText(_translate("Dialog", "Add to pad"))
        self.NewList.setToolTip(_translate("Dialog", "Save current earmarked examples and start a new scratchpad."))
        self.NewList.setText(_translate("Dialog", "New pad"))
        self.Save.setToolTip(_translate("Dialog", "Save earmarked examples."))
        self.Save.setText(_translate("Dialog", "Save"))
        self.Discard.setToolTip(_translate("Dialog", "Remove this example from search results."))
        self.Discard.setText(_translate("Dialog", "Discard"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

