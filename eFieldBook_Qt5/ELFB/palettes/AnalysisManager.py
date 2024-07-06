# -*- coding: utf-8 -*-

"""
Module implementing AnalysisManager.
This dialog adds and manages new texts
"""

from PyQt6 import QtGui, QtWidgets, QtCore
from ELFB import NumberedLineEdit, idGenerator, dataIndex, cardLoader, formattingHandlers, autoparsing, MissingDataBox, \
    update
from xml.etree import ElementTree as etree
from os import path
from ELFB.palettes import SessionDate, ElanImporter
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDialog
from .Ui_AnalysisManager import Ui_Dialog


class AnalysisManager(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        super(AnalysisManager, self).__init__(parent)
        self.setupUi(self)
        self.setModal(0)
        self.portal.setTabStopDistance(15)
        self.tNumberBox = NumberedLineEdit.TextNumberWidget(self.tPortalBox, self.portal)
        self.tNumberBox.setGeometry(8, 8, 875, 444)
        self.tNumberBox.setVisible(1)
        self.replaceBtn.setEnabled(0)
        self.findReplaceBtn.setEnabled(0)
        self.replaceAllBtn.setEnabled(0)
        self.replaceTerm.setEnabled(0)
        self.rpcLabel.setStyleSheet('color: gray;')
        self.removeHiliteBtn.setEnabled(0)
        self.alignTextBtn.setEnabled(0)
        self.importSelector.addItem('ELAN file')
        self.helpBtn.setStyleSheet('QToolButton {border: 0px; background: transparent;'
                                   ' padding: 0px; min-width: 40px; min-height: 40px;}'
                                   'QToolButton:pressed {border: 3px outset transparent;}')
        newCardIconSize = QtCore.QSize(40, 40)
        newCardIcon = QtGui.QIcon(':HelpBtn.png')
        self.helpBtn.setIcon(newCardIcon)
        self.helpBtn.setIconSize(newCardIconSize)
        self.L2Gloss = 0

    def toggleActivation(self, checked):
        """
        makes the replace functions available or hides them
        when the checkbox is toggled
        """
        if checked == 1:
            self.replaceBtn.setEnabled(1)
            self.findReplaceBtn.setEnabled(1)
            self.replaceAllBtn.setEnabled(1)
            self.replaceTerm.setEnabled(1)
            self.rpcLabel.setStyleSheet('color: black;')
        else:
            self.replaceBtn.setEnabled(0)
            self.findReplaceBtn.setEnabled(0)
            self.replaceAllBtn.setEnabled(0)
            self.replaceTerm.setEnabled(0)
            self.rpcLabel.setStyleSheet('color: gray;')

    def clearNewText(self):
        """
        clears all fields
        """
        self.portal.clear()
        self.tNumberBox.number_bar.update()
        self.tTitle.clear()
        self.tNewSource.clear()
        self.tNewResearcher.clear()
        self.tNewDate.clear()
        self.tNewUpdated.clear()
        self.tNewTranscriber.clear()
        self.lineErrorNumber.setText('')
        self.wordErrorNumber.setText('')
        self.morphErrorNumber.setText('')
        self.tLinesValidBtn.setChecked(0)
        self.tWordsValidBtn.setChecked(0)
        self.tMorphsValidBtn.setChecked(0)

    def checkIleg(self, parseLine, ilegLine, blockNumber):
        """
        ensures that there are the same number of words on each line of the gloss
        """
        parseLine = parseLine.replace('\t\n', '')
        ilegLine = ilegLine.replace('\t\n', '')
        wordList = parseLine.split(' ')
        ilegList = ilegLine.split(' ')
        if len(wordList) != len(ilegList):
            self.tNumberBox.wordErrors.append(blockNumber - 2)
        else:
            for i, item in enumerate(wordList):
                morphList = item.split('–')
                abbrList = ilegList[i].split('–')
                if len(morphList) != len(abbrList):
                    self.tNumberBox.morphErrors.append(blockNumber - 2)
                    break
                else:
                    cliticList = item.split('=')
                    cliticGlossList = ilegList[i].split('=')
                    if len(cliticList) != len(cliticGlossList):
                        self.tNumberBox.morphErrors.append(blockNumber - 2)
                        break

    def editTracker(self):
        """
        removes hilighting from corrected lines
        """
        cursor = self.portal.textCursor()
        selection = cursor.select(QtGui.QTextCursor.SelectionType.BlockUnderCursor)
        try:
            if selection.background() == QtCore.Qt.GlobalColor.white:
                return
        except AttributeError:
            pass
        if len(self.tNumberBox.morphErrors) + len(self.tNumberBox.wordErrors) == 0:
            return
        text = self.portal.document()
        blockNumber = cursor.blockNumber()
        block = cursor.block()
        if len(self.tNumberBox.wordErrors) != 0:
            format = QtGui.QTextCharFormat()
            format.setBackground(QtCore.Qt.GlobalColor.white)
            for item in self.tNumberBox.wordErrors:
                if item == blockNumber + 1:
                    self.tNumberBox.wordErrors.remove(item)
                    nextBlock = text.findBlockByNumber(blockNumber + 1)
                    cursor = QtGui.QTextCursor(block)
                    cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                    cursor.setCharFormat(format)
                    cursor = QtGui.QTextCursor(nextBlock)
                    cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                    cursor.setCharFormat(format)
                    if self.tNumberBox.wordErrorIndex:
                        self.tNumberBox.wordErrorIndex -= 1
                    errorNumber = len(self.tNumberBox.wordErrors)
                    if errorNumber == 0:
                        self.wordErrorNumber.setText('')
                        self.tWordsValidBtn.setChecked(1)
                        self.wordErrorPrev.setEnabled(0)
                        self.wordErrorNext.setEnabled(0)
                    elif errorNumber == 1:
                        self.wordErrorNumber.setText('1 word error')
                    else:
                        self.wordErrorNumber.setText('%d word errors' % errorNumber)
                    break
                elif item == blockNumber:
                    self.tNumberBox.wordErrors.remove(item)
                    prevBlock = text.findBlockByNumber(blockNumber - 1)
                    cursor = QtGui.QTextCursor(prevBlock)
                    cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                    cursor.setCharFormat(format)
                    cursor = QtGui.QTextCursor(block)
                    cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                    cursor.setCharFormat(format)
                    if self.tNumberBox.wordErrorIndex:
                        self.tNumberBox.wordErrorIndex -= 1
                    errorNumber = len(self.tNumberBox.wordErrors)
                    if errorNumber == 0:
                        self.wordErrorNumber.setText('')
                        self.tWordsValidBtn.setChecked(1)
                        self.wordErrorPrev.setEnabled(0)
                        self.wordErrorNext.setEnabled(0)
                    elif errorNumber == 1:
                        self.wordErrorNumber.setText('1 word error')
                    else:
                        self.wordErrorNumber.setText('%d word errors' % errorNumber)
                    break
        if len(self.tNumberBox.morphErrors) != 0:
            format = QtGui.QTextCharFormat()
            format.setBackground(QtCore.Qt.GlobalColor.white)
            for item in self.tNumberBox.morphErrors:
                if item == blockNumber + 1:
                    self.tNumberBox.morphErrors.remove(item)
                    nextBlock = text.findBlockByNumber(blockNumber + 1)
                    cursor = QtGui.QTextCursor(block)
                    cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                    cursor.setCharFormat(format)
                    cursor = QtGui.QTextCursor(nextBlock)
                    cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                    cursor.setCharFormat(format)
                    if self.tNumberBox.morphErrorIndex:
                        self.tNumberBox.morphErrorIndex -= 1
                    errorNumber = len(self.tNumberBox.morphErrors)
                    if errorNumber == 0:
                        self.morphErrorNumber.setText('')
                        self.tMorphsValidBtn.setChecked(1)
                        self.morphErrorPrev.setEnabled(0)
                        self.morphErrorNext.setEnabled(0)
                    elif errorNumber == 1:
                        self.morphErrorNumber.setText('1 morph error')
                    else:
                        self.morphErrorNumber.setText('%d morph errors' % errorNumber)
                    break
                elif item == blockNumber:
                    self.tNumberBox.morphErrors.remove(item)
                    prevBlock = text.findBlockByNumber(blockNumber - 1)
                    cursor = QtGui.QTextCursor(prevBlock)
                    cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                    cursor.setCharFormat(format)
                    cursor = QtGui.QTextCursor(block)
                    cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                    cursor.setCharFormat(format)
                    if self.tNumberBox.morphErrorIndex:
                        self.tNumberBox.morphErrorIndex -= 1
                    errorNumber = len(self.tNumberBox.morphErrors)
                    if errorNumber == 0:
                        self.morphErrorNumber.setText('')
                        self.tMorphsValidBtn.setChecked(1)
                        self.morphErrorPrev.setEnabled(0)
                        self.morphErrorNext.setEnabled(0)
                    elif errorNumber == 1:
                        self.morphErrorNumber.setText('1 morph error')
                    else:
                        self.morphErrorNumber.setText('%d morph errors' % errorNumber)
                    break

    def cleanText(self, text):
        """
        corrects for common punctuation errors in input
        """
        text = text.replace('-', '–')
        text = text.strip()
        text = text.replace('\t\n', '\n')
        return text

    def alignText(self):
        """
        aligns lines 2 and 3 of four-line glosses throughout the text
        """
        text = self.portal.document()
        cursor = self.portal.textCursor()
        block = text.begin()
        prevBlock = -1
        while block.isValid():
            if not '\t' in block.text():
                block = block.next()
                continue
            blockNumber = block.blockNumber()
            pLine = block.text()
            aLine = block.next().text()
            pLine, aLine = self.align(pLine, aLine, blockNumber)
            if pLine is None:
                break
            if blockNumber == prevBlock:
                breakbox = QtWidgets.QMessageBox()
                breakbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                breakbox.setText("Format Error")
                breakbox.setInformativeText('There is an error in the formatting of this text at line %d. '
                                            'The most likely cause is a tab character somewhere in the line. '
                                            'Please replace it with a space.' % blockNumber)
                breakbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                breakbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                breakbox.exec()
                text = self.portal.document()
                block = text.findBlockByNumber(blockNumber)
                position = text.documentLayout().blockBoundingRect(block).topLeft()
                self.portal.verticalScrollBar().setValue(position.y() - 220)
                self.portal.horizontalScrollBar().setValue(0)
                break
            cursor.setPosition(block.position())
            cursor.select(QtGui.QTextCursor.SelectionType.BlockUnderCursor)
            cursor.insertText('\n' + pLine)
            block = block.next()
            cursor.setPosition(block.position())
            cursor.select(QtGui.QTextCursor.SelectionType.BlockUnderCursor)
            cursor.insertText('\n' + aLine)
            block = block.next()
            prevBlock = blockNumber

    def align(self, pLine, aLine, blockNumber):
        """
        adds spaces as needed to align glosses.
        called by alignText() for each pair of lines
        """
        pLineList = pLine.split('\t')
        aLineList = aLine.split('\t')
        for i, item in enumerate(pLineList):
            spacer = ''
            try:
                if len(pLineList[i]) > len(aLineList[i]):
                    for j in range(len(pLineList[i]) - len(aLineList[i])):
                        spacer += ' '
                    aLineList[i] += spacer
                else:
                    for j in range(len(aLineList[i]) - len(pLineList[i])):
                        spacer += ' '
                    pLineList[i] += spacer
            except IndexError:
                breakbox = QtWidgets.QMessageBox()
                breakbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                breakbox.setText("Format Error")
                breakbox.setInformativeText(
                    'There is an error in the formatting of this text at line %d.' % blockNumber)
                breakbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                breakbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                breakbox.exec()
                text = self.portal.document()
                block = text.findBlockByNumber(blockNumber)
                position = text.documentLayout().blockBoundingRect(block).topLeft()
                self.portal.verticalScrollBar().setValue(position.y() - 220)
                self.portal.horizontalScrollBar().setValue(0)
                return None, None
        newPLine = '\t'.join(pLineList)
        newALine = '\t'.join(aLineList)
        return newPLine, newALine

    def tryParse(self):
        """
        trial parsing of new texts, results shown in portal
        """
        if len(self.portal.toPlainText()) == 0:
            return
        if len(dataIndex.fldbk.iIndex.toPlainText()) == 0:
            parse = autoparsing.askToBuildIndex()
            if parse is False:
                return
        if self.validateNewText() != 'okay':
            QtWidgets.QApplication.beep()
            return
        text = self.portal.document()
        block = text.begin()
        counter = 0
        blockNumber = 0
        parsedText = ''
        for i in range(0, text.blockCount()):
            timeCode = None
            spokenBy = None
            blockNumber += 1
            if len(block.text()) <= 1:
                block = block.next()
                continue
            counter += 1
            if len(block.next().text()) <= 1:
                if counter == 4:
                    # if this is a 4-line block
                    textLine = text.findBlockByNumber(blockNumber - 4).text()
                    textLine, speaker, tCode, eTime = update.fixGlosses(textLine)
                    glossLine = text.findBlockByNumber(blockNumber - 1).text()
                    glossLine, spokenBy, timeCode, endTime = update.fixGlosses(glossLine)
                    if speaker is not None and spokenBy is None:
                        spokenBy = speaker
                    if tCode is not None and timeCode is None:
                        timeCode = tCode
                    if eTime is not None and endTime is None:
                        endTime = tCode
                    parseLine = text.findBlockByNumber(blockNumber - 3).text()
                    parseLine = self.cleanText(parseLine)
                    ilegLine = text.findBlockByNumber(blockNumber - 2).text()
                    ilegLine = self.cleanText(ilegLine)
                    if '[—]' in ilegLine:
                        wordList = parseLine.split(' ')
                        ilegList = ilegLine.split(' ')
                        for i, item in enumerate(ilegList):
                            if item == '[—]':
                                newMorphs, newAnalysis = autoparsing.autoParse(wordList[i], textLine, glossLine)
                                if newMorphs is not None:
                                    ilegList[i] = newAnalysis
                                    wordList[i] = newMorphs
                        parseLine = ' '.join(wordList)
                        ilegLine = ' '.join(ilegList)
                elif counter == 2:
                    # if this is a 2-line block without an interlinear gloss
                    textLine, glossLine, parseLine, ilegLine, timeCode, spokenBy, endTime = self.twoLineTextHandler(
                        text, blockNumber, True)
                if timeCode is not None:
                    timeCode = ' [' + timeCode
                    if endTime is not None:
                        timeCode += ' – ' + endTime + ']'
                    else:
                        timeCode += ']'
                else:
                    timeCode = ''
                if spokenBy is not None:
                    spokenBy += ': '
                else:
                    spokenBy = ''
                parsedText += spokenBy + textLine + '\n' + parseLine + '\n' + ilegLine + '\n' + glossLine + timeCode + '\n\n'
                block = block.next().next()
                counter = 0
                blockNumber += 1
            else:
                block = block.next()
        newText = parsedText[:-1]
        self.portal.setText(newText)

    def twoLineTextHandler(self, text, blockNumber, parse):
        """
        breaks up a two-line text into chunks either for 
        creating eg cards or for trial parsing
        """
        textLine = text.findBlockByNumber(blockNumber - 2).text()
        textLine, speaker, tCode, eTime = update.fixGlosses(textLine)
        glossLine = text.findBlockByNumber(blockNumber - 1).text()
        glossLine, spokenBy, timeCode, endTime = update.fixGlosses(glossLine)
        if speaker is not None and spokenBy is None:
            spokenBy = speaker
        if tCode is not None and timeCode is None:
            timeCode = tCode
        if eTime is not None and endTime is None:
            endTime = tCode
        parseLine = ''
        ilegLine = ''
        if parse is True:
            QtWidgets.QApplication.restoreOverrideCursor()
            wordList = autoparsing.cleanLine(textLine)
            for i, word in enumerate(wordList):
                newMorphs, newAnalysis = autoparsing.autoParse(word, textLine, glossLine)
                if newMorphs is None:
                    newMorphs = word
                    newAnalysis = "[—]"
                if parseLine == '':
                    parseLine = newMorphs
                    ilegLine = newAnalysis
                else:
                    parseLine += ' ' + newMorphs
                    ilegLine += ' ' + newAnalysis
        return textLine, glossLine, parseLine, ilegLine, timeCode, spokenBy, endTime

    def newBlock(self, count):
        """
        adjusts line numbers, etc., when blocks are added
        """
        oldCount = self.tNumberBox.editorBlockCount
        if oldCount == count:
            return
        self.tNumberBox.editorBlockCount = count
        diff = count - oldCount
        errorFixed = None
        try:
            errorNumber = len(self.tNumberBox.lineErrors)
            if self.tNumberBox.lineErrorIndex is None:
                targetLine = self.tNumberBox.lineErrors[0]
            else:
                targetLine = self.tNumberBox.lineErrors[self.tNumberBox.lineErrorIndex]
            if count > oldCount:
                boundaryBlock = self.portal.document().findBlockByNumber(targetLine - 4)
            elif count < oldCount:
                adjustment = diff + -5
                boundaryBlock = self.portal.document().findBlockByNumber(targetLine + adjustment)
            if len(boundaryBlock.text()) <= 1:
                errorFixed = 1
            if errorFixed:
                if self.tNumberBox.lineErrorIndex is None:
                    self.tNumberBox.lineErrors.pop(0)
                else:
                    self.tNumberBox.lineErrors.pop(self.tNumberBox.lineErrorIndex)
                    self.tNumberBox.lineErrorIndex -= 1
                if count > oldCount and errorNumber != 0:
                    block = self.portal.document().findBlockByNumber(targetLine)
                    cursor = QtGui.QTextCursor(block)
                    cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                    charformat = QtGui.QTextCharFormat()
                    charformat.setBackground(QtCore.Qt.GlobalColor.white)
                    cursor.setCharFormat(charformat)
                elif count < oldCount and errorNumber != 0:
                    adjustment = diff - 1
                    block = self.portal.document().findBlockByNumber(targetLine + adjustment)
                    cursor = QtGui.QTextCursor(block)
                    cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                    charformat = QtGui.QTextCharFormat()
                    charformat.setBackground(QtCore.Qt.GlobalColor.white)
                    cursor.setCharFormat(charformat)
        except IndexError:
            pass
        targetLine = self.portal.textCursor().blockNumber()
        try:
            if len(self.tNumberBox.lineErrors) != 0:
                for i, item in enumerate(self.tNumberBox.lineErrors):
                    if item > targetLine:
                        item += diff
                        self.tNumberBox.lineErrors[i] = item
                if len(self.tNumberBox.lineErrors) == 1:
                    self.lineErrorNumber.setText('1 line error')
                else:
                    self.lineErrorNumber.setText('%d line errors' % len(self.tNumberBox.lineErrors))
            else:
                if self.tNumberBox.lineErrorIndex is not None:
                    self.tLinesValidBtn.setChecked(1)
                    self.lineErrorPrev.setEnabled(0)
                    self.lineErrorNext.setEnabled(0)
                    self.lineErrorNumber.setText('')
        except TypeError:
            pass
        try:
            if len(self.tNumberBox.wordErrors) != 0:
                for i, item in enumerate(self.tNumberBox.wordErrors):
                    if item > targetLine:
                        item += diff
                        self.tNumberBox.wordErrors[i] = item
        except TypeError:
            pass
        try:
            if len(self.tNumberBox.morphErrors) != 0:
                for i, item in enumerate(self.tNumberBox.morphErrors):
                    if item > targetLine:
                        item += diff
                        self.tNumberBox.morphErrors[i] = item
        except TypeError:
            pass

    def validateNewText(self):
        """
        checks for mismatched lines, words, and morphs
        """
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        self.tLinesValidBtn.setChecked(0)
        self.tWordsValidBtn.setChecked(0)
        self.tMorphsValidBtn.setChecked(0)
        self.lineErrorPrev.setEnabled(0)
        self.lineErrorNext.setEnabled(0)
        self.wordErrorPrev.setEnabled(0)
        self.wordErrorNext.setEnabled(0)
        self.morphErrorPrev.setEnabled(0)
        self.morphErrorNext.setEnabled(0)
        text = self.portal.document()
        block = text.begin()
        counter = 0
        textLine = ''
        formatted = ''
        blockNumber = 0
        self.tNumberBox.lineErrors = []
        self.tNumberBox.wordErrors = []
        self.tNumberBox.morphErrors = []
        self.tNumberBox.lineErrorIndex = None
        self.tNumberBox.wordErrorIndex = None
        self.tNumberBox.morphErrorIndex = None
        self.lineErrorNumber.setText('')
        self.wordErrorNumber.setText('')
        self.morphErrorNumber.setText('')
        for i in range(0, text.blockCount()):
            blockNumber += 1
            if len(block.text()) == 1 or len(block.text()) == 0:
                block = block.next()
                continue
            textLine += block.text() + "\n"
            counter += 1
            if len(block.next().text()) == 1 or len(block.next().text()) == 0:
                if counter == 4:
                    parseLine = text.findBlockByNumber(blockNumber - 3).text()
                    parseLine = self.cleanText(parseLine)
                    ilegLine = text.findBlockByNumber(blockNumber - 2).text()
                    ilegLine = self.cleanText(ilegLine)
                    self.checkIleg(parseLine, ilegLine, blockNumber)
                elif counter == 2:
                    pass
                elif counter == 1:
                    pass
                else:
                    self.tNumberBox.lineErrors.append(blockNumber)
                formatted += textLine + "\n"
                textLine = ""
                block = block.next().next()
                counter = 0
                blockNumber += 1
            else:
                block = block.next()
        formatted = self.cleanText(formatted)
        self.portal.setText(formatted)
        text = self.portal.document()
        text.blockCountChanged.connect(self.newBlock)
        block = text.begin()
        cursor = QtGui.QTextCursor(block)
        cursor.select(QtGui.QTextCursor.SelectionType.Document)
        charformat = QtGui.QTextCharFormat()
        charformat.setBackground(QtCore.Qt.GlobalColor.white)
        cursor.setCharFormat(charformat)
        okayToGo = 1
        if len(self.tNumberBox.lineErrors) == 0:
            self.tLinesValidBtn.setChecked(1)
        else:
            okayToGo = 0
            self.lineErrorPrev.setEnabled(1)
            self.lineErrorNext.setEnabled(1)
            if len(self.tNumberBox.lineErrors) == 1:
                self.lineErrorNumber.setText('1 line error')
            else:
                self.lineErrorNumber.setText('%d line errors' % len(self.tNumberBox.lineErrors))
            for line in self.tNumberBox.lineErrors:
                text = self.portal.document()
                block = text.findBlockByNumber(line - 1)
                cursor = QtGui.QTextCursor(block)
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                charformat = QtGui.QTextCharFormat()
                charformat.setBackground(QtCore.Qt.GlobalColor.yellow)
                cursor.setCharFormat(charformat)
        if len(self.tNumberBox.wordErrors) == 0:
            self.tWordsValidBtn.setChecked(1)
        else:
            okayToGo = 0
            self.wordErrorPrev.setEnabled(1)
            self.wordErrorNext.setEnabled(1)
            if len(self.tNumberBox.wordErrors) == 1:
                self.wordErrorNumber.setText('1 word error')
            else:
                self.wordErrorNumber.setText('%d word errors' % len(self.tNumberBox.wordErrors))
            for line in self.tNumberBox.wordErrors:
                text = self.portal.document()
                block = text.findBlockByNumber(line - 1)
                cursor = QtGui.QTextCursor(block)
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                charformat = QtGui.QTextCharFormat()
                charformat.setBackground(QtCore.Qt.GlobalColor.cyan)
                cursor.setCharFormat(charformat)
                block = text.findBlockByNumber(line)
                cursor = QtGui.QTextCursor(block)
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                charformat = QtGui.QTextCharFormat()
                charformat.setBackground(QtCore.Qt.GlobalColor.cyan)
                cursor.setCharFormat(charformat)

        if len(self.tNumberBox.morphErrors) == 0:
            self.tMorphsValidBtn.setChecked(1)
        else:
            okayToGo = 0
            self.morphErrorPrev.setEnabled(1)
            self.morphErrorNext.setEnabled(1)
            if len(self.tNumberBox.morphErrors) == 1:
                self.morphErrorNumber.setText('1 morph error')
            else:
                self.morphErrorNumber.setText('%d morph errors' % len(self.tNumberBox.morphErrors))
            for line in self.tNumberBox.morphErrors:
                text = self.portal.document()
                block = text.findBlockByNumber(line - 1)
                cursor = QtGui.QTextCursor(block)
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                charformat = QtGui.QTextCharFormat()
                charformat.setBackground(QtCore.Qt.GlobalColor.green)
                cursor.setCharFormat(charformat)
                block = text.findBlockByNumber(line)
                cursor = QtGui.QTextCursor(block)
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.KeepAnchor)
                charformat = QtGui.QTextCharFormat()
                charformat.setBackground(QtCore.Qt.GlobalColor.green)
                cursor.setCharFormat(charformat)
        QtWidgets.QApplication.restoreOverrideCursor()
        if len(self.portal.toPlainText()) == 0:
            self.portal.setText('blank text')
        QtWidgets.QApplication.restoreOverrideCursor()
        if okayToGo == 1:
            self.alignTextBtn.setEnabled(1)
            #            self.alignText()
            return 'okay'

    def removeHiliting(self):
        """
        removes all highlighting added by searches and validation
        """
        text = self.portal.document()
        block = text.begin()
        cursor = QtGui.QTextCursor(block)
        cursor.select(QtGui.QTextCursor.SelectionType.Document)
        charformat = QtGui.QTextCharFormat()
        charformat.setBackground(QtCore.Qt.GlobalColor.white)
        cursor.setCharFormat(charformat)
        self.removeHiliteBtn.setEnabled(0)

    """FIND AND REPLACE SCRIPTS"""

    def findItem(self, flag=None, silent=None):
        """
        find item typed in findTerm LineEdit
        """
        if flag is not None:
            direction = 'back'
            flag |= QtGui.QTextDocument.FindFlag.FindCaseSensitively
        else:
            direction = 'forwards'
            flag = QtGui.QTextDocument.FindFlag.FindCaseSensitively
        if len(self.portal.toPlainText()) == 0:
            return
        self.removeHiliting()
        if self.wholeWordBtn.isChecked():
            if flag is None:
                flag = QtGui.QTextDocument.FindFlag.FindWholeWords
            else:
                flag |= QtGui.QTextDocument.FindFlag.FindWholeWords
        if self.portal.find(self.findTerm.text(), flag) is False:
            if direction == 'back':
                self.portal.moveCursor(QtGui.QTextCursor.MoveOperation.End)
            else:
                self.portal.moveCursor(QtGui.QTextCursor.MoveOperation.Start)
            if self.portal.find(self.findTerm.text(), flag) is False and silent is None:
                QtWidgets.QApplication.beep()
            return self.portal.find(self.findTerm.text(), flag)

    def replaceOnce(self, silent=None):
        """
        replaces one instance of the find term with replace term
        """
        if self.portal.textCursor().selection().toPlainText() == self.findTerm.text():
            self.portal.textCursor().insertText(self.replaceTerm.text())
            return
        hit = self.findItem(None, silent)
        if hit is not False:
            self.portal.textCursor().insertText(self.replaceTerm.text())
        return hit

    def replaceFind(self):
        """
        replaces one instance of the find term with replace term and finds
        the next candidate for replacement
        """
        if len(self.portal.textCursor().selection().toPlainText()) == 0:
            self.findItem()
            return
        else:
            self.portal.textCursor().insertText(self.replaceTerm.text())
            self.findItem()

    def replaceAll(self):
        """
        global find and replace
        """
        hit = True
        self.portal.moveCursor(QtGui.QTextCursor.MoveOperation.Start)
        while hit is not False:
            hit = self.replaceOnce('no beep')
            self.portal.moveCursor(QtGui.QTextCursor.MoveOperation.Start)
        self.removeHiliteBtn.setEnabled(0)

    def findAll(self):
        """
        finds and highlights all instances of find term
        """
        self.removeHiliting()
        lookFor = self.findTerm.text()
        cursor = self.portal.textCursor()
        charformat = QtGui.QTextCharFormat()
        charformat.setBackground(QtGui.QBrush(QtGui.QColor("yellow")))
        if self.wholeWordBtn.isChecked():
            lookFor = r'(\s|^)' + lookFor + r'(\s|$)'
        regex = QtCore.QRegularExpression(lookFor)
        pos = 0
        index = QtCore.QRegularExpressionMatch()
        dataset = self.portal.toPlainText()
        index = regex.match(dataset, pos)
        if index.hasMatch():
            self.removeHiliteBtn.setEnabled(1)
            while (index.hasMatch()):
                if self.wholeWordBtn.isChecked():
                    cursor.setPosition(index.capturedStart() + 1)
                else:
                    cursor.setPosition(index.capturedStart())
                cursor.setPosition(index.capturedEnd(), QtGui.QTextCursor.MoveMode.KeepAnchor)
                pos = index.capturedStart() + len(index.captured())
                cursor.mergeCharFormat(charformat)
                index = regex.match(dataset, pos)
        else:
            self.removeHiliteBtn.setEnabled(0)
            QtWidgets.QApplication.beep()

    def importFiles(self, fileType):
        if fileType == 'ELAN file':
            dialog = ElanImporter.ElanImporter(self)
            askFile = dialog.getFilePath()
            if askFile is False:
                return
            else:
                dialog.displayTiers()
            if dialog.exec():
                # get metadata from dialog as list [source, researcher, date, transcriber, title]
                metaData = dialog.getMetadata()
                self.tNewSource.setPlainText(metaData[0])
                self.tNewResearcher.setPlainText(metaData[1])
                self.tNewDate.setPlainText(metaData[2])
                self.tNewTranscriber.setPlainText(metaData[3])
                self.tTitle.setPlainText(metaData[4])
                newText = dialog.importText()
                self.portal.setPlainText(newText)
            self.setWindowState(QtCore.Qt.WindowState.WindowActive)
            self.raise_()

    @pyqtSlot()
    def on_portal_textChanged(self):
        """
        tracks edits in new text field.
        """
        self.editTracker()

    @pyqtSlot()
    def on_tSpliceBtn_released(self):
        """
        joins line pairs that were split to fit on a typeset page, as in
            line
            parse line 1
            interlinear line 1
                parse line 2
                interlinear line 2
            gloss
        """
        if self.portal.textCursor() and len(self.portal.textCursor().selectedText()) != 0:
            cursor = self.portal.textCursor()
            text = self.portal.document()
            try:
                selectionStart = cursor.selectionStart()
                selectionEnd = cursor.selectionEnd()
                cursor.setPosition(selectionStart)
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine, QtGui.QTextCursor.MoveMode.MoveAnchor)
                selectionStart = cursor.position()
                firstBlock = cursor.blockNumber()
                cursor.setPosition(selectionEnd)
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfLine, QtGui.QTextCursor.MoveMode.MoveAnchor)
                selectionEnd = cursor.position()
                lastBlock = cursor.blockNumber()
                cursor.setPosition(selectionStart, QtGui.QTextCursor.MoveMode.MoveAnchor)
                cursor.setPosition(selectionEnd, QtGui.QTextCursor.MoveMode.KeepAnchor)
                if not len(text.findBlockByNumber(firstBlock - 1).text()) <= 1 or not len(
                        text.findBlockByNumber(lastBlock + 1).text()) <= 1:
                    QtWidgets.QApplication.beep()
                    return
                oldBlock = cursor.selectedText()
                lineList = oldBlock.split('\u2029')
                newLine = lineList.pop(0) + '\n'
                glossLine = lineList.pop(-1)
                parseLine = lineList.pop(0).strip()
                ilegLine = lineList.pop(0).strip()
                for i in range(0, len(lineList), 2):
                    parseLine += ' ' + lineList[i].strip()
                    ilegLine += ' ' + lineList[i + 1].strip()
                newLine += parseLine + '\n' + ilegLine + '\n' + glossLine
                charformat = QtGui.QTextCharFormat()
                charformat.setBackground(QtCore.Qt.GlobalColor.white)
                cursor.setCharFormat(charformat)
                # newBlock() called HERE
                cursor.insertText(newLine)
                if self.tNumberBox.lineErrorIndex is not None:
                    if len(self.tNumberBox.lineErrors) == 0:
                        self.lineErrorNumber.setText('')
                        self.tLinesValidBtn.setChecked(1)
                        self.lineErrorPrev.setEnabled(0)
                        self.lineErrorNext.setEnabled(0)
                    elif len(self.tNumberBox.lineErrors) == 1:
                        self.lineErrorNumber.setText('1 line error.')
                    else:
                        self.lineErrorNumber.setText('%d line errors.' % len(self.tNumberBox.lineErrors))
                self.tNumberBox.number_bar.update()
                return
            except IndexError:
                pass
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        text = self.portal.document()
        block = text.begin()
        cursor = QtGui.QTextCursor(block)
        cursor.select(QtGui.QTextCursor.SelectionType.Document)
        charformat = QtGui.QTextCharFormat()
        charformat.setBackground(QtCore.Qt.GlobalColor.white)
        cursor.setCharFormat(charformat)
        counter = 0
        textLines = []
        formatted = ''
        blockNumber = 0
        self.tNumberBox.lineErrors = []
        self.tNumberBox.wordErrors = []
        self.tNumberBox.morphErrors = []
        self.tNumberBox.lineErrorIndex = None
        self.tNumberBox.wordErrorIndex = None
        self.tNumberBox.morphErrorIndex = None
        self.lineErrorNumber.setText('')
        self.wordErrorNumber.setText('')
        self.morphErrorNumber.setText('')
        self.lineErrorPrev.setEnabled(0)
        self.lineErrorNext.setEnabled(0)
        self.wordErrorPrev.setEnabled(0)
        self.wordErrorNext.setEnabled(0)
        self.morphErrorPrev.setEnabled(0)
        self.morphErrorNext.setEnabled(0)
        for i in range(0, text.blockCount()):
            blockNumber += 1
            if len(block.text()) <= 1:
                block = block.next()
                continue
            textLines.append(block.text())
            counter += 1
            if len(block.next().text()) <= 1:
                if counter == 6:
                    parseLine = textLines[1]
                    parsePart2 = textLines.pop(3)
                    parseLine += ' ' + parsePart2
                    parseLine = self.cleanText(parseLine)
                    textLines[1] = parseLine
                    ilegLine = textLines[2]
                    ilegPart2 = textLines.pop(3)
                    ilegLine += ' ' + ilegPart2
                    ilegLine = self.cleanText(ilegLine)
                    textLines[2] = ilegLine

                textLine = ''
                for line in textLines:
                    textLine += line + '\n'
                formatted += textLine + "\n"
                block = block.next().next()
                counter = 0
                blockNumber += 1
                textLines = []
            else:
                block = block.next()
        formatted = formatted.strip()
        self.portal.setText(formatted)
        text.blockCountChanged.connect(self.newBlock)
        self.tNumberBox.number_bar.update()
        QtWidgets.QApplication.restoreOverrideCursor()

    @pyqtSlot()
    def on_tLoadNewTextBtn_released(self):
        """
        loads UTF-8 file into portal field for manual editing
        """
        openFileDialog = QtWidgets.QFileDialog(self)
        filePath = path.dirname(openFileDialog.directory().currentPath())
        fileDir = path.split(filePath)
        if fileDir[1] == 'com.UNTProject.eFieldbook':
            openFileDialog.setDirectory(dataIndex.homePath)
        fname = openFileDialog.getOpenFileName(self, "Open...")
        fname = fname[0]
        if fname:
            loaded = open(fname, 'r', encoding="UTF-8").read()
            pieces = loaded.partition('\n')
            metaData = pieces[0]
            metaDataList = metaData.split(':')
            if metaDataList[0] == 'HEADER' and len(metaDataList) == 6:
                self.tTitle.setPlainText(metaDataList[1])
                self.tNewSource.setPlainText(metaDataList[2])
                self.tNewResearcher.setPlainText(metaDataList[3])
                self.tNewDate.setPlainText(metaDataList[4])
                self.tNewTranscriber.setPlainText(metaDataList[5])
                text = self.cleanText(pieces[2])
            else:
                text = self.cleanText(loaded)
            self.portal.setText(text)
            self.portal.document().blockCountChanged.connect(self.newBlock)
            self.tNumberBox.number_bar.update()
            self.tNumberBox.editorBlockCount = self.portal.document().blockCount()
            self.tLinesValidBtn.setChecked(0)
            self.tWordsValidBtn.setChecked(0)
            self.tMorphsValidBtn.setChecked(0)

    @pyqtSlot()
    def on_tFormatNewTextBtn_released(self):
        """
        makes sure that the text in the portal is formatted correctly
        """
        self.validateNewText()

    @pyqtSlot()
    def on_tClearNewTextBtn_released(self):
        """
        clear fields, etc.
        """
        self.clearNewText()

    @pyqtSlot()
    def on_lineErrorPrev_released(self):
        """
        find prev line error.
        """
        errors = self.tNumberBox
        if errors.lineErrorIndex is None:
            errors.lineErrorIndex = 0
        else:
            errors.lineErrorIndex -= 1
            if errors.lineErrorIndex < 0:
                errors.lineErrorIndex = len(errors.lineErrors) - 1
        try:
            targetLine = errors.lineErrors[errors.lineErrorIndex]
            text = self.portal.document()
            block = text.findBlockByNumber(targetLine)
            position = text.documentLayout().blockBoundingRect(block).topLeft()
            self.portal.verticalScrollBar().setValue(position.y() - 220)
            self.portal.horizontalScrollBar().setValue(0)
            errors.number_bar.update()
        except IndexError:
            pass

    @pyqtSlot()
    def on_lineErrorNext_released(self):
        """
        find next line error.
        """
        errors = self.tNumberBox
        if errors.lineErrorIndex is None:
            errors.lineErrorIndex = 0
        else:
            errors.lineErrorIndex += 1
            if errors.lineErrorIndex > len(errors.lineErrors) - 1:
                errors.lineErrorIndex = 0
        try:
            targetLine = errors.lineErrors[errors.lineErrorIndex]
            text = self.portal.document()
            block = text.findBlockByNumber(targetLine)
            position = text.documentLayout().blockBoundingRect(block).topLeft()
            self.portal.verticalScrollBar().setValue(position.y() - 220)
            self.portal.horizontalScrollBar().setValue(0)
            errors.number_bar.update()
        except IndexError:
            pass

    @pyqtSlot()
    def on_wordErrorPrev_released(self):
        """
        find prev word error.
        """
        errors = self.tNumberBox
        if errors.wordErrorIndex is None:
            errors.wordErrorIndex = 0
        else:
            errors.wordErrorIndex -= 1
            if errors.wordErrorIndex < 0:
                errors.wordErrorIndex = len(errors.wordErrors) - 1
        targetLine = errors.wordErrors[errors.wordErrorIndex]
        text = self.portal.document()
        block = text.findBlockByNumber(targetLine)
        position = text.documentLayout().blockBoundingRect(block).topLeft()
        self.portal.verticalScrollBar().setValue(position.y() - 220)
        self.portal.horizontalScrollBar().setValue(0)
        errors.number_bar.update()

    @pyqtSlot()
    def on_wordErrorNext_released(self):
        """
        find next word error.
        """
        errors = self.tNumberBox
        if errors.wordErrorIndex is None:
            errors.wordErrorIndex = 0
        else:
            errors.wordErrorIndex += 1
            if errors.wordErrorIndex > len(errors.wordErrors) - 1:
                errors.wordErrorIndex = 0
        targetLine = errors.wordErrors[errors.wordErrorIndex]
        text = self.portal.document()
        block = text.findBlockByNumber(targetLine)
        position = text.documentLayout().blockBoundingRect(block).topLeft()
        self.portal.verticalScrollBar().setValue(position.y() - 220)
        self.portal.horizontalScrollBar().setValue(0)
        errors.number_bar.update()

    @pyqtSlot()
    def on_morphErrorPrev_released(self):
        """
        find prev morph error.
        """
        errors = self.tNumberBox
        if errors.morphErrorIndex is None:
            errors.morphErrorIndex = 0
        else:
            errors.morphErrorIndex -= 1
            if errors.morphErrorIndex < 0:
                errors.morphErrorIndex = len(errors.morphErrors) - 1
        targetLine = errors.morphErrors[errors.morphErrorIndex]
        text = self.portal.document()
        block = text.findBlockByNumber(targetLine)
        position = text.documentLayout().blockBoundingRect(block).topLeft()
        self.portal.verticalScrollBar().setValue(position.y() - 220)
        self.portal.horizontalScrollBar().setValue(0)
        errors.number_bar.update()

    @pyqtSlot()
    def on_morphErrorNext_released(self):
        """
        find next morph error.
        """
        errors = self.tNumberBox
        if errors.morphErrorIndex is None:
            errors.morphErrorIndex = 0
        else:
            errors.morphErrorIndex += 1
            if errors.morphErrorIndex > len(errors.morphErrors) - 1:
                errors.morphErrorIndex = 0
        targetLine = errors.morphErrors[errors.morphErrorIndex]
        text = self.portal.document()
        block = text.findBlockByNumber(targetLine)
        position = text.documentLayout().blockBoundingRect(block).topLeft()
        self.portal.verticalScrollBar().setValue(position.y() - 220)
        self.portal.horizontalScrollBar().setValue(0)
        errors.number_bar.update()

    @pyqtSlot()
    def on_cancelNewTextBtn_released(self):
        """
        quit this window without comitting results.
        """
        self.reject()

    @pyqtSlot()
    def on_okayNewTextBtn_released(self):
        """
        close this window and committ results to database. 
        this will divvy up the lines into EX cards.
        """
        if len(self.tTitle.toPlainText()) == 0:
            warning = MissingDataBox.MissingDataBox(self)
            warning.setWarningText('Please give this text a working title.', 'Missing title.')
            warning.exec()
            return
        if len(self.tNewSource.toPlainText()) == 0:
            warning = MissingDataBox.MissingDataBox(self)
            warning.setWarningText('Please provide a source for this text.', 'Missing source.')
            warning.exec()
            return
        if len(self.tNewResearcher.toPlainText()) == 0:
            warning = MissingDataBox.MissingDataBox(self)
            warning.setWarningText('Please provide the name of the researcher.', 'Missing researcher.')
            warning.exec()
            return
        if len(self.tNewDate.toPlainText()) == 0:
            warning = MissingDataBox.MissingDataBox(self)
            warning.setWarningText('Please provide the date this text was recorded.', 'Missing date.')
            warning.exec()
            return
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        validate = self.validateNewText()
        if validate == 'okay':
            try:
                del dataIndex.root.attrib["noText"]
            except AttributeError:
                pass
            except KeyError:
                pass
            textNode = dataIndex.textDict[dataIndex.currentCard]
            if textNode.find('Ln') is None:
                noText = 1
            else:
                noText = None
            if noText:
                newTextID = "TX001"
                newTextNode = dataIndex.root.find('Text[@TextID="TX001"]')
                self.tTextNav.model().removeRow(0)
                title = newTextNode.find("Title")
                newTextNode.remove(title)
            else:
                newTextID = idGenerator.generateID('TX', dataIndex.textDict)
                newTextNode = etree.Element('Text', attrib={'TextID': newTextID})
                k = dataIndex.root.find('Dset')
                d = list(dataIndex.root).index(k)
                dataIndex.root.insert(d, newTextNode)
            newTextNode.set('Rschr', self.tNewResearcher.toPlainText())
            newTextNode.set('Spkr', self.tNewSource.toPlainText())
            newTextNode.set('Date', self.tNewDate.toPlainText())
            tDate = SessionDate.dateFinder()
            newTextNode.set('Update', tDate)
            title = etree.SubElement(newTextNode, "Title")
            dataIndex.textDict[newTextID] = newTextNode
            if len(self.tTitle.toPlainText()) != 0:
                plainTextTitle = self.tTitle.toPlainText()
                html = self.tTitle.toHtml()
                newHtml = formattingHandlers.textStyleHandler(html)
                self.tTitle.setHtml(newHtml)
                title.text = self.tTitle.toPlainText()
                self.tTitle.setHtml(html)
            else:
                title.text = "new text"
            text = self.portal.document()
            block = text.begin()
            counter = 0
            blockNumber = 0
            if self.tNewAutoparseBtn.isChecked():
                if len(dataIndex.fldbk.iIndex.toPlainText()) == 0:
                    parse = autoparsing.askToBuildIndex()
            else:
                parse = False
            for i in range(0, text.blockCount()):
                timeCode = None
                spokenBy = None
                blockNumber += 1
                if len(block.text()) <= 1:
                    block = block.next()
                    continue
                counter += 1
                if len(block.next().text()) <= 1:
                    if counter == 4:
                        # if this is a 4-line block
                        textLine = text.findBlockByNumber(blockNumber - 4).text()
                        textLine, speaker, tCode, eTime = update.fixGlosses(textLine)
                        parseLine = text.findBlockByNumber(blockNumber - 3).text()
                        parseLine = self.cleanText(parseLine)
                        ilegLine = text.findBlockByNumber(blockNumber - 2).text()
                        ilegLine = self.cleanText(ilegLine)
                        glossLine = text.findBlockByNumber(blockNumber - 1).text()
                        glossLine, spokenBy, timeCode, endTime = update.fixGlosses(glossLine)
                        if speaker is not None and spokenBy is None:
                            spokenBy = speaker
                        if tCode is not None and timeCode is None:
                            timeCode = tCode
                        if eTime is not None and endTime is None:
                            endTime = tCode
                    elif counter == 2:
                        # if this is a 2-line block without an interlinear gloss
                        textLine, glossLine, parseLine, ilegLine, timeCode, spokenBy, endTime = self.twoLineTextHandler(
                            text, blockNumber, parse)
                    elif counter == 1:
                        # if this is an unglossed (untranslated) text
                        textLine = text.findBlockByNumber(blockNumber - 1).text()
                        textLine, spokenBy, timeCode, endTime = update.fixGlosses(textLine)
                        parseLine = ''
                        ilegLine = ''
                        glossLine = '—'
                    if self.portal.toPlainText() != 'blank text':
                        try:
                            noEG = dataIndex.root.get("noEG")
                            del dataIndex.root.attrib["noEG"]
                        except AttributeError:
                            noEG = None
                        except KeyError:
                            noEG = None
                        if noEG:
                            newExID = 'EX001'
                            newEx = dataIndex.root.find('Ex[@ExID="EX001"]')
                            newEx.set('Rschr', self.tNewResearcher.toPlainText())
                            newEx.set('Spkr', self.tNewSource.toPlainText())
                            newEx.set('Date', self.tNewDate.toPlainText())
                            newEx.set('Update', tDate)
                            newEx.set('SourceText', newTextID)
                            newLine = newEx.find('Line')
                            newMorph = newEx.find('Mrph')
                            newILEG = newEx.find('ILEG')
                            newL1Gloss = newEx.find('L1Gloss')
                        else:
                            newExID = idGenerator.generateID('EX', dataIndex.exDict)
                            newEx = etree.Element('Ex',
                                                  attrib={'ExID': newExID, 'Rschr': self.tNewResearcher.toPlainText(),
                                                          'Spkr': self.tNewSource.toPlainText(),
                                                          'Date': self.tNewDate.toPlainText(),
                                                          'Update': tDate, 'SourceText': newTextID})
                            newLine = etree.SubElement(newEx, 'Line')
                            newMorph = etree.SubElement(newEx, 'Mrph')
                            newILEG = etree.SubElement(newEx, 'ILEG')
                            newL1Gloss = etree.SubElement(newEx, 'L1Gloss')
                            if self.L2Gloss != 0:
                                newL2Gloss = etree.SubElement(newEx, 'L2Gloss')
                            dataIndex.exDict[newExID] = newEx
                            k = dataIndex.root.find('Speaker')
                            d = list(dataIndex.root).index(k)
                            dataIndex.root.insert(d, newEx)
                        newLine.text = textLine
                        newMorph.text = parseLine
                        newILEG.text = ilegLine
                        if self.L2Gloss != 0:
                            newL2Gloss.text = glossLine
                        else:
                            newL1Gloss.text = glossLine
                        newLineElement = etree.SubElement(newTextNode, "Ln", attrib={'LnRef': newExID})
                        if timeCode is not None:
                            newLineElement.set('Time', timeCode)
                        if endTime is not None:
                            newLineElement.set('EndTime', endTime)
                        if spokenBy is not None:
                            newLineElement.set('SpokenBy', spokenBy)
                            for speaker in dataIndex.root.iter("Speaker"):
                                if speaker.attrib.get('SCode') == spokenBy:
                                    newEx.set('Spkr', spokenBy)
                                    break
                    """TODO: ??use case with gloss in two languages? this would involve changing the setLangBtn to tristate"""
                    block = block.next().next()
                    counter = 0
                    blockNumber += 1
                else:
                    block = block.next()
                    """set new text as current text, add new text to navList, restore card"""
            dataIndex.currentCard = newTextID
            dataIndex.lastText = newTextID
            dataIndex.root.set('LastText', newTextID)
            dataIndex.newText = True
            if dataIndex.currentText is not True:
                item = QtGui.QStandardItem(plainTextTitle)
                item.setData(newTextID, 32)
                dataIndex.fldbk.tTextNav.model().sourceModel().appendRow(item)
                for i in range(0, dataIndex.fldbk.tTextNav.model().rowCount()):
                    if dataIndex.fldbk.tTextNav.model().index(i, 0).data(32) == newTextID:
                        theItem = i
                        break
                dataIndex.fldbk.tTextNav.setCurrentIndex(dataIndex.fldbk.tTextNav.model().index(theItem, 0))
            dataIndex.fldbk.tTextNav.scrollTo(dataIndex.fldbk.tTextNav.currentIndex(),
                                              QtWidgets.QAbstractItemView.ScrollHint.PositionAtCenter)
            self.tTitle.setText(title.text)
            cardLoader.loadTextCard(newTextNode)
            self.clearNewText()
            QtWidgets.QApplication.restoreOverrideCursor()
            self.accept()

    @pyqtSlot()
    def on_parserBtn_released(self):
        """
        Create a trial parse in the main text field.
        """
        self.tryParse()

    @pyqtSlot()
    def on_findPrevBtn_released(self):
        """
        find item in findItem LineEdit going backwards.
        """
        self.findItem(QtGui.QTextDocument.FindBackward)

    @pyqtSlot()
    def on_findNextBtn_released(self):
        """
        find item in findItem LineEdit going forewards.
        """
        self.findItem()

    @pyqtSlot()
    def on_replaceAllBtn_released(self):
        """
        global search and replace.
        """
        self.replaceAll()

    @pyqtSlot()
    def on_saveDraftBtn_released(self):
        """
        Save a copy of a text in process to a plain text file.
        Metadata saved as a sort of "header" at the top.
        """
        title = self.tTitle.toPlainText()
        source = self.tNewSource.toPlainText()
        researcher = self.tNewResearcher.toPlainText()
        tDate = self.tNewDate.toPlainText()
        trans = self.tNewTranscriber.toPlainText()
        metaData = 'HEADER:' + title + ':' + source + ':' + researcher + ':' + tDate + ':' + trans
        saveDoc = metaData + '\n' + self.portal.toPlainText()
        openFileDialog = QtWidgets.QFileDialog(dataIndex.fldbk)
        filePath = path.dirname(openFileDialog.directory().currentPath())
        fileDir = path.split(filePath)
        if fileDir[1] == 'com.UNTProject.eFieldbook':
            openFileDialog.setDirectory(dataIndex.homePath)
        fname = openFileDialog.getSaveFileName(dataIndex.fldbk, "Save As...")[0]
        if fname:
            saveFile = open(fname, "w", encoding="UTF-8")
            saveFile.write(saveDoc)
            saveFile.close()
        self.raise_()

    @pyqtSlot()
    def on_findAllBtn_released(self):
        """
        find and highlight all.
        """
        self.findAll()

    @pyqtSlot()
    def on_findTerm_returnPressed(self):
        """
        find once.
        """
        self.findItem()

    @pyqtSlot()
    def on_replaceBtn_released(self):
        """
        replace once.
        """
        self.replaceOnce()

    @pyqtSlot()
    def on_findReplaceBtn_released(self):
        """
        replace current selection and find next
        """
        self.replaceFind()

    @pyqtSlot(bool)
    def on_activateReplace_toggled(self, checked):
        """
        makes the replace fucntions available.
        
        @param checked DESCRIPTION
        @type bool
        """
        self.toggleActivation(checked)

    @pyqtSlot()
    def on_removeHiliteBtn_released(self):
        """
        remove highlighting.
        """
        self.removeHiliting()

    @pyqtSlot()
    def on_alignTextBtn_released(self):
        """
        align whole text.
        """
        self.alignText()

    @pyqtSlot(str)
    def on_importSelector_activated(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        print('entering on_importSelector_activated')
        self.importFiles(p0)

    @pyqtSlot()
    def on_helpBtn_released(self):
        """
        Slot documentation goes here.
        """
        helpBox = QtWidgets.QMessageBox(self)
        helpBox.setText("<center><b>Entering a new text</b></center>")
        helpBox.setInformativeText("Enter or paste text in the field or load a new text in "
                                   "2- or 4-line format by clicking “Open”. This window "
                                   "can validate the text format and glossing, and "
                                   "provides rudimentary editing and parsing tools. "
                                   "It is good for making global speling changes, but "
                                   "it is better to work on new analyses in the Examples "
                                   "tab, after committing the validated text by pressing "
                                   "“Okay”. Transcription files in some formats can be "
                                   "imported automatically using the “Import file:” pulldown "
                                   "menu. Time codes can be entered following the gloss, in "
                                   "“[MM:SS(.SS)]” format. Indicate change of speaker by "
                                   "adding a speaker code of 1–3 characters followed by a "
                                   "colon and a space or tab before the translation.")
        helpBox.exec()

    @pyqtSlot(int)
    def on_tSetLangBtn_stateChanged(self, p0):
        """
        allows user to set up text glossed in the secondary langugge
        
        @param p0 DESCRIPTION
        @type int (0 = unchecked, 2 = checked)
        """
        self.L2Gloss = p0


class ExampleManager(AnalysisManager):

    def __init__(self, parent=None):
        """
        provides tools for adding multiple examples not necessarily in a text
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(AnalysisManager, self).__init__(parent)
        self.setupUi(self)
        self.setModal(0)
        self.tTitle.deleteLater()
        self.tPortalBox.setGeometry(8, 16, 893, 564)
        self.controlBox.setGeometry(0, 514, 893, 48)
        self.portal.setGeometry(40, 8, 875, 507)
        self.tNumberBox = NumberedLineEdit.TextNumberWidget(self.tPortalBox, self.portal)
        self.tNumberBox.setGeometry(8, 8, 855, 494)
        self.tNumberBox.setVisible(1)
        self.tNewTranscriber.deleteLater()
        self.tLabelTranscriber.deleteLater()
        self.tNewMetadataBox.setGeometry(913, -1, 148, 103)
        self.replaceBtn.setEnabled(0)
        self.findReplaceBtn.setEnabled(0)
        self.replaceAllBtn.setEnabled(0)
        self.replaceTerm.setEnabled(0)
        self.rpcLabel.setStyleSheet('color: gray;')
        self.removeHiliteBtn.setEnabled(0)

    def clearNewExamples(self):
        self.portal.clear()
        self.tNumberBox.number_bar.update()
        self.tNewSource.clear()
        self.tNewResearcher.clear()
        self.tNewDate.clear()
        self.tNewUpdated.clear()
        self.lineErrorNumber.setText('')
        self.wordErrorNumber.setText('')
        self.morphErrorNumber.setText('')
        self.tLinesValidBtn.setChecked(0)
        self.tWordsValidBtn.setChecked(0)
        self.tMorphsValidBtn.setChecked(0)

    @pyqtSlot()
    def on_saveDraftBtn_released(self):
        """
        Save a copy of a set of examples in process to a plain text file.
        Metadata saved as a sort of "header" at the top.
        """
        source = self.tNewSource.toPlainText()
        researcher = self.tNewResearcher.toPlainText()
        tDate = self.tNewDate.toPlainText()
        metaData = 'HEADER:' + source + ':' + researcher + ':' + tDate
        saveDoc = metaData + '\n' + self.portal.toPlainText()
        openFileDialog = QtWidgets.QFileDialog(dataIndex.fldbk)
        filePath = path.dirname(openFileDialog.directory().currentPath())
        fileDir = path.split(filePath)
        if fileDir[1] == 'com.UNTProject.eFieldbook':
            openFileDialog.setDirectory(dataIndex.homePath)
        fname = openFileDialog.getSaveFileName(dataIndex.fldbk, "Save As...")[0]
        if fname:
            saveFile = open(fname, "w", encoding="UTF-8")
            saveFile.write(saveDoc)
            saveFile.close()
        self.raise_()

    @pyqtSlot()
    def on_tLoadNewTextBtn_released(self):
        """
        loads UTF-8 file into portal field for manual editing
        """
        openFileDialog = QtWidgets.QFileDialog(self)
        filePath = path.dirname(openFileDialog.directory().currentPath())
        fileDir = path.split(filePath)
        if fileDir[1] == 'com.UNTProject.eFieldbook':
            openFileDialog.setDirectory(dataIndex.homePath)
        fname = openFileDialog.getOpenFileName(self, "Open...")
        fname = fname[0]
        if fname:
            loaded = open(fname, 'r', encoding="UTF-8").read()
            pieces = loaded.partition('\n')
            metaData = pieces[0]
            metaDataList = metaData.split(':')
            if metaDataList[0] == 'HEADER' and len(metaDataList) == 4:
                self.tNewSource.setPlainText(metaDataList[1])
                self.tNewResearcher.setPlainText(metaDataList[2])
                self.tNewDate.setPlainText(metaDataList[3])
                text = self.cleanText(pieces[2])
            else:
                text = self.cleanText(loaded)
            self.portal.setText(text)
            self.portal.document().blockCountChanged.connect(self.newBlock)
            self.tNumberBox.number_bar.update()
            self.tNumberBox.editorBlockCount = self.portal.document().blockCount()
            self.tLinesValidBtn.setChecked(0)
            self.tWordsValidBtn.setChecked(0)
            self.tMorphsValidBtn.setChecked(0)

    @pyqtSlot()
    def on_okayNewTextBtn_released(self):
        """
        Slot documentation goes here.
        """
        if len(self.tNewSource.toPlainText()) == 0:
            warning = MissingDataBox.MissingDataBox(self)
            warning.setWarningText('Please provide a source for these examples.', 'Missing source.')
            warning.exec()
            return
        if len(self.tNewResearcher.toPlainText()) == 0:
            warning = MissingDataBox.MissingDataBox(self)
            warning.setWarningText('Please provide the name of the researcher.', 'Missing researcher.')
            warning.exec()
            return
        if len(self.tNewDate.toPlainText()) == 0:
            warning = MissingDataBox.MissingDataBox(self)
            warning.setWarningText('Please provide the date these examples were collected.', 'Missing date.')
            warning.exec()
            return
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        validate = self.validateNewText()
        # this will be differen, starting here
        if validate == 'okay':
            tDate = SessionDate.dateFinder()
            text = self.portal.document()
            block = text.begin()
            counter = 0
            blockNumber = 0
            if self.tNewAutoparseBtn.isChecked():
                if len(dataIndex.fldbk.iIndex.toPlainText()) == 0:
                    parse = autoparsing.askToBuildIndex()
            else:
                parse = False
            for i in range(0, text.blockCount()):
                timeCode = None
                blockNumber += 1
                if len(block.text()) <= 1:
                    block = block.next()
                    continue
                counter += 1
                if len(block.next().text()) <= 1:
                    if counter == 4:
                        # if this is a 4-line block
                        textLine = text.findBlockByNumber(blockNumber - 4).text()
                        textLine, speaker, tCode, eTime = update.fixGlosses(textLine)
                        parseLine = text.findBlockByNumber(blockNumber - 3).text()
                        parseLine = self.cleanText(parseLine)
                        ilegLine = text.findBlockByNumber(blockNumber - 2).text()
                        ilegLine = self.cleanText(ilegLine)
                        glossLine = text.findBlockByNumber(blockNumber - 1).text()
                        glossLine, spokenBy, timeCode, endTime = update.fixGlosses(glossLine)
                        if speaker is not None and spokenBy is None:
                            spokenBy = speaker
                        if tCode is not None and timeCode is None:
                            timeCode = tCode
                        if eTime is not None and endTime is None:
                            endTime = tCode
                    elif counter == 2:
                        # if this is a 2-line block without an interlinear gloss
                        textLine, glossLine, parseLine, ilegLine, timeCode, spokenBy = self.twoLineTextHandler(text,
                                                                                                               blockNumber,
                                                                                                               parse)
                    elif counter == 1:
                        # if this is an unglossed (untranslated) text
                        textLine = text.findBlockByNumber(blockNumber - 1).text()
                        textLine, spokenBy, timeCode, endTime = update.fixGlosses(textLine)
                        parseLine = ''
                        ilegLine = ''
                        glossLine = '—'
                    try:
                        noEG = dataIndex.root.get("noEG")
                        del dataIndex.root.attrib["noEG"]
                    except AttributeError:
                        noEG = None
                    except KeyError:
                        noEG = None
                    if noEG:
                        newExID = 'EX001'
                        newEx = dataIndex.root.find('Ex[@ExID="EX001"]')
                        newEx.set('Rschr', self.tNewResearcher.toPlainText())
                        newEx.set('Spkr', self.tNewSource.toPlainText())
                        newEx.set('Date', self.tNewDate.toPlainText())
                        newEx.set('Update', tDate)
                        newLine = newEx.find('Line')
                        newMorph = newEx.find('Mrph')
                        newILEG = newEx.find('ILEG')
                        newL1Gloss = newEx.find('L1Gloss')
                    else:
                        newExID = idGenerator.generateID('EX', dataIndex.exDict)
                        newEx = etree.Element('Ex', attrib={'ExID': newExID, 'Rschr': self.tNewResearcher.toPlainText(),
                                                            'Spkr': self.tNewSource.toPlainText(),
                                                            'Date': self.tNewDate.toPlainText(),
                                                            'Update': tDate})
                        #                        if timeCode is not None:
                        #                            newEx.set('Time', timeCode)
                        newLine = etree.SubElement(newEx, 'Line')
                        newMorph = etree.SubElement(newEx, 'Mrph')
                        newILEG = etree.SubElement(newEx, 'ILEG')
                        newL1Gloss = etree.SubElement(newEx, 'L1Gloss')
                        dataIndex.exDict[newExID] = newEx
                        k = dataIndex.root.find('Speaker')
                        d = list(dataIndex.root).index(k)
                        dataIndex.root.insert(d, newEx)
                        newLine.text = textLine
                        newMorph.text = parseLine
                        newILEG.text = ilegLine
                        newL1Gloss.text = glossLine
                    # TODO: ??use case with gloss in two languages?
                    block = block.next().next()
                    counter = 0
                    blockNumber += 1
                else:
                    block = block.next()
            self.clearNewExamples()
            cardLoader.loadExCard(newEx)
            QtWidgets.QApplication.restoreOverrideCursor()
            self.accept()

    @pyqtSlot()
    def on_tClearNewTextBtn_released(self):
        """
        clear fields, etc.
        """
        self.clearNewExamples()
