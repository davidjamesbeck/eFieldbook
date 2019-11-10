from PyQt5 import QtWidgets, QtCore
import re, copy
from xml.etree import ElementTree as etree
from ELFB import contextMenus, dataIndex, Orthographies, formattingHandlers, textOnlyBtns, codeExtractor, cardLoader
from ELFB.palettes import CrossRefManager
from ELFB.palettes import SessionDate

def fixGlosses(gloss):
    '''method removes quotes and timeCodes, creates
    SpokenBy and TimeCode attributes from text'''
    gloss = gloss.replace('–', '-')
    gloss = gloss.strip()
    spokenBy = None
    spokenBy, gloss = codeExtractor.getSpokenBy(gloss)
    gloss = gloss.strip()
    if gloss[0] == '‘' or gloss[0] == '“':
        gloss = gloss[1:]
    timeCode, endTime, gloss = codeExtractor.getTime(gloss)
    gloss = gloss.strip()
    if gloss[-1] == '’' or gloss[-1] == '“':
        gloss = gloss[:-1]    
    return gloss, spokenBy, timeCode, endTime

def manageHomonyms(synList):
    '''makes sure that homonymous words have the correct cross-references, 
    manages changes after additions, editing, and deletions'''
    '''first, control synList for defunct IDs in the list of synonyms'''
    synList[:] = [x for x in synList if x in dataIndex.lexDict.keys()]
    for card in synList:
        entry = dataIndex.lexDict[card]
        entryID = entry.attrib.get('LexID')
        newSynList = copy.deepcopy(synList)
        try:
            newSynList.remove(newSynList[newSynList.index(entryID)])
        except ValueError:
            pass
        newSyn = ', '.join(newSynList)
        dataIndex.lexDict[card].set('Hom', newSyn)

def prepareTextUpdate(fldbk, ExNode):
    TextNode = dataIndex.currentText
    if ExNode.attrib.get('SourceText') == TextNode.attrib.get('TextID'):
        textOnlyBtns.updateText(fldbk, ExNode)

def setContents(fldbk, fieldname):
    update = SessionDate.dateFinder()
#    print('updating %s' %fieldname)
    '''update XML for edited fields'''
#    if dataIndex.updateEnabled == 'off':
#        return
    if fieldname[0] == "l":
        fldbk.lUpdated.setPlainText(update)
        newContent = fldbk.lUpdated.toPlainText()
        child = dataIndex.lexDict[dataIndex.currentCard]
        child.set('Update',newContent)

    elif fieldname[0] == "t":
        fldbk.tUpdated.setPlainText(update)
        newContent = fldbk.tUpdated.toPlainText()
        child = dataIndex.textDict[dataIndex.currentCard]
        child.set('Update',newContent)

    elif fieldname[0] == "e":
        fldbk.eUpdated.setPlainText(update)
        newContent = fldbk.eUpdated.toPlainText()
        child = dataIndex.exDict[dataIndex.currentCard]
        child.set('Update',newContent)

    elif fieldname[0] == "d":
        fldbk.dUpdated.setPlainText(update)
        newContent = fldbk.dUpdated.toPlainText()
        child = dataIndex.dataDict[dataIndex.currentCard]
        child.set('Update',newContent)
  
    #Home tab
    if fieldname == 'hTitle':
        html = fldbk.hTitle.toHtml()
        newHtml = formattingHandlers.textStyleHandler(html)
        fldbk.hTitle.setText(newHtml)
        newContent = fldbk.hTitle.toPlainText()
        dataIndex.root.set('Dbase',newContent)
        fldbk.hTitle.setText(html)

    elif fieldname == 'hLanguage':
        newContent = fldbk.hLanguage.toPlainText()
        dataIndex.root.set('Language',newContent)

    elif fieldname == 'hFamily':
        newContent = fldbk.hFamily.toPlainText()
        dataIndex.root.set('Family',newContent)

    elif fieldname == 'hPopulation':
        newContent = fldbk.hPopulation.toPlainText()
        dataIndex.root.set('Population',newContent)

    elif fieldname == 'hLocation':
        newContent = fldbk.hLocation.toPlainText()
        dataIndex.root.set('Location',newContent)

    elif fieldname == 'hISO':
        newContent = fldbk.hISO.toPlainText()
        dataIndex.root.set('ISO',newContent)           
        
    #Lexicon
    elif fieldname == 'lOrthography':
        newContent = fldbk.lOrthography.text()
        oldListText = child.find('Orth').text
        entryID = child.attrib.get('LexID')
        if newContent != oldListText:
            child.find('Orth').text = newContent
            currentProxyIndex = fldbk.lLexNav.currentIndex()
            currentSourceIndex = fldbk.lLexNav.model().mapToSource(currentProxyIndex)
            fldbk.lLexNav.model().sourceModel().itemFromIndex(currentSourceIndex).setText(newContent)
            cardLoader.resetNavBars(fldbk.lLexNav, dataIndex.currentCard)
            
            '''if this was a homonym and now isn't in the same set, delink it'''
            if child.attrib.get('Hom') != None:
                syn = child.attrib.get('Hom')
                synList = syn.split(', ')
                if len(synList) != 0:
                    for card in synList:
                        del dataIndex.lexDict[card].attrib['Hom']
                    try:
                        synList.remove(entryID)
                    except ValueError:
                        pass
                if len(synList) != 1:
                    manageHomonyms(synList)

            '''check to see if you've created homonymy'''
            homList = [entryID]
            for node in dataIndex.root.iter('Lex'):
                '''create list of all homophonous entries'''
                if node.find('Orth').text == newContent and node.attrib.get('LexID') != entryID:
                    homList.append(node.attrib.get('LexID'))
            if len(homList) > 1:
                manageHomonyms(homList)
            
            '''autoconversion'''
            if fldbk.lAutoBtn.isChecked():
                IPA = Orthographies.toIPA(newContent)
                fldbk.lIPA.setText(IPA)
                ipaNode = child.find('IPA')
                if ipaNode != None:
                    child.remove(ipaNode)
                if len(newContent) != 0:
                    elemList = list(child)
                    elemList.reverse()
                    for i,item in enumerate(elemList):
                        if item.tag == 'POS': 
                            break
                        elif item.tag == 'Orth': 
                            break
                    i = len(elemList) - i
                    child.insert(i,etree.Element('IPA'))
                    child.find('IPA').text = IPA

    elif fieldname == 'lPOS':
        newContent = fldbk.lPOS.toPlainText()
        posNode = child.find('POS')
        if posNode != None:
            child.remove(posNode)
        if len(newContent) != 0:
            child.insert(1,etree.Element('POS'))
            child.find('POS').text = newContent

    elif fieldname == 'lIPA':
        newContent = fldbk.lIPA.text()
        ipaNode = child.find('IPA')
        if ipaNode != None:
            child.remove(ipaNode)
        if len(newContent) != 0:
            elemList = list(child)
            elemList.reverse()
            for i,item in enumerate(elemList):
                if item.tag == 'POS': 
                    break
                elif item.tag == 'Orth': 
                    break
            i = len(elemList) - i
            child.insert(i,etree.Element('IPA'))
            child.find('IPA').text = newContent

    elif fieldname == 'lLiteral':
        newContent = fldbk.lLiteral.toPlainText()
        if len(newContent) != 0:
            newContent, newText = formattingHandlers.smallCapsConverter(newContent)
            fldbk.lLiteral.setText(newText)
        else:
            newContent = ''
        litNode = child.find('Lit')
        if litNode != None:
            child.remove(litNode)
        if len(newContent) != 0:
            elemList = list(child)
            for i, item in enumerate(elemList):
                if item.tag == 'Def':
                    break
            child.insert(i,etree.Element('Lit'))
            child.find('Lit').text = newContent
            
    elif fieldname == 'lRegister':
        newContent = fldbk.lRegister.toPlainText()
        regNode = child.find('Reg')
        if regNode != None:
            child.remove(regNode)
        if len(newContent) != 0:
            elemList = list(child)
            elemList.reverse()
            for i,item in enumerate(elemList):
                if item.tag == 'Cf.':
                    break
                elif item.tag == 'C2':
                    break
                elif item.tag == 'Grm': 
                    break
                elif item.tag == 'IPA': 
                    break
                elif item.tag == 'POS': 
                    break
                elif item.tag == 'Orth': 
                    break
            i = len(elemList) - i
            child.insert(i,etree.Element('Reg'))
            child.find('Reg').text = newContent
           
    elif fieldname == 'lDialect':
        newContent = fldbk.lDialect.toPlainText()
        alternate = ''
        if newContent:
            dialectList = newContent.split(None,1)
            dialect = dialectList[0]
            diaText = dialect
            altList = None
            if len(dialectList) > 1:
                alternate = dialectList[1]              
                alternate = re.sub("\(", "", alternate)
                alternate = re.sub("\)", "", alternate)
                altList = alternate.split("; ")
                for i in range(0,len(altList)):
                    alternative = altList[i].split(None,1)
                    variant = alternative[0]
                    try:
                        alternate = alternative[1]
                    except IndexError:
                        fldbk.dialectBox = QtWidgets.QMessageBox()
                        fldbk.dialectBox.setIcon(QtWidgets.QMessageBox.Warning)
                        fldbk.dialectBox.setStandardButtons(QtWidgets.QMessageBox.Cancel)
                        fldbk.dialectBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        fldbk.dialectBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                        fldbk.dialectBox.setText('Formatting error.')
                        fldbk.dialectBox.setInformativeText('Format dialect information as'
                                                           '<blockquote><big>Cdn. (US. soda; UK fizzy drink)</big></blockquote>'
                                                           'For expressions known for only one dialect, simply<br /> '
                                                           'give the dialect name without an alternative.<br />')
                        fldbk.dialectBox.exec_()
                        return
                    if i == 0 and len(altList) - 1 == 0:
                        dialect = dialect + " (" + variant + " " + alternate + ")"
                    elif i == 0:
                        dialect = dialect + " (" + variant + " " + alternate
                    elif i == len(altList) - 1:
                        dialect = dialect + "; " + variant + " " + alternate + ")"
                    else:
                        dialect = dialect + "; " + variant + " " + alternate
                fldbk.lDialect.setText(dialect)                    
        crossRef = None
        oldCrossRef = None
        if child.find('Dia') != None:
            oldAlt = child.findall('Dia/Alternative')
            oldCrossRef = []
            if oldAlt != None:
                for item in oldAlt:
                    oldRef = item.attrib.get('CrossRef')
                    oldCrossRef.append(oldRef)
            child.remove(child.find('Dia'))
        if newContent:
            elemList = list(child)
            elemList.reverse()
            for i, item in enumerate(elemList):
                if item.tag == 'Reg':
                    break
                elif item.tag == 'Cf':
                    break
                elif item.tag == 'C2':
                    break
                elif item.tag == 'Grm':
                    break
                elif item.tag == 'IPA':
                    break
                elif item.tag == 'POS': 
                    break
                elif item.tag == 'Orth': 
                    break
            i = len(elemList) - i
            child.insert(i,etree.Element('Dia',{'Dialect':diaText}))
            if altList != None and len(altList) != 0:
                crossRefList = []
                alterList = []
                for j in range(0,len(altList)):
                    altParts = altList[j].split(None,1)
                    variant = altParts[0]
                    alternate = altParts[1]
                    newAltNode = etree.SubElement(child.find('Dia'),'Alternative',{'Variant':variant})
                    newAltNode.text = alternate
                    for entry in dataIndex.root.iter('Lex'):
                        lexeme = entry.find('Orth').text
                        if lexeme == alternate and entry.attrib.get('Hom') != None:
                            #TODO: fix so you can see defs as well as forms?
                            for oldRef in oldCrossRef:
                                if entry.attrib.get('LexID') == oldRef:
                                    crossRef = oldRef
                                    newAltNode.set('CrossRef',crossRef)
                                    break
                                else: 
                                    synList = entry.attrib.get('Hom').split(", ")
                                    for syn in synList:
                                        if entry.attrib.get('LexID') == oldCrossRef:
                                           crossRef = oldRef
                                           newAltNode.set('CrossRef',crossRef)
                                           break
                                    synList.append(entry.attrib.get('LexID'))
                                    newCf = CrossRefManager.Dialog(fldbk)
                                    newCf.setRefs(synList)
                                    if newCf.exec_():
                                        crossRef = newCf.getRef()
                                    else:
                                        crossRef = None
                                    break
                            
                        elif lexeme == alternate:
                            crossRef = entry.attrib.get('LexID')
                            newAltNode.set('CrossRef',crossRef)
                            break
                    if crossRef != None:
                        crossRefList.append(crossRef)
                        alterList.append(alternate)
                if crossRefList != None:
                    contextMenus.updateContextMenu(fldbk, fieldname,crossRefList,alterList)
                if crossRefList == None:
                    contextMenus.clearContextMenu(fldbk, fieldname)
       
    elif fieldname == 'lBrrw':
        newContent = fldbk.lBrrw.toPlainText()
        if newContent:
            borrowing = newContent.split(None,1)
            source = borrowing[0]
            cognate = borrowing[1]
            cognate = re.sub('"', '', cognate)
            cognate = re.sub('“', '', cognate)
            cognate = re.sub('”', '', cognate)
            newText = source + ' “' + cognate + '”'
            fldbk.lBrrw.setPlainText(newText)
        borrowNode = child.find('Brrw')
        if borrowNode != None:
            child.remove(borrowNode)
        if newContent:
            elemList = list(child)
            elemList.reverse()
            for i, item in enumerate(elemList):
                if item.tag == 'Dia':
                    break
                elif item.tag == 'Reg':
                    break
                elif item.tag == 'Cf.':
                    break
                elif item.tag == 'C2':
                    break
                elif item.tag == 'Grm': 
                    break
                elif item.tag == 'IPA': 
                    break
                elif item.tag == 'POS': 
                    break
                elif item.tag == 'Orth': 
                    break
            i = len(elemList) - i
            child.insert(i,etree.Element('Brrw'))
            child.find('Brrw').text = cognate
            child.find('Brrw').set('Source',source)
        
    elif fieldname == 'lSource':
        newContent = fldbk.lSource.toPlainText()
        child.set('Spkr',newContent)

    elif fieldname == 'lResearcher':
        newContent = fldbk.lResearcher.toPlainText()
        child.set('Rschr',newContent)
        
    elif fieldname == 'lDate':
        newContent = fldbk.lDate.toPlainText()
        child.set('Date',newContent)
        
    elif fieldname == 'lUpdated':
        newContent = fldbk.lUpdated.toPlainText()
        child.set('Update',newContent)
        
    elif fieldname == 'lConfirmed':
        newContent = fldbk.lConfirmed.toPlainText()
        child.set('Confirmed',newContent)

    elif fieldname == 'lNotes':
        html = fldbk.lNotes.toHtml()
        newHtml = formattingHandlers.textStyleHandler(html)
        fldbk.lNotes.setHtml(newHtml)
        newContent = fldbk.lNotes.toPlainText().strip()
        fldbk.lNotes.setHtml(html)
        comNode = child.find('Comments')
        if comNode != None:
            child.remove(comNode)
        if len(newContent) != 0:
            elemList = list(child)
            elemList.reverse()
            for i, item in enumerate(elemList):
                if item.tag == 'Root':
                    break
                elif item.tag == 'Drvn':
                    break
                elif item.tag == 'Def':
                    break
            i = len(elemList) - i
            newCommentNode = etree.Element('Comments')
            newCommentNode.text = newContent
            child.insert(i,newCommentNode)

    elif fieldname == 'lPrimaryIndex':
        newContent = fldbk.lPrimaryIndex.toPlainText()
        child.set('L1Index',newContent)

    elif fieldname == 'lSecondaryIndex':
        newContent = fldbk.lSecondaryIndex.toPlainText()
        child.set('L2Index',newContent)

    elif fieldname == 'lKeywordIndex':
        newContent = fldbk.lKeywordIndex.toPlainText()
        child.set('Kywd',newContent)

    #Examples
        
    elif fieldname == 'eLine':
        html = fldbk.eLine.toHtml()
        while '  ' in html:
            html = html.replace('  ', ' ')
        newHtml = formattingHandlers.textStyleHandler(html)
        fldbk.eLine.setHtml(newHtml)
        child.find('Line').text = fldbk.eLine.toPlainText().strip()
        fldbk.eLine.setHtml(html)
        ExNode = dataIndex.exDict[dataIndex.currentCard]
        if dataIndex.currentText != None and ExNode.attrib.get('SourceText') != None:
            prepareTextUpdate(fldbk, ExNode)
        
    elif fieldname == 'eL1Gloss':
        html = fldbk.eL1Gloss.toHtml()
        while '  ' in html:
            html = html.replace('  ', ' ')
        newHtml = formattingHandlers.textStyleHandler(html)
        fldbk.eL1Gloss.setHtml(newHtml)
        child.find('L1Gloss').text = fldbk.eL1Gloss.toPlainText().strip()
        fldbk.eL1Gloss.setHtml(html)
        ExNode = dataIndex.exDict[dataIndex.currentCard]
        if dataIndex.currentText != None and ExNode.attrib.get('SourceText') != None:
            prepareTextUpdate(fldbk, ExNode)
            
    elif fieldname == 'eL2Gloss':
        html = fldbk.eL2Gloss.toHtml()
        while '  ' in html:
            html = html.replace('  ', ' ')        
        newHtml = formattingHandlers.textStyleHandler(html)
        fldbk.eL2Gloss.setHtml(newHtml)
        newGloss = fldbk.eL2Gloss.toPlainText().strip()
        fldbk.eL2Gloss.setHtml(html)
        l2Node = child.find('L2Gloss')
        if l2Node != None:
            child.remove(l2Node)
        if len(newContent) != 0:
            elemList = list(child)
            elemList.reverse()
            for i, item in enumerate(elemList):
                if item.tag == 'L1Gloss':
                    break
            i = len(elemList) - i
            child.insert(i,etree.Element('L2Gloss'))
            child.find('L2Gloss').text = newGloss
        ExNode = dataIndex.exDict[dataIndex.currentCard]
        if dataIndex.currentText != None and ExNode.attrib.get('SourceText') != None:
            prepareTextUpdate(fldbk, ExNode)
            
    elif fieldname == 'eNotes':
        if len(fldbk.eNotes.toPlainText()) != 0:
            html = fldbk.eNotes.toHtml()
            newHtml = formattingHandlers.textStyleHandler(html)
            fldbk.eNotes.setHtml(newHtml)
            newContent = fldbk.eNotes.toPlainText().strip()
            fldbk.eNotes.setHtml(html)
            comNode = child.find('Comments')
            if comNode != None:
                child.remove(comNode)
            if len(newContent) != 0:
                elemList = list(child)
                elemList.reverse()
                for i, item in enumerate(elemList):
                    if item.tag == 'L2Gloss':
                        break
                    elif item.tag == 'L1Gloss':
                        break                            
                i = len(elemList) - i
            child.insert(i,etree.Element('Comments'))
            child.find('Comments').text = newContent

    elif fieldname == 'eKeywords':
        newContent = fldbk.eKeywords.toPlainText()
        child.set('Kywd',newContent)

    elif fieldname == 'eSource':
        newContent = fldbk.eSource.toPlainText()
        child.set('Spkr',newContent)
      
    elif fieldname == 'eResearcher':
        newContent = fldbk.eResearcher.toPlainText()
        child.set('Rschr',newContent)

    elif fieldname == 'eDate':
        newContent = fldbk.eDate.toPlainText()
        child.set('Date',newContent)
        
    elif fieldname == 'eTimeCode':
        newContent = fldbk.eTimeCode.toPlainText()
        child.set('Time', newContent)
        
    elif fieldname == 'eSpokenBy':
        newContent = fldbk.eSpokenBy.toPlainText()
        if child.attrib.get("SourceText") != None:
            for line in dataIndex.textDict[child.attrib.get("SourceText")].iter('Ln'):
                if line.attrib.get('LnRef') == child.attrib.get('ExID'):
                    if len(newContent) == 0 and line.attrib.get("SpokenBy") != None:
                        del line.attrib['SpokenBy']
                    elif len(newContent) != 0:
                        line.set('SpokenBy', newContent)
                        for speaker in dataIndex.root.iter('Speaker'):
                            if speaker.attrib.get('SCode') == newContent:
                                child.attrib['Spkr'] = newContent
                                fldbk.eSource.setPlainText(newContent)
                                break
                    break
        
    #TEXTS
    elif fieldname == 'tNotes':
        if len(fldbk.tNotes.toPlainText()) != 0:
            html = fldbk.tNotes.toHtml()
            newHtml = formattingHandlers.textStyleHandler(html)
            fldbk.tNotes.setHtml(newHtml)
            newContent = fldbk.tNotes.toPlainText().strip()
            fldbk.tNotes.setHtml(html)
            comNode = child.find('Comments')
            if comNode != None:
                child.remove(comNode)
            if len(newContent) != 0:
                elemList = list(child)
                elemList.reverse()
                for i, item in enumerate(elemList):
                    if item.tag == 'Ln':
                        break
                i = len(elemList) - i
            child.insert(i,etree.Element('Comments'))
            child.find('Comments').text = newContent

    elif fieldname == 'tTranscriber':
       newContent = fldbk.tTranscriber.toPlainText()
       child.set('Trns',newContent)

    elif fieldname == 'tSource':
       newContent = fldbk.tSource.toPlainText()
       child.set('Spkr',newContent)
      
    elif fieldname == 'tResearcher':
        newContent = fldbk.tResearcher.toPlainText()
        child.set('Rschr',newContent)

    elif fieldname == 'tDate':
        newContent = fldbk.tDate.toPlainText()
        child.set('Date',newContent)

    elif fieldname == 'tTitle':
        plainTextTitle = fldbk.tTitle.toPlainText()
        html = fldbk.tTitle.toHtml()
        newHtml = formattingHandlers.textStyleHandler(html)
        fldbk.tTitle.setHtml(newHtml)
        newContent = fldbk.tTitle.toPlainText()
        fldbk.tTitle.setHtml(html)
        child.find('Title').text = newContent
        currentProxyIndex = fldbk.tTextNav.currentIndex()
        currentSourceIndex = fldbk.tTextNav.model().mapToSource(currentProxyIndex)
        fldbk.tTextNav.model().sourceModel().itemFromIndex(currentSourceIndex).setText(plainTextTitle)
        fldbk.tTextNav.model().setSortCaseSensitivity(0)
        fldbk.tTextNav.model().sort(0,QtCore.Qt.AscendingOrder)
        fldbk.tTextNav.scrollTo(fldbk.tTextNav.currentIndex(), QtWidgets.QAbstractItemView.EnsureVisible)

    #DATASETS
    elif fieldname == 'dSource':
       newContent = fldbk.dSource.toPlainText()
       child.set('Spkr',newContent)
      
    elif fieldname == 'dResearcher':
        newContent = fldbk.dResearcher.toPlainText()
        child.set('Rschr',newContent)

    elif fieldname == 'dDate':
        newContent = fldbk.dDate.toPlainText()
        
    elif fieldname == 'dKeywords':
       newContent = fldbk.dKeywords.toPlainText()
       child.set('Kywd',newContent)
        
    elif fieldname == 'dNotes':
        if len(fldbk.dNotes.toPlainText()) != 0:
            html = fldbk.dNotes.toHtml()
            newHtml = formattingHandlers.textStyleHandler(html)
            fldbk.dNotes.setHtml(newHtml)
            newContent = fldbk.dNotes.toPlainText().strip()
            fldbk.dNotes.setHtml(html)
            comNode = child.find('Comments')
            if comNode != None:
                child.remove(comNode)
            if len(newContent) != 0:
                elemList = list(child)
                elemList.reverse()
                for i, item in enumerate(elemList):
                    if item.tag == 'Data':
                        break
                    elif item.tag == 'Ln':
                        break
                i = len(elemList) - i
            child.insert(i,etree.Element('Comments'))
            child.find('Comments').text = newContent
        
    elif fieldname == 'dData':
        html = fldbk.dData.toHtml()
        newHtml = formattingHandlers.textStyleHandler(html)
        fldbk.dData.setHtml(newHtml)
        newContent = fldbk.dData.toPlainText()
        fldbk.dData.setHtml(html)
        child.find('Data').text = newContent
    
    elif fieldname == 'dTitle':
        html = fldbk.dTitle.toHtml()
        plainTextTitle = fldbk.dTitle.toPlainText()
        newHtml = formattingHandlers.textStyleHandler(html)
        fldbk.dTitle.setHtml(newHtml)
        newContent = fldbk.dTitle.toPlainText()
        fldbk.dTitle.setHtml(html)
        child.find('Title').text = newContent           
        currentProxyIndex = fldbk.dDataNav.currentIndex()
        currentSourceIndex = fldbk.dDataNav.model().mapToSource(currentProxyIndex)
        fldbk.dDataNav.model().sourceModel().itemFromIndex(currentSourceIndex).setText(plainTextTitle)
        fldbk.dDataNav.model().setSortCaseSensitivity(0)
        fldbk.dDataNav.model().sort(0,QtCore.Qt.AscendingOrder)
        fldbk.dDataNav.scrollTo(fldbk.dDataNav.currentIndex(), QtWidgets.QAbstractItemView.EnsureVisible)
        
    #METADATA fields
#    elif fieldname == 'oOrder' or fieldname == 'oDiacriticsField':
#        alert = '!Orthography has been edited. Use “Update” to save permanent changes.'
#        fldbk.oOrthChangedLabel.setText(alert)
#        fldbk.oOrthChangedLabel.setToolTip('This warning indicates that changes have been made to the\n'
#        'Mapping or Diacritics field. These will not be saved unless\n'
#        'you click the "Update" button. The original orthography can\n'
#        'be restored by clicking on its name in the list below.')
        
    elif fieldname == 'sOrder' or fieldname == 'sExclusions':
        alert = '!Sorting order has been edited. Use “Update” to save permanent changes.'
        fldbk.sOrderChangedLabel.setText(alert)
        fldbk.sOrderChangedLabel.setToolTip('This warning indicates that changes have been made to the\n'
        'Sorting order or Exclusions field. These will not be saved\n'
        'unless you click the "Update" button. The original order can\n'
        'be restored by clicking on its name in the list below.')

def cleanUpIDs(tag):
    '''removes defunct IDs once elements have been deleted'''
    if tag[0] == "M":
        '''media can be linked to: Lex/Sound,Text/Sound,Dset/Sound,Ex/Sound,Lex/Grm,Lex/C2'''
        for node in dataIndex.root.iter():
            soundNode = node.find('Sound[@MediaRef="%s"]'%tag)
            if soundNode != None:
                node.remove(soundNode)
            soundNode = node.find('Grm[@MediaRef="%s"]'%tag)
            if soundNode != None:
                del soundNode.attrib['MediaRef']
            soundNode = node.find('C2[@MediaRef="%s"]'%tag)
            if soundNode != None:
                del soundNode.attrib['MediaRef']
    
    if tag[0] == "L":
        '''lex cards can be linked to Lex[Hom],Lex/Cf[CrossRef],Lex/Dia/Alternative[CrossRef],
        Lex/Def/Dia/Alternative[CrossRef],Drvn[LexIDREF],Root[LexIDREF],Ex[Links]; however, deleting the
        lex card already fixes up the Hom crossrefs, so no need to do it here'''
        for node in dataIndex.root.iter('Lex'):
            ##remove cross-refs in grammar table##
            lexNode = node.find('Cf[@CrossRef]')
            if lexNode != None:
                cf = lexNode.attrib.get('CrossRef')
                cfList = cf.split(', ')
                if tag in cfList:
                    cfList.pop(cfList.index(tag))
                    lexNode.set('CrossRef', ', '.join(cfList))
            ##remove cross-refs in both levels of the dialectal tags
            lexNode = node.find('Dia/Alternative[@CrossRef="%s"]'%tag)
            if lexNode != None:
                del lexNode.attrib['CrossRef']
            lexNode = node.find('Def/Dia/Alternative[@CrossRef="%s"]'%tag)
            if lexNode != None:
                del lexNode.attrib['CrossRef']        
            lexNode = node.find('Drvn[@LexIDRef="%s"]'%tag)
            if lexNode != None:
                del lexNode
            lexNode = node.find('Root[@LexIDRef="%s"]'%tag)
            if lexNode != None:
                del lexNode
        for node in dataIndex.root.iter('Ex'):
            if 'Links' in node.keys():
                links = node.attrib.get('Links')
                linksList = links.split(',')
                if tag in linksList:
                    linksList.pop(linksList.index(tag))
                    node.set('Links', ', '.join(linksList))
        if dataIndex.lastLex == tag:
            dataIndex.lastLex = None
    
    if tag[0] == 'E':
        '''ex cards can be linked to Def/Ln[LnRef],Text/Ln[LnRef],Dset/Ln[LnRef]'''
        for node in dataIndex.root.iter():
            lineNode = node.find('Ln[@LnRef="%s"]'%tag)
            if lineNode != None:
                node.remove(lineNode)
            lineNode = node.find('Def/Ln[@LnRef="%s"]'%tag)
            if lineNode != None:
                defNodes = node.findall('Def')
                for dfn in defNodes:
                    badNode = dfn.find('Ln[@LnRef="%s"]'%tag)
                    if badNode != None:
                        dfn.remove(badNode)
        if dataIndex.lastEx == tag:
            dataIndex.lastEx = None
    
    if tag[0] == 'D':
        for node in dataIndex.root.iter('Ex'):
            if 'Links' in node.keys():
                links = node.attrib.get('Links')
                linksList = links.split(',')
                if tag in linksList:
                    linksList.pop(linksList.index(tag))
                    node.set('Links', ', '.join(linksList))
        if dataIndex.lastDset == tag:
            dataIndex.lastDset = None
    
    if tag[0] == 'T':
        '''texts are cross-referenced in Ex[SourceText]'''
        for node in dataIndex.root.iter('Ex'):
            if 'SourceText' in node.keys():
                if node.attrib.get('SourceText') == tag:
                    del node.attrib['SourceText']
        if dataIndex.lastText == tag:
            dataIndex.lastText = None
