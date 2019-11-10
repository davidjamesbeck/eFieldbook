from PyQt5 import QtWidgets, QtCore
from ELFB import dataIndex
from ELFB.palettes import GrammarManager

class GrmField(QtWidgets.QTextEdit): 
    '''class defines the properties of the grammar field on the lexicon card'''
    def __init__(self, parent):
        super(GrmField, self).__init__(parent)
        self.initUI()
        self.setStyleSheet('font-size: 10pts;')

    def initUI(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setReadOnly(True)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.setObjectName("lGrammar")

    def mouseDoubleClickEvent(* event):
        gManager = GrammarManager.GrammarManager(dataIndex.fldbk)
        gManager.setValues(dataIndex.currentCard)
        gManager.exec()
