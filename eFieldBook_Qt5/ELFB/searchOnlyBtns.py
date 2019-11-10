from PyQt5 import QtWidgets, QtCore
from ELFB import dataIndex, searchClasses
from ELFB.palettes import SearchResultsToFile, RecordBrowser
from ELFB.searchClasses import SearchEngine

def saveResults(fldbk):
    if not fldbk.cSearchResults.model():
        return
    formatBox = SearchResultsToFile.SearchResultsToFile(fldbk)
    if formatBox.exec_():
        output = formatBox.compileResults()
        if output == False:
            return
        fname = QtWidgets.QFileDialog.getSaveFileName(fldbk, "Save As...")[0]  
        if fname:
            saveFile = open(fname, "w", encoding = "UTF-8")
            saveFile.write(output)
            saveFile.close()

def clearResults(fldbk):
    fldbk.cTarget.clear()
    fldbk.cNumberOfHits.clear()
    if not fldbk.cSearchResults.model():
        return
    fldbk.cSearchResults.model().clear()
    fldbk.cNarrowBtn.setDisabled(1)
    fldbk.cNarrowBtn.setChecked(0)

def returnToSearch(fldbk):
    if dataIndex.activeSearch:
        try:
            if dataIndex.callingCard[0] == 'L':
                fldbk.tabWidget.setCurrentIndex(1)
                fldbk.lSearchForm.setVisible(1)
                fldbk.lexicon.setVisible(0)
            elif dataIndex.callingCard[0] == 'T':
                fldbk.tabWidget.setCurrentIndex(2)
            elif dataIndex.callingCard[0] == 'E':
                fldbk.tabWidget.setCurrentIndex(3)
            elif dataIndex.callingCard[0] == 'D':
                fldbk.tabWidget.setCurrentIndex(4)
            dataIndex.callingCard = None
        except (TypeError, AttributeError):
            pass
        return
    dataIndex.activeSearch = 'return'
    fldbk.tabWidget.setCurrentIndex(1)

def archive(fldbk):
    try:
        hitsList = ''
        for i in range(0, fldbk.cSearchResults.model().rowCount()):
            node = fldbk.cSearchResults.model().item(i, 0).data(35)
            if i == 0:
                hitsList = node
            else:
                hitsList += "; " + node
        if len(hitsList) != 0:
            fname = QtWidgets.QFileDialog.getSaveFileName(fldbk, "Archive as …")[0]
            if fname:
                saveFile = open(fname, "w", encoding = "UTF-8")
                saveFile.write(hitsList)
                saveFile.close()
    except AttributeError:
        pass
    
def load(fldbk):
    loadDialog = QtWidgets.QFileDialog(fldbk, "Open archive … ?")
    loadDialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
    loadDialog.setOption(QtWidgets.QFileDialog.ReadOnly)
    if loadDialog.exec_():
        fname = loadDialog.selectedFiles()[0]
        archive = open(fname, 'r', encoding='UTF-8').read()
    else:
        return
    hitsList = archive.split('; ')
    searchEngine = SearchEngine(fldbk)
    for item in hitsList:
        if item[0:2] == 'LX':
            hit = dataIndex.lexDict[item]
            SearchEngine.displayLexResults(searchEngine, hit)
        if item[0:2] == 'EX':
            hit = dataIndex.exDict[item]
            SearchEngine.displayExResults(searchEngine, hit)
        if item[0:2] == 'DS':
            hit = dataIndex.dataDict[item]
            SearchEngine.displayDsetResults(searchEngine, hit)
    
def toggleFocus(fldbk, checked):
    if checked == True:
        uncheck(fldbk.cLexiconFocusBox.children())
        uncheck(fldbk.cTextsFocusBox.children())
        uncheck(fldbk.cExamplesFocusBox.children())

def uncheck(targets):
    for checkBox in targets:
        try:
            checkBox.setChecked(0)
        except AttributeError:
            pass

def checkBoxToggled(state):
    if state == 2:
        dataIndex.fldbk.cFindAllBtn.setChecked(0)

def ExCheckBoxToggled(state):
    if state == 2:
        dataIndex.fldbk.cFindAllBtn.setChecked(0)
        uncheck(dataIndex.fldbk.cTextsFocusBox.children())
        dataIndex.fldbk.cTextsFocusBox.setDisabled(1)
    else:
        noCheck = True
        for button in dataIndex.fldbk.cExamplesFocusBox.children():
            try:
                if button.isChecked():
                    noCheck = False
            except AttributeError:
                    pass
        if noCheck == True:
            dataIndex.fldbk.cTextsFocusBox.setEnabled(1)

def searchFor(fldbk):
    #specify search term
    target = fldbk.cTarget.text()
    target = target.strip()

    #set parameters (no accents, diacrits, etc.)
    '''parameters = [accent,diacrit,case,append,recOnly,wholeWord,secondLanguage]'''
    parameters = []
    if fldbk.cAccentBtn.isChecked():
        parameters.append(1)
    else:
        parameters.append(0)
    if fldbk.cDiacritBtn.isChecked():
        parameters.append(1)
    else:
        parameters.append(0)
    if fldbk.cCaseBtn.isChecked():
        parameters.append(1)
    else:
        parameters.append(0)    
    if fldbk.cAppendBtn.isChecked():
        parameters.append(1)
    else:
        fldbk.cNumberOfHits.clear()
        if fldbk.cSearchResults.model() and fldbk.cNarrowBtn.isChecked() == 0:
            fldbk.cSearchResults.model().clear()
        parameters.append(1) 
    if fldbk.cRecOnlyBtn.isChecked():
        parameters.append(1)
    else:
        parameters.append(0)  
    if fldbk.cWholeWordBtn.isChecked():
        parameters.append(1)
    else:
        parameters.append(0)
    if fldbk.cSetLangBtn.isChecked():
        parameters.append(1)
    else:
        parameters.append(0)
        
    #define scope of search
    if fldbk.cFindAllBtn.isChecked():
        lexList =['Orth', 'Def/L1', 'Def/L2', 'Lit', 'Grm', '@Kywd']
        exList = ['Line', 'Mrph', 'ILEG','L1Gloss', 'L2Gloss' ]
        dsetList = ['Data', 'Comments', '@Kywd', '@Spkr', '@Rschr', '@Date', '@Update']
        textList = []
    else:
        lexList = []
        if fldbk.cOrthographyBtn.isChecked():
            lexList.append('Orth')
        if fldbk.cL1DefinitionBtn.isChecked():
            lexList.append('Def/L1')
        if fldbk.cL2DefinitionBtn.isChecked():
            lexList.append('Def/L2')
        if fldbk.cLiteralGlossBtn.isChecked():
            lexList.append('Lit')    
        if fldbk.cGrammarBtn.isChecked():
            lexList.append('Grm')        
        if fldbk.cKeywordBtn.isChecked():
            lexList.append('@Kywd')        
        textList = []
        if fldbk.cLineTextsBtn.isChecked():
            textList.append('Line')
        if fldbk.cParseTextsBtn.isChecked():
            textList.append('Mrph')
        if fldbk.cAnalysisTextsBtn.isChecked():
            textList.append('ILEG')
        if fldbk.cL1GlossTextsBtn.isChecked():
            textList.append('L1Gloss')    
        if fldbk.cL2GlossTextsBtn.isChecked():
            textList.append('L2Gloss')        
        exList = []
        if fldbk.cLineExamplesBtn.isChecked():
            exList.append('Line')
        if fldbk.cParseExamplesBtn.isChecked():
            exList.append('Mrph')
        if fldbk.cAnalysisExamplesBtn.isChecked():
            exList.append('ILEG')
        if fldbk.cL1GlossExamplesBtn.isChecked():
            exList.append('L1Gloss')    
        if fldbk.cL2GlossExamplesBtn.isChecked():
            exList.append('L2Gloss')   
        if fldbk.cExKeywordBtn.isChecked():
            lexList.append('@Kywd')
        dsetList = []
    if fldbk.cNarrowBtn.isChecked():
        #get list of IDRefs of elements to search
        elemList = []
        for i in range(0, fldbk.cSearchResults.model().rowCount()):
            node = fldbk.cSearchResults.model().item(i, 0).data(35)
            elemList.append(node)
        fldbk.cSearchResults.model().clear()
        lxIDList = []
        exIDList = []
        dsIDList = []
        for item in elemList:
            if item[0:2] == 'LX':
                lxIDList.append(item)
            if item[0:2] == 'EX':
                exIDList.append(item)
            if item[0:2] == 'DS':
                dsIDList.append(item)
        if len(lxIDList) != 0:
            engine = searchClasses.LexSearchEngine(fldbk, target, parameters, lexList, lxIDList)
            engine.doSearch()     
        if len(exIDList) != 0:
            engine = searchClasses.ExSearchEngine(fldbk, target, parameters, exList, exIDList)   
            engine.doSearch()     
        if len(dsIDList) != 0:
            engine = searchClasses.DSetSearchEngine(fldbk, target, parameters, dsetList, dsIDList)
            engine.doSearch()     
    else:
        if len(lexList) != 0:
            engine = searchClasses.LexSearchEngine(fldbk, target, parameters, lexList)
            engine.doSearch()     
        if len(exList) != 0:
            engine = searchClasses.ExSearchEngine(fldbk, target, parameters, exList)
            engine.doSearch()     
        if len(textList) != 0:
            engine = searchClasses.TextSearchEngine(fldbk, target, parameters, textList)
            engine.doSearch()     
        if len(dsetList) != 0:
            engine = searchClasses.DSetSearchEngine(fldbk, target, parameters, dsetList)
            engine.doSearch()     
            
def searchBrowser(fldbk):
    if fldbk.cSearchResults.model() != None:
        try:
            fldbk.recordBrowser.close()
        except AttributeError:
            pass
        fldbk.recordBrowser = RecordBrowser.RecordBrowser(fldbk)
        fldbk.recordBrowser.setObjectName('recordBrowser')
        fldbk.recordBrowser.setModal(0)
        fldbk.recordBrowser.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowStaysOnTopHint)
        fldbk.recordBrowser.show()
        fldbk.recordBrowser.raise_()
