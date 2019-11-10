from PyQt5 import QtWidgets
from ELFB import dataIndex

# -*- coding: utf-8 -*-

"""
Module implementing TierManager.
"""

#from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog

from .Ui_TierManager import Ui_Dialog


class TierManager(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(TierManager, self).__init__(parent)
        self.setupUi(self)
        if dataIndex.root.attrib.get('Tiers') != None:
            tierList = dataIndex.root.attrib.get('Tiers').split(", ")
            for item in tierList:
                self.tierBox.addItem(item)
        self.tierBox.addItem('New …')
        currentIndex = self.tierBox.findText('New …')
        self.tierBox.setCurrentIndex(currentIndex)
        self.newTierName = None
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        self.fldbk = dataIndex.fldbk
 
    @QtCore.pyqtSlot(str)
    def on_tierBox_activated(self, p0):
        """
        Slot documentation goes here.
        """
        labelList = []
        for r in range(0, self.fldbk.eAnalysis.rowCount()):
            labelList.append(self.fldbk.eAnalysis.verticalHeaderItem(r).text())
        if p0 == "New …":    
            tierDialog = QtWidgets.QInputDialog()
            newTier = tierDialog.getText(self, 'Create New Tier Type','Tier Name:' , QtWidgets.QLineEdit.Normal)
            if newTier[1] == True:
                if self.newTierName == None:
                    self.newTierName = []
                self.newTierName.append(newTier[0])
                self.tierBox.addItem(newTier[0])
                currentIndex = self.tierBox.findText(newTier[0])
                self.tierBox.setCurrentIndex(currentIndex)
        elif p0 in labelList:
            '''there is already the selected type of tier on this card'''
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Warning)
            mbox.setText("Non-unique tier.")
            mbox.setInformativeText('Tiers must be unique for each example.')
            mbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            mbox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            mbox.exec_()
        else:
            if self.newTierName == None:
                self.newTierName = []
            self.newTierName.append(self.tierBox.currentText())

    def onOkay(self):
        if self.newTierName == "New …":
            self.reject()
        if self.newTierName == None:
            self.newTierName.append(self.tierBox.currentText())

    def onCancel(self):
        return
        
