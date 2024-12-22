"""codes for getting stuff out of the database"""
from PyQt6 import QtWidgets
from ELFB import dataIndex
from yattag import *
from ELFB.palettes import SelectOutputSchema
import re
#from ELFB import cardLoader
#from xml.etree import ElementTree as etree

class LexNodeObject():
    
    def __init__(self, node):
        #elements
        self.fldbk = dataIndex.fldbk
        self.orth = node.findtext("Orth")
        self.POS = node.findtext("POS")
        self.IPA = node.findtext("IPA")
        self.Grm = self.makeGrm(node) #returns list of strings, None if absent
        self.C2 = self.makeC2(node)  #returns list of strings, None if absent
        self.Cf = self.makeCf(node)  #returns list of strings, None if absent
        self.Reg = node.findtext("Reg")
        self.Dia = self.findDialect(node) #returns list [Dialect, Variant, Altform] or None if absent
        self.Brrw = node.findtext("Brrw")
        self.PhKey = node.findtext("PhKey")
        self.lit = node.findtext("Lit")
        self.definition = self.findDefinition(node) #returns list of Definition objects
#        self.drvn = node.findtext("Drvn") #<Drvn> has attrib LexID, iterable element
        self.root = node.findtext("Root") #<Root> has attrib LexID, unique element
        self.comments = node.findtext("Comments")
        self.definitions = self.findDefinition(node)
        
        # attributes
        self.lexID = node.attrib.get("LexID")
        self.entrySpkr = node.attrib.get("Spkr")
        self.kywd = node.attrib.get("Kywd")
        self.L1Index = node.attrib.get("L1Index")
        self.L2Index = node.attrib.get("L2Index")
        self.Done = node.attrib.get("Done")
        
        # firstletter
        self.firstletter = self.findFirstLetter()
        
    def findFirstLetter(self):
#        print('finding first letter')
        sortKey = dataIndex.root.findtext("SortKey")
        longList = sortKey.split('; ')
        interimList = longList[0].split(', ')
        sortList = sorted(interimList, key=lambda s: len(s),  reverse=True)
#        print(sortList)
        for item in sortList:
            if item == "*":
                return '*'
            if re.match(item, self.orth):
                return item
        print("You might be missing a letter in your alphabet -- %s!!!" %self.orth[0])
        return self.orth[0]

    def findRoot(self, node):
        if node.find("Root"):
            rootNode = node.find("Root")
            rootID = rootNode.attrib.get("LexID")
        else:
            return None
        root = dataIndex.lexDict[rootID].findtext("Orth")
        return root

    def findDialect(self, node):
        dialectNode = node.find("Dia")
        dia = []
        if dialectNode != None:
            dia.append(dialectNode.attrib.get('Dialect'))
        else:
            return None
        altNode = dialectNode.find('Alternative')
        if altNode != None:
            dia.append(altNode.attrib.get('Variant'))
            dia.append(altNode.text)
        return dia

    def findDefinition(self, node):
        '''called by LexObject constructor, makes list of definition object for all senses'''
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
            return None
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
#        print(grammarPoints)
        return grammarPoints
        
    def makeC2(self, node):
        C2List = node.findall("C2")
        if len(C2List) == 0:
            return None
#        print(etree.tostring(C2List[0],  encoding='unicode'))
        C2s = []
        for item in C2List:
            form = item.text
#            form = "<i>" + form + "</i>"
            C2s.append(form)
        return C2s
        
    def makeCf(self, node):
        CfList = node.findall("Cf")
        if len(CfList) == 0:
            return None
#        print(etree.tostring(CfList[0],  encoding='unicode'))
        Cfs = []
        for item in CfList:
            form = item.text
#            form = "<i>" + form + "</i>"
            Cfs.append(form)
        return Cfs
            
class Definition():
    
    def __init__(self):
        self.defIndex = None #sense number
        self.defL1Index = None #possible English index keyword
        self.defL2Index = None #possible Spanish index keyword
        self.defPOS = None
        self.defReg = None
        self.defDia = None
        self.defL1 = None
        self.defL2 = None
        self.defCxt = None
        self.L1examples = []
        self.L2examples = []

        
    def makeDefinition(self, defn):
#        print('checking',  etree.tostring(defn,  encoding='unicode'))
        self.defIndex = defn.attrib.get("Index")
        if defn.attrib.get("L1Index") != None:
            self.defL1Index = defn.attrib.get("L1Index").replace('\n',  ' ')
        else: 
            self.defL1Index = defn.attrib.get("L1Index")
        if defn.attrib.get("L2Index") != None:
            self.defL2Index = defn.attrib.get("L2Index").replace('\n',  ' ')
        else:
            self.defL2Index = defn.attrib.get("L2Index")
        self.defPOS = defn.findtext("POS")
        self.defReg = defn.findtext("Reg")
        self.defL1 = defn.findtext("L1")
        self.defL2 = defn.findtext("L2")
        self.defCxt = defn.findtext("Cxt")
        exampleList = defn.findall("Ln")
        self.L1examples, self.L2examples = self.findExamples(exampleList)
            
    def findExamples(self, exampleList):
        L1lines = []
        L2lines = []
        for item in exampleList:
            targetID = item.attrib.get("LnRef")
#            print(targetID)
            example = dataIndex.exDict[targetID]
            transcript = example.findtext("Line")
#            print(transcript)
            L1 = example.findtext("L1Gloss")
            if len(L1) == 0 or L1 == None:
                L1 = example.findtext("L2Gloss")
            L1translation = self.fixCapitalization(L1)
            source = example.attrib.get("Spkr")
            L1line = "<i>" + transcript + "</i> ‘" + L1translation + ".’ <small>(" + source + ")</small> "
            L1lines.append(L1line)
            L2 = example.findtext("L2Gloss")
            if L2 == None or len(L2) == 0:
                L2line = "<i>" + transcript + "</i> ‘" + L1translation + ".’"  
            else:
                L2translation = self.fixCapitalization(L2)
                L2line = "<i>" + transcript + "</i> ‘" + L2translation + ".’"
#                    print(L2line)
            L2lines.append(L2line)
        return L1lines, L2lines

    def secondSentence(self, line, chr):
        '''this might have to be modified eventually for multiple second sentences?'''
        quotes = r'’”"'
        n = line.index(chr)
        if line[n+1] in quotes:
            newline = line
        else:
            newline = line[:n+2] + line[n+2].upper() + line[n+3:]
        return newline

    def capString(self, line, n):
        if n == 0:
             secondPass = line[:n+1] + line[n+1].upper() + line[n+2:]
        elif line[n-2] == ',':
            secondPass = line
        else:
            secondPass = line[:n+1] + line[n+1].upper() + line[n+2:]
        return secondPass

    def fixCapitalization(self, text):
        '''add capital letters'''
        quotes = r'“‘"'
        if text[0] in quotes:
            firstPass = text[0] + text[1].upper() + text[2:]
        else:
            firstPass = text[0].upper() + text[1:]
            '''hack to capitalize after Spanish initial punctuation'''
        if '¿' in firstPass:
            indexlist = [i for i, ltr in enumerate(firstPass) if ltr == '¿']
            secondPass = firstPass
            for index in indexlist:
                secondPass = self.capString(secondPass,index)
            if secondPass.index('?') != len(secondPass) - 1:
                secondPass = self.secondSentence(secondPass,'?')
#                print(secondPass)
        else:
            secondPass = firstPass
        if '¡' in secondPass:
            indexlist = [i for i, ltr in enumerate(secondPass) if ltr == '¡']
            newtext = secondPass
            for index in indexlist:
                newtext = self.capString(newtext,index)
            if newtext.index('!') != len(newtext) - 1:
                newtext = self.secondSentence(newtext,'!')
#                print(newtext)
        else:
            newtext = secondPass
        return newtext
    
def selectSchema(fldbk):
    print('entering selectSchema')
    schemaSelector = SelectOutputSchema.SelectOutputSchema(fldbk)
    if schemaSelector.exec():
        selectedSchema = schemaSelector.schema
        print('the schema is', selectedSchema)
    else:
        return
    fldbk = dataIndex.fldbk

    if selectedSchema == 'DeneDict':
        DeneDict(fldbk)
    elif selectedSchema == 'DictLatexSpan':
        UNTLatexSpan(fldbk)

'''BEGIN UNT Latex Spanish Dictionary'''

def UNTLatexSpan(fldbk):
    print('entering UNTLatexSpan')
    lexDict = dataIndex.lexDict
    LexList = []
    navModel = fldbk.lLexNav.model()
    for i in range(0, navModel.rowCount()):
        LexID = navModel.index(i, 0).data(32)
        LexList.append(LexID)
    print("preparing to write LaTEX code")
    UNTLatexDict = makePreamble()
    UNTLatexDict += '\n' + r'\begin{document}\raggedright \raggedbottom' + '\n'
    firstLetter = ''
    i = 0
    small = r'{\raisebox{2pt}{\scriptsize{$\diamondsuit$}}}'
    for ID in LexList:
        entry = LexNodeObject(lexDict[ID])
#        print('processing ',  entry.lexID, entry.orth)
        if entry.firstletter == '-' or entry.firstletter == '*':
            continue
#        if entry.Done != '1':
#            print(entry.orth)
#            continue
        if firstLetter != removeDiacrits(entry.firstletter).upper():
            if firstLetter == '':
                firstLetter = removeDiacrits(entry.firstletter).upper()
                UNTLatexDict += r'\section*{%s %s %s}'%(small, firstLetter,  small) + '\n'
                UNTLatexDict += r'\begin{hangparas}{.20in}{1}' + '\n'
            else:
                firstLetter = removeDiacrits(entry.firstletter).upper()
                UNTLatexDict += r'\end{hangparas}' + '\n'
                UNTLatexDict += r'\newpage'+ '\n' + r'\section*{%s %s %s}'%(small, firstLetter,  small) + '\n'
                UNTLatexDict += r'\begin{hangparas}{.20in}{1}'
                i = 0
#        else:
#            i = i + 1
#            if i > 60:
#                continue
        '''gather entry components'''
        '''orthography'''
        ORTH = cleanUp(entry.orth)
        '''POS'''
        POS = '(' + hispanizePOS(entry.POS) +') '
        '''dialect'''
        if entry.Dia != None:
            diaString = '<i>' + entry.Dia[0] + '</i> '
            if len(entry.Dia) == 3:
                diaString += '(' + entry.Dia[1] + ' <i>' + entry.Dia[2] +'</i>) '
        else:
            diaString = ''
        '''grammar notes'''
        if entry.Grm != None:
            GRM = getGrm(entry.Grm)
        else:
            GRM = ''
        '''alternate forms'''
        if entry.C2 != None:
            alternatives = ", ".join(entry.C2)
            if "(" in alternatives:
                n = alternatives.index('(')
            else:
                n = len(alternatives)+1
            C2 = '<small><i>t. %s</i></small> ' %alternatives[:n-1]
        else:
            C2 = ''
        '''definitions'''
        definitions = formatDefinitions(entry.definitions)
        fullEntry = POS + diaString + C2 + GRM + definitions
        fullEntry = cleanUp(fullEntry)
        #make Latex entry
        UNTLatexDict += r'\entry{%s}{%s}' %(ORTH, fullEntry) + '\n'

    leadOut = r'\end{hangparas}' + '\n'
    leadOut += '	%------------------------------------------------' + '\n'
    leadOut += r'\end{document}' + '\n'
    UNTLatexDict += leadOut
#    print(UNTLatexDict)
    parent = None
    openFileDialog = QtWidgets.QFileDialog(fldbk)
    fname = openFileDialog.getSaveFileName(parent, "Save As...", "/Users/David/Documents/Latex_sandbox/UNTDict25")[0]
    if fname:
        with open(fname,  'w', encoding="utf-8") as file:
            file.write(UNTLatexDict)

def cleanUp(text):  
    '''add Latex italics/small'''
    if '{i}' in text:
        text = text.replace('{i}', '<i>')
        text = text.replace('{/i}', '</i>')
    if '<i>' in text:
        text = text.replace('<i>', r'\textit{')
        text = text.replace('</i>', '}')
    if '<small>' in text:
        text = text.replace('<small>', r'{\small ')
        text = text.replace('</small>', '}')
    '''add special characters'''
    text = text.replace("' ", r'\textquotesingle \textcolor{white}{n}')
    text = text.replace("'", r'\textquotesingle ')
    text = text.replace("$", r'\$')
    text = text.replace("&", r'\&')
    return text

def formatDefinitions(dfnList):
#    print('entering formatDefinitions')
    definition = ''
    for dfn in dfnList:
        if len(dfnList) == 1:
            entryText = getExamples(dfn.L2examples, dfn.defL2)
            definition += entryText + '; ' 
        else: 
            index = dfn.defIndex
            entryText = getExamples(dfn.L2examples, dfn.defL2)
            definition += index + ") " + dfn.defL2 + "; "
    definition = definition[:-2]
    return definition
    
def formatClf(tail):
    '''formats classifier'''
    newTail = ''
    clfList = tail.split('), ')
    if len(clfList) == 1:
        newTail += '<i>' + clfList[0] + '</i>'
    else:
        midTail = ''
        for form in clfList:
            n = form.index('(') 
            midTail += '<i>' + form[:n-1] + '</i> ' + form[n:] + r'), '
        newTail = midTail[:-3]
    newTail = translate(newTail)
#    print(newTail)
    return newTail

def getGrm(grm):
    '''format grammatical info'''
    grmNotes = ''
    clfEntry = ''
    plEntry = ''
    for item in grm:
        if "[clf]" in item:
            if item == '[clf] *clf.':
                clfEntry += 'clf. *clf.'
            else:
                clfEntry += 'clf. '
                tail = formatClf(item[6:])
                clfEntry += tail
#                print(clfEntry)
        if "[pl]" in item:
            if item == '[pl] *pl.':
                plEntry += 'pl. *pl.'
            else:    
                plEntry += 'pl. <i>'                
                plEntry += item[5:] + '</i>'
#            print(plEntry)
    if len(clfEntry) != 0:
        grmNotes = '<small>[' + clfEntry
        if len(plEntry) != 0:
            grmNotes += '; ' + plEntry + ']</small> '
        else:
            grmNotes += ']</small> '
    elif len(plEntry) != 0:
        grmNotes = '<small>[' + plEntry + ']</small> '
#    print(grmNotes)
    return grmNotes

def getExamples(examples, entryText):
    '''examples is the list of examples from the Definition object; these are already 
    extracted and formatted. entryText starts out as the text of the definition'''
    if len(examples) != 0:
        for eg in examples:
            entryText += r' \ding{71} ' + eg
        
    return entryText

def hispanizePOS(POS):
#    print('entering hispanizePOS')
    if POS == 'n':
        POS = 's'
    elif POS == 'idph':
        POS = 'idpf'
    elif POS == 'ni':
        POS = 'si'
    elif POS == 'vs':
        POS = 've'    
    elif POS == 'vst':
        POS = 'vet'    
    elif POS == 'dynadv':
        POS = 'advdin'    
    return POS

def removeDiacrits(letter):
#    print('removing diacrits from letter')
    letter = letter.replace(':', '')
    letter = letter.replace("'", "")
    letter = letter.replace('=', '')
    return letter

def makePreamble():
    print('entering makePreamble')
    preamble = r'''%----------------------------------------------------------------------------------------
%	PACKAGES AND OTHER DOCUMENT CONFIGURATIONS
%----------------------------------------------------------------------------------------

\documentclass[11pt,a4paper,twoside]{article} % 11pt font size, A4 paper and two-sided margins

\usepackage[top=3.5cm,bottom=3.5cm,left=3.7cm,right=4.7cm,columnsep=30pt]{geometry} % Document margins and spacings
\usepackage{pifont}
\usepackage[spanish]{babel}
\usepackage[utf8x]{inputenc} % Required for inputting international characters
\usepackage[T1]{fontenc} % Output font encoding for international characters
\usepackage{textcomp}
\usepackage{mathptmx} % Use the Times New Roman font
\frenchspacing
\usepackage{xcolor}
\usepackage{microtype} % Improves spacing
\usepackage{hanging}
\usepackage[bf,rm,center]{titlesec} % Required for modifying section titles - bold, sans-serif, centered
\usepackage[all]{nowidow}
\usepackage{fancyhdr} % Required for modifying headers and footers
\fancyhead[L]{\textit{\rightmark}} % Top left header
\fancyhead[R]{\textit{\leftmark}} % Top right header
\renewcommand{\headrulewidth}{.25pt} % Rule under the header
\fancyfoot[C]{\footnotesize{\textsf{\thepage}}} % Bottom center footer
\renewcommand{\footrulewidth}{.25pt} % Rule under the footer
\setlength{\headsep}{0.15in}
\pagestyle{fancy} % Use the custom headers and footers throughout the document
\usepackage{indentfirst}

\newcommand{\entry}[2]{\markboth{#1}{#1}\textbf{#1}\ {#2}\mbox{}\\}  % Defines the command to print each word on the page, 
% \markboth{}{} prints the first word on the page in the top left header and the last word in the top right; 
% textbf{#1} BOLD first unit (headword)
%----------------------------------------------------------------------------------------
'''
    return preamble

def translate(text):
#    start = text
    text = text.replace('powderhorn', 'chifle') 
    text = text.replace('horn', 'cuerno') 
    text = text.replace('antenna', 'antena') 
    text = text.replace('just planted', 'tierno') 
    text = text.replace('treetop', 'copa') 
    text = text.replace('root', 'raíz') 
    text = text.replace('small bunch', 'manojo')    
    text = text.replace('full bunch', 'rácimo')    
    text = text.replace('bunch', 'manojo') 
    text = text.replace('plant', 'planta')
    text = text.replace('dried leaf', 'hoja seca') 
    text = text.replace('leaf', 'hoja')
    text = text.replace('branch', 'rama')
    text = text.replace('flower', 'flor')
    text = text.replace('extended', 'extendido')
    text = text.replace('rolled','enrollado')
    text = text.replace('bean', 'semilla')
    text = text.replace('pod', 'vaina')
    text = text.replace('fruit', 'fruto')
    text = text.replace('infected places', 'lugar infectado')
    text = text.replace('cases', 'casos')
    text = text.replace('tree', 'árbol')
    text = text.replace('full bunch', 'rácimo entero')
    text = text.replace('(tub)', '(bandeja)')    
    text = text.replace('tuber', 'tubérculo')    
    text = text.replace('(roll', '(rollo')    
    text = text.replace('bouquet', 'ramo')    
    text = text.replace('bottle', 'botella')    
    text = text.replace('bag', 'bolsa')    
    text = text.replace('bar', 'barra')    
    text = text.replace('person', 'persona')    
    text = text.replace('seed', 'semilla')    
    text = text.replace('spine', 'espina')    
    text = text.replace('kneecap', 'rótula')    
    text = text.replace('large piece', 'pedazo grande')    
    text = text.replace('small pieces', 'pedacitos')    
    text = text.replace('by container', 'clf. por contenedor')    
    text = text.replace('by container (milk), *clf. (breast)',  '*clf. (seno)')
    text = text.replace('container', 'contenedor')
    text = text.replace('slingshot', 'resortera')    
    text = text.replace('language', 'idioma')    
    text = text.replace('type', 'clase')    
    text = text.replace('plot', 'terreno')    
    text = text.replace('beard', 'barba')    
    text = text.replace('disposable', 'deshechable')
    text = text.replace('by object', 'clf. por objeto')
    text = text.replace('object', 'objeto')    
    text = text.replace('clothes', 'ropa')    
    text = text.replace('stalk', 'tallo')    
    text = text.replace('mole', 'lunar')    
    text = text.replace('scourer', 'estropajo')    
    text = text.replace('church', 'iglesia')    
    text = text.replace('sheaf', 'manojo')    
    text = text.replace('insect', 'insecto')    
    text = text.replace('organ', 'órgano')    
    text = text.replace('fixture', 'orinal')    
    text = text.replace('nest', 'nido')    
    text = text.replace('gourd', 'guaje')    
    text = text.replace('cup', 'taza')    
    text = text.replace('basket', 'canasta')    
    text = text.replace('by garment', 'clf. por prenda')    
    text = text.replace('garment', 'prenda') 
    text = text.replace('certificate', 'documento') 
    text = text.replace('rocket', 'cohete') 
    text = text.replace('boll', 'cápsula') 
    text = text.replace('nail', 'uña') 
    text = text.replace('claw', 'garra')
    text = text.replace('entire husk', 'totomoxtle') 
    text = text.replace('web', 'telaraña') 
    text = text.replace('fan', 'abanico') 
    text = text.replace('costume', 'traje') 
    text = text.replace('shirt', 'camisa') 
    text = text.replace('file', 'lima') 
    text = text.replace('iron', 'hierro') 
    text = text.replace('ladder', 'escalera') 
    text = text.replace('rung, step', 'peldaño') 
    text = text.replace('growing', 'cresciente') 
    text = text.replace('umbrella', 'paraguas') 
    text = text.replace('ball', 'pelota') 
    text = text.replace('figurine', 'figura') 
    text = text.replace('splinter', 'astilla')    
    text = text.replace('shred', 'trozo') 
    text = text.replace('kernel', 'grano') 
    text = text.replace('cob', 'mazorca') 
    text = text.replace('pad)', 'tallo)') 
    text = text.replace('(pad,', '(tallo,') 
    text = text.replace('bulb', 'cabeza') 
    text = text.replace('clove', 'diente') 
    text = text.replace('bodypart', 'parte del cuerpo') 
    text = text.replace('cuff', 'puño') 
    text = text.replace('lung', 'pulmón') 
    text = text.replace('whole', 'entero') 
    text = text.replace('half', 'mitad') 
    text = text.replace('river', 'río') 
    text = text.replace('general flooding', 'inundación') 
    text = text.replace('opening', 'apertura') 
    text = text.replace('surface', 'superficie') 
    text = text.replace('water', 'agua') 
    text = text.replace('piece', 'pieza') 
    text = text.replace('spool', 'carrete') 
    text = text.replace('strand', 'hilo') 
    text = text.replace('berry', 'fruto') 
    text = text.replace('clap', 'trueno') 
    text = text.replace('being', 'espíritu') 
    text = text.replace('period', 'periodo') 
    text = text.replace('(age', '(edad)') 
    text = text.replace('hoop', 'aro') 
    text = text.replace('stick', 'palo') 
    text = text.replace('cuff', 'puño') 
    text = text.replace('issue', 'asunto') 
    text = text.replace('group', 'personas')
    text = text.replace('mattress', 'colchón')
    text = text.replace('dance', 'danza')
    text = text.replace('hair', 'pelo')
    text = text.replace('(nut', '(nuez)')
    text = text.replace('cloth', 'tela')    
    text = text.replace('broom', 'escoba') 
#    if text != start:   
#        print(text) 
    return text

'''END UNT Latex Dictionary'''

'''BEGIN Dene output'''

def DeneDict(fldbk):
    print("Outputting Josh’s database to text")
    '''this needs to be fixed so the node is passed to the lex object constructor instead of
    building the object here. Note Grm, C2, Cf now have None if absent, not []'''
    return
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
            dictDoc.asis(buildDeneEntries(dictionaryEntries))
            with dictDoc.tag('h2'):
                dictDoc.asis('English-Dene')
            dictDoc.asis(buildEnglishDene(dictionaryEntries))
    fname = dataIndex.homePath + '/Documents/Output.html'
    saveFile = open(fname, "w", encoding="UTF-8")
    saveFile.write(dictDoc.getvalue())
    saveFile.close()
    print("all done")
    
def buildDeneEntries(entries):
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
            entryDoc.asis(getDeneDefs(entry))
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
    
def getDeneDefs(entry):
#    print('entering getDeneDefs')
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

def buildEnglishDene(entries):
    print('entering buildEnglishDene')
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

'''END DENE output'''

