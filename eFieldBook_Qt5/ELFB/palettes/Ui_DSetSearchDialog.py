# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/eFieldBook_Qt5/ELFB/palettes/DSetSearchDialog.ui'
#
# Created by: PyQt6 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SearchDSets(object):
    def setupUi(self, SearchDSets):
        SearchDSets.setObjectName("SearchDSets")
        SearchDSets.resize(520, 224)
        self.buttonBox = QtWidgets.QDialogButtonBox(SearchDSets)
        self.buttonBox.setGeometry(QtCore.QRect(361, 171, 141, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(SearchDSets)
        self.groupBox.setGeometry(QtCore.QRect(352, 0, 148, 107))
        self.groupBox.setObjectName("groupBox")
        self.Source = QtWidgets.QPlainTextEdit(self.groupBox)
        self.Source.setGeometry(QtCore.QRect(8, 39, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Source.setFont(font)
        self.Source.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Source.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.Source.setObjectName("Source")
        self.Researcher = QtWidgets.QPlainTextEdit(self.groupBox)
        self.Researcher.setGeometry(QtCore.QRect(80, 39, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Researcher.setFont(font)
        self.Researcher.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Researcher.setObjectName("Researcher")
        self.Date = QtWidgets.QPlainTextEdit(self.groupBox)
        self.Date.setGeometry(QtCore.QRect(8, 78, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Date.setFont(font)
        self.Date.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Date.setObjectName("Date")
        self.Updated = QtWidgets.QPlainTextEdit(self.groupBox)
        self.Updated.setGeometry(QtCore.QRect(80, 78, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Updated.setFont(font)
        self.Updated.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Updated.setObjectName("Updated")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(8, 22, 35, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(80, 22, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(8, 61, 35, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(80, 61, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.groupBox_2 = QtWidgets.QGroupBox(SearchDSets)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 72, 150, 71))
        self.groupBox_2.setObjectName("groupBox_2")
        self.Comments = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.Comments.setGeometry(QtCore.QRect(8, 22, 134, 42))
        self.Comments.setObjectName("Comments")
        self.groupBox_3 = QtWidgets.QGroupBox(SearchDSets)
        self.groupBox_3.setGeometry(QtCore.QRect(182, 72, 150, 71))
        self.groupBox_3.setObjectName("groupBox_3")
        self.Keywords = QtWidgets.QPlainTextEdit(self.groupBox_3)
        self.Keywords.setGeometry(QtCore.QRect(8, 22, 134, 42))
        self.Keywords.setObjectName("Keywords")
        self.groupBox_4 = QtWidgets.QGroupBox(SearchDSets)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 0, 312, 71))
        self.groupBox_4.setObjectName("groupBox_4")
        self.SearchText = QtWidgets.QPlainTextEdit(self.groupBox_4)
        self.SearchText.setGeometry(QtCore.QRect(8, 23, 295, 42))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SearchText.setFont(font)
        self.SearchText.setObjectName("SearchText")
        self.gridLayoutWidget = QtWidgets.QWidget(SearchDSets)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(28, 148, 325, 61))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.accentBtn = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.accentBtn.setFont(font)
        self.accentBtn.setObjectName("accentBtn")
        self.gridLayout.addWidget(self.accentBtn, 0, 1, 1, 1)
        self.appendBtn = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.appendBtn.setFont(font)
        self.appendBtn.setObjectName("appendBtn")
        self.gridLayout.addWidget(self.appendBtn, 1, 1, 1, 1)
        self.caseBtn = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.caseBtn.setFont(font)
        self.caseBtn.setChecked(True)
        self.caseBtn.setObjectName("caseBtn")
        self.gridLayout.addWidget(self.caseBtn, 0, 0, 1, 1)
        self.diacritBtn = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.diacritBtn.setFont(font)
        self.diacritBtn.setObjectName("diacritBtn")
        self.gridLayout.addWidget(self.diacritBtn, 0, 2, 1, 1)
        self.wholeWordBtn = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.wholeWordBtn.setFont(font)
        self.wholeWordBtn.setObjectName("wholeWordBtn")
        self.gridLayout.addWidget(self.wholeWordBtn, 1, 0, 1, 1)
        self.recOnlyBtn = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.recOnlyBtn.setFont(font)
        self.recOnlyBtn.setCheckable(False)
        self.recOnlyBtn.setObjectName("recOnlyBtn")
        self.gridLayout.addWidget(self.recOnlyBtn, 1, 2, 1, 1)
        self.limitBtn = QtWidgets.QCheckBox(SearchDSets)
        self.limitBtn.setGeometry(QtCore.QRect(367, 154, 131, 18))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.limitBtn.setFont(font)
        self.limitBtn.setChecked(True)
        self.limitBtn.setObjectName("limitBtn")
        self.clearBtn = QtWidgets.QPushButton(SearchDSets)
        self.clearBtn.setGeometry(QtCore.QRect(393, 119, 60, 19))
        self.clearBtn.setStyleSheet("QPushButton {\n"
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
                                    "}")
        self.clearBtn.setObjectName("clearBtn")

        self.retranslateUi(SearchDSets)
        self.buttonBox.accepted.connect(SearchDSets.accept)
        self.buttonBox.rejected.connect(SearchDSets.reject)
        QtCore.QMetaObject.connectSlotsByName(SearchDSets)
        SearchDSets.setTabOrder(self.SearchText, self.Source)
        SearchDSets.setTabOrder(self.Source, self.Researcher)
        SearchDSets.setTabOrder(self.Researcher, self.Date)
        SearchDSets.setTabOrder(self.Date, self.Updated)
        SearchDSets.setTabOrder(self.Updated, self.Comments)
        SearchDSets.setTabOrder(self.Comments, self.Keywords)
        SearchDSets.setTabOrder(self.Keywords, self.caseBtn)
        SearchDSets.setTabOrder(self.caseBtn, self.accentBtn)
        SearchDSets.setTabOrder(self.accentBtn, self.appendBtn)
        SearchDSets.setTabOrder(self.appendBtn, self.buttonBox)

    def retranslateUi(self, SearchDSets):
        _translate = QtCore.QCoreApplication.translate
        SearchDSets.setWindowTitle(_translate("SearchDSets", "Dialog"))
        SearchDSets.setToolTip(_translate("SearchDSets", "Enter text to find in the fields where you wish to search. \n"
                                                         "Entering terms in more than one field will search for entries \n"
                                                         "that meet all search criteria. Enter \"&\" between AND search \n"
                                                         "terms in the same field, place \"¬\" before terms for NOT searches. \n"
                                                         "For edge-sensitive searches, place \"#\" on the edge you wish the \n"
                                                         "search to key on (e.g., \"#an\" will find all words beginning with \n"
                                                         "the string \"an\"). Combine AND/NOT and \"#\" in the order \"¬#\". \n"
                                                         "Use the checkboxes on the left to parameterize searches."))
        self.groupBox.setTitle(_translate("SearchDSets", "Metadata"))
        self.label.setText(_translate("SearchDSets", "Source"))
        self.label_2.setText(_translate("SearchDSets", "Researcher"))
        self.label_3.setText(_translate("SearchDSets", "Date"))
        self.label_4.setText(_translate("SearchDSets", "Updated"))
        self.groupBox_2.setTitle(_translate("SearchDSets", "Comments"))
        self.groupBox_3.setTitle(_translate("SearchDSets", "Keywords"))
        self.groupBox_4.setTitle(_translate("SearchDSets", "Search text"))
        self.accentBtn.setToolTip(_translate("SearchDSets", "Perform searches that ignore lexical accent.\n"
                                                            "Search term must contain no accented characters."))
        self.accentBtn.setText(_translate("SearchDSets", "Ignore accents"))
        self.appendBtn.setToolTip(_translate("SearchDSets", "Search results will not overwrite the results\n"
                                                            "of previous searches on \"Search\" card."))
        self.appendBtn.setText(_translate("SearchDSets", "Append results"))
        self.caseBtn.setToolTip(_translate("SearchDSets", "Perform case-insensitive searches"))
        self.caseBtn.setText(_translate("SearchDSets", "Ignore case"))
        self.diacritBtn.setToolTip(_translate("SearchDSets", "Perform searches that ignore diacritics. \n"
                                                             "Search term must contain no diacritics."))
        self.diacritBtn.setText(_translate("SearchDSets", "Ignore diacrits"))
        self.wholeWordBtn.setText(_translate("SearchDSets", "Whole word"))
        self.recOnlyBtn.setText(_translate("SearchDSets", "Recorded only"))
        self.limitBtn.setToolTip(_translate("SearchDSets", "limit search to current card. Lines\n"
                                                           "containing results will be highlighted.\n"
                                                           "Does not support AND or NOT searches."))
        self.limitBtn.setText(_translate("SearchDSets", "find on this page only"))
        self.clearBtn.setText(_translate("SearchDSets", "Clear"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    SearchDSets = QtWidgets.QDialog()
    ui = Ui_SearchDSets()
    ui.setupUi(SearchDSets)
    SearchDSets.show()
    sys.exit(app.exec())
