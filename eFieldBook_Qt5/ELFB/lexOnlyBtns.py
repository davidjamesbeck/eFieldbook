from PyQt5 import QtWidgets, QtCore
from ELFB import dataIndex, formattingHandlers
from ELFB.palettes import DerivationManager
from xml.etree import ElementTree as etree

def delDrvn(fldbk):
    if fldbk.lDerivatives.currentItem() == None:
        return
    derivative = fldbk.lDerivatives.currentItem().data(32)
    current = dataIndex.currentCard
    child = dataIndex.lexDict[derivative]
    root = child.find('Root')
    child.remove(root)
    child = dataIndex.lexDict[current]
    drvnList = child.findall('Drvn')
    for item in drvnList:
        if item.attrib.get('LexIDREF') == derivative:
            badNode = item
            break
    child.remove(badNode)
    for i in range(0,fldbk.lDerivatives.count()):
        if fldbk.lDerivatives.item(i).data(32) == derivative:
            badNode = fldbk.lDerivatives.takeItem(i)
            del(badNode)
            break
    dataIndex.unsavedEdit = 1
    if fldbk.lDerivatives.count() == 0:
        fldbk.lRemoveDerBtn.setEnabled(0)

'''buttons on lexicon card'''

def addDrvn(fldbk):
    dManager = DerivationManager.DerivationManager(fldbk)
    dManager.listEntries()
    exitFlag = 0
    if dManager.exec_():
        derivative = dManager.setData()
        current = dataIndex.currentCard
        child = dataIndex.lexDict[derivative]        
        if child.find('Root') != None:
            queryBox = QtWidgets.QMessageBox()
            queryBox.setIcon(QtWidgets.QMessageBox.Question)
            queryBox.setStandardButtons(QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok)
            queryBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            queryBox.setText('Replace base?')
            queryBox.setInformativeText('This derivative was attributed to another base.\n'
                                                        'Are you sure you want to replace this link?')
            queryBox.exec_()
            if queryBox.result() == QtWidgets.QMessageBox.Ok:                            
                try:                                   
                    child.remove(child.find('Root'))
                except TypeError:
                    pass
            else:
                exitFlag = 1
        if exitFlag == 1:
            return
        elemList = list(child)
        i = 0
        for item in elemList:
            if item.tag != 'Def':
                i += 1
            else:
                break                    
        while child[i].tag == 'Def':
            i += 1
        while child[i].tag == 'Drvn':
            i += 1
        newBase = etree.Element('Root',{"LexIDREF":current})
        child.insert(i,newBase)
        item = QtWidgets.QListWidgetItem()
        item.setData(32, derivative)
        try:
            text = child.findtext('Orth') + " (" + child.findtext('POS') + ") " + child.findtext('Def/L1')
        except TypeError:
            text = child.findtext('Orth') + " " + child.findtext('Def/L1')                        
        item.setText(text)
        fldbk.lDerivatives.addItem(item)
        fldbk.lDerivatives.sortItems(QtCore.Qt.AscendingOrder)
        dataIndex.unsavedEdit = 1  
        child = dataIndex.lexDict[current]
        elemList = list(child)
        newDrvn = etree.Element('Drvn',{"LexIDREF":derivative})
        i = 0
        for item in elemList:
            if item.tag != 'Def':
                i += 1
            else:
                break
        try:
            while child[i].tag == 'Def':
                i += 1
        except IndexError:
            pass
        child.insert(i,newDrvn)  
        fldbk.lRemoveDerBtn.setEnabled(1)

def addRoot(fldbk):
    if fldbk.lBase.count() != 0:
        queryBox = QtWidgets.QMessageBox()
        queryBox.setIcon(QtWidgets.QMessageBox.Question)
        queryBox.setStandardButtons(QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok)
        queryBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
        queryBox.setText('Replace base?')
        queryBox.setInformativeText('Are you sure you want to replace this link?')
        queryBox.exec_()
        if queryBox.result() == QtWidgets.QMessageBox.Ok:
            removeRoot(fldbk)
            makeDManager(fldbk)
    else:
        makeDManager(fldbk)
        fldbk.lBreakLnkBtn.setEnabled(1)

def makeDManager(fldbk):
    '''
    run the window for making derivations.
    adds current card to list of derivations on the base card
    '''
    dManager = DerivationManager.DerivationManager(fldbk)
    dManager.listEntries()
    if dManager.exec_():
        base = dManager.setData()
        current = dataIndex.currentCard
        child = dataIndex.lexDict[base]
        ##check to make sure derviation isn't already there for some reason##
        drvnList = child.findall('Drvn')
        if len(drvnList) != 0:
            for drvn in drvnList:
                if drvn.attrib.get('LexIDREF') == current:
                    return
        k = child.find('Def')
        i = list(child).index(k)
        try:
            while child[i+1].tag == 'Def':
                i += 1
        except IndexError:
            pass
        i += 1
        newDrvn = etree.Element('Drvn',{"LexIDREF":current})
        child.insert(i,newDrvn)
        text = child.findtext('Orth')        
        child = dataIndex.lexDict[current]
        fldbk.lBase.clear()
        try:
            child.remove(child.find('Root'))
        except TypeError:
            pass
        k = child.find('Def')
        i = list(child).index(k)
        try:        
            while child[i].tag == 'Def':
                i += 1
            while child[i].tag == 'Drvn':
                i += 1
        except IndexError:
            pass
        newBase = etree.Element('Root',{"LexIDREF":base})
        child.insert(i,newBase)
        item = QtWidgets.QListWidgetItem()
        item.setData(32, base)
        item.setText(text)
        fldbk.lBase.addItem(item)
        dataIndex.unsavedEdit = 1

def removeRoot(fldbk):
    '''
    removes the current card from the list of the root's derivations
    '''
    child = dataIndex.lexDict[fldbk.lBase.item(0).data(32)]
    for item in child.iter('Drvn'):
        if item.get('LexIDREF') == dataIndex.currentCard:
            child.remove(item)
            break
    '''
    removes the root from the Lex entry of the current card
    '''
    child = dataIndex.lexDict[dataIndex.currentCard]
    root = child.find('Root')
    child.remove(root)
    fldbk.lBase.clear()
    fldbk.lBreakLnkBtn.setEnabled(0)
    dataIndex.unsavedEdit = 1

def toggleAuto(fldbk):
    if fldbk.lAutoBtn.isChecked():
        dataIndex.root.set('lAuto','on')
        fldbk.lIPA.setEnabled(0)
    else:
        dataIndex.root.set('lAuto','off')
        fldbk.lIPA.setEnabled(1)
    dataIndex.unsavedEdit = 1

def clipEG(fldbk, outputLanguage):
    lex = dataIndex.lexDict[dataIndex.currentCard]
    datum = lex.find('Orth').text + " "
    if lex.find('POS') != None:
        datum += "(" + lex.find('POS').text + ") "
    if lex.find('Lit') != None:
        datum += "<" + lex.find('Lit').text + "> "
    defList = lex.findall('Def')

    for i in range(0,len(defList)):
        entry = ''
        dialect = ''
        variant = ''
        alternative = ''
        POS = defList[i].findtext('POS')
        index = defList[i].attrib.get('Index')
        if POS:
            entry = "(" + POS + ") "
        Reg = defList[i].findtext('Reg')
        dNode = defList[i].find('Dia')
        if dNode != None:
            dialect = dNode.attrib.get('Dialect')
            entry = entry + dialect + " "
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
                    j += 1
                  
        if Reg:
            entry = entry + Reg + " "
        if outputLanguage == 'L2':
            entry = entry + defList[i].findtext('L2')
        else:
            entry = entry + defList[i].findtext('L1')
        entry = formattingHandlers.XMLtoPlainText(entry)
        
        if i == 0:
            if len(defList) == 1:
                datum += entry
            else:
                datum += "1) " + entry
        else:
            datum += index + ") " + entry
        examples = defList[i].findall('Ln')
        if len(examples) == 0:
            if len(defList) != 1:
                datum += "; "
        else: 
            datum += " ♢ "
            L2Flag = 1
            for j in range(0,len(examples)):
                egID = examples[j].attrib.get('LnRef')
                egElement = dataIndex.exDict[egID]
                eg = egElement.findtext('Line') + ' '
                try: 
                    L2Gloss = egElement.findtext('L2Gloss')
                except AttributeError:
                    L2Flag = 0                
                if  outputLanguage == 'L2' and L2Flag != 0:
                    gloss = L2Gloss
                elif len(egElement.findtext('L1Gloss')) == 0:
                    gloss = L2Gloss
                else:
                    gloss = egElement.findtext('L1Gloss')
                eg += '‘' + gloss + "’ ("
                eg += egElement.attrib.get('Spkr') + ")"
                datum += eg
                if len(examples) != 1 and j != len(examples) - 1:
                    datum += ", "
            if len(defList) != 1 and i != len(defList) - 1:
                datum += "; "
    datum = datum.replace('<i>','')
    datum = datum.replace('</i>','')
    datum = datum.replace('<br />',' ')
    datum = datum.replace('{i}','')
    datum = datum.replace('{/i}','')
    clipboard = QtWidgets.QApplication.clipboard()
    clipping = QtCore.QMimeData()
    clipping.setText(datum)
    clipboard.setMimeData(clipping)

def doneBtn(fldbk, state):
    '''updates the XML to reflect the state of the "Done" button'''
    dataIndex.unsavedEdit = 1
    lexNode = dataIndex.lexDict[dataIndex.currentCard]
    if state == 2:
        lexNode.set('Done', '1')
    else:
        lexNode.set('Done', '0')
