from PyQt5 import QtWidgets, QtCore
from ELFB import dataIndex, indexOnlyBtns
from ELFB.palettes import HomophoneManager
import re

def doParse():
    fldbk = dataIndex.fldbk
    line = fldbk.eLine.toPlainText()
    if len(fldbk.eL1Gloss.toPlainText()) != 0:
        gloss = fldbk.eL1Gloss.toPlainText()
    elif len(fldbk.eL2Gloss.toPlainText()) != 0:
        gloss = fldbk.eL1Gloss.toPlainText()
    else:
        gloss = ''
    try:
        if len(fldbk.eAnalysis.item(0, 0).text()) == 0:
            noParse = True
        elif not fldbk.eAnalysis.item(1, 0):
            noParse = True
        else:
            noParse = False
    except AttributeError:
        noParse = True
    if fldbk.eAnalysis.columnCount() <= 2 and noParse == True:
        fldbk.eAnalysis.setColumnCount(0)
        wordList = cleanLine(line)
        fldbk.eAnalysis.setColumnCount(len(wordList)+1)
        for i, word in enumerate(wordList):
            newMorphs, newAnalysis = autoParse(word, line, gloss)
            if newMorphs == None:
                newMorphs = word
                newAnalysis = "[—]"
            newItem = QtWidgets.QTableWidgetItem(1001)
            newItem.setText(newMorphs)
            fldbk.eAnalysis.setItem(0, i, newItem)
            newItem = QtWidgets.QTableWidgetItem(1001)
            newItem.setText(newAnalysis)
            fldbk.eAnalysis.setItem(1, i, newItem)
            fldbk.eAnalysis.resizeColumnToContents(i)
        inertItem = QtWidgets.QTableWidgetItem(1001)
        flags = QtCore.Qt.ItemFlags()
        flags != QtCore.Qt.ItemIsEnabled
        inertItem.setFlags(flags)
        fldbk.eAnalysis.setItem(0, i+1, inertItem)
        inertItem = QtWidgets.QTableWidgetItem(1001)
        inertItem.setFlags(flags)
        fldbk.eAnalysis.setItem(1, i+1, inertItem)
        lastHeadWidget = QtWidgets.QTableWidgetItem(1001)
        lastHeadWidget.setText('+')
        fldbk.eAnalysis.setHorizontalHeaderItem(i+1,lastHeadWidget)
        fldbk.eAnalysis.resizeColumnToContents(i+1)
    else:
        wordList = cleanLine(line)
        for i in range(0, fldbk.eAnalysis.columnCount()):
            if fldbk.eAnalysis.item(1, i).text() == '[—]':
                newMorphs,  newAnalysis = autoParse(wordList[i], line, gloss)
                fldbk.eAnalysis.item(1, i).setText(newAnalysis)
                fldbk.eAnalysis.item(0, i).setText(newMorphs)
    fldbk.eAnalysis.delegate.updateExample()
        
def autoParse(word, textLine=None, glossLine=None):
    fldbk = dataIndex.fldbk
    newMorphs = None
    newAnalysis = None
    if len(fldbk.iIndex.toPlainText()) != 0:
        Index = fldbk.iIndex.toPlainText()
        regex = re.compile('^%s' %word, re.MULTILINE)
        if regex.search(Index):
            matchedLines = []
            for match in regex.finditer(Index):
                begin = match.start()
                try:
                    end = Index.index('\n', begin)
                except ValueError:
                    end = len(Index)
                line = Index[begin:end]
                lineList = line.split('\t')
                if lineList[0] == word:
                    matchedLines.append(lineList)
            if len(matchedLines) == 1:
                newMorphs = matchedLines[0][1]
                newAnalysis = matchedLines[0][2]
            elif len(matchedLines) > 1:
                homophoneList = []
                for line in matchedLines:
                    homophoneList.append(line[1] + ' ‘' + line[2] +'’')
                if dataIndex.homophoneDefaultChoice != None and word in dataIndex.homophoneDefaultChoice:
                    form = dataIndex.homophoneDefaultChoice[word]
                    newMorphs = form[0]
                    newAnalysis = form[1]
                else:
                    dialog = HomophoneManager.HomophoneManager(fldbk)
                    if textLine != None:
                        dialog.line.setPlainText(textLine)
                    if glossLine != None:
                        dialog.gloss.setPlainText(glossLine)
                    for item in homophoneList:
                        newItem = QtWidgets.QListWidgetItem()
                        newItem.setText(item)
                        dialog.alternativesList.addItem(newItem)
                    if dialog.exec_() and dialog.index != None:
                        lineMatch = matchedLines[dialog.index]
                        newMorphs = lineMatch[1]
                        newAnalysis = lineMatch[2]
                        if dialog.defaultSelect.isChecked():
                            if dataIndex.homophoneDefaultChoice == None:
                                dataIndex.homophoneDefaultChoice = {lineMatch[0] : [lineMatch[1], lineMatch[2]]}
                            else:
                                dataIndex.homophoneDefaultChoice[lineMatch[0]] = [lineMatch[1], lineMatch[2]]
    return newMorphs, newAnalysis
    
def askToBuildIndex():
    breakbox = QtWidgets.QMessageBox()
    breakbox.setIcon(QtWidgets.QMessageBox.Warning)
    breakbox.setText("Build index?")
    breakbox.setInformativeText('Full auto-parsing requires a morphological index to be generated. Do you want to build one now?')
    breakbox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
    breakbox.setDefaultButton(QtWidgets.QMessageBox.Ok)
    breakbox.exec_()
    if breakbox.result() == QtWidgets.QMessageBox.Ok:    
        indexOnlyBtns.buildIndex()
        return True
    else:
        return False

def cleanLine(line):
    #TODO: make it possible for users to define punctuation characters
    table = str.maketrans('','','!¡?¿.,/…-–—“”;')
    line = line.translate(table)
    p = re.compile('[\(\[\{<].*?[\)\]\}>]')
    line = p.sub('', line)
    while '  ' in line:
        line = line.replace('  ', ' ')
    line = line.strip()
    lineList = line.split(' ')
    return lineList

def storeUnparsedItem(item):
    '''this seems essentially to be a flag, either None or [--]'''
    if item.row() == 1:
        dataIndex.unparsedILEG = item
    
def updateIndex(column):
    fldbk = dataIndex.fldbk
    line = fldbk.eLine.toPlainText()
    lineList = cleanLine(line)
    word = lineList[column]
    morph = fldbk.eAnalysis.item(0, column).text()
    ileg = fldbk.eAnalysis.item(1, column).text()
    indexEntry = word + '\t' + morph + '\t' + ileg
    locatorID = '\t' + dataIndex.currentCard + ':' + str(column) + '\n'
    regex = re.compile('^%s' %indexEntry,  re.MULTILINE)
    Index = fldbk.iIndex.toPlainText()
    if regex.search(Index): #if this form is already in the index for some reason
        match = regex.search(Index)
        begin = match.start()
        try:
            end = Index.index('\n', begin)
        except ValueError:
            end = len(Index)
        head = Index[:end]
        tail = Index[end:]
        Index = head + locatorID[:-1] + tail
        fldbk.iIndex.setText(Index)
    else:
        indexEntry += locatorID
        Index += '\n'+ indexEntry
#        indexList = Index.split('\n')
        indexOnlyBtns.sortIndex(fldbk, Index)
#        Index = '\n'.join(indexList[1:])
#        fldbk.iIndex.setText(Index)
#        fldbk.iSortNowBtn.setStyleSheet('background: red;')
