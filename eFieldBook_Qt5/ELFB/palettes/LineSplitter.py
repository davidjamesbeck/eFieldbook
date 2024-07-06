# -*- coding: utf-8 -*-

"""
Module implementing LineSplitter.
"""
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog
from ELFB import dataIndex, textTable, idGenerator
from xml.etree import ElementTree as etree
from ELFB.palettes import SessionDate
from .Ui_LineSplitter import Ui_Dialog


class LineSplitter(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        super(LineSplitter, self).__init__(parent)
        self.setupUi(self)
        self.egTable = textTable.textTable(self.egArea)
        self.egTable.setFixedWidth(900)

    def newData(self, oldID):
        self.fldbk = dataIndex.fldbk
        line1 = self.firstLine.toPlainText()
        line2 = self.secondLine.toPlainText()
        gloss11 = self.firstL1.toPlainText()
        gloss12 = self.secondL1.toPlainText()
        if len(self.firstL2.toPlainText()) != 0:
            gloss21 = self.firstL2.toPlainText()
            gloss22 = self.secondL2.toPlainText()
        if self.egTable.columnCount() != 0:
            mrphList1 = []
            mrphList2 = []
            ilegList1 = []
            ilegList2 = []
            mrph1 = None
            mrph2 = None
            ileg1 = None
            ileg2 = None
            for i in range(0, self.egTable.currentColumn()):
                mrphList1.append(self.egTable.item(0, i).text())
                ilegList1.append(self.egTable.item(1, i).text())
            for i in range(self.egTable.currentColumn(), self.egTable.columnCount()):
                mrphList2.append(self.egTable.item(0, i).text())
                ilegList2.append(self.egTable.item(1, i).text())
            for item in mrphList1:
                if mrph1 is None:
                    mrph1 = item
                else:
                    mrph1 += ' ' + item
            for item in mrphList2:
                if mrph2 is None:
                    mrph2 = item
                else:
                    mrph2 += ' ' + item
            for item in ilegList1:
                if ileg1 is None:
                    ileg1 = item
                else:
                    ileg1 += ' ' + item
            for item in ilegList2:
                if ileg2 is None:
                    ileg2 = item
                else:
                    ileg2 += ' ' + item
        update = SessionDate.dateFinder()
        tDate = self.fldbk.tDate.toPlainText()
        spkr = self.fldbk.tSource.toPlainText()
        rschr = self.fldbk.tResearcher.toPlainText()
        newID = idGenerator.generateID('Ex', dataIndex.exDict)
        """##revised node"""
        node = dataIndex.exDict[oldID]
        node.find('Line').text = line1
        d = i
        if self.egTable.columnCount() != 0:
            node.find('Mrph').text = mrph1
            node.find('ILEG').text = ileg1
        node.find('L1Gloss').text = gloss11
        node.find('L2Gloss').text = gloss21
        node.set('Update', update)
        k = dataIndex.root.find('Ex[@ExID="%s"]' % oldID)
        d = list(dataIndex.root).index(k) + 1
        """##new node"""
        newNode = etree.Element('Ex')
        etree.SubElement(newNode, 'Line')
        newNode.find('Line').text = line2
        if self.egTable.columnCount() != 0:
            etree.SubElement(newNode, 'Mrph')
            etree.SubElement(newNode, 'ILEG')
            newNode.find('Mrph').text = mrph2
            newNode.find('ILEG').text = ileg2
        etree.SubElement(newNode, 'L1Gloss')
        newNode.find('L1Gloss').text = gloss12
        etree.SubElement(newNode, 'L2Gloss')
        newNode.find('L2Gloss').text = gloss22
        newNode.set('Date', tDate)
        newNode.set('Update', update)
        newNode.set('Spkr', spkr)
        newNode.set('Rschr', rschr)
        newNode.set('ExID', newID)
        if node.attrib.get('SourceText') is not None:
            newNode.set('SourceText', node.attrib.get('SourceText'))
        dataIndex.root.insert(d, newNode)
        dataIndex.exDict[newID] = newNode
        idList = [oldID, newID]
        return idList

    def fillForm(self, exID):
        node = dataIndex.exDict[exID]
        self.firstLine.setHtml(node.find('Line').text)
        self.firstL1.setHtml(node.find('L1Gloss').text)
        if node.find('L2Gloss').text is not None:
            self.firstL2.setHtml(node.find('L2Gloss').text)
        self.egTable.horizontalHeader().show()
        self.egTable.horizontalHeader().setEnabled(1)
        if node.find('Mrph') is not None:
            entryRow1 = node.findtext('Mrph').split(' ')
            entryRow2 = node.findtext('ILEG').split(' ')
            self.egTable.setRowCount(2)
            self.egTable.setColumnCount(len(entryRow1))
            self.egTable.setRowHeight(0, 20)
            self.egTable.setRowHeight(1, 20)
            for i in range(len(entryRow1)):
                parse = entryRow2[i]
                tableCellTop = QtWidgets.QTableWidgetItem(10001)
                tableCellTop.setText(entryRow1[i])
                self.egTable.setItem(0, i, tableCellTop)
                tableCellBottom = QtWidgets.QTableWidgetItem(10001)
                tableCellBottom.setText(parse + " ")
                tableCellBottom.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)
                self.egTable.setItem(1, i, tableCellBottom)
                self.egTable.resizeColumnToContents(i)

    @QtCore.pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        if self.egTable.currentColumn() == -1:
            queryBox = QtWidgets.QMessageBox()
            queryBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            queryBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            queryBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            queryBox.setText('No column selected!')
            queryBox.setInformativeText('Please indicate where the morphological analysis\n'
                                        'should be divided by selecting a column.')
            queryBox.exec()
            return
        self.accept()

    @QtCore.pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        self.reject()
