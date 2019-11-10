
"""
Module implementing DSetSearchDialog.
"""

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot

from .Ui_DSetSearchDialog import Ui_SearchDSets


class DSetSearchDialog(QDialog, Ui_SearchDSets):
    """
    Class documentation goes here.
    """
    def __init__(self, parent):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(DSetSearchDialog, self).__init__(parent)
        self.setupUi(self)
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
            self.appendBtn.setEnabled(1)
        else:
            self.Source.setEnabled(0)
            self.Researcher.setEnabled(0)
            self.Date.setEnabled(0)
            self.Updated.setEnabled(0)            
            self.Comments.setEnabled(0)
            self.Keywords.setEnabled(0)
            self.appendBtn.setEnabled(0)

    @pyqtSlot()
    def on_clearBtn_released(self):
        """
        Clear search fields.
        """
        self.SearchText.clear()
        self.Comments.clear()
        self.Keywords.clear()
        self.Source.clear()
        self.Researcher.clear()
        self.Date.clear()
        self.Updated.clear()
