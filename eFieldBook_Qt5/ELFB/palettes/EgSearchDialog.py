"""
Module implementing EgSearchDialog.
"""

from PyQt6.QtWidgets import QDialog
from PyQt6 import QtCore
from .Ui_EgSearchDialog import Ui_SearchExamples
from ELFB.palettes import SearchHelp


class EgSearchDialog(QDialog, Ui_SearchExamples):
    """
    Class documentation goes here.
    """

    def __init__(self, parent):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        print('building eg search dialog')
        super(EgSearchDialog, self).__init__(parent)
        self.setupUi(self)

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key.Key_Return:
            print('return in field')
            self.callSearchEngine()
        else:
            super().keyPressEvent(qKeyEvent)

    @QtCore.pyqtSlot()
    def on_egSearchHelpBtn_released(self):
        """
        Slot documentation goes here.
        """
        helpDialog = SearchHelp.EgSearchHelpDialog(self)
        helpDialog.exec()

    @QtCore.pyqtSlot()
    def on_clearBtn_released(self):
        """
        Clear search fields.
        """
        self.Line.clear()
        self.Morph.clear()
        self.ILEG.clear()
        self.L1Gloss.clear()
        self.L2Gloss.clear()
        self.Comments.clear()
        self.Keywords.clear()
        self.Source.clear()
        self.Researcher.clear()
        self.Date.clear()
        self.Updated.clear()
