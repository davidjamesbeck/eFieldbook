from PyQt6 import QtWidgets, QtCore
from ELFB import dataIndex, idGenerator, cardLoader, textTable, searchClasses, egOnlyBtns, indexOnlyBtns, update, \
    codeExtractor, autoparsing
from xml.etree import ElementTree as etree
from ELFB.palettes import SessionDate
from ELFB.palettes import LineSplitter, AnalysisManager, AddTextLine

"""buttons on text cards """


def enterNewText(fldbk):
    textManager = AnalysisManager.AnalysisManager(fldbk)
    textManager.setWindowTitle('New Text')
    textManager.show()


def tryAfter(thisText, lineNo):
    """
    seeks a line subsequent to the insertion that has been parsed to an EX card.
    returns "False" if there is none
    """
    a = 1
    try:
        while thisText[lineNo + a].attrib.get('LnRef') is None:
            a += 1
        return a
    except IndexError:
        return False


def tryBefore(thisText, lineNo):
    """
    seeks a line previous to the insertion that has been parsed to an EX card.
    returns "False" if there is none
    """
    a = 1
    try:
        while thisText[lineNo - a].attrib.get('LnRef') is None:
            a += 1
        if lineNo - a < 0:
            return False
        else:
            return a
    except IndexError:
        return False


def tAnalyzeLine(fldbk):
    """take user to the example card for parsing/editing"""
    if dataIndex.currentTextTable is not None:
        ExNode = dataIndex.currentTextTable.verticalHeaderItem(0).data(35)
        if ExNode is None:
            thisText = dataIndex.textDict[dataIndex.currentCard]
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            msgbox.setText("Parse line?")
            msgbox.setInformativeText("This line was previously treated as “unparseable”. Parse it now?")
            msgbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
            msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            reply = msgbox.exec()
            if reply == QtWidgets.QMessageBox.StandardButton.Cancel:
                return
            else:
                lineNode = dataIndex.currentTextTable.verticalHeaderItem(0).data(36)
                text = lineNode.text
                if text is None or len(text) == 0:
                    text = "new line"
                if len(text.split('\n')) == 2:
                    line = text.split('\n')[0]
                    line2 = text.split('\n')[1].strip()
                else:
                    line = text
                    line2 = None
                date = fldbk.tDate.toPlainText()
                spkr = fldbk.tSource.toPlainText()
                rschr = fldbk.tResearcher.toPlainText()
                ExNode = etree.Element('Ex')
                etree.SubElement(ExNode, 'Line')
                etree.SubElement(ExNode, 'Mrph')
                etree.SubElement(ExNode, 'ILEG')
                etree.SubElement(ExNode, 'L1Gloss')
                ExNode.find('Line').text = line
                ExNode.find('L1Gloss').text = line2
                ExID = idGenerator.generateID('Ex', dataIndex.exDict)
                ExNode.set('ExID', ExID)
                ExNode.set('Date', date)
                ExNode.set('Update', date)
                ExNode.set('Spkr', spkr)
                ExNode.set('Rschr', rschr)
                ExNode.set('SourceText', dataIndex.currentCard)
                if lineNode.attrib.get('Time') is not None:
                    ExNode.set('Time', lineNode.attrib.get('Time'))
                    """insert ex nodes into XML and add to dicts"""
                dataIndex.exDict[ExID] = ExNode
                lineNo = list(thisText).index(lineNode)
                if lineNo == 0:
                    """first, make sure this isn't the first line of text"""
                    a = tryAfter(thisText, lineNo)
                    if a is not False:
                        prevID = thisText[lineNo + a].attrib.get('LnRef')
                        k = dataIndex.root.find('Ex[@ExID="%s"]' % prevID)
                        d = list(dataIndex.root).index(k)
                        dataIndex.root.insert(d, ExNode)
                elif thisText[lineNo - 1].attrib.get('LnRef') is not None:
                    """next, check to see if this is the normal case where the previous line has been analyzed """
                    prevID = thisText[lineNo - 1].attrib.get('LnRef')
                    a = True
                    k = dataIndex.root.find('Ex[@ExID="%s"]' % prevID)
                    d = list(dataIndex.root).index(k)
                    dataIndex.root.insert(d + 1, ExNode)
                else:
                    """if the previous line is not parsed, find first previous line that has been parsed"""
                    a = tryBefore(thisText, lineNo)
                    if a is not False:
                        prevID = thisText[lineNo - a].attrib.get('LnRef')
                        k = dataIndex.root.find('Ex[@ExID="%s"]' % prevID)
                        d = list(dataIndex.root).index(k)
                        dataIndex.root.insert(d + 1, ExNode)
                    else:
                        # if no previous lines have been parsed, look for a subsequent line
                        a = tryAfter(thisText, lineNo)
                        if a is not False:
                            prevID = thisText[lineNo + a].attrib.get('LnRef')
                            k = dataIndex.root.find('Ex[@ExID="%s"]' % prevID)
                            d = list(dataIndex.root).index(k)
                            dataIndex.root.insert(d, ExNode)
                if a is False:
                    egList = list(dataIndex.exDict.keys())
                    prevID = egList[-1]
                lineNode.set('LnRef', ExID)
    if len(fldbk.iIndex.toPlainText()) == 0:
        indexOnlyBtns.buildIndex()
    #        if buildIndex is False:
    #            return
    cardLoader.loadExCard(ExNode)
    fldbk.tabWidget.setCurrentIndex(3)
    fldbk.eAnalysis.setColumnCount(1)
    autoparsing.doParse()
    updateText(fldbk, ExNode)


def updateText(fldbk, ExNode):
    lineLabel = fldbk.eLineNumber.toPlainText()
    lineNo = int(lineLabel[5:])
    textWidget = fldbk.textLayout.itemAt(lineNo - 1)
    textTable = textWidget.widget()
    try:
        spokenBy = textTable.verticalHeaderItem(0).data(36).attrib.get('SpokenBy')
    except AttributeError:
        spokenBy = None
    for child in dataIndex.currentText.iter('Ln'):
        if child.attrib.get('LnRef') == ExNode.attrib.get('ExID'):
            lineNode = child  # child.attrib.get('LnRef')
    newTextTable = cardLoader.textTableBuilder(ExNode, lineNo - 1, spokenBy, lineNode)
    #    newTextTable.verticalHeaderItem(0).setData(36, textTable.verticalHeaderItem(0).data(36))
    fldbk.textLayout.replaceWidget(textTable, newTextTable)
    dataIndex.currentTextTable = newTextTable
    textTable.deleteLater()


def tNewLine(fldbk):
    """
    adds a new line to a text immediately following the currently selected line
    """
    if dataIndex.currentTextTable is None:
        return
    update = SessionDate.dateFinder()
    scroll = fldbk.tFullText.verticalScrollBar().value()
    timeCode = None
    spokenBy = None
    newLineDialog = AddTextLine.AddLineDialog()
    if newLineDialog.exec():
        values = newLineDialog.returnValues()
        if len(values[0]) == 0:  # bial if there is no text supplied
            return
    else:
        return
    if values[1] is not None:
        spokenBy, values[1] = codeExtractor.getSpokenBy(values[1])
        if '[' in values[1]:  # check to see if timeCode is contained in the gloss
            timeCode, endTime, values[1] = codeExtractor.getTime(values[1])
    """step one: generate nodes (Ln in both cases, EX if possible)"""
    newLineNode = etree.Element('Ln')
    if spokenBy is not None:
        newLineNode.set('SpokenBy', spokenBy)
    if values[2] is True:  # if unparseable
        if values[1] is None:
            newLineNode.text = values[0]
        else:
            newLineNode.text = values[0] + '\n' + values[1]
        if timeCode is not None:
            newLineNode.set('Time', timeCode)
        if endTime is not None:
            newLineNode.set('EndTime', endTime)
    else:  # if parseable, we need to set up an Ex Node for it
        tDate = fldbk.tDate.toPlainText()
        spkr = fldbk.tSource.toPlainText()
        rschr = fldbk.tResearcher.toPlainText()
        newExNode = etree.Element('Ex')
        etree.SubElement(newExNode, 'Line')
        etree.SubElement(newExNode, 'Mrph')
        etree.SubElement(newExNode, 'ILEG')
        etree.SubElement(newExNode, 'L1Gloss')
        newExNode.find('Line').text = values[0]
        newExNode.find('L1Gloss').text = values[1]
        ExID = idGenerator.generateID('Ex', dataIndex.exDict)
        newExNode.set('ExID', ExID)
        newExNode.set('Date', tDate)
        newExNode.set('Update', update)
        newExNode.set('Spkr', spkr)
        newExNode.set('Rschr', rschr)
        newExNode.set('SourceText', dataIndex.currentCard)
        if timeCode is not None:
            newExNode.set('Time', timeCode)
        """insert ex nodes into XML and add to dicts"""
        dataIndex.exDict[ExID] = newExNode
        prevID = dataIndex.currentTextTable.verticalHeaderItem(0).data(35).attrib.get('ExID')
        k = dataIndex.root.find('Ex[@ExID="%s"]' % prevID)
        d = list(dataIndex.root).index(k)
        dataIndex.root.insert(d + 1, newExNode)
        newLineNode.set('LnRef', ExID)
    """insert Ln node"""
    textRoot = dataIndex.currentText
    textViewIndex = int(dataIndex.currentTextTable.verticalHeaderItem(0).text())
    if textViewIndex == 1:
        msgbox = QtWidgets.QMessageBox()
        msgbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        msgbox.setText("Add line at beginning?")
        msgbox.setInformativeText("Add this line before the first line of the text?")
        msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        reply = msgbox.exec()
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            textRoot.insert(0, newLineNode)
            scroll -= 65
        else:
            textRoot.insert(1, newLineNode)
    else:
        textRoot.insert(textViewIndex + 1, newLineNode)
    """step 5: rebuild tText"""
    cardLoader.addTextWidget(fldbk, dataIndex.currentText)
    fldbk.tUpdated.setPlainText(update)
    dataIndex.unsavedEdit = 1
    dataIndex.currentTextTable = None
    fldbk.tFullText.verticalScrollBar().setValue(scroll + 65)


def tSplitLine(fldbk):
    if dataIndex.currentTextTable is not None and dataIndex.currentTextTable.verticalHeaderItem(0).data(35) is not None:
        oldID = dataIndex.currentTextTable.verticalHeaderItem(0).data(35).attrib.get('ExID')
        tSplitter = LineSplitter.LineSplitter(fldbk)
        tSplitter.fillForm(oldID)
        tSplitter.exec()
        if tSplitter:
            idList = tSplitter.newData(oldID)
        else:
            return
        """add new line to text element"""
        lineList = dataIndex.currentText.findall('Ln')
        for i, line in enumerate(lineList):
            if line.attrib.get('LnRef') == oldID:
                newLine = etree.Element('Ln', {'LnRef': idList[1]})
                dataIndex.currentText.insert(i + 2, newLine)
        """rebuild tText"""
        cardLoader.addTextWidget(fldbk, dataIndex.currentText)


def tRemoveLine(fldbk):
    dataIndex.unsavedEdit = 1
    updated = SessionDate.dateFinder()
    fldbk.tUpdated.setPlainText(updated)
    text = dataIndex.currentText
    """step 1: update text XML (remove line from text)"""
    text.set('Update', updated)
    textElementList = text.findall('Ln')
    try:
        badID = dataIndex.currentTextTable.verticalHeaderItem(0).data(35).attrib.get('ExID')
        for line in textElementList:
            if line.attrib.get('LnRef') == badID:
                text.remove(line)
                break
    except AttributeError:
        badID = None
        index = int(dataIndex.currentTextTable.verticalHeaderItem(0).text()) - 1
        badLine = textElementList[index]
        text.remove(badLine)

    """step 2: rebuild tText"""
    cardLoader.addTextWidget(fldbk, text)
    dataIndex.currentTextTable = None

    """step 3: expunge line from database altogether?"""
    if badID is not None:
        expungeMessage = QtWidgets.QMessageBox()
        expungeMessage.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Cancel | QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        expungeMessage.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        expungeMessage.setText('Expunge line from database?')
        expungeMessage.setInformativeText('This will remove the example and all cross-references permanently.')
        expungeMessage.exec()
        if expungeMessage.result() == QtWidgets.QMessageBox.StandardButton.Yes:
            update.cleanUpIDs(badID)


def switchLanguage(fldbk):
    if dataIndex.glossingLanguage == 'L1Gloss':
        dataIndex.glossingLanguage = 'L2Gloss'
    else:
        dataIndex.glossingLanguage = 'L1Gloss'
    text = dataIndex.textDict[dataIndex.currentCard]
    lineList = text.findall('Ln')
    textWidgetList = fldbk.tFullText.findChildren(QtWidgets.QWidget)
    for item in textWidgetList:
        if item.objectName() == 'tText':
            textWidget = item
    tableList = textWidget.findChildren(textTable.textTable)
    for i, line in enumerate(lineList):
        nodeID = line.attrib.get('LnRef')
        if nodeID is None:
            continue
        node = dataIndex.exDict[nodeID]
        if dataIndex.glossingLanguage == 'L2Gloss':
            entryRow3 = node.findtext('L2Gloss')
        else:
            entryRow3 = node.findtext('L1Gloss')
        if not entryRow3:
            entryRow3 = "[—]"
        entryRow3 = "‘" + entryRow3 + "’"
        if node.attrib.get("SpokenBy") is not None:
            speaker = node.attrib.get("SpokenBy")
            entryRow3 = speaker + ': ' + entryRow3
        if "Time" in node.attrib and len(node.attrib.get("Time")) > 1:
            timeCode = node.attrib.get("Time")
            entryRow3 += ' [' + timeCode + ']'
        if tableList[i].rowCount() > 2:
            tableList[i].item(3, 0).setText(entryRow3)
            tableList[i].resizeColumns()
        else:
            tableList[i].item(1, 0).setText(entryRow3)
    L1 = dataIndex.root.attrib.get('L1Choice')
    L2 = dataIndex.root.attrib.get('L2Choice')
    if dataIndex.glossingLanguage == 'L1Gloss':
        label = L1 + " ➔ " + L2
    else:
        label = L2 + " ➔ " + L1
    if len(label) < 10:
        fldbk.tLanguageBtn.setText(label)


def tAdvancedSearch(fldbk):
    engine = searchClasses.TextSearchEngine(fldbk)
    engine.doSearch()


def clipText(outputLanguage):
    """place text on clipboard"""
    exampleP = ''
    textNode = dataIndex.textDict[dataIndex.currentCard]
    for line in textNode.iter('Ln'):
        nodeRef = line.attrib.get('LnRef')
        node = dataIndex.exDict[nodeRef]
        newP = egOnlyBtns.copyLine(node, outputLanguage)
        exampleP += "\r\r" + newP
    clipboard = QtWidgets.QApplication.clipboard()
    clipping = QtCore.QMimeData()
    clipping.setText(exampleP)
    clipboard.setMimeData(clipping)


def toggleParse(fldbk):
    if fldbk.tNewAutoparseBtn.isChecked():
        if len(fldbk.iIndex.toPlainText()) == 0:
            indexOnlyBtns.buildIndex()
            #            autoparsing.askToBuildIndex()
            fldbk.tabWidget.setCurrentIndex(2)
