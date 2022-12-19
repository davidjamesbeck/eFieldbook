from PyQt6 import QtWidgets, QtCore
from ELFB.GrmField import GrmField
from ELFB.DefTable import DefTable
from ELFB.EgTable import EgTable
from ELFB.HTMLDelegate import HTMLDelegate
from ELFB import metaDataBtns, dataIndex, cardLoader
from ELFB.palettes.SoundPanel import SoundPanel
from ELFB.palettes.NavBar import NavBar, ExampleNavBar


def soundPanelBuilder(fldbk):
    fldbk.lSound = SoundPanel(fldbk.lexicon)
    fldbk.lSound.setGeometry(8, 575, 146, 77)
    fldbk.tSound = SoundPanel(fldbk.texts)
    fldbk.tSound.setGeometry(8, 575, 146, 77)
    fldbk.eSound = SoundPanel(fldbk.examples)
    fldbk.eSound.setGeometry(8, 575, 146, 77)
    fldbk.dSound = SoundPanel(fldbk.datasets)
    fldbk.dSound.setGeometry(8, 575, 146, 77)    
    

def grammarTableBuilder(fldbk):
    fldbk.lGrammar = GrmField(fldbk.lGrammarBox)
    fldbk.lGrammar.setGeometry(6, 22, 182, 87)
    fldbk.lGrammar.setToolTip(QtWidgets.QApplication.translate("Fieldbook", "Grammatical information, comparisons, and cross-refs.\n"
    "Doubleclick to edit.", None))


def defTableBuilder(fldbk):
    fldbk.lL1Definition = DefTable(fldbk.lL1Box)
    fldbk.lL2Definition = DefTable(fldbk.lL2Box)
    fldbk.lL1Definition.setToolTip(QtWidgets.QApplication.translate("Fieldbook", "Definitions in primary working language.\n"
    "Doubleclick definition to edit, click example\nto go to analysis.", None))
    fldbk.lL2Definition.setToolTip(QtWidgets.QApplication.translate("Fieldbook", "Definitions in secondary working language. \n"
    "Doubleclick definition to edit, click example\nto go to analysis.", None))


def egTableBuilder(fldbk):
    fldbk.eAnalysis = EgTable(fldbk.eExScrollAreaContents)
    fldbk.eAnalysis.setGeometry(0, 54, 1900, 200)


def speakerTableBuilder(fldbk):
    delegate = HTMLDelegate()
    fldbk.mSpTable = QtWidgets.QTableWidget(fldbk.mConsultantsTab)
    fldbk.mSpTable.setGeometry(15, 0, 500, 272)
    fldbk.mSpTable.setItemDelegate(delegate)
    fldbk.mSpTable.horizontalHeader().setEnabled(0)
    fldbk.mSpTable.verticalHeader().setEnabled(0)
    fldbk.mSpTable.verticalHeader().hide()
    fldbk.mSpTable.horizontalHeader().hide()
    fldbk.mSpTable.setShowGrid(0)
    fldbk.mSpTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    fldbk.mSpTable.setStyleSheet("selection-background-color: #E6E6E6;")
    fldbk.mSpTable.setColumnCount(5)
    
    def fillSpForm():
        fldbk.mSpTable.selectRow(fldbk.mSpTable.currentRow())
        u = fldbk.mSpTable.currentRow()
        fldbk.mSCode.clear()
        fldbk.mSpeaker.clear()
        fldbk.mBirthday.clear()
        fldbk.mBirthplace.clear()
        fldbk.mInfo.clear()
        fldbk.mSCode.setHtml(fldbk.mSpTable.item(u, 0).text())
        fldbk.mSpeaker.setHtml(fldbk.mSpTable.item(u, 1).text())
        fldbk.mBirthday.setHtml(fldbk.mSpTable.item(u, 2).text())
        fldbk.mBirthplace.setHtml(fldbk.mSpTable.item(u, 3).text())
        fldbk.mInfo.setHtml(fldbk.mSpTable.item(u, 4).text())
        fldbk.mSpAddBtn.setEnabled(0)
        fldbk.mSpDelBtn.setEnabled(1)
        fldbk.mSpUpdateBtn.setEnabled(1)
        fldbk.mSCode.setReadOnly(1)
        fldbk.mSpSetDefaultBtn.setEnabled(1)
    
    fldbk.mSpTable.itemClicked.connect(fillSpForm)
    

def researcherTableBuilder(fldbk):
    delegate = HTMLDelegate()
    fldbk.mRTable = QtWidgets.QTableWidget(fldbk.mResearchersTab)
    fldbk.mRTable.setGeometry(15, 0, 500, 272)
    fldbk.mRTable.setItemDelegate(delegate)
    fldbk.mRTable.horizontalHeader().setEnabled(0)
    fldbk.mRTable.verticalHeader().setEnabled(0)
    fldbk.mRTable.verticalHeader().hide()
    fldbk.mRTable.horizontalHeader().hide()
    fldbk.mRTable.setShowGrid(0)
    fldbk.mRTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    fldbk.mRTable.setStyleSheet("selection-background-color: #E6E6E6;")
    fldbk.mRTable.setColumnCount(5)

    def fillRForm():
        fldbk.mRTable.selectRow(fldbk.mRTable.currentRow())
        u = fldbk.mRTable.currentRow()
        fldbk.mRCode.clear()
        fldbk.mResearcher.clear()
        fldbk.mAffiliation.clear()
        fldbk.mRInfo.clear()
        fldbk.mRCode.setHtml(fldbk.mRTable.item(u, 0).text())
        fldbk.mResearcher.setHtml(fldbk.mRTable.item(u, 1).text())
        fldbk.mAffiliation.setHtml(fldbk.mRTable.item(u, 3).text())
        fldbk.mRInfo.setHtml(fldbk.mRTable.item(u, 4).text())
        fldbk.mRAddBtn.setEnabled(0)
        fldbk.mRDelBtn.setEnabled(1)
        fldbk.mRCode.setReadOnly(1)
        fldbk.mRUpdateBtn.setEnabled(1)
        y = fldbk.mPrivilegesBox.findText(fldbk.mRTable.item(u, 0).data(40))
        if y != -1:
            fldbk.mPrivilegesBox.setCurrentIndex(y)
        elif y == 'None':
            fldbk.mPrivilegesBox.setCurrentIndex(-1)
        else:
            fldbk.mPrivilegesBox.setCurrentIndex(-1)
        fldbk.mRSetDefaultBtn.setEnabled(1)

    fldbk.mRTable.itemClicked.connect(fillRForm)
    

def mediaTableBuilder(fldbk):
    fldbk.mMediaTable = QtWidgets.QTableWidget(fldbk.mMediaBox)
    fldbk.mMediaTable.setGeometry(15, 33, 328, 576)
    fldbk.mMediaTable.horizontalHeader().setEnabled(0)
    fldbk.mMediaTable.verticalHeader().setEnabled(0)
    fldbk.mMediaTable.verticalHeader().hide()
    fldbk.mMediaTable.horizontalHeader().hide()
    fldbk.mMediaTable.setShowGrid(0)
    fldbk.mMediaTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    fldbk.mMediaTable.setStyleSheet("selection-background-color: #E6E6E6;")
    fldbk.mMediaTable.setColumnCount(4)
    fldbk.mMediaTable.setAlternatingRowColors(1)
    fldbk.mMediaTable.itemClicked.connect(metaDataBtns.selectMRow)


def egAbbreviationsBuilder(fldbk):
    delegate = HTMLDelegate()
    fldbk.eAbbreviations = QtWidgets.QTableView(fldbk.eAbbrBox)
    fldbk.eAbbreviations.setGeometry(12, 29, 234, 448)
    fldbk.eAbbreviations.setObjectName('Abbreviations')
    fldbk.eAbbreviations.setItemDelegate(delegate)
    fldbk.eAbbreviations.horizontalHeader().setEnabled(0)
    fldbk.eAbbreviations.verticalHeader().setEnabled(0)
    fldbk.eAbbreviations.verticalHeader().hide()
    fldbk.eAbbreviations.horizontalHeader().hide()
    fldbk.eAbbreviations.setShowGrid(0)
    fldbk.eAbbreviations.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    fldbk.eAbbreviations.setStyleSheet("selection-background-color: #ADD8E6;")
    

def indexAbbreviationsBuilder(fldbk):
    delegate = HTMLDelegate()
    fldbk.iAbbreviations = QtWidgets.QTableView(fldbk.iAbbrBox)
    fldbk.iAbbreviations.setGeometry(15, 30, 230, 470)
    fldbk.iAbbreviations.setObjectName('Abbreviations')
    fldbk.iAbbreviations.setItemDelegate(delegate)
    fldbk.iAbbreviations.horizontalHeader().setEnabled(0)
    fldbk.iAbbreviations.verticalHeader().setEnabled(0)
    fldbk.iAbbreviations.verticalHeader().hide()
    fldbk.iAbbreviations.horizontalHeader().hide()
    fldbk.iAbbreviations.setShowGrid(0)
    fldbk.iAbbreviations.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    fldbk.iAbbreviations.setStyleSheet("selection-background-color: #ADD8E6;")


def navBarBuilder(fldbk):
    fldbk.lNavBar = NavBar(fldbk.lexicon)
    fldbk.lNavBar.setGeometry(167, 594, 258, 56)
    fldbk.lNavBar.navIndex = fldbk.lLexNav
    fldbk.lNavBar.dict = dataIndex.lexDict
    fldbk.lNavBar.loader = cardLoader.loadLexCard
    if len(dataIndex.lastLex) != 0:
        fldbk.lNavBar.stack.append(dataIndex.lastLex)
    fldbk.eNavBar = ExampleNavBar(fldbk.examples)
    fldbk.eNavBar.setGeometry(167, 594, 258, 56)
    fldbk.eNavBar.navIndex = dataIndex.exDict
    fldbk.eNavBar.dict = dataIndex.exDict
    fldbk.eNavBar.loader = cardLoader.loadExCard
    if len(dataIndex.lastEx) != 0:
        fldbk.eNavBar.stack.append(dataIndex.lastEx)
    fldbk.tNavBar = NavBar(fldbk.texts)
    fldbk.tNavBar.setGeometry(167, 594, 258, 56)
    fldbk.tNavBar.navIndex = fldbk.tTextNav
    fldbk.tNavBar.dict = dataIndex.textDict
    fldbk.tNavBar.loader = cardLoader.loadTextCard
    if len(dataIndex.lastText) != 0:
        fldbk.tNavBar.stack.append(dataIndex.lastText)
    fldbk.dNavBar = NavBar(fldbk.datasets)
    fldbk.dNavBar.setGeometry(167, 594, 258, 56)
    fldbk.dNavBar.navIndex = fldbk.dDataNav
    fldbk.dNavBar.dict = dataIndex.dataDict
    fldbk.dNavBar.loader = cardLoader.loadDataCard
    if len(dataIndex.lastDset) != 0:
        fldbk.dNavBar.stack.append(dataIndex.lastDset)
