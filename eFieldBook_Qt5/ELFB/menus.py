from PyQt6 import QtGui, QtWidgets, QtCore
from ELFB import dataIndex, Orthographies, cardLoader, idGenerator, navLists, dictBuilder, metaDataTableFillers
from ELFB import update, formattingHandlers, textOnlyBtns
from ELFB.palettes import NewLexDialog, StyledInputDialog, SessionDate
from ELFB.searchClasses import SearchEngine
from xml.etree import ElementTree as etree
import os
import re
import copy
from os import path

"""Menu action definitions"""


def okToContinue(fldbk):
    if dataIndex.unsavedEdit == 1:
        msgbox = QtWidgets.QMessageBox()
        msgbox.setText("Any unsaved changes will be lost.")
        msgbox.setInformativeText("Do you want to save changes?")
        msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Save | QtWidgets.QMessageBox.StandardButton.Discard | QtWidgets.QMessageBox.StandardButton.Cancel)
        msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Save)
        reply = msgbox.exec()
        if reply == QtWidgets.QMessageBox.StandardButton.Discard:
            dataIndex.unsavedEdit = 0
            return True
        elif reply == QtWidgets.QMessageBox.StandardButton.Save:
            dataIndex.unsavedEdit = 0
            saveDb(fldbk)
            return True
        elif reply == QtWidgets.QMessageBox.StandardButton.Cancel:
            return False
    else:
        return True


"""Application menu items"""


def quitApplication(fldbk):
    if okToContinue:
        if dataIndex.sourceFile not in dataIndex.recentFile:
            dataIndex.recentFile.insert(0, dataIndex.sourceFile)
        fldbk.settings.setValue('RecentFile', dataIndex.recentFile)
        fldbk.settings.setValue('LastFile', dataIndex.sourceFile)
        QtWidgets.QApplication.quit()


def showAbout(fldbk):
    GNUfile = QtCore.QFile(dataIndex.rootPath + '/ELFB/GNU.txt')
    GNUfile.open(QtCore.QIODevice.OpenModeFlag.ReadOnly | QtCore.QIODevice.OpenModeFlag.Text)
    GNUstream = QtCore.QTextStream(GNUfile)
    details = GNUstream.readAll()
    GNUfile.close()
    fldbk.aboutBox = QtWidgets.QMessageBox(fldbk)
    fldbk.aboutBox.setDetailedText(details)
    fldbk.aboutBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
    fldbk.aboutBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
    fldbk.aboutBox.setText("<center><b>Electronic Fieldbook 3.0</b></center>")
    fldbk.aboutBox.setInformativeText("<center><small>© 2016, David Beck</small></center>"
                                "<p>This program is free software; you can redistribute it "
                                "and/or modify it under the terms of the GNU General Public "
                                "License as published by the Free Software Foundation, "
                                "given below.</p>"
                                "<p>This program is distributed in the hope "
                                "that it will be useful, but <i>without any warranty</i>; "
                                "without even the implied warranty of <i>merchant ability "
                                "or fitness for a particular purpose</i>. See the GNU General "
                                "Public License below for more details.</p>")
    fldbk.aboutBox.exec()


"""File Menu items"""

"""New file"""


def newDb(fldbk):
    if not okToContinue(fldbk):
        return
    blankDb = dataIndex.rootPath + '/ELFB/newFileTemplate.xml'
    openDb(fldbk, blankDb)
    saveAsDb(fldbk, newDb)


"""Open"""


def openDb(fldbk, fname=None):
    fldbk.tabWidget.setCurrentIndex(0)
    currentFile = dataIndex.sourceFile
    if currentFile:
        if not okToContinue(fldbk):
            return
        else:
            closeDb(fldbk)
    if fname is None:
        openFileDialog = QtWidgets.QFileDialog(fldbk)
        filePath = path.dirname(openFileDialog.directory().currentPath())
        fileDir = path.split(filePath)
        if fileDir[1] == 'com.UNTProject.eFieldbook':
            openFileDialog.setDirectory(dataIndex.homePath)
        fname = openFileDialog.getOpenFileName(fldbk, "Open...")
        fname = fname[0]
    if fname:
        xmlFile = QtCore.QFile(fname)
        xmlFile.open(QtCore.QIODevice.OpenModeFlag.ReadOnly | QtCore.QIODevice.OpenModeFlag.Text)
        xmlString = xmlFile.readAll()
        xmlFile.close()
        dataIndex.root = etree.XML(xmlString)
        """rebuild the window contents using the new file"""
        fldbk.tabWidget.setTabEnabled(1, 1)
        fldbk.tabWidget.setTabEnabled(2, 1)
        fldbk.tabWidget.setTabEnabled(3, 1)
        fldbk.tabWidget.setTabEnabled(4, 1)
        fldbk.tabWidget.setTabEnabled(5, 1)
        fldbk.tabWidget.setTabEnabled(6, 1)
        fldbk.tabWidget.setTabEnabled(7, 1)
        fldbk.tabWidget.setTabEnabled(8, 1)
        dbTitle = dataIndex.root.attrib.get('Dbase')
        dbTitle = formattingHandlers.XMLtoRTF(dbTitle)
        fldbk.hTitle.setText(dbTitle)
        fldbk.hTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        lang = dataIndex.root.attrib.get('Language')
        fldbk.hLanguage.setPlainText(lang)
        family = dataIndex.root.attrib.get('Family')
        fldbk.hFamily.setPlainText(family)
        population = dataIndex.root.attrib.get('Population')
        fldbk.hPopulation.setPlainText(population)
        location = dataIndex.root.attrib.get('Location')
        fldbk.hLocation.setPlainText(location)
        iso = dataIndex.root.attrib.get('ISO')
        fldbk.hISO.setPlainText(iso)
        if dataIndex.sourceFile not in dataIndex.recentFile and dataIndex.sourceFile is not None:
            dataIndex.recentFile.insert(0, dataIndex.sourceFile)
        dataIndex.sourceFile = fname[len(dataIndex.homePath):]
        if fname[len(dataIndex.homePath):] in dataIndex.recentFile:
            del dataIndex.recentFile[dataIndex.recentFile.index(fname[len(dataIndex.homePath):])]
        fldbk.settings.setValue('LastFile', dataIndex.sourceFile)
        dataIndex.recentFile.insert(0, fname[len(dataIndex.homePath):])
        dataIndex.recentFile = dataIndex.recentFile[:6]
        dataIndex.unsavedEdit = 1
        fldbk.giveWindowTitle()
        navLists.navListBuilderLex(fldbk)
        navLists.navListBuilderText(fldbk)
        navLists.navListBuilderData(fldbk)
        dictBuilder.exDictBuilder()
        dictBuilder.mediaDictBuilder()
        dictBuilder.speakerDictBuilder()
        dictBuilder.rschrDictBuilder()
        metaDataTableFillers.fillRTable(fldbk)
        metaDataTableFillers.fillConsultantTable(fldbk)
        metaDataTableFillers.fillMediaTable(fldbk)
        metaDataTableFillers.fillOrth(fldbk)
        metaDataTableFillers.fillAbbrevTables(fldbk)
        dataIndex.lastText = dataIndex.root.attrib.get('LastText')
        dataIndex.lastLex = dataIndex.root.attrib.get('LastLex')
        dataIndex.lastEx = dataIndex.root.attrib.get('LastEx')
        dataIndex.lastDset = dataIndex.root.attrib.get('LastDset')
        try:
            if dataIndex.root.attrib.get('lAuto') == 'on':
                fldbk.lAutoBtn.setChecked(1)
            else:
                fldbk.lAutoBtn.setChecked(0)
        except AttributeError:
            fldbk.lAutoBtn.setChecked(0)


"""Close"""


def closeDb(fldbk):
    if okToContinue(fldbk):
        fldbk.tabWidget.setCurrentIndex(0)
        fldbk.tabWidget.setTabEnabled(1, 0)
        fldbk.tabWidget.setTabEnabled(2, 0)
        fldbk.tabWidget.setTabEnabled(3, 0)
        fldbk.tabWidget.setTabEnabled(4, 0)
        fldbk.tabWidget.setTabEnabled(5, 0)
        fldbk.tabWidget.setTabEnabled(6, 0)
        fldbk.tabWidget.setTabEnabled(7, 0)
        fldbk.tabWidget.setTabEnabled(8, 0)
        dataIndex.lexDict.clear()
        dataIndex.textDict.clear()
        dataIndex.dataDict.clear()
        fldbk.hTitle.clear()
        fldbk.hLanguage.clear()
        fldbk.hFamily.clear()
        fldbk.hLocation.clear()
        fldbk.hPopulation.clear()
        fldbk.hISO.clear()
        try:
            fldbk.cSearchResults.model().clear()
        except AttributeError:
            pass
        fldbk.iIndex.clear()
        try:
            itemNumber = fldbk.hLexNav.model().rowCount()
            for i in reversed(range(0, itemNumber)):
                fldbk.hLexNav.model().removeRow(i)
            itemNumber = fldbk.lLexNav.model().rowCount()
            for i in reversed(range(0, itemNumber)):
                fldbk.lLexNav.model().removeRow(i)
            itemNumber = fldbk.hTextNav.model().rowCount()
            for i in reversed(range(0, itemNumber)):
                fldbk.hTextNav.model().removeRow(i)
            itemNumber = fldbk.tTextNav.model().rowCount()
            for i in reversed(range(0, itemNumber)):
                fldbk.tTextNav.model().removeRow(i)
            itemNumber = fldbk.hDataNav.model().rowCount()
            for i in reversed(range(0, itemNumber)):
                fldbk.hDataNav.model().removeRow(i)
            itemNumber = fldbk.dDataNav.model().rowCount()
            for i in reversed(range(0, itemNumber)):
                fldbk.dDataNav.model().removeRow(i)
        except AttributeError:
            pass
        fldbk.hLexiconLabel.clear()
        fldbk.hTextsLabel.clear()
        fldbk.hDatasetLabel.clear()
    if dataIndex.sourceFile not in dataIndex.recentFile:
        dataIndex.recentFile.insert(0, dataIndex.sourceFile)
    fldbk.settings.setValue('RecentFile', dataIndex.recentFile)
    fldbk.settings.setValue('LastFile', dataIndex.sourceFile)
    dataIndex.unsavedEdit = 0
    dataIndex.sourceFile = None
    try:
        fldbk.mRTable.clear()
        fldbk.mSpTable.clear()
        fldbk.mMediaTable.clear()
        fldbk.sOrder.clear()
        fldbk.oOrder.clear()
    except AttributeError:
        pass
    fldbk.giveWindowTitle()

 
"""Save"""


def saveDb(fldbk):
    if QtWidgets.QApplication.focusWidget() is not None:
        fieldname = QtWidgets.QApplication.focusWidget().objectName()
        if len(fieldname) != 0:
            try:
                update.setContents(fldbk, fieldname)
            except IndexError:
                pass
    if dataIndex.sourceFile is not None:
        saveDoc = etree.tostring(dataIndex.root, "unicode")
#        saveFile = QtCore.QFile(dataIndex.sourceFile)
#        saveFile.open(QtCore.QIODevice.ReadWrite)
        saveFile = open(dataIndex.homePath + dataIndex.sourceFile, "w", encoding="UTF-8")
        saveFile.write(saveDoc)
        saveFile.close()
    else:
        saveAsDb(fldbk)
    dataIndex.unsavedEdit = 0
    fldbk.settings.setValue('LastFile', dataIndex.sourceFile)
    fldbk.settings.setValue('RecentFile', dataIndex.recentFile)
 

"""Save As"""


def saveAsDb(fldbk, newDb=None):
    if QtWidgets.QApplication.focusWidget() is not None:
        fieldname = QtWidgets.QApplication.focusWidget().objectName()
        try:
            update.setContents(fldbk, fieldname)
        except IndexError:
            pass  
    parent = None
    openFileDialog = QtWidgets.QFileDialog(fldbk)
    filePath = path.dirname(openFileDialog.directory().currentPath())
    fileDir = path.split(filePath)
    if fileDir[1] == 'com.UNTProject.eFieldbook':
        openFileDialog.setDirectory(dataIndex.homePath)
    if newDb is not None:
        openFileDialog.setDirectory(dataIndex.homePath)
        openFileDialog.selectFile('*.xml')
        fname = openFileDialog.getSaveFileName(parent, "Create database.")[0]
    else:
        fname = openFileDialog.getSaveFileName(parent, "Save As...")[0]
    if fname:
        saveDoc = etree.tostring(dataIndex.root, encoding="unicode")
        saveFile = open(fname, "w", encoding="UTF-8")
        saveFile.write(saveDoc)
        saveFile.close()
        dataIndex.unsavedEdit = 0
        dataIndex.sourceFile = fname[len(dataIndex.homePath):]
        if dataIndex.sourceFile not in dataIndex.recentFile:
            dataIndex.recentFile.insert(0, dataIndex.sourceFile)
        fldbk.settings.setValue('LastFile', dataIndex.sourceFile)
        fldbk.settings.setValue('RecentFile', dataIndex.recentFile)
        fldbk.giveWindowTitle()


def clearCard(fldbk):
    fieldList = fldbk.tabWidget.currentWidget().findChildren(QtWidgets.QTextEdit)
    for item in fieldList:
        item.clear()
    plainList = fldbk.tabWidget.currentWidget().findChildren(QtWidgets.QPlainTextEdit)
    for item in plainList:
        item.clear()
    lineList = fldbk.tabWidget.currentWidget().findChildren(QtWidgets.QLineEdit)
    for item in lineList:
        item.clear()
    tableList = fldbk.tabWidget.currentWidget().findChildren(QtWidgets.QTableWidget)
    for item in tableList:
        if item.objectName() != 'Abbreviations':
            item.clear()
    listList = fldbk.tabWidget.currentWidget().findChildren(QtWidgets.QListWidget)
    for item in listList:
        item.clear()


"""Copy card"""


def copyCard(fldbk):
    tDate = setSessionDate()
    dataIndex.unsavedEdit = 1
    if fldbk.tabWidget.currentIndex() == 1:  # lexicon card
        cardType = 'LX'
        newID = idGenerator.generateID(cardType, dataIndex.lexDict)
        ID = 'LexID'
        elemListType = 'Lex[@LexID="%s"]' %dataIndex.currentCard
        lexdict = dataIndex.lexDict
    elif fldbk.tabWidget.currentIndex() == 2:  # text card
        cardType = 'TX'
        newID = idGenerator.generateID(cardType, dataIndex.lexDict)
        ID = 'TextID'
        elemListType = 'Text[@TextID="%s"]'%dataIndex.currentCard
        lexdict = dataIndex.textDict
    elif fldbk.tabWidget.currentIndex() == 3:  # example card
        cardType = 'EX'
        newID = idGenerator.generateID(cardType, dataIndex.lexDict)
        ID = 'ExID'
        elemListType = 'Ex[@ExID="%s"]'%dataIndex.currentCard
        lexdict = dataIndex.exDict
    elif fldbk.tabWidget.currentIndex() == 4:  # dataset card
        cardType = 'DS'
        newID = idGenerator.generateID(cardType, dataIndex.lexDict)
        ID = 'DsetID'
        elemListType = 'Dset[@DsetID="%s"]'%dataIndex.currentCard
        lexdict = dataIndex.dataDict
    newID = idGenerator.generateID(cardType, lexdict)
    sourceCard = lexdict[dataIndex.currentCard]
    newElem = copy.deepcopy(sourceCard)
    newElem.set(ID, newID)
    newElem.set('Date', tDate)
    newElem.set('Update', tDate) 
    k = dataIndex.root.find(elemListType)
    i = list(dataIndex.root).index(k) + 1
    dataIndex.root.insert(i, newElem)
    """delink sounds and media files"""
    soundList = newElem.findall('Sound')
    if len(soundList) != 0:
        for sound in soundList:
            newElem.remove(sound)
    if cardType == 'LX':
        dataIndex.lexDict[newID] = newElem
        cardLoader.loadLexCard(newElem)
        navLists.navListBuilderLex(fldbk)
        cardLoader.resetNavBars(fldbk.lLexNav, newID)
        dataIndex.currentCard = newID
        dataIndex.lastLex = newID
        dataIndex.root.set('LastLex', newID)
        fldbk.lSound.Recordings.clear()
        fldbk.lSound.SoundFileMeta.clear()
        """clear derivations"""
        fldbk.lDerivatives.clear()
        drvnList = newElem.findall('Drvn')
        if len(drvnList) != 0:
            for drvn in drvnList:
                newElem.remove(drvn)
        """clear root"""
        root = newElem.find('Root')
        try:
            newElem.remove(root)
            fldbk.lBase.clear()
            fldbk.lBreakLnkBtn.setEnabled(0)
        except TypeError:
            pass
        """deal with existing homonyms"""
        if newElem.attrib.get('Hom') is not None:
            syn = newElem.attrib.get('Hom')
            synList = syn.split(', ')
            synList.append(newID)
            try:
                synList.index(sourceCard.attrib.get('LexID'))
            except ValueError:
                synList.append(sourceCard.attrib.get('LexID'))
            update.manageHomonyms(synList)
    elif cardType == 'TX':
        dataIndex.textDict[newID] = newElem
        cardLoader.loadTextCard(newElem)
        navLists.navListBuilderText(fldbk)
        cardLoader.resetNavBars(fldbk.tTextNav, newID)
        dataIndex.currentCard = newID
        dataIndex.lastText = newID
        dataIndex.root.set('LastText', newID)
        fldbk.tRecordings.clear()
        fldbk.tSoundFileMeta.clear()
    elif cardType == 'EX':
        dataIndex.exDict[newID] = newElem
        cardLoader.loadExCard(newElem)
        dataIndex.currentCard = newID
        dataIndex.lastText = newID
        dataIndex.root.set('LastEx', newID)
        try:
            if newElem.attrib['Links'] is not None:
                del newElem.attrib['Links']
                fldbk.eLinksList.clear()
        except KeyError:
            pass
        fldbk.eSound.Recordings.clear()
        fldbk.eSound.SoundFileMeta.clear()
    elif cardType == 'DS':
        dataIndex.dataDict[newID] = newElem
        cardLoader.loadDataCard(newElem)
        navLists.navListBuilderData(fldbk)
        cardLoader.resetNavBars(fldbk.dDataNav, newID)
        dataIndex.currentCard = newID
        dataIndex.lastText = newID
        dataIndex.root.set('LastDset', newID)
        fldbk.dSound.Recordings.clear()
        fldbk.dSound.SoundFileMeta.clear()
        

"""New card"""


def newCard(fldbk):
    today = SessionDate.dateFinder()
    tDate = setSessionDate()
    dataIndex.unsavedEdit = 1
    if fldbk.tabWidget.currentIndex() == 1:  # lexicon card
        newID = idGenerator.generateID('LX', dataIndex.lexDict)
        newCdWindow = NewLexDialog.NewLexDialog(fldbk)
        navBar = fldbk.lNavBar
        if newCdWindow.exec():
            clearCard(fldbk)
            fldbk.lL1Definition.clear() 
            fldbk.lL2Definition.clear() 
            fldbk.lDerivatives.clear()
            fldbk.lSound.Recordings.clear()
            fldbk.lSound.SoundFileMeta.clear()
            fldbk.lDoneBtn.setChecked(0)
            data = newCdWindow.getData()
            """returns a list [speaker, researcher, entry word, gloss]"""
            newNode = etree.Element('Lex', {"LexID":newID})
            newNode.set('Date', tDate)
            newNode.set('Update', today)
            newNode.set('Spkr', data[0])
            newNode.set('Rschr', data[1])
            newNode.set('Done', '0')
            newOrth = etree.SubElement(newNode, 'Orth')
            newOrth.text = data[2]
            """generate IPA node if Auto checked"""
            if fldbk.lAutoBtn.isChecked():
                IPA = Orthographies.toIPA(data[2])
                newIPA = etree.SubElement(newNode, 'IPA')
                newIPA.text = IPA
                fldbk.lIPA.setText(IPA)
            newDef = etree.SubElement(newNode, 'Def', {'Index':'1'})
            newL1 = etree.SubElement(newDef, 'L1')
            newL1.text = data[3]
            fldbk.lSource.setPlainText(data[0])
            fldbk.lResearcher.setPlainText(data[1])
            fldbk.lDate.setPlainText(tDate)
            fldbk.lUpdated.setPlainText(tDate)
            fldbk.lOrthography.setText(data[2])
            """if new word in data[2] is homophonous with another entry"""
            homList = fldbk.lLexNav.findChildren(QtGui.QStandardItem, data[2])
            if homList is not None:
                homList.append(newID)
                update.manageHomonyms(homList)
            cardLoader.loadDefinitions(fldbk, newNode)
            if len(dataIndex.lexDict.keys()) == 1:
                badNode = dataIndex.root.find('Lex')
                badID = badNode.attrib.get('LexID')
                if badID == 'LX00':
                    dataIndex.root.remove(badNode)
                    del dataIndex.lexDict[badID]
            dataIndex.root.insert(1, newNode)
            dataIndex.lexDict[newID] = newNode
            navLists.navListBuilderLex(fldbk)
            cardLoader.resetNavBars(fldbk.lLexNav, newID)
            dataIndex.currentCard = newID
            dataIndex.lastLex = newID
            dataIndex.lexDict[newID] = newNode
            dataIndex.root.set('LastLex', newID)

    if fldbk.tabWidget.currentIndex() == 2:  # text card
        textOnlyBtns.enterNewText(fldbk)
        navBar = fldbk.tNavBar
        
    if fldbk.tabWidget.currentIndex() == 3:  # example card
        navBar = fldbk.eNavBar
        fldbk.eAnalysis.clear()
        fldbk.eAnalysis.setColumnCount(2)
        fldbk.eAnalysis.setRowCount(2)
        lastHeadWidget = QtWidgets.QTableWidgetItem(1001)
        lastHeadWidget.setText('+')
        fldbk.eAnalysis.setHorizontalHeaderItem(1, lastHeadWidget)
        fldbk.eAnalysis.resizeColumnToContents(1)
        rowHeader = QtWidgets.QTableWidgetItem(1001)
        rowHeader.setText('Morph')   
        fldbk.eAnalysis.setVerticalHeaderItem(0, rowHeader)
        rowHeader = QtWidgets.QTableWidgetItem(1001)
        rowHeader.setText('ILEG')   
        fldbk.eAnalysis.setVerticalHeaderItem(1, rowHeader)
        clearCard(fldbk)
        fldbk.eLinksList.clear()
        newID = idGenerator.generateID('EX', dataIndex.exDict)
        newNode = etree.Element('Ex', {"ExID":newID})
        newNode.set('Date', tDate)
        newNode.set('Update', today)
        if dataIndex.lastRschr is not None and len(dataIndex.lastRschr) != 0:
            newNode.set('Rschr', dataIndex.lastRschr)
        else:
            newNode.set('Rschr', 'YYY')
        if dataIndex.lastSpeaker is not None and len(dataIndex.lastSpeaker) != 0:
            newNode.set('Spkr', dataIndex.lastSpeaker)
        else:
            newNode.set('Spkr', 'XX')
        etree.SubElement(newNode, 'Line')
        etree.SubElement(newNode, 'Mrph')
        etree.SubElement(newNode, 'ILEG')
        etree.SubElement(newNode, 'L1Gloss')
        egList = list(dataIndex.exDict.keys())
        lastExCard = dataIndex.exDict[egList[len(dataIndex.exDict)-1]]
        i = list(dataIndex.root).index(lastExCard)
        if len(dataIndex.exDict.keys()) == 1:
            badNode = dataIndex.root.find('Ex')
            badID = badNode.attrib.get('ExID')
            if badID == 'EX00':
                dataIndex.root.remove(badNode)
                del dataIndex.exDict[badID]
        dataIndex.root.insert(i, newNode)
        dataIndex.currentCard = newID
        dataIndex.exDict[newID] = newNode
        dataIndex.lastEx = newID
        dataIndex.root.set('LastEx', newID)
        cardLoader.loadExCard(newNode)
       
    if fldbk.tabWidget.currentIndex() == 4:  # dataset card
        nameBox = StyledInputDialog.StyledInputDialog(fldbk)
        nameBox.setWindowTitle('New dataset.')
        nameBox.inputLabel.setText('Give the dataset a name.')
        navBar = fldbk.dNavBar
        if nameBox.exec():
            title = nameBox.returnInput()
            newNode = newDataset(fldbk, title)
            clearCard(fldbk)
            cardLoader.loadDataCard(newNode)
            
    navBar.stack.append(dataIndex.currentCard)
    navBar.index = navBar.index + 1
    

def newDataset(fldbk, title, newText=''):
    """1 create DSNode"""
    tDate = setSessionDate()
    today = SessionDate.dateFinder()
    newID = idGenerator.generateID('DS', dataIndex.dataDict)
    newNode = etree.Element('Dset')
    newNode.set('DsetID', newID)
    newNode.set('Date',  tDate)
    newNode.set('Update', today)
    if dataIndex.lastSpeaker is not None:
        newNode.set('Spkr', dataIndex.lastSpeaker)
    else:
        newNode.set('Spkr', '')
    if dataIndex.lastRschr is not None:
        newNode.set('Rschr', dataIndex.lastRschr)
    else:
        newNode.set('Rschr', '')
    etree.SubElement(newNode, 'Title')
    etree.SubElement(newNode, 'Data')
    newNode.find('Title').text = title
    newNode.find('Data').text = newText
    """2 add new DS to XML and dataDict and set current DSet"""
    dataIndex.dataDict[newID] = newNode
    dataIndex.lastDset = newID
    dList = list(dataIndex.dataDict.keys())
    lastDCard = dataIndex.dataDict[dList[len(dataIndex.dataDict)-1]]
    try:
        i = list(dataIndex.root).index(lastDCard)  
    except ValueError:
        lastDCard = dataIndex.dataDict[dList[len(dataIndex.dataDict)-2]]
        i = list(dataIndex.root).index(lastDCard)
    if len(dataIndex.dataDict.keys()) == 1:
        badNode = dataIndex.root.find('Dset')
        badID = badNode.attrib.get('DsetID')
        if badID == 'DS00':
            dataIndex.root.remove(badNode)
            del dataIndex.dataDict[badID]
    dataIndex.root.insert(i, newNode)
    """3 add new DS to listnav"""
    navLists.navListBuilderData(fldbk)
    cardLoader.resetNavBars(fldbk.dDataNav, newID)
    dataIndex.currentCard = newID  
    dataIndex.lastDset = newID
    dataIndex.root.set('LastDset', newID)    
    return newNode
        

def delCard(fldbk):
    target = dataIndex.currentCard
    if fldbk.tabWidget.currentIndex() == 1:
        cardType = "lexical entry"
        badNode = dataIndex.lexDict[target]
        navBar = fldbk.lNavBar
    if fldbk.tabWidget.currentIndex() == 2:
        cardType = "text"
        badNode = dataIndex.textDict[target]
        navBar = fldbk.tNavBar
    if fldbk.tabWidget.currentIndex() == 3:
        cardType = "example"
        badNode = dataIndex.exDict[target]
        navBar = fldbk.eNavBar
    if fldbk.tabWidget.currentIndex() == 4:
        cardType = "dataset"
        badNode = dataIndex.dataDict[target]
        navBar = fldbk.dNavBar
    if cardType == "example" and badNode.attrib.get('SourceText') is not None:
        textTitle = "<i>" + fldbk.eSourceText.toPlainText() + "</i>"
        msgbox = QtWidgets.QMessageBox()
        msgbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        msgbox.setText("Line from text.")
        msgbox.setInformativeText('This is a line from the text %s. Please edit texts from the <b>Texts</b> tab.' %textTitle)
        msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        reply = msgbox.exec()
        return
    else:
        msgbox = QtWidgets.QMessageBox()
        msgbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msgbox.setText("Delete card?")
        msgbox.setInformativeText("This will remove the current %s and all cross-references to it from the database." %cardType)
        msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
        msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        reply = msgbox.exec()
        if reply == QtWidgets.QMessageBox.StandardButton.Ok:
            if cardType == "lexical entry":
                if badNode.attrib.get('Hom') is not None:
                    homs = badNode.attrib.get('Hom')
                    homList = homs.split(', ')
                    update.manageHomonyms(homList)
                if len(dataIndex.lexDict) != 1:
                    for i in range(fldbk.lLexNav.model().rowCount()):
                        if fldbk.lLexNav.model().index(i, 0).data(32) == target:
                            fldbk.lLexNav.model().removeRow(i)
                            break                     
                    update.cleanUpIDs(target)
                    fldbk.lNavBar.goPrev()
                    dataIndex.root.remove(badNode)
                else:
                    clearCard(fldbk)
                    tDate = setSessionDate()
                    today = SessionDate.dateFinder()
                    update.cleanUpIDs(target)
                    node = dataIndex.lexDict[target]
                    node.clear()
                    node.set("LexID", target)
                    node.set("Date", tDate)
                    node.set("Update", today)
                    etree.SubElement(node, "Orth")
                    defNode = etree.SubElement(node, "Def", attrib={"Index" : "1"})
                    dummyDef = etree.SubElement(defNode, "L1")
                    dummyDef.text = 'new word'
                    fldbk.lOrthography.setText(dummyDef.text)
                    currentProxyIndex = fldbk.lLexNav.currentIndex()
                    currentSourceIndex = fldbk.lLexNav.model().mapToSource(currentProxyIndex)
                    fldbk.lLexNav.model().sourceModel().itemFromIndex(currentSourceIndex).setText(dummyDef.text)
                    dataIndex.currentCard = target
            elif cardType == "text":
                if len(dataIndex.textDict) != 1:
                    purgeTexts(target)
                    del dataIndex.textDict[target]
                    for i in range(fldbk.tTextNav.model().rowCount()):
                        if fldbk.tTextNav.model().index(i, 0).data(32) == target:
                            fldbk.tTextNav.model().removeRow(i)
                            break
                    update.cleanUpIDs(target)
                    fldbk.tNavBar.goPrev()
                    dataIndex.root.remove(badNode)
                else:
                    purgeTexts(target)
                    update.cleanUpIDs(target)
                    clearCard(fldbk)
                    while fldbk.textLayout.count():
                        item = fldbk.textLayout.takeAt(0)
                        widget = item.widget()
                        if widget is not None:
                            widget.deleteLater()
                    node = dataIndex.textDict[target]
                    node.clear()
                    node.set("TextID", target)
                    node.set("Date", tDate)
                    node.set("Update", today)
                    dummyTitle = etree.SubElement(node, "Title")
                    dummyTitle.text = "new text"
                    fldbk.tTitle.setText(dummyTitle.text)
                    fldbk.tNewTitle.setText(dummyTitle.text)
                    currentProxyIndex = fldbk.tTextNav.currentIndex()
                    currentSourceIndex = fldbk.tTextNav.model().mapToSource(currentProxyIndex)
                    fldbk.tTextNav.model().sourceModel().itemFromIndex(currentSourceIndex).setText(dummyTitle.text)       
                    dataIndex.currentText = True
                    dataIndex.currentCard = target
                    textOnlyBtns.enterNewText(fldbk)
            elif cardType == "example":
                if len(dataIndex.exDict) != 1:
                    del dataIndex.exDict[target]
                    update.cleanUpIDs(target)
                    fldbk.eNavBar.goPrev()
                    dataIndex.root.remove(badNode)
                else:
                    clearCard(fldbk)
                    node = dataIndex.exDict[target]
                    update.cleanUpIDs(target)
                    node.clear()
                    node.set("ExID", target)
                    node.set("Date", tDate)
                    node.set("Update", today)
                    etree.SubElement(node, "Line")
                    etree.SubElement(node, "Mrph")
                    etree.SubElement(node, "ILEG")
                    etree.SubElement(node, "L1Gloss")
                    dataIndex.currentCard = target
            elif cardType == "dataset":
                if len(dataIndex.dataDict) != 1:
                    del dataIndex.dataDict[target]
                    for i in range(fldbk.dDataNav.model().rowCount()):
                        if fldbk.dDataNav.model().index(i, 0).data(32) == target:
                            fldbk.dDataNav.model().removeRow(i)
                            break
                    update.cleanUpIDs(target)
                    fldbk.dNavBar.goPrev()
                    dataIndex.root.remove(badNode)
                else:
                    clearCard(fldbk)
                    node = dataIndex.dataDict[target]
                    node.clear()
                    update.cleanUpIDs(target)
                    node.set("DSetID", target)
                    node.set("Date", tDate)
                    node.set("Update", today)
                    etree.SubElement(node, "Title")
                    etree.SubElement(node, "Data")
                    currentProxyIndex = fldbk.dDataNav.currentIndex()
                    currentSourceIndex = fldbk.dDataNav.model().mapToSource(currentProxyIndex)
                    fldbk.dDataNav.model().sourceModel().itemFromIndex(currentSourceIndex).setText("") 
                    dataIndex.currentCard = target
        else:
            return
        dataIndex.unsavedEdit = 1
        if target in navBar.stack:
            navBar.stack.remove(target)
            navBar.index = navBar.index - 1


def purgeTexts(badTextID):
    msgbox = QtWidgets.QMessageBox()
    msgbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
    msgbox.setText("Remove examples?")
    msgbox.setInformativeText("Remove all the lines in this text from the database as well?")
    msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
    msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Yes)
    reply = msgbox.exec()
    if reply == QtWidgets.QMessageBox.StandardButton.Yes:
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        node = dataIndex.textDict[badTextID]
        lineList = node.findall('Ln')
        for line in lineList:
            exID = line.attrib.get('LnRef')
            badNode = dataIndex.root.find('Ex[@ExID="%s"]'%exID)
            dataIndex.root.remove(badNode)
            update.cleanUpIDs(exID)
        if dataIndex.root.find('Ex') is None:
            soloEx = etree.Element('Ex', {'ExID':'EX001',  'Date':'2000-01-01',  'Update':"2015-05-07"})
            etree.SubElement(soloEx, 'Line')
            etree.SubElement(soloEx, 'Mrph')
            etree.SubElement(soloEx, 'ILEG')
            etree.SubElement(soloEx, 'L1Gloss')
            k = dataIndex.root.find('Speaker')
            d = list(dataIndex.root).index(k)
            dataIndex.root.insert(d, soloEx)
        QtWidgets.QApplication.restoreOverrideCursor()


def updateRecentFile(fldbk):
    """update for Open Recent file menu"""
    fileList = dataIndex.recentFile
    if fileList is None:
        return
    topMenu = fldbk.menuBar
    for item in topMenu.children():
        if item.objectName() == 'menuFile':
            fileMenu = item
            break
    for item in fileMenu.children():
        if item.objectName() == 'menuOpen_Recent':
            recentMenu = item
            break      
    shortNameList = []
    for tPath in fileList:
        if tPath != dataIndex.sourceFile:
            if QtCore.QFile.exists(dataIndex.homePath + tPath):
                shortName = os.path.basename(tPath)
                shortNameList.append((shortName, tPath))
    if len(shortNameList) == 0:
        recentMenu.setEnabled(False)
        return
    recentMenu.setEnabled(True)
    recentMenu.clear()
    for (shortName, tPath) in shortNameList:
        menuAction = recentMenu.addAction(
                '{0}'.format(shortName)
                )
        menuAction.triggered.connect(lambda: openRecent(fldbk))
        menuAction.setObjectName(tPath)
        """TODO: need to add a path to file names that are duplicated in the list"""


def openRecent(fldbk):
    fname = dataIndex.homePath + QtCore.QObject.objectName(fldbk.sender())
    openDb(fldbk, fname)


def findByID(fldbk):
    inputBox = StyledInputDialog.StyledInputDialog(fldbk)
    inputBox.setWindowTitle('Find by ID')
    inputBox.inputLabel.setText('Enter unique ID for entry.')
    if inputBox.exec():
        ID = inputBox.returnInput()
    if ID[0] == 'L':
        try:
            target = dataIndex.lexDict[ID]
            cardLoader.loadLexCard(target)
            fldbk.tabWidget.setCurrentIndex(1)
        except KeyError:
            QtWidgets.QApplication.beep()
    elif ID[0] == 'E':
        try:
            target = dataIndex.exDict[ID]
            cardLoader.loadExCard(target)
            fldbk.tabWidget.setCurrentIndex(3)
        except KeyError:
            QtWidgets.QApplication.beep() 
    elif ID[0] == 'D':
        try: 
            target = dataIndex.dataDict[ID]
            cardLoader.loadDataCard(target)
            fldbk.tabWidget.setCurrentIndex(4)
        except KeyError:
            QtWidgets.QApplication.beep()
    else:
        QtWidgets.QApplication.beep()


"""Search menu"""

"""Find"""


def findMenu(fldbk):
    target = QtWidgets.QInputDialog().getText(fldbk, "Find", "Enter text to find.")
    if target[1] is True and len(target[0]) != 0:
        regExp = QtCore.QRegularExpression(target[0], QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
        hits = searchXML(regExp)
        if hits:
            dataIndex.searchResults = hits
            dataIndex.searchPointer = 1
    

def findAgain():
    if dataIndex.searchResults is not None:
        dataIndex.searchPointer += 1
        if dataIndex.searchPointer > len(dataIndex.searchResults):
            dataIndex.searchPointer = 1
        tCard = dataIndex.searchResults[dataIndex.searchPointer]
        if tCard[0] == 'L':
            cardLoader.loadLexCard(dataIndex.lexDict[tCard])
        elif tCard[0] == 'D':
            cardLoader.loadDataCard(dataIndex.dataDict[tCard])
        elif tCard[0] == 'E':
            cardLoader.loadExCard(dataIndex.exDict[tCard])
    

def fuzzyFind(fldbk):
    target = QtWidgets.QInputDialog().getText(fldbk, "Fuzzy find", "Enter text to find. Accents, caps, \n"
                                                    "and diacrits will be ignored.")
    if target[1] is True and len(target[0]) != 0:
        lookFor = target[0]
        lookFor = SearchEngine.removeDiacrits(SearchEngine, lookFor)
        lookFor = SearchEngine.removeAccents(SearchEngine, lookFor)  
        regExp = QtCore.QRegularExpression(lookFor, QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)  
        hits = searchXML(regExp)
        if hits:
            dataIndex.fuzzyResults = hits
            dataIndex.fuzzyPointer = 1


def fuzzyAgain():
    if dataIndex.fuzzyResults is not None:
        dataIndex.fuzzyPointer += 1
        if dataIndex.fuzzyPointer > len(dataIndex.fuzzyResults):
            dataIndex.fuzzyPointer = 1
        tCard = dataIndex.fuzzyResults[dataIndex.fuzzyPointer]
        if tCard[0] == 'L':
            cardLoader.loadLexCard(dataIndex.lexDict[tCard])
        elif tCard[0] == 'D':
            cardLoader.loadDataCard(dataIndex.dataDict[tCard])
        elif tCard[0] == 'E':
            cardLoader.loadExCard(dataIndex.exDict[tCard])


def searchXML(regExp):
    resultsDict = {}
    matchObject = QtCore.QRegularExpressionMatch()
    if dataIndex.currentCard[0] == "L":
        cardType = "Lex"
        ID = 'LexID'
    elif dataIndex.currentCard[0] == "T":
        return
    elif dataIndex.currentCard[0] == "D":
        cardType = "Dset"
        ID = 'DsetID'
    elif dataIndex.currentCard[0] == "E":
        cardType = "Ex"
        ID = 'ExID'
    else:
        return
    i = 0
    for node in dataIndex.root.iter(cardType):
        for item in node.itertext():
            matchObject = regExp.match(item)
            if matchObject.hasMatch():
                i += 1
                resultsDict[i] = node.get(ID)
    if len(resultsDict) != 0:
        tCard = resultsDict[1]
        if cardType == 'Lex':
            cardLoader.loadLexCard(dataIndex.lexDict[tCard])
        elif cardType == 'Dset':
            cardLoader.loadDataCard(dataIndex.dataDict[tCard])
        elif cardType == 'Ex':
            cardLoader.loadExCard(dataIndex.exDict[tCard]) 
        return resultsDict
    else:
        notFoundBox = QtWidgets.QMessageBox()
        notFoundBox.setText('Text not found.')
        notFoundBox.exec()
        return False


def lookUp(fldbk):
    inputBox = QtWidgets.QInputDialog()
    result = inputBox.getText(fldbk, 'Look up … ?', 'Type search term in the box.')
    if result[1] is True:
        tTerm = result[0]
    else:
        return
    regex = re.compile('^[LTED][XS]\d')
    if regex.match(tTerm):
        try:
            if tTerm[0] == "L":
                tEntry = dataIndex.lexDict[tTerm]
                cardLoader.loadLexCard(tEntry)
                fldbk.tabWidget.setCurrentIndex(1)
            elif tTerm[0] == "T":
                tEntry = dataIndex.textDict[tTerm]
                cardLoader.loadTextCard(tEntry)
                fldbk.tabWidget.setCurrentIndex(2)
            elif tTerm[0] == "E":
                tEntry = dataIndex.exDict[tTerm]
                cardLoader.loadExCard(tEntry)
                fldbk.tabWidget.setCurrentIndex(3)
            elif tTerm[0] == "D":
                tEntry = dataIndex.dataDict[tTerm]
                cardLoader.loadDataCard(tEntry)
                fldbk.tabWidget.setCurrentIndex(4)
        except (IndexError, KeyError):
            tEntry = None
    else:
        tEntry = None
        for child in dataIndex.root.iter('Lex'):
            if child.findtext('Orth') == tTerm: 
                tEntry = child
                break
        if tEntry is not None:
            cardLoader.loadLexCard(tEntry)
            fldbk.tabWidget.setCurrentIndex(1)
            
    if tEntry is None:
        QtWidgets.QApplication.beep()


def setSessionDate():
    """sets a default date for new cards"""
    if dataIndex.sessionDate is None:
        dialog = SessionDate.SessionDateManager()
        if dialog.exec():
            tDate = dialog.getSessionDate()
            dataIndex.sessionDate = tDate
            dataIndex.fldbk.actionSession_Date.setChecked(1)
        else:
            dataIndex.sessionDate = 'today'
    else:
        tDate = dataIndex.sessionDate
    if dataIndex.sessionDate == 'today':
        tDate = SessionDate.dateFinder()
        dataIndex.fldbk.actionSession_Date.setChecked(0)
    dataIndex.lastDate = dataIndex.sessionDate
    return tDate


def setSessionSpeaker(p0):
    if p0 is True:
        dialog = SessionDate.SessionSpeakerManager()
        if dialog.exec():
            speaker = dialog.getSessionSpeaker()
            dataIndex.sessionSpeaker = speaker
            dataIndex.lastSpeaker = speaker
            dataIndex.root.set('LastSpeaker', speaker)
        else:
            dataIndex.sessionSpeaker = None
    

def setSessionResearcher(p0):
    if p0 is True:
        dialog = SessionDate.SessionResearcherManager()
        if dialog.exec():
            researcher = dialog.getSessionResearcher()
            dataIndex.sessionResearcher = researcher
            dataIndex.lastRschr = researcher
            dataIndex.root.set('LastRschr', researcher)
        else:
            dataIndex.sessionResearcher = None
