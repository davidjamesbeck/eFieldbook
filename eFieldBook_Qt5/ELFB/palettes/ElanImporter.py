# -*- coding: utf-8 -*-

"""
Module implementing import for ELAN files.
"""

from PyQt6.QtCore import pyqtSlot
from PyQt6 import QtWidgets
from xml.etree import ElementTree as etree
import re
from .Ui_ElanImporter import Ui_ElanImporter


class ElanImporter(QtWidgets.QDialog, Ui_ElanImporter):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        super(ElanImporter, self).__init__(parent)
        self.setupUi(self)
        self.tierList = None  # list of ELAN TIERS
        self.text = etree.Element('Text')  # XML tree reflecting embedded structure of ELAN tiers
        self.treeWidgetList = None  # list of widgets created in sourceList tree widget
        self.timeCodes = None  # dictionary of time codes extracted from ELAN file
        self.tierAttribList = None  # list [TIER_ID, PARENT_REF]
        self.root = None  # XML represent of ELAN file
        self.elanAnnotationIdDict = {}  # a dictionary with key ANNOTATION_ID, content XML
        self.path = None  # the path to the working folder where all the pieces are
        self.setWindowTitle('Import ELAN file')
        self.targetList.setRowCount(5)
        self.targetList.setColumnCount(1)
        self.targetList.setVerticalHeaderLabels(['Line', 'Morph', 'ILEG', 'L1 Gloss', 'L2 Gloss'])
        self.targetList.verticalHeader().setFixedWidth(80)
        self.targetList.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.targetList.horizontalHeader().hide()

    def displayTiers(self):
        tree = etree.parse(self.transcript)
        self.root = tree.getroot()
        # get list of tiers
        self.tierList = self.root.findall('TIER')
        itemList = []
        tierNameList = []
        for tier in self.tierList:
            # get information for each tier
            itemList.append([tier.attrib.get('TIER_ID'), tier.attrib.get('PARENT_REF')])
            self.tierAttribList = itemList
            tierNameList.append(tier.attrib.get('TIER_ID'))
        for i, item in enumerate(itemList):
            # find the root
            if item[1] is None:
                rootIndex = i
                break
        primaryTier = itemList.pop(rootIndex)
        # get time codes
        timeOrder = self.root.find('TIME_ORDER')
        self.timeCodes = {}
        for node in timeOrder.iter('TIME_SLOT'):
            if node.attrib.get('TIME_VALUE') is not None:
                timeID = node.attrib.get('TIME_SLOT_ID')
                seconds = int(node.attrib.get('TIME_VALUE')) / 1000
                self.timeCodes[timeID] = str(seconds)
                # start map of ELAN file as tree structure
        topNode = etree.Element(primaryTier[0])
        primaryItem = QtWidgets.QTreeWidgetItem()
        primaryItem.setText(0, primaryTier[0])
        primaryItem.setData(0, 32, 'root')
        # get all instance of tier and add to the appropriate parent nodes
        self.gatherNodes(primaryTier[0])
        self.sourceList.setColumnCount(2)
        self.sourceList.addTopLevelItem(primaryItem)
        self.treeWidgetList = [primaryItem]
        foundList = []
        for item in itemList:
            if item[1] == primaryTier[0]:
                etree.SubElement(topNode, item[0])
                show = self.gatherNodes(item[0], item[1])
                if show is True:
                    # if the method returns False, the annotation is empty
                    secondaryItem = QtWidgets.QTreeWidgetItem(primaryItem)
                    secondaryItem.setText(0, item[0])
                    secondaryItem.setData(0, 32, item[1])
                    self.treeWidgetList.append(secondaryItem)
                foundList.append(item)
            for foundItem in foundList:
                itemList.pop(itemList.index(foundItem))
            foundList = []
        while len(itemList) != 0:
            for item in itemList:
                for node in topNode.iter(item[1]):
                    etree.SubElement(node, item[0])
                    parent = self.findParent(item[1])
                    show = self.gatherNodes(item[0], item[1])
                    if show is True:
                        # if the method returns False, the annotation is empty
                        lowerLevelItem = QtWidgets.QTreeWidgetItem(parent)
                        lowerLevelItem.setText(0, item[0])
                        lowerLevelItem.setData(0, 32, parent.data(0, 32) + '/' + item[1])
                        self.treeWidgetList.append(lowerLevelItem)
                    foundList.append(item)
            for foundItem in foundList:
                itemList.pop(itemList.index(foundItem))
            foundList = []
        self.sourceList.expandAll()

    def getFilePath(self):
        fileDialog = QtWidgets.QFileDialog(self, "Open ELAN trancript ...")
        fileDialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        fileDialog.setOption(QtWidgets.QFileDialog.Option.ReadOnly)
        if fileDialog.exec():
            self.transcript = fileDialog.selectedFiles()[0]
            self.path = fileDialog.directory().absolutePath() + '/'
        else:
            return False

    def findParent(self, text):
        for item in self.treeWidgetList:
            if item.text(0) == text:
                return item

    def gatherNodes(self, child, parent=None):
        # start by creating XML elements of type child named for TIER_ID of ELAN TIER
        elemList = []
        # remove spaces if tier names contain them (spaces not valid in XML names)
        child2 = child.replace(" ", "_")
        if parent is not None:
            parent2 = parent.replace(" ", "_")
        tier = self.root.find('TIER[@TIER_ID="%s"]' % child)
        for node in tier.iter('ANNOTATION'):
            element = etree.Element(child2)
            alignable = list(node)[0]
            annotationid = alignable.attrib.get('ANNOTATION_ID')
            value = alignable.find('ANNOTATION_VALUE')
            contents = value.text
            element.set('ANNOTATION_ID', annotationid)
            self.elanAnnotationIdDict[annotationid] = element
            if alignable.attrib.get('TIME_SLOT_REF1') is not None:
                try:
                    tStart = self.timeCodes[alignable.attrib.get('TIME_SLOT_REF1')]
                    element.set('start', tStart)
                except KeyError:
                    pass
                try:
                    tEnd = self.timeCodes[alignable.attrib.get('TIME_SLOT_REF2')]
                    element.set('end', tEnd)
                except KeyError:
                    pass
            if alignable.attrib.get('ANNOTATION_REF') is not None:
                element.set('ANNOTATION_REF', alignable.attrib.get('ANNOTATION_REF'))
            element.text = contents
            elemList.append(element)
        if elemList == []:
            return False
        if parent is None:
            for i, elem in enumerate(elemList):
                self.text.insert(i, elem)
        elif elemList[0].attrib.get('start') is not None:  # is the tier time-aligned rather than linked
            for upperNode in self.text.iter(parent2):
                i = 0
                try:
                    upperNode.insert(0, elemList.pop(0))
                except IndexError:
                    break
                i += 1
                while elemList[0].attrib.get('start') is None:
                    upperNode.insert(i, elemList.pop(0))
                    try:
                        if elemList[0].attrib.get('start') is not None:
                            if upperNode.attrib.get('start') < elemList[0].attrib.get('start') < upperNode.attrib.get(
                                    'end'):
                                del elemList[0].attrib['start']
                    except IndexError:
                        pass
                    i += 1
                    if len(elemList) == 0:
                        break
        else:  # daughter tiers are linked by id references to parents
            oldUpperNode = None
            for elem in elemList:
                upperNode = self.elanAnnotationIdDict[elem.attrib.get('ANNOTATION_REF')]
                if upperNode != oldUpperNode:
                    oldUpperNode = upperNode
                    i = 0
                else:
                    i += 1
                upperNode.insert(i, elem)
        return True

    def getMetadata(self):
        source = self.newSource.toPlainText()
        researcher = self.newResearcher.toPlainText()
        date = self.newDate.toPlainText()
        transcriber = self.newTranscriber.toPlainText()
        title = self.title.toPlainText()
        return source, researcher, date, transcriber, title

    def importText(self):
        errorList = ''
        newText = ''
        timeCodeList = ''
        if self.targetList.item(0, 0) is None:
            return
        # make a list of the XML elements in targetList you need to capture
        itemList = []
        rowspan = 0
        for i in range(0, self.targetList.rowCount()):
            try:
                label = self.targetList.item(i, 0).text()
                if len(label) != 0:
                    itemList.append(label.replace(' ', '_'))
                    rowspan += 1
            except AttributeError:
                itemList.append(None)
        for primaryTier in self.text.iter(itemList[0]):
            # LINE
            try:
                line = primaryTier.text
            except (TypeError, AttributeError):
                errorList += 'missing line of text at line #%d\n' % i
                line = 'ERROR'

            # MORPHS and their GLOSSES
            morphList = primaryTier.findall('.//%s' % itemList[1])
            glossList = primaryTier.findall('.//%s' % itemList[2])
            partsList = []
            for item in morphList:
                try:
                    # remove leading/ending whitespace, correct for use of spaces instead of annotations
                    text = item.text.strip()
                    text = text.replace(' ', '\t')
                    partsList.append(text)
                except (TypeError, AttributeError):
                    errorList += 'missing morph at line #%d\n' % i
                    partsList.append('ERROR')
            morphLine = ' '.join(partsList)
            partsList = []
            for item in glossList:
                try:
                    # correct for use of spaces instead of annotations
                    text = item.text.strip()
                    text = text.replace(' ', '\t')
                    partsList.append(text)
                except (TypeError, AttributeError):
                    print('?????')
                    errorList += 'missing gloss at line #%d\n' % i
                    partsList.append('ERROR')
            glossLine = ' '.join(partsList)
            partsList = []

            # FREE TRANSLATION
            try:
                translation = primaryTier.find(itemList[3]).text
            except (TypeError, AttributeError):
                # these errors may arise if the gloss depends on the parent of the primary tier
                primaryTierID = primaryTier.attrib.get('ANNOTATION_ID')
                if primaryTierID in self.elanAnnotationIdDict.keys():
                    parentRef = self.elanAnnotationIdDict[primaryTierID].attrib.get('ANNOTATION_REF')
                    parentNode = self.elanAnnotationIdDict[parentRef]
                    translation = parentNode.find(itemList[3]).text
                else:
                    errorList += 'missing translation at line #%d\n' % i
                    translation = 'ERROR'
            translation = self.formatting(translation)

            # L2 TRANSLATION (additional translation in a second language)
            if itemList[4] is not None:
                try:
                    secondaryTrans = primaryTier.find(itemList[4]).text
                except (TypeError, AttributeError):
                    # these errors may arise if the gloss depends on the parent of the primary tier
                    primaryTierID = primaryTier.attrib.get('ANNOTATION_ID')
                    if primaryTierID in self.elanAnnotationIdDict.keys():
                        parentRef = self.elanAnnotationIdDict[primaryTierID].attrib.get('ANNOTATION_REF')
                        parentNode = self.elanAnnotationIdDict[parentRef]
                        secondaryTrans = parentNode.find(itemList[4]).text
                    else:
                        errorList += 'missing second translation tier at line #%d\n' % i
                        secondaryTrans = 'ERROR'
                secondaryTrans = self.formatting(secondaryTrans)
            else:
                secondaryTrans = None
            # build timeCodeList
            i += 1
            annotation = 'a' + str(i)
            timeCodeList += "{ 'annotation': '" + annotation + "', "
            try:
                startCode = primaryTier.attrib.get('start')
                endCode = primaryTier.attrib.get('end')
                timeCodeList += "'start': " + startCode + ", "
                timeCodeList += "'end': " + endCode + " }, "
            except TypeError:
                # this error occurs when the primary tier is not time-aligned
                parentID = primaryTier.attrib.get('ANNOTATION_REF')
                if parentID in self.elanAnnotationIdDict.keys():
                    # this requires that the parent of the primarytier is time-aligned
                    parentRef = self.elanAnnotationIdDict[parentID].attrib.get('ANNOTATION_ID')
                    parentTier = self.elanAnnotationIdDict[parentRef]
                    startCode = parentTier.attrib.get('start')
                    endCode = parentTier.attrib.get('end')
                    timeCodeList += "'start' : " + startCode + ", "
                    timeCodeList += "'end' : " + endCode + " }, "
            if secondaryTrans is None:
                newTextParts = [line, morphLine, glossLine, translation]
            else:
                newTextParts = [line, morphLine, glossLine, translation, secondaryTrans]
            newText += '\n'.join(newTextParts)
            if startCode is None:
                startCode = 'timecode error'
            else:
                # TODO: you might want to gather all the time formatting routines into a parameterizable module for Preferences
                rest, seconds = divmod(float(startCode), 60)
                hours, minutes = divmod(rest, 60)
                if round(hours) != 0:
                    timeCode = str(round(hours)) + ":" + str(round(minutes)) + ":" + str(round(seconds, 2))
                elif round(minutes) != 0:
                    timeCode = str(round(minutes)) + ":" + str(round(seconds, 2))
                else:
                    timeCode = '00:' + str(round(seconds, 2))
            newText += ' [' + timeCode + ']\n\n'
        return newText[:-2]

        # report errors and save to file
        if len(errorList) != 0:
            errorWarning = QtWidgets.QMessageBox(self)
            errorWarning.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            errorWarning.setText('Errors in ELAN file')
            errorWarning.setInformativeText('There are errors in the formatting of the ELAN file.')
            errorWarning.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Save | QtWidgets.QMessageBox.StandardButton.Cancel)
            errorWarning.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Save)
            if errorWarning.exec() == QtWidgets.QMessageBox.StandardButton.Save:
                openFileDialog = QtWidgets.QFileDialog(self)
                fname = openFileDialog.getSaveFileName(self, "Save error file as...", "", "*.txt")[0]
                if fname:
                    saveFile = open(fname, "w", encoding="UTF-8")
                    saveFile.write(errorList)
                    saveFile.close()

    def formatting(self, text):
        # TODO: this script removes final punctuation from texts that have it outside close quotes
        if text is None:
            return ''
        # remove timecodes written in to the glosses in square brackets
        # this is probably not a general necessity, but is needed for my own old texts
        if "[" in text:
            text = self.stripTextTimeCode(text)
        text = text.strip()
        text = text.replace('‘', '')
        try:
            if text[-1] == '‘':
                text = text[:-1]
            if text[-1] == '.':
                text = text[:-1]
            if text[-1] == '?':
                text = text[:-1]
            if text[-1] == '!':
                text = text[:-1]
            if text[-1] == '’':
                text = text[:-1]
        except IndexError:
            # this error should only occur if the string has somehow been reduced to a length of 0
            return ''
        text = text.replace('“', '&ldquo;')
        text = text.replace('”', '&rdquo;')
        return text

    def stripTextTimeCode(self, text):
        regex = '\[(\d*)(:\d\d){1, 2}(.\d\d)?\]'
        m = re.search(regex, text)
        if m is not None:
            text = text[:m.start()].strip()
        return text

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        self.accept()

    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        self.reject()

    @pyqtSlot(QtWidgets.QAbstractButton)
    def on_buttonBox_clicked(self, button):

        if button.text() == "Reset":
            self.targetList.clear()
