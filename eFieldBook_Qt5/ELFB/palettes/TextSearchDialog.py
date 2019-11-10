
"""
Module implementing TextSearchDialog.
"""

from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore
from .Ui_TextSearchDialog import Ui_SearchTexts
from ELFB.palettes import SearchHelp

class TextSearchDialog(QDialog, Ui_SearchTexts):
    """
    Class documentation goes here.
    """
    def __init__(self, parent):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(TextSearchDialog, self).__init__(parent)
        self.setupUi(self)
        self.Source.setEnabled(0)
        self.Researcher.setEnabled(0)
        self.Date.setEnabled(0)
        self.Updated.setEnabled(0)
        self.Comments.setEnabled(0)
        self.Keywords.setEnabled(0)
        self.limitBtn.stateChanged.connect(self.toggleLimit)
        self.toggleLimit()
        
    def toggleLimit(self):
        if self.limitBtn.isChecked() == 0:
            self.Source.setEnabled(1)
            self.Researcher.setEnabled(1)
            self.Date.setEnabled(1)
            self.Updated.setEnabled(1)
            self.Comments.setEnabled(1)
            self.Keywords.setEnabled(1)
        else:
            self.Source.setEnabled(0)
            self.Researcher.setEnabled(0)
            self.Date.setEnabled(0)
            self.Updated.setEnabled(0)            
            self.Comments.setEnabled(0)
            self.Keywords.setEnabled(0)
    
    @QtCore.pyqtSlot()
    def on_textSearchHelpBtn_released(self):
        """
        Slot documentation goes here.
        """
        helpDialog = SearchHelp.EgSearchHelpDialog(self)
        helpDialog.exec_()

