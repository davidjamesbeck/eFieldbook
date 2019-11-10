# -*- coding: utf-8 -*-

"""
Module implementing StyledInputDialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_StyledInputDialog import Ui_Dialog


class StyledInputDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(StyledInputDialog, self).__init__(parent)
        self.setupUi(self)
        self.input = None
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        if len(self.lineInput.text()) == 0:
            self.reject()
        else:
            self.input = self.lineInput.text()            
            self.accept()
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        self.reject()
    
    @pyqtSlot()
    def on_lineInput_returnPressed(self):
        """
        Slot documentation goes here.
        """
        self.input = self.lineInput.text()
        self.accept()

    def returnInput(self):
        return self.input
