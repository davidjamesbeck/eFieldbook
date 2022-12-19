# -*- coding: utf-8 -*-

"""
Module implementing AddLineDialog.
"""

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDialog

from .Ui_AddTextLine import Ui_Dialog


class AddLineDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(AddLineDialog, self).__init__(parent)
        self.setupUi(self)
        
    def returnValues(self):
        newLine = self.newLine.toPlainText()
        if len(self.newGloss.toPlainText()) != 0:
            newGloss = self.newGloss.toPlainText()
        else:
            newGloss = None
        unparseable = self.parsingBox.isChecked()
        values = [newLine, newGloss, unparseable]
        return values
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        self.accept()
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        self.reject()
