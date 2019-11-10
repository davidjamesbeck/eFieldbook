from PyQt5 import QtGui, QtWidgets, QtCore
from ELFB import dataIndex, cardLoader, searchClasses, HTMLDelegate

def lAdvancedSearch(fldbk):
    '''sets up form for searches'''
    dataIndex.updateEnabled = 'off'
    dataIndex.activeSearch = 1
    fldList = listFields(fldbk)
    for fld in fldList:
        fld.clear()
    fldbk.lDerivationBox.setVisible(0)
    fldbk.lLexNav.setVisible(0)
#    fldbk.lControlBar.setVisible(0)
#    fldbk.lSoundBox.setVisible(0)
    fldbk.lL1Definition.setVisible(0)
    fldbk.lL2Definition.setVisible(0)
    fldbk.lHeader.setVisible(0)
    fldbk.lUpdated.setVisible(0)
    if fldbk.lAutoBtn.isChecked():
        dataIndex.autoTransform = 1
    else:
        dataIndex.autoTransform = 0
    fldbk.lAutoBtn.setChecked(0)
    fldbk.lAutoBtn.setVisible(0)
    fldbk.lDoneBtn.setVisible(0)
    fldbk.lNewBtn.setVisible(0)
    fldbk.lClipBtn.setVisible(0)
    delegate = HTMLDelegate.HTMLDelegate()
    font = QtGui.QFont()
    
    fldbk.sDoneBtn = QtWidgets.QCheckBox(fldbk.lexicon)
    fldbk.sDoneBtn.setGeometry(920, 117, 65, 18)
    fldbk.sDoneBtn.setText('Done?')
    fldbk.sDoneBtn.setStyleSheet('QCheckBox {font-size: 9pt; font-style: italic;}')
    fldbk.sDoneBtn.setToolTip('Check box to search only completed entries.\nClear box to search for unfinished entries.')
    fldbk.sDoneBtn.setTristate(1)
    fldbk.sDoneBtn.setCheckState(1)
    fldbk.sDoneBtn.setVisible(1)
    
    fldbk.lSearchHeader = QtWidgets.QGroupBox(fldbk.lexicon)
    fldbk.lSearchHeader.setGeometry(7, -2, 904, 138)
    fldbk.lSearchHeader.setObjectName('lSearchHeader')
    fldbk.lSearchHeader.setStyleSheet('QLineEdit {padding-left: 3px;}'
                                        'QFrame {border: 0px solid black; border-radius: 8px;'
                                        'padding: 0px; background-color: rgb(255, 255, 255);}')
    fldbk.lSearchHeader.setTitle('Lexicographic info')
    fldbk.lSearchHeader.setVisible(1)
    
    fldbk.lSearchPOS = QtWidgets.QPlainTextEdit(fldbk.lSearchHeader)
    fldbk.lSearchPOS.setGeometry(9, 28, 57, 30)    
    fldbk.lSearchPOS.setObjectName('lSearchPOS')
    fldbk.lSearchPOS.setStyleSheet('padding-left: 6px;')
    font.setPointSize(12)
    fldbk.lSearchPOS.setToolTip('search part of speech')
    fldbk.lSearchPOS.setFont(font)
    fldbk.lSearchPOS.setVisible(1)
    
    fldbk.lSearchReg = QtWidgets.QPlainTextEdit(fldbk.lSearchHeader)
    fldbk.lSearchReg.setGeometry(9, 70, 57, 26)
    fldbk.lSearchReg.setObjectName('lSearchReg')
    fldbk.lSearchReg.setStyleSheet('padding-left: 6px')
    font.setPointSize(10)
    fldbk.lSearchReg.setToolTip('search register')
    fldbk.lSearchReg.setFont(font)    
    fldbk.lSearchReg.setVisible(1)

    fldbk.lSearchOrth = QtWidgets.QLineEdit(fldbk.lSearchHeader)
    fldbk.lSearchOrth.setGeometry(74, 24, 473, 39)
    fldbk.lSearchOrth.setObjectName('lSearchOrth')
    font.setPointSize(18)
    fldbk.lSearchOrth.setToolTip('search orthographic form')
    fldbk.lSearchOrth.setFont(font)    
    fldbk.lSearchOrth.setVisible(1)
    
    fldbk.lSearchIPA = QtWidgets.QLineEdit(fldbk.lSearchHeader)
    fldbk.lSearchIPA.setGeometry(74, 68, 473, 30)
    fldbk.lSearchIPA.setObjectName('lSearchIPA')
    font.setPointSize(12)
    fldbk.lSearchIPA.setToolTip('search phonetic form')
    fldbk.lSearchIPA.setFont(font)    
    fldbk.lSearchIPA.setVisible(1)
    
    fldbk.lSearchLit = QtWidgets.QTextEdit(fldbk.lSearchHeader)
    fldbk.lSearchLit.setGeometry(9, 104, 633, 26)
    fldbk.lSearchLit.setObjectName('lSearchLit')
    font.setPointSize(10)
    fldbk.lSearchLit.setToolTip('search literal gloss')
    fldbk.lSearchLit.setFont(font)    
    fldbk.lSearchLit.setVisible(1)
    
    fldbk.lDialectSearch = QtWidgets.QTableWidget(fldbk.lSearchHeader)
    fldbk.lDialectSearch.setGeometry(554, 28, 140, 30)
    fldbk.lDialectSearch.setObjectName('lDialectSearch')
    fldbk.lDialectSearch.setStyleSheet('QTableWidget {gridline-color: white; border-radius: 8px;}')
    fldbk.lDialectSearch.setItemDelegate(delegate)   
    fldbk.lDialectSearch.setRowCount(1)
    fldbk.lDialectSearch.setColumnCount(2)
    fldbk.lDialectSearch.setColumnWidth(0, 40)
    fldbk.lDialectSearch.setColumnWidth(1, 98)
    fldbk.lDialectSearch.horizontalHeader().hide()
    fldbk.lDialectSearch.verticalHeader().hide()
    item1 = QtWidgets.QTableWidgetItem()
    item1.setToolTip('search by dialect name')
    item1.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable)
    item2 = QtWidgets.QTableWidgetItem()
    item2.setToolTip('search for forms')
    item2.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable)
    fldbk.lDialectSearch.setItem(0, 0, item1)
    fldbk.lDialectSearch.setItem(0, 1, item2)
    fldbk.lDialectSearch.setVisible(1)   
    
    fldbk.notations = QtWidgets.QGroupBox(fldbk.lSearchHeader)
    fldbk.notations.setGeometry(QtCore.QRect(700, 25, 194, 105))
    fldbk.notations.setVisible(1)
    
    fldbk.lGrammarSearch = QtWidgets.QTableWidget(fldbk.notations)
    fldbk.lGrammarSearch.setObjectName('lGrammarSearch')
    fldbk.lGrammarSearch.setItemDelegate(delegate)
    fldbk.lGrammarSearch.setGeometry(QtCore.QRect(4, 3, 186, 29))
    fldbk.lGrammarSearch.setStyleSheet('QTableWidget {gridline-color: white; border-radius: 8px;}')
    fldbk.lGrammarSearch.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    fldbk.lGrammarSearch.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    fldbk.lGrammarSearch.setRowCount(1)
    fldbk.lGrammarSearch.setColumnCount(2)
    fldbk.lGrammarSearch.setColumnWidth(0, 40)
    fldbk.lGrammarSearch.setColumnWidth(1, 144)
    fldbk.lGrammarSearch.horizontalHeader().hide()
    fldbk.lGrammarSearch.verticalHeader().hide()
    item1 = QtWidgets.QTableWidgetItem()
    item1.setToolTip('search grammatical labels (e.g., "pl.")')
    item1.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable)
    item2 = QtWidgets.QTableWidgetItem()
    item2.setToolTip('search for forms')
    item2.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable)
    fldbk.lGrammarSearch.setItem(0, 0, item1)
    fldbk.lGrammarSearch.setItem(0, 1, item2)
    fldbk.lGrammarSearch.setVisible(1)
    
    fldbk.lCfSearch = QtWidgets.QTextEdit(fldbk.notations)
    fldbk.lCfSearch.setObjectName('lCfSearch')
    fldbk.lCfSearch.setGeometry(QtCore.QRect(4, 37, 186, 29))
    fldbk.lCfSearch.setVisible(1)
    fldbk.lCfSearch.setToolTip('search cross-references')

    fldbk.lC2Search = QtWidgets.QTextEdit(fldbk.notations)
    fldbk.lC2Search.setObjectName('lC2Search')
    fldbk.lC2Search.setGeometry(QtCore.QRect(4, 70, 186, 29))
    fldbk.lC2Search.setVisible(1)
    fldbk.lC2Search.setToolTip('search comparisons')
    
    fldbk.lSearchBrrw = QtWidgets.QTextEdit(fldbk.lSearchHeader)
    fldbk.lSearchBrrw.setObjectName('lSrchBrrw')
    fldbk.lSearchBrrw.setGeometry(QtCore.QRect(554, 68, 140, 30))
    fldbk.lSearchBrrw.setToolTip('search borrowings')
    font.setPointSize(11)
    fldbk.lSearchBrrw.setFont(font)
    fldbk.lSearchBrrw.setVisible(1)
    fldbk.notations = QtWidgets.QGroupBox(fldbk.lSearchHeader)
    fldbk.notations.setGeometry(QtCore.QRect(700, 25, 194, 105))
    fldbk.notations.setVisible(1)   
    fldbk.lSearchUpdate = QtWidgets.QPlainTextEdit(fldbk.lMetadataBox)
    fldbk.lSearchUpdate.setGeometry(QtCore.QRect(80, 76, 60, 18))
    font.setPointSize(8)
    font.setBold(False)
    font.setItalic(False)
    font.setWeight(50)
    fldbk.lSearchUpdate.setFont(font)
    fldbk.lSearchUpdate.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    fldbk.lSearchUpdate.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    fldbk.lSearchUpdate.setObjectName("lSearchUpdate")
    fldbk.lSearchUpdate.setVisible(1)
    
    fldbk.lL1Search = QtWidgets.QTextEdit(fldbk.lL1Box)
    fldbk.lL1Search.setObjectName('lL1Search')
    fldbk.lL1Search.setGeometry(QtCore.QRect(7, 26, 689, 116))
    fldbk.lL2Search = QtWidgets.QTextEdit(fldbk.lL2Box)
    fldbk.lL2Search.setObjectName('lL2Search')
    fldbk.lL2Search.setGeometry(QtCore.QRect(7, 26, 689, 116))
    fldbk.lL1Search.setVisible(1)
    fldbk.lL2Search.setVisible(1)   
    fldbk.lSearchControlBar = QtWidgets.QFrame(fldbk.lexicon)
    fldbk.lSearchControlBar.setGeometry(QtCore.QRect(167, 594, 342, 56))
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(fldbk.lSearchControlBar.sizePolicy().hasHeightForWidth())
    fldbk.lSearchControlBar.setSizePolicy(sizePolicy)
    controlBar = dataIndex.rootPath + '/ELFB/ui/rsrc/ControlPanel.png'
    fldbk.lSearchControlBar.setStyleSheet("QPushButton {border: 0px solid black;"
"     border-radius: 4px;"
"     min-width: 76px;"
"     min-height: 24px;"
"     max-width: 76px;"
"     max-height: 24px;"
"     background: #6698FF;"
"     color: white;}"
"QPushButton:pressed {background: #1E90FF; border: 2px outset #1E90FF;}"
"QFrame {border: 1px solid gray; "
        "border: 0px solid black;"
        "border-radius: 8px;"
        "padding: 0px;"
        "background-image: url('%s');}" %controlBar)
    fldbk.lSearchControlBar.setFrameShape(QtWidgets.QFrame.StyledPanel)
    fldbk.lSearchControlBar.setFrameShadow(QtWidgets.QFrame.Sunken)  
    fldbk.lSearchControlBar.setVisible(1)
    barLayout = QtWidgets.QHBoxLayout()
    fldbk.lSearchControlBar.setLayout(barLayout)
    fldbk.doSearch = QtWidgets.QPushButton()
    font.setPointSize(10)
    font.setBold(False)
    font.setItalic(False)
    font.setWeight(50)
    fldbk.doSearch.setFont(font)
    fldbk.doSearch.setText('Submit')
    fldbk.doSearch.setToolTip('Perform search')
    barLayout.addWidget(fldbk.doSearch)
    fldbk.clearForm = QtWidgets.QPushButton()
    font.setPointSize(10)
    font.setBold(False)
    font.setItalic(False)
    font.setWeight(50)
    fldbk.clearForm.setFont(font)
    fldbk.clearForm.setText('Clear form')
    fldbk.clearForm.setToolTip('Clear all fields')
    barLayout.addWidget(fldbk.clearForm)
    fldbk.lCancelSearch = QtWidgets.QPushButton()
    font.setPointSize(10)
    font.setBold(False)
    font.setItalic(False)
    font.setWeight(50)
    fldbk.lCancelSearch.setFont(font)
    fldbk.lCancelSearch.setText('Cancel')
    fldbk.lCancelSearch.setToolTip('Go back to lexicon')
    barLayout.addWidget(fldbk.lCancelSearch)
    fldbk.doSearch.clicked.connect(callSearchEngine)
    fldbk.clearForm.clicked.connect(clearForm)
    fldbk.lCancelSearch.clicked.connect(restoreLexCard)
    fldbk.searchParam = QtWidgets.QGroupBox(fldbk.lexicon)
    fldbk.searchParam.setGeometry(QtCore.QRect(8, 136, 147, 213))
    fldbk.searchParam.setTitle("Settings")
    fldbk.searchParam.setStyleSheet("QCheckBox {font-size: 10pts; font-style: italic;}")
    fldbk.caseBtn = QtWidgets.QCheckBox(fldbk.searchParam)
    fldbk.caseBtn.setGeometry(10, 30, 120, 20)
    fldbk.caseBtn.setText('  Ignore case')
    fldbk.caseBtn.setToolTip('Perform case-insensitive searches.')
    fldbk.caseBtn.setChecked(1)
    fldbk.accentBtn = QtWidgets.QCheckBox(fldbk.searchParam)
    fldbk.accentBtn.setGeometry(10, 60, 120, 20)
    fldbk.accentBtn.setText('  Ignore accents')
    fldbk.accentBtn.setToolTip('Perform searches that ignore lexical accent.\n'
                                        'Search term must contain no accented characters.')
    fldbk.accentBtn.setChecked(0)    
    fldbk.diacritBtn = QtWidgets.QCheckBox(fldbk.searchParam)
    fldbk.diacritBtn.setGeometry(10, 90, 120, 20)
    fldbk.diacritBtn.setText('  Ignore diacritics')
    fldbk.diacritBtn.setToolTip('Perform searches that ignore diacritics.\n'
                                        'Search term must contain no diacritics.')    
    fldbk.diacritBtn.setChecked(0)      
    fldbk.appendBtn = QtWidgets.QCheckBox(fldbk.searchParam)
    fldbk.appendBtn.setGeometry(10, 120, 120, 20)
    fldbk.appendBtn.setText('  Append results')
    fldbk.appendBtn.setToolTip('Search results will not overwrite the results\n'
                                            'of previous searches on "Search" card.')    
    fldbk.appendBtn.setChecked(0)   
    fldbk.wholeWordBtn = QtWidgets.QCheckBox(fldbk.searchParam)
    fldbk.wholeWordBtn.setGeometry(10, 150, 120, 20)
    fldbk.wholeWordBtn.setText('  Whole word')
    fldbk.wholeWordBtn.setToolTip('Find whole words only.')    
    fldbk.wholeWordBtn.setChecked(0)      
    fldbk.setLangBtn = QtWidgets.QCheckBox(fldbk.searchParam)
    fldbk.setLangBtn.setGeometry(10, 180, 120, 20)
    fldbk.setLangBtn.setText('  Secondary lang.')
    fldbk.setFont
    fldbk.setLangBtn.setToolTip('Select for results in secondary language.')    
    fldbk.setLangBtn.setChecked(0)      
    fldbk.searchParam.setVisible(1)
    
    fldbk.instructionBox = QtWidgets.QGroupBox(fldbk.lexicon)
    fldbk.instructionBox.setGeometry(QtCore.QRect(912, 136, 210, 340))
    fldbk.instructionBox.setTitle('Instructions')
    fldbk.instruction = QtWidgets.QTextEdit(fldbk.instructionBox)
    fldbk.instruction.setGeometry(QtCore.QRect(10, 30, 190, 410))
    fldbk.instruction.setReadOnly(1)
    fldbk.instruction.setObjectName('Instructions')
    fldbk.instruction.setStyleSheet('background-color: rgb(217,217,217); border: 0px,0px,0px,0px')
    fldbk.instruction.setText('Enter text to find in the fields where you wish to search. '
                                        'Entering terms in more than one field will search for entries that '
                                        'meet all search criteria.\n\n'
                                        'Enter "&" between AND search terms in the same field, place "¬" before terms '
                                        'for NOT searches. \n\nFor edge-sensitive searches, place "#" on the edge you '
                                        'wish the search to key on (e.g., "#an" will find all words beginning '
                                        'with the string "an").\n\n'
                                        'Combine AND/NOT and "#" in the order "¬#". \n\n'
                                        'Use the checkboxes on the left to parameterize searches.')
    fldbk.instructionBox.setVisible(1)
    
def callSearchEngine():
    fldbk = dataIndex.fldbk
    searchClasses.LexSearchEngine(fldbk)

def clearForm():
    fldbk = dataIndex.fldbk
    fldList = listFields(fldbk)  
    for fld in fldList:
        fld.clear()

def listFields(fldbk):
    fldList = []
    childList = fldbk.tabWidget.findChildren(QtWidgets.QPlainTextEdit)
    for child in childList:
        if child.objectName()[0] == 'l':
            fldList.append(child)
    childList = fldbk.tabWidget.findChildren(QtWidgets.QTextEdit)
    for child in childList:
        if child.objectName()[0] == 'l':
            fldList.append(child)
    childList = fldbk.tabWidget.findChildren(QtWidgets.QLineEdit)
    for child in childList:
        if child.objectName()[0] == 'l':
            fldList.append(child)
    return fldList
    
def restoreLexCard(textRoot=None):
    fldbk = dataIndex.fldbk
    if textRoot == False:
        textRoot = dataIndex.lexDict[dataIndex.currentCard]
    cardLoader.loadLexCard(textRoot)
    fldbk.lSearchHeader.setVisible(0)
    fldbk.lL1Search.setVisible(0)
    fldbk.lL2Search.setVisible(0)
    fldbk.lSearchControlBar.setVisible(0)
    fldbk.lSearchUpdate.setVisible(0)
    fldbk.searchParam.setVisible(0)
    fldbk.sDoneBtn.setVisible(0)
    fldbk.instructionBox.setVisible(0)
    fldbk.searchParam.deleteLater()
    fldbk.lL1Search.deleteLater()
    fldbk.lL2Search.deleteLater()
    fldbk.lSearchHeader.deleteLater()
    fldbk.lSearchControlBar.deleteLater()
    fldbk.lSearchUpdate.deleteLater()
    fldbk.sDoneBtn.deleteLater()
    fldbk.instructionBox.deleteLater()
    fldbk.lDerivationBox.setVisible(1)
    fldbk.lLexNav.setVisible(1)
    fldbk.lHeader.setVisible(1)
    fldbk.lL1Definition.setVisible(1)
    fldbk.lL2Definition.setVisible(1)
    fldbk.lSoundBox.setVisible(1)
    fldbk.lControlBar.setVisible(1)
    fldbk.lUpdated.setVisible(1)
    fldbk.lAutoBtn.setVisible(1)
    try:
        if dataIndex.autoTransform == 1:
            fldbk.lAutoBtn.setChecked(1)
        else:
            fldbk.lAutoBtn.setChecked(0)
        dataIndex.autoTransform = None
    except AttributeError:
        pass
    fldbk.lDoneBtn.setVisible(1)
    fldbk.lNewBtn.setVisible(1)
    fldbk.lClipBtn.setVisible(1)
    dataIndex.updateEnabled = 'on'
    dataIndex.activeSearch = None
