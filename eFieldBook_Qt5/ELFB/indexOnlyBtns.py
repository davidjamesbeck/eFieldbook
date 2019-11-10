from PyQt5 import QtGui, QtCore, QtWidgets
from ELFB import dataIndex, cardLoader, formattingHandlers, autoparsing
from ELFB.searchClasses import SearchEngine
from ELFB.palettes import RecordBrowser

def buildIndex():
    fldbk = dataIndex.fldbk
    indexList = []
    errorList = []
    dict = dataIndex.exDict
    fldbk.iErrorBox.clear()
    fldbk.iSortingBox.setCurrentIndex(0)
    tokenCount = 0
    for key in dict:
        try:
            line = dict[key].find('Line').text
            lineList = autoparsing.cleanLine(line)
            morphList = dict[key].find('Mrph').text.split('\t')
            glossList = dict[key].find('ILEG').text.split('\t')
            for i in range(0, len(morphList)):
                morph = morphList[i]
                if len(morph) == 0:
                    morph = '[-]'
                gloss = glossList[i]
                if len(gloss) == 0:
                    gloss = '[-]'
                indexList.append(lineList[i] + '\t' + morph + '\t' + gloss + '\t' + key + ':' + str(i+1) + '\n')
                tokenCount +=1
        except (TypeError, AttributeError):
            pass
        except IndexError:
            errorList.append(key)
    if len(errorList) != 0:
        for key in errorList:
            item = QtWidgets.QListWidgetItem()
            item.setText(key)
            fldbk.iErrorBox.addItem(item)
    indexList = sorted(indexList)
    prevMorph = ''
    trimmedList = []
    for i, item in enumerate(indexList):
        index = item.index('\tEX')
        if item[:index-1] != prevMorph:
            prevMorph = item[:index-1]
            trimmedList.append(item)
        else:
            trimmedList[-1] = trimmedList[-1][:-1] + item[index:]
    
    indexString = ''.join(trimmedList)[:-1]
    wordformCount = formattingHandlers.addCommas(len(trimmedList))
    tokenCount = formattingHandlers.addCommas(tokenCount)
    fldbk.iIndex.setText(indexString)
#    fldbk.tabWidget.setCurrentIndex(7)
    fldbk.iWordformLbl.setText("Wordforms: " + str(wordformCount))
    fldbk.iTokensLbl.setText("Tokens: " + str(tokenCount))
    fldbk.iSortNowBtn.setStyleSheet('background: #6698FF;')
    
def iDelAbbr(fldbk):
    '''remove abbreviation from list'''
    try:
        badNode = fldbk.iAbbreviations.currentItem().data(36)
        badRow = fldbk.iAbbreviations.currentRow()
        fldbk.iAbbreviations.removeRow(badRow)
        fldbk.eAbbreviations.removeRow(badRow)
    except AttributeError:
        return
    ##update XML
    dataIndex.root.find('Abbreviations').remove(badNode)
    dataIndex.unsavedEdit = 1

def indexBrowser(fldbk):
    if len(fldbk.iIndex.toPlainText()) != 0:
        cursor = fldbk.iIndex.textCursor()
        if cursor.selectedText():
            cursor.clearSelection()
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        selection = cursor.selectedText()
        try:
            fldbk.recordBrowser.close()
        except AttributeError:
            pass
        fldbk.recordBrowser = RecordBrowser.RecordBrowser(fldbk, selection)
        fldbk.recordBrowser.setObjectName('recordBrowser')
        fldbk.recordBrowser.setWindowTitle('Browse index')
        fldbk.recordBrowser.setModal(0)
        fldbk.recordBrowser.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowStaysOnTopHint)
        fldbk.recordBrowser.show()
        fldbk.recordBrowser.raise_()

def findForm(fldbk):
    '''go to the example selected'''
    cursor = fldbk.iIndex.textCursor()
    if cursor.selectedText():
        cursor.clearSelection()
    cursor.select(QtGui.QTextCursor.WordUnderCursor)
    selection = cursor.selectedText()
    try:
        tEntry = dataIndex.exDict[selection]
        cardLoader.loadExCard(tEntry)
        fldbk.tabWidget.setCurrentIndex(3)
    except KeyError:
        pass
        
def makeSet(fldbk):
    cursor = fldbk.iIndex.textCursor()
    if cursor.selectedText():
        cursor.clearSelection()
    cursor.select(QtGui.QTextCursor.LineUnderCursor)
    selection = cursor.selectedText()
    list = selection.split('\t')
    list = list[3:]
    searchEngine = SearchEngine(fldbk)
    for item in list:
        index = item.index(':')
        newItem = item[:index]
        hit = dataIndex.exDict[newItem]
        SearchEngine.displayExResults(searchEngine, hit)
    fldbk.tabWidget.setCurrentIndex(5)
    
def updateWordForms(fldbk):
    cursor = fldbk.iIndex.textCursor()
    if cursor.selectedText():
        cursor.clearSelection()
    cursor.select(QtGui.QTextCursor.LineUnderCursor)
    selection = cursor.selectedText()
    list = selection.split('\t')
    morphs = list[1]
    analysis = list[2]
    list = list[3:]
    for item in list:
        parts = item.split(':')
        ID = parts[0]
        stringIndex = parts[1]
        index = int(stringIndex) - 1
        node = dataIndex.exDict[ID]
        morphNode = node.find('Mrph').text
        glossNode = node.find('ILEG').text
        morphList = morphNode.split('\t')
        glossList = glossNode.split('\t')
        morphList[index] = morphs
        glossList[index] = analysis
        morphNode = '\t'.join(morphList)
        glossNode = '\t'.join(glossList)
        node.find('Mrph').text = morphNode
        node.find('ILEG').text = glossNode

def findFirst(fldbk):
    if len(fldbk.iFindInIndex.text()) != 0:
        if fldbk.iIndex.find(fldbk.iFindInIndex.text()) == False:
            fldbk.iIndex.moveCursor(QtGui.QTextCursor.Start)
            fldbk.iIndex.find(fldbk.iFindInIndex.text())

def sortNow(fldbk):
    index = fldbk.iSortingBox.currentIndex()
    clearHighlighting(fldbk)
    if len(fldbk.iIndex.toPlainText()) == 0:
        return
    indexString = fldbk.iIndex.toPlainText()
    sortIndex(fldbk, indexString, index)
    
def sortIndex(fldbk,indexString,index=0):
    '''have to trap this because fieldbook.py triggers this routine 
    when it fills the Sorting bos on the index card (and there is no index to sort)'''
    try:
        indexList = indexString.split('\n')
    except AttributeError:
        return
    indexListList = []
    for item in indexList:
        itemList = item.split('\t')
        indexListList.append(itemList)
    sortedIndexList = sorted(indexListList,  key = lambda s: s[index])
    finalList = []
    for item in sortedIndexList:
        itemString = '\t'.join(item)
        finalList.append(itemString)
    indexString = '\n'.join(finalList)
    if indexString[0] == '\n':
        indexString = indexString[1:]
    fldbk.iIndex.setText(indexString)
    fldbk.iSortNowBtn.setStyleSheet('background: #6698FF;')
    wordformCount = formattingHandlers.addCommas(len(indexList))
    fldbk.iWordformLbl.setText("Wordforms: " + str(wordformCount))
    
def showDuplicates(fldbk):
    cursor = fldbk.iIndex.textCursor()
    document = fldbk.iIndex.document()
    cursor.select(QtGui.QTextCursor.Document)
    format = QtGui.QTextCharFormat()
    format.setBackground(QtCore.Qt.white)
    cursor.setCharFormat(format)    
    if fldbk.iSortingBox.currentIndex() == -1:
        index = 0
    else:
        index = fldbk.iSortingBox.currentIndex()
    lineList = fldbk.iIndex.toPlainText().split('\n')
    lineItemsList = []
    for line in lineList:
        lineItems = line.split('\t')
        lineItemsList.append(lineItems)
    i = 0
    while i != len(lineList)-1:
        if lineItemsList[i][index] == lineItemsList[i+1][index]:
            firstBlock = document.findBlockByNumber(i).position()
            cursor.setPosition(firstBlock)
            cursor.movePosition(QtGui.QTextCursor.NextBlock, QtGui.QTextCursor.KeepAnchor)
            cursor.movePosition(QtGui.QTextCursor.EndOfBlock, QtGui.QTextCursor.KeepAnchor)
            format = QtGui.QTextCharFormat()
            format.setBackground(QtCore.Qt.yellow)
            cursor.setCharFormat(format)           
        i += 1
        
def clearHighlighting(fldbk):
    cursor = fldbk.iIndex.textCursor()
    cursor.select(QtGui.QTextCursor.Document)
    format = QtGui.QTextCharFormat()
    format.setBackground(QtCore.Qt.white)
    cursor.setCharFormat(format)    
