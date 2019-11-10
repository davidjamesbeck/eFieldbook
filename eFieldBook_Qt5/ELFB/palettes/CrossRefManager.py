# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog
from ELFB import dataIndex

from .Ui_CrossRefManager import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
    
    def setRefs(self,synList):
        j = 0
        for item in list(set(synList)):
            node = dataIndex.lexDict[item]
            linkText = node.findtext('Orth') + " (" + node.findtext('POS') + ") " + node.findtext('Def/L1')
            listItem = QtWidgets.QListWidgetItem()
            listItem.setText(linkText)
            listItem.setData(34,item)
            self.refList.insertItem(j,listItem)
            j += 1
        self.refList.sortItems(QtCore.Qt.AscendingOrder)

    def getRef(self):
        crossRef = self.refList.currentItem().data(34)
        return crossRef
   
    @QtCore.pyqtSlot()
    def on_buttonBox_accepted(self):
        self.accept()
    
    @QtCore.pyqtSlot()
    def on_buttonBox_rejected(self):
        self.reject()
    
    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem)
    def on_refList_itemDoubleClicked(self, item):
        """
        Slot documentation goes here.
        
        @param item DESCRIPTION
        @type QListWidgetItem
        """
        self.accept()
