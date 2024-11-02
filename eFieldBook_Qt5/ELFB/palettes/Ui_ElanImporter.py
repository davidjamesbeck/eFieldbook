# Form implementation generated from reading ui file 'ELFB/palettes/ElanImporter.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ElanImporter(object):
    def setupUi(self, ElanImporter):
        ElanImporter.setObjectName("ElanImporter")
        ElanImporter.resize(449, 382)
        ElanImporter.setWindowTitle("")
        self.centralWidget = QtWidgets.QWidget(parent=ElanImporter)
        self.centralWidget.setGeometry(QtCore.QRect(0, 0, 602, 670))
        self.centralWidget.setObjectName("centralWidget")
        self.label = QtWidgets.QLabel(parent=self.centralWidget)
        self.label.setGeometry(QtCore.QRect(14, 140, 267, 16))
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.centralWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 165, 428, 175))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sourceList = QtWidgets.QTreeWidget(parent=self.horizontalLayoutWidget)
        self.sourceList.setMinimumSize(QtCore.QSize(0, 157))
        self.sourceList.setMaximumSize(QtCore.QSize(300, 157))
        self.sourceList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sourceList.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.sourceList.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.DragOnly)
        self.sourceList.setIndentation(5)
        self.sourceList.setUniformRowHeights(True)
        self.sourceList.setAllColumnsShowFocus(True)
        self.sourceList.setColumnCount(0)
        self.sourceList.setObjectName("sourceList")
        self.sourceList.header().setVisible(False)
        self.horizontalLayout.addWidget(self.sourceList)
        self.targetList = QtWidgets.QTableWidget(parent=self.horizontalLayoutWidget)
        self.targetList.setMinimumSize(QtCore.QSize(0, 157))
        self.targetList.setMaximumSize(QtCore.QSize(300, 157))
        self.targetList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.targetList.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.targetList.setDragEnabled(True)
        self.targetList.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.DragDrop)
        self.targetList.setDefaultDropAction(QtCore.Qt.DropAction.MoveAction)
        self.targetList.setColumnCount(0)
        self.targetList.setObjectName("targetList")
        self.targetList.setRowCount(0)
        self.targetList.horizontalHeader().setHighlightSections(False)
        self.targetList.verticalHeader().setDefaultSectionSize(31)
        self.horizontalLayout.addWidget(self.targetList)
        self.tMetadataBox = QtWidgets.QGroupBox(parent=self.centralWidget)
        self.tMetadataBox.setGeometry(QtCore.QRect(9, 60, 429, 64))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tMetadataBox.sizePolicy().hasHeightForWidth())
        self.tMetadataBox.setSizePolicy(sizePolicy)
        self.tMetadataBox.setStyleSheet("QPlainTextEdit {\n"
"    font-size: 9;\n"
"    border-radius: 0pts;\n"
"    max-height: 16px;\n"
"    min-width: 45px;\n"
"    min-height: 16px;\n"
"    padding: 1px;\n"
"}")
        self.tMetadataBox.setObjectName("tMetadataBox")
        self.formLayoutWidget = QtWidgets.QWidget(parent=self.tMetadataBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 30, 414, 20))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.formLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tLabelSource = QtWidgets.QLabel(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tLabelSource.setFont(font)
        self.tLabelSource.setObjectName("tLabelSource")
        self.horizontalLayout_2.addWidget(self.tLabelSource)
        self.newResearcher = QtWidgets.QPlainTextEdit(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.newResearcher.setFont(font)
        self.newResearcher.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.newResearcher.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.newResearcher.setObjectName("newResearcher")
        self.horizontalLayout_2.addWidget(self.newResearcher)
        self.tLabelResearcher = QtWidgets.QLabel(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tLabelResearcher.setFont(font)
        self.tLabelResearcher.setObjectName("tLabelResearcher")
        self.horizontalLayout_2.addWidget(self.tLabelResearcher)
        self.newSource = QtWidgets.QPlainTextEdit(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.newSource.setFont(font)
        self.newSource.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.newSource.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.newSource.setObjectName("newSource")
        self.horizontalLayout_2.addWidget(self.newSource)
        self.tLabelDate = QtWidgets.QLabel(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tLabelDate.setFont(font)
        self.tLabelDate.setObjectName("tLabelDate")
        self.horizontalLayout_2.addWidget(self.tLabelDate)
        self.newDate = QtWidgets.QPlainTextEdit(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.newDate.setFont(font)
        self.newDate.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.newDate.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.newDate.setObjectName("newDate")
        self.horizontalLayout_2.addWidget(self.newDate)
        self.tLabelUpdated = QtWidgets.QLabel(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tLabelUpdated.setFont(font)
        self.tLabelUpdated.setObjectName("tLabelUpdated")
        self.horizontalLayout_2.addWidget(self.tLabelUpdated)
        self.newTranscriber = QtWidgets.QPlainTextEdit(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.newTranscriber.setFont(font)
        self.newTranscriber.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.newTranscriber.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.newTranscriber.setReadOnly(False)
        self.newTranscriber.setObjectName("newTranscriber")
        self.horizontalLayout_2.addWidget(self.newTranscriber)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=self.centralWidget)
        self.buttonBox.setGeometry(QtCore.QRect(189, 343, 243, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok|QtWidgets.QDialogButtonBox.StandardButton.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(parent=self.centralWidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(13, 9, 426, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_2)
        self.label_5.setMinimumSize(QtCore.QSize(35, 0))
        self.label_5.setMaximumSize(QtCore.QSize(35, 16777215))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.title = QtWidgets.QPlainTextEdit(parent=self.horizontalLayoutWidget_2)
        self.title.setMinimumSize(QtCore.QSize(85, 0))
        self.title.setMaximumSize(QtCore.QSize(485, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.horizontalLayout_3.addWidget(self.title)

        self.retranslateUi(ElanImporter)
        QtCore.QMetaObject.connectSlotsByName(ElanImporter)

    def retranslateUi(self, ElanImporter):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("ElanImporter", "Drag ELAN tiers into the box on the right."))
        self.tMetadataBox.setTitle(_translate("ElanImporter", "Metadata"))
        self.tLabelSource.setText(_translate("ElanImporter", "Source"))
        self.newResearcher.setToolTip(_translate("ElanImporter", "person who collected form"))
        self.tLabelResearcher.setText(_translate("ElanImporter", "Researcher"))
        self.newSource.setToolTip(_translate("ElanImporter", "original speaker source"))
        self.tLabelDate.setText(_translate("ElanImporter", "Date"))
        self.newDate.setToolTip(_translate("ElanImporter", "date collected. yyyy–MM–dd \n"
"format recommended"))
        self.tLabelUpdated.setText(_translate("ElanImporter", "Transcribers"))
        self.newTranscriber.setToolTip(_translate("ElanImporter", "date last updated"))
        self.label_5.setText(_translate("ElanImporter", "Title:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ElanImporter = QtWidgets.QDialog()
    ui = Ui_ElanImporter()
    ui.setupUi(ElanImporter)
    ElanImporter.show()
    sys.exit(app.exec())
