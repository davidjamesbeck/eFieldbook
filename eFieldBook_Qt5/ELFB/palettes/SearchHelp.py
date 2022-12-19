"""
Module implementing SearchHelp dialog.
"""

from PyQt6.QtWidgets import QDialog
from PyQt6 import QtCore
from ELFB import dataIndex
from .Ui_SearchHelp import Ui_SearchHelpDialog


class SearchHelpDialog(QDialog, Ui_SearchHelpDialog):
    """
    template for help dialogs.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setHelpText()

    @QtCore.pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        self.accept()

    @QtCore.pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        self.reject()

    def setHelpText(self):
        pass


class EgSearchHelpDialog(SearchHelpDialog):
    """
    Search help for examples.
    """

    def setHelpText(self):
        self.setWindowTitle('Search help')
        helpFile = QtCore.QFile(dataIndex.rootPath + '/ELFB/EgHelpText.txt')
        helpFile.open(QtCore.QIODevice.OpenModeFlag.ReadOnly | QtCore.QIODevice.OpenModeFlag.Text)
        stream = QtCore.QTextStream(helpFile)
        details = stream.readAll()
        helpFile.close()
        self.helpText.setHtml(details)


class OrthHelpDialog(SearchHelpDialog):
    """
    Search help for examples.
    """

    def setHelpText(self):
        # TODO: write a more complete help text
        self.setWindowTitle('Orthographies help')
        helpFile = QtCore.QFile(dataIndex.rootPath + '/ELFB/OrthHelpText.txt')
        helpFile.open(QtCore.QIODevice.OpenModeFlag.ReadOnly | QtCore.QIODevice.OpenModeFlag.Text)
        stream = QtCore.QTextStream(helpFile)
        details = stream.readAll()
        helpFile.close()
        self.helpText.setHtml(details)
