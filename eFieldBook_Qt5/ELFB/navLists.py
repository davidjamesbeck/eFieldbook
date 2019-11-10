from PyQt5 import QtWidgets, QtCore, QtGui
from ELFB import dataIndex,  Alphabetizer, formattingHandlers

'''Build list boxes for Home, Lexicon, Texts, and Dataset cards'''

def navListBuilderLex(fldbk):
    '''make models for the lex Navs'''
    navModelL = QtGui.QStandardItemModel()
    for node in dataIndex.root.iter('Lex'):
        LexID = node.attrib.get('LexID')
        Orth = node.findtext('Orth')
        dataIndex.lexDict[LexID] = node
        item = QtGui.QStandardItem(Orth)
        item.setData(LexID, 32)
        navModelL.appendRow(item)
    proxyModelL = Alphabetizer.Alphabetizer(fldbk)
    proxyModelL.setSourceModel(navModelL)
    proxyModelL.setDynamicSortFilter(True)
    fldbk.hLexNav.setModel(proxyModelL)
    fldbk.lLexNav.setModel(proxyModelL)
    fldbk.hLexNav.setSelectionModel(fldbk.lLexNav.selectionModel())     
    s = str(formattingHandlers.addCommas(navModelL.rowCount()))
    if s == '1':
        fldbk.hLexiconLabel.setText("Lexicon: 1 entry")
    else:
        fldbk.hLexiconLabel.setText("Lexicon: %s entries" % s)    
   
def navListBuilderText(fldbk):    
    navModelT = QtGui.QStandardItemModel()
    for node in dataIndex.root.iter('Text'):
        TextID = node.attrib.get('TextID')
        Title = node.findtext('Title')
        Title = formattingHandlers.XMLtoPlainText(Title)
        dataIndex.textDict[TextID] = node
        item = QtGui.QStandardItem(Title)
        item.setData(TextID, 32)
        navModelT.appendRow(item)
    proxyModelT = QtCore.QSortFilterProxyModel()
    proxyModelT.setSourceModel(navModelT)
    proxyModelT.setSortCaseSensitivity(0)
    proxyModelT.sort(0,QtCore.Qt.AscendingOrder)
    fldbk.hTextNav.setModel(proxyModelT)
    fldbk.tTextNav.setModel(proxyModelT)
    fldbk.hTextNav.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    fldbk.tTextNav.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    s = str(formattingHandlers.addCommas(navModelT.rowCount()))
    if s == '1':
        fldbk.hTextsLabel.setText("Texts: 1 text")
    else:
        fldbk.hTextsLabel.setText("Texts: %s texts" % s)
    fldbk.hTextNav.setSelectionModel(fldbk.tTextNav.selectionModel())        
    
def navListBuilderData(fldbk):
    navModelD = QtGui.QStandardItemModel()
    for node in dataIndex.root.iter('Dset'):
        dsetID = node.attrib.get('DsetID')
        dTitle = node.findtext('Title')
        dTitle = formattingHandlers.XMLtoPlainText(dTitle)
        dataIndex.dataDict[dsetID] = node
        item = QtGui.QStandardItem(dTitle)
        item.setData(dsetID, 32)
        navModelD.appendRow(item)
    proxyModelD = QtCore.QSortFilterProxyModel()
    proxyModelD.setSourceModel(navModelD)
    proxyModelD.setSortCaseSensitivity(0)
    proxyModelD.sort(0,QtCore.Qt.AscendingOrder)
    fldbk.hDataNav.setModel(proxyModelD)
    fldbk.dDataNav.setModel(proxyModelD)
    s = str(formattingHandlers.addCommas(navModelD.rowCount()))
    if s == '1':
        fldbk.hDatasetLabel.setText("Datasets: 1 dataset")
    else:
        fldbk.hDatasetLabel.setText("Datasets: %s datasets" % s)
    fldbk.hDataNav.setSelectionModel(fldbk.dDataNav.selectionModel())        

    
