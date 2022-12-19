from PyQt6 import QtWidgets, QtCore
from ELFB import HTMLDelegate, dataIndex, cardLoader, formattingHandlers, codeExtractor
# from xml.etree import ElementTree as etree
from ELFB.palettes import SessionDate

"""class defines the properties of the text field on the text card"""


class focusInFilter(QtCore.QObject):
    def __init__(self, parent):
        super(focusInFilter, self).__init__(parent)
        self.lastContents = None

    def eventFilter(self, sender, event):
        if event.type() == QtCore.QEvent.Type.FocusIn:
            if dataIndex.currentTextTable is not None:
                try:
                    dataIndex.currentTextTable.setStyleSheet("QTableWidget QHeaderView::section {border: 0px;"
                                                             "padding: 5px; outline: 0px; background: white;}")
                    dataIndex.currentTextTable.setFrameStyle(QtWidgets.QFrame.Shape.NoFrame)
                except RuntimeError:
                    pass
            dataIndex.currentTextTable = sender
            sender.setFrameStyle(QtWidgets.QFrame.Shape.Box)
            sender.setStyleSheet("QTableWidget QHeaderView::section {border: 0px;"
                                 "padding: 5px; outline: 0px; background: #E6E6E6;}")
        return False


class TextDelegate(HTMLDelegate.HTMLDelegate):
    def __init__(self, parent):
        super(TextDelegate, self).__init__(parent)
        self.closeEditor.connect(self.updateExample)
        self.fldbk = dataIndex.fldbk

    def updateExample(self):
        dataIndex.unsavedEdit = 1
        update = SessionDate.dateFinder()
        self.fldbk.tUpdated.setPlainText(update)
        ExNode = dataIndex.currentTextTable.verticalHeaderItem(0).data(35)
        LnNode = dataIndex.currentTextTable.verticalHeaderItem(0).data(36)
        timeCode = None
        spokenBy = None
        endTime = None
        if ExNode is not None:
            ExNode.set('Update', update)
            newLine = formattingHandlers.RTFtoXML(dataIndex.currentTextTable.item(0, 0).text())
            ExNode.find('Line').text = newLine
            j = dataIndex.currentTextTable.rowCount() - 1
            glossLine = formattingHandlers.RTFtoXML(dataIndex.currentTextTable.item(j, 0).text())
            spokenBy, glossLine = codeExtractor.getSpokenBy(glossLine)
            if spokenBy is not None:
                LnNode.set('SpokenBy', spokenBy)
            if '[' in glossLine:  # check to see if timeCode is contained in the gloss
                timeCode, endTime, glossLine = codeExtractor.getTime(glossLine)
            if timeCode is not None:
                LnNode.set('Time', timeCode)
            if endTime is not None:
                LnNode.set('EndTime', endTime)
            glossLine = glossLine[1:-1]
            if dataIndex.glossingLanguage == 'L1Gloss':
                ExNode.find('L1Gloss').text = glossLine
            else:
                ExNode.find('L2Gloss').text = glossLine
            if dataIndex.currentTextTable.rowCount() > 2:
                for r in range(1, 3):
                    string = ''
                    for c in range(0, dataIndex.currentTextTable.columnCount()):
                        try:
                            itemText = dataIndex.currentTextTable.item(r, c).text()
                        except AttributeError:
                            itemText = ''
                        if len(string) == 0:
                            string = itemText
                        else:
                            string = string + "\t" + itemText
                    if r == 1:
                        ExNode.find('Mrph').text = string
                    elif r == 2:
                        ExNode.find('ILEG').text = formattingHandlers.RTFtoXML(string)
                dataIndex.currentTextTable.resizeColumns()
            else:
                dataIndex.currentTextTable.resizeColumnsToContents()
        else:
            if dataIndex.currentTextTable.rowCount() == 2:
                # don't forget to extract the speaker code
                gloss = dataIndex.currentTextTable.item(1, 0).text()
                spokenBy, gloss = codeExtractor.getSpokenBy(gloss)
                if '[' in gloss:  # check to see if timeCode is contained in the gloss
                    timeCode, endTime, gloss = codeExtractor.getTime(gloss)
                gloss = gloss.replace('‘', '')
                gloss = gloss.replace('’', '')
                newText = dataIndex.currentTextTable.item(0, 0).text() + '\n' + gloss.strip()
            else:
                newText = dataIndex.currentTextTable.item(0, 0).text()
            LnNode.text = newText
            if spokenBy is not None:
                LnNode.set('SpokenBy', spokenBy)
            if timeCode is not None:
                LnNode.set('Time', timeCode)
            if endTime is not None:
                LnNode.set('EndTime', endTime)


class textTable(QtWidgets.QTableWidget):

    def __init__(self, parent):
        super(textTable, self).__init__(parent)
        self.filter = focusInFilter(self)
        self.installEventFilter(self.filter)
        self.SelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setStyleSheet("selection-background-color: #E6E6E6;")
        self.delegate = TextDelegate(self)
        self.setItemDelegate(self.delegate)
        self.horizontalHeader().setEnabled(0)
        self.verticalHeader().setEnabled(1)
        self.verticalHeader().show()
        self.horizontalHeader().hide()
        self.verticalHeader().sectionClicked.connect(self.headerClicked)
        self.setStyleSheet("QTableWidget QHeaderView::section {border: 0px;"
                           "padding: 5px; outline: 0px; background: white;}"
                           "QTableWidget {border: 0px;}")
        self.setShowGrid(0)
        self.setMinimumHeight(95)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.fldbk = dataIndex.fldbk

    def headerClicked(self):
        ExNode = self.verticalHeaderItem(0).data(35)
        if ExNode is None:
            return
        dataIndex.currentTextTable.setStyleSheet("QTableWidget QHeaderView::section {border: 0px;"
                                                 "padding: 5px; outline: 0px; background: white;}")
        cardLoader.loadExCard(ExNode)
        self.fldbk.tabWidget.setCurrentIndex(3)

    def resizeColumns(self):
        morphList = []
        ILEGList = []
        for i in range(0, self.columnCount()):
            morph = self.takeItem(1, i)
            morphList.append(morph)
            ILEG = self.takeItem(2, i)
            ILEGList.append(ILEG)
        lineItem = self.takeItem(0, 0)
        glossItem = self.takeItem(3, 0)
        self.setColumnCount(1)
        self.setItem(0, 0, lineItem)
        self.setItem(3, 0, glossItem)
        self.resizeColumnsToContents()
        minWidth = self.columnWidth(0)
        self.takeItem(0, 0)
        self.takeItem(3, 0)
        sumWidth = 0
        self.setColumnCount(len(morphList))
        for i in range(0, len(morphList)):
            self.setItem(1, i, morphList[i])
            self.setItem(2, i, ILEGList[i])
            self.resizeColumnToContents(i)
            sumWidth += self.columnWidth(i)
        self.setItem(0, 0, lineItem)
        self.setItem(3, 0, glossItem)
        if self.columnCount() > 1:
            self.setSpan(0, 0, 1, self.columnCount())
            self.setSpan(3, 0, 1, self.columnCount())
        if sumWidth < minWidth:
            tDiff = minWidth - sumWidth + 5
            lastColumn = self.columnCount() - 1
            newWidth = self.columnWidth(lastColumn) + tDiff
            self.setColumnWidth(lastColumn, newWidth)
