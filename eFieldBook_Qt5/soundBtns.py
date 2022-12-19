from PyQt6 import QtCore,  QtGui, QtWidgets,  QtMultimedia,  QtNetwork
from ELFB import dataIndex, idGenerator, cardLoader
from ELFB.palettes import MediaManager
from xml.etree import ElementTree as etree
from os import path

'''media buttons (all cards)'''

def updateMediaInfo(fldbk, item, newName):
    '''create new media node'''
    tree = dataIndex.root
    medID = idGenerator.generateID("MC",dataIndex.mediaDict)
    elemList = list(tree)
    elemList.reverse()
    for i, node in enumerate(elemList):
        if node.tag == 'Abbreviations':
            break
    i = len(elemList) - i
    newNode = etree.Element('Media')
    tree.insert(i,newNode)
    '''add attributes to media element'''
    newNode.set('MedID',medID)
    newNode.set('Filename',newName)
    dataIndex.mediaDict[medID] = newNode  
    
    '''update media table'''
    mediaTable = fldbk.mMediaTable
    nextRow = mediaTable.rowCount()
    mediaTable.setRowCount(nextRow+1)
    firstItem = QtWidgets.QTableWidgetItem(1001)
    firstItem.setText(newName)
    '''data 36 is the new XML node'''
    firstItem.setData(36,newNode)
    '''data 37 is the path to the sound file'''
    firstItem.setData(37, item)
    firstItem.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
    mediaTable.setItem(nextRow,0,firstItem)
    secondItem = QtWidgets.QTableWidgetItem(1001)
    secondItem.setText('XX')
    secondItem.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
    mediaTable.setItem(nextRow,1,secondItem)
    thirdItem = QtWidgets.QTableWidgetItem(1001)
    thirdItem.setText("???")
    thirdItem.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
    mediaTable.setItem(nextRow,2,thirdItem)
    fourthItem = QtWidgets.QTableWidgetItem(1001)
    fourthItem.setIcon(QtGui.QIcon(":/new/infoBtn.png"))
    mediaTable.setItem(nextRow,3,fourthItem)       
    mediaTable.sortItems(0,QtCore.Qt.SortOrder.AscendingOrder)
    mediaTable.scrollToItem(fourthItem, QtWidgets.QAbstractItemView.PositionAtCenter)
    mediaTable.selectRow(fourthItem.row())
    return medID, newNode

def setDefaultDirectory(fldbk, newFile):
        setPathBox = QtWidgets.QMessageBox()
        setPathBox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        setPathBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.No | QtWidgets.QMessageBox.StandardButton.Ok)
        setPathBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        setPathBox.setText('Set default directory.')
        setPathBox.setInformativeText('Use this directory as the default for locating recordings?')
        setPathBox.exec()
        if setPathBox.result() == QtWidgets.QMessageBox.StandardButton.Ok:
            prefix = path.dirname(newFile)
            fldbk.mMediaPath.setText(prefix)
            dataIndex.root.set("MediaFolder",prefix)
            dataIndex.unsavedEdit = 1        

def addLinktoXML(metadataLabel, medID):
    '''links the sound file to the current <Lex> element'''
    if QtCore.QObject.objectName(metadataLabel)[0] == 'l':
        child = dataIndex.lexDict[dataIndex.currentCard]
        elemList = list(child)
        elemList.reverse()
        for i, item in enumerate(elemList):
            if item.tag == 'Comments':
                break
            elif item.tag == 'Root':
                break
            elif item.tag == 'Drvn':
                break
            elif item.tag == 'Def':
                break
        i = len(elemList) - i
        newElem = etree.Element('Sound')
        child.insert(i,newElem)
        newElem.attrib['MediaRef'] = medID
    elif QtCore.QObject.objectName(metadataLabel)[0] == 't':
        child = dataIndex.textDict[dataIndex.currentCard]
        newElem = etree.Element('Sound')
        child.append(newElem)
        newElem.attrib['MediaRef'] = medID
    elif QtCore.QObject.objectName(metadataLabel)[0] == 'e':
        child = dataIndex.exDict[dataIndex.currentCard]
        newElem = etree.Element('Sound')
        child.append(newElem)
        newElem.attrib['MediaRef'] = medID
    elif QtCore.QObject.objectName(metadataLabel)[0] == 'd':
        child = dataIndex.dataDict[dataIndex.currentCard]
        newElem = etree.Element('Sound')
        child.append(newElem)
        newElem.attrib['MediaRef'] = medID

def fileExists(item, newName):
    node = dataIndex.root.find('Media[@Filename="%s"]'%newName)
    if path.dirname(item) != dataIndex.root.attrib.get('MediaFolder'):
        file = node.attrib.get('Filename')
        speaker = node.attrib.get('Spkr')
        date = node.attrib.get('Date')
        fileInfo = file + " [" + speaker + " " + date + "]"
        msgbox = QtWidgets.QMessageBox()
        msgbox.setText("File in database.")
        msgbox.setInformativeText('There is already a recording named\n\n%s\n\nin the database. '
                                  'If this is not the recording you are linking to, '
                                  'select "Cancel" and rename the file.'%fileInfo)
        msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel | QtWidgets.QMessageBox.StandardButton.Ok)
        msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        msgbox.exec()
        if msgbox.result() == QtWidgets.QMessageBox.StandardButton.Cancel:
            return False            
    medID = node.get('MedID')
    return medID

def fileDuplicate(item, newName):
    node = dataIndex.root.find('Media[@Filename="%s"]'%newName)
    file = node.attrib.get('Filename')
    speaker = node.attrib.get('Spkr')
    date = node.attrib.get('Date')
    fileInfo = file + " [" + speaker + " " + date + "]"
    msgbox = QtWidgets.QMessageBox()
    msgbox.setText("File in database.")
    msgbox.setInformativeText('There is already a recording named\n\n%s\n\nin the database. '
                              'Media files should have unique names.'%fileInfo)
    msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
    msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
    msgbox.exec()

def newMedia(fldbk,):
    #TODO: need to tweak this to allow multiple fields to be selected
    newFile = QtWidgets.QFileDialog(fldbk, "Add recordings.")
    if dataIndex.root.get("MediaFolder") != None:
        newFile.setDirectory(dataIndex.root.get("MediaFolder"))
    else:
        '''this keeps the finder out of the interior of the application bundle'''
        filePath = path.dirname(newFile.directory().currentPath())
        fileDir = path.split(filePath)
        if fileDir[1] == 'com.UNTProject.eFieldbook':        
            newFile.setDirectory(dataIndex.homePath)
    newFile.setFileMode(QtWidgets.QFileDialog.ExistingFile)
    if newFile.exec():
        newNames = newFile.selectedFiles()
        newName = newNames[0]
        if dataIndex.root.get("MediaFolder") is None or dataIndex.root.get("MediaFolder") != path.dirname(newName):
            setDefaultDirectory(fldbk, newName)        
        for item in newNames:
            sound2play = item
            newName = path.basename(item)
            node = dataIndex.root.find('Media[@Filename="%s"]'%newName)
            if node is None:
                medID, node = updateMediaInfo(fldbk, item, newName)
                mManager = MediaManager.MediaManager(dataIndex.fldbk)
                mManager.renameWindow(newName)
                mManager.setValues(medID,fldbk.mediaTable,item)
                mManager.setComboBoxes()
                mManager.exec()      
            else:
                fileDuplicate(item, newName)
                return
        QtMultimedia.QSound.play(sound2play)
        dataIndex.unsavedEdit = 1

def delMedia(fldbk,caller,metadataLabel):
    try:
        metadataLabel.clear()
    except AttributeError:
        pass
    i = caller.currentIndex()
    medID = caller.itemData(i,35)
    msgbox = QtWidgets.QMessageBox()
    msgbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
    msgbox.setText("Remove recording.")
    msgbox.setInformativeText('This will remove the link to this \n'
                              'media file. To remove this recording \n'
                              'from the database, use the Media \n'
                              'Manager on the Metadata tab.')
    msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
    msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
    msgbox.exec()
    if msgbox.result() == QtWidgets.QMessageBox.StandardButton.Ok:
        address = dataIndex.currentCard
        if address[0] == "L":
            lexNode = dataIndex.lexDict[address]
            if metadataLabel != 'gManager':
                if lexNode.find('Sound[@MediaRef="%s"]'%medID) != None:
                    badNode = lexNode.find('Sound[@MediaRef="%s"]'%medID)
                    lexNode.remove(badNode)
        elif address[0] == "E":
            egNode = dataIndex.exDict[address]
            badNode = egNode.find('Sound[@MediaRef="%s"]'%medID)
            egNode.remove(badNode)
        elif address[0] == "D":
            dataNode = dataIndex.dataDict[address]
            badNode = dataNode.find('Sound[@MediaRef="%s"]'%medID)
            dataNode.remove(badNode)
        elif address[0] == "T":
            textNode = dataIndex.textDict[address]
            badNode = textNode.find('Sound[@MediaRef="%s"]'%medID)
            textNode.remove(badNode)
        caller.removeItem(i)
    dataIndex.unsavedEdit = 1
    if caller.count() == 0:
        if QtCore.QObject.objectName(caller)[0] == 'l':
            fldbk.lDelEgBtn.setEnabled(0)
        elif QtCore.QObject.objectName(caller)[0] == 'e':
            fldbk.eDelEgBtn.setEnabled(0)
        elif QtCore.QObject.objectName(caller)[0] == 't':
            fldbk.tDelEgBtn.setEnabled(0)
        elif QtCore.QObject.objectName(caller)[0] == 'd':
            fldbk.dDelEgBtn.setEnabled(0)

def mediaInfo(caller):
    '''item is the path to file, data 37 in combobox item'''
    i = caller.currentIndex()
    mediaID = caller.itemData(i,35)
    item = caller.itemData(i,37)
    mManager = MediaManager.MediaManager(dataIndex.fldbk)
    mManager.renameWindow(caller.currentText())
    mManager.setValues(mediaID,caller,item)
    mManager.exec()  

def playSound(fldbk, caller, IDREF=None):
    '''begins by checking to see if temporary paths have been set for sound files
    (rather than building the path each time)'''
    data37 = None
    if caller != None:
        if IDREF is None:
            if caller.currentIndex() == -1:
                return
            if caller.itemData(caller.currentIndex(), 37):
                data37 = caller.itemData(caller.currentIndex(), 37)
        else:
            if caller.item(caller.currentRow(),0).data(37):
                data37 = caller.item(caller.currentRow(),0).data(37)
    if data37:
        soundFile = data37
    else:
        if dataIndex.root.get("MediaFolder"):
            prefix = dataIndex.root.get("MediaFolder")
        else:
            prefix = None
        if IDREF != None:
            soundFile = dataIndex.mediaDict[IDREF].get('Filename')
        else:
            soundFile = caller.currentText()
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(soundFile)
        if prefix != None:
            soundFile = prefix + "/" + soundFile
    if path.isfile(soundFile):
        QtMultimedia.QSound.play(soundFile)            
    else:
        soundFile = locateFile(fldbk, caller, soundFile, IDREF)
        if soundFile:
            QtMultimedia.QSound.play(soundFile)

def locateFile(fldbk, caller, soundFile, IDREF=None):
    mFolder = QtWidgets.QFileDialog(fldbk, "Find missing recording?")
    mFolder.setFileMode(QtWidgets.QFileDialog.ExistingFile)
    mFolder.setOption(QtWidgets.QFileDialog.ReadOnly)
    if mFolder.exec():
        soundFile = mFolder.selectedFiles()[0]
        print(soundFile)
        if dataIndex.root.get("MediaFolder") is None or dataIndex.root.get("MediaFolder") != path.dirname(soundFile):
            setDefaultDirectory(fldbk, soundFile)
        if path.isfile(soundFile):
            if IDREF is None:
                caller.setItemData(caller.currentIndex(), soundFile, 37)
            else:
                caller.item(caller.currentRow(),0).setData(37, soundFile)
        return soundFile
    else:
        return False

def mChooseDir(fldbk):
    mFolder = QtWidgets.QFileDialog(fldbk, "Choose a directory")
    mFolder.setFileMode(QtWidgets.QFileDialog.Directory)
    mFolder.setOption(QtWidgets.QFileDialog.ReadOnly)
    if mFolder.exec():
        soundFile = mFolder.selectedFiles()[0]
        dataIndex.root.set("MediaFolder",soundFile)
        dataIndex.unsavedEdit = 1
