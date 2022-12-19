from PyQt6 import QtWidgets, QtCore, QtGui
from xml.etree import ElementTree as etree
from random import choice
from os import path
from ELFB import Orthographies, dataIndex, Alphabetizer, dictBuilder, idGenerator, playaudio
from ELFB.palettes import SearchHelp, MediaManager

"""metadata orthography buttons"""


def oClearTransform(fldbk):
    """clear transform field"""
    fldbk.oOrder.clear()
    fldbk.oList.clearSelection()
    fldbk.oDeleteBtn.setEnabled(0)
    fldbk.oUpdateBtn.setEnabled(0)
    fldbk.oClearTransformBtn.setEnabled(0)
    fldbk.oSetBtn.setEnabled(0)
    fldbk.oApplyBtn.setEnabled(0)


def oDelete(fldbk):
    """delete orthography"""
    fldbk.oOrder.clear()
    fldbk.oDiacriticsField.clear()
    badRow = fldbk.oList.currentRow()
    badNode = fldbk.oList.item(badRow, 0).data(36)
    dataIndex.root.remove(badNode)
    if fldbk.oList.item(badRow, 1).text() == 'primary':
        del dataIndex.root.attrib['Orth']
        fldbk.lAutoBtn.setChecked(0)
        dataIndex.root.set('lAuto', 'off')
    fldbk.oDeleteBtn.setEnabled(0)
    fldbk.oUpdateBtn.setEnabled(0)
    fldbk.oClearTransformBtn.setEnabled(0)
    fldbk.oSetBtn.setEnabled(0)
    fldbk.oApplyBtn.setEnabled(0)
    fldbk.oList.removeRow(badRow)
    dataIndex.unsavedEdit = 1


def oSet(fldbk):
    """sets the selected orthography as the primary orthography"""
    row = fldbk.oList.currentRow()
    if dataIndex.root.get('Orth'):
        """if there is already a practical orthography designated"""
        if fldbk.oList.item(row, 0).text() == dataIndex.root.get('Orth'):
            """selecting the orthography listed in the database as the primary
            orthography simply resets the orthography in the mappings fields"""
            selectORow()
            return
        else:
            """otherwise, ask to make sure the user wants to change"""
            breakbox = QtWidgets.QMessageBox()
            breakbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            breakbox.setText("Change primary orthography?")
            breakbox.setInformativeText('This will set the orthography used automatically '
                                        'by the application for various purposes. If switching to '
                                        'a new orthography, only forms you subsequently edit will reflect '
                                        'these changes unless you use the “Update database function”. Proceed?')
            breakbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
            breakbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            breakbox.exec()
            if breakbox.result() == QtWidgets.QMessageBox.StandardButton.Cancel:
                return
    name = fldbk.oList.item(row, 0).text()
    dataIndex.root.set('Orth', name)
    for i in range(0, fldbk.oList.rowCount()):
        if fldbk.oList.item(i, 1).text() == 'primary':
            fldbk.oList.item(i, 1).setText('export')
            break
    fldbk.oList.item(row, 1).setText('primary')
    dataIndex.unsavedEdit = 1


def oApply(fldbk):
    """this will convert orthographies in the database"""
    mapping = fldbk.oOrder.toPlainText()
    pairList = mapping.split(';')
    if fldbk.oTransformBox.currentIndex() == 0:
        """if you set a new pohnetic value for a grapheme"""
        for child in dataIndex.root.iter('Lex'):
            string = child.find('Orth').text
            string = Orthographies.doTransform(string, pairList)
            try:
                child.find('IPA').text = string
            except AttributeError:
                elemList = list(child)
                elemList.reverse()
                for i, item in enumerate(elemList):
                    if item.tag == 'POS':
                        break
                    elif item.tag == 'Orth':
                        break
                i = len(elemList) - i
                child.insert(i, etree.Element('IPA'))
                child.find('IPA').text = string
    else:
        """if you have changed practical orthographies, goes from IPA to new ortho"""
        for child in dataIndex.root.iter('Lex'):
            try:
                string = child.find('IPA').text
                string = Orthographies.doReverseTransform(string, pairList)
                child.find('Orth').text = string
            except AttributeError:
                pass
    dataIndex.unsavedEdit = 1


def oNew(fldbk):
    """define new orthography"""
    fldbk.oList.clearSelection()
    orthManager = QtWidgets.QInputDialog()
    newName = orthManager.getText(orthManager, 'New orthography', 'Enter name for new orthography')
    if newName[1] is not False and len(newName[0]) > 0:
        kind = 'export'
        root = dataIndex.root
        elemList = list(root)
        elemList.reverse()
        for i, item in enumerate(elemList):
            if item.tag == 'Media':
                break
            elif item.tag == 'Abbreviations':
                break
        i = len(elemList) - i
        newOrthNode = etree.Element('Orthography')
        root.insert(i, newOrthNode)
        if fldbk.oList.rowCount() == 0:
            newPrimeBox = QtWidgets.QMessageBox()
            newPrimeBox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            newPrimeBox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Cancel | QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            newPrimeBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Yes)
            newPrimeBox.setText('Set as primary orthography?')
            newPrimeBox.setInformativeText('Use these transformations automatically to '
                                           'generate IPA forms of lexical items on Lexicon cards?'
                                           'These transcriptions become part of the database.')
            choice = newPrimeBox.exec()
            if choice == QtWidgets.QMessageBox.StandardButton.Yes:
                kind = 'primary'
                for i in range(0, fldbk.oList.rowCount()):
                    if fldbk.oList.item(i, 1).text() == 'primary':
                        fldbk.oList.item(i, 1).setText('')
                        break
                dataIndex.root.set('Orth', newName[0])
                if len(fldbk.oDiacriticsField.toPlainText()) != 0:
                    dataIndex.diacrits = []
                    for item in fldbk.oDiacriticsField.toPlainText().split(', '):
                        dataIndex.diacrits.append(item.strip())
            elif choice == QtWidgets.QMessageBox.StandardButton.Cancel:
                return
        newOrthNode.text = fldbk.oOrder.toPlainText()
        if len(fldbk.oDiacriticsField.toPlainText()) != 0:
            diacrits = fldbk.oDiacriticsField.toPlainText()
            newOrthNode.set('Diacrits', diacrits)
        newOrthNode.set('Name', newName[0])
        i = fldbk.oList.rowCount()
        newOrth = QtWidgets.QTableWidgetItem(1001)
        newType = QtWidgets.QTableWidgetItem(1001)
        newOrth.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
        newType.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
        newOrth.setText(newName[0])
        newOrth.setData(36, newOrthNode)
        newType.setText(kind)
        fldbk.oList.setRowCount(i + 1)
        fldbk.oList.setItem(i, 0, newOrth)
        fldbk.oList.setItem(i, 1, newType)
        fldbk.oList.setRowHeight(i, 20)
        fldbk.oList.selectRow(i)
        fldbk.oDeleteBtn.setEnabled(1)
        fldbk.oUpdateBtn.setEnabled(1)
        fldbk.oClearTransformBtn.setEnabled(1)
        fldbk.oSetBtn.setEnabled(1)
        fldbk.oApplyBtn.setEnabled(1)
        dataIndex.unsavedEdit = 1


def selectORow():
    fldbk = dataIndex.fldbk
    theRow = fldbk.oList.currentRow()
    node = fldbk.oList.item(theRow, 0).data(36)
    order = node.text
    fldbk.oOrder.setPlainText(order)
    fldbk.oList.selectRow(theRow)
    fldbk.oDeleteBtn.setEnabled(1)
    fldbk.oUpdateBtn.setEnabled(1)
    fldbk.oClearTransformBtn.setEnabled(1)
    fldbk.oSetBtn.setEnabled(1)
    fldbk.oApplyBtn.setEnabled(1)


def oUpdate(fldbk):
    """update changes to orthography"""
    newTrans = fldbk.oOrder.toPlainText()
    tRow = fldbk.oList.currentRow()
    tNode = fldbk.oList.item(tRow, 0).data(36)
    tNode.text = newTrans
    if len(fldbk.oDiacriticsField.toPlainText()) != 0:
        diacrits = fldbk.oDiacriticsField.toPlainText()
        tNode.set('Diacrits', diacrits)
        if fldbk.oList.item(tRow, 1).text() == 'primary':
            dataIndex.diacrits = []
            for item in fldbk.oDiacriticsField.toPlainText().split(', '):
                dataIndex.diacrits.append(item.strip())
    dataIndex.unsavedEdit = 1


def oClearTest(fldbk):
    """clear test fields"""
    fldbk.oOutput.clear()
    fldbk.oInput.clear()


def oRandomTest(fldbk, n):
    """select random forms to test"""
    for i in range(0, n):
        lexList = dataIndex.lexDict
        node = choice(list(lexList.keys()))
        string = dataIndex.lexDict[node].findtext('Orth')
        if i == 0:
            inPut = string
        else:
            inPut += "\n" + string
        IPA = Orthographies.testTransform(fldbk, string)
        if i == 0:
            output = IPA
        else:
            output += "\n" + IPA
    fldbk.oInput.setPlainText(inPut)
    fldbk.oOutput.setPlainText(output)


def oTest(fldbk):
    """test transformations on a string"""
    string = fldbk.oInput.toPlainText()
    IPA = Orthographies.testTransform(fldbk, string)
    fldbk.oOutput.setPlainText(IPA)


def oRandom(fldbk):
    """test alphabetization on a random set of n lexical entries"""
    n = fldbk.oNumberBox.value()
    oRandomTest(fldbk, n)


def oNumber(fldbk):
    """set the number of random lexical entries for orthography test"""
    n = fldbk.oNumberBox.value()
    oRandomTest(fldbk, n)


def oHelp(self):
    helpBox = SearchHelp.OrthHelpDialog(self)
    helpBox.exec()


"""metadata researcher buttons"""


def mRDataCheck(fldbk, rCode):
    """ensures minimal content and prevents duplication of researchers and codes"""
    if len(rCode) == 0 or len(fldbk.mResearcher.toPlainText()) == 0:
        missingDataBox = QtWidgets.QMessageBox()
        missingDataBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        missingDataBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        missingDataBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        missingDataBox.setText('Missing data.')
        missingDataBox.setInformativeText('You must have a name and a researcher code for every '
                                          'researcher. Please provide the missing information.')
        missingDataBox.exec()
        return 'abort'
    for i in range(0, fldbk.mRTable.rowCount()):
        if fldbk.mRTable.item(i, 0).text() == rCode:
            duplicateCodeBox = QtWidgets.QMessageBox()
            duplicateCodeBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            duplicateCodeBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            duplicateCodeBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            duplicateCodeBox.setText('Duplicate speaker code.')
            duplicateCodeBox.setInformativeText('This code is already in use. Please provide a '
                                                'unique code for this researcher.')
            duplicateCodeBox.exec()
            return 'abort'
    return 'okay'


def mRUpdate(fldbk):
    """update researcher metadata"""
    try:
        node = fldbk.mRTable.item(fldbk.mRTable.currentRow(), 0).data(36)
    except AttributeError:
        return
    RCode = node.attrib.get("RCode")
    node.clear()
    node.set('RCode', RCode)
    researcher = fldbk.mResearcher.toPlainText()
    affiliation = fldbk.mAffiliation.toPlainText()
    info = fldbk.mRInfo.toPlainText()
    if len(researcher) != 0:
        subNode = etree.SubElement(node, 'Name')
        subNode.text = researcher
    if len(affiliation) != 0:
        subNode = etree.SubElement(node, 'Affiliation')
        subNode.text = affiliation
    if len(info) != 0:
        subNode = etree.SubElement(node, 'Info')
        subNode.text = info
    try:
        level = fldbk.mPrivilegesBox.currentText()
    except AttributeError:
        level = 0
    if level == 'None':
        level = 0

    fldbk.mRTable.item(fldbk.mRTable.currentRow(), 1).setText(researcher)
    if level != 0:
        fldbk.mRTable.item(fldbk.mRTable.currentRow(), 2).setText(level)
        node.set('Level', level)
        fldbk.mRTable.item(fldbk.mRTable.currentRow(), 0).setData(40, level)
    else:
        fldbk.mRTable.item(fldbk.mRTable.currentRow(), 2).setText(None)
        fldbk.mRTable.item(fldbk.mRTable.currentRow(), 0).setData(40, None)
        try:
            del node.attrib['Level']
        except AttributeError:
            pass
    fldbk.mRTable.item(fldbk.mRTable.currentRow(), 3).setText(affiliation)
    fldbk.mRTable.item(fldbk.mRTable.currentRow(), 4).setText(info)
    for j in range(0, fldbk.mRTable.columnCount() - 1):
        fldbk.mRTable.resizeColumnToContents(j)
        if fldbk.mRTable.columnWidth(j) > 165:
            fldbk.mRTable.setColumnWidth(j, 165)
    fldbk.mRTable.resizeColumnToContents(fldbk.mRTable.columnCount() - 1)
    dataIndex.unsavedEdit = 1


def mRClear(fldbk):
    """clear researcher metadata entry fields"""
    fldbk.mResearcher.clear()
    fldbk.mRCode.clear()
    fldbk.mAffiliation.clear()
    fldbk.mRInfo.clear()
    fldbk.mRAddBtn.setEnabled(1)
    fldbk.mRUpdateBtn.setEnabled(0)
    fldbk.mRDelBtn.setEnabled(0)
    fldbk.mRCode.setReadOnly(0)
    fldbk.mPrivilegesBox.setCurrentIndex(-1)
    fldbk.mRTable.selectRow(-1)
    fldbk.mRSetDefaultBtn.setEnabled(0)


def mRAdd(fldbk):
    """add new researcher metadata"""
    rCode = fldbk.mRCode.toPlainText()
    status = mRDataCheck(fldbk, rCode)
    if status == 'abort':
        return
    newRschr = etree.Element('Rschr', {'RCode': rCode})
    newName = etree.SubElement(newRschr, 'Name')
    name = newName.text = fldbk.mResearcher.toPlainText()
    if len(fldbk.mAffiliation.toPlainText()) != 0:
        newAff = etree.SubElement(newRschr, 'Affiliation')
        affiliation = newAff.text = fldbk.mAffiliation.toPlainText()
    else:
        affiliation = None
    if len(fldbk.mRInfo.toPlainText()) != 0:
        newInfo = etree.SubElement(newRschr, 'Info')
        info = newInfo.text = fldbk.mRInfo.toPlainText()
    else:
        info = None
    """need to set level attrib"""
    if fldbk.mPrivilegesBox.currentIndex() != -1:
        level = fldbk.mPrivilegesBox.currentText()
    else:
        level = None
    if level == 'None':
        level = None
    if level is not None:
        newRschr.set('Level', level)
    k = dataIndex.root.find('Rschr')
    d = list(dataIndex.root).index(k)
    dataIndex.root.insert(d, newRschr)
    if k.attrib.get('RCode') == 'YYY':
        dataIndex.root.remove(k)
        del dataIndex.rschrDict['YYY']
    dataList = [rCode, name, level, affiliation, info]
    if fldbk.mRTable.rowCount() == 0:
        fldbk.mRTable.setRowCount(1)
    else:
        fldbk.mRTable.setRowCount(fldbk.mRTable.rowCount() + 1)
    newRow = fldbk.mRTable.rowCount() - 1
    for i in range(0, 5):
        newItem = QtWidgets.QTableWidgetItem(1001)
        if dataList[i] is not None:
            itemText = dataList[i]
            newItem.setText(itemText)
            newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
        fldbk.mRTable.setItem(newRow, i, newItem)
    fldbk.mRTable.item(newRow, 0).setData(36, newRschr)
    fldbk.mRTable.item(newRow, 0).setData(40, level)
    for j in range(0, fldbk.mRTable.columnCount() - 1):
        fldbk.mRTable.resizeColumnToContents(j)
    fldbk.mRTable.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
    fldbk.mRTable.scrollToItem(newItem, QtWidgets.QAbstractItemView.ScrollHint.PositionAtCenter)
    fldbk.mRTable.selectRow(newRow)
    for j in range(0, fldbk.mRTable.columnCount() - 1):
        fldbk.mRTable.resizeColumnToContents(j)
        if fldbk.mRTable.columnWidth(j) > 165:
            fldbk.mRTable.setColumnWidth(j, 165)
    fldbk.mRTable.resizeColumnToContents(fldbk.mRTable.columnCount() - 1)
    fldbk.mRUpdateBtn.setEnabled(1)
    dictBuilder.rschrDictBuilder(fldbk)
    fldbk.mRSetDefaultBtn.setEnabled(1)
    dataIndex.unsavedEdit = 1


def mRDel(fldbk):
    """delete researcher metadata"""
    badRow = fldbk.mRTable.currentRow()
    badNode = fldbk.mRTable.item(badRow, 0).data(36)
    RCode = badNode.attrib.get('RCode')
    deletedCodeBox = QtWidgets.QMessageBox()
    deletedCodeBox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
    purgeBtn = deletedCodeBox.addButton("Purge", QtWidgets.QMessageBox.ButtonRole.ActionRole)
    purgeBtn.setToolTip("remove all instances of this code from\n database and replace with “YYY”.")
    deletedCodeBox.setStandardButtons(
        QtWidgets.QMessageBox.StandardButton.Cancel | QtWidgets.QMessageBox.StandardButton.Ok)
    deletedCodeBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
    deletedCodeBox.setText('Delete researcher code?')
    deletedCodeBox.setInformativeText('This code may be in use in the database and '
                                      'removing it could cause validation errors. '
                                      'Selecting “Purge” will replace the code '
                                      'throughout the database. Proceed with deletion?')
    choice = deletedCodeBox.exec()
    if deletedCodeBox.clickedButton() == purgeBtn:
        """Rschr attributes are found in Lex, Ex, Text, Dset, Media;
        these need to be replaced with YYY"""
        for node in dataIndex.root.iter():
            if node.attrib.get('Rschr') == RCode:
                node.set('Rschr', 'YYY')
        fldbk.mRTable.removeRow(badRow)
        dataIndex.root.remove(badNode)
        del dataIndex.rschrDict[RCode]
    if choice == QtWidgets.QMessageBox.StandardButton.Ok:
        fldbk.mRTable.removeRow(badRow)
        dataIndex.root.remove(badNode)
        del dataIndex.rschrDict[RCode]
    mRClear(fldbk)


"""metadata speaker buttons"""


def mSpDataCheck(fldbk, sCode):
    """ensures minimal content and prevent lack of duplication for consultants and codes"""
    if len(sCode) == 0 or len(fldbk.mSpeaker.toPlainText()) == 0:
        missingDataBox = QtWidgets.QMessageBox()
        missingDataBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        missingDataBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        missingDataBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        missingDataBox.setText('Missing data.')
        missingDataBox.setInformativeText('You must have a name and a speaker code for every '
                                          'consultant. Please provide the missing information.')
        missingDataBox.exec()
        return 'abort'
    for i in range(0, fldbk.mSpTable.rowCount()):
        if fldbk.mSpTable.item(i, 0).text() == sCode:
            duplicateCodeBox = QtWidgets.QMessageBox()
            duplicateCodeBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            duplicateCodeBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            duplicateCodeBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            duplicateCodeBox.setText('Duplicate speaker code.')
            duplicateCodeBox.setInformativeText('This code is already in use. Please provide a '
                                                'unique code for this consultant.')
            duplicateCodeBox.exec()
            return 'abort'
    return 'okay'


def mSpUpdate(fldbk):
    """update speaker metadata"""
    try:
        node = fldbk.mSpTable.item(fldbk.mSpTable.currentRow(), 0).data(36)
    except AttributeError:
        return
    SCode = node.attrib.get("SCode")
    node.clear()
    node.set('SCode', SCode)
    speaker = fldbk.mSpeaker.toPlainText()
    birthday = fldbk.mBirthday.toPlainText()
    place = fldbk.mBirthplace.toPlainText()
    info = fldbk.mInfo.toPlainText()
    if len(speaker) != 0:
        subNode = etree.SubElement(node, 'Name')
        subNode.text = speaker
    if len(birthday) != 0:
        subNode = etree.SubElement(node, 'Birthdate')
        subNode.text = birthday
    if len(place) != 0:
        subNode = etree.SubElement(node, 'Place')
        subNode.text = place
    if len(info) != 0:
        subNode = etree.SubElement(node, 'Info')
        subNode.text = info
    fldbk.mSpTable.item(fldbk.mSpTable.currentRow(), 1).setText(speaker)
    fldbk.mSpTable.item(fldbk.mSpTable.currentRow(), 2).setText(birthday)
    fldbk.mSpTable.item(fldbk.mSpTable.currentRow(), 3).setText(place)
    fldbk.mSpTable.item(fldbk.mSpTable.currentRow(), 4).setText(info)
    dataIndex.unsavedEdit = 1


def mSpClear(fldbk):
    """clears speaker metadata"""
    fldbk.mSpeaker.clear()
    fldbk.mSCode.clear()
    fldbk.mBirthday.clear()
    fldbk.mBirthplace.clear()
    fldbk.mInfo.clear()
    fldbk.mSpAddBtn.setEnabled(1)
    fldbk.mSpDelBtn.setEnabled(0)
    fldbk.mSpUpdateBtn.setEnabled(0)
    fldbk.mSCode.setReadOnly(0)
    fldbk.mSpSetDefaultBtn.setEnabled(0)


def mSpAdd(fldbk):
    """add new speaker metadata"""
    sCode = fldbk.mSCode.toPlainText()
    status = mSpDataCheck(fldbk, sCode)
    if status == 'abort':
        return
    newSpkr = etree.Element('Speaker', {'SCode': sCode})
    newName = etree.SubElement(newSpkr, 'Name')
    name = newName.text = fldbk.mSpeaker.toPlainText()
    if len(fldbk.mBirthday.toPlainText()) != 0:
        newBD = etree.SubElement(newSpkr, 'Birthdate')
        birthday = newBD.text = fldbk.mBirthday.toPlainText()
    else:
        birthday = None
    if len(fldbk.mBirthplace.toPlainText()) != 0:
        newBP = etree.SubElement(newSpkr, 'Place')
        place = newBP.text = fldbk.mBirthplace.toPlainText()
    else:
        place = None
    if len(fldbk.mInfo.toPlainText()) != 0:
        newInfo = etree.SubElement(newSpkr, 'Info')
        info = newInfo.text = fldbk.mInfo.toPlainText()
    else:
        info = None
    k = dataIndex.root.find('Speaker')
    d = list(dataIndex.root).index(k)
    dataIndex.root.insert(d, newSpkr)
    if k.attrib.get('SCode') == 'XX':
        dataIndex.root.remove(k)
        del dataIndex.speakerDict['XX']
    dataList = [sCode, name, birthday, place, info]
    if fldbk.mSpTable.rowCount() == 0:
        fldbk.mSpTable.setRowCount(1)
    else:
        fldbk.mSpTable.setRowCount(fldbk.mSpTable.rowCount() + 1)
    newRow = fldbk.mSpTable.rowCount() - 1
    for i in range(0, 5):
        newItem = QtWidgets.QTableWidgetItem(1001)
        if dataList[i] is not None:
            itemText = dataList[i]
            newItem.setText(itemText)
            newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
        fldbk.mSpTable.setItem(newRow, i, newItem)
    fldbk.mSpTable.item(newRow, 0).setData(36, newSpkr)
    fldbk.mSpTable.selectRow(newRow)
    for j in range(0, fldbk.mSpTable.columnCount() - 1):
        fldbk.mSpTable.resizeColumnToContents(j)
    fldbk.mSpTable.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
    fldbk.mSpTable.scrollToItem(newItem, QtWidgets.QAbstractItemView.ScrollHint.PositionAtCenter)
    fldbk.mSpUpdateBtn.setEnabled(1)
    dictBuilder.speakerDictBuilder(fldbk)
    dataIndex.unsavedEdit = 1
    fldbk.mSpSetDefaultBtn.setEnabled(1)


def mSpDel(fldbk):
    badRow = fldbk.mSpTable.currentRow()
    badNode = fldbk.mSpTable.item(badRow, 0).data(36)
    SCode = badNode.attrib.get('SCode')
    """delete speaker metadata"""
    deletedCodeBox = QtWidgets.QMessageBox()
    deletedCodeBox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
    purgeBtn = deletedCodeBox.addButton("Purge", QtWidgets.QMessageBox.ButtonRole.ActionRole)
    purgeBtn.setToolTip("remove all instances of this code from\n database and replace with “XX”.")
    deletedCodeBox.setStandardButtons(
        QtWidgets.QMessageBox.StandardButton.Cancel | QtWidgets.QMessageBox.StandardButton.Ok)
    deletedCodeBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
    deletedCodeBox.setText('Delete speaker code?')
    deletedCodeBox.setInformativeText('This code may be in use in the database and '
                                      'removing it could cause validation errors. '
                                      'Selecting “Purge” will replace the code '
                                      'throughout the database. Proceed with deletion?')
    choice = deletedCodeBox.exec()
    if deletedCodeBox.clickedButton() == purgeBtn:
        """Rschr attributes are found in Lex, Ex, Text, Dset, Media;
        these need to be replaced with YYY"""
        for node in dataIndex.root.iter():
            if node.attrib.get('Spkr') == SCode:
                node.set('Spkr', 'XX')
        fldbk.mSpTable.removeRow(badRow)
        dataIndex.root.remove(badNode)
        del dataIndex.speakerDict[SCode]
    if choice == QtWidgets.QMessageBox.StandardButton.Ok:
        fldbk.mSpTable.removeRow(badRow)
        dataIndex.root.remove(badNode)
        del dataIndex.speakerDict[SCode]
    mSpClear(fldbk)


"""metadata sorting/alphabetization buttons"""


def sSaveOrder(fldbk, title='Save as …'):
    orderManager = QtWidgets.QInputDialog()
    result = orderManager.getText(orderManager, title, 'Enter name for new sorting order.')
    if result[1] is False:
        return
    else:
        newName = result[0]
    sortOrder = fldbk.sOrder.toPlainText()
    if len(fldbk.sExclusions.toPlainText()) != 0:
        exclude = fldbk.sExclusions.toPlainText()
        exclusionList = exclude.split(', ')
        for i in range(0, len(exclusionList)):
            if i == 0:
                sortOrder += "; " + exclusionList[i]
            else:
                sortOrder += ", " + exclusionList[i]
    newNode = etree.SubElement(dataIndex.root, 'SortKey', attrib={'SName': newName})
    # 2) add to list
    item = QtWidgets.QListWidgetItem(newName)
    item.setData(32, newName)
    item.setFlags(
        QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEditable)
    fldbk.sList.addItem(item)
    fldbk.sList.setCurrentItem(item)
    # 3) make sortKey element
    if fldbk.sAccentBtn.isChecked():
        sortOrder += "; exclude accents"
    else:
        sortOrder += "; include accents"
    newNode.text = sortOrder
    fldbk.sOrderChangedLabel.clear()
    fldbk.sOrderChangedLabel.setToolTip('')


def sDeleteOrder(fldbk):
    theRow = fldbk.sList.currentRow()
    theItem = fldbk.sList.currentItem()
    orderName = theItem.data(32)
    # 1) clear from list
    fldbk.sList.takeItem(theRow)
    del theItem
    # 2) delete XML
    if orderName != 'Built-In':
        for child in dataIndex.root.iter('SortKey'):
            if child.attrib.get('SName') == orderName:
                dataIndex.root.remove(child)
                dataIndex.unsavedEdit = 1
                break
    else:
        dataIndex.root.set("noDefaultSort", "1")
    # 3) select previous and load
    if fldbk.sList.currentRow() != 0:
        fldbk.sList.setCurrentRow(theRow - 1)
    else:
        fldbk.sList.setCurrentRow(0)
    selectSRow()
    dataIndex.root.set('SortKey', fldbk.sList.currentItem().data(32))


def sTestOrder(fldbk):
    proxyModelL = Alphabetizer.AlphaTester(fldbk)
    proxyModelL.setSourceModel(fldbk.lLexNav.model())
    proxyModelL.setDynamicSortFilter(True)
    fldbk.sTestView.setModel(proxyModelL)


def sUpdateOrder(fldbk):
    sortOrder = fldbk.sOrder.toPlainText()
    if len(fldbk.sExclusions.toPlainText()) != 0:
        exclude = fldbk.sExclusions.toPlainText()
        exclusionList = exclude.split(', ')
        for i in range(0, len(exclusionList)):
            if i == 0:
                sortOrder += "; " + exclusionList[i]
            else:
                sortOrder += ", " + exclusionList[i]
    if fldbk.sAccentBtn.isChecked():
        sortOrder += "; exclude accents"
    else:
        sortOrder += "; include accents"
    orderName = fldbk.sList.currentItem().text()
    if orderName == 'Built-In':
        orderName = 'default.txt'
        saveFile = open(orderName, "w", encoding="UTF-8")
        saveFile.write(sortOrder)
        saveFile.close()
    else:
        for child in dataIndex.root.iter('SortKey'):
            if child.attrib.get('SName') == orderName:
                child.text = sortOrder
    fldbk.sOrderChangedLabel.clear()
    fldbk.sOrderChangedLabel.setToolTip('')


def sSort(fldbk):
    sUpdateOrder(fldbk)
    proxyModelL = Alphabetizer.Alphabetizer(fldbk)
    proxyModelL.setSourceModel(fldbk.lLexNav.model().sourceModel())
    proxyModelL.setDynamicSortFilter(True)
    fldbk.hLexNav.setModel(proxyModelL)
    fldbk.lLexNav.setModel(proxyModelL)
    fldbk.hLexNav.setSelectionModel(fldbk.lLexNav.selectionModel())


def sNew(fldbk):
    """creates new sortKey from scratch"""
    sSaveOrder(fldbk, 'New sorting order')


def sClear(fldbk):
    fldbk.sOrderChangedLabel.clear()
    fldbk.sOrderChangedLabel.setToolTip('')
    fldbk.sExclusions.clear()
    fldbk.sOrder.clear()


def selectSRow():
    fldbk = dataIndex.fldbk
    theRow = fldbk.sList.currentRow()
    sorting = fldbk.sList.item(theRow).data(32)
    dataIndex.root.set('SortKey', sorting)
    Alphabetizer.Alphabetizer(fldbk)
    fldbk.sList.setCurrentRow(theRow)
    fldbk.sOrderChangedLabel.clear()
    fldbk.sOrderChangedLabel.setToolTip('')


def changeOrderName():
    """this changes the name of the sorting order as it appears in the fieldbook, but does not rename the file"""
    fldbk = dataIndex.fldbk
    newText = fldbk.sList.currentItem().text()
    oldText = fldbk.sList.currentItem().data(32)
    for child in dataIndex.root.iter('SortKey'):
        if child.attrib.get('SName') == oldText:
            child.set('SName', newText)
            break
    dataIndex.root.set('SortKey', newText)
    fldbk.sList.currentItem().setText(newText)


def sMoveUp(fldbk):
    currentRow = fldbk.sList.currentRow()
    if currentRow == 0:
        return
    item = fldbk.sList.takeItem(currentRow)
    fldbk.sList.insertItem(currentRow - 1, item)
    fldbk.sList.setCurrentItem(item)
    sName = item.data(32)
    node = dataIndex.root.find('SortKey[@SName="%s"]' % sName)
    index = list(dataIndex.root).index(node)
    dataIndex.root.remove(node)
    dataIndex.root.insert(index - 1, node)


def sMoveDown(fldbk):
    currentRow = fldbk.sList.currentRow()
    if currentRow == fldbk.sList.count() - 1:
        return
    item = fldbk.sList.takeItem(currentRow)
    fldbk.sList.insertItem(currentRow + 1, item)
    fldbk.sList.setCurrentItem(item)
    sName = item.data(32)
    node = dataIndex.root.find('SortKey[@SName="%s"]' % sName)
    index = list(dataIndex.root).index(node)
    dataIndex.root.remove(node)
    dataIndex.root.insert(index + 1, node)


def selectMRow():
    if dataIndex.fldbk.mMediaTable.currentColumn() == 3:
        caller = dataIndex.fldbk.mMediaTable
        i = caller.currentRow()
        mediaNode = caller.item(i, 0).data(36)
        mediaID = mediaNode.attrib.get('MedID')
        item = None
        mManager = MediaManager.MediaManager(dataIndex.fldbk)
        mManager.renameWindow(mediaNode.attrib.get('Filename'))
        mManager.setValues(mediaID, caller, item)
        mManager.exec()
    dataIndex.fldbk.mMediaTable.selectRow(dataIndex.fldbk.mMediaTable.currentRow())


def playSound(fldbk):
    """begins by checking to see if temporary paths have been set for sound files
    (rather than building the path each time)"""
    caller = fldbk.mMediaTable
    row = caller.currentRow()
    if row == -1:
        return
    node = caller.item(row, 0).data(36)
    IDREF = node.attrib.get('MedID')
    if dataIndex.root.get("MediaFolder"):
        prefix = dataIndex.root.get("MediaFolder")
    else:
        prefix = None
    soundFile = dataIndex.mediaDict[IDREF].get('Filename')
    clipboard = QtWidgets.QApplication.clipboard()
    clipboard.setText(soundFile)
    oldFile = soundFile
    if prefix is not None:
        soundFile = prefix + "/" + soundFile
    if path.isfile(soundFile):
        playaudio.soundOutput(soundFile)

    else:
        mFolder = QtWidgets.QFileDialog(dataIndex.fldbk, "Find missing recording?")
        mFolder.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        mFolder.setOption(QtWidgets.QFileDialog.Option.ReadOnly)
        if mFolder.exec():
            soundFile = mFolder.selectedFiles()[0]
            if dataIndex.root.get("MediaFolder") is None or dataIndex.root.get("MediaFolder") != path.dirname(
                    soundFile):
                setDefaultDirectory(soundFile)
            if path.isfile(soundFile):
                if path.basename(soundFile) != oldFile:
                    dataIndex.mediaDict[IDREF].set('Filename', path.basename(soundFile))
                    caller.item(row, 0).setText(path.basename(soundFile))
        if soundFile:
            playaudio.soundOutput(soundFile)


def setDefaultDirectory(newFile):
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


def newMedia(fldbk):
    # TODO: need to tweak this to allow multiple fields to be selected
    caller = fldbk.mMediaTable
    newFile = QtWidgets.QFileDialog(fldbk, "Add recordings.")
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
        newName = newNames[0]
        if dataIndex.root.get("MediaFolder") is None or dataIndex.root.get("MediaFolder") != path.dirname(newName):
            setDefaultDirectory(newName)
        for item in newNames:
            sound2play = item
            newName = path.basename(item)
            node = dataIndex.root.find('Media[@Filename="%s"]' % newName)
            """call from metadata tab, add media elements to the media table"""
            if node is None:
                medID, node = updateMediaInfo(item, newName)
                mManager = MediaManager.MediaManager(dataIndex.fldbk)
                mManager.renameWindow(newName)
                mManager.setValues(medID, caller, item)
                mManager.setComboBoxes()
                mManager.exec()
            else:
                node = dataIndex.root.find('Media[@Filename="%s"]' % newName)
                file = node.attrib.get('Filename')
                speaker = node.attrib.get('Spkr')
                date = node.attrib.get('Date')
                fileInfo = file + " [" + speaker + " " + date + "]"
                msgbox = QtWidgets.QMessageBox()
                msgbox.setText("File in database.")
                msgbox.setInformativeText('There is already a recording named\n\n%s\n\nin the database. '
                                          'Media files should have unique names.' % fileInfo)
                msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                msgbox.exec()
                return
        playaudio.soundOutput(sound2play)
        dataIndex.unsavedEdit = 1
        return medID


def updateMediaInfo(item, newName):
    """create new media node"""
    tree = dataIndex.root
    medID = idGenerator.generateID("MC", dataIndex.mediaDict)
    elemList = list(tree)
    elemList.reverse()
    for i, node in enumerate(elemList):
        if node.tag == 'Abbreviations':
            break
    i = len(elemList) - i
    newNode = etree.Element('Media')
    tree.insert(i, newNode)
    """add attributes to media element"""
    newNode.set('MedID', medID)
    newNode.set('Filename', newName)
    dataIndex.mediaDict[medID] = newNode

    """update media table"""
    mediaTable = dataIndex.fldbk.mMediaTable
    nextRow = mediaTable.rowCount()
    mediaTable.setRowCount(nextRow + 1)
    firstItem = QtWidgets.QTableWidgetItem(1001)
    firstItem.setText(newName)
    """data 36 is the new XML node"""
    firstItem.setData(36, newNode)
    """data 37 is the path to the sound file"""
    firstItem.setData(37, item)
    firstItem.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
    mediaTable.setItem(nextRow, 0, firstItem)
    secondItem = QtWidgets.QTableWidgetItem(1001)
    secondItem.setText('XX')
    secondItem.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
    mediaTable.setItem(nextRow, 1, secondItem)
    thirdItem = QtWidgets.QTableWidgetItem(1001)
    thirdItem.setText("???")
    thirdItem.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
    mediaTable.setItem(nextRow, 2, thirdItem)
    fourthItem = QtWidgets.QTableWidgetItem(1001)
    fourthItem.setIcon(QtGui.QIcon(':InfoBtn.png'))
    mediaTable.setItem(nextRow, 3, fourthItem)
    mediaTable.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
    mediaTable.scrollToItem(fourthItem, QtWidgets.QAbstractItemView.ScrollHint.PositionAtCenter)
    mediaTable.selectRow(fourthItem.row())
    return medID, newNode
