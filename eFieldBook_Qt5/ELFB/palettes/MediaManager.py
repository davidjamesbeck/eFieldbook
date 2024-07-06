from PyQt6 import QtWidgets, QtCore
from ELFB.palettes import SessionDate
from ELFB import dataIndex, metaDataBtns
from os import path
import os
from xml.etree import ElementTree as etree
from .Ui_MediaManager import Ui_MediaManager


class MediaManager(QtWidgets.QDialog, Ui_MediaManager):
    """class for setting metadata for recorded media"""

    def __init__(self, parent, soundPanel):
        super(MediaManager, self).__init__(parent)
        self.setupUi(self)
        self.soundPanel = soundPanel
        codeList = sorted(dataIndex.speakerDict.keys())
        for index, item in enumerate(codeList):
            try:
                fullName = dataIndex.speakerDict.get(item).findtext('Name')
                if fullName == 'Unattributed':
                    fullName = 'unattr.'
                item += ' (' + fullName + ')'
            except TypeError:
                item += ' (unattr.)'
            codeList[index] = item
        self.speakerCode.insertItems(0, codeList)

        """manager is initially created with defaults filled in"""
        """these are overwritten if an existing media element is called"""
        if dataIndex.lastSpeaker:
            j = self.speakerCode.findText(dataIndex.lastSpeaker, QtCore.Qt.MatchFlag.MatchStartsWith)
            self.speakerCode.setCurrentIndex(j)

        codeList = sorted(dataIndex.rschrDict.keys())
        self.researcherCode.insertItems(0, codeList)
        if dataIndex.lastRschr:
            j = self.researcherCode.findText(dataIndex.lastRschr, QtCore.Qt.MatchFlag.MatchExactly)
            self.researcherCode.setCurrentIndex(j)

        if dataIndex.lastDate:
            self.date.setPlainText(dataIndex.lastDate)

        if dataIndex.lastApparatus:
            self.apparatus.setText(dataIndex.lastApparatus)

        if dataIndex.lastPlace:
            self.place.setText(dataIndex.lastPlace)

        if dataIndex.lastFileFormat:
            self.type.setText(dataIndex.lastFileFormat)

    def setDate(self):
        dataIndex.lastDate = self.date.dateTime()
        dataIndex.unsavedEdit = 1

    def setSpeaker(self):
        lastSpeaker = self.speakerCode.currentText().split(None, 1)
        dataIndex.lastSpeaker = lastSpeaker[0]
        dataIndex.unsavedEdit = 1

    def setRschr(self):
        lastRschr = self.researcherCode.currentText().split(None, 1)
        dataIndex.lastRschr = lastRschr[0]
        dataIndex.unsavedEdit = 1

    def setValues(self, mediaID, caller, item, metadataLabel=None):
        """loads current values when the palette is called"""
        self.caller = caller
        self.mediaID = mediaID
        self.metadataLabel = metadataLabel
        self.item = item
        child = dataIndex.mediaDict[mediaID]
        self.child = child
        attribDict = child.attrib
        if 'Spkr' in attribDict and len(attribDict['Spkr']) != 0:
            sNode = dataIndex.speakerDict[attribDict['Spkr']]
            try:
                fullName = attribDict['Spkr'] + ' (' + sNode.find('Name').text + ')'
            except AttributeError:
                fullName = attribDict['Spkr'] + ' (unattr.)'
            l = self.speakerCode.findText(fullName, QtCore.Qt.MatchFlag.MatchExactly)
            self.speakerCode.setCurrentIndex(l)
        elif dataIndex.lastSpeaker:
            pass
        else:
            self.speakerCode.setCurrentIndex(-1)
        if 'Rschr' in attribDict and len(attribDict['Rschr']) != 0:
            l = self.researcherCode.findText(attribDict['Rschr'], QtCore.Qt.MatchFlag.MatchExactly)
            self.researcherCode.setCurrentIndex(l)
        elif dataIndex.lastRschr:
            pass
        else:
            self.speakerCode.setCurrentIndex(-1)

        if 'Date' in attribDict and len(attribDict['Date']) != 0:
            tDate = attribDict['Date']
            self.date.setPlainText(tDate)
        elif dataIndex.lastDate:
            pass
        else:
            self.date.setPlainText(SessionDate.dateFinder())

        if 'Filename' in attribDict and len(attribDict['Filename']) != 0:
            self.filename.setText(attribDict['Filename'])

        if 'Place' in attribDict and len(attribDict['Place']) != 0:
            self.place.setText(attribDict['Place'])

        if 'FileType' in attribDict and len(attribDict['FileType']) != 0:
            self.type.setText(attribDict['FileType'])

        if 'Catalog' in attribDict and len(attribDict['Catalog']) != 0:
            self.catalog.setText(attribDict['Catalog'])

        if 'Apparatus' in attribDict and len(attribDict['Apparatus']) != 0:
            self.apparatus.setText(attribDict['Apparatus'])

        if child.find('Comments') is not None:
            self.comments.setText(child.findtext('Comments'))

    def getValues(self):
        """retrieves values from palette for updating in XML file"""
        print('entering getValues')
        fldbk = dataIndex.fldbk
        caller = self.caller
        child = self.child
        mediaID = self.mediaID
        item = self.item
        #        metadataLabel = self.metadataLabel
        metaData = []
        newname = None
        if self.speakerCode.currentIndex() == -1:
            speaker = 'XX'
            metaData.append(speaker)
        else:
            speakerPieces = self.speakerCode.currentText().split(None, 1)
            speaker = speakerPieces[0]
            metaData.append(speaker)
        if self.researcherCode.currentIndex() == -1:
            researcher = 'YYY'
            metaData.append(researcher)
        else:
            researcher = self.researcherCode.currentText()
            metaData.append(researcher)
        metaData.append(self.date.toPlainText())
        metaData.append(self.filename.toPlainText())
        metaData.append(self.type.toPlainText())
        metaData.append(self.place.toPlainText())
        metaData.append(self.apparatus.toPlainText())
        metaData.append(self.catalog.toPlainText())
        metaData.append(self.comments.toPlainText())
        oldFile = child.get('Filename')
        oldResearcher = child.get('Rschr')
        # TODO: move this back into the calling routine in metaDataBtns?
        if caller == fldbk.mMediaTable:
            fldbk.mMediaTable.item(fldbk.mMediaTable.currentRow(), 0).setText(self.filename.toPlainText())
            fldbk.mMediaTable.item(fldbk.mMediaTable.currentRow(), 1).setText(speaker)
            fldbk.mMediaTable.item(fldbk.mMediaTable.currentRow(), 2).setText(researcher)
        if len(metaData[3]) != 0:
            """if there is a filename in the field"""
            if metaData[3] != oldFile:
                """if the filename has been changed by the user"""
                if item is None and caller == fldbk.mMediaTable:
                    """if no location for old file has been provided and the caller is the media table"""
                    item = caller.item(caller.currentRow(), 0).data(37)
                if item is not None:
                    """if a file location for old file has been provided"""
                    oldname = item
                elif dataIndex.root.get('MediaFolder'):
                    """if not, try to find the old file"""
                    testPath = dataIndex.root.get('MediaFolder') + "/" + oldFile
                    if os.path.isfile(testPath):
                        """old file in the default media folder"""
                        oldname = testPath
                    else:
                        """find the file manually, might have been moved"""
                        oldname = self.locateFile(fldbk, caller, oldFile, mediaID)
                else:
                    """there is no default media folder and no location for the old file is provided"""
                    oldname = self.locateFile(fldbk, caller, oldFile, mediaID)
                if oldname is False:
                    return False
                prefix = os.path.dirname(oldname)
                newname = prefix + "/" + metaData[3]
                os.rename(oldname, newname)
                child.set('Filename', metaData[3])
        else:
            return False
        if len(metaData[0]) != 0:
            child.set('Spkr', metaData[0])
        if len(metaData[1]) != 0:
            child.set('Rschr', metaData[1])
        if len(metaData[2]) != 0:
            child.set('Date', metaData[2])
        """metaData[3] is the filename, set in line 178 above"""
        if len(metaData[4]) != 0:
            child.set('FileType', metaData[4])
        if len(metaData[5]) != 0:
            child.set('Place', metaData[5])
        if len(metaData[6]) != 0:
            child.set('Apparatus', metaData[6])
        if len(metaData[7]) != 0:
            child.set('Catalog', metaData[7])
        if len(metaData[8]) != 0:
            if child.find('Comments') is None:
                etree.SubElement(child, 'Comments')
                child[0].text = metaData[8]
            else:
                child.find('Comments').text = metaData[8]
        if oldFile != metaData[3] or oldResearcher == "???":
            for i in range(0, fldbk.mMediaTable.rowCount()):
                if fldbk.mMediaTable.item(i, 0).text() == oldFile:
                    fldbk.mMediaTable.item(i, 0).setText(metaData[3])
                    fldbk.mMediaTable.item(i, 1).setText(metaData[0])
                    fldbk.mMediaTable.item(i, 2).setText(metaData[1])
                    if newname:
                        fldbk.mMediaTable.item(i, 0).setData(37, newname)
                    fldbk.mMediaTable.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
                    break
#        print(etree.tostring(child, encoding='unicode'))
#        print(etree.tostring(self.child, encoding='unicode'))
        dataIndex.mediaDict[mediaID] = self.child
        self.speaker = metaData[0]
        self.date = metaData[2]
        return metaData

    def locateFile(self, fldbk, caller, soundFile, IDREF=None):
        mFolder = QtWidgets.QFileDialog(fldbk, "Find recording to rename.")
        mFolder.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        mFolder.setOption(QtWidgets.QFileDialog.Option.ReadOnly)
        if mFolder.exec():
            soundFile = mFolder.selectedFiles()[0]
            if dataIndex.root.get("MediaFolder") is None or dataIndex.root.get("MediaFolder") != path.dirname(
                    soundFile):
                metaDataBtns.setDefaultDirectory(fldbk, soundFile)
            if path.isfile(soundFile):
                if IDREF is None:
                    caller.setItemData(caller.currentIndex(), soundFile, 37)
                else:
                    caller.item(caller.currentRow(), 0).setData(37, soundFile)
            return soundFile
        else:
            return False

    def renameWindow(self, fileName):
        """renames window for filename when manager is created"""
        self.setWindowTitle(QtWidgets.QApplication.translate("MediaManager", "Metadata: %s" % fileName, None))

    def clearAll(self):
        """clears fields when Reset button is clicked"""
        print('entering clearAll')
        self.apparatus.clear()
        self.catalog.clear()
        self.place.clear()
        self.comments.clear()

    def setComboBoxes(self):
        self.speakerCode.setCurrentIndex(-1)
        self.researcherCode.setCurrentIndex(-1)

    @QtCore.pyqtSlot(QtWidgets.QAbstractButton)
    def on_buttonBox_clicked(self, button):
        """
        button box code
        """
        print("clicked on button ", self.buttonBox.buttonRole(button))
        if self.buttonBox.buttonRole(button) == QtWidgets.QDialogButtonBox.ButtonRole.ResetRole:
            print('preparing to clear palette')
            self.clearAll()
        elif self.buttonBox.buttonRole(button) == QtWidgets.QDialogButtonBox.ButtonRole.AcceptRole:
            print('preparing to get values')
            self.getValues()
            dataIndex.lastApparatus = self.apparatus.toPlainText()
            dataIndex.lastPlace = self.place.toPlainText()
            dataIndex.lastFileFormat = self.type.toPlainText()
            dataIndex.unsavedEdits = 1
            self.soundPanel.updatePanel(self.speaker,  self.date)
#            cardLoader.loadLexCard(dataIndex.lexDict[dataIndex.currentCard], navBtn=False, currentRecording=self.child)
            self.accept()


class GrammarMediaManager(MediaManager):
    @QtCore.pyqtSlot(QtWidgets.QAbstractButton)
    def on_buttonBox_clicked(self, button):
        """
        button box code
        """
        if self.buttonBox.buttonRole(button) == 7:
            self.clearAll()
        elif self.buttonBox.buttonRole(button) == 0:
            dataIndex.lastApparatus = self.apparatus.toPlainText()
            dataIndex.lastPlace = self.place.toPlainText()
            dataIndex.lastFileFormat = self.type.toPlainText()
            dataIndex.unsavedEdits = 1
            self.accept()
