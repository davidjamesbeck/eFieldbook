from PyQt6 import QtWidgets, QtCore, QtGui
from xml.etree import ElementTree as etree
from ELFB import cardLoader, textTable, dataIndex, EgTable, Orthographies, formattingHandlers,  indexOnlyBtns
from ELFB.palettes import AbbrManager, LineSplitter, LinkToLexicon, TierManager, AnalysisManager
from ELFB import searchClasses, idGenerator#, autoparsing
from copy import deepcopy
import re

"""abbreviation data on example cards"""

def addAbbr(fldbk):
    """add a new abbreviation to list"""
    aManager = AbbrManager.AbbrManager(fldbk)
    if aManager.exec():
        newData = aManager.setData()
        topNode = dataIndex.root.find('Abbreviations')
        abbrList = []
        for child in topNode.iter('Abbr'):
            abbrList.append(child.attrib.get('ACode'))
        if len(abbrList) != 0:
            codeList = sorted(abbrList, key=lambda i : int(i[2:]))
            lastCode = codeList[-1]
            lastNumber = int(lastCode[2:])
            lastNumber += 1
        else:
            lastNumber = 1
        newCode = 'AC' + str(lastNumber)
        abbrev = etree.SubElement(topNode, 'Abbr')
        abbrev.set('Abv', newData[0])
        abbrev.set('Term', newData[1])
        itemText = '<small>' + newData[0].swapcase() + '</small>&emsp;‘' + newData[1] + '’'
        if not newData[2] is None:
            abbrev.set('Form', newData[2])
            itemText += ' (' + newData[2] + ')'
        ##generate ACode
        abbrev.set('ACode', newCode)
        
        #add item to model and sort
        newItem = QtGui.QStandardItem()
        newItem.setData(newCode, 35)
        newItem.setData(abbrev, 36)
        newItem.setText(itemText)
        newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)   
        abbrModelProxy = fldbk.eAbbreviations.model()
        abbrModel = abbrModelProxy.sourceModel()
        abbrModel.appendRow(newItem)
        fldbk.eAbbreviations.resizeColumnToContents(0)
        fldbk.eAbbreviations.resizeRowsToContents()        
        fldbk.iAbbreviations.resizeColumnToContents(0)
        fldbk.iAbbreviations.resizeRowsToContents()
        for i in range(0, abbrModelProxy.rowCount()):
            if fldbk.eAbbreviations.model().index(i, 0).data(35) == newCode:
                theItem = i
                break  
        fldbk.eAbbreviations.setCurrentIndex(fldbk.eAbbreviations.model().index(theItem, 0))
        fldbk.eAbbreviations.scrollTo(fldbk.eAbbreviations.currentIndex(), QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)        
        fldbk.iAbbreviations.setCurrentIndex(fldbk.iAbbreviations.model().index(theItem, 0))
        fldbk.iAbbreviations.scrollTo(fldbk.iAbbreviations.currentIndex(), QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
        dataIndex.unsavedEdit = 1

def delAbbr(fldbk):
    """remove abbreviation from list"""
    badNode = fldbk.eAbbreviations.currentIndex().data(36)
    badAbbr = badNode.attrib.get('ACode')
    proxyModel = fldbk.eAbbreviations.model()
    model = proxyModel.sourceModel()
    for i in range(model.rowCount()):
        if model.index(i, 0).data(35) == badAbbr:
            model.removeRow(i)
            break
    ##update XML
    fldbk.eAbbreviations.setModel(proxyModel)
    fldbk.iAbbreviations.setModel(proxyModel)
    dataIndex.root.find('Abbreviations').remove(badNode)
    dataIndex.unsavedEdit = 1

def editAbbr(fldbk, card):
    """edit abbreviation in list"""
    if card == 'eg':
        view = fldbk.eAbbreviations
    else:
        view = fldbk.iAbbreviations
    if view.currentIndex().row() == -1:
        return
    try:
        abbrev = view.currentIndex().data(36)
    except AttributeError:
        return
    a = abbrev.attrib.get('Abv')
    b = abbrev.attrib.get('Term')
    try:
        c = abbrev.attrib.get('Form')
    except AttributeError:
        c = None
    oldData = [a, b, c]
    aManager = AbbrManager.AbbrManager(fldbk)
    aManager.setAbbr(abbrev)
    if aManager.exec():
        newData = aManager.setData()
        checked = aManager.checkUpdate()
        if oldData == newData:
            return
        else:
            abbrev.set('Abv', newData[0])
            abbrev.set('Term', newData[1])
            itemText = '<small>' + newData[0].swapcase() + '</small>&emsp;‘' + newData[1] + '’'
            if newData[2] is not None:
                abbrev.set('Form', newData[2])
                itemText += ' (' + newData[2] + ')'
            else:
                try:
                    del abbrev.attrib['Form']
                except AttributeError:
                    pass
            currentProxyIndex = view.currentIndex()
            currentSourceIndex = view.model().mapToSource(currentProxyIndex)
            item = view.model().sourceModel().itemFromIndex(currentSourceIndex)
            item.setText(itemText)
            item.setData(abbrev, 36)
            dataIndex.unsavedEdit = 1       
        if checked:
            oldAbbr = a
            newAbbr = newData[0]
            oldLitAbbr = "‘" + oldAbbr + "’"
            regex = re.compile(r'(?<!\w)%s(?!\w)'%oldAbbr) 
            for child in dataIndex.root.iter('Lit'):
                if oldLitAbbr in child.text:
                    child.text = regex.sub(newAbbr, child.text)                   
            for child in dataIndex.root.iter('ILEG'):
                if child.text is not None:
                    if regex.search(child.text):
                        child.text = regex.sub(newAbbr, child.text)

"""other buttons on example cards"""

def toggleParse(fldbk):
    if fldbk.eAutoParsingBtn.isChecked():
        if len(fldbk.iIndex.toPlainText()) == 0:
            indexOnlyBtns.buildIndex()
#            autoparsing.askToBuildIndex()
            fldbk.tabWidget.setCurrentIndex(3)

def eAddColumn(fldbk):
    columnCount = fldbk.eAnalysis.columnCount()
    fldbk.eAnalysis.insertColumn(columnCount-1)

def eAddTier(fldbk):
    trManager = TierManager.TierManager(fldbk)
    if trManager.exec():
        nameList = trManager.newTierName
        if nameList is None:
            return
        if dataIndex.root.attrib.get('Tiers') is None:
            tierList = ''
        else:
            tierList = dataIndex.root.attrib.get('Tiers')
        for item in nameList:
            if len(tierList) == 0:
                tierList = item
            else:
                if item not in tierList:
                    tierList = tierList + ', ' + item
            fldbk.eAnalysis.insertRow(fldbk.eAnalysis.rowCount())
            for c in range(0, fldbk.eAnalysis.columnCount()-1):
                newItem = QtWidgets.QTableWidgetItem(1001)
                fldbk.eAnalysis.setItem(fldbk.eAnalysis.rowCount()-1, c, newItem)
            rowHeader = QtWidgets.QTableWidgetItem(1001)
            rowHeader.setText(item)
            fldbk.eAnalysis.setVerticalHeaderItem(fldbk.eAnalysis.rowCount()-1, rowHeader)
            fldbk.eAnalysis.delegate = EgTable.ExampleDelegate()
            fldbk.eAnalysis.setItemDelegate(fldbk.eAnalysis.delegate)
            syntNode = etree.Element('Synt', {'Tier' : item})
            egNode = dataIndex.root.find('Ex[@ExID="%s"]'%dataIndex.currentCard)
            k = egNode.find('L1Gloss')
            d = list(egNode).index(k)
            egNode.insert(d, syntNode)
        dataIndex.root.set('Tiers', tierList)
        dataIndex.unsavedEdit = 1
    
def eDelTier(fldbk):
    theRow = fldbk.eAnalysis.currentRow()
    if theRow is None:
        return
    elif theRow <= 1:
        return
    if fldbk.eAnalysis.verticalHeaderItem(theRow).text() == 'Morph' or fldbk.eAnalysis.verticalHeaderItem(theRow).text() == 'ILEG':
        return
    tierLabel = fldbk.eAnalysis.verticalHeaderItem(theRow).text()
    egNode = dataIndex.exDict[dataIndex.currentCard]
    syntNode = egNode.find('Synt[@Tier="%s"]' %tierLabel)
    egNode.remove(syntNode)
    if dataIndex.root.find('Ex/Synt[@Tier="%s"]' %tierLabel) is None:
        tiers = dataIndex.root.attrib.get('Tiers')
        tierList = tiers.split(', ')
        tiers = ''
        for item in tierList:
            if item == tierLabel:
                continue
            if len(tiers) == 0:
                tiers = item
            else:
                tiers = tiers + ', ' + item
        if len(tiers) == 0:
            del dataIndex.root.attrib['Tiers']
        else:
            dataIndex.root.set("Tiers", tiers)
    fldbk.eAnalysis.removeRow(theRow)
    dataIndex.unsavedEdit = 1

def eRemoveColumn(fldbk):
    """removes columns from analysis table"""
    if fldbk.eAnalysis.columnCount() == 1:
        return    
    fldbk.eAnalysis.removeColumn(fldbk.eAnalysis.currentColumn())
    mrphList = []
    ilegList = []
    mrph = None
    ileg = None
    for i in range(0, fldbk.eAnalysis.columnCount()):
        try:
            mrphList.append(fldbk.eAnalysis.item(0, i).text())
            ilegList.append(fldbk.eAnalysis.item(1, i).text())
        except AttributeError:
            mrphList.append('[—]')
            ilegList.append('[—]')
    for item in mrphList:
        if mrph is None:
            mrph = item
        else:
            mrph += ' ' + item
    for item in ilegList:
        if ileg is None:
            ileg = item
        else:
            ileg += ' ' + item
    node = dataIndex.exDict[dataIndex.currentCard]
    try:
        node.find('Mrph').text = mrph
    except AttributeError:
        pass
    try:
        node.find('ILEG').text = ileg
    except AttributeError:
        pass
    dataIndex.unsavedEdit = 1

def eSplitEg(fldbk):
    """splits example between two cards"""
    oldID = dataIndex.currentCard
    tSplitter = LineSplitter.LineSplitter(fldbk)
    tSplitter.fillForm(oldID)
    tSplitter.exec()
    if tSplitter.result() == 0:
        return
    else:
        idList = tSplitter.newData(oldID)
    oldRoot = dataIndex.exDict[idList[0]]
    try:
        source = dataIndex.textDict[oldRoot.get('SourceText')]
    except KeyError:
        source = None
    ##update XML if this is from a text
    if source is not None:
        lineList = source.findall('Ln')
        i = 2
        for line in lineList:
            if line.attrib.get('LnRef') == oldID:
                newNode = etree.Element('Ln', {'LnRef':idList[1]})
                source.insert(i, newNode)
            else:
                i += 1
        ##update Text card if that text is open
        if oldRoot.get('SourceText') == dataIndex.lastText and fldbk.tText.findChildren(textTable) is not None:
            cardLoader.loadTextCard(source)                
    cardLoader.loadExCard(oldRoot)
    dataIndex.unsavedEdit = 1
        
def eLocateEg(fldbk):
    """goes to example in context (text or, eventually, dataset)"""
    #TODO: link up with datasets
    egNode = dataIndex.exDict[dataIndex.currentCard]
    lineLabel = fldbk.eLineNumber.toPlainText()
    lineNo = int(lineLabel[5:])
    text = egNode.attrib.get('SourceText')
    if text is None:
        return
    try:
        if text == dataIndex.currentText.attrib.get('TextID'):
            fldbk.tabWidget.setCurrentIndex(2)
        else:
            cardLoader.loadTextCard(dataIndex.textDict[text])
            fldbk.tabWidget.setCurrentIndex(2)
    except AttributeError:
        cardLoader.loadTextCard(dataIndex.textDict[text])
        fldbk.tabWidget.setCurrentIndex(2)
    textWidget = fldbk.textLayout.itemAt(lineNo-1)
    textTable = textWidget.widget()
    dataIndex.currentTextTable = textTable
    textTable.setStyleSheet("QTableWidget QHeaderView::section {border-bottom: 0px;"
                            "border-left: 0px; border-top: 0px; border-right: 0px;"
                            "padding: 5px; outline: 0px; background: #E6E6E6;}")    
    fldbk.tFullText.ensureWidgetVisible(textTable)
    fldbk.tFullText.horizontalScrollBar().setValue(0)

def eAdd2Lex(fldbk):
    """adds example to a lexical entry"""
    eManager = LinkToLexicon.EntryManager(fldbk)
    eManager.listEntries()
    if eManager.exec():
        data = eManager.setData() 
        node = dataIndex.lexDict[data[0]]
        definition = node.find('Def[@Index="%s"]' %str(data[1]))
        etree.SubElement(definition, 'Ln', {'LnRef':dataIndex.currentCard})
        fldbk.eLinksList.insertItem (-1, data[0])
        fldbk.eLinksList.setCurrentIndex(fldbk.eLinksList.findText(data[0]))
        example = dataIndex.root.find('Ex[@ExID="%s"]' %dataIndex.currentCard)
        if example.attrib.get('Links'):
            linksList = example.attrib.get('Links')
            linksList = linksList + ", " + data[0]        
        else:
            linksList = data[0]
        example.set("Links",  linksList)
#        print(etree.tostring(definition, encoding='unicode'))
        cardLoader.loadLexCard(node)
        fldbk.tabWidget.setCurrentIndex(1)    
        dataIndex.unsavedEdit = 1
    
def eBreakLink(fldbk):
    """removes a link to a lex card ONLY—need to consider the breaking of a link to a text"""
    targetNumber = fldbk.eLinksList.currentIndex()
    if targetNumber == -1:
        return
    target = fldbk.eLinksList.currentText()
    exNode = dataIndex.exDict[dataIndex.currentCard]
    if target[0:2] == "LX":
        lexNode = dataIndex.lexDict[target]
        name = 'the lexical entry <i>'+ lexNode.findtext("Orth") + "</i>"
        breakbox = QtWidgets.QMessageBox()
        breakbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        breakbox.setText("Break link?")
        breakbox.setInformativeText('This will remove the link to %s' %name)
        breakbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
        breakbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        breakbox.exec()
        if breakbox.result() == QtWidgets.QMessageBox.StandardButton.Ok:    
            fldbk.eLinksList.removeItem(fldbk.eLinksList.findText(target))
            line = lexNode.find('Def/Ln[@LnRef="%s"]' %dataIndex.currentCard)
            defNode = lexNode.find('.//Ln[@LnRef="%s"]/..' %dataIndex.currentCard )
            defNode.remove(line)
            links = exNode.attrib.get('Links')
            linksList = links.split(', ')
            newLinks =''
            for item in linksList:
                if item != target:
                    if len(newLinks) == 0:
                        newLinks = item
                    else:
                        newLinks = newLinks + ", " + item
            if len(newLinks) == 0:
                del exNode.attrib['Links']
            else:
                exNode.set('Links', newLinks)
        
def eAdvancedSearch(fldbk):
    engine = searchClasses.ExSearchEngine(fldbk)
    engine.doSearch()

def copyLine(node, outputLanguage='L1'):
    """copy example to clipboard"""
    fldbk = dataIndex.fldbk
    L2Flag = 1
    entryRow0 = node.findtext('Line')
    if fldbk.eOrthography.currentText() == 'Phonetic':
        baseOrthography = dataIndex.root.get('Orth')
        mapping = dataIndex.root.find('Orthography[@Name="%s"]'%baseOrthography).text
        pairList = mapping.split(';')
        entryRow0 = Orthographies.doTransform(entryRow0, pairList)
    if len(entryRow0) == 0:
        return
    exampleP = entryRow0
    try: 
        entryRow1 = node.findtext('Mrph')
        if fldbk.eOrthography.currentText() == 'Phonetic':
            #TODO: set up output of examples in IPA
            entryRow1 = Orthographies.doTransform(entryRow1, pairList)
        exampleP += "\r" + entryRow1
        entryRow2 = node.findtext('ILEG')
        exampleP += "\r" + entryRow2
    except AttributeError:
        pass
    try: 
        entryRow3 = node.findtext('L2Gloss')
    except AttributeError:
        L2Flag = 0
    if  outputLanguage == 'L2' and L2Flag != 0:
        entryRow3 = node.findtext('L2Gloss')
    elif len(node.findtext('L1Gloss')) == 0:
        entryRow3 = node.findtext('L2Gloss')
    else:
        entryRow3 = node.findtext('L1Gloss')
    exampleP += "\r‘" + entryRow3 + "’"
    exampleP = formattingHandlers.XMLtoPlainText(exampleP) + " (" + node.attrib.get('Spkr') + ")"
    clipboard = QtWidgets.QApplication.clipboard()
    clipboard.setText(exampleP)
    return exampleP

def eDuplicate(fldbk):
    """duplicate entry"""
    oldNode = dataIndex.exDict[dataIndex.currentCard]
    newID = idGenerator.generateID('EX', dataIndex.exDict)
    newNode = deepcopy(oldNode)
    newNode.set('ExID', newID)
    k = dataIndex.root.find('Ex[@ExID="%s"]'%dataIndex.currentCard)
    i = list(dataIndex.root).index(k) + 1
    dataIndex.root.insert(i, newNode)
    dataIndex.currentCard = newID
    dataIndex.exDict[newID] = newNode
    cardLoader.loadExCard(newNode)
    
def goToLink(fldbk):
    if len(fldbk.eLinksList.currentText()) == 0:
        return
    else:
        link = fldbk.eLinksList.currentText()
    if link[0:2] == "LX":
        linkedCard = dataIndex.root.find('Lex[@LexID="%s"]' %link)
        cardLoader.loadLexCard(linkedCard)
        fldbk.tabWidget.setCurrentIndex(1)
    elif link[0:2] == "DS":
        linkedCard = dataIndex.root.find('Dset[@DsetID="%s"]' %link)
        cardLoader.loadDataCard(linkedCard)
        fldbk.tabWidget.setCurrentIndex(4)
    else:
        return
    
def delColumn(fldbk):
    if fldbk.eAnalysis.currentColumn() == -1:
        return
    else:
        badColumn = fldbk.eAnalysis.currentColumn()
        colNumber = str(fldbk.eAnalysis.currentColumn() + 1)
        queryBox = QtWidgets.QMessageBox()
        queryBox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        queryBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel | QtWidgets.QMessageBox.StandardButton.Ok)
        queryBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        queryBox.setText('Delete column %s and its contents?' %colNumber)
        queryBox.exec()
        if queryBox.result() == QtWidgets.QMessageBox.StandardButton.Ok:                            
            fldbk.eAnalysis.removeColumn(badColumn)
            fldbk.eAnalysis.delegate.updateExample()
        else:
            return

def findUnparsed(fldbk):
    exList = dataIndex.root.findall('Ex')
    start = 0
    firstBlank = ''
    nextUnparsed = ''
    for node in exList:
        if node.attrib.get('ExID') == dataIndex.currentCard:
            start = 1
        elif node.find('Mrph') is None or len(node.findtext('Mrph')) == 0:
            if start == 1:
                nextUnparsed = node.attrib.get('ExID')
                break
            elif len(firstBlank) == 0:
                firstBlank = node.attrib.get('ExID')
    if len(nextUnparsed) == 0:
        nextUnparsed = firstBlank
    if len(nextUnparsed) != 0:
        unparsedNode = dataIndex.exDict[nextUnparsed]
        cardLoader.loadExCard(unparsedNode)
    
def clearAnalysis(fldbk):
    fldbk.eAnalysis.setColumnCount(0)
    fldbk.eAnalysis.insertColumn(0)
    lastHeadWidget = QtWidgets.QTableWidgetItem(1001)
    lastHeadWidget.setText('+')
    fldbk.eAnalysis.setHorizontalHeaderItem(0, lastHeadWidget)
    fldbk.eAnalysis.resizeColumnToContents(0)
    
def addMulti(fldbk):
    egManager = AnalysisManager.ExampleManager(fldbk)
    egManager.setWindowTitle('New Examples')
    egManager.show()    
    
def eSplitColumn(fldbk):
    print('ok')
    table = fldbk.eAnalysis
    if table.currentColumn() == -1:
        return
    else:
        table.insertColumn(table.currentColumn()+1)
    
