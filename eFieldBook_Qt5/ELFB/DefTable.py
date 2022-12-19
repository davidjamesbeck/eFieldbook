from PyQt6 import QtWidgets, QtCore
from ELFB import cardLoader, dataIndex, HTMLDelegate
from ELFB.palettes import DefinitionsManager


class DefTable(QtWidgets.QTableWidget):
    """class defines the properties of the definition fields on the lexicon card"""
    def __init__(self, parent):
        super(DefTable, self).__init__(parent)
        self.initUI()
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("selection-background-color: #F0F0F0;")
        delegate = HTMLDelegate.HTMLDelegate()
        self.setItemDelegate(delegate)
        self.itemDoubleClicked.connect(self.cellDoubleClicked)
#        self.itemClicked.connect(self.cellClicked)
        self.fldbk = dataIndex.fldbk
        
    def initUI(self):
        self.setGeometry(QtCore.QRect(7, 26, 689, 116))
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setShowGrid(0)

        
    def cellDoubleClicked(self, item):
        if item.data(35) is None:
            fManager = DefinitionsManager.DefinitionsManager(self.fldbk)
            fManager.exec()
        else:
            exRoot = dataIndex.exDict[item.data(35)]
            cardLoader.loadExCard(exRoot)
            self.fldbk.tabWidget.setCurrentIndex(3)
