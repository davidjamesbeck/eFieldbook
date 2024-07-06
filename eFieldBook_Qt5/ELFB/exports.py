"""codes for getting stuff out of the database"""

from ELFB import dataIndex
from yattag import *
from ELFB import cardLoader
#from xml.etree import ElementTree as etree

class LexNodeObject():
    
    def __init__(self):
        #elements
        self.fldbk = dataIndex.fldbk
        self.orth = None
        self.POS = None
        self.IPA = None
        self.Grm = []
        self.C2 = []
        self.Cf = []
        self.Reg = None
        self.Dia = None
        self.Brrw = None
        self.PhKey = None
        self.lit = None
        self.definition = None
        self.drvn = None
        self.root = None
        self.comments = None
        self.definitions = []
        
        # attributes
        self.lexiconID = None
        self.entrySpkr = None
        self.kywd = None
        self.L1Index = None

    def findDefinition(self, node):
        defsList = node.findall("Def")
        definitionsList = []
        for defn in defsList:
            definition = Definition()
            definition.makeDefinition(defn)
            definitionsList.append(definition)
        return definitionsList
        
    def makeGrm(self, node):
        grmList = node.findall("Grm")
        if len(grmList) == 0:
            return []
#        print(etree.tostring(grmList[0],  encoding='unicode'))        
        grammarPoints = []
        for item in grmList:
            attribs = item.attrib
            form = item.text
            if len(attribs) != 0:
#                print(attribs["Prefix"])
                prefix = attribs["Prefix"]
                gram = "[" + prefix + "] " + form
            else:
                gram = form
            grammarPoints.append(gram)
        return grammarPoints
        
    def makeC2(self, node):
        C2List = node.findall("C2")
        if len(C2List) == 0:
            return []
#        print(etree.tostring(C2List[0],  encoding='unicode'))
        C2s = []
        for item in C2List:
            form = item.text
            form = "<i>" + form + "</i>"
            C2s.append(form)
        return C2s
        
    def makeCf(self, node):
        CfList = node.findall("Cf")
        if len(CfList) == 0:
            return []
#        print(etree.tostring(CfList[0],  encoding='unicode'))
        Cfs = []
        for item in CfList:
            form = item.text
            form = "<i>" + form + "</i>"
            Cfs.append(form)
        return Cfs
            
class Definition():
    
    def __init__(self):
        self.defIndex = None
        self.defL1Index = None
        self.defL2Index = None
        self.defPOS = None
        self.defReg = None
        self.defL1 = None
        self.defCxt = None
        self.examples = []
        
    def makeDefinition(self, defn):
#        print(etree.tostring(defn,  encoding='unicode'))
        self.defIndex = defn.attrib.get("Index")
        self.defL1Index = defn.attrib.get("L1Index")
        self.defL2Index = defn.attrib.get("L2Index")
        self.defPOS = defn.attrib.get("POS")
        self.defReg = defn.attrib.get("Reg")
        self.defL1 = defn.findtext("L1")
        self.defCxt = defn.attrib.get("Cxt")
        exampleList = defn.findall("Ln")
        self.examples = self.findExamples(exampleList)
            
    def findExamples(self, exampleList):
        lines = []
        for item in exampleList:
            targetID = item.attrib.get("LnRef")
            example = dataIndex.exDict[targetID]
            transcript = example.findtext("Line")
            translation = example.findtext("L1Gloss")
            source = example.attrib.get("Spkr")
            line = "<i>" + transcript + "</i> ‘" + translation + "’ <small>(" + source + ")</small>. "
            lines.append(line)
        return lines

def sayHello():
    print("Outputting Josh’s database to text")
    fldbk = dataIndex.fldbk
    if fldbk.tabWidget.currentIndex() != 1:  # Lexicon tab
        data = dataIndex.lastLex
        dataIndex.currentCard = data
        targetCard = dataIndex.lexDict[data]
        cardLoader.loadLexCard(targetCard)
        dataIndex.unsavedEdit = 0
        fldbk.tabWidget.setCurrentIndex(1)
    navModel = fldbk.lLexNav.model()
    LexList = []
    dictionaryEntries = []
    for i in range(0, navModel.rowCount()):
        LexID = navModel.index(i, 0).data(32)
        LexList.append(LexID)
    for ID in LexList:
        lexEntry = LexNodeObject()
        node = dataIndex.lexDict[ID]
        if node.attrib.get("Confirmed") != "C":
            continue
        lexEntry.orth = node.findtext("Orth")
        lexEntry.POS = node.findtext("POS")
        lexEntry.IPA = node.findtext("IPA")
        lexEntry.Grm = lexEntry.makeGrm(node) #returns list of strings, empty list if no nodes
        lexEntry.C2 = lexEntry.makeC2(node)  #returns list of strings, empty list if no nodes
        lexEntry.Cf = lexEntry.makeCf(node)  #returns list of strings, empty list if no nodes
        lexEntry.Reg = node.findtext("Reg")
        dialectNode = node.find("Dia")
        if dialectNode != None:
            lexEntry.Dia = dialectNode.attrib.get('Dialect') 
        lexEntry.Brrw = node.findtext("Brrw")
        lexEntry.PhKey = node.findtext("PhKey")
        lexEntry.lit = node.findtext("Lit")
        lexEntry.drvn = node.findtext("Drvn")
        lexEntry.root = node.findtext("Root")
        lexEntry.comments = node.findtext("Comments")
        # attributes
        lexEntry.entrySpkr = node.attrib.get("Spkr")
        lexEntry.kywd = node.attrib.get("Kywd")
        lexEntry.L1Index = node.attrib.get("L1Index")
        lexEntry.L2Index = node.attrib.get("L2Index")
        # Definitions objects
        lexEntry.definitions = lexEntry.findDefinition(node)
        dictionaryEntries.append(lexEntry)
    
    dictDoc = Doc()
    dictDoc.asis('<!DOCTYPE html>')
    with dictDoc.tag('html'):
        with dictDoc.tag('head'):
            dictDoc.asis('<meta charset="UTF-8"/>')
        with dictDoc.tag('body'):
            with dictDoc.tag('h2'):
                dictDoc.asis('Dene–English')
            dictDoc.asis(buildEntries(dictionaryEntries))
            with dictDoc.tag('h2'):
                dictDoc.asis('English-Dene')
            dictDoc.asis(buildEnglish(dictionaryEntries))
    fname = dataIndex.homePath + '/Documents/Output.html'
    saveFile = open(fname, "w", encoding="UTF-8")
    saveFile.write(dictDoc.getvalue())
    saveFile.close()
    print("all done")
    
def buildEntries(entries):
#    print('building')
    entryDoc = Doc()
    for entry in entries:
#        print('working on ',  entry.orth)
        with entryDoc.tag('p'):
            with entryDoc.tag('b'):
                entryDoc.asis(entry.orth)
                entryDoc.asis('&nbsp;')
            if len(entry.C2) != 0:
#                print(entry.orth, "C2 is", entry.C2)
                with entryDoc.tag('i'):
                    entryDoc.asis('also')
                entryDoc.asis('&nbsp;')
                with entryDoc.tag('b'):
                    alternatives = ', '.join(entry.C2)
                    entryDoc.asis(alternatives)
                entryDoc.asis('&nbsp;')
            if entry.POS != None:
                entryDoc.asis('(')
                with entryDoc.tag('i'):
                    entryDoc.asis(entry.POS)
                entryDoc.asis(')&nbsp;')
            if entry.entrySpkr != None:
                with entryDoc.tag('small'):
#                    print(entry.orth, "speaker is", entry.entrySpkr)
                    entryDoc.asis(entry.entrySpkr)
            entryDoc.asis('&nbsp;')
            entryDoc.asis(getDefs(entry))
#            print('got defs')
            if len(entry.Grm) != 0:
                entryDoc.asis('&nbsp;|&nbsp;Verb forms:&nbsp;')
                grammar = ', '.join(entry.Grm)
#                print("grammar is",grammar)
                entryDoc.asis(grammar)
#                print('put grammar in doc')
    print('finishing up building entries')
    HTML = entryDoc.getvalue()
    print('got values')
    return HTML
    
def getDefs(entry):
#    print('entering getDefs')
    dfnsList = entry.definitions
#    print(entry.orth,  dfnsList)
    defsDoc = Doc()
    for dfn in dfnsList:
        if len(dfnsList) > 1:
            defsDoc.asis(dfn.defIndex)
            defsDoc.asis('.&nbsp;')
        if dfn.defReg != None:
            with defsDoc.tag('i'):
                defsDoc.asis(dfn.defReg)
            defsDoc.asis('&nbsp;')
#        print('getting definition', dfn.defL1)
        if dfn.defL1 == None:
            dfn.defL1 = "MISSING"
        else:
            defsDoc.asis(dfn.defL1)
            defsDoc.asis('&nbsp;')
#        print('got definition')
        if len(dfn.examples) != 0:
#            print('getting examples')
            for eg in dfn.examples:
                defsDoc.asis('&nbsp;')
                defsDoc.asis(eg)
#    print('finishing defs')
    HTML = defsDoc.getvalue()
    return HTML

def buildEnglish(entries):
    print('entering buildEnglish')
    engDoc = Doc()
    for entry in entries:
        keyList = None
        if entry.kywd != None and len(entry.kywd) != 0:
            keyList = entry.kywd.split(';')
        for dfn in entry.definitions:
            if dfn.defL1Index != None:
                if keyList == None:
                    keyList = []
#                print('getting L1Index',  entry.orth)
                indList = dfn.defL1Index.split(';')
                keyList.extend(indList) 
        if keyList != None:
            for kywd in keyList:
                with engDoc.tag('p'):
                    with engDoc.tag('b'):
                        engDoc.asis(kywd)
                    engDoc.asis('&nbsp;')
                    if entry.POS != None:
                        engDoc.asis("(")
                        engDoc.asis(entry.POS)
                        engDoc.asis(')&nbsp;')
                    engDoc.asis(entry.orth)
                    engDoc.asis('&nbsp;(')
                    if entry.POS != None:
                        engDoc.asis(entry.POS)
                        engDoc.asis(')')
    HTML = engDoc.getvalue()
    return HTML


def outputLexiconToCSV(fldbk):
    print('entering outputLexiconToCSV')
    return
    if fldbk.tabWidget.currentIndex() == 1:  # Lexicon tab
        navModel = fldbk.lLexNav.model()
        LexList = []
        for i in range(0, navModel.rowCount()):
            LexID = navModel.index(i, 0).data(32)
            LexList.append(LexID)
        forms = ''
        for ID in LexList:
            node = dataIndex.lexDict[ID]
            entry = node.findtext("Orth")
            entry += ", " + node.findtext("Def/L1")
            entry += ", " + node.attrib.get('Update') + '\n'
            forms += entry
        saveFile = open('/Users/David/Desktop/CSVOutput.txt', "w", encoding="UTF-8")
        saveFile.write(forms)
        saveFile.close()
