# -*- coding: utf-8 -*-

"""
Module implementing NewLexDialog.
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog
from ELFB import dataIndex

from .Ui_NewLexDialog import Ui_NewLexDialog


class NewLexDialog(QDialog, Ui_NewLexDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(NewLexDialog, self).__init__(parent)
        self.setupUi(self)
        codeList = sorted(dataIndex.speakerDict.keys())
        for index, item in enumerate(codeList):
            try:
                fullName = dataIndex.speakerDict.get(item).findtext('Name')
                item += ' (' + fullName + ')'
                codeList[index] = item
            except TypeError:
                pass
        self.speakerCode.insertItems(0,codeList)
        if dataIndex.lastSpeaker:
            j = self.speakerCode.findText(dataIndex.lastSpeaker,QtCore.Qt.MatchStartsWith)
            self.speakerCode.setCurrentIndex(j)        
        
        codeList = sorted(dataIndex.rschrDict.keys())
        self.researcherCode.insertItems(0,codeList)                                
        if dataIndex.lastRschr:
            j = self.researcherCode.findText(dataIndex.lastRschr,QtCore.Qt.MatchExactly)
            self.researcherCode.setCurrentIndex(j)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        if dataIndex.unsavedEdit == 1:
            self.prevEdit = 1
        self.entryWord.setFocus()

    def setSpeaker(self):
        lastSpeaker = self.speakerCode.currentText().split(None,1)
        dataIndex.lastSpeaker = lastSpeaker[0]
        dataIndex.unsavedEdit = 1

    def setRschr(self):
        lastRschr = self.researcherCode.currentText().split(None,1)
        dataIndex.lastRschr = lastRschr[0]
        dataIndex.unsavedEdit = 1

    def getData(self):
        metaData = []
        speaker = self.speakerCode.currentText().split(None,1)
        metaData.append(speaker[0])
        metaData.append(self.researcherCode.currentText())
        metaData.append(self.entryWord.toPlainText())
        metaData.append(self.gloss.toPlainText())
        return metaData
    
    @QtCore.pyqtSlot()
    def on_buttonBox_accepted(self):
        if len(self.entryWord.toPlainText()) == 0 or len(self.gloss.toPlainText()) == 0:
            self.badBox = QtWidgets.QMessageBox()
            self.badBox.setIcon(QtWidgets.QMessageBox.Warning)
            self.badBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.badBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            self.badBox.setText('Incomplete entry.')
            self.badBox.setInformativeText('Provide a form and a gloss '
                                           'in the primary working language.')
            self.badBox.exec_()
            return
        dataIndex.unsavedEdit = 1
        self.accept()
        
    @QtCore.pyqtSlot()
    def on_buttonBox_rejected(self):
        if self.prevEdit == 0:
            dataIndex.unsavedEdit = 0
        self.reject()
