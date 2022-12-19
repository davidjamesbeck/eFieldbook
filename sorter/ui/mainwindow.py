# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
import xml.etree.ElementTree as etree
from .Ui_mainwindow import Ui_MainWindow

class Alphabetizer(QtGui.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(Alphabetizer, self).__init__(parent)
        self.setSortCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.sort(0,QtCore.Qt.SortOrder.AscendingOrder)
        self.buildOrder()
        
    def buildOrder(self):    
        defaultOrdering = open('/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/sorter/default.txt', 'r', encoding="UTF-8").read()
        orderList = defaultOrdering.split(',')
        sortOrderList = []
        for i in range(0, len(orderList)):
            item = orderList[i].strip()
            ordinal = str(chr(i+8704))
            sortOrderList.append([item, ordinal,  len(item)])
        unorderedSortKey = sorted(sortOrderList,  key = lambda s: s[2],  reverse=True)
        self.sortKey = []
        for item in unorderedSortKey:
            self.sortKey.append(item[:-1])
 
    def lessThan(self,  left,  right):
        leftData = self.transform(self.sourceModel().data(left))
        rightData = self.transform(self.sourceModel().data(right))
        if leftData < rightData:
            return True
        else:
            return False
  
    def transform(self, string):
        string = string.replace("á", "a")
        string = string.replace("é", "e")
        string = string.replace("í", "i")
        string = string.replace("ó", "o")
        string = string.replace("ú", "u")
        if string[-1] == '-':
            string = string[:-1]
        string = string.replace("=", "")
        for item in self.sortKey:
            if item[0] in string:
                string = string.replace(item[0], item[1])
        return string

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.fname ='/Users/David/Library/Mobile Documents/com~apple~CloudDocs/Current/ELFB/data/2015-06-23.xml'
        xmltree = etree.parse(self.fname)
        root = xmltree.getroot()
        navModel = QtGui.QStandardItemModel()
        for node in root.iter('Lex'):
            LexID = node.attrib.get('LexID')
            Orth = node.findtext('Orth') + '\n' + 'another line'
            item = QtGui.QStandardItem(Orth)
            item.setData(LexID, 32)
            navModel.appendRow(item)
        self.start.setModel(navModel)       
        self.start.setSelectionModel(self.start.selectionModel())   
    
    @pyqtSlot()
    def on_doSort_released(self):
        """
        Slot documentation goes here.
        """
        proxyModel = Alphabetizer()
        proxyModel.setDynamicSortFilter(True)
        proxyModel.setSourceModel(self.start.model())
        self.finish.setModel(proxyModel)
