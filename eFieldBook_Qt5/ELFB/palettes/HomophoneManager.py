# -*- coding: utf-8 -*-

"""
Module implementing HomophoneManager.
"""

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDialog, QListWidgetItem

from .Ui_HomophoneManager import Ui_Dialog


class HomophoneManager(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(HomophoneManager, self).__init__(parent)
        self.setupUi(self)
        self.selection = ''
        self.index = None
        self.defaultChecked = 0

    @pyqtSlot(int)
    def on_defaultSelect_stateChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type int
        """
        if p0 == 0:
            self.defaultchecked == 0
        else:
            self.defaultChecked == 1

    @pyqtSlot()
    def on_okButton_released(self):
        """
        Slot documentation goes here.
        """
        self.accept()

    @pyqtSlot(QListWidgetItem)
    def on_alternativesList_itemClicked(self, item):
        self.selection = item.text()
        self.index = self.alternativesList.currentRow()

    @pyqtSlot(QListWidgetItem)
    def on_alternativesList_itemDoubleClicked(self, item):
        self.selection = item.text()
        self.index = self.alternativesList.currentRow()
        self.accept()
