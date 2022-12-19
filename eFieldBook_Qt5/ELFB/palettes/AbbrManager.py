# -*- coding: utf-8 -*-

"""
Module implementing AbbrManager.
"""

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog

from .Ui_AbbrManager import Ui_AbbrManager


class AbbrManager(QDialog, Ui_AbbrManager):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(AbbrManager, self).__init__(parent)
        self.setupUi(self)

    def checkUpdate(self):
        if self.updateCheckbox.isChecked():
            return True
        else:
            return False

    def setAbbr(self, abvNode):
        self.abbreviation.setHtml(abvNode.attrib.get('Abv'))
        self.gloss.setHtml(abvNode.attrib.get('Term'))
        try:
            self.form.setHtml(abvNode.attrib.get('Form'))
        except AttributeError:
            pass

    def setData(self):
        if len(self.abbreviation.toPlainText()) != 0 and len(self.gloss.toPlainText()) != 0:
            dataList = [self.abbreviation.toPlainText(), self.gloss.toPlainText()]
            if len(self.form.toPlainText()) != 0:
                dataList.append(self.form.toPlainText())
            else:
                dataList.append(None)
        else:
            queryBox = QtWidgets.QMessageBox()
            queryBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            queryBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            queryBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            queryBox.setText('Please give an abbreviation\nand a gloss.')
            queryBox.exec()
            return
        return dataList
    
    @QtCore.pyqtSlot()
    def on_buttonBox_accepted(self):
        
        self.accept()
    
    @QtCore.pyqtSlot()
    def on_buttonBox_rejected(self):
        
        self.reject()
