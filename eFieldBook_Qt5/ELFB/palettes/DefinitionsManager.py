from PyQt6 import QtWidgets, QtCore, QtGui
from copy import deepcopy
from xml.etree import ElementTree as etree
import re
from ELFB.palettes import CrossRefManager, AddEgDialog
from ELFB import HTMLDelegate, dataIndex, cardLoader, formattingHandlers

from .Ui_DefinitionsManager import Ui_Dialog


class DefinitionsManager(QtWidgets.QDialog, Ui_Dialog):
    """class for constraining user input to lexicon def fields"""

    class FocusOutFilter(QtCore.QObject):
        def __init__(self, parent):
            super(DefinitionsManager.FocusOutFilter, self).__init__(parent)

        def eventFilter(self, sender, event):
            if event.type() == QtCore.QEvent.Type.FocusOut:
                try:
                    sender.clearSelection()
                except AttributeError:
                    pass
            if event.type() == QtCore.QEvent.Type.Leave:
                parent = sender.parent()
                while parent.parent() is not None:
                    parent = parent.parent()
                    if parent.objectName() == 'DefinitionsManager':
                        break
                if parent.currentSubentry != 0:
                    parent.XmlUpdater()

            return False

    class paletteField(QtWidgets.QTextEdit):
        def __init__(self, parent):
            super(DefinitionsManager.paletteField, self).__init__(parent)
            self.filter = DefinitionsManager.FocusOutFilter(self)
            self.installEventFilter(self.filter)
            self.textChanged.connect(self.flagUnsavedEdits)

        def flagUnsavedEdits(field):
            fManager = field
            palette = fManager.parent()
            while palette.parent() is not None:
                palette = palette.parent()
                if palette.objectName() == 'DefinitionsManager':
                    break
            palette.unsavedEdit = 1

    class L1Field(paletteField):
        def __init__(self, parent):
            super(DefinitionsManager.L1Field, self).__init__(parent)
            self.textChanged.connect(self.activateAddButton)

        def activateAddButton(text):
            """enables the add new subenty button"""
            fManager = text.parent()
            palette = fManager.parent()
            while palette.parent() is not None:
                if palette.parent().objectName() == 'Fieldbook':
                    break
                else:
                    palette = palette.parent()
            if len(palette.L1.toPlainText()) == 1:
                palette.New.setEnabled(1)
                palette.Clear.setEnabled(1)
            elif len(palette.L1.toPlainText()) == 0:
                palette.Clear.setDisabled(1)

    class lexTable(QtWidgets.QTableWidget):
        def __init__(self, parent):
            super(DefinitionsManager.lexTable, self).__init__(parent)
            self.setStyleSheet("selection-background-color: #F0F0F0;")
            delegate = HTMLDelegate.HTMLDelegate()
            self.setItemDelegate(delegate)
            self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.SelectedClicked)

    class exTable(lexTable):
        def __init__(self, parent):
            super(DefinitionsManager.exTable, self).__init__(parent)
            self.cellClicked.connect(self.activateMinusEg)

        def activateMinusEg(self):
            fManager = self.parent().parent().parent()
            fManager.minusEgBtn.setEnabled(1)
            fManager.switchEgBtn.setEnabled(1)

    def __init__(self, parent):
        super(DefinitionsManager, self).__init__(parent)
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        italics = QtGui.QAction(self)
        self.addAction(italics)
        italics.setShortcut(QtGui.QKeySequence.StandardKey.Italic)
        italics.triggered.connect(self.italics)
        underline = QtGui.QAction(self)
        self.addAction(underline)
        underline.setShortcut(QtGui.QKeySequence.StandardKey.Underline)
        underline.triggered.connect(self.underline)
        bold = QtGui.QAction(self)
        self.addAction(bold)
        bold.setShortcut(QtGui.QKeySequence.StandardKey.Bold)
        bold.triggered.connect(self.bold)
        normal = QtGui.QAction(self)
        self.addAction(normal)
        normal.setShortcut(QtGui.QKeySequence("Ctrl+Shift+I"))
        normal.triggered.connect(self.normal)

        self.fldbk = dataIndex.fldbk
        self.unsavedEdit = 0
        child = dataIndex.lexDict[dataIndex.currentCard]
        self.child = child
        self.workingCopy = deepcopy(child)
        if child.find('Def/L1').text is None:
            dataIndex.unsavedEdit == 1
        else:
            dataIndex.unsavedEdit = 0
        self.currentCell = []
        self.currentSubentry = 0
        self.setObjectName("DefinitionsManager")
        self.orderEntries.setDisabled(1)
        self.Clear.setDisabled(1)
        self.Kill.setDisabled(1)
        self.New.setEnabled(1)
        self.Update.setDisabled(1)
        self.addEgBtn.setDisabled(1)
        self.minusEgBtn.setDisabled(1)
        self.switchEgBtn.setDisabled(1)

        self.POS = self.paletteField(self.diaBox)
        self.POS.setGeometry(QtCore.QRect(80, 10, 144, 25))
        self.POS.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.POS.setObjectName("POS")
        self.POS.setToolTip(QtWidgets.QApplication.translate("DefinitionsManager",
                                                             "part of speech (if different <br />for this subentry)",
                                                             None))

        self.Reg = self.paletteField(self.diaBox)
        self.Reg.setGeometry(QtCore.QRect(338, 10, 144, 25))
        self.Reg.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Reg.setObjectName("Reg")
        self.Reg.setToolTip(
            QtWidgets.QApplication.translate("DefinitionsManager", "register (if specific <br />to this subentry)",
                                             None))

        self.Dia = self.paletteField(self.diaBox)
        self.Dia.setGeometry(QtCore.QRect(80, 48, 144, 25))
        self.Dia.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Dia.setObjectName("Dia")
        self.Dia.setToolTip(
            QtWidgets.QApplication.translate("DefinitionsManager", "dialect (if specific <br />to this subentry)",
                                             None))

        self.Alternative = self.paletteField(self.diaBox)
        self.Alternative.setGeometry(QtCore.QRect(338, 48, 144, 25))
        self.Alternative.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Alternative.setObjectName("Alternative")
        self.Alternative.setToolTip(
            QtWidgets.QApplication.translate("DefinitionsManager", "alternative form in other dialects.<br /> "
                                                                   "Use the format: US. soda. Separate <br />multiple entries with a semi-colon.",
                                             None))

        self.L1Index = self.paletteField(self.diaBox)
        self.L1Index.setGeometry(QtCore.QRect(80, 86, 144, 25))
        self.L1Index.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.L1Index.setObjectName("L1Index")
        self.L1Index.setToolTip(
            QtWidgets.QApplication.translate("DefinitionsManager", "primary language index terms", None))

        self.L2Index = self.paletteField(self.diaBox)
        self.L2Index.setGeometry(QtCore.QRect(338, 86, 144, 25))
        self.L2Index.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.L2Index.setObjectName("L2Index")
        self.L2Index.setToolTip(
            QtWidgets.QApplication.translate("DefinitionsManager", "secondary language index", None))

        self.Primary = QtWidgets.QLabel(self.fieldBox)
        self.Primary.setGeometry(QtCore.QRect(10, 167, 59, 24))
        self.Primary.setObjectName("Primary")
        self.L1 = self.L1Field(self.fieldBox)
        self.L1.setGeometry(QtCore.QRect(90, 153, 410, 70))
        self.L1.setObjectName("L1")
        self.L1.setToolTip(
            QtWidgets.QApplication.translate("DefinitionsManager", "definition in primary working language", None))

        self.L2 = self.paletteField(self.fieldBox)
        self.L2.setGeometry(QtCore.QRect(90, 233, 410, 70))
        self.L2.setObjectName("L2")
        self.L2.setToolTip(
            QtWidgets.QApplication.translate("DefinitionsManager", "definition in secondary working language", None))

        self.Context = self.paletteField(self.fieldBox)
        self.Context.setGeometry(QtCore.QRect(90, 310, 410, 70))
        self.Context.setObjectName("L2")
        self.Context.setToolTip(QtWidgets.QApplication.translate("DefinitionsManager", "context and usage notes", None))

        self.LnBox = QtWidgets.QScrollArea(self.fieldBox)
        self.LnBox.setGeometry(QtCore.QRect(90, 393, 410, 140))
        self.LnBox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.LnBox.setObjectName("LnBox")
        self.Ln = self.exTable(self.LnBox)
        self.Ln.setGeometry(QtCore.QRect(0, 0, 410, 140))
        self.Ln.setRowCount(0)
        self.Ln.horizontalHeader().setEnabled(0)
        self.Ln.horizontalHeader().hide()
        self.Ln.verticalHeader().setEnabled(0)
        self.Ln.verticalHeader().hide()
        self.Ln.setColumnCount(1)
        self.Ln.setColumnWidth(0, 410)
        self.Ln.setSortingEnabled(0)
        self.Ln.setObjectName("Ln")

        self.table = self.lexTable(self.lexBox)
        self.table.setGeometry(8, 8, 450, 532)
        self.table.setRowCount(1)
        self.table.horizontalHeader().setEnabled(0)
        self.table.horizontalHeader().hide()
        self.table.setColumnCount(1)
        self.table.setColumnWidth(0, 450)
        self.table.setSortingEnabled(0)
        self.table.setObjectName("subTable")
        self.table.cellClicked.connect(self.fillForm)
        self.fillTable(child)

    def italics(self):
        """
        toggle italic typeface in textEdits.
        """
        field = QtGui.QGuiApplication.focusObject()
        if field.metaObject().className() == 'paletteField' or field.metaObject().className() == 'L1Field':
            state = field.fontItalic()
            field.setFontItalic(not state)

    def underline(self):
        """
        toggle underline typeface in textEdits.
        """
        field = QtGui.QGuiApplication.focusObject()
        if field.metaObject().className() == 'paletteField' or field.metaObject().className() == 'L1Field':
            state = field.fontUnderline()
            field.setFontUnderline(not state)

    def bold(self):
        """
        toggle bold typeface in textEdits.
        """
        field = QtGui.QGuiApplication.focusObject()
        if field.metaObject().className() == 'paletteField' or field.metaObject().className() == 'L1Field':
            if field.fontWeight() == QtGui.QFont.Weight.Bold:
                field.setFontWeight(QtGui.QFont.Weight.Normal)
            else:
                field.setFontWeight(QtGui.QFont.Weight.Bold)

    def normal(self):
        """
        remove formatting in textEdits.
        """
        field = QtGui.QGuiApplication.focusObject()
        if field.metaObject().className() == 'paletteField' or field.metaObject().className() == 'L1Field':
            field.setFontUnderline(0)
            field.setFontItalic(0)
            field.setFontWeight(QtGui.QFont.Weight.Normal)

    def fillForm(self, row, column):
        """fills in the fields with data from the subentry selected in the table list"""
        self.POS.clear()
        self.Reg.clear()
        self.Dia.clear()
        self.Alternative.clear()
        self.L1.clear()
        self.L2.clear()
        self.Ln.clear()
        self.Context.clear()
        thisRow = self.table.item(row, column)
        self.currentCell = thisRow
        L1Text = thisRow.data(35).findtext('L1')
        L1Text = formattingHandlers.XMLtoRTF(L1Text)
        self.L1.setHtml(L1Text)
        if thisRow.data(35).findtext('L2'):
            L2Text = thisRow.data(35).findtext('L2')
            L2Text = formattingHandlers.XMLtoRTF(L2Text)
            self.L2.setHtml(L2Text)
        if thisRow.data(35).findtext('Cxt'):
            CxtText = thisRow.data(35).findtext('Cxt')
            CxtText = formattingHandlers.XMLtoRTF(CxtText)
            self.Context.setHtml(CxtText)
        n = self.table.rowCount()
        self.orderEntries.setMaximum(n)
        self.orderEntries.setMinimum(1)
        self.orderEntries.setEnabled(1)
        self.currentSubentry = int(thisRow.data(35).attrib.get('Index'))
        self.orderEntries.setValue(int(thisRow.data(35).attrib.get('Index')))
        try:
            L1Index = thisRow.data(35).attrib.get('L1Index')
            self.L1Index.setHtml(L1Index)
        except AttributeError:
            self.L1Index.clear()
        try:
            L2Index = thisRow.data(35).attrib.get('L2Index')
            self.L2Index.setHtml(L2Index)
        except AttributeError:
            self.L2Index.clear()
        self.currentSubentry = self.orderEntries.value()
        if thisRow.data(35).findtext('POS'):
            self.POS.setHtml(thisRow.data(35).findtext('POS'))
        else:
            self.POS.clear()
        if thisRow.data(35).findtext('Reg'):
            self.Reg.setHtml(thisRow.data(35).findtext('Reg'))
        else:
            self.Reg.clear()
        dNode = thisRow.data(35).find('Dia')
        try:
            dialect = dNode.attrib.get('Dialect')
            self.Dia.setHtml(dialect)
            if dNode.find('Alternative') is not None:
                aNodeList = dNode.findall('Alternative')
                j = 0
                for aNode in aNodeList:
                    variant = " " + aNode.attrib.get('Variant')
                    alternative = " " + aNode.text
                    if j == 0:
                        entry = variant + alternative
                    else:
                        entry = entry + "; " + variant + alternative
                    j += 1
                self.Alternative.setHtml(entry)
        except AttributeError:
            self.Dia.clear()
            self.Alternative.clear()

        examples = thisRow.data(35).findall('Ln')
        if examples:
            self.Ln.setRowCount(len(examples))
            for j in range(0, len(examples)):
                egID = examples[j].attrib.get('LnRef')
                egElement = dataIndex.exDict[egID]
                eg = '<i>' + egElement.findtext('Line') + '</i>'
                if len(egElement.findtext('L1Gloss')) != 0:
                    eg = eg + " ‘" + egElement.findtext('L1Gloss') + "’ ("
                elif egElement.findtext == None:
                    eg = eg + " ‘" + egElement.findtext('L2Gloss') + "’ ("
                else:
                    eg = eg + " ‘" + '[UNGLOSSED]' + "’ ("
                eg = eg + egElement.attrib.get('Spkr') + ")"
                eg = re.sub('{i}', '', eg)
                eg = re.sub('{/i}', '', eg)
                tableCell = QtWidgets.QTableWidgetItem(1002)
                tableCell.setTextAlignment(QtCore.Qt.TextFlag.TextWordWrap)
                tableCell.setText(eg)
                tableCell.setData(36, egID)
                self.Ln.setItem(j, 0, tableCell)
                self.Ln.resizeRowToContents(j)
        else:
            self.Ln.clear()

        a = self.Ln.selectedRanges()
        if len(a) != 0:
            self.Ln.setRangeSelected(a[0], 0)

        self.Kill.setEnabled(1)
        self.Update.setEnabled(1)
        self.Clear.setEnabled(1)
        self.addEgBtn.setEnabled(1)
        self.minusEgBtn.setDisabled(1)
        self.switchEgBtn.setDisabled(1)

    def fillTable(self, child):
        """updates table with list of subentries"""
        subentry = child.findall('Def')
        howMany = len(subentry)
        self.table.setRowCount(howMany)
        for i in range(0, len(subentry)):
            entry = ''
            dialect = ''
            variant = ''
            alternative = ''
            POS = subentry[i].findtext('POS')
            if POS:
                entry = "(" + POS + ") "
            dNode = subentry[i].find('Dia')
            if dNode is not None:
                dialect = dNode.attrib.get('Dialect')
                entry = entry + " <i>" + dialect + "</i> "
                aNodeList = dNode.findall('Alternative')
                if len(aNodeList) != 0:
                    j = 0
                    for aNode in aNodeList:
                        variant = aNode.attrib.get('Variant')
                        alternative = aNode.text
                        if j == 0 and len(aNodeList) - 1 == 0:
                            entry = entry + "[" + variant + " " + alternative + "] "
                        elif j == 0:
                            entry = entry + "[" + variant + " " + alternative
                        elif j == len(aNodeList) - 1:
                            entry = entry + "; " + variant + " " + alternative + "] "
                        else:
                            entry = entry + "; " + variant + " " + alternative
                        j += 1

            Reg = subentry[i].findtext('Reg')
            if Reg:
                entry = entry + "<i>" + Reg + "</i> "
            entry = entry + subentry[i].findtext('L1')
            entry = formattingHandlers.XMLtoRTF(entry)

            tableCell = QtWidgets.QTableWidgetItem(1002)
            tableCell.setData(35, subentry[i])
            tableCell.setText(entry)
            tableCell.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.table.setItem(i, 0, tableCell)
            self.table.resizeRowToContents(i)

    def updateLexCard(self, child):
        cardLoader.loadDefinitions(dataIndex.fldbk, child)
        self.unsavedEdit = 1

    def makeFormatBox(self):
        self.formatBox = QtWidgets.QMessageBox()
        self.formatBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        self.formatBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
        self.formatBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        self.formatBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        self.formatBox.setText('Formatting error.')
        self.formatBox.setInformativeText('The Alternative field must have both<br />'
                                          'the abbreviated variant name and the <br />'
                                          'alternative form, as in:'
                                          '<blockquote><big>US soda</big></blockquote><br />'
                                          'Separate multiple entries with a semi-colon.')
        self.formatBox.exec()

    def newNodeBuilder(self, child, defIndex, upDateDef):
        """##insert new <Def> in <Lex> at index upDateDef"""
        child.insert(upDateDef, etree.Element('Def', {'Index': defIndex}))
        optIndex = 0

        """##insert new POS"""
        if len(self.POS.toPlainText()) != 0:
            newPOS = etree.SubElement(child[upDateDef], 'POS')
            newPOS.text = self.POS.toPlainText()
            optIndex += 1

        """##insert new Reg"""
        if len(self.Reg.toPlainText()) != 0:
            newReg = etree.SubElement(child[upDateDef], 'Reg')
            newReg.text = self.Reg.toPlainText()
            optIndex += 1

        """##insert new Dia"""
        if len(self.Dia.toPlainText()) != 0:
            crossRef = None
            dialect = self.Dia.toPlainText()
            etree.SubElement(child[upDateDef], 'Dia', {'Dialect': dialect})
            if len(self.Alternative.toPlainText()) != 0:
                """##should probably check to ensure that there is a dialect specified and warn user if not##"""
                altList = self.Alternative.toPlainText().split("; ")
                for item in altList:
                    alternative = item.split(None, 1)
                    if len(alternative) == 1:
                        self.makeFormatBox()
                        return
                    variant = alternative[0]
                    if variant.endswith('.') is False:
                        variant += '.'
                    for item2 in dataIndex.root.iter('Lex'):
                        lexeme = item2.find('Orth').text
                        if lexeme == alternative[1] and item2.attrib.get('Hom') is not None:
                            # TODO fix so you see defnitions with alternatives
                            synList = item2.attrib.get('Hom').split(", ")
                            synList.append(item2.attrib.get('LexID'))
                            newCf = CrossRefManager.Dialog(self)
                            newCf.setRefs(synList)
                            if newCf.exec():
                                crossRef = newCf.getRef()
                            else:
                                crossRef = None
                            break
                        elif lexeme == alternative[1]:
                            crossRef = item2.attrib.get('LexID')
                            break
                    if crossRef is not None:
                        newAlt = etree.SubElement(child[upDateDef][optIndex], 'Alternative',
                                                  {'Variant': variant, 'CrossRef': crossRef})
                    else:
                        newAlt = etree.SubElement(child[upDateDef][optIndex], 'Alternative', {'Variant': variant})
                    newAlt.text = alternative[1]

        """insert new indices"""
        if len(self.L1Index.toPlainText()) != 0:
            L1Index = self.L1Index.toPlainText()
            child[upDateDef].set('L1Index', L1Index)
        if len(self.L2Index.toPlainText()) != 0:
            L2Index = self.L2Index.toPlainText()
            child[upDateDef].set('L2Index', L2Index)

        """insert new L1"""
        newL1 = etree.SubElement(child[upDateDef], 'L1')
        html = self.L1.toHtml()
        newHtml = formattingHandlers.textStyleHandler(html)
        self.L1.setHtml(newHtml)
        plain = self.L1.toPlainText()
        self.L1.setHtml(html)
        newL1.text = plain

        """insert new L2"""
        """Note that this creates an empty L2 node for all entries"""
        newL2 = etree.SubElement(child[upDateDef], 'L2')
        if len(self.L2.toPlainText()) != 0:
            html = self.L2.toHtml()
            newHtml = formattingHandlers.textStyleHandler(html)
            self.L2.setHtml(newHtml)
            plain = self.L2.toPlainText()
            self.L2.setHtml(html)
            newL2.text = plain
        else:
            newL2.text = ''

        """##insert new <Cxt> node"""
        if len(self.Context.toPlainText()) != 0:
            newContext = etree.SubElement(child[upDateDef], 'Cxt')
            html = self.Context.toHtml()
            newHtml = formattingHandlers.textStyleHandler(html)
            self.Context.setHtml(newHtml)
            plain = self.Context.toPlainText()
            self.Context.setHtml(html)
            newContext.text = plain

        """##insert new <Ln> nodes"""
        try:
            for i in range(0, self.Ln.rowCount()):
                number = self.Ln.item(i, 0).data(36)
                etree.SubElement(child[upDateDef], 'Ln', {'LnRef': number})
        except AttributeError:
            pass

    def XmlUpdater(self):
        child = self.workingCopy
        pointer = 0
        if self.orderEntries.value() == 0:
            toUpdate = self.orderEntries.value()
        else:
            toUpdate = self.orderEntries.value() - 1  # gets ordinal for subentry
        elemList = list(child)
        for i in range(0, len(elemList)):
            if elemList[i].tag == 'Def':
                pointer = i
                break
        upDateDef = toUpdate + pointer
        defIndex = str(toUpdate + 1)
        oldDef = elemList[upDateDef]
        child.remove(oldDef)
        self.newNodeBuilder(child, defIndex, upDateDef)
        """##update table on palette"""
        self.fillTable(child)

    def updateDatabase(self):
        child = self.workingCopy
        """##update XML"""
        dataIndex.lexDict[child.attrib.get('LexID')] = child
        """##update lex card"""
        self.updateLexCard(child)
        """##update XML tree"""
        for node in dataIndex.root.iter('Lex'):
            if node.attrib.get('LexID') == dataIndex.currentCard:
                i = list(dataIndex.root).index(node)
                dataIndex.root.remove(node)
                dataIndex.root.insert(i, child)
                break
        self.unsavedEdit = 0

    def clearAll(self):
        self.POS.clear()
        self.Reg.clear()
        self.Dia.clear()
        self.Alternative.clear()
        self.L1.clear()
        self.L2.clear()
        self.Ln.clear()
        self.Context.clear()
        self.orderEntries.setMinimum(0)
        self.orderEntries.setValue(0)
        self.currentSubentry = 0
        self.Kill.setDisabled(1)
        self.Update.setDisabled(1)
        self.Clear.setDisabled(1)
        self.addEgBtn.setDisabled(1)
        self.minusEgBtn.setDisabled(1)
        self.switchEgBtn.setDisabled(1)
        self.orderEntries.setDisabled(1)
        self.New.setEnabled(1)

    @QtCore.pyqtSlot()
    def on_Clear_released(self):
        """
        Clear all fields.
        """
        self.clearAll()

    @QtCore.pyqtSlot()
    def on_Kill_released(self):
        """
        remove selected subentry
        """
        if len(self.L1.toPlainText()) == 0:
            return
        toUpdate = self.orderEntries.value() - 1  # gets ordinal for subentry
        child = self.workingCopy
        elemList = list(child)
        for i in range(0, len(elemList)):
            if elemList[i].tag == 'Def':
                pointer = i
                break
        badDef = toUpdate + pointer
        badNode = elemList[badDef]
        child.remove(badNode)
        number = 0
        for Def in child.iter('Def'):
            number += 1
            Def.set('Index', str(number))
        self.orderEntries.setMinimum(0)
        self.orderEntries.setValue(0)
        self.orderEntries.setMaximum(self.orderEntries.maximum() - 1)
        """##clear fields"""
        self.clearAll()
        self.unsavedEdit = 1
        """##update table on palette"""
        self.fillTable(child)

    @QtCore.pyqtSlot()
    def on_New_released(self):
        """
        Add a new subentry to definition.
        """
        child = self.workingCopy

        """clear current entry (to avoid mixing)"""
        self.clearAll()
        self.Ln.clear()

        """remove an empty subentry (not sure why we need this?)"""
        if child.find('Def/L1').text is None:
            badNode = child.find('Def')
            child.remove(badNode)
            numSubs = 0
        else:
            numSubs = self.table.rowCount()  # gets ordinal for subentry
        """defIndex will be the Index attribute of <Def> (i.e., subentry number)"""
        defIndex = str(numSubs + 1)

        """pointer gets an index for the location of the new sub-entry"""
        firstDef = child.find('Def')
        pointer = list(child).index(firstDef)
        for item in child.findall('Def'):
            pointer += 1

        self.newNodeBuilder(child, defIndex, pointer)
        self.unsavedEdit = 1

        """update table on palette and activate spinbox"""
        self.fillTable(child)
        n = self.table.rowCount()
        self.orderEntries.setMaximum(n)
        n -= 1
        thisRow = self.table.item(n, 0)
        self.orderEntries.setValue(int(thisRow.data(35).attrib.get('Index')))
        self.currentSubentry = self.orderEntries.value()
        self.orderEntries.setEnabled(1)
        self.Update.setEnabled(1)

    @QtCore.pyqtSlot()
    def on_Update_released(self):
        """
        Update the XML database.
        """
        #        self.XmlUpdater()
        self.updateDatabase()
        dataIndex.unsavedEdit = 1

    @QtCore.pyqtSlot()
    def on_CancelBtn_released(self):
        """
        Close without saving.
        """
        self.reject()

    @QtCore.pyqtSlot()
    def on_OkayBtn_released(self):
        """
        Update XML and close.
        """
        if self.unsavedEdit == 1:
            #            self.XmlUpdater()
            self.updateDatabase()
            dataIndex.unsavedEdit = 1
        self.accept()

    @QtCore.pyqtSlot()
    def on_addEgBtn_released(self):
        """
        Attach example to selected subentry.
        """
        if self.orderEntries.value() == 0:
            return
        addEgDialog = AddEgDialog.AddEgDialog(self)
        if addEgDialog.exec():
            newExRef = addEgDialog.validateID()
            if newExRef is False:
                QtWidgets.QApplication.beep()
                return
            newElement = '<Ln LnRef="' + newExRef + '" />'
            newEg = etree.XML(newElement)
            exNode = dataIndex.exDict[newExRef]
            links = exNode.attrib.get('Links')
            if links is None or len(links) == 0:
                exNode.set('Links', self.child.attrib.get('LexID'))
            else:
                linksList = links.split(', ')
                if len(linksList) != 1:
                    links += ', ' + self.child.attrib.get('LexID')
                exNode.set('Links', links)
        else:
            return
        child = self.workingCopy
        defNode = ''
        for node in child.iter('Def'):
            if node.attrib.get('Index') == str(self.currentSubentry):
                defNode = node
                break
        numberOfElements = len(list(defNode))
        defNode.insert(numberOfElements, newEg)

        # update Ln table
        j = self.currentSubentry - 1
        self.table.item(j, 0).setData(35, defNode)
        self.fillForm(j, 0)

        self.unsavedEdit = 1

    @QtCore.pyqtSlot()
    def on_minusEgBtn_released(self):
        """
        Unlink example from subentry.
        """
        if self.Ln.rowCount() == 0:
            return
        try:
            thisCell = self.Ln.currentRow()
            egIndex = self.Ln.item(thisCell, 0).data(36)
        except AttributeError:
            return
        child = self.workingCopy
        for Def in child.iter('Def'):
            tag = 'Ln[@LnRef="' + egIndex + '"]'
            badEg = Def.find(tag)
            if badEg is not None:
                Def.remove(badEg)
                break
        self.Ln.removeRow(thisCell)
        self.unsavedEdit = 1
        exNode = dataIndex.exDict[egIndex]
        links = exNode.get('Links')
        linksList = links.split(', ')
        try:
            i = linksList.index(dataIndex.currentCard)
            linksList.pop(i)
        except ValueError:
            pass
        if len(linksList) == 1:
            exNode.set('Links', linksList[0])
        elif len(linksList) > 1:
            links = ', '.join(linksList)
            exNode.set('Links', links)
        else:
            del exNode.attrib['Links']
        if self.Ln.rowCount() < 2:
            self.switchEgBtn.setEnabled(1)
        else:
            self.switchEgBtn.setDisabled(1)
        if self.Ln.rowCount() == 0:
            self.minusEgBtn.setDisabled(1)

    @QtCore.pyqtSlot(int)
    def on_orderEntries_valueChanged(self, newValue):
        """
        reorders subentries when spin box is clicked
        
        @param newValue activated index of combBox
        @type int
        """

        if newValue == 0 or self.currentSubentry == 0:
            return
        if newValue == self.currentSubentry:
            return
        """##rearrange XML and renumber Index attrib"""
        child = self.workingCopy
        elemList = list(child)
        for i in range(2, len(elemList)):
            if elemList[i].tag == 'Def':
                firstDef = i
                break
        insertPoint = firstDef + newValue - 1
        def2move = firstDef + self.currentSubentry - 1
        a = child[def2move]
        child.remove(child[def2move])
        child.insert(insertPoint, a)
        if newValue < self.currentSubentry:
            self.currentSubentry -= 1
        elif newValue > self.currentSubentry:
            self.currentSubentry += 1

        index = 0
        for Def in child.iter('Def'):
            index += 1
            Def.set('Index', str(index))

        self.table.setCurrentCell(self.currentSubentry - 1, 0)
        self.unsavedEdit = 1

        """##fix display (self.table)"""
        self.fillTable(child)

    @QtCore.pyqtSlot()
    def on_switchEgBtn_released(self):
        """moves examples to another subentry"""
        self.switchEgDialog = QtWidgets.QInputDialog()
        self.switchEgDialog.setWindowTitle('Select subentry number.')
        self.switchEgDialog.setLabelText('Which subentry would you like<br />to move the example to?')
        if self.switchEgDialog.exec():
            moveTarget = self.switchEgDialog.textValue()
            try:
                eNumber = int(moveTarget)
            except ValueError:
                self.badBox = QtWidgets.QMessageBox()
                self.badBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                self.badBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                self.badBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                self.badBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                self.badBox.setText('Index error.')
                self.badBox.setInformativeText('Enter the number of one of<br />'
                                               'the subentries for this word.')
                self.badBox.exec()
                return
            if eNumber > self.table.rowCount() or eNumber <= 0:
                self.badBox = QtWidgets.QMessageBox()
                self.badBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                self.badBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                self.badBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                self.badBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                self.badBox.setText('Index out of range error.')
                self.badBox.setInformativeText('Enter the number of one of<br />'
                                               'the existing subentries.')
                self.badBox.exec()
                return
            if eNumber == self.orderEntries.value():
                return
        else:
            return

        """##change the XML"""
        currentLoc = self.orderEntries.value() - 1
        ex2Move = self.Ln.currentRow()
        child = self.workingCopy
        elemList = list(child)
        for i in range(2, len(elemList)):
            if elemList[i].tag == 'Def':
                pointer = i
                break
        currentLoc += pointer
        elemList = list(child[currentLoc])
        for i in range(2, len(elemList)):
            if elemList[i].tag == 'Ln':
                pointer2 = i
                break
        ex2Move += pointer2
        transplant = etree.tostring(child[currentLoc][ex2Move], encoding='unicode')
        newEg = etree.XML(transplant)
        child[currentLoc].remove(child[currentLoc][ex2Move])
        newLoc = pointer + eNumber - 1
        elemList = list(child[newLoc])
        insertPoint = len(elemList)
        child[newLoc].insert(insertPoint, newEg)
        self.workingCopy = child

        """##update eg table"""
        thisRow = self.Ln.currentRow()
        self.Ln.removeRow(thisRow)
        self.minusEgBtn.setDisabled(1)
        self.switchEgBtn.setDisabled(1)

        """##update entries in table"""
        self.fillTable(child)

        self.unsavedEdit = 1
