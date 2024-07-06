from PyQt6 import QtWidgets, QtCore,  QtGui
from ELFB import dataIndex, metaDataBtns, fileMaintenance


def fillRTable(fldbk):
    fldbk.mRTable.setRowCount(0)
    if dataIndex.root.findall("./Rschr/Name"):
        for child in dataIndex.root.iter('Rschr'):
            if child.get('RCode') != 'YYY':
                name = child.find('Name').text
                code = child.attrib.get('RCode')
                try:
                    level = child.attrib.get('Level')
                except AttributeError:
                    level = None
                try:
                    affiliation = child.find('Affiliation').text
                except AttributeError:
                    affiliation = None
                try:
                    info = child.find('Info').text
                except AttributeError:
                    info = None
                dataList = [code, name, level, affiliation, info]
                nextRow = fldbk.mRTable.rowCount()
                fldbk.mRTable.setRowCount(nextRow+1)
                fldbk.mRTable.setRowHeight(nextRow, 20)
                for i in range(0, 5):
                    newItem = QtWidgets.QTableWidgetItem(1001)
                    if dataList[i] is not None:
                        itemText = dataList[i]
                        newItem.setText(itemText)
                    newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
                    fldbk.mRTable.setItem(nextRow, i, newItem)
                fldbk.mRTable.item(nextRow, 0).setData(36, child)
                fldbk.mRTable.item(nextRow, 0).setData(40, level)
        for j in range(0, fldbk.mRTable.columnCount()-1):
            fldbk.mRTable.resizeColumnToContents(j)
            if fldbk.mRTable.columnWidth(j) > 165:
                fldbk.mRTable.setColumnWidth(j, 165)
        fldbk.mRTable.resizeColumnToContents(fldbk.mRTable.columnCount()-1)
        
def fillConsultantTable(fldbk):
    if dataIndex.root.findall("./Speaker/Name"):
        fldbk.mSpTable.setRowCount(0)
        for child in dataIndex.root.iter('Speaker'):
            if child.get('SCode') != "XX":
                name = child.find('Name').text
                code = child.attrib.get('SCode')
                try:
                    birthday = child.find('Birthdate').text
                except AttributeError:
                    birthday = None
                try:
                    place = child.find('Place').text
                except AttributeError:
                    place = None
                try:
                    info = child.find('Info').text
                except AttributeError:
                    info = None
                dataList = [code, name, birthday, place, info]
                nextRow = fldbk.mSpTable.rowCount()
                fldbk.mSpTable.setRowCount(nextRow+1)
                fldbk.mSpTable.setRowHeight(nextRow, 20)
                for i in range(0, 5):
                    newItem = QtWidgets.QTableWidgetItem(1001)
                    if dataList[i] is not None:
                        itemText = dataList[i]
                        newItem.setText(itemText)
                    newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
                    fldbk.mSpTable.setItem(nextRow, i, newItem)
                fldbk.mSpTable.item(nextRow, 0).setData(36, child)
        for j in range(0, fldbk.mSpTable.columnCount()-1):
            fldbk.mSpTable.resizeColumnToContents(j)
    else:
        fldbk.mSpTable.clear()
            
def fillMediaTable(fldbk, icon=None):
    if icon is None:
        icon = QtGui.QIcon(':InfoBtn.png')
    if dataIndex.root.findall("Media"):
        fldbk.mMediaTable.setRowCount(0)
        fldbk.mMediaTable.setColumnWidth(0, 216)
        fldbk.mMediaTable.setColumnWidth(1, 34)
        fldbk.mMediaTable.setColumnWidth(2, 40)
        fldbk.mMediaTable.setColumnWidth(3, 25)
        for item in dataIndex.mediaDict:
            mediaElement = dataIndex.mediaDict[item]
            file = mediaElement.attrib.get('Filename')
            try:
                speaker = mediaElement.attrib.get('Spkr')
            except AttributeError:
                speaker = 'XX'
                mediaElement.set('Spkr', 'XX')
            try:
                researcher = mediaElement.attrib.get('Rschr')
            except AttributeError:
                researcher = "YYY"
                mediaElement.set('Rschr', 'YYY')
            dataList = [file, speaker, researcher]
            nextRow = fldbk.mMediaTable.rowCount()
            fldbk.mMediaTable.setRowCount(nextRow+1)
            fldbk.mMediaTable.setRowHeight(nextRow, 20)
            for i in range(0, len(dataList)):
                newItem = QtWidgets.QTableWidgetItem(1001)
                if dataList[i] is not None:
                    itemText = dataList[i]
                    newItem.setText(itemText)
                    newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
                    fldbk.mMediaTable.setItem(nextRow, i, newItem)
            fldbk.mMediaTable.item(nextRow, 0).setData(36, mediaElement)
            newItem = QtWidgets.QTableWidgetItem(1001)
            newItem.setIcon(icon)
            fldbk.mMediaTable.setItem(nextRow, 3, newItem) 
        fldbk.mMediaTable.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)    
    else:
        fldbk.mMediaTable.clear()
        
def fillOrth(fldbk):
    if dataIndex.root.find('Orthography') is not None:
        labelList = []
        orthList = dataIndex.root.findall('Orthography')
        fldbk.oList.setRowCount(len(orthList))
        for i, item in enumerate(orthList):
            item = fileMaintenance.cleanOrthoElement(item)
            name = item.attrib.get('Name')
            labelList.append(name)
            kind = ''
            newOrth = QtWidgets.QTableWidgetItem(1001)
            newType = QtWidgets.QTableWidgetItem(1001)
            newOrth.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
            newType.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
            newOrth.setText(name)
            newType.setText(kind)
            fldbk.oList.setItem(i, 0, newOrth)
            fldbk.oList.setItem(i, 1, newType)
            fldbk.oList.item(i, 0).setData(36, item)
            fldbk.oList.setRowHeight(i, 20) 
        fldbk.oExportSelect.insertItems(0, labelList)
    
        if dataIndex.root.attrib.get('Orth') is not None:
            for i, item in enumerate(orthList):
                if item.attrib.get('Name') == dataIndex.root.attrib.get('Orth'):
                    fldbk.oList.item(i, 1).setText('primary')
                    fldbk.oExportSelect.setCurrentIndex(i)
                    node = fldbk.oList.item(i, 0).data(36)
                    order = node.text
                    try:
                        diacrits = node.attrib.get('Diacrits')
                        fldbk.oDiacriticsField.setPlainText(diacrits)
                        dataIndex.diacrits = []
                        for item2 in diacrits.split(', '):
                            dataIndex.diacrits.append(item2.strip())
                    except AttributeError:  
                        pass
                    fldbk.oOrder.setPlainText(order)
                    fldbk.oList.selectRow(i)
                    fldbk.oDeleteBtn.setEnabled(1)
                    fldbk.oUpdateBtn.setEnabled(1)
                    fldbk.oClearTransformBtn.setEnabled(1)   
                    fldbk.oSetBtn.setEnabled(1)   
                    fldbk.oApplyBtn.setEnabled(1)
    else:
        fldbk.oDeleteBtn.setEnabled(0)
        fldbk.oUpdateBtn.setEnabled(0)
        fldbk.oClearTransformBtn.setEnabled(0)   


def fillSort(fldbk):
    if dataIndex.root.get("noDefaultSort") is None:
        item = QtWidgets.QListWidgetItem('Built-In')
        item.setData(32, 'Built-In')
        item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
        fldbk.sList.addItem(item)
    delegate = QtWidgets.QItemDelegate()
    fldbk.sList.setItemDelegate(delegate)
    delegate.commitData.connect(metaDataBtns.changeOrderName)        
    for node in dataIndex.root.iter('SortKey'):
        node = fileMaintenance.cleanSortElement(node)
        sortKey = node.attrib.get('SName')
        item = QtWidgets.QListWidgetItem(sortKey)
        item.setData(32, sortKey)
        item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEditable)
        fldbk.sList.addItem(item)  
    currentItem = fldbk.sList.findItems(dataIndex.root.get('SortKey', default="Built-In"), QtCore.Qt.MatchFlag.MatchExactly)
    fldbk.sList.setCurrentItem(currentItem[0])


def fillAbbrevTables(fldbk):
    abbrModel = QtGui.QStandardItemModel()
    for child in dataIndex.root.iter('Abbr'):
        abbrev = child.attrib.get('Abv').swapcase()
        itemText = '<small>' + abbrev + '</small>&emsp;‘' + child.attrib.get('Term') + '’'
        try:
            form = child.attrib.get('Form')
            itemText += ' (' + form + ')'
        except AttributeError:
            pass
        except TypeError:
            pass
        newItem = QtGui.QStandardItem()
        newItem.setData(child.attrib.get('ACode'), 35)
        newItem.setData(child, 36)
        newItem.setText(itemText)
        newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
        abbrModel.appendRow(newItem)
    abbrModelProxy = QtCore.QSortFilterProxyModel()
    abbrModelProxy.setSourceModel(abbrModel)
    abbrModelProxy.setDynamicSortFilter(True)
    abbrModelProxy.sort(0, QtCore.Qt.SortOrder.AscendingOrder)
    fldbk.eAbbreviations.setModel(abbrModelProxy)
    fldbk.eAbbreviations.resizeColumnToContents(0)
    fldbk.eAbbreviations.resizeRowsToContents()
    fldbk.iAbbreviations.setModel(abbrModelProxy)
    fldbk.iAbbreviations.resizeColumnToContents(0)
    fldbk.iAbbreviations.resizeRowsToContents()
