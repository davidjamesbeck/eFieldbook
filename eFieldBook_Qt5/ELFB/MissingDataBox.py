# -*- coding: utf-8 -*-

"""
Module implementing Missing data warning.
"""

from PyQt6 import QtWidgets


class MissingDataBox(QtWidgets.QMessageBox):
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """        
        super(MissingDataBox, self).__init__(parent)
        QtWidgets.QDialog.__init__(self, parent)
        self.setStyleSheet('font-size: 18pts;')

    def setWarningText(self, text, title):
        self.setWindowTitle(title)
        self.setText(text)
