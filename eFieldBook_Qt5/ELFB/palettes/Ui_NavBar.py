# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/NavBar.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NavBar(object):
    def setupUi(self, NavBar):
        NavBar.setObjectName("NavBar")
        NavBar.resize(258, 56)
        self.ControlBar = QtWidgets.QFrame(NavBar)
        self.ControlBar.setGeometry(QtCore.QRect(0, 0, 258, 56))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ControlBar.sizePolicy().hasHeightForWidth())
        self.ControlBar.setSizePolicy(sizePolicy)
        self.ControlBar.setStyleSheet("QFrame {\n"
"     border: 1px solid gray;\n"
"}\n"
"\n"
"QToolButton {\n"
"     background: transparent;\n"
"     min-width: 32px;\n"
"     min-height: 32px;\n"
"     max-width: 32px;\n"
"     max-height: 32px;\n"
"}\n"
"")
        self.ControlBar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ControlBar.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.ControlBar.setObjectName("ControlBar")
        self.BeginBtn = QtWidgets.QToolButton(self.ControlBar)
        self.BeginBtn.setGeometry(QtCore.QRect(13, 13, 34, 34))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BeginBtn.sizePolicy().hasHeightForWidth())
        self.BeginBtn.setSizePolicy(sizePolicy)
        self.BeginBtn.setMinimumSize(QtCore.QSize(12, 12))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.BeginBtn.setFont(font)
        self.BeginBtn.setAutoFillBackground(False)
        self.BeginBtn.setText("")
        self.BeginBtn.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.BeginBtn.setObjectName("BeginBtn")
        self.PrevBtn = QtWidgets.QToolButton(self.ControlBar)
        self.PrevBtn.setGeometry(QtCore.QRect(53, 13, 34, 34))
        self.PrevBtn.setMinimumSize(QtCore.QSize(12, 12))
        self.PrevBtn.setText("")
        self.PrevBtn.setObjectName("PrevBtn")
        self.RtnBtn = QtWidgets.QToolButton(self.ControlBar)
        self.RtnBtn.setGeometry(QtCore.QRect(93, 13, 34, 34))
        self.RtnBtn.setMinimumSize(QtCore.QSize(12, 12))
        self.RtnBtn.setStyleSheet("")
        self.RtnBtn.setText("")
        self.RtnBtn.setAutoRaise(True)
        self.RtnBtn.setObjectName("RtnBtn")
        self.NextBtn = QtWidgets.QToolButton(self.ControlBar)
        self.NextBtn.setGeometry(QtCore.QRect(175, 13, 34, 34))
        self.NextBtn.setMinimumSize(QtCore.QSize(12, 12))
        self.NextBtn.setText("")
        self.NextBtn.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.NextBtn.setArrowType(QtCore.Qt.NoArrow)
        self.NextBtn.setObjectName("NextBtn")
        self.EndBtn = QtWidgets.QToolButton(self.ControlBar)
        self.EndBtn.setGeometry(QtCore.QRect(213, 13, 34, 34))
        self.EndBtn.setMinimumSize(QtCore.QSize(12, 12))
        self.EndBtn.setText("")
        self.EndBtn.setObjectName("EndBtn")
        self.FwdBtn = QtWidgets.QToolButton(self.ControlBar)
        self.FwdBtn.setGeometry(QtCore.QRect(133, 13, 34, 34))
        self.FwdBtn.setMinimumSize(QtCore.QSize(12, 12))
        self.FwdBtn.setMaximumSize(QtCore.QSize(34, 34))
        self.FwdBtn.setText("")
        self.FwdBtn.setObjectName("FwdBtn")

        self.retranslateUi(NavBar)
        QtCore.QMetaObject.connectSlotsByName(NavBar)

    def retranslateUi(self, NavBar):
        _translate = QtCore.QCoreApplication.translate
        NavBar.setWindowTitle(_translate("NavBar", "Form"))
        self.BeginBtn.setToolTip(_translate("NavBar", "go to first card of lexicon"))
        self.PrevBtn.setToolTip(_translate("NavBar", "go to previous card of lexicon"))
        self.RtnBtn.setToolTip(_translate("NavBar", "go back"))
        self.NextBtn.setToolTip(_translate("NavBar", "go to next card of lexicon"))
        self.EndBtn.setToolTip(_translate("NavBar", "go to last cd of lexicon"))
        self.FwdBtn.setToolTip(_translate("NavBar", "go forward"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NavBar = QtWidgets.QWidget()
    ui = Ui_NavBar()
    ui.setupUi(NavBar)
    NavBar.show()
    sys.exit(app.exec_())
