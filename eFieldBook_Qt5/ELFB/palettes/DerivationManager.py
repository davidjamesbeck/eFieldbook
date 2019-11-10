# -*- coding: utf-8 -*-

"""
Module implementing DerivationManager.
"""

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QDialog
from ELFB import dataIndex

from .Ui_DerivationManager import Ui_DerivationManager


class DerivationManager(QDialog, Ui_DerivationManager):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DerivationManager, self).__init__(parent)
        self.setupUi(self)
        self.lexList.doubleClicked.connect(self.on_buttonBox_accepted)
        self.lexList.setStyleSheet("selection-background-color:#E6E6E6;selection-color:black;")
        self.fldbk = dataIndex.fldbk

    def listEntries(self):
        proxyModel = self.fldbk.lLexNav.model()
        drvnModel = QtGui.QStandardItemModel()
        for i in range(0, proxyModel.rowCount()):
            key = proxyModel.index(i, 0).data(32)
            head = dataIndex.lexDict[key].findtext('Orth')
            Def = dataIndex.lexDict[key].findtext('Def/L1')
            if dataIndex.lexDict[key].find('POS') != None:
                POS = "(" + dataIndex.lexDict[key].findtext('POS') + ")"
                newText = head + " " + POS + " " + Def
            else:
                newText = head + " " + Def
            newItem = QtGui.QStandardItem(newText)
            newItem.setData(key, 32)
            drvnModel.appendRow(newItem)
        self.lexList.setModel(drvnModel)
        self.setWindowTitle("Select entry to link to")

    def listDerivatives(self):
        fldbk = self.fldbk
        drModel = QtGui.QStandardItemModel()
        for i in range(0,fldbk.lDerivatives.count()):
            derID = fldbk.lDerivatives.item(i).data(32)
            text = fldbk.lDerivatives.item(i).text()
            item = QtGui.QStandardItem()
            item.setData(derID, 32)
            item.setText(text)
            drModel.appendRow(item) 
        self.lexList.setModel(drModel)
        self.setWindowTitle("Select derivative to remove")
    
    def setData(self):
        data = self.lexList.currentIndex().data(32)
        return(data)
        
    @QtCore.pyqtSlot()
    def on_buttonBox_accepted(self):
        self.accept()
    
    @QtCore.pyqtSlot()
    def on_buttonBox_rejected(self):
        self.reject()
