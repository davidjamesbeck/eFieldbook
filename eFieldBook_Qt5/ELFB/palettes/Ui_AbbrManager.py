# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/AbbrManager.ui'
#
# Created by: PyQt6 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AbbrManager(object):
    def setupUi(self, AbbrManager):
        AbbrManager.setObjectName("AbbrManager")
        AbbrManager.resize(350, 179)
        self.buttonBox = QtWidgets.QDialogButtonBox(AbbrManager)
        self.buttonBox.setGeometry(QtCore.QRect(140, 141, 202, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(AbbrManager)
        self.groupBox.setGeometry(QtCore.QRect(10, 9, 330, 125))
        self.groupBox.setStyleSheet("font-size: 10pts;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.formLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(8, 13, 312, 99))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.abbreviation = QtWidgets.QTextEdit(self.formLayoutWidget)
        self.abbreviation.setMinimumSize(QtCore.QSize(200, 25))
        self.abbreviation.setMaximumSize(QtCore.QSize(200, 25))
        self.abbreviation.setObjectName("abbreviation")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.abbreviation)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.gloss = QtWidgets.QTextEdit(self.formLayoutWidget)
        self.gloss.setMinimumSize(QtCore.QSize(200, 25))
        self.gloss.setMaximumSize(QtCore.QSize(200, 25))
        self.gloss.setObjectName("gloss")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.gloss)
        self.form = QtWidgets.QTextEdit(self.formLayoutWidget)
        self.form.setMinimumSize(QtCore.QSize(200, 25))
        self.form.setMaximumSize(QtCore.QSize(200, 25))
        self.form.setObjectName("form")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.form)
        self.updateCheckbox = QtWidgets.QCheckBox(AbbrManager)
        self.updateCheckbox.setGeometry(QtCore.QRect(56, 146, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.updateCheckbox.setFont(font)
        self.updateCheckbox.setObjectName("updateCheckbox")

        self.retranslateUi(AbbrManager)
        self.buttonBox.accepted.connect(AbbrManager.accept)
        self.buttonBox.rejected.connect(AbbrManager.reject)
        QtCore.QMetaObject.connectSlotsByName(AbbrManager)

    def retranslateUi(self, AbbrManager):
        _translate = QtCore.QCoreApplication.translate
        AbbrManager.setWindowTitle(_translate("AbbrManager", "Edit abbreviations"))
        self.label.setText(_translate("AbbrManager", "Abbreviation"))
        self.abbreviation.setToolTip(_translate("AbbrManager", "abbreviation used in glosses"))
        self.label_2.setText(_translate("AbbrManager", "Gloss"))
        self.label_3.setText(_translate("AbbrManager", "Full form"))
        self.gloss.setToolTip(_translate("AbbrManager", "meaning of the abbreviation"))
        self.form.setToolTip(_translate("AbbrManager", "underlying form(s) or description (optional)"))
        self.updateCheckbox.setToolTip(_translate("AbbrManager", "select this if you change an abbreviation\n"
                                                                 "arleady in use and want to change all\n"
                                                                 "instances in the lexicon and examples."))
        self.updateCheckbox.setText(_translate("AbbrManager", "Update examples?"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    AbbrManager = QtWidgets.QDialog()
    ui = Ui_AbbrManager()
    ui.setupUi(AbbrManager)
    AbbrManager.show()
    sys.exit(app.exec())
