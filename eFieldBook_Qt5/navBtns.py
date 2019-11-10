from PyQt5 import QtWidgets
from ELFB import cardLoader, cardStack, dataIndex

'''navigation buttons'''

def btnForward(fldbk):
    cardStack.goToCard(fldbk, +1)

def btnBack(fldbk):
    cardStack.goToCard(fldbk, -1)

def lastLxCard(fldbk):
    navBar = fldbk.lLexNav
    dct = dataIndex.lexDict
    targetCard = lastCard(navBar,dct)
    cardLoader.loadLexCard(targetCard)

def lastTxtCard(fldbk):
    navBar = fldbk.tTextNav
    dct = dataIndex.textDict
    targetCard = lastCard(navBar,dct)
    cardLoader.loadTextCard(targetCard)

def LastExCard(fldbk):
    egList = list(dataIndex.exDict.keys())
    targetCard = dataIndex.exDict[egList[len(dataIndex.exDict)-1]]
    cardLoader.loadExCard(targetCard)

def lastDsetCard(fldbk):
    navBar = fldbk.dDataNav
    dct = dataIndex.dataDict
    targetCard = lastCard(navBar,dct)
    cardLoader.loadDataCard(targetCard)

def lastCard(navBar,dct):
    lastItem = navBar.model().rowCount() - 1
    data = navBar.model().index(lastItem,0).data(32)
    targetCard = dct[data]
    navBar.setCurrentIndex(navBar.model().index(lastItem,0))
    navBar.scrollTo(navBar.currentIndex(), QtWidgets.QAbstractItemView.EnsureVisible)
    return targetCard
    
def firstLxCard(fldbk):
    navBar = fldbk.lLexNav
    dct = dataIndex.lexDict
    targetCard = firstCard(navBar,dct)
    cardLoader.loadLexCard(targetCard)

def firstTxtCard(fldbk):
    navBar = fldbk.tTextNav
    dct = dataIndex.textDict
    targetCard = firstCard(navBar,dct)
    cardLoader.loadTextCard(targetCard)

def firstEgCard(fldbk):
    egList = list(dataIndex.exDict.keys())
    targetCard = dataIndex.exDict[egList[0]]
    cardLoader.loadExCard(targetCard)

def firstDsetCard(fldbk):
    navBar = fldbk.dDataNav
    dct = dataIndex.dataDict
    targetCard = firstCard(navBar,dct)
    cardLoader.loadDataCard(targetCard)

def firstCard(navBar,dct):
    data = navBar.model().index(0,0).data(32)
    targetCard = dct[data]
    navBar.setCurrentIndex(navBar.model().index(0,0))
    navBar.scrollTo(navBar.currentIndex(), QtWidgets.QAbstractItemView.EnsureVisible)
    return targetCard

def goPrevLx(fldbk):
    navBar = fldbk.lLexNav
    dct = dataIndex.lexDict
    targetCard = goPrev(navBar,dct)
    cardLoader.loadLexCard(targetCard)

def goPrevEg(fldbk):
    currentID = dataIndex.currentCard               
    i = 1
    for child in dataIndex.root.iter('Ex'):
        if child.attrib.get('ExID') != currentID:
            prevID = child.attrib.get('ExID')
            i += 1
        else:
            if i != 1:
                break
            else:
                prevID = currentID
    targetCard = dataIndex.exDict[prevID]
    cardLoader.loadExCard(targetCard)
    
def goPrevTxt(fldbk):
    navBar = fldbk.tTextNav
    dct = dataIndex.textDict
    targetCard = goPrev(navBar,dct)
    cardLoader.loadTextCard(targetCard)

def goPrevDset(fldbk):
    navBar = fldbk.dDataNav
    dct = dataIndex.dataDict
    targetCard = goPrev(navBar,dct)
    cardLoader.loadDataCard(targetCard)

def goPrev(navBar,dct):
    try:
        if navBar.currentIndex().row() == 0:
            current = navBar.model().rowCount() - 1
        else:
            current = navBar.currentIndex().row() - 1
        navBar.setCurrentIndex(navBar.model().index(current,0))
        navBar.scrollTo(navBar.currentIndex(), QtWidgets.QAbstractItemView.EnsureVisible)
        data = navBar.currentIndex().data(32)
        targetCard = dct[data]
        return targetCard
    except AttributeError:
        pass

def goNextLx(fldbk):
    navBar = fldbk.lLexNav
    dct = dataIndex.lexDict
    targetCard = goNext(navBar,dct)
    cardLoader.loadLexCard(targetCard)

def goNextEg(fldbk):
    currentID = dataIndex.currentCard
    getNextCard = 0
    for child in dataIndex.root.iter('Ex'):
        if child.attrib.get('ExID') == currentID:
            getNextCard = 1
        else:
            if getNextCard == 1:
                nextID = child.attrib.get('ExID')
                break
    try:
        targetCard = dataIndex.exDict[nextID]
    except UnboundLocalError:
        nextID = dataIndex.root.find('Ex').attrib.get('ExID')
        targetCard = dataIndex.exDict[nextID]
    cardLoader.loadExCard(targetCard)
    
def goNextTxt(fldbk):
    navBar = fldbk.tTextNav
    dct = dataIndex.textDict
    targetCard = goNext(navBar,dct)
    cardLoader.loadTextCard(targetCard)

def goNextDset(fldbk):
    navBar = fldbk.dDataNav
    dct = dataIndex.dataDict
    targetCard = goNext(navBar,dct)
    cardLoader.loadDataCard(targetCard)

def goNext(navBar,dct):
    if navBar.currentIndex().row() == navBar.model().rowCount() - 1:
        current = 0
    else:
        current = navBar.currentIndex().row() + 1
    navBar.setCurrentIndex(navBar.model().index(current,0))
    navBar.scrollTo(navBar.currentIndex(), QtWidgets.QAbstractItemView.EnsureVisible)
    data = navBar.currentIndex().data(32)
    targetCard = dct[data]
    return targetCard
