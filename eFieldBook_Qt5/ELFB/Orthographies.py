from PyQt5 import QtWidgets
from ELFB import dataIndex, cardLoader
import re

def toIPA(string):
    string = string.replace("(')", "")
    ortho = dataIndex.root.attrib.get('Orth')
    if ortho == None:
        noOrthBox = QtWidgets.QMessageBox()
        noOrthBox.setIcon(QtWidgets.QMessageBox.Warning)
        noOrthBox.setText("No primary orthography")
        noOrthBox.setInformativeText('Set a primary orthography on the Metadata tab.')
        noOrthBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        noOrthBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
        noOrthBox.exec_()
        return
    mapping = dataIndex.root.findtext('Orthography[@Name="%s"]' %ortho)
    pairList = mapping.split(';')
    string = doTransform(string, pairList)
    return string
    
def doTransform(string, pairList):
    '''converts orthography into IPA'''
    quadrupletList = []
    for i, item in enumerate(pairList):
        segList = item.split(',')        
#        segIn = segList[0].strip()
        segOut= segList[1].strip()
        key = str(chr(i + 8704))
#        length = len(segIn)
#        quadruplet = [segIn, key, segOut, length]
        
        segIn = segList[0].strip()
        if segIn[0] == "#":
            segIn = '^' + segIn[1:]
            length = len(segIn) - 1
        elif segIn[-1] == "#":
            segIn = segIn[:-1] + '$'
            length = len(segIn) - 1
        else:
            length = len(segIn)
        regIn = re.compile(segIn)
        quadruplet = [regIn, key, segOut, length]
        
        quadrupletList.append(quadruplet)
    orderedList = sorted(quadrupletList,  key = lambda s: s[3],  reverse=True)
    for quad in orderedList:
#        string = string.replace(quad[0], quad[1])
        string = re.sub(quad[0], quad[1], string)
    for quad in orderedList:
        string = string.replace(quad[1], quad[2])
    return string

def doReverseTransform(string, pairList):
    '''converts IPA into orthography'''
    quadrupletList = []
    for i, item in enumerate(pairList):
        segList = item.split(',')        
        segIn = segList[0].strip()
        segIn = segIn.replace('#','')
        segOut= segList[1].strip()
        key = str(chr(i + 8704))
        length = len(segOut)
        quadruplet = [segOut, key, segIn, length]
        quadrupletList.append(quadruplet)
    orderedList = sorted(quadrupletList,  key = lambda s: s[3],  reverse=True)
    for quad in orderedList:
        string = string.replace(quad[0], quad[1])
    for quad in orderedList:
        string = string.replace(quad[1], quad[2])
    return string

def testTransform(fldbk, string):
    mapping = fldbk.oOrder.toPlainText()
    pairList = mapping.split(';')
    string = doTransform(string, pairList)
    return string

def fillOrthPickers(comboBox):
    comboBox.clear()
    if dataIndex.root.get('Orth'):
        comboBox.setEnabled(1)
        orthName = dataIndex.root.get('Orth')
        comboBox.insertItem(0,orthName)
        comboBox.insertItem(0,'Phonetic')
        dataIndex.displayOrthography = orthName
    else:
        comboBox.setEnabled(0)
        comboBox.setCurrentIndex(-1)

def changeDisplayOrthography(fldbk, index, type):
    if type == 'Txt':
        comboBox = fldbk.tOrthography
    else:
        comboBox = fldbk.eOrthography
    if dataIndex.displayOrthography != comboBox.currentText():
        if index != -1:
            '''the cardloader sends an index of -1 so that texts will automatically'''
            '''match the display orthography of example cards'''
            dataIndex.displayOrthography = comboBox.currentText()
        else:
            comboBox.setCurrentIndex(comboBox.findText(dataIndex.displayOrthography))
        baseOrthography = dataIndex.root.get('Orth')
        mapping = dataIndex.root.find('Orthography[@Name="%s"]'%baseOrthography).text
        pairList = mapping.split(';')
        if comboBox.currentText() == 'Phonetic':
            fldbk.eLine.setReadOnly(1)
            fldbk.eAnalysis.setEnabled(0)
            if type == 'Ex':
                changeExDisplay(fldbk, pairList)
            else:
                for table in fldbk.tText.children():
                    if table.objectName() != 'textLayout':
                        changeTextDisplay(fldbk, pairList, table)
        else:
            fldbk.eLine.setReadOnly(0)
            fldbk.eAnalysis.setEnabled(1)
            if type == 'Ex':
                cardLoader.loadExCard(dataIndex.exDict[dataIndex.currentCard])
            else:
                for table in fldbk.tText.children():
                    if table.objectName() != 'textLayout':
                        reverseTextDisplay(fldbk, pairList, table)

def changeExDisplay(fldbk, pairList):
    string = fldbk.eLine.toPlainText()
    string = doTransform(string, pairList)
    fldbk.eLine.setPlainText(string)
    for i in range(0, fldbk.eAnalysis.columnCount()):
        string = fldbk.eAnalysis.item(0, i).text()
        string = doTransform(string, pairList)
        fldbk.eAnalysis.item(0, i).setText(string)
        fldbk.eAnalysis.resizeColumnToContents(i)

def changeTextDisplay(fldbk, pairList, table):
    try:
        string = table.item(0, 0).text()
        string = doTransform(string, pairList)
        table.item(0, 0).setText(string)
        for i in range(0, table.columnCount()):
            string = table.item(1, i).text()
            string = doTransform(string, pairList)
            table.item(1, i).setText(string)
            if i == 0:
                topRow = table.takeItem(0, 0)
                bottomRow = table.takeItem(3, 0)
                table.resizeColumnToContents(0)
                table.setItem(0, 0, topRow)
                table.setItem(3, 0, bottomRow)
            else:
                table.resizeColumnToContents(i)
            
        table.setEnabled(0)
        return table
    except AttributeError:
        pass
        
def reverseTextDisplay(fldbk, pairList, table):
    try:
        string = table.item(0, 0).text()
        string = doReverseTransform(string, pairList)
        table.item(0, 0).setText(string)
        for i in range(0, table.columnCount()):
            string = table.item(1, i).text()
            string = doReverseTransform(string, pairList)
            table.item(1, i).setText(string)
            if i == 0:
                topRow = table.takeItem(0, 0)
                bottomRow = table.takeItem(3, 0)
                table.resizeColumnToContents(0)
                table.setItem(0, 0, topRow)
                table.setItem(3, 0, bottomRow)
            else:
                table.resizeColumnToContents(i)  
        table.setEnabled(1)
    except AttributeError:
        pass
