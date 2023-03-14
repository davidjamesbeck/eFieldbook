import re
import textwrap
from PyQt6 import  QtCore, QtWidgets
from ELFB import textTable, contextMenus, dataIndex, Orthographies, formattingHandlers, update
#import xml.etree.ElementTree as etree

def loadDataCard(dataRoot, navBtn=False):
    fldbk = dataIndex.fldbk
    targetCard = dataRoot.attrib.get('DsetID')
    dataIndex.currentCard = targetCard
    dataIndex.lastDset = dataRoot.attrib.get('DsetID')   
    dataIndex.root.set('LastDset', dataIndex.lastDset)
    if navBtn is False:
        if len(fldbk.dNavBar.stack) == 0:
            fldbk.dNavBar.stack.append(targetCard)
            fldbk.dNavBar.index = fldbk.dNavBar.index + 1
        elif fldbk.dNavBar.stack[-1] != targetCard:
            fldbk.dNavBar.stack.append(targetCard)       
            fldbk.dNavBar.index = fldbk.dNavBar.index + 1
    fldbk.dSource.clear()
    entry = dataRoot.attrib.get('Spkr')
    if entry:
      fldbk.dSource.setPlainText(entry)
      
    fldbk.dResearcher.clear()
    entry = dataRoot.attrib.get('Rschr')
    if entry:
      fldbk.dResearcher.setPlainText(entry)
      
    fldbk.dDate.clear()
    entry = dataRoot.attrib.get('Date')
    if entry:
      fldbk.dDate.setPlainText(entry)
      
    fldbk.dUpdated.clear()
    entry = dataRoot.attrib.get('Update')
    if entry:
      fldbk.dUpdated.setPlainText(entry)
      
    fldbk.dKeywords.clear()
    entry = dataRoot.attrib.get('Kywd')
    if entry:
      fldbk.dKeywords.setPlainText(entry)
      
    fldbk.dNotes.clear()
    entry = dataRoot.findtext('Comments')
    if entry:
        entry = formattingHandlers.XMLtoRTF(entry)
        fldbk.dNotes.setHtml(entry)
    else:
        fldbk.dNotes.setFontItalic(0)
        fldbk.dNotes.setFontUnderline(0)
        fldbk.dNotes.setFontWeight(50)
        
    fldbk.dTitle.clear()
    entry = dataRoot.findtext('Title')
    if entry:
        entry = formattingHandlers.XMLtoRTF(entry)
        fldbk.dTitle.setHtml(entry)
      
    fldbk.dData.clear()
    fldbk.dData.setAcceptRichText(1)
    fldbk.dData.setFontItalic(0)
    fldbk.dData.setFontUnderline(0)
    fldbk.dData.setFontWeight(50)
#    html = fldbk.dData.toHtml()
    entry = dataRoot.findtext('Data')
    if entry:
        fldbk.dData.setPlainText(entry)
#        html = fldbk.dData.toHtml()
#        newHtml = formattingHandlers.XMLtoRTF(html)
#        fldbk.dData.setHtml(newHtml)
      
    """Recordings"""
    fldbk.dSound.loadMedia(dataRoot)
    resetNavBars(fldbk.dDataNav, dataIndex.currentCard)

def textTableBuilder(node, j, spokenBy, lineNode):
    """builds tables for presenting lines on the text card"""
    aFlag = 1
    entryRow0 = node.findtext('Line')
    entryRow0 = formattingHandlers.XMLtoRTF(entryRow0)
    try: 
        if len(node.findtext('Mrph')) == 0:
            aFlag = 0 
        else:
            entryRow1 = node.findtext('Mrph').split('\t')
            entryRow2 = node.findtext('ILEG').split('\t')
    except AttributeError:
        aFlag = 0
    if node.find('L2Gloss') is not None:    
        if dataIndex.glossingLanguage  == 'L2Gloss' and len(node.findtext('L2Gloss')) != 0:
            entryRow3 = node.findtext('L2Gloss')
            dataIndex.glossingLanguage = 'L2Gloss'
        elif len(node.findtext('L1Gloss')) == 0 and len(node.findtext('L2Gloss')) !=0:
            entryRow3 = node.findtext('L2Gloss')
            dataIndex.glossingLanguage = 'L2Gloss'
        else:
            entryRow3 = node.findtext('L1Gloss')
            dataIndex.glossingLanguage = 'L1Gloss'
    else:
        entryRow3 = node.findtext('L1Gloss')
        dataIndex.glossingLanguage = 'L1Gloss'
    """code to normalize glossing"""
    entryRow3, spokenBy, timeCode, endTime = update.fixGlosses(entryRow3)
    node.find(dataIndex.glossingLanguage).text = entryRow3
    if timeCode is not None:
        lineNode.set('Time', timeCode)
    if endTime is not None:
        lineNode.set('EndTime', endTime)
    if spokenBy is not None:
        lineNode.set('SpokenBy', spokenBy)
    """end code for normalizing"""
    entryRow3 = formattingHandlers.XMLtoRTF(entryRow3)
    entryRow3 = "‘" + entryRow3 + "’"
    if lineNode.attrib.get('Time') is not None:
        timeCode = lineNode.attrib.get('Time')
        entryRow3 += ' [' + timeCode
        if lineNode.attrib.get('EndTime') is not None:
            endTime = lineNode.attrib.get('EndTime')
            entryRow3 += ' – ' + endTime + ']'
        else:
            entryRow3 += ']'
    if lineNode.attrib.get('SpokenBy') is not None:
        spokenBy = lineNode.attrib.get('SpokenBy')
        entryRow3 = spokenBy + ": " + entryRow3
        if lineNode.attrib.get('SpokenBy') != node.attrib.get('Spkr'):
            for speaker in dataIndex.root.iter("Speaker"):
                if speaker.attrib.get('SCode') == spokenBy:
                    node.set('Spkr', spokenBy)
                    break
    newTable = textTable.textTable(parent=None)
    newTable.setGeometry(0, 0, 200, 58)
    newTable.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
    if aFlag == 1:
        newTable.setRowCount(4)
        newTable.setColumnCount(len(entryRow1))
        newTable.setRowHeight(0, 20)
        newTable.setRowHeight(1, 20)          
        newTable.setRowHeight(2, 20)
        newTable.setRowHeight(3, 20)
        newTable.setMinimumHeight(100)
        newTable.setMaximumHeight(100)
        newTable.setVerticalHeaderLabels(["", "", "", ""])
    else:
        newTable.setRowCount(2)
        newTable.setColumnCount(1)
        newTable.setRowHeight(0, 20)
        newTable.setRowHeight(1, 20)
        newTable.setMinimumHeight(50)
        newTable.setMaximumHeight(50)
        newTable.setVerticalHeaderLabels(["", ""])
    tableCellLine = QtWidgets.QTableWidgetItem(10001)
    tableCellLine.setText(entryRow0)
    tableCellGloss = QtWidgets.QTableWidgetItem(10001)
    tableCellGloss.setText(entryRow3)
    if len(entryRow0) > len(entryRow3):
        newTable.setItem(0, 0, tableCellLine)
    else:
        newTable.setItem(0, 0, tableCellGloss)
    newTable.resizeColumnToContents(0)
    minWidth = newTable.columnWidth(0)
    sumWidth = 0
    newTable.takeItem(0, 0)
    if aFlag == 1:
        if len(entryRow1) != len(entryRow2):
            missingDataBox = QtWidgets.QMessageBox()
            missingDataBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            missingDataBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            missingDataBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            missingDataBox.setText('Mismatched lines.')
            missingDataBox.setInformativeText('You must have the same number of words '
                                              'on the analysis and the interlinear gloss lines.\n'
                                              'Line number %s' %str(j+1))
            missingDataBox.exec()
            return
        sumWidth = 0
        for i in range(0, len(entryRow1)):
            parse = entryRow2[i]
            parse = parse.replace(' ', '')
            newContent, parse = formattingHandlers.smallCapsConverter(parse)
            tableCellTop = QtWidgets.QTableWidgetItem(10001)
            tableCellTop.setText(entryRow1[i])
            tableCellBottom = QtWidgets.QTableWidgetItem(10001)
            tableCellBottom.setText(parse + " ")
            tableCellBottom.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)
            newTable.setItem(1, i, tableCellTop)
            newTable.setItem(2, i, tableCellBottom)
            newTable.resizeColumnToContents(i)
            sumWidth += newTable.columnWidth(i)
        if sumWidth < minWidth:
            tDiff = minWidth - sumWidth + 5
            newTable.setColumnWidth(i, newTable.columnWidth(i) + tDiff)
    if aFlag == 1:
        newTable.setItem(0, 0, tableCellLine)
        newTable.setItem(3, 0, tableCellGloss)
        if newTable.columnCount() > 1:
            newTable.setSpan(0, 0, 1, newTable.columnCount())
            newTable.setSpan(3, 0, 1, newTable.columnCount())
    else:
        newTable.setItem(0, 0, tableCellLine)
        newTable.setItem(1, 0, tableCellGloss)
        newTable.resizeColumnToContents(0)
    tableCellNumber = QtWidgets.QTableWidgetItem(1001)
    tableCellNumber.setText(str(j+1))
    tableCellNumber.setData(35, node)
    tableCellNumber.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)    
    newTable.setVerticalHeaderItem(0, tableCellNumber)
#    newTable.setObjectName(eg)
    newTable.setToolTip(QtWidgets.QApplication.translate("Fieldbook", 
                                                     "click on line number to view \n"
                                                     "example in the Examples tab.\n"
                                                     "Sideways scroll long examples with mouse.", None))
    if dataIndex.displayOrthography == "Phonetic":
        mapping = dataIndex.root.find('Orthography[@Name="%s"]'%dataIndex.root.get('Orth')).text
        pairList = mapping.split(';')   
        Orthographies.changeTextDisplay(dataIndex.fldbk, pairList, newTable)
        dataIndex.fldbk.tOrthography.setCurrentIndex(dataIndex.fldbk.tOrthography.findText("Phonetic"))
    return newTable

def loadTextCard(textRoot, navBtn=False):   
    fldbk = dataIndex.fldbk
    if dataIndex.currentText == textRoot:
        if dataIndex.displayOrthography != fldbk.tOrthography.currentText():
            Orthographies.changeDisplayOrthography(fldbk, -1, 'Txt')
        return
    dataIndex.currentText = textRoot
    dataIndex.newText = False
    if dataIndex.currentTextTable is not None:
        dataIndex.currentTextTable.setStyleSheet("QTableWidget QHeaderView::section {border-bottom: 0px;"
                                                    "border-left: 0px; border-top: 0px; border-right: 0px;"
                                                    "padding: 5px; outline: 0px; background: white;}")   
        dataIndex.currentTextTable = None
    targetCard = textRoot.attrib.get('TextID')   
    dataIndex.currentCard = targetCard   
    dataIndex.lastText = textRoot.attrib.get('TextID')
    dataIndex.root.set('LastText', dataIndex.lastText)
    if navBtn is False:
        if len(fldbk.tNavBar.stack) == 0:
            fldbk.tNavBar.stack.append(targetCard)
            fldbk.tNavBar.index = fldbk.tNavBar.index + 1
        elif fldbk.tNavBar.stack[-1] != targetCard:
            fldbk.tNavBar.stack.append(targetCard)
            fldbk.tNavBar.index = fldbk.tNavBar.index + 1
    fldbk.tSource.clear()
    entry = textRoot.attrib.get('Spkr')
    if entry:
        fldbk.tSource.setPlainText(entry)         
    fldbk.tResearcher.clear()
    entry = textRoot.attrib.get('Rschr')
    if entry:
        fldbk.tResearcher.setPlainText(entry)         
    fldbk.tDate.clear()
    entry = textRoot.attrib.get('Date')
    if entry:
        fldbk.tDate.setPlainText(entry)          
    fldbk.tUpdated.clear()
    entry = textRoot.attrib.get('Update')
    if entry:
        fldbk.tUpdated.setPlainText(entry)
    fldbk.tTranscriber.clear()
    entry = textRoot.attrib.get('Trns')
    if entry:
        fldbk.tTranscriber.setPlainText(entry)         
    fldbk.tTitle.clear()
    entry = textRoot.findtext('Title')
    if entry:
        entry = formattingHandlers.XMLtoRTF(entry)
        fldbk.tTitle.setHtml(entry) 
    fldbk.tNotes.clear()
    entry = textRoot.findtext('Comments')
    if entry:
        entry = formattingHandlers.XMLtoRTF(entry)
        fldbk.tNotes.setHtml(entry) 
    else:
        fldbk.tNotes.setFontItalic(0)
        fldbk.tNotes.setFontUnderline(0)
        fldbk.tNotes.setFontWeight(50)
    
    """text table build"""
    addTextWidget(fldbk, textRoot)
      
    """Recordings"""
    fldbk.tSound.loadMedia(textRoot)
    L1 = dataIndex.root.attrib.get('L1Choice')
    L2 = dataIndex.root.attrib.get('L2Choice')
    if dataIndex.glossingLanguage == 'L1Gloss' and L2 is not None:
        label = L1 + " ➔ " + L2
    elif dataIndex.glossingLanguage == 'L2Gloss' and L2 is not None:
        label = L2 + " ➔ " + L1
    else:
        label = "—"
    if len(label) < 10:
        fldbk.tLanguageBtn.setText(label)
    resetNavBars(fldbk.tTextNav, dataIndex.currentCard)

def loadExCard(egRoot, navBtn=False):
    fldbk = dataIndex.fldbk
    targetCard = egRoot.attrib.get('ExID')
    dataIndex.currentCard = targetCard
    dataIndex.lastEx = egRoot.attrib.get('ExID')   
    dataIndex.root.set('lastEx', dataIndex.lastEx)
    if navBtn is False:
        if len(fldbk.eNavBar.stack) == 0:
            fldbk.eNavBar.stack.append(targetCard)
            fldbk.eNavBar.index = fldbk.eNavBar.index + 1
        elif fldbk.eNavBar.stack[-1] != targetCard:
            fldbk.eNavBar.stack.append(targetCard)
            fldbk.eNavBar.index = fldbk.eNavBar.index + 1
    fldbk.eExampleNumber.clear()
    IDRef = egRoot.get('ExID')
    fldbk.eExampleNumber.setPlainText(IDRef)
    
    fldbk.eKeywords.clear()
    entry = egRoot.attrib.get('Kywd')
    if entry:
        fldbk.eKeywords.setPlainText(entry)

    """get data from text <Ln> elements if example is textual"""
    fldbk.eSourceText.clear()
    fldbk.eTimeCode.clear()
    fldbk.eSpokenBy.clear()
    fldbk.eLineNumber.clear()
    sourceID = egRoot.attrib.get('SourceText')
    if sourceID:
        sourceText = dataIndex.textDict[sourceID]
        title = sourceText.find('Title').text
        fldbk.eSourceText.setPlainText(title)
        lineList = sourceText.findall('Ln')
        for i in range(0, len(lineList)):
            if lineList[i].attrib.get('LnRef') == targetCard:
                fldbk.eLineNumber.setPlainText('line ' + str(i + 1))
                if lineList[i].attrib.get('SpokenBy') is not None:
                    fldbk.eSpokenBy.setPlainText(lineList[i].attrib.get('SpokenBy'))
                elif egRoot.attrib.get('SpokenBy') is not None:
                    spokenBy = egRoot.attrib.get('SpokenBy')
                    lineList[i].set('SpokenBy', spokenBy)
                    for speaker in dataIndex.root.iter("Speaker"):
                        if speaker.attrib.get('SCode') == spokenBy:
                            egRoot.set('Spkr', spokenBy)
                            break
                    del egRoot.attrib['SpokenBy']
                if lineList[i].attrib.get('Time') is not None:
                    timeCode = lineList[i].attrib.get('Time')
                    if lineList[i].attrib.get('EndTime') is not None:
                        endTime = lineList[i].attrib.get('EndTime')
                        timeCode += ' – ' + endTime
                    fldbk.eTimeCode.setPlainText(timeCode)
                elif egRoot.attrib.get('Time') is not None:
                    lineList[i].set('Time', egRoot.attrib.get('Time'))
                    del egRoot.attrib['Time']
                break

    fldbk.eLinksList.clear()
    entry = egRoot.attrib.get('Links')
    if entry:
        linksList = entry.split(', ')
        for item in linksList:
            fldbk.eLinksList.insertItem(-1, item)
        fldbk.eLinksList.setCurrentIndex(0)

    fldbk.eSource.clear()
    entry = egRoot.attrib.get('Spkr')
    if entry:
        fldbk.eSource.setPlainText(entry)
      
    fldbk.eResearcher.clear()
    entry = egRoot.attrib.get('Rschr')
    if entry:
        fldbk.eResearcher.setPlainText(entry)
      
    fldbk.eDate.clear()
    entry = egRoot.attrib.get('Date')
    if entry:
        fldbk.eDate.setPlainText(entry)
      
    fldbk.eUpdated.clear()
    entry = egRoot.attrib.get('Update')
    if entry:
        fldbk.eUpdated.setPlainText(entry)
      
    fldbk.eLine.clear()
    entry = egRoot.findtext('Line')
    if entry:
        entry = formattingHandlers.XMLtoRTF(entry)
        fldbk.eLine.setHtml(entry)
    else:
        fldbk.eLine.setFontItalic(0)
        fldbk.eLine.setFontUnderline(0)
        fldbk.eLine.setFontWeight(50)        

    fldbk.eL1Gloss.clear()
    entry = egRoot.findtext('L1Gloss')
    if entry:
        entry = formattingHandlers.XMLtoRTF(entry)
        fldbk.eL1Gloss.setHtml(entry)
    else:
        fldbk.eL1Gloss.setFontItalic(0)
        fldbk.eL1Gloss.setFontUnderline(0)
        fldbk.eL1Gloss.setFontWeight(50)  

    fldbk.eL2Gloss.clear()
    entry = egRoot.findtext('L2Gloss')
    if entry:
        entry = formattingHandlers.XMLtoRTF(entry)
        fldbk.eL2Gloss.setHtml(entry)
    else:
        fldbk.eL2Gloss.setFontItalic(0)
        fldbk.eL2Gloss.setFontUnderline(0)
        fldbk.eL2Gloss.setFontWeight(50)

    fldbk.eExScrollArea.horizontalScrollBar().setValue(0)
    fldbk.eAnalysis.clear()
    fldbk.eAnalysis.setColumnCount(0)
    if egRoot.findtext('Mrph') is not None and len(egRoot.findtext('Mrph')) != 0:
        entryRow1 = egRoot.findtext('Mrph').split('\t')
        entryRow2 = egRoot.findtext('ILEG').split('\t')
        #need to handle case where the two lines have different numbers of cells (BAD!)
        if len(entryRow1) > len(entryRow2):
            while len(entryRow1) > len(entryRow2):
                entryRow2.append('[—]')
        elif len(entryRow1) < len(entryRow2):
            while len(entryRow1) < len(entryRow2):
                entryRow1.append('[—]')
        fldbk.eAnalysis.setRowCount(2)
        fldbk.eAnalysis.setColumnCount(len(entryRow1))
        fldbk.eAnalysis.setRowHeight(0, 20)
        fldbk.eAnalysis.setRowHeight(1, 20)
        for i in range(len(entryRow1)):
            morphs = entryRow1[i]
            morphs = morphs.replace(' ', '')
            if morphs == '':
                morphs = '[—]'
            parse = entryRow2[i]
            parse = parse.replace(' ', '')
            if parse == '':
                parse = '[—]'
            newContent, parse = formattingHandlers.smallCapsConverter(parse)
            tableCellTop = QtWidgets.QTableWidgetItem(1001)
            tableCellTop.setText(morphs)
            fldbk.eAnalysis.setItem(0, i, tableCellTop)
            tableCellBottom = QtWidgets.QTableWidgetItem(1001)
            tableCellBottom.setText(parse)
            tableCellBottom.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)
            fldbk.eAnalysis.setItem(1, i, tableCellBottom)
            fldbk.eAnalysis.resizeColumnToContents(i)
    lastColumn = fldbk.eAnalysis.columnCount()
    fldbk.eAnalysis.insertColumn(lastColumn)
    lastHeadWidget = QtWidgets.QTableWidgetItem(1001)
    lastHeadWidget.setText('+')
    fldbk.eAnalysis.setHorizontalHeaderItem(lastColumn, lastHeadWidget)
    fldbk.eAnalysis.resizeColumnToContents(lastColumn)
    rowHeader = QtWidgets.QTableWidgetItem(1001)
    rowHeader.setText('Morph')   
    fldbk.eAnalysis.setVerticalHeaderItem(0, rowHeader)
    rowHeader = QtWidgets.QTableWidgetItem(1001)
    rowHeader.setText('ILEG')   
    fldbk.eAnalysis.setVerticalHeaderItem(1, rowHeader)
    if egRoot.findtext('Synt') is not None:
        syntList = egRoot.findall('Synt')
        for item in syntList:
            rowHeader = QtWidgets.QTableWidgetItem(1001)
            rowHeader.setText(item.attrib.get('Tier'))
            lastRow = fldbk.eAnalysis.rowCount()
            fldbk.eAnalysis.insertRow(lastRow)
            fldbk.eAnalysis.setVerticalHeaderItem(lastRow, rowHeader)
            tagsList = item.text.split("\t")
            for t, tag in enumerate(tagsList):
                itemWidget = QtWidgets.QTableWidgetItem(1001)
                itemWidget.setText(tag)
                fldbk.eAnalysis.setItem(fldbk.eAnalysis.rowCount()-1, t, itemWidget)
    for i in range(0, fldbk.eAnalysis.rowCount()):
        inertWidget = QtWidgets.QTableWidgetItem(1001)
        inertWidget.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
        fldbk.eAnalysis.setItem(1, lastColumn, inertWidget)
    lastCol = fldbk.eAnalysis.columnCount()-1
    for i in range(0, fldbk.eAnalysis.rowCount()):
        newItem = QtWidgets.QTableWidgetItem(1001)
        # flags = QtCore.Qt.ItemFlag()
        flags = newItem.flags()
        if flags != QtCore.Qt.ItemFlag.ItemIsEnabled:
            newItem.setFlags(flags)
        fldbk.eAnalysis.setItem(i, lastCol, newItem)   
    if dataIndex.displayOrthography == "Phonetic":
        mapping = dataIndex.root.find('Orthography[@Name="%s"]'%dataIndex.root.get('Orth')).text
        pairList = mapping.split(';')   
        Orthographies.changeExDisplay(fldbk, pairList)
        fldbk.eOrthography.setCurrentIndex(fldbk.eOrthography.findText("Phonetic"))
    else:
        fldbk.eOrthography.setCurrentIndex(fldbk.eOrthography.findText(dataIndex.root.get('Orth')))
    try:
        for c in range(0, fldbk.eAnalysis.columnCount()-1):
            fldbk.eAnalysis.delegate.boundaryChecker(1, c)
    except AttributeError:
        pass
    
    fldbk.eNotes.clear()
    entry = egRoot.findtext('Comments')
    if entry:
        entry = formattingHandlers.XMLtoRTF(entry)
        fldbk.eNotes.setHtml(entry)
    else:
        fldbk.eNotes.setFontItalic(0)
        fldbk.eNotes.setFontUnderline(0)
        fldbk.eNotes.setFontWeight(50)
        
    """''Recordings"""
#    fldbk.eRecordings.setItemData(0, dataIndex.lastEx, 33)
    fldbk.eSound.loadMedia(egRoot)

def breakLines(text, lineLength, indent=None):
    wrapper = textwrap.TextWrapper()
    if indent is not None:
      wrapper.initial_indent = indent
      wrapper.subsequent_indent = indent
    wrapper.width = lineLength
    textList = wrapper.wrap(text)
    newText = ''
    newText = '<br />'.join(textList)
    return newText

def loadDefinitions(fldbk, lexRoot):
    fldbk.lL1Definition.clear()
    fldbk.lL1Definition.verticalScrollBar().setValue(0)
    fldbk.lL1Definition.horizontalScrollBar().setValue(0)
    fldbk.lL2Definition.clear()
    fldbk.lL2Definition.verticalScrollBar().setValue(0)
    fldbk.lL2Definition.horizontalScrollBar().setValue(0)
    subentry = lexRoot.findall('Def')
    L1DefList = []
    L2DefList = []
    for i in range(0, len(subentry)):
        #L1
        entry = ''
        dialect = ''
        variant = ''
        alternative = ''
        POS = subentry[i].findtext('POS')
        index = subentry[i].attrib.get('Index')
        try:
            if subentry[i].attrib.get('L1Index') is not None:
                L1Index = subentry[i].attrib.get('L1Index') #check to see if there are index words for the subentry
                if len(fldbk.lPrimaryIndex.toPlainText()) == 0: 
                    #if there are no indices from other subentries in the field on the card
                    L1Index += '(' + index + ')'
                    fldbk.lPrimaryIndex.setPlainText(L1Index)
                else:
                    #otherwise add new indices to old with semi-colons as separators
                    newIndex = fldbk.lPrimaryIndex.toPlainText().strip() + '; ' + L1Index + '(' + index + ')'
                    fldbk.lPrimaryIndex.setPlainText(newIndex)
        except AttributeError:
            pass
        try:
            if subentry[i].attrib.get('L2Index') is not None:
                L2Index = subentry[i].attrib.get('L2Index') #same as above for L1Index
                if len(fldbk.lSecondaryIndex.toPlainText()) == 0:
                    L2Index += '(' + index + ')'
                    fldbk.lSecondaryIndex.setPlainText(L2Index)
                else:
                    newIndex = fldbk.lSecondaryIndex.toPlainText().strip() + '; ' + L2Index + '(' + index + ')'
                    fldbk.lSecondaryIndex.setPlainText(newIndex)
        except AttributeError:
            pass
        if POS:
            entry = "(" + POS + ") "
        Reg = subentry[i].findtext('Reg')
        dNode = subentry[i].find('Dia')
        if dNode is not None:
            dialect = dNode.attrib.get('Dialect')
            entry = entry + " <i>" + dialect + "</i> "
            aNodeList = dNode.findall('Alternative')
            if len(aNodeList) != 0:
                crossRefList = []
                altList = []
                j = 0
                for item in aNodeList:
                    variant = item.attrib.get('Variant')
                    crossref = item.attrib.get('CrossRef')
                    alternative = item.text
                    if j == 0 and j == len(aNodeList) - 1:
                        entry = entry + "[" + variant + " " + alternative + "] "
                    elif j == 0:
                        entry = entry + "[" + variant + " " + alternative
                    elif j == len(aNodeList) - 1:
                        entry = entry + "; " + variant + " " + alternative + "] "
                    else:
                        entry = entry + "; " + variant + " " + alternative
                    if crossref:
                        crossRefList.append(crossref)
                        altList.append(alternative)
                    if len(crossRefList) != 0:
                        field = 'lL1Definition'
                        contextMenus.buildContextMenu(field, crossRefList, altList)
                    j += 1
                  
        if Reg:
            entry = entry + "<i>" + Reg + "</i> "
        entry2 = entry
        entry = entry + subentry[i].findtext('L1')
        try:
            entry = entry + ' [' + subentry[i].findtext('Cxt').strip() + ']'
        except AttributeError:
            pass
        entry = formattingHandlers.XMLtoRTF(entry)
        exampleList = []
        exampleList2 = []
        examples = subentry[i].findall('Ln')
        if examples:
            for j in range(0, len(examples)):
                egID = examples[j].attrib.get('LnRef')
                egElement = dataIndex.exDict[egID]
                eg = '<i>' + egElement.findtext('Line') + '</i>'
                try:
                    if len(egElement.findtext('L1Gloss')) != 0:
                        eg = eg + " ‘" + egElement.findtext('L1Gloss') + "’ (" 
                except TypeError:
                    eg = eg + " ‘" + egElement.findtext('L2Gloss') + "’ ("
                eg = eg + egElement.attrib.get('Spkr') + ")"
                eg = re.sub('{i}', '', eg)
                eg = re.sub('{/i}', '', eg)
                eg += "@" + egID
                exampleList.append(eg)

                eg2 = '<i>' + egElement.findtext('Line') + '</i>'
                try: 
                    if len(egElement.findtext('L2Gloss')) != 0:
                        eg2 = eg2 + " ‘" + egElement.findtext('L2Gloss') + "’ (" 
                except TypeError:
                    eg2 = eg2 + " ‘" + egElement.findtext('L1Gloss') + "’ ("
                eg2 = eg2 + egElement.attrib.get('Spkr') + ")"
                eg2 = re.sub('{i}', '', eg2)
                eg2 = re.sub('{/i}', '', eg2)
                eg2 += "@" + egID
                exampleList2.append(eg2)

        L1DefList.append([index, entry, exampleList])

        """L2"""
        try:
            entry2 = entry2 + subentry[i].findtext('L2')
            entry2 = formattingHandlers.XMLtoRTF(entry2)
            L2DefList.append([index, entry2, exampleList2])
        except TypeError:
            pass
          
    if len(subentry) == 1:
        i = 0
        cWidth = 681
        fldbk.lL1Definition.setColumnCount(1)
        fldbk.lL2Definition.setColumnCount(1)
        fldbk.lL1Definition.setColumnWidth(0, cWidth)
        fldbk.lL2Definition.setColumnWidth(0, cWidth)
    else:
        i = 1
        cWidth = 645
        fldbk.lL1Definition.setColumnCount(2)
        fldbk.lL1Definition.setColumnWidth(0, 25)
        fldbk.lL1Definition.setColumnWidth(1, cWidth)
        fldbk.lL2Definition.setColumnCount(2)
        fldbk.lL2Definition.setColumnWidth(0, 25)
        fldbk.lL2Definition.setColumnWidth(1, cWidth)

#    L1DefList = sorted(L1DefList, key = lambda x: int(x[0][0]))
#    L2DefList = sorted(L2DefList, key = lambda x: int(x[0][0]))
    j = 0
    for item in L1DefList:
        fldbk.lL1Definition.insertRow(j)
        if i == 1:
            indexTag = item[0] + ")"
            tableCell = QtWidgets.QTableWidgetItem()
            tableCell.setText(indexTag)
            tableCell.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            fldbk.lL1Definition.setItem(j, 0, tableCell)
        tableCell = QtWidgets.QTableWidgetItem()
        tableCell.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
        tableCell.setTextAlignment(QtCore.Qt.TextFlag.TextWordWrap)
        text = breakLines(item[1], 100)
        tableCell.setText(text)
        tableCell.setSizeHint(QtCore.QSize(cWidth, 16))
        fldbk.lL1Definition.setItem(j, i, tableCell)
        if len(item[2]) !=0:
            for eg in item[2]:
                j += 1
                fldbk.lL1Definition.insertRow(j)
                tableCell = QtWidgets.QTableWidgetItem()
                egIndex = eg.split("@")
                text = breakLines(egIndex[0], 120, '&nbsp;&nbsp;&nbsp;')
                tableCell.setText(text)
                tableCell.setData(35, egIndex[1])
                tableCell.setTextAlignment(QtCore.Qt.TextFlag.TextWordWrap)
                tableCell.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                fldbk.lL1Definition.setItem(j, i, tableCell)
        j += 1
    fldbk.lL1Definition.resizeRowsToContents()
    j = 0
    for item in L2DefList:
        fldbk.lL2Definition.insertRow(j)
        if i == 1:
            indexTag = item[0] + ")"
            tableCell = QtWidgets.QTableWidgetItem()
            tableCell.setText(indexTag)
            tableCell.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            fldbk.lL2Definition.setItem(j, 0, tableCell)
        tableCell = QtWidgets.QTableWidgetItem()
        text = breakLines(item[1], 100)
        tableCell.setText(text)
        tableCell.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
        tableCell.setTextAlignment(QtCore.Qt.TextFlag.TextWordWrap)
        fldbk.lL2Definition.setItem(j, i, tableCell)
        if len(item[2]) !=0:
            for eg in item[2]:
                j += 1
                fldbk.lL2Definition.insertRow(j)
                tableCell = QtWidgets.QTableWidgetItem()
                egIndex = eg.split("@")
                text = breakLines(egIndex[0], 120, '&nbsp;&nbsp;&nbsp;')
                tableCell.setText(text)
                tableCell.setData(35, egIndex[1])
                tableCell.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                tableCell.setTextAlignment(QtCore.Qt.TextFlag.TextWordWrap)
                fldbk.lL2Definition.setItem(j, i, tableCell)
        j += 1
    fldbk.lL2Definition.resizeRowsToContents()

def loadLexCard(lexRoot, navBtn=False):
    fldbk = dataIndex.fldbk
    targetCard = lexRoot.attrib.get('LexID')
    dataIndex.currentCard = targetCard
    dataIndex.lastLex = lexRoot.attrib.get('LexID')   
    dataIndex.root.set('LastLex', dataIndex.lastLex)
    if navBtn is False:
        if len(fldbk.lNavBar.stack) == 0:
            fldbk.lNavBar.stack.append(targetCard)
            fldbk.lNavBar.index = fldbk.lNavBar.index + 1
        elif fldbk.lNavBar.stack[-1] != targetCard:
            fldbk.lNavBar.stack.append(targetCard)
            fldbk.lNavBar.index = fldbk.lNavBar.index + 1
    try:
          del(fldbk.lGrammar.crossrefMenu)
    except AttributeError:
        pass
          
    try:
        del(fldbk.lDialect.dialectMenu)
    except AttributeError:
        pass
    
    try:
        del(fldbk.lL1Definition.L1DefinitionMenu)
    except AttributeError:
        pass
    
    try:
        del(fldbk.lL2Definition.L2DefinitionMenu)
    except AttributeError:
        pass
    
    try:
        if lexRoot.attrib.get('Done') == '1':
            fldbk.lDoneBtn.setChecked(1)
        else:
            fldbk.lDoneBtn.setChecked(0)
    except (KeyError, AttributeError):
        fldbk.lDoneBtn.setChecked(0)
    
    fldbk.lOrthography.clear()
    entry = lexRoot.findtext('Orth')
    if entry:
      fldbk.lOrthography.setText(entry)

    fldbk.lPOS.clear()
    entry = lexRoot.findtext('POS')
    if entry:
      fldbk.lPOS.setPlainText(entry)

    fldbk.lRegister.clear()
    entry = lexRoot.findtext('Reg')
    if entry:
      fldbk.lRegister.setPlainText(entry)

    fldbk.lIPA.clear()
    entry = lexRoot.findtext('IPA')
    if entry:
      if "̰" in entry:
        entry = entry.replace("(̰)", "")
        lexRoot.find('IPA').text = entry
      fldbk.lIPA.setText(entry)

    fldbk.lLiteral.clear()
    entry = lexRoot.findtext('Lit')
    if entry:
        newContent,  entry = formattingHandlers.smallCapsConverter(entry)
        fldbk.lLiteral.setText(entry)

    """Grammar"""
    fldbk.lGrammar.clear()
    subentry = lexRoot.findall('Grm')
    grmList = ''
    entryList = []
    refList = []
    mediaRefs = []
    if len(subentry) != 0:
      for i in range(0, len(subentry)):
          if subentry[i].attrib.get('Prefix'):
              entry = "<i>" + subentry[i].attrib.get('Prefix') + ".</i> " + subentry[i].text
          else:
              entry = subentry[i].text
          if subentry[i].attrib.get('Variant'):
              entry += ' (' + subentry[i].attrib.get('Variant') + ')'
          if entry is None:
                 continue
        #TODO: the above is a hack in case we have a <Grm />, need to delete instead
          entry += "<br/>"
          grmList += entry
          if subentry[i].attrib.get('MediaRef'):
            entryList.append(subentry[i].text)
            refList.append(subentry[i].attrib.get('MediaRef'))
            mediaRefs.append(subentry[i].attrib.get('MediaRef'))
      fldbk.lGrammar.insertHtml(grmList)
        
    subentry = lexRoot.findall('C2')
    if subentry:
      c2List = '<i>also</i> '
      for i in range(0, len(subentry)):
          entry = subentry[i].text
          if subentry[i].attrib.get('Variant'):
              entry += " (" + subentry[i].attrib.get('Variant') + ")"
          if subentry[i].attrib.get('MediaRef'):
            entryList.append(entry)
            refList.append(subentry[i].attrib.get('MediaRef'))
            mediaRefs.append(subentry[i].attrib.get('MediaRef'))
          c2List = c2List + entry
          if i != len(subentry)-1:
              c2List = c2List + ', '
      if len(fldbk.lGrammar.toPlainText()) != 0:
          c2List = c2List
      fldbk.lGrammar.insertHtml(c2List)
      
    subentry = lexRoot.findall('Cf')
    if subentry:
      cfList = '<i>cf.</i> '
      for i in range(0, len(subentry)):
          entry = subentry[i].text
          if subentry[i].attrib.get('CrossRef'):
             entryList.append(entry)
             refList.append(subentry[i].attrib.get('CrossRef'))
             cfList = cfList + entry
          else:
              cfList = cfList + '<span style="color:blue">' + entry + '</span>'               
          if i != len(subentry)-1:
              cfList = cfList + ', '
      # if len(fldbk.lGrammar.toPlainText()) != 0:
      #     cfList = "<br />" + cfList
      fldbk.lGrammar.insertHtml(cfList)
    if refList:
        field = 'lGrammar'
        contextMenus.buildContextMenu(field, refList, entryList)

    """Indices"""
    fldbk.lPrimaryIndex.clear()
    entry = lexRoot.attrib.get('L1Index')
    if entry:
        fldbk.lPrimaryIndex.setPlainText(entry)

    fldbk.lSecondaryIndex.clear()
    entry = lexRoot.attrib.get('L2Index')
    if entry:
        fldbk.lSecondaryIndex.setPlainText(entry)

    """Comments"""
    fldbk.lNotes.clear()
    entry = lexRoot.findtext('Comments')
    if entry:
        entry = formattingHandlers.XMLtoRTF(entry)
        fldbk.lNotes.setHtml(entry)
    else:
        fldbk.lNotes.setFontItalic(0)
        fldbk.lNotes.setFontUnderline(0)
        fldbk.lNotes.setFontWeight(50)
    
    fldbk.lKeywordIndex.clear()
    entry = lexRoot.attrib.get('Kywd')
    if entry:
        fldbk.lKeywordIndex.setPlainText(entry)

    """Dialect"""
    fldbk.lDialect.clear()
    ##dia = ''
    entry = ''
    subentry = lexRoot.find('Dia')
    if subentry is not None:
        dialect = subentry.attrib.get('Dialect')
        entry = entry + " <i>" + dialect + "</i> "
        aNodeList = subentry.findall('Alternative')
        if len(aNodeList) != 0:
            crossRefList = []
            altList = []
            j = 0
            for item in aNodeList:
                alternative = item.text
                variant = item.attrib.get('Variant')
                crossref = item.attrib.get('CrossRef')
                if j == 0 and j == len(aNodeList) - 1:
                    entry = entry + " (" + variant + " " + alternative + ")"
                elif j == 0:
                    entry = entry + " (" + variant + " " + alternative
                elif j == len(aNodeList) - 1:
                    entry = entry + "; " + variant + " " + alternative + ")"
                else:
                    entry = entry + "; " + variant + " " + alternative
                j += 1
                if crossref:
                    crossRefList.append(crossref)
                    altList.append(alternative)
                if len(crossRefList) != 0:
                    field = 'lDialect'
                    contextMenus.buildContextMenu(fldbk, field, crossRefList, altList)
        fldbk.lDialect.insertHtml(entry)
           
    fldbk.lBrrw.clear()
    subentry = lexRoot.find('Brrw')
    if subentry is not None:
        source = subentry.attrib.get('Source')
        cognate = lexRoot.findtext('Brrw')
        cognate = '“' + cognate + '”'
        borrowing = source + ' ' + cognate
        fldbk.lBrrw.setPlainText(borrowing)

    """Metadata"""
    fldbk.lSource.clear()
    fldbk.lResearcher.clear()
    fldbk.lDate.clear()
    fldbk.lUpdated.clear()
    fldbk.lConfirmed.clear()
    entry = lexRoot.attrib.get('Spkr')
    if entry:
      fldbk.lSource.setPlainText(entry)
 
    entry = lexRoot.attrib.get('Rschr')
    if entry:
      fldbk.lResearcher.setPlainText(entry)
      
    entry = lexRoot.attrib.get('Date')
    if entry:
      fldbk.lDate.setPlainText(entry)

    entry = lexRoot.attrib.get('Update')
    if entry:
      fldbk.lUpdated.setPlainText(entry)

    entry = lexRoot.attrib.get('Confirmed')
    if entry:
      fldbk.lConfirmed.setPlainText(entry)

    """Definitions and examples"""
    loadDefinitions(fldbk, lexRoot)
    
    """Derivations"""
    fldbk.lDerivatives.clear()
    fldbk.lRemoveDerBtn.setEnabled(0)
    derivatives = lexRoot.findall('Drvn')
    parent = None
    if derivatives:
        fldbk.lDerivatives.setAlternatingRowColors(True)
        for i in range(0, len(derivatives)):
            text = ''
            derID = derivatives[i].attrib.get('LexIDREF')
            der = dataIndex.lexDict[derID]
            word = der.findtext('Orth')
            POS = der.findtext('POS')
            L1 = der.findtext('Def/L1')
            if POS:
                text = word + " (" + POS + ") " + L1
            item = QtWidgets.QListWidgetItem(parent, QtWidgets.QListWidgetItem.ItemType.UserType)
            item.setData(32, derID)
            item.setText(text)
            fldbk.lDerivatives.addItem(item)
        fldbk.lRemoveDerBtn.setEnabled(1)
        try:
            fldbk.lDerivatives.sortItems(QtCore.Qt.SortOrder.AscendingOrder)
        except AttributeError:
            pass

    """Bases"""
    fldbk.lBase.clear()
    fldbk.lBreakLnkBtn.setEnabled(0)
    base = lexRoot.find('Root')
    if base is not None:
        baseID = base.attrib.get('LexIDREF')
        baseElement = dataIndex.lexDict[baseID]
        baseName = baseElement.findtext('Orth')
        item = QtWidgets.QListWidgetItem(parent, QtWidgets.QListWidgetItem.ItemType.UserType)
        item.setData(32, baseID)
        item.setText(baseName)
        fldbk.lBase.addItem(item)
        fldbk.lBreakLnkBtn.setEnabled(1)

    """Recordings"""
    fldbk.lSound.loadMedia(lexRoot, mediaRefs)
    resetNavBars(fldbk.lLexNav, dataIndex.currentCard)

def resetNavBars(navBar, tCard):
    """navbar = listwidget being manipulated"""
    for i in range(0, navBar.model().rowCount()):
        if navBar.model().index(i, 0).data(32) == tCard:
            navBar.setCurrentIndex(navBar.model().index(i, 0))
            break
    navBar.scrollTo(navBar.currentIndex(), QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)

def unparsedLineBuilder(child, j):
    if child.attrib.get('SpokenBy'):
        spokenBy = child.attrib.get('SpokenBy') + ': '
    else:
        spokenBy = ''
    if len(child.text.split('\n')) == 2:
        line = child.text.split('\n')[0]
        line2 = spokenBy + '‘' + child.text.split('\n')[1].strip() + '’'
    else:
        line = spokenBy + child.text
        line2 = None
    if child.attrib.get('Time'):
        timeCode = child.attrib.get('Time')
        if line2 is not None:
            line2 += ' [' + timeCode + ']'
        else:
            line += ' [' + timeCode + ']'
    newTable = textTable.textTable(parent=None)
    newTable.setRowCount(1)
    newTable.setColumnCount(1)
    newTable.setRowHeight(0, 20)
    newTable.setMinimumHeight(20)
    newTable.setMaximumHeight(20)
    newTable.setVerticalHeaderLabels(["", ""])
    tableCellNumber = QtWidgets.QTableWidgetItem(1001)
    tableCellNumber.setText(str(j+1))
    newTable.setVerticalHeaderItem(0, tableCellNumber)
    tableCellLine = QtWidgets.QTableWidgetItem(10001)
    tableCellLine.setText(line)
    newTable.setItem(0, 0, tableCellLine)
    if line2 is not None:
        newTable.setMinimumHeight(40)
        newTable.setMaximumHeight(40)
        newTable.setRowCount(2)
        newTable.setRowHeight(1, 20)
        tableCellGloss = QtWidgets.QTableWidgetItem(10001)
        tableCellGloss.setText(line2)
        newTable.setItem(1, 0, tableCellGloss)
        tableCellNumber = QtWidgets.QTableWidgetItem(1001)
        tableCellNumber.setText('')
        newTable.setVerticalHeaderItem(1, tableCellNumber)
    newTable.resizeColumnToContents(0)
    return newTable
    
def addTextWidget(fldbk, textRoot):
    """
    adds a table for every line in the text. cell 0 of vertical header
    contains a line number, data 35 is a cross-ref to an EX and data 36 is the
    Ln node represented by the table
    """
    numLines = len(textRoot.findall('Ln'))
    progDialog = QtWidgets.QProgressDialog("Loading text ...", "Stop", 0, numLines, fldbk)
    progDialog.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
    progDialog.setWindowTitle('Loading')
    j = 0
    fldbk.tText.setVisible(0)
    while fldbk.textLayout.count():
        item = fldbk.textLayout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
    for child in textRoot.iter('Ln'):
        if child.attrib.get('LnRef'):
            lineRef = child.attrib.get('LnRef')
            spokenBy = child.attrib.get('SpokenBy')
            progDialog.setValue(j)
            if (progDialog.wasCanceled()):
                break
            node = dataIndex.exDict[lineRef]
            newTable = textTableBuilder(node, j, spokenBy, child)
        else:
            newTable = unparsedLineBuilder(child, j)
        newTable.verticalHeaderItem(0).setData(36, child)
        fldbk.textLayout.addWidget(newTable)
        j += 1
    fldbk.textLayout.insertStretch(-1, 100)
    progDialog.setValue(numLines)
    fldbk.tText.setVisible(1)
    if dataIndex.lastText != dataIndex.currentCard:
        dataIndex.unsavedEdit = 1
