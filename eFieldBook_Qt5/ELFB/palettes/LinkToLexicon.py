# -*- coding: utf-8 -*-

"""
Module implementing EntryManager.
Selects lexical entry to link to example card.
"""
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog, QTreeWidgetItem
from ELFB import HTMLDelegate, dataIndex, formattingHandlers
from .Ui_LinkToLexicon import Ui_EntryManager


class EntryManager(QDialog, Ui_EntryManager):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        super(EntryManager, self).__init__(parent)
        self.setupUi(self)
        delegate = HTMLDelegate.HTMLDelegate()
        self.lexList.setItemDelegate(delegate)
        self.setStyleSheet("selection-background-color:#E6E6E6;selection-color:black;")
        self.fldbk = dataIndex.fldbk

    def listEntries(self):
        proxyModel = self.fldbk.lLexNav.model()
        for j in range(0, proxyModel.rowCount()):
            derID = proxyModel.index(j, 0).data(32)
            child = dataIndex.lexDict[derID]
            lexeme = '<b>' + child.findtext('Orth') + '</b>'
            POS = child.findtext('POS')
            L1List = child.findall('Def/L1')
            item = QtWidgets.QTreeWidgetItem()
            item.setData(0, 32, derID)
            for i in range(0, len(L1List)):
                L1 = L1List[i].text
                L1 = formattingHandlers.XMLtoRTF(L1)
                if len(L1List) != 1:
                    indexNo = str(i + 1) + ") "
                else:
                    indexNo = None
                if indexNo is None:
                    try:
                        txt1 = lexeme + " (" + POS + ") " + L1
                    except TypeError:
                        txt1 = lexeme + " " + L1
                    item.setText(0, txt1)
                    item.setData(0, 33, 1)
                else:
                    if i == 0:
                        try:
                            txt1 = lexeme + " (" + POS + ") "
                        except TypeError:
                            txt1 = lexeme + " "
                        item.setText(0, txt1)
                        item.setData(0, 33, i + 1)
                    txt = indexNo + L1
                    defItem = QtWidgets.QTreeWidgetItem(item)
                    defItem.setText(0, txt)
                    defItem.setData(0, 32, derID)
                    defItem.setData(0, 33, i + 1)
            self.lexList.addTopLevelItem(item)
            item.setExpanded(1)
        self.setWindowTitle(QtWidgets.QApplication.translate("EntryManager", "Select lexical entry", None))

    def setDataAndGo(self):
        self.setData()
        self.accept()

    def setData(self):
        entry = self.lexList.currentItem().data(0, 32)
        index = self.lexList.currentItem().data(0, 33)
        data = [entry, index]
        return (data)

    @QtCore.pyqtSlot(QTreeWidgetItem, int)
    def on_lexList_itemDoubleClicked(self):
        self.setDataAndGo()

    @QtCore.pyqtSlot()
    def on_buttonBox_accepted(self):
        self.setData()
        self.accept()

    @QtCore.pyqtSlot()
    def on_buttonBox_rejected(self):
        self.reject()
