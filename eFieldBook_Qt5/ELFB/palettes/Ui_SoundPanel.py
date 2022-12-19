# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/SoundPanel.ui'
#
# Created by: PyQt6 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SoundPanel(object):
    def setupUi(self, SoundPanel):
        SoundPanel.setObjectName("SoundPanel")
        SoundPanel.resize(146, 77)
        self.SoundBox = QtWidgets.QGroupBox(SoundPanel)
        self.SoundBox.setGeometry(QtCore.QRect(0, 0, 146, 77))
        self.SoundBox.setStyleSheet("QToolButton {\n"
                                    "    background: auto;\n"
                                    "}\n"
                                    "QToolButton:pressed {\n"
                                    "    border: 2px outset transparent;\n"
                                    "}")
        self.SoundBox.setObjectName("SoundBox")
        self.Recordings = QtWidgets.QComboBox(self.SoundBox)
        self.Recordings.setGeometry(QtCore.QRect(5, 21, 101, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Recordings.setFont(font)
        self.Recordings.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAtTop)
        self.Recordings.setObjectName("Recordings")
        self.PlaySoundBtn = QtWidgets.QToolButton(self.SoundBox)
        self.PlaySoundBtn.setGeometry(QtCore.QRect(112, 24, 27, 23))
        self.PlaySoundBtn.setStyleSheet("")
        self.PlaySoundBtn.setText("")
        self.PlaySoundBtn.setObjectName("PlaySoundBtn")
        self.SoundFileMeta = QtWidgets.QLabel(self.SoundBox)
        self.SoundFileMeta.setGeometry(QtCore.QRect(8, 52, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.SoundFileMeta.setFont(font)
        self.SoundFileMeta.setStyleSheet("")
        self.SoundFileMeta.setObjectName("SoundFileMeta")
        self.SoundMetaBtn = QtWidgets.QToolButton(self.SoundBox)
        self.SoundMetaBtn.setGeometry(QtCore.QRect(86, 51, 19, 19))
        self.SoundMetaBtn.setObjectName("SoundMetaBtn")
        self.AddMediaBtn = QtWidgets.QToolButton(self.SoundBox)
        self.AddMediaBtn.setGeometry(QtCore.QRect(108, 53, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.AddMediaBtn.setFont(font)
        self.AddMediaBtn.setAutoFillBackground(False)
        self.AddMediaBtn.setStyleSheet("QToolButton {\n"
                                       "    background: #6698FF;\n"
                                       "    color: white;\n"
                                       "    border: 1px solid #6698FF;\n"
                                       "}\n"
                                       "\n"
                                       "QToolButton:pressed {\n"
                                       "    border: 2px outset #1E90FF;\n"
                                       "}")
        self.AddMediaBtn.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.AddMediaBtn.setAutoRaise(True)
        self.AddMediaBtn.setObjectName("AddMediaBtn")
        self.DelMediaBtn = QtWidgets.QToolButton(self.SoundBox)
        self.DelMediaBtn.setGeometry(QtCore.QRect(125, 53, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.DelMediaBtn.setFont(font)
        self.DelMediaBtn.setStyleSheet("QToolButton {\n"
                                       "    background: #6698FF;\n"
                                       "    color: white;\n"
                                       "    border: 1px solid #6698FF;\n"
                                       "}\n"
                                       "\n"
                                       "QToolButton:pressed {\n"
                                       "    border: 2px outset #1E90FF;\n"
                                       "}")
        self.DelMediaBtn.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.DelMediaBtn.setAutoRaise(True)
        self.DelMediaBtn.setObjectName("DelMediaBtn")

        self.retranslateUi(SoundPanel)
        QtCore.QMetaObject.connectSlotsByName(SoundPanel)

    def retranslateUi(self, SoundPanel):
        _translate = QtCore.QCoreApplication.translate
        SoundPanel.setWindowTitle(_translate("SoundPanel", "Form"))
        self.SoundBox.setTitle(_translate("SoundPanel", "Sound"))
        self.Recordings.setToolTip(_translate("SoundPanel", "select and play recording. \n"
                                                            "Filename is placed on clipboard\n"
                                                            "to paste into a text document."))
        self.PlaySoundBtn.setToolTip(_translate("SoundPanel", "play recording. Filename\n"
                                                              "is placed on clipboard to\n"
                                                              "paste into a text document."))
        self.SoundFileMeta.setToolTip(_translate("SoundPanel", "speaker info for recording"))
        self.SoundMetaBtn.setToolTip(_translate("SoundPanel", "metadata"))
        self.AddMediaBtn.setToolTip(_translate("SoundPanel", "add media file"))
        self.AddMediaBtn.setText(_translate("SoundPanel", "+"))
        self.DelMediaBtn.setToolTip(_translate("SoundPanel", "delete media file"))
        self.DelMediaBtn.setText(_translate("SoundPanel", "–"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    SoundPanel = QtWidgets.QWidget()
    ui = Ui_SoundPanel()
    ui.setupUi(SoundPanel)
    SoundPanel.show()
    sys.exit(app.exec())
