# -*- coding: utf-8 -*-

"""
Module implementing SoundPanel.
Provides basic media access functionality on
data cards
"""

from PyQt6 import QtWidgets, QtGui, QtCore#, QtMultimedia, QtNetwork
from ELFB import dataIndex, metaDataBtns, playaudio
from ELFB.palettes import MediaManager
from os import path
from xml.etree import ElementTree as etree
from .Ui_SoundPanel import Ui_SoundPanel


class SoundPanel(QtWidgets.QWidget, Ui_SoundPanel):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(SoundPanel, self).__init__(parent)
        self.setupUi(self)
        soundIconSize = QtCore.QSize(23, 23)
        soundIcon = QtGui.QIcon(':SpeakerBtn.png')
        self.PlaySoundBtn.setStyleSheet('background: transparent; padding: 0px; min-width: 23px; min-height: 23px;')
        self.PlaySoundBtn.setIcon(soundIcon)
        self.PlaySoundBtn.setIconSize(soundIconSize)
        infoIconSize = QtCore.QSize(18, 18)
        infoIcon = QtGui.QIcon(':infoBtn.png')
        self.SoundMetaBtn.setStyleSheet('background: transparent; padding: 0px; min-width: 18px; min-height: 18px;')
        self.SoundMetaBtn.setIcon(infoIcon)
        self.SoundMetaBtn.setIconSize(infoIconSize)
        self.GrammarManagerCell = None

    def loadMedia(self, root, mediaRefs=None, currentRecording=None):
        print('entering loadMedia')
        self.Recordings.clear()
        self.SoundFileMeta.clear()
        if root is not None:
            """root will be None if the caller is Grammar Manager"""
            media = root.findall('Sound')
        else:
            media = None
        mediaList = []
        if media is not None:
            for i in range(0, len(media)):
                mediaRef = media[i].attrib.get('MediaRef')
                mediaList.append(mediaRef)
        if mediaRefs is not None:
            mediaList += mediaRefs
        if len(mediaList) != 0:
            for i, item in enumerate(mediaList):
                mediaElement = dataIndex.mediaDict[item]
                recording = mediaElement.attrib.get('Filename')
                self.Recordings.insertItem(i, recording)
                self.Recordings.setItemData(i, item, 35)
                if i == 0:
                    speaker = mediaElement.attrib.get('Spkr')
                    date = mediaElement.attrib.get('Date')
                    self.updatePanel(speaker,  date,  currentRecording=None)
        else:
            self.Recordings.setEnabled(0)
            self.DelMediaBtn.setEnabled(0)

    def mediaInfo(self):
        """item is the path to file, data 37 in combobox item"""
        i = self.Recordings.currentIndex()
        mediaID = self.Recordings.itemData(i, 35)
        item = self.Recordings.itemData(i, 37)
        mManager = MediaManager.MediaManager(dataIndex.fldbk, self)
        mManager.renameWindow(self.Recordings.currentText())
        mManager.setValues(mediaID, self.Recordings, item, self.SoundFileMeta)
        mManager.exec()

    def playSound(self):
        """begins by checking to see if temporary paths have been set for sound files
        (rather than building the path each time)"""
        if self.Recordings.currentIndex() == -1:
            return
        else:
            mediaElement = dataIndex.mediaDict[self.Recordings.currentData(35)]
            speaker = mediaElement.attrib.get('Spkr')
            date = mediaElement.attrib.get('Date')
            print(speaker,  date)
        if dataIndex.root.get("MediaFolder"):
            prefix = dataIndex.root.get("MediaFolder")
        else:
            prefix = None
        soundFile = self.Recordings.currentText()
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(soundFile)
        self.updatePanel(speaker,  date, mediaElement)
        oldSoundFile = soundFile
        if prefix is not None:
            soundFile = prefix + "/" + soundFile
        if path.isfile(soundFile):
            playaudio.soundOutput(soundFile)
        else:
            soundFile = self.locateFile(soundFile)
            if soundFile:
                if path.basename(soundFile) != oldSoundFile:
                    mediaElement.set('Filename', path.basename(soundFile))
                    self.Recordings.setItemText(self.Recordings.currentIndex(), path.basename(soundFile))
                playaudio.soundOutput(soundFile)
    
    def updatePanel(self,  speaker,  date,  currentRecording=None):
        print('entering updatePanel')
        if currentRecording == None:
            self.Recordings.setCurrentIndex(0)
            self.SoundFileMeta.setText(speaker + " " + date)
        else:
            soundfile = currentRecording.attrib.get('Filename')
            filenameindex = self.Recordings.findText(soundfile)
            speaker = currentRecording.attrib.get('Spkr')
            date = currentRecording.attrib.get('Date')
            self.Recordings.setCurrentIndex(filenameindex)
            self.SoundFileMeta.setText(speaker + " " + date)
        self.Recordings.setEnabled(1)
        self.DelMediaBtn.setEnabled(1)
        self.update()
        
    def locateFile(self, soundFile):
        mFolder = QtWidgets.QFileDialog(dataIndex.fldbk, "Find missing recording?")
        mFolder.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        mFolder.setOption(QtWidgets.QFileDialog.Option.ReadOnly)
        if mFolder.exec():
            soundFile = mFolder.selectedFiles()[0]
            if dataIndex.root.get("MediaFolder") is None or dataIndex.root.get("MediaFolder") != path.dirname(
                    soundFile):
                self.setDefaultDirectory(soundFile)
            return soundFile
        else:
            return False

    def setDefaultDirectory(self, newFile):
        setPathBox = QtWidgets.QMessageBox()
        setPathBox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        setPathBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.No | QtWidgets.QMessageBox.StandardButton.Ok)
        setPathBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        setPathBox.setText('Set default directory.')
        setPathBox.setInformativeText('Use this directory as the default for locating recordings?')
        setPathBox.exec()
        if setPathBox.result() == QtWidgets.QMessageBox.StandardButton.Ok:
            prefix = path.dirname(newFile)
            dataIndex.fldbk.mMediaPath.setText(prefix)
            dataIndex.root.set("MediaFolder", prefix)
            dataIndex.unsavedEdit = 1

    def delMedia(self):
        try:
            self.SoundFileMeta.clear()
        except AttributeError:
            pass
        i = self.Recordings.currentIndex()
        medID = self.Recordings.itemData(i, 35)
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
                if QtCore.QObject.objectName(QtCore.QObject.parent(self)) == 'lexicon':
                    if lexNode.find('Sound[@MediaRef="%s"]' % medID) is not None:
                        badNode = lexNode.find('Sound[@MediaRef="%s"]' % medID)
                        lexNode.remove(badNode)
                elif QtCore.QObject.objectName(QtCore.QObject.parent(self)) == 'gManager':
                    if lexNode.find('Grm[@MediaRef="%s"]' % medID) is not None:
                        badNode = lexNode.find('Grm[@MediaRef="%s"]' % medID)
                        del badNode.attrib['MediaRef']
                    elif lexNode.find('C2[@MediaRef="%s"]' % medID) is not None:
                        badNode = lexNode.find('C2[@MediaRef="%s"]' % medID)
                        del badNode.attrib['MediaRef']
            elif address[0] == "E":
                egNode = dataIndex.exDict[address]
                badNode = egNode.find('Sound[@MediaRef="%s"]' % medID)
                egNode.remove(badNode)
            elif address[0] == "D":
                dataNode = dataIndex.dataDict[address]
                badNode = dataNode.find('Sound[@MediaRef="%s"]' % medID)
                dataNode.remove(badNode)
            elif address[0] == "T":
                textNode = dataIndex.textDict[address]
                badNode = textNode.find('Sound[@MediaRef="%s"]' % medID)
                textNode.remove(badNode)
            self.Recordings.removeItem(i)
        dataIndex.unsavedEdit = 1
        if self.Recordings.count() == 0:
            self.DelMediaBtn.setEnabled(0)

    def fileExists(self, item, newName):
        node = dataIndex.root.find('Media[@Filename="%s"]' % newName)
        if path.dirname(item) != dataIndex.root.attrib.get('MediaFolder'):
            file = node.attrib.get('Filename')
            speaker = node.attrib.get('Spkr')
            date = node.attrib.get('Date')
            fileInfo = file + " [" + speaker + " " + date + "]"
            msgbox = QtWidgets.QMessageBox()
            msgbox.setText("File in database.")
            msgbox.setInformativeText('There is already a recording named\n\n%s\n\nin the database. '
                                      'If this is not the recording you are linking to, '
                                      'select "Cancel" and rename the file.' % fileInfo)
            msgbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Cancel | QtWidgets.QMessageBox.StandardButton.Ok)
            msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            msgbox.exec()
            if msgbox.result() == QtWidgets.QMessageBox.StandardButton.Cancel:
                return False
        medID = node.get('MedID')
        return medID

    def addLinktoXML(self, medID):
        """links the sound file to the current element"""
        if dataIndex.currentCard[0] == 'L':
            child = dataIndex.lexDict[dataIndex.currentCard]
            if QtCore.QObject.objectName(QtCore.QObject.parent(self)) == 'lexicon':
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
                child.insert(i, newElem)
                newElem.attrib['MediaRef'] = medID
            elif QtCore.QObject.objectName(QtCore.QObject.parent(self)) == 'gManager':
                self.placeMediaRef(medID)
        elif dataIndex.currentCard[0] == 'T':
            child = dataIndex.textDict[dataIndex.currentCard]
            newElem = etree.Element('Sound')
            child.append(newElem)
            newElem.attrib['MediaRef'] = medID
        elif dataIndex.currentCard[0] == 'E':
            child = dataIndex.exDict[dataIndex.currentCard]
            newElem = etree.Element('Sound')
            child.append(newElem)
            newElem.attrib['MediaRef'] = medID
        elif dataIndex.currentCard[0] == 'D':
            child = dataIndex.dataDict[dataIndex.currentCard]
            newElem = etree.Element('Sound')
            child.append(newElem)
            newElem.attrib['MediaRef'] = medID

    def placeMediaRef(self, medID):
        """when the sound is added in the Grammar Manager, we have to know if it goes
        on a Grm Node or a C2 node"""
        whichTag = QtCore.QObject.parent(self).whichTable
        r = self.GrammarManagerCell[0]
        if whichTag == 'grammar':
            tableCell = QtCore.QObject.parent(self).grammar.item(r, 0)
            tableCell.setData(35, medID)
        elif whichTag == 'C2':
            tableCell = QtCore.QObject.parent(self).C2.item(r, 0)
            tableCell.setData(35, medID)

    def clearAll(self):
        self.Recordings.clear()
        self.SoundFileMeta.clear()

    def fileDuplicate(self, item, newName):
        """warns user that the media file selected may have a duplicate name
        Cancel bails, Okay means you know it is a file alread in the database"""
        node = dataIndex.root.find('Media[@Filename="%s"]' % newName)
        file = node.attrib.get('Filename')
        if node.attrib.get('Spkr'):
            speaker = node.attrib.get('Spkr')
        else:
            speaker = "??"
        if node.attrib.get('Date'):
            date = node.attrib.get('Date')
        else:
            date = "??"
        medID = node.attrib.get('MedID')
        fileInfo = file + " [" + speaker + " " + date + "]"
        msgbox = QtWidgets.QMessageBox()
        msgbox.setText("File in database.")
        msgbox.setInformativeText('There is already a recording named\n\n%s\n\nin the database. '
                                  'Media files should have unique names, so if '
                                  'this isn’t the one you want, Cancel and rename the file.' % fileInfo)
        msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel | QtWidgets.QMessageBox.StandardButton.Ok)
        msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        msgbox.exec()
        if msgbox.result() == QtWidgets.QMessageBox.StandardButton.Ok:
            return medID
        else:
            return False

    def newMedia(self):
        newFile = QtWidgets.QFileDialog(dataIndex.fldbk, "Add recordings.")
        if dataIndex.root.get("MediaFolder") is not None:
            newFile.setDirectory(dataIndex.root.get("MediaFolder"))
        else:
            """this keeps the finder out of the interior of the application bundle"""
            filePath = path.dirname(newFile.directory().currentPath())
            fileDir = path.split(filePath)
            if fileDir[1] == 'com.UNTProject.eFieldbook':
                newFile.setDirectory(dataIndex.homePath)
        newFile.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        if newFile.exec():
            newNames = newFile.selectedFiles()
            newPath = newNames[0]
            if dataIndex.root.get("MediaFolder") is None or dataIndex.root.get("MediaFolder") != path.dirname(newPath):
                self.setDefaultDirectory(newPath)
            sound2play = newPath
            newName = path.basename(newPath)
            node = dataIndex.root.find('Media[@Filename="%s"]' % newName)
            if node is None:
                """create a new <Media> Node, add to the media table"""
                medID, node = metaDataBtns.updateMediaInfo(newPath, newName)
                """add additional information to the <Media> Node"""
                mManager = MediaManager.MediaManager(dataIndex.fldbk)
                mManager.renameWindow(newName)
                mManager.setValues(medID, self.Recordings, newPath, self.SoundFileMeta)
                #                mManager.setComboBoxes()
                mManager.exec()
            else:
                medID = self.fileDuplicate(newPath, newName)
                if not medID:
                    return
            self.Recordings.addItem(newName)
            self.Recordings.setCurrentIndex(self.Recordings.findText(newName, QtCore.Qt.MatchFlag.MatchExactly))
            self.Recordings.setItemData(self.Recordings.currentIndex(), medID, 35)
            self.Recordings.setEnabled(1)
            try:
                speaker = node.get('Spkr')
                date = node.get('Date')
                self.SoundFileMeta.setText(speaker + " " + date)
            except TypeError:
                pass
            self.DelMediaBtn.setEnabled(1)
            self.addLinktoXML(medID)
            playaudio.soundOutput(sound2play)
            dataIndex.unsavedEdit = 1
            return medID

    @QtCore.pyqtSlot(int)
    def on_Recordings_activated(self, p0):
        """
        plays the sound shown in the combobox list if selection is changed, 
        and updates the metadata synopsis on the card
        calls the play sound button command
        """
        print('entering on_Recordings_activated')
        self.playSound()
#        soundID = self.Recordings.itemData(self.Recordings.currentIndex(), 35)
#        child = dataIndex.mediaDict[soundID]
#        speaker = child.attrib.get('Spkr')
#        date = child.attrib.get('Date')
#        self.SoundFileMeta.setText(speaker + ' ' + date)

    @QtCore.pyqtSlot()
    def on_PlaySoundBtn_released(self):
        """
        plays sound when speaker button is pressed
        """
        self.playSound()

    @QtCore.pyqtSlot()
    def on_SoundMetaBtn_released(self):
        """
        updates label with recording info
        """
        print('entering on_SoundMetaBtn_released')
        if self.Recordings.count() != 0:
            self.mediaInfo()

    @QtCore.pyqtSlot()
    def on_AddMediaBtn_released(self):
        """
        adds media to card.
        """
        self.newMedia()

    @QtCore.pyqtSlot()
    def on_DelMediaBtn_released(self):
        """
        unlinks recording from card
        """
        if self.Recordings.count() != 0:
            self.delMedia()
