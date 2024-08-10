from PyQt6 import QtGui, QtCore
import ELFB.dataIndex as dataIndex
import ELFB.HTMLDelegate as HTMLDelegate
import ELFB.dsetOnlyBtns as dsetOnlyBtns
import ELFB.formattingHandlers as formattingHandlers
import ELFB.palettes.EgSearchDialog as EgSearchDialog
import ELFB.palettes.TextSearchDialog as TextSearchDialog
import ELFB.palettes.DSetSearchDialog as DSetSearchDialog
import operator
import xml.etree.ElementTree as etree


class SearchEngine(QtCore.QObject):
    def __init__(self, parent, target=None, parameters=None, scope=None, list=None):
        super(SearchEngine, self).__init__(parent)
        self.fldbk = dataIndex.fldbk
        self.fldbk.cSearchResults.setSpacing(5)
        self.fldbk.cSearchResults.setStyleSheet("selection-background-color: #E6E6E6; color: rgb(0, 0, 0);")
        delegate = HTMLDelegate.SearchDelegate()
        self.fldbk.cSearchResults.setItemDelegate(delegate)
        self.numberOfHits = 0
        if target is None:
            self.parameters = []
            self.scope = []
            self.target = None
            self.orSwitch = 'off'
        else:
            self.parameters = parameters
            self.scope = scope
            self.target = target
            self.orSwitch = 'on'
        if list is None:
            self.list = None
        else:
            self.list = list
            self.numberOfHits = len(list)
        self.diacritList = self.makeDiacritList()
        dataIndex.callingCard = dataIndex.currentCard
        if not self.fldbk.cSearchResults.model():
            self.fldbk.cNarrowBtn.setDisabled(1)
        elif self.fldbk.cSearchResults.model().rowCount() == 0:
            self.fldbk.cNarrowBtn.setDisabled(1)
        else:
            self.fldbk.cNarrowBtn.setEnabled(1)
        
    def checkForRecordings(self, entry):
        if entry.find('Sound') is None:
            rec = False
        else:
            rec = True
        return rec

    def updateBrowser(self, idList, parameters):
        """this next line means that after each search, the browser’s index 
        is reset, even if this is an appended search. Might want to reconsider later."""
        self.fldbk.recordBrowser.listIndex = 0 
        if parameters[3] == 1:
            self.fldbk.recordBrowser.hitList.extend(idList)
        else:
            self.fldbk.recordBrowser.hitList = idList
            
    def doSearch(self):
        pass
        
    def formatHandler(self, theString):
        theString = theString.replace("{i}", "<i>")
        theString = theString.replace("{/i}", "</i>")
        return theString
    
    def removeDiacrits(self, lookFor):
        try:
            if dataIndex.diacrits:
                diacrits = ''
                for item in dataIndex.diacrits:
                    diacrits += item
                if 'a' in lookFor:
                    lookFor = lookFor.replace("a", "a([%s]*)?"%diacrits)
                if 'e' in lookFor:
                    lookFor = lookFor.replace("e", "e([%s]*)?"%diacrits)
                if 'i' in lookFor:
                    lookFor = lookFor.replace("i", "i([%s]*)?"%diacrits)
                if 'o' in lookFor:
                    lookFor = lookFor.replace("o", "o([%s]*)?"%diacrits)
                if 'u' in lookFor:
                    lookFor = lookFor.replace("u", "u([%s]*)?"%diacrits)
        except AttributeError:
            pass
        return lookFor
        
    def removeAccents(self, lookFor):
        if 'a' in lookFor:
            lookFor = lookFor.replace("a", "(a|á)")
        if 'e' in lookFor:
            lookFor = lookFor.replace("e", "(e|é)")
        if 'i' in lookFor:
            lookFor = lookFor.replace("i", "(i|í)")
        if 'o' in lookFor:
            lookFor = lookFor.replace("o", "(o|ó)")
        if 'u' in lookFor:
            lookFor = lookFor.replace("u", "(u|ú)")
        return lookFor
        
    def setEdge(self, lookFor):
        if lookFor[0] == "#":
            lookFor = r"(\s|^)" + lookFor[1:]
        elif lookFor[-1] == "#":
            lookFor = lookFor[:-1] + r"(\s|$)"
        return lookFor        

    def makeDiacritList(self):
        if dataIndex.diacrits:
            diacritList = dataIndex.diacrits
        elif len(self.fldbk.oDiacriticsField.toPlainText()) != 0:
            diacritList = []
            diacrits = self.fldbk.oDiacriticsField.toPlainText().split(', ')
            for item in diacrits:
                diacritList.append(item.strip())
        else:
             diacritList = None
        return diacritList
        
    def searchAnalysis(self, entry, term, target):
        """this allows for searches in the interlinear glosses
        to be restricted to containment in a single wordform
        using <>. It creates two lists and for each pair from the
        list tests the target entry by calling searchElement"""
        if "<" in term[1]:
            subTerms = term[1].replace("<", "")
            subTerms = subTerms.replace(">", "")
            subTermList = subTerms.split(" ")
            newTermList = []
            for item in subTermList:
                newItem = ['a', 'b']
                newItem[0] = term[0]
                newItem[1] = item.strip()
                newTermList.append(newItem)
            targetList = target.split(' ')
            thisWordIsGood = False
            for item in targetList:
                for nTerm in newTermList:
                    hit = self.searchElement(entry, nTerm, item)
                    if hit is False:
                        thisWordIsGood = False
                        break
                    else:
                        thisWordIsGood = True
                if thisWordIsGood is True:
                    hit = True
                    break
                else:
                    hit is False
        else:
            hit = self.searchElement(entry, term, target)
        return hit
    
    def searchElement(self, entry, term, target):
        """tests the entry to see if the search term is in the target string"""
        """parameters = [accent, diacrit, case, append, recOnly, wholeWord]"""
        if target is None or target is False:
            hit = False
            return hit  
        lookFor = term[1].strip()
        if '@' in term[0]:
            if lookFor[-1] == ".":
                lookFor = lookFor.replace('.', '')       
        polarity = None
        if lookFor[0] == '¬':
            lookFor = lookFor[1:]
            polarity = 'neg'
        """perform a search that abstracts over accents"""   # parameters[0] flags accents
        if self.parameters[1] == 1: 
            """perform a search that abstracts over diacritics""" # parameters[1] flags diacrits
            lookFor = self.removeDiacrits(lookFor)
        if self.parameters[0] == 1:
            lookFor = self.removeAccents(lookFor)
        if self.parameters[5] == 1: # if whole word search
            lookFor = '(\s|^)' + lookFor + '(\s|$)'
        elif "#" in lookFor:
            lookFor = self.setEdge(lookFor)
        if self.parameters[2] == 0:  # parameters[2] flags caps
            p = QtCore.QRegularExpression(lookFor, QtCore.QRegularExpression.PatternOption.NoPatternOption)
        else:
            p = QtCore.QRegularExpression(lookFor, QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
        m = QtCore.QRegularExpressionMatch()
        m = p.match(target)
        if m.hasMatch():
            if polarity == 'neg':
                hit = False
            else:
                hit = True
        else:
            hit = False
        return hit

    def buildDisplay(self, hits):
        """display search results"""
        if self.parameters[3] != 0:
            try:
                existingModel = self.fldbk.cSearchResults.model()
                for i in range(0, existingModel.rowCount()):
                    self.resultsList.append(existingModel.item(i, 0).text())
                    self.idList.append(existingModel.item(i, 0).data(35))
            except AttributeError:
                pass
        else:
            try:
                if self.fldbk.cSearchResults.model().rowCount() != 0:
                    self.fldbk.cSearchResults.model().clear()
            except AttributeError:
                pass
        self.displayResults(hits)
        hitNumber = self.fldbk.cSearchResults.model().rowCount()
        self.fldbk.cNumberOfHits.setText('Hits: %s' %str(hitNumber))
        if len(self.findField) != 0:
            self.fldbk.cTarget.setText(self.findField)

class LexSearchEngine(SearchEngine):

    def setScope(self):
        searchList = []
        findField = ''
        XMLDict = {'lSearchSource': '@Spkr', 'lSearchResearcher': '@Rschr', 'lSearchDate': '@Date', 
                        'lSearchConfirmed': '@Confirmed', 'lSearchUpdate': '@Update',  
                        'lSearchKeywordIndex': '@Kywd', 'lSearchPrimaryIndex': '@L1Index', 
                        'lSearchSecondaryIndex': '@L2Index', 'lSearchPOS': 'POS', 'lSearchLit': 'Lit', 
                        'lDialectSearch': 'Dia', 'lSearchReg': 'Reg', 'lGrmSearch': 'Grm', 
                        'lSearchBrrw': 'Brrw', 'lL1Search': 'Def/L1', 'lL2Search': 'Def/L2', 
                        'lSearchNotes': 'Comments', 'lSearchOrth': 'Orth', 'lSearchIPA': 'IPA',  'lCfSearch': 'Cf',  'lC2Search': 'C2', 
                        'lCatSearch': '@Grm', 'lSearchDialectName': '@Dialect', 'lGrmDialectSearch': '@GrmVar', 'lC2DialectSearch': '@AltVar'}    
        userDict = {'lSearchSource': 'Source', 'lSearchResearcher': 'Researcher', 'lSearchDate': 'Date', 
                        'lSearchConfirmed': 'Confirmed', 'lSearchUpdate': 'Update',  
                        'lSearchKeywordIndex': 'Keyword', 'lSearchPrimaryIndex': 'L1 Index', 
                        'lSearchSecondaryIndex': 'L2 Index', 'lSearchPOS': 'p.o.s.', 'lSearchLit': 'Literal', 
                        'lDialectSearch': 'Dialect', 'lSearchReg': 'Register', 'lGrmSearch': 'Grammar', 
                        'lSearchBrrw': 'Borrow', 'lL1Search': 'L1', 'lL2Search': 'L2', 
                        'lSearchNotes': 'Comments', 'lSearchOrth': 'Orthography', 'lSearchIPA': 'IPA',  
                        'lCfSearch': 'Cross-references',  'lC2Search': 'Comparisons', 
                        'lCatSearch': 'Grammar', 'lSearchDialectName': 'Dialect', 'lGrmDialectSearch': 'Grammatical variant', 
                        'lC2DialectSearch': 'Dialectal restriction'}
        if len(self.scope) != 0:
            findField = self.target
            for item in self.scope:
                searchKey = item
                searchList.append([searchKey, self.target])
        else:
            fldList = self.fieldList
            for field in fldList:
                try:
                    if field.text():
                        searchKey = XMLDict[field.objectName()]
                        userKey = userDict[field.objectName()]
                        if '&' in field.text():
                            termList = field.text().split('&')
                            for term in termList:
                                searchList.append([searchKey, term.strip()])
                        else:
                            searchList.append([searchKey, field.text()])
                        if len(findField) == 0:
                            findField = field.text() + " in " + userKey
                        else:
                            findField += "; " + field.text() + " in " + userKey
                except AttributeError:
                    pass
                except KeyError:
                    pass
        return searchList,  findField

    def thumbThroughElems(self, entry, term):
        # print(entry.find('Orth').text)
        try:
            if term[0] == '@Kywd':
                """should be a contains match"""
                target = entry.attrib.get('Kywd')
                hit = self.searchElement(entry, term, target)
    
            if term[0] == '@Spkr':
                """should be an exact match"""
                target = entry.attrib.get('Spkr')
                hit = self.searchElement(entry, term, target)
    
            if term[0] == '@Rschr':
                """should be an exact match"""
                target = entry.attrib.get('Rschr')
                hit = self.searchElement(entry, term, target)
    
            if term[0] == '@Confirmed':
                """should be a contains match"""
                target = entry.attrib.get('Confirmed')
                hit = self.searchElement(entry, term, target)
    
            if term[0] == '@L1Index':
                """should be a contains match"""
                target = entry.attrib.get('L1Index')
                hit = self.searchElement(entry, term, target)
                if hit is False:
                    defList = entry.findall('Def')
                    for node in defList:
                        if node.attrib.get('L1Index') is not None:
                            target = node.attrib.get('L1Index')
                            hit = self.searchElement(entry, term, target)
    
            if term[0] == '@L2Index':
                """should be a contains match"""
                target = entry.attrib.get('L2Index')
                hit = self.searchElement(entry, term, target)
                if hit is False:
                    defList = entry.findall('Def')
                    for node in defList:
                        if node.attrib.get('L2Index') is not None:
                            target = node.attrib.get('L2Index')
                            hit = self.searchElement(entry, term, target)
                            
            if term[0] == '@Update':
                """should be a date match"""
                target = entry.attrib.get('Update')
                hit = self.searchElement(entry, term, target)
    
            if term[0] == '@Date':
                """should be a date match"""
                target = entry.attrib.get('Date')
                hit = self.searchElement(entry, term, target)
    
            if term[0] == '@Dialect':
                """search for the Dialect attribute (e.g, "get all words tagged as Pateco")"""
                dNode = entry.find('Dia')
                if dNode is not None:
                    target = entry.attrib.get('Dialect')
                    hit = self.searchElement(dNode, term, target)
                else:
                    hit = False
                """a dialect node can appear in a Def node, have to check there, too"""
                if hit is False:
                    defDiaList = entry.findall('Def/Dia')
                    if len(defDiaList) != 0:
                        for item in defDiaList:
                            if term[1] in item.attrib.get('Dialect'):
                                hit = True
                                break
            
            if term[0] == 'Alternative':
                """searches text of alternative attribute"""
                dNode = entry.find('Dia')
                if dNode is not None:
                    aNodeList = dNode.findall('Alternative')
                    if len(aNodeList) != 0:
                        for aNode in aNodeList:
                            target = aNode.text
                            hit = self.searchElement(aNode, term, target)
                            if hit is True:
                                break
                    else:
                        hit = False
                else:
                    hit = False
                """a dialect node can appear in a Def node, have to check there, too"""
                if hit is False:
                    aNodeList = entry.findall('Def/Dia/Alternative')
                    if len(aNodeList) != 0:
                        for aNode in aNodeList:
                            target = aNode.text
                            hit = self.searchElement(aNode, term, target)
                            if hit is True:
                                break  
    
            if term[0] == 'Brrw':
                """element is unique but contains an attribute @Source"""
                subentry = entry.find('Brrw')
                newKey = '@Source'
                thisTerm= [newKey,  term[1]]
                try:
                    target = subentry.attrib.get("Source")
                    hit = self.searchElement(subentry, thisTerm, target)
                except AttributeError:
                    hit = False
                if hit is False:
                    target = entry.find('Brrw').text
                    hit = self.searchElement(entry, term, target)
                
            if term[0] == '@Grm':
                prefix = term[1].strip()
                prefix = term[1].replace('.', '')
                gElementsList = entry.findall('Grm[@Prefix="%s"]' %prefix)
                if len(gElementsList) != 0:
                    hit = True
                else:
                    hit = False
                    
            if term[0] == '@GrmVar':
                variant = term[1].strip()
                gElementsList = entry.findall('Grm[@Variant="%s"]' %variant)
                if len(gElementsList) != 0:
                    hit = True
                else:
                    hit = False  
                    
            if term[0] == '@AltVar':
                variant = term[1].strip()
                gElementsList = entry.findall('C2[@Variant="%s"]' %variant)
                if len(gElementsList) != 0:
                    hit = True
                else:
                    hit = False  

            if term[0] == 'Grm':
                """element is iterable and contains text and @Prefix"""
                gElementsList = entry.findall('Grm')
                target = entry.find('Grm').text
                hit = self.searchElement(entry, term, target)
                if hit is not True:
                    for gNode in gElementsList:
                        target = gNode.text
                        hit = self.searchElement(gNode, term, target)
                        if hit is True:
                            break
                    
            if term[0] == 'POS':
                """should be a contained or exact match"""
                try: 
                    target = entry.find('POS').text
                    hit = self.searchElement(entry, term, target)
                except AttributeError:
                    hit = False
                """a POS node can appear in a Def node, have to check there, too"""
                if hit is False:
                    if entry.findall('Def/POS'):
                        defPOSList = entry.findall('Def/POS')
                        for item in defPOSList:
                            if term[1] in item.text:
                                hit = True
                                break
    
            if term[0] == 'Lit':
                """should be an exact match"""
                target = entry.find('Lit').text
                hit = self.searchElement(entry, term, target)
            
            if term[0] == 'Cf':
                """should be an exact match"""
                target = entry.find('Cf').text
                hit = self.searchElement(entry, term, target)
    
            if term[0] == 'C2':
                """should be an exact match"""
                target = entry.find('C2').text
                hit = self.searchElement(entry, term, target)
    
            if term[0] == 'Reg':
                """should be an exact match"""
                try:
                    target = entry.find('Reg').text
                    hit = self.searchElement(entry, term,  target)
                except AttributeError:
                    hit = False
                """a Reg node can appear in a Def node, have to look there, too"""
                if hit is False:
                    if entry.findall('Def/Reg'):
                        defRegList = entry.findall('Def/Reg')
                        for item in defRegList:
                            if term[1] in item.text:
                                hit = True
                                break
    
            if term[0] == 'Def/L1':
                defList = entry.findall('Def')
                for node in defList:
                    target = node.findtext('L1')
                    if node.find('Cxt') is not None:
                        context = node.findtext('Cxt')
                        target += ' [' + context.strip() + "]"                    
                    hit = self.searchElement(node, term, target)
                    if hit is True:
                        break
    
            if term[0] == 'Def/L2':
                defList = entry.findall('Def')
                for node in defList:
                    target = node.findtext('L2')
                    if node.find('Cxt') is not None:
                        context = node.findtext('Cxt')
                        target += ' [' + context.strip() + "]"
                    hit = self.searchElement(node, term,  target)
                    if hit is True:
                        break                
    
            if term[0] == 'Comments':
                """should be a contained or exact match"""
                target = entry.find('Comments').text
                hit = self.searchElement(entry, term, target)
    
            if term[0] =='Orth':
                """should be a contained or exact match"""
                target = entry.find('Orth').text
                hit = self.searchElement(entry, term, target)    
    
            if term[0] == 'IPA':
                """should be a contained or exact match"""
                target = entry.find('IPA').text
                hit = self.searchElement(entry, term, target)
                
            return hit
        except AttributeError:
            hit = False
            return hit

    def doSearch(self): 
        """searchList is the list of items being looked for; 
        findField provides text for hit results bar on the Search card"""
        searchList,  self.findField = self.setScope()
        # print(searchList, self.findField)
        hits = []
        if self.list is None:
            """scope of search is general"""
            for entry in dataIndex.root.iter('Lex'):
                if self.parameters[4] == 1:
                    rec = self.checkForRecordings(entry)
                    if rec is False:
                        continue
                """iterate through the lexicon, checking each entry"""
                for term in searchList:
                    """apply each search for X to all specified places (Ys) in the entry"""
                    hit = self.thumbThroughElems(entry, term)
                    if hit is False and self.orSwitch == 'off':
                        """if X is not in Y AND we need X in both, search next entry"""
                        break
                    elif hit is True and self.orSwitch == 'on':
                        """if X is found and we don't need it anywhere else in the same entry"""
                        break
                    if hit is True:
                        hits.append(entry)
        else:
            """scope of search is narrow"""
            for item in self.list:
                entry = dataIndex.lexDict[item]
                if self.parameters[4] == 1:
                    rec = self.checkForRecordings(entry)
                    if rec is False:
                        break
                for term in searchList:
                    """apply each search for X to all specified places (Ys) in the entry"""
                    hit = self.thumbThroughElems(entry, term)
                    if hit is False and self.orSwitch == 'off':
                        """if X is not in Y AND we need X in both, search next entry"""
                        break
                    elif hit is True and self.orSwitch == 'on':
                        """if X is found and we don't need it anywhere else in the same entry"""
                        break
                if hit is True:
                    hits.append(entry)
        self.buildDisplay(hits)
        try:
            if self.fldbk.recordBrowser:
                self.updateBrowser(self.idList, self.parameters)
        except AttributeError:
            pass   
        self.fldbk.tabWidget.setCurrentIndex(5)
        if len(hits) == 0:
            targetText = self.fldbk.cTarget.text()
            targetText = "! " + targetText
            targetText.replace('!!', '!')
            self.fldbk.cTarget.clear()
            self.fldbk.cTarget.insert(targetText)

    def displayResults(self, hits): 
        if self.fldbk.cSearchResults.model():
            hitsModel = self.fldbk.cSearchResults.model()
        else:
            hitsModel = QtGui.QStandardItemModel()
        self.resultsList = []
        self.idList = []
        resultsdict = {} 
        for hit in hits:
            if self.parameters[6] == 0:
                defText = hit.find('Def/L1').text
                if not defText:
                    defText = hit.find('Def/L2').text
            else:
                defText = hit.find('Def/L2').text
                if not defText:
                    defText = hit.find('Def/L1').text
            defText = self.formatHandler(defText)
            hitid = hit.attrib.get('LexID')
            #print(hitid)
            try:
#            if hit.find('POS').text != None:
                POS = hit.find('POS').text
            except AttributeError:
                POS = ' '
            try:
                result = "<b>" + hit.find('Orth').text + "</b> (" + POS + ") " + defText
            except AttributeError: 
                result = "<b>" + hit.find('Orth').text + "</b> " + defText        
            resultsdict[hitid] = result
        sortedMasterList = sorted(resultsdict.items(),  key=operator.itemgetter(1))
        for item in sortedMasterList:
            self.resultsList.append(item[1])
            self.idList.append(item[0])
        for i, result in enumerate(self.resultsList):
            entry = QtGui.QStandardItem()   
            entry.setText(result)
            entry.setData(self.idList[i], 35)
            hitsModel.appendRow(entry)
        self.fldbk.cSearchResults.setModel(hitsModel)


class ExSearchEngine(SearchEngine):

    def setScope(self, dialog=None):
        searchList = []
        findField = ''
        elemList = ['Line', 'Mrph', 'ILEG', 'L1Gloss', 'L2Gloss', 'Comments', '@Kywd', '@Spkr', 
                    '@Rschr', '@Date', '@Update']     
        if dialog is not None:
            fldList = [dialog.Line, dialog.Morph, dialog.ILEG, dialog.L1Gloss, 
                            dialog.L2Gloss, dialog.Comments, dialog.Keywords, 
                            dialog.Source, dialog.Researcher, dialog.Date, dialog.Updated] 
            for i, field in enumerate(fldList):
                if len(field.toPlainText()) != 0:
                    termList = field.toPlainText().split('&')
                    for term in termList:
                        searchList.append([elemList[i], term.strip()])   
            for item in searchList:
                searchTerm = item[1] + ' in ' + item[0]
                if len(findField) == 0:
                    findField = searchTerm
                else:
                    findField += ', '+ searchTerm
            findField = findField.replace("Mrph", "Morph")
            findField = findField.replace("@Kywd", "Keyword")
            findField = findField.replace("@Spkr", "Source")
            findField = findField.replace("@Rschr", "Researcher")
            findField = findField.replace("@Update", "Updated")
            findField = findField.replace("@Date", "Date")
        else:
            findField = self.target
            for item in self.scope:
                searchKey = item
                searchList.append([searchKey, self.target])

        return searchList, findField

    def formatHandler(self, theString):
        theString = theString.replace("{i}", "")
        theString = theString.replace("{/i}", "")
        return theString
        
    def setParameters(self, dialog):
        """parameters = [accent, diacrit, case, append, recOnly, wholeWord, secondLanguage]"""
        if dialog.accentBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
        if dialog.diacritBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
        if dialog.caseBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)   
        if dialog.appendBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
        if dialog.recOnlyBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
        if dialog.wholeWordBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
        if dialog.setLangBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
    
    def displayResults(self, hits, text="no"):
        if self.fldbk.cSearchResults.model():
            hitsModel = self.fldbk.cSearchResults.model()
        else:
            hitsModel = QtGui.QStandardItemModel()
        for hit in hits:
            entry = QtGui.QStandardItem()
            Line = hit.find('Line').text
            result = "<p>" + self.formatHandler(Line) + "</p>" 
            try:
                if len(hit.find('Mrph').text) != 0:
                    result += "<p>" + hit.find('Mrph').text + "</p>" + "<p>" + hit.find('ILEG').text + "</p>"
            except TypeError:
                pass
            try:
                L1Gloss = hit.find('L1Gloss').text
            except AttributeError:
                L1Gloss = None
            try:
                L2Gloss = hit.find('L2Gloss').text
            except AttributeError:
                L2Gloss = None
            if self.parameters[6] == 0:
                if L1Gloss:
                    gloss = L1Gloss
#                else:
#                    gloss = L2Gloss
                elif L2Gloss:
                    gloss = L2Gloss
                else:
                    gloss = None
            if gloss is None:
                print(etree.tostring(hit, encoding='unicode'))
            else:
                result += "<p>" + "‘" + self.formatHandler(gloss) + "’" + "</p>"
            hitsModel.appendRow(entry)
            entry.setText(result)
            if text == 'no':
                entry.setData(hit.attrib.get('ExID'), 35)
            else:
                try:
                    entry.setData(hit.attrib.get('SourceText'), 35)
                    entry.setData(hit.attrib.get('ExID'), 36)
                except AttributeError:
                    entry.setData(hit.attrib.get('ExID'), 35)
            self.idList.append(hit.attrib.get('LexID'))
        self.fldbk.cSearchResults.setModel(hitsModel)
       
    def thumbThroughElems(self, entry, term):
        try: 
            if term[0] == '@Kywd':
                """should be a contains match"""
                target = entry.attrib.get('Kywd')
                hit = self.searchElement(entry, term, target)
    
            if term[0] == '@Spkr':
                """should be an exact match"""
                target = entry.attrib.get('Spkr')
                hit = self.searchElement(entry, term, target)
    
            if term[0] == '@Rschr':
                """should be an exact match"""
                target = entry.attrib.get('Rschr')
                hit = self.searchElement(entry, term, target)       
    
            if term[0] == '@Update':
                """should be a date match"""
                target = entry.attrib.get('Update')
                hit = self.searchElement(entry, term, target)
    
            if term[0] == '@Date':
                """should be a date match"""
                target = entry.attrib.get('Date')
                hit = self.searchElement(entry, term, target)
    
            if term[0] == 'Comments':
                """should be a contained or exact match"""
                target = entry.find('Comments').text
                hit = self.searchElement(entry, term, target)
    
            if term[0] == 'Line':
                """should be a contained or exact match"""
                target = entry.find('Line').text
                target = formattingHandlers.XMLtoPlainText(target)
                hit = self.searchElement(entry, term, target) 
    
            if term[0] == 'Mrph':
                """should be a contained or exact match"""
                target = entry.find('Mrph').text
                hit = self.searchAnalysis(entry, term, target)
                    
            if term[0] == 'ILEG':
                """should be a contained or exact match"""
                target = entry.find('ILEG').text
                hit = self.searchAnalysis(entry, term, target)                          
                    
            if term[0] == 'L1Gloss':
                """should be a contained or exact match"""
                target = entry.find('L1Gloss').text
                target = formattingHandlers.XMLtoPlainText(target)
                hit = self.searchElement(entry, term, target)    
                    
            if term[0] == 'L2Gloss':
                """should be a contained or exact match"""
                target = entry.find('L2Gloss').text
                target = formattingHandlers.XMLtoPlainText(target)
                hit = self.searchElement(entry, term, target)    
            
            return hit
        except AttributeError:
            hit = False
            return hit

    def callDialog(self):
        dialog = EgSearchDialog.EgSearchDialog(self.fldbk)
        dialog.setWindowTitle('Search examples')
        return dialog
        
    def doSearch(self):
        """TODO: this does not take into account any additional Synt tiers the user defines"""
        if self.target is not None:
            """is the search being called from the Search tab? If so, """
            searchList, self.findField = self.setScope()
        else:
            """if not"""
            dialog = self.callDialog()
            if dialog.exec():
                self.setParameters(dialog)
                searchList, self.findField = self.setScope(dialog) 
                if len(searchList) == 0:
                   return 
            else:
                return
        hits = []
        if self.list is None:
            for entry in dataIndex.root.iter('Ex'):
                """iterate through examples, checking each entry"""
                if self.parameters[4] == 1:
                    rec = self.checkForRecordings(entry)
                    if rec is False:
                        continue
                for term in searchList:
                    """apply each search for X to all specified places (Ys) in the entry"""
                    hit = self.thumbThroughElems(entry, term)
                    if hit is False and self.orSwitch == 'off':
                        """if X is not in Y AND we need X in both, search next entry"""
                        break
                    elif hit is True and self.orSwitch == 'on':
                        """if X is found and we don't need it anywhere else in the same entry"""
                        break
                if hit is True:
                    hits.append(entry)
        else:
            """scope of search is narrow"""
            for item in self.list:
                entry = dataIndex.exDict[item]
                if self.parameters[4] == 1:
                    rec = self.checkForRecordings(entry)
                    if rec is False:
                        continue
                for term in searchList:
                    """apply each search for X to all specified places (Ys) in the entry"""
                    hit = self.thumbThroughElems(entry, term)
                    if hit is False and self.orSwitch == 'off':
                        """if X is not in Y AND we need X in both, search next entry"""
                        break
                    elif hit is True and self.orSwitch == 'on':
                        """if X is found and we don't need it anywhere else in the same entry"""
                        break
                if hit is True:
                    hits.append(entry)
        self.idList = []
        self.buildDisplay(hits)
        try:
            if self.fldbk.recordBrowser:
                self.updateBrowser(self.idList, self.parameters)
        except AttributeError:
            pass   
        self.fldbk.tabWidget.setCurrentIndex(5)
        if len(hits) == 0:
            targetText = self.fldbk.cTarget.text()
            targetText = "! " + targetText
            targetText.replace('!!', '!')
            self.fldbk.cTarget.clear()
            self.fldbk.cTarget.insert(targetText)


class TextSearchEngine(ExSearchEngine):

    def callDialog(self):
        dialog = TextSearchDialog.TextSearchDialog(self.fldbk)
        dialog.setWindowTitle('Search texts')
        return dialog
        
    def doSearch(self):
        if self.target is not None:
            """is the search being called from the Search tab? If so, """
            searchList, self.findField = self.setScope()
        else:
            dialog = self.callDialog()
            if dialog.exec():
                if dialog.limitBtn.isChecked():
                    self.list = dataIndex.textDict[dataIndex.currentCard]
                else:
                    self.list = None                
                self.setParameters(dialog)
                searchList, self.findField = self.setScope(dialog)
                if len(searchList) == 0:
                    return
            else:
                return
        hits = []
        hit = False            
        textList = []
        if self.list is None:
            """if we are not limited to a specific list text"""
            for item in dataIndex.root.iter('Text'):
                textList.append(item)
        else:
            """search only current text (will this work for narrow searches, too?)"""
            textList.append(self.list)
        lineList = []
        for text in textList:
            """get the IDs of the Ex nodes that make up the text(s)"""
            for line in text.iter('Ln'):
                lineList.append(line)
        domain = []
        for line in lineList:
            """get the nodes you want to search from the ExDictionary"""
            domain.append(dataIndex.exDict[line.get('LnRef')])
        for entry in domain:
            """iterate through the nodes, checking each example"""
            for term in searchList:
                """apply each search for X to all specified places (Ys) in the example"""
                hit = self.thumbThroughElems(entry, term)
                if hit is False and self.orSwitch == 'off':
                    """if X is not in Y AND we need X in both, search next entry"""
                    break
                elif hit is True and self.orSwitch == 'on':
                    """if X is found and we don't need it anywhere else in the same entry"""
                    break
            if hit is True:
                hits.append(entry)
                hit = False
        self.idList = []
        self.buildDisplay(hits)
        try:
            if self.fldbk.recordBrowser:
                self.updateBrowser(self.idList, self.parameters)
        except AttributeError:
            pass
        self.fldbk.tabWidget.setCurrentIndex(5)
        if len(hits) == 0:
            targetText = self.fldbk.cTarget.text()
            targetText = "! " + targetText
            targetText.replace('!!', '!')
            self.fldbk.cTarget.clear()
            self.fldbk.cTarget.insert(targetText)

    def setParameters(self, dialog):
        """parameters = [accent, diacrit, case, append, recOnly, wholeWord, secondLanguage]"""
        if dialog.accentBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
        if dialog.diacritBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
        if dialog.caseBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)   
        if dialog.appendBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
        self.parameters.append(0)
        if dialog.wholeWordBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
        if dialog.setLangBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
            
class DSetSearchEngine(SearchEngine):
    
    def callDialog(self):
        dialog = DSetSearchDialog.DSetSearchDialog(self.fldbk)
        dialog.setWindowTitle('Search datasets')
        return dialog
        
    def setParameters(self, dialog):
        """parameters = [accent, diacrit, case, append, recOnly, wholeWord]"""
        if dialog.accentBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
        if dialog.diacritBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
        if dialog.caseBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)   
        if dialog.appendBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
        if dialog.recOnlyBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
        if dialog.wholeWordBtn.isChecked():
            self.parameters.append(1)
        else:
            self.parameters.append(0)
    
    def setScope(self, dialog=None):
        searchList = []
        findField = ''
        elemList = ['Data', 'Comments', '@Kywd', '@Spkr', '@Rschr', '@Date', '@Update']
        if dialog is not None:
            fldList = [dialog.SearchText, dialog.Comments, dialog.Keywords, 
                        dialog.Source, dialog.Researcher, dialog.Date, dialog.Updated]
            for i, field in enumerate(fldList):
                if len(field.toPlainText()) != 0:
                    termList = field.toPlainText().split('&')
                    for term in termList:
                        searchList.append([elemList[i], term.strip()])
            for item in searchList:
                searchTerm = item[1] + ' in ' + item[0]
                if len(findField) == 0:
                    findField = searchTerm
                else:
                    findField += ', '+ searchTerm
            findField = findField.replace("@Kywd", "Keyword")
            findField = findField.replace("@Spkr", "Source")
            findField = findField.replace("@Rschr", "Researcher")
            findField = findField.replace("@Update", "Updated")
            findField = findField.replace("@Date", "Date")
        else:
            findField = self.target
            for item in self.scope:
                searchKey = item
                searchList.append([searchKey, self.target])
        return searchList, findField
        
    def displayResults(self, hits): 
        if self.fldbk.cSearchResults.model():
            hitsModel = self.fldbk.cSearchResults.model()
        else:
            hitsModel = QtGui.QStandardItemModel()
        for hit in hits:
            entry = QtGui.QStandardItem()
            defText = self.formatHandler(hit.find('Title').text)
            entry.setText(defText)
            entry.setData(hit.attrib.get('DsetID'), 35)
            hitsModel.appendRow(entry)
            self.idList.append(hit.attrib.get('LexID'))
        self.fldbk.cSearchResults.setModel(hitsModel)

    def thumbThroughElems(self, entry, term):
        try: 
            if term[0] == '@Kywd':
                """should be a contains match"""
                target = entry.attrib.get('Kywd')
                hit = self.searchElement(entry, term, target)
    
            if term[0] == '@Spkr':
                """should be an exact match"""
                target = entry.attrib.get('Spkr')
                hit = self.searchElement(entry, term, target)
    
            if term[0] == '@Rschr':
                """should be an exact match"""
                target = entry.attrib.get('Rschr')
                hit = self.searchElement(entry, term, target)      
    
            if term[0] == '@Update':
                """should be a date match"""
                target = entry.attrib.get('Update')
                hit = self.searchElement(entry, term, target)
    
            if term[0] == '@Date':
                """should be a date match"""
                target = entry.attrib.get('Date')
                hit = self.searchElement(entry, term, target)
    
            if term[0] == 'Comments':
                """should be a contained or exact match"""
                target = entry.find('Comments').text
                hit = self.searchElement(entry, term, target) 
    
            if term[0] == 'Data':
                """should be a contained or exact match"""
                target = entry.find('Data').text
                hit = self.searchElement(entry, term, target)
            
            return hit
        except AttributeError:
            hit = False
            return hit
 
    def doSearch(self):
        dsetOnlyBtns.removeHiliting(self.fldbk)
        if self.target is not None:
            """is the search being called from the Search tab? If so, """
            searchList, self.findField = self.setScope()
        else:
            dialog = self.callDialog()
            if dialog.exec():
                self.setParameters(dialog)
                searchList, self.findField = self.setScope(dialog)
                if len(searchList) == 0:
                    return
                if dialog.limitBtn.isChecked():
                    self.findInField(dialog.SearchText.toPlainText(), self.parameters)
                    return
            else:
                return
        hits = []
        if self.list is None:
            """scope of the search is general"""
            for entry in dataIndex.root.iter('Dset'):
                """iterate through examples, checking each entry"""
                if self.parameters[4] == 1:
                    rec = self.checkForRecordings(entry)
                    if rec is False:
                        continue
                for term in searchList:
                    """apply each search for X to all specified places (Ys) in the entry"""
                    hit = self.thumbThroughElems(entry, term)
                    if hit is False and self.orSwitch == 'off':
                        """if X is not in Y AND we need X in both, search next entry"""
                        break
                    elif hit is True and self.orSwitch == 'on':
                        """if X is found and we don't need it anywhere else in the same entry"""
                        break
                if hit is True:
                    hits.append(entry)
                    hit = False
        else:
            """scope of the search is narrow"""
            for item in self.list:
                entry = dataIndex.dataDict[item]
                if self.parameters[4] == 1:
                    rec = self.checkForRecordings(entry)
                    if rec is False:
                        continue
                for term in searchList:
                    """apply each search for X to all specified places (Ys) in the entry"""
                    hit = self.thumbThroughElems(entry, term)
                    if hit is False and self.orSwitch == 'off':
                        """if X is not in Y AND we need X in both, search next entry"""
                        break
                    elif hit is True and self.orSwitch == 'on':
                        """if X is found and we don't need it anywhere else in the same entry"""
                        break
                if hit is True:
                    hits.append(entry)            
        self.idList = []
        self.buildDisplay(hits)
        try:
            if self.fldbk.recordBrowser:
                self.updateBrowser(self.idList, self.parameters)
        except AttributeError:
            pass   
        self.fldbk.tabWidget.setCurrentIndex(5)
        if len(hits) == 0:
            targetText = self.fldbk.cTarget.text()
            targetText = "! " + targetText
            targetText.replace('!!', '!')
            self.fldbk.cTarget.clear()
            self.fldbk.cTarget.insert(targetText)

    def findInField(self, lookFor, parameters):
        cursor = self.fldbk.dData.textCursor()
        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QBrush(QtGui.QColor("yellow")))
        if parameters[0] == 1:
            lookFor = self.removeAccents(lookFor)
        if parameters[1] == 1:
            lookFor = self.removeDiacrits(lookFor)
        if "#" in lookFor:
            lookFor = self.setEdge(lookFor)
        if parameters[2] == 0:
            regex = QtCore.QRegularExpression(lookFor, QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
        else:
            regex = QtCore.QRegularExpression(lookFor)
        pos = 0
        index = QtCore.QRegularExpressionMatch()
        dataset = self.fldbk.dData.toPlainText()
        index = regex.match(dataset, pos)
        while index.hasMatch():
            cursor.setPosition(index.capturedStart())
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfBlock)
            cursor.movePosition(QtGui.QTextCursor.MoveOperation.EndOfBlock, QtGui.QTextCursor.MoveMode.KeepAnchor)
            cursor.mergeCharFormat(format)
            pos = index.capturedStart() + len(index.captured())
            index = regex.match(dataset, pos)


class SearchLexFromCard(LexSearchEngine):
    
    def __init__(self, parent):
        self.parameters = []
        
