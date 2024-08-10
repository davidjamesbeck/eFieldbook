# -*- coding: utf-8 -*-

"""
Module implementing RecordBrowser.
"""

from PyQt6 import QtWidgets, QtCore, QtGui
from ELFB import dataIndex, cardLoader, menus
from ELFB.palettes import StyledInputDialog
from ELFB.outputFilters import lexToText, egToText

from .Ui_RecordBrowser import Ui_Dialog


class RecordBrowser(QtWidgets.QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """

    def __init__(self, parent, selection=None):

        super(RecordBrowser, self).__init__(parent)
        self.setupUi(self)
        iconSize = QtCore.QSize(40, 40)
        prevIcon = QtGui.QIcon(':PrevBtn.png')
        self.PrevBtn.setIcon(prevIcon)
        self.PrevBtn.setIconSize(iconSize)
        nextIcon = QtGui.QIcon(':NextBtn.png')
        self.NextBtn.setIcon(nextIcon)
        self.NextBtn.setIconSize(iconSize)
        self.Save.setEnabled(0)
        self.fldbk = dataIndex.fldbk
        self.listIndex = 0
        self.earmarks = []
        self.oldEarmarks = []
        self.hitList = []
        self.scratchPadName = None
        self.progressBar.setMinimum(-1)
        self.progressBar.setMaximum(0)
        if selection is None:
            results = self.fldbk.cSearchResults.model()
        else:
            results = None
            exampleList = selection.split('\t')
            exampleList = exampleList[3:]
            for item in exampleList:
                try:
                    index = item.index(':')
                except ValueError:
                    continue
                self.hitList.append(item[:index])
                self.progressBar.setMaximum(len(self.hitList))
        if results:
            for i in range(0, results.rowCount()):
                self.hitList.append(results.item(i, 0).data(35))
                self.progressBar.setMaximum(len(self.hitList))

    @QtCore.pyqtSlot()
    def on_PrevBtn_released(self):
        """
        Step back to previous search result.
        """
        if len(self.hitList) == 0:
            return
        if self.fldbk.tabWidget.currentIndex() < 5:
            self.listIndex -= 1
            if self.listIndex < 0:
                self.listIndex = len(self.hitList) - 1
        tCard = self.hitList[self.listIndex]
        dataIndex.currentCard = tCard
        self.showCards(tCard)

    @QtCore.pyqtSlot()
    def on_NextBtn_released(self):
        """
        Step to next search result.
        """
        if len(self.hitList) == 0:
            return
        if self.fldbk.tabWidget.currentIndex() != 5:
            self.listIndex += 1
        try:
            tCard = self.hitList[self.listIndex]
        except IndexError:
            self.listIndex = 0
            tCard = self.hitList[self.listIndex]
        dataIndex.currentCard = tCard
        self.showCards(tCard)

    def showCards(self, tCard):
        if tCard[0] == "T":
            targetCard = dataIndex.textDict[tCard]
            cardLoader.loadtextCard(targetCard)
            self.fldbk.tabWidget.setCurrentIndex(2)
            cardLoader.resetNavBars(self.fldbk.tTextNav, tCard)
        elif tCard[0] == "L":
            targetCard = dataIndex.lexDict[tCard]
            cardLoader.loadLexCard(targetCard)
            self.fldbk.tabWidget.setCurrentIndex(1)
            cardLoader.resetNavBars(self.fldbk.lLexNav, tCard)
        elif tCard[0] == "E":
            targetCard = dataIndex.exDict[tCard]
            cardLoader.loadExCard(targetCard)
            self.fldbk.tabWidget.setCurrentIndex(3)
        elif tCard[0] == "D":
            targetCard = dataIndex.dataDict[tCard]
            cardLoader.loadDataCard(targetCard)
            self.fldbk.tabWidget.setCurrentIndex(4)
            cardLoader.resetNavBars(self.fldbk.dDataNav, tCard)
        self.progressBar.setValue(self.listIndex)
        if tCard in self.earmarks:
            self.Select.setChecked(1)
        else:
            self.Select.setChecked(0)

    @QtCore.pyqtSlot()
    def on_NewList_released(self):
        """
        Creates new scratchpad
        """
        if len(self.earmarks) == 0:
            saveDoc = ''
        else:
            saveDoc = self.makeSaveDoc()
            """need to check to see if existing earmarks have to be saved first separately"""
            if self.scratchPadName is not None:
                if self.oldEarmarks != self.earmarks:
                    if self.scratchPadName[1] == 'file':
                        self.saveAsFile(self.scratchPadName[0], saveDoc)
                    else:
                        self.saveAsDataset(self.scratchPadName[0], saveDoc)
                saveDoc = ''
                self.earmarks = []
                self.Select.setChecked(0)
        self.chooseTypeAndSave(saveDoc)

    def chooseTypeAndSave(self, saveDoc):
        mbox = QtWidgets.QMessageBox()
        mbox.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        mbox.setText("Scratch pad.")
        mbox.setInformativeText('Save scratch pad as a dataset or a file?')
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
        datasetButton = QtWidgets.QPushButton()
        datasetButton.setText('Dataset')
        mbox.addButton(datasetButton, QtWidgets.QMessageBox.ButtonRole.ActionRole)
        fileButton = QtWidgets.QPushButton()
        fileButton.setText('File')
        mbox.addButton(fileButton, QtWidgets.QMessageBox.ButtonRole.ActionRole)
        mbox.exec()
        if mbox.clickedButton() == fileButton:
            fileDialog = QtWidgets.QFileDialog()
            fileDialog.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
            self.setVisible(0)
            fname = fileDialog.getSaveFileName(self.fldbk, "Save Scratchpad As...")[0]
            if fname:
                self.scratchPadName = [fname, 'file']
                self.saveAsFile(fname, saveDoc)
                self.setVisible(1)
            else:
                self.setVisible(1)
                return
        elif mbox.clickedButton() == datasetButton:
            nameBox = StyledInputDialog.StyledInputDialog(self.fldbk)
            nameBox.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
            nameBox.setWindowTitle('Scratchpad')
            nameBox.inputLabel.setText('Give the scratchpad a name.')
            if nameBox.exec():
                fname = nameBox.returnInput()
                self.scratchPadName = [fname, 'dataset']
                menus.newDataset(self.fldbk, fname, saveDoc)
            else:
                return
        else:
            return

    def saveAsFile(self, fname, saveDoc=''):
        saveDoc = saveDoc.replace('<p>', '')
        saveDoc = saveDoc.replace('</p>', '\n')
        saveFile = open(fname, "w", encoding="UTF-8")
        saveFile.write(saveDoc)
        saveFile.close()

    def saveAsDataset(self, saveDoc):
        DSetID = dataIndex.lastDset
        DSet = dataIndex.dataDict[DSetID]
        DSet.find('Data').text = saveDoc

    def makeSaveDoc(self):
        saveDoc = ''
        for item in self.earmarks:
            if item[0] == "L":
                newText = lexToText(item)
            elif item[0] == "E":
                newText = egToText(item)
            else:
                dataNode = dataIndex.dataDict[item]
                reference = dataNode.find('Title').text
                saveDoc += '<p>example in Dataset “' + reference + '”</p>'
            saveDoc += '<p>' + newText + '</p>'
        return saveDoc

    @QtCore.pyqtSlot()
    def on_Save_released(self):
        """
        Saves existing scratchpad.
        First checks to make sure one exists.
        """
        if self.scratchPadName is None:
            self.on_NewList_released()
        elif self.scratchPadName[1] == 'file':
            saveDoc = self.makeSaveDoc()
            self.saveAsFile(self.scratchPadName[0], saveDoc)
        else:
            saveDoc = self.makeSaveDoc()
            self.saveAsDataset(saveDoc)

    @QtCore.pyqtSlot()
    def on_Discard_released(self):
        """
        Delete result from list.
        """
        if self.fldbk.tabWidget.currentIndex() > 3:
            return
        self.fldbk.cSearchResults.model().removeRow(self.listIndex)
        del self.hitList[self.listIndex]
        self.listIndex -= 1
        if self.listIndex < 0:
            self.listIndex = len(self.hitList) - 1
        self.progressBar.setMaximum(len(self.hitList))
        self.progressBar.setValue(self.listIndex)
        prevCard = self.hitList[self.listIndex]
        self.showCards(prevCard)

    @QtCore.pyqtSlot()
    def on_Select_released(self):
        """
        Selects/deselects example for earmarking.
        """
        if self.Select.checkState() == 0:
            try:
                badItem = self.hitList[self.listIndex]
                badIndex = self.earmarks.index(badItem)
                del self.earmarks[badIndex]
                if len(self.earmarks) == 0:
                    self.Save.setEnabled(0)
            except ValueError:
                pass
            except IndexError:
                pass
        else:
            self.oldEarmarks = self.earmarks
            self.earmarks.append(self.hitList[self.listIndex])
            self.Save.setEnabled(1)

    def closeEvent(self, event):
        if len(self.earmarks) != 0:
            mbox = QtWidgets.QMessageBox()
            mbox.setText("Keep scratch pad.")
            mbox.setInformativeText('Scratchpad will be reloaded next time the browser is opened.')
            mbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Cancel | QtWidgets.QMessageBox.StandardButton.No | QtWidgets.QMessageBox.StandardButton.Yes)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Yes)
            mbox.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
            mbox.exec()
            if mbox.result() == QtWidgets.QMessageBox.StandardButton.Ok:
                saveDoc = self.makeSaveDoc()
                self.chooseTypeAndSave(saveDoc)
            elif mbox.result() == QtWidgets.QMessageBox.StandardButton.Cancel:
                event.ignore()
        self.hitList = []
        pass
