# -*- coding: utf-8 -*-

"""
Module implementing GrammarManager.
"""

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog
from ELFB import HTMLDelegate, dataIndex, contextMenus, cardLoader
from ELFB.palettes import CrossRefManager
from xml.etree import ElementTree as etree
from ELFB.palettes.SoundPanel import SoundPanel

from .Ui_GrammarManager import Ui_gManager


class GrammarManager(QDialog, Ui_gManager):
    """
    class for constraining user input to lexicon grammar fields
    """

    class focusFilter(QtCore.QObject):
        def __init__(self, parent):
            super(GrammarManager.focusFilter, self).__init__(parent)

        def eventFilter(self, sender, event):
            gManager = sender.parent().parent()
            if event.type() == QtCore.QEvent.Type.FocusIn:
#                print("my name is %s" % sender.objectName())
                if sender.objectName() == "grammar" or sender.objectName() == "C2":
#                    print('okay')
                    gManager.whichTable = sender.objectName()
                    gManager.gSound.setEnabled(1)
                    gManager.Del.setEnabled(1)
                    gManager.Add.setEnabled(1)
                    pass
                if sender.objectName() == "Cross_ref":
                    gManager.Del.setEnabled(0)
                    gManager.Add.setEnabled(0)
                    pass
                try:
                    sender.clearSelection()
                except AttributeError:
                    pass
            if event.type() == QtCore.QEvent.Type.FocusOut:
                if sender.objectName() == "grammar" or sender.objectName() == "C2":
                    gManager.gSound.setEnabled(0)
                    gManager.gSound.clearAll()
                    sender.clearSelection()
            if event.type() == QtCore.QEvent.Type.Leave:
                if sender.objectName() == "grammar" or sender.objectName() == "C2":
                    sender.endEdit()
            return False

    class paletteField(QtWidgets.QTextEdit):
        def __init__(self, parent):
            super(GrammarManager.paletteField, self).__init__(parent)
            self.filter = GrammarManager.focusFilter(self)
            self.installEventFilter(self.filter)
            self.textChanged.connect(self.flagUnsavedEdits)

        def flagUnsavedEdits(self):
            dataIndex.unsavedEdit = 1
            pass

    class grmTable(QtWidgets.QTableWidget):
        def __init__(self, parent):
            super(GrammarManager.grmTable, self).__init__(parent)
            self.gManager = self.parent().parent()
            self.gManager.whichTable = ''
            self.setStyleSheet("selection-background-color: #F0F0F0;")
            delegate = HTMLDelegate.HTMLDelegate()
            self.setItemDelegate(delegate)
            self.filter = GrammarManager.focusFilter(self)
            self.installEventFilter(self.filter)
            self.cellChanged.connect(self.flagUnsavedEdits)
            self.cellClicked.connect(self.showMedia)

        def showMedia(self, r, c):
            self.gManager.gSound.setEnabled(1)
            self.gManager.gSound.GrammarManagerCell = [r, c]
            try:
                if self.item(r, 0).data(35):
                    MediaRef = [self.item(r, 0).data(35)]
                    self.gManager.gSound.loadMedia(None, MediaRef)
                    return
            except AttributeError:
                pass

        def flagUnsavedEdits(self):
            dataIndex.unsavedEdit = 1
            pass

        def endEdit(self):
            """this is needed so when the user clicks okay after making a change"""
            """without having clicked on another field, the change is registered"""
            index = self.currentIndex()
            self.currentChanged(index, index)

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(GrammarManager, self).__init__(parent)
        self.setupUi(self)
        self.fldbk = dataIndex.fldbk
        self.gManager = self
        self.fldbk = dataIndex.fldbk
        self.grammar = self.grmTable(self.lexBox)
        self.grammar.setObjectName('grammar')
        self.grammar.setGeometry(15, 37, 380, 137)
        self.grammar.setRowCount(0)
        self.grammar.horizontalHeader().setEnabled(0)
        self.grammar.horizontalHeader().hide()
        self.grammar.verticalHeader().setEnabled(0)
        self.grammar.verticalHeader().hide()
        self.grammar.setColumnCount(3)
        self.grammar.setColumnWidth(0, 30)
        self.grammar.setColumnWidth(1, 300)
        self.grammar.setColumnWidth(2, 48)
        self.grammar.setSortingEnabled(1)

        self.C2 = self.grmTable(self.lexBox)
        self.C2.setObjectName('C2')
        self.C2.setGeometry(15, 210, 380, 92)
        self.C2.setRowCount(0)
        self.C2.horizontalHeader().setEnabled(0)
        self.C2.horizontalHeader().hide()
        self.C2.verticalHeader().setEnabled(0)
        self.C2.verticalHeader().hide()
        self.C2.setColumnCount(2)
        self.C2.setColumnWidth(0, 330)
        self.C2.setColumnWidth(1, 48)
        self.C2.setSortingEnabled(0)

        self.cf = self.paletteField(self.lexBox)
        self.cf.setGeometry(15, 338, 380, 36)
        self.cf.setObjectName('Cross_ref')

        self.Clear.setToolTip("clear all fields")
        self.Del.setToolTip("delete selection")
        self.Add.setToolTip("add new grammatical information\n or alternative form (select field to edit)")
        self.grammar.setToolTip("grammatical information, abbreviations for grammatical \n"
                                "categories can be placed in the first column on the left, \n"
                                "dialects can be specified in the rightmost column.")
        self.C2.setToolTip("alternative forms not in dictionary, dialects\n"
                           "can be specified in the righthand column.")
        self.cf.setToolTip("other related entries")
        self.gSound = SoundPanel(self)
        self.gSound.setGeometry(10, 391, 146, 77)
        self.gSound.setEnabled(0)
        self.cf.setFocus()

        if dataIndex.unsavedEdit == 1:
            self.prevEdit = 1
        else:
            self.prevEdit = 0
        dataIndex.unsavedEdit = 0

    def updateXML(self):
        """updates XML and grammar field on lex card"""
        self.grammar.sortItems(1, QtCore.Qt.SortOrder.AscendingOrder)
        self.grammar.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
        #        fieldContents = ''
        """build a new set of <Grm>, <C2>, and <Cf> nodes"""
        child = dataIndex.lexDict[dataIndex.currentCard]
        """remove old elments"""
        killList = []
        for node in child.iter('Grm'):
            killList.append(node)
        for item in killList:
            child.remove(item)
        killList = []
        for node in child.iter('C2'):
            killList.append(node)
        for item in killList:
            child.remove(item)
        killList = []
        for node in child.iter('Cf'):
            killList.append(node)
        for item in killList:
            child.remove(item)
        """build the new nodes"""
        if child.find('IPA') is not None:
            k = child.find('IPA')
            index = list(child).index(k) + 1
        elif child.find('POS') is not None:
            k = child.find('POS')
            index = list(child).index(k) + 1
        else:
            k = child.find('Orth')
            index = list(child).index(k) + 1
        refList = []
        altList = []
        """add grm nodes"""
        for i in range(0, self.grammar.rowCount()):
            if self.grammar.item(i, 0) is None:
                break
            if not self.grammar.item(i, 1):
                break
            if self.grammar.item(i, 1).text() == 'new item':
                break
            newGrm = etree.Element('Grm')
            newGrm.text = self.grammar.item(i, 1).text()
            """get a prefix/grammatical category"""
            if len(self.grammar.item(i, 0).text()) != 0:
                if len(self.grammar.item(i, 1).text()) == 0:
                    self.grammar.item(i, 1).setText(' ')
                prefix = self.grammar.item(i, 0).text()
                if prefix[-1] == ".":
                    prefix = prefix[:-1]
                newGrm.set("Prefix", prefix)
            #                fieldContents += "<i>" + prefix + ".</i> "
            if self.grammar.item(i, 0).data(35) is not None:
                newGrm.set("MediaRef", self.grammar.item(i, 0).data(35))
                refList.append(self.grammar.item(i, 0).data(35))
                altList.append(self.grammar.item(i, 1).text())
            """get a dialect designation"""
            try:
                if len(self.grammar.item(i, 2).text()) != 0:
                    dialect = self.grammar.item(i, 2).text()
                    newGrm.set("Variant", dialect)
            except AttributeError:
                pass
            child.insert(index, newGrm)
            index += 1
        """add C2 nodes"""
        for i in range(0, self.C2.rowCount()):
            if self.C2.item(i, 0) is None:
                break
            if not self.C2.item(i, 0):
                break
            if self.C2.item(i, 0).text() == 'new item':
                break
            if len(self.C2.item(i, 0).text()) == 0:
                break
            try:
                if len(self.C2.item(i, 1).text()) != 0:
                    dialect = self.C2.item(i, 1).text()
                else:
                    dialect = None
            except AttributeError:
                dialect = None
            newC2 = etree.Element('C2')
            newC2.text = self.C2.item(i, 0).text()
            if self.C2.item(i, 0).data(35) is not None:
                newC2.set("MediaRef", self.C2.item(i, 0).data(35))
                refList.append(self.C2.item(i, 0).data(35))
                altList.append(self.C2.item(i, 0).text())
            if dialect is not None:
                newC2.set("Variant", dialect)
            child.insert(index, newC2)
            index += 1
        """add Cf Nodes"""
        if len(self.cf.toPlainText()) != 0:
            CfInfo = self.cf.toPlainText()
            CfElems = CfInfo.split(', ')
            for item in CfElems:
                newCross = etree.Element('Cf')
                newCross.text = item
                crossRef = None
                for entry in dataIndex.root.findall('Lex'):
                    lexeme = entry.find('Orth').text
                    if lexeme == item and entry.attrib.get('Hom') is not None:
                        """TODO: fix so you see definitions with alternatives"""
                        synList = entry.attrib.get('Hom').split(", ")
                        newCf = CrossRefManager.Dialog(self)
                        newCf.setRefs(synList)
                        if newCf.exec():
                            crossRef = newCf.getRef()
                        else:
                            crossRef = None
                        break
                    elif lexeme == item:
                        crossRef = entry.attrib.get('LexID')
                        break
                if crossRef is not None:
                    newCross.set("CrossRef", crossRef)
                    refList.append(crossRef)
                    altList.append(item)
                child.insert(index, newCross)
                index += 1
        cardLoader.loadLexCard(child)
        if len(refList) != 0:
            field = 'lGrammar'
            contextMenus.buildContextMenu(self.fldbk, field, refList, altList)
        else:
            try:
                del self.fldbk.lGrammar.crossrefMenu
            except AttributeError:
                pass

    def setValues(self, currentCard):
        """fills in the tables and fields with the initial values"""
        self.grammar.clear()
        self.C2.clear()
        node = dataIndex.lexDict[currentCard]
        grmList = node.findall('Grm')
        C2List = node.findall('C2')
        CfList = node.findall('Cf')
        if len(grmList) != 0:
            self.grammar.setRowCount(len(grmList))
            for i in range(0, len(grmList)):
                try:
                    prefix = grmList[i].attrib.get('Prefix')
                    if prefix[-1] == ".":
                        prefix = prefix[:-1]
                except (AttributeError, TypeError):
                    prefix = None
                try:
                    mediaRef = grmList[i].attrib.get('MediaRef')
                except AttributeError:
                    mediaRef = None
                try:
                    dialect = grmList[i].attrib.get('Variant')
                except AttributeError:
                    dialect = None
                datum = grmList[i].text
                newItem = QtWidgets.QTableWidgetItem(1001)
                if prefix is not None:
                    newItem.setText(prefix)
                if mediaRef is not None:
                    newItem.setData(35, mediaRef)
                newItem.setData(36, grmList[i])
                self.grammar.setItem(i, 0, newItem)
                nextItem = QtWidgets.QTableWidgetItem(1001)
                nextItem.setText(datum)
                self.grammar.setItem(i, 1, nextItem)
                if dialect is not None:
                    lastItem = QtWidgets.QTableWidgetItem(1001)
                    lastItem.setText(dialect)
                    self.grammar.setItem(i, 2, lastItem)
        else:
            self.grammar.setRowCount(1)
            newItem = QtWidgets.QTableWidgetItem(1001)
            self.grammar.setItem(0, 0, newItem)
            nextItem = QtWidgets.QTableWidgetItem(1001)
            nextItem.setText('new item')
            self.grammar.setItem(0, 1, nextItem)
        if len(C2List) != 0:
            self.C2.setRowCount(len(C2List))
            for i in range(0, len(C2List)):
                try:
                    mediaRef = C2List[i].attrib.get('MediaRef')
                except AttributeError:
                    mediaRef = None
                try:
                    dialect = C2List[i].attrib.get('Variant')
                except AttributeError:
                    dialect = None
                print(dialect)
                datum = C2List[i].text
                newItem = QtWidgets.QTableWidgetItem(1001)
                if mediaRef is not None:
                    newItem.setData(35, mediaRef)
                newItem.setData(36, C2List[i])
                newItem.setText(datum)
                self.C2.setItem(i, 0, newItem)
                if dialect is not None:
                    nextItem = QtWidgets.QTableWidgetItem(1001)
                    nextItem.setText(dialect)
                    self.C2.setItem(i, 1, nextItem)
        else:
            self.C2.setRowCount(1)
            nextItem = QtWidgets.QTableWidgetItem(1001)
            nextItem.setText('new item')
            self.C2.setItem(0, 0, nextItem)
        if len(CfList) != 0:
            textLine = ''
            for item in CfList:
                CfLine = item.text
                if len(textLine) == 0:
                    textLine = CfLine
                else:
                    textLine += ', ' + CfLine
            self.cf.setText(textLine)

    @QtCore.pyqtSlot()
    def on_Del_released(self):
        """
        Slot documentation goes here.
        """
        target = self.whichTable
        if target == 'grammar':
            table = self.grammar
        else:
            table = self.C2
        table.removeRow(table.currentRow())
        dataIndex.unsavedEdit = 1

    @QtCore.pyqtSlot()
    def on_Add_released(self):
        """
        Slot documentation goes here.
        """
        target = self.whichTable
        if target == 'grammar':
            column = 1
            prefixCell = QtWidgets.QTableWidgetItem(1002)
            table = self.grammar
        elif target == 'C2':
            column = 0
            table = self.C2
        else:
            pass
        tableCell = QtWidgets.QTableWidgetItem(1002)
        tableCell.setText('new item')
        i = table.rowCount()
        table.insertRow(i)
        table.setItem(i, column, tableCell)
        if target == 'grammar':
            table.setItem(i, 0, prefixCell)
        table.resizeRowToContents(i)
        dataIndex.unsavedEdit = 1

    @QtCore.pyqtSlot()
    def on_Clear_pressed(self):
        """
        Slot documentation goes here.
        """
        self.C2.clear()
        self.cf.clear()
        self.grammar.clear()
        self.Del.setEnabled(0)
        self.Add.setEnabled(1)

    @QtCore.pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        self.grammar.endEdit()
        self.C2.endEdit()
        if dataIndex.unsavedEdit == 1:
            self.updateXML()
        if self.prevEdit == 1:
            dataIndex.unsavedEdit = 1
        self.accept()

    @QtCore.pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        if self.prevEdit == 0:
            dataIndex.unsavedEdit = 0
        else:
            dataIndex.unsavedEdit = 1
        self.reject()
