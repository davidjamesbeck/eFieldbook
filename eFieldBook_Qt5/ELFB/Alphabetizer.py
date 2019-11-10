from PyQt5 import QtWidgets,  QtCore
from ELFB import dataIndex

class Alphabetizer(QtCore.QSortFilterProxyModel):
    
    def __init__(self,  parent):
        super(Alphabetizer, self).__init__(parent)
        self.setSortCaseSensitivity(0)
        self.sort(0,QtCore.Qt.AscendingOrder)
        self.fldbk = dataIndex.fldbk
        accents = "áéíóú"
        plains = "aeiou"
        self.transTable = accents.maketrans(accents, plains)        
        self.buildOrder()
        self.fldbk.lLexNav.scrollTo(self.fldbk.lLexNav.currentIndex(),QtWidgets.QAbstractItemView.EnsureVisible)
        self.fldbk.hLexNav.scrollTo(self.fldbk.hLexNav.currentIndex(),QtWidgets.QAbstractItemView.EnsureVisible)

    def buildOrder(self):
        defaultFile = QtCore.QFile(dataIndex.rootPath + '/ELFB/default.txt')
        if dataIndex.root.attrib.get('SortKey') == None:
            dataIndex.root.set('SortKey', 'Built-In')
        if dataIndex.root.attrib.get('SortKey') == "Built-In":
            defaultFile.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text)
            defaultString = QtCore.QTextStream(defaultFile)
            sortOrder = defaultString.readAll()
        else:
            currentSortKey = dataIndex.root.attrib.get('SortKey')
            for child in dataIndex.root.iter('SortKey'):
                if child.attrib.get('SName') == currentSortKey: 
                    sortOrder = child.text
                    break
        sortOrder = sortOrder.strip()
        twoLists = sortOrder.split(';')        
        orderList = twoLists[0].split(',')
        if len(twoLists) == 3:
            exclusionList = twoLists[1].split(',')
        else:
            exclusionList = None
        if twoLists[-1] == ' exclude accents':
            self.fldbk.sAccentBtn.setChecked(True)
        else:
            self.fldbk.sAccentBtn.setChecked(False)
        self.exclusions = []
        sortOrderList = []
        excludeString = ''
        sortString = ''
        if exclusionList != None:
            for item in exclusionList:
                newItem = item.strip()
                self.exclusions.append(newItem)
                if len(excludeString) != 0:
                    excludeString += ", " + newItem
                else:
                    excludeString += newItem                
        for i in range(0, len(orderList)):
            item = orderList[i].strip()
            ordinal = str(chr(i+8704))
            sortOrderList.append([item, ordinal,  len(item)])
            if len(sortString) != 0:
                sortString += ", " + item
            else:
                sortString += item
        unorderedSortKey = sorted(sortOrderList,  key = lambda s: s[2],  reverse=True)
        self.sortKey = []
        for item in unorderedSortKey:
            self.sortKey.append(item[:-1])
        self.fldbk.sOrder.setPlainText(sortString)
        self.fldbk.sExclusions.setPlainText(excludeString)
 
    def lessThan(self,  left,  right):
        leftData = self.transform(self.sourceModel().data(left))
        rightData = self.transform(self.sourceModel().data(right))
        if leftData < rightData:
            return True
        else:
            return False
  
    def transform(self, string):
        '''removes character to be excluded from sorting'''
        if self.fldbk.sAccentBtn.isChecked():
            string = string.translate(self.transTable)
        if string[-1] == '-':
            string = string[:-1]
        for item in self.exclusions:
            if item in string:
                string = string.replace(item, "")
        for item in self.sortKey:
            if item[0] in string:
                string = string.replace(item[0], item[1])
        return string

class AlphaTester(Alphabetizer):
    '''class for testing sorting orders without implementing them'''
    def buildOrder(self):
        orderList = self.fldbk.sOrder.toPlainText().split(',')
        exclusionList = self.fldbk.sExclusions.toPlainText().split(",")
        self.exclusions = []
        sortOrderList = []
        if exclusionList != None:
            for item in exclusionList:
                newItem = item.strip()
                self.exclusions.append(newItem)         
        for i in range(0, len(orderList)):
            item = orderList[i].strip()
            ordinal = str(chr(i+8704))
            sortOrderList.append([item, ordinal,  len(item)])
        unorderedSortKey = sorted(sortOrderList,  key = lambda s: s[2],  reverse=True)
        self.sortKey = []
        for item in unorderedSortKey:
            self.sortKey.append(item[:-1])
