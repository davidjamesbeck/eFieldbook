# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/AnalysisManager.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1124, 590)
        Dialog.setToolTip("")
        Dialog.setStyleSheet("QPushButton {\n"
"    max-height: 19px;\n"
"    min-height: 19px;\n"
"    max-width: 60px;\n"
"    min-width: 60px;\n"
"    background: #6698FF;\n"
"    color: white;    \n"
"    border: 0px solid black;\n"
"    border-radius: 4px;\n"
"        padding: 0 0 0 0;\n"
"        margin: 0 0 0 0;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: #1E90FF;\n"
"    border: 2px outset #E6E6FA;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background: #E6E6FA;\n"
"    border: 0px outset #E6E6FA;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    background: transparent;\n"
"}\n"
"\n"
"QCheckBox {\n"
"    background: transparent;\n"
"}\n"
"\n"
"QToolButton {\n"
"    background: #6698FF;\n"
"    color: white;\n"
"    border: 1px solid #6698FF;\n"
"    max-width: 18px;\n"
"    max-height: 18px;\n"
"    min-height: 18px;\n"
"    min-width: 18px;\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    border: 2px outset #1E90FF;\n"
"}")
        Dialog.setSizeGripEnabled(True)
        self.tTitle = QtWidgets.QTextEdit(Dialog)
        self.tTitle.setGeometry(QtCore.QRect(8, 16, 893, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.tTitle.setFont(font)
        self.tTitle.setObjectName("tTitle")
        self.tPortalBox = QtWidgets.QGroupBox(Dialog)
        self.tPortalBox.setGeometry(QtCore.QRect(8, 66, 893, 514))
        self.tPortalBox.setTitle("")
        self.tPortalBox.setObjectName("tPortalBox")
        self.portal = QtWidgets.QTextEdit(self.tPortalBox)
        self.portal.setGeometry(QtCore.QRect(40, 8, 843, 457))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        self.portal.setFont(font)
        self.portal.setToolTip("")
        self.portal.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.portal.setObjectName("portal")
        self.controlBox = QtWidgets.QGroupBox(self.tPortalBox)
        self.controlBox.setGeometry(QtCore.QRect(0, 464, 893, 48))
        self.controlBox.setTitle("")
        self.controlBox.setObjectName("controlBox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.controlBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 1, 873, 49))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.findTerm = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.findTerm.setMinimumSize(QtCore.QSize(120, 25))
        self.findTerm.setMaximumSize(QtCore.QSize(120, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.findTerm.setFont(font)
        self.findTerm.setObjectName("findTerm")
        self.horizontalLayout_3.addWidget(self.findTerm)
        self.findPrevBtn = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.findPrevBtn.setArrowType(QtCore.Qt.NoArrow)
        self.findPrevBtn.setObjectName("findPrevBtn")
        self.horizontalLayout_3.addWidget(self.findPrevBtn)
        self.findNextBtn = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.findNextBtn.setArrowType(QtCore.Qt.NoArrow)
        self.findNextBtn.setObjectName("findNextBtn")
        self.horizontalLayout_3.addWidget(self.findNextBtn)
        self.findAllBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.findAllBtn.setObjectName("findAllBtn")
        self.horizontalLayout_3.addWidget(self.findAllBtn)
        self.wholeWordBtn = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.wholeWordBtn.setMinimumSize(QtCore.QSize(85, 20))
        self.wholeWordBtn.setMaximumSize(QtCore.QSize(85, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.wholeWordBtn.setFont(font)
        self.wholeWordBtn.setObjectName("wholeWordBtn")
        self.horizontalLayout_3.addWidget(self.wholeWordBtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.activateReplace = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.activateReplace.setText("")
        self.activateReplace.setObjectName("activateReplace")
        self.horizontalLayout_3.addWidget(self.activateReplace)
        self.rpcLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.rpcLabel.setMinimumSize(QtCore.QSize(75, 16))
        self.rpcLabel.setMaximumSize(QtCore.QSize(75, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rpcLabel.setFont(font)
        self.rpcLabel.setObjectName("rpcLabel")
        self.horizontalLayout_3.addWidget(self.rpcLabel)
        self.replaceTerm = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.replaceTerm.setMinimumSize(QtCore.QSize(120, 25))
        self.replaceTerm.setMaximumSize(QtCore.QSize(120, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.replaceTerm.setFont(font)
        self.replaceTerm.setObjectName("replaceTerm")
        self.horizontalLayout_3.addWidget(self.replaceTerm)
        self.replaceBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.replaceBtn.setObjectName("replaceBtn")
        self.horizontalLayout_3.addWidget(self.replaceBtn)
        self.findReplaceBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.findReplaceBtn.setObjectName("findReplaceBtn")
        self.horizontalLayout_3.addWidget(self.findReplaceBtn)
        self.replaceAllBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.replaceAllBtn.setObjectName("replaceAllBtn")
        self.horizontalLayout_3.addWidget(self.replaceAllBtn)
        self.portal.raise_()
        self.controlBox.raise_()
        self.tNewMetadataBox = QtWidgets.QGroupBox(Dialog)
        self.tNewMetadataBox.setGeometry(QtCore.QRect(913, -1, 148, 138))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tNewMetadataBox.sizePolicy().hasHeightForWidth())
        self.tNewMetadataBox.setSizePolicy(sizePolicy)
        self.tNewMetadataBox.setStyleSheet("QPlainTextEdit {\n"
"    font-size: 9;\n"
"    border-radius: 0pts;\n"
"    max-height: 16px;\n"
"    min-width: 45px;\n"
"    min-height: 16px;\n"
"    padding: 1px;\n"
"}")
        self.tNewMetadataBox.setObjectName("tNewMetadataBox")
        self.tLabelSource_3 = QtWidgets.QLabel(self.tNewMetadataBox)
        self.tLabelSource_3.setGeometry(QtCore.QRect(8, 22, 35, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tLabelSource_3.setFont(font)
        self.tLabelSource_3.setObjectName("tLabelSource_3")
        self.tLabelDate_3 = QtWidgets.QLabel(self.tNewMetadataBox)
        self.tLabelDate_3.setGeometry(QtCore.QRect(8, 59, 21, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tLabelDate_3.setFont(font)
        self.tLabelDate_3.setObjectName("tLabelDate_3")
        self.tLabelResearcher_3 = QtWidgets.QLabel(self.tNewMetadataBox)
        self.tLabelResearcher_3.setGeometry(QtCore.QRect(80, 22, 52, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tLabelResearcher_3.setFont(font)
        self.tLabelResearcher_3.setObjectName("tLabelResearcher_3")
        self.tLabelTranscriber = QtWidgets.QLabel(self.tNewMetadataBox)
        self.tLabelTranscriber.setGeometry(QtCore.QRect(8, 96, 58, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tLabelTranscriber.setFont(font)
        self.tLabelTranscriber.setObjectName("tLabelTranscriber")
        self.tLabelUpdated_2 = QtWidgets.QLabel(self.tNewMetadataBox)
        self.tLabelUpdated_2.setGeometry(QtCore.QRect(80, 59, 37, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tLabelUpdated_2.setFont(font)
        self.tLabelUpdated_2.setObjectName("tLabelUpdated_2")
        self.tNewSource = QtWidgets.QPlainTextEdit(self.tNewMetadataBox)
        self.tNewSource.setGeometry(QtCore.QRect(8, 39, 60, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tNewSource.setFont(font)
        self.tNewSource.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tNewSource.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tNewSource.setObjectName("tNewSource")
        self.tNewResearcher = QtWidgets.QPlainTextEdit(self.tNewMetadataBox)
        self.tNewResearcher.setGeometry(QtCore.QRect(80, 39, 60, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tNewResearcher.setFont(font)
        self.tNewResearcher.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tNewResearcher.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tNewResearcher.setObjectName("tNewResearcher")
        self.tNewDate = QtWidgets.QPlainTextEdit(self.tNewMetadataBox)
        self.tNewDate.setGeometry(QtCore.QRect(8, 76, 60, 18))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tNewDate.setFont(font)
        self.tNewDate.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tNewDate.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tNewDate.setObjectName("tNewDate")
        self.tNewTranscriber = QtWidgets.QPlainTextEdit(self.tNewMetadataBox)
        self.tNewTranscriber.setGeometry(QtCore.QRect(8, 113, 132, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tNewTranscriber.setFont(font)
        self.tNewTranscriber.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tNewTranscriber.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tNewTranscriber.setObjectName("tNewTranscriber")
        self.tNewUpdated = QtWidgets.QPlainTextEdit(self.tNewMetadataBox)
        self.tNewUpdated.setGeometry(QtCore.QRect(80, 76, 60, 18))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tNewUpdated.setFont(font)
        self.tNewUpdated.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tNewUpdated.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tNewUpdated.setReadOnly(True)
        self.tNewUpdated.setObjectName("tNewUpdated")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(974, 536, 139, 38))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.verticalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancelNewTextBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cancelNewTextBtn.setObjectName("cancelNewTextBtn")
        self.horizontalLayout.addWidget(self.cancelNewTextBtn)
        self.okayNewTextBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.okayNewTextBtn.setObjectName("okayNewTextBtn")
        self.horizontalLayout.addWidget(self.okayNewTextBtn)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(915, 174, 199, 350))
        self.groupBox.setMinimumSize(QtCore.QSize(199, 350))
        self.groupBox.setMaximumSize(QtCore.QSize(199, 350))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tLoadNewTextBtn = QtWidgets.QPushButton(self.groupBox)
        self.tLoadNewTextBtn.setObjectName("tLoadNewTextBtn")
        self.gridLayout_3.addWidget(self.tLoadNewTextBtn, 0, 0, 1, 1)
        self.tSetLangBtn = QtWidgets.QCheckBox(self.groupBox)
        self.tSetLangBtn.setMinimumSize(QtCore.QSize(60, 0))
        self.tSetLangBtn.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(True)
        self.tSetLangBtn.setFont(font)
        self.tSetLangBtn.setObjectName("tSetLangBtn")
        self.gridLayout_3.addWidget(self.tSetLangBtn, 1, 1, 1, 1)
        self.tClearNewTextBtn = QtWidgets.QPushButton(self.groupBox)
        self.tClearNewTextBtn.setObjectName("tClearNewTextBtn")
        self.gridLayout_3.addWidget(self.tClearNewTextBtn, 1, 0, 1, 1)
        self.saveDraftBtn = QtWidgets.QPushButton(self.groupBox)
        self.saveDraftBtn.setObjectName("saveDraftBtn")
        self.gridLayout_3.addWidget(self.saveDraftBtn, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tFormatNewTextBtn = QtWidgets.QPushButton(self.groupBox)
        self.tFormatNewTextBtn.setDefault(False)
        self.tFormatNewTextBtn.setObjectName("tFormatNewTextBtn")
        self.gridLayout.addWidget(self.tFormatNewTextBtn, 0, 0, 1, 1)
        self.tSpliceBtn = QtWidgets.QPushButton(self.groupBox)
        self.tSpliceBtn.setObjectName("tSpliceBtn")
        self.gridLayout.addWidget(self.tSpliceBtn, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.frame_3 = QtWidgets.QFrame(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(169, 135))
        self.frame_3.setMaximumSize(QtCore.QSize(169, 135))
        font = QtGui.QFont()
        font.setPointSize(2)
        self.frame_3.setFont(font)
        self.frame_3.setStyleSheet("")
        self.frame_3.setObjectName("frame_3")
        self.tLinesValidBtn = QtWidgets.QCheckBox(self.frame_3)
        self.tLinesValidBtn.setGeometry(QtCore.QRect(12, 0, 74, 20))
        self.tLinesValidBtn.setMinimumSize(QtCore.QSize(0, 20))
        self.tLinesValidBtn.setMaximumSize(QtCore.QSize(16777215, 20))
        self.tLinesValidBtn.setAutoFillBackground(False)
        self.tLinesValidBtn.setObjectName("tLinesValidBtn")
        self.lineErrorPrev = QtWidgets.QToolButton(self.frame_3)
        self.lineErrorPrev.setGeometry(QtCore.QRect(108, 0, 20, 20))
        self.lineErrorPrev.setMaximumSize(QtCore.QSize(20, 20))
        self.lineErrorPrev.setAutoRepeatDelay(298)
        self.lineErrorPrev.setAutoRaise(True)
        self.lineErrorPrev.setObjectName("lineErrorPrev")
        self.lineErrorNext = QtWidgets.QToolButton(self.frame_3)
        self.lineErrorNext.setGeometry(QtCore.QRect(139, 0, 20, 20))
        self.lineErrorNext.setMaximumSize(QtCore.QSize(20, 20))
        self.lineErrorNext.setAutoRaise(True)
        self.lineErrorNext.setObjectName("lineErrorNext")
        self.lineErrorNumber = QtWidgets.QLabel(self.frame_3)
        self.lineErrorNumber.setGeometry(QtCore.QRect(12, 24, 49, 10))
        self.lineErrorNumber.setMinimumSize(QtCore.QSize(0, 10))
        self.lineErrorNumber.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineErrorNumber.setFont(font)
        self.lineErrorNumber.setStyleSheet("margin-left: 6px;")
        self.lineErrorNumber.setObjectName("lineErrorNumber")
        self.tWordsValidBtn = QtWidgets.QCheckBox(self.frame_3)
        self.tWordsValidBtn.setGeometry(QtCore.QRect(12, 42, 74, 20))
        self.tWordsValidBtn.setMinimumSize(QtCore.QSize(0, 20))
        self.tWordsValidBtn.setMaximumSize(QtCore.QSize(16777215, 20))
        self.tWordsValidBtn.setAutoFillBackground(False)
        self.tWordsValidBtn.setObjectName("tWordsValidBtn")
        self.wordErrorPrev = QtWidgets.QToolButton(self.frame_3)
        self.wordErrorPrev.setGeometry(QtCore.QRect(108, 42, 20, 20))
        self.wordErrorPrev.setMaximumSize(QtCore.QSize(20, 20))
        self.wordErrorPrev.setAutoRepeatDelay(298)
        self.wordErrorPrev.setAutoRaise(True)
        self.wordErrorPrev.setObjectName("wordErrorPrev")
        self.wordErrorNext = QtWidgets.QToolButton(self.frame_3)
        self.wordErrorNext.setGeometry(QtCore.QRect(139, 42, 20, 20))
        self.wordErrorNext.setMaximumSize(QtCore.QSize(20, 20))
        self.wordErrorNext.setAutoRaise(True)
        self.wordErrorNext.setObjectName("wordErrorNext")
        self.wordErrorNumber = QtWidgets.QLabel(self.frame_3)
        self.wordErrorNumber.setGeometry(QtCore.QRect(12, 66, 49, 10))
        self.wordErrorNumber.setMinimumSize(QtCore.QSize(0, 10))
        self.wordErrorNumber.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.wordErrorNumber.setFont(font)
        self.wordErrorNumber.setStyleSheet("margin-left: 6px;")
        self.wordErrorNumber.setObjectName("wordErrorNumber")
        self.tMorphsValidBtn = QtWidgets.QCheckBox(self.frame_3)
        self.tMorphsValidBtn.setGeometry(QtCore.QRect(12, 84, 70, 20))
        self.tMorphsValidBtn.setMinimumSize(QtCore.QSize(70, 20))
        self.tMorphsValidBtn.setMaximumSize(QtCore.QSize(70, 20))
        self.tMorphsValidBtn.setObjectName("tMorphsValidBtn")
        self.morphErrorPrev = QtWidgets.QToolButton(self.frame_3)
        self.morphErrorPrev.setGeometry(QtCore.QRect(108, 84, 20, 20))
        self.morphErrorPrev.setMaximumSize(QtCore.QSize(20, 20))
        self.morphErrorPrev.setAutoRepeatDelay(298)
        self.morphErrorPrev.setAutoRaise(True)
        self.morphErrorPrev.setObjectName("morphErrorPrev")
        self.morphErrorNext = QtWidgets.QToolButton(self.frame_3)
        self.morphErrorNext.setGeometry(QtCore.QRect(139, 84, 20, 20))
        self.morphErrorNext.setMaximumSize(QtCore.QSize(20, 20))
        self.morphErrorNext.setAutoRaise(True)
        self.morphErrorNext.setObjectName("morphErrorNext")
        self.morphErrorNumber = QtWidgets.QLabel(self.frame_3)
        self.morphErrorNumber.setGeometry(QtCore.QRect(12, 108, 49, 10))
        self.morphErrorNumber.setMinimumSize(QtCore.QSize(0, 10))
        self.morphErrorNumber.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.morphErrorNumber.setFont(font)
        self.morphErrorNumber.setStyleSheet("margin-left: 6 px;")
        self.morphErrorNumber.setObjectName("morphErrorNumber")
        self.verticalLayout.addWidget(self.frame_3)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tNewAutoparseBtn = QtWidgets.QCheckBox(self.groupBox)
        self.tNewAutoparseBtn.setMinimumSize(QtCore.QSize(60, 0))
        self.tNewAutoparseBtn.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(True)
        self.tNewAutoparseBtn.setFont(font)
        self.tNewAutoparseBtn.setObjectName("tNewAutoparseBtn")
        self.gridLayout_4.addWidget(self.tNewAutoparseBtn, 0, 1, 1, 1)
        self.parserBtn = QtWidgets.QPushButton(self.groupBox)
        self.parserBtn.setObjectName("parserBtn")
        self.gridLayout_4.addWidget(self.parserBtn, 0, 0, 1, 1)
        self.alignTextBtn = QtWidgets.QPushButton(self.groupBox)
        self.alignTextBtn.setObjectName("alignTextBtn")
        self.gridLayout_4.addWidget(self.alignTextBtn, 1, 0, 1, 1)
        self.removeHiliteBtn = QtWidgets.QPushButton(self.groupBox)
        self.removeHiliteBtn.setObjectName("removeHiliteBtn")
        self.gridLayout_4.addWidget(self.removeHiliteBtn, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(918, 152, 69, 16))
        self.label.setObjectName("label")
        self.importSelector = QtWidgets.QComboBox(Dialog)
        self.importSelector.setGeometry(QtCore.QRect(994, 139, 114, 45))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.importSelector.setFont(font)
        self.importSelector.setObjectName("importSelector")
        self.helpBtn = QtWidgets.QToolButton(Dialog)
        self.helpBtn.setGeometry(QtCore.QRect(919, 533, 42, 42))
        self.helpBtn.setStyleSheet("QToolButton {\n"
"    min-height: 40px;\n"
"    min-width: 40px;\n"
"    max-height: 40px;\n"
"    max-width:40px;\n"
"    background: transparent;\n"
"}")
        self.helpBtn.setText("")
        self.helpBtn.setAutoRaise(False)
        self.helpBtn.setObjectName("helpBtn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Find text:"))
        self.findTerm.setToolTip(_translate("Dialog", "enter term to search.\n"
"\"Enter\" begins search."))
        self.findPrevBtn.setToolTip(_translate("Dialog", "find previous token."))
        self.findPrevBtn.setText(_translate("Dialog", "◀︎"))
        self.findNextBtn.setToolTip(_translate("Dialog", "find next token."))
        self.findNextBtn.setText(_translate("Dialog", "▶︎"))
        self.findAllBtn.setToolTip(_translate("Dialog", "hihglight all instances of serach term."))
        self.findAllBtn.setText(_translate("Dialog", "Find All"))
        self.wholeWordBtn.setToolTip(_translate("Dialog", "limit search to whole words"))
        self.wholeWordBtn.setText(_translate("Dialog", "Whole word"))
        self.rpcLabel.setText(_translate("Dialog", "Replace with:"))
        self.replaceBtn.setText(_translate("Dialog", "Replace"))
        self.findReplaceBtn.setText(_translate("Dialog", "Find/Rpl"))
        self.replaceAllBtn.setText(_translate("Dialog", "Rpl All"))
        self.tNewMetadataBox.setTitle(_translate("Dialog", "New Metadata"))
        self.tLabelSource_3.setText(_translate("Dialog", "Source"))
        self.tLabelDate_3.setText(_translate("Dialog", "Date"))
        self.tLabelResearcher_3.setText(_translate("Dialog", "Researcher"))
        self.tLabelTranscriber.setText(_translate("Dialog", "Transcribers"))
        self.tLabelUpdated_2.setText(_translate("Dialog", "Updated"))
        self.tNewSource.setToolTip(_translate("Dialog", "original speaker source"))
        self.tNewResearcher.setToolTip(_translate("Dialog", "person who collected form"))
        self.tNewDate.setToolTip(_translate("Dialog", "date collected. yyyy–MM–dd \n"
"format recommended"))
        self.tNewTranscriber.setToolTip(_translate("Dialog", "consultants and researchers \n"
"who worked on transcription"))
        self.tNewUpdated.setToolTip(_translate("Dialog", "date last updated"))
        self.cancelNewTextBtn.setToolTip(_translate("Dialog", "Cancel."))
        self.cancelNewTextBtn.setText(_translate("Dialog", "Cancel"))
        self.okayNewTextBtn.setToolTip(_translate("Dialog", "Add new text to database."))
        self.okayNewTextBtn.setText(_translate("Dialog", "Okay"))
        self.groupBox.setTitle(_translate("Dialog", "Controls"))
        self.tLoadNewTextBtn.setToolTip(_translate("Dialog", "Load prepared text from file."))
        self.tLoadNewTextBtn.setText(_translate("Dialog", "Open"))
        self.tSetLangBtn.setToolTip(_translate("Dialog", "Check if the text is glossed in the secondary language only"))
        self.tSetLangBtn.setText(_translate("Dialog", "L2 Gloss"))
        self.tClearNewTextBtn.setToolTip(_translate("Dialog", "Clear text."))
        self.tClearNewTextBtn.setText(_translate("Dialog", "Clear"))
        self.saveDraftBtn.setText(_translate("Dialog", "Save"))
        self.tFormatNewTextBtn.setToolTip(_translate("Dialog", "Check the format of the text. Strongly \n"
"recommended before clicking \"Okay\"."))
        self.tFormatNewTextBtn.setText(_translate("Dialog", "Validate"))
        self.tSpliceBtn.setToolTip(_translate("Dialog", "Splices lines that have been broken into\n"
"multiple blocks to fit to a set page width.\n"
"Select a line (including text and gloss) to\n"
"splice one line at a time, or click button with\n"
"no selection to process the entire text."))
        self.tSpliceBtn.setText(_translate("Dialog", "Splice"))
        self.tLinesValidBtn.setToolTip(_translate("Dialog", "Lines are grouped correctly \n"
"in blocks of 1, 2, or 4."))
        self.tLinesValidBtn.setText(_translate("Dialog", "Lines"))
        self.lineErrorPrev.setText(_translate("Dialog", "◀︎"))
        self.lineErrorNext.setText(_translate("Dialog", "▶︎"))
        self.lineErrorNumber.setText(_translate("Dialog", "TextLabel"))
        self.tWordsValidBtn.setToolTip(_translate("Dialog", "The number of words on line 2 equals\n"
"the number of words on line 3."))
        self.tWordsValidBtn.setText(_translate("Dialog", "Words"))
        self.wordErrorPrev.setText(_translate("Dialog", "◀︎"))
        self.wordErrorNext.setText(_translate("Dialog", "▶︎"))
        self.wordErrorNumber.setText(_translate("Dialog", "TextLabel"))
        self.tMorphsValidBtn.setToolTip(_translate("Dialog", "Number of morphs delimited by\n"
"\"–\" and \"=\" is the same for each\n"
"word on lines 2 and 3."))
        self.tMorphsValidBtn.setText(_translate("Dialog", "Morphs"))
        self.morphErrorPrev.setText(_translate("Dialog", "◀︎"))
        self.morphErrorNext.setText(_translate("Dialog", "▶︎"))
        self.morphErrorNumber.setText(_translate("Dialog", "TextLabel"))
        self.tNewAutoparseBtn.setToolTip(_translate("Dialog", "autoparse entire text when you click \"Okay\".\n"
"This will add parsed example cards for every \n"
"line of the text based on the parses in the Index."))
        self.tNewAutoparseBtn.setText(_translate("Dialog", "Autoparse"))
        self.parserBtn.setToolTip(_translate("Dialog", "run the parser into the text field without committing\n"
"the analysis to the database. This allows for the \n"
"correction of common errors in transcription and\n"
"makes it easier to fix such errors globally."))
        self.parserBtn.setText(_translate("Dialog", "Parser"))
        self.alignTextBtn.setToolTip(_translate("Dialog", "align units in the interlinear glosses of 4-line\n"
"format examples. Uses spaces, so be careful\n"
"when saving and using cut-and-paste of the\n"
"plain text in the window. Spaces are eliminated\n"
"when the text is committed to the database."))
        self.alignTextBtn.setText(_translate("Dialog", "Align"))
        self.removeHiliteBtn.setText(_translate("Dialog", "Deselect"))
        self.label.setText(_translate("Dialog", "Import file:"))
        self.importSelector.setToolTip(_translate("Dialog", "select type of file to import"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

