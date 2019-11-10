from PyQt5 import QtWidgets, QtCore, QtGui
from ELFB import HTMLDelegate, dataIndex, formattingHandlers, autoparsing, textOnlyBtns
import re
from ELFB.palettes import SessionDate

class ExampleDelegate(HTMLDelegate.HTMLDelegate):
    def __init__(self, parent):
        super(ExampleDelegate, self).__init__(parent)
        self.closeEditor.connect(self.updateExample)
        self.fldbk = dataIndex.fldbk       
        
    def updateExample(self):
        dataIndex.unsavedEdit = 1
        update = SessionDate.dateFinder()
        self.fldbk.eUpdated.setPlainText(update)
        ExNode = dataIndex.exDict[dataIndex.currentCard]
        ExNode.set('Update',update)
        updateFlag = False
        if self.fldbk.eAutoParsingBtn.isChecked() and dataIndex.unparsedILEG != None:
            updateFlag = True
        for r in range(0, self.fldbk.eAnalysis.rowCount()): #for every row
            try:
                string = ''
                label = self.fldbk.eAnalysis.verticalHeaderItem(r).text()
                for c in range(0,self.fldbk.eAnalysis.columnCount()-1): #for each cell
                    try:
                        itemText = self.fldbk.eAnalysis.item(r, c).text()
                        itemText = itemText.strip()
                    except AttributeError:
                        itemText = ''
                    if label == 'ILEG':
                        newContents = ''
                        if itemText != '[—]':
                            itemText = itemText.replace('-', '–')
                            itemText = itemText.replace('<small>', '')
                            itemText = itemText.replace('</small>', '')
                            newContents, newText = formattingHandlers.smallCapsConverter(itemText)
                            self.boundaryChecker(r, c)
                            self.fldbk.eAnalysis.item(r, c).setText(newText)
                        try:
                            if updateFlag == True and dataIndex.unparsedILEG.column() == c:
                                autoparsing.updateIndex(c)
                        except RuntimeError:
                            pass
                        itemText = newContents
                    elif label == 'Morph':
                        if itemText != '[—]':
                            itemText = itemText.replace('-', '–')
                        self.fldbk.eAnalysis.item(r, c).setText(itemText)
                    if len(string) == 0:
                        string = itemText
                    else:
                        string += "\t" + itemText
                if label =='Morph':
                    ExNode.find('Mrph').text = string
                elif label == 'ILEG':
                    ExNode.find('ILEG').text = string
                else: 
                    ExNode.find('Synt[@Tier="%s"]' %label).text = string
            except AttributeError:
                pass
        self.fldbk.eAnalysis.resizeColumnsToContents()  
        self.fldbk.eAnalysis.clearSelection()
        if ExNode.attrib.get('SourceText') != None and dataIndex.currentText != None:
            if ExNode.attrib.get('SourceText') == dataIndex.currentText:
                textOnlyBtns.updateText(self.fldbk, ExNode)
        
    def boundaryChecker(self, row, column):
        '''first step in checking to make sure divisions match on Mrph and ILEG lines'''
        '''row will always be 1'''
        #TODO allow customization of boundary list
        theMorphs = self.fldbk.eAnalysis.item(row -1, column)
        theAnalysis = self.fldbk.eAnalysis.item(row, column)
        boundaryList = ["–","=", "•","+"]
        '''check to make sure that the target cell is not monomorphemic'''
        unparsed = 'yes'
        for boundary in boundaryList:
            if boundary in theAnalysis.text() or boundary in theMorphs.text():
                self.compareItems(theMorphs, theAnalysis, boundary)
                unparsed = 'no'
        if unparsed == 'yes':
            brush = QtGui.QBrush(QtCore.Qt.white)
            theMorphs.setBackground(brush)
            theAnalysis.setBackground(brush)
            
    def compareItems(self, theMorphs, theAnalysis, boundary):
        '''checks morphs and glosses to ensure that there is no mismatched boundary,
        hilites the errors'''
        morphs = theMorphs.text()
        analysis = theAnalysis.text()
        morphList = morphs.split(boundary)
        analysisList = analysis.split(boundary)
        if len(morphList) != len(analysisList):
            brush = QtGui.QBrush(QtCore.Qt.cyan)
            theMorphs.setBackground(brush)
            theAnalysis.setBackground(brush)
        else:
            brush = QtGui.QBrush(QtCore.Qt.white)
            theMorphs.setBackground(brush)
            theAnalysis.setBackground(brush)

class EgTable(QtWidgets.QTableWidget):
    '''class defines the properties of the example field on the example card'''
        
    def __init__(self, parent):
        super(EgTable, self).__init__(parent)
        self.SelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setStyleSheet("selection-background-color: #E6E6E6; border: 0px;")
        self.delegate = ExampleDelegate(self)
        self.setItemDelegate(self.delegate)
        self.horizontalHeader().setEnabled(1)
        self.verticalHeader().setEnabled(1)
        self.verticalHeader().show()
        self.horizontalHeader().show()
        self.horizontalHeader().sectionClicked.connect(self.headerClicked)
        self.setShowGrid(0)
        self.setMinimumHeight(95)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.MinimumExpanding)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.fldbk = dataIndex.fldbk
        self.itemDoubleClicked.connect(self.stripTags)
    
    def stripTags(self, item):
        newText =item.text()
        if newText == '[—]':
            autoparsing.storeUnparsedItem(item)
        else:
            regex = re.compile('(?<=<small>)\w*(?=</small>)')
            abbrList = regex.findall(newText)
            if len(abbrList) != 0:
                for abbr in abbrList:
                    newText = newText.replace(abbr, abbr.lower())
            newText = newText.replace('<small>', '')
            newText = newText.replace('</small>', '')
            item.setText(newText)
            dataIndex.unparsedILEG = None

    def headerClicked(self):
        colLoc = self.columnCount()-1
        if colLoc ==  self.currentColumn():
            self.insertColumn(colLoc)
        for i in range(0,self.rowCount()):
            newItem = QtWidgets.QTableWidgetItem(1001)
            self.setItem(i,colLoc,newItem)
        self.delegate = ExampleDelegate(self)
        self.setItemDelegate(self.delegate)
        lastCol = self.columnCount()-1
        for i in range(0, self.rowCount()):
            newItem = QtWidgets.QTableWidgetItem(1001)
            flags = QtCore.Qt.ItemFlags()
            flags != QtCore.Qt.ItemIsEnabled
            newItem.setFlags(flags)
            self.setItem(i, lastCol, newItem)

