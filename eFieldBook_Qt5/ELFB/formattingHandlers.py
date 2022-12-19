import re
import locale
from ELFB import dataIndex


def addCommas(number):
    """TODO we can set locales in preferences"""
    locale.setlocale(locale.LC_ALL, 'en_CA')
    number = locale.format_string("%d", number, grouping=True)
    return number


def textStyleHandler(html):
    utag = '<span style=" text-decoration: underline;">'
    btag = '<span style=" font-weight:600;">'
    itag = '<span style=" font-style:italic;">'
    iutag = '<span style=" font-style:italic; text-decoration: underline;">'
    butag = '<span style=" font-weight:600; text-decoration: underline;">'
    bitag = '<span style=" font-weight:600; font-style:italic;">'
    biutag = '<span style=" font-weight:600; font-style:italic; text-decoration: underline;">'
    endtag = '</span>'
    while utag in html:
        findUnderline = '(?<=%s)' %utag
        findUnderline += '(.*?)'
        findUnderline += '(?=%s)' %endtag
        uRegex = re.compile(findUnderline)
        hit = re.search(uRegex, html)
        matches = hit.group(0)
        html = html[:hit.start()-len(utag)] + '{u}' + matches + '{/u}' + html[hit.end()+len(endtag):]
    while itag in html:
        findItalics = '(?<=%s)' %itag
        findItalics += '(.*?)'
        findItalics += '(?=%s)' %endtag
        iRegex = re.compile(findItalics)
        hit = re.search(iRegex, html)
        matches = hit.group(0)
        html = html[:hit.start()-len(itag)] + '{i}' + matches + '{/i}' + html[hit.end()+len(endtag):]
    while btag in html:
        findBold = '(?<=%s)' %btag
        findBold += '(.*?)'
        findBold += '(?=%s)' %endtag
        bRegex = re.compile(findBold)
        hit = re.search(bRegex, html)
        matches = hit.group(0)
        html = html[:hit.start()-len(btag)] + '{b}' + matches + '{/b}' + html[hit.end()+len(endtag):]
    while biutag in html:
        findBIU = '(?<=%s)' %biutag
        findBIU += '(.*?)'
        findBIU += '(?=%s)' %endtag
        biuRegex = re.compile(findBIU)
        hit = re.search(biuRegex, html)
        matches = hit.group(0)
        html = html[:hit.start()-len(biutag)] + '{b}{i}{u}' + matches + '{/u}{/i}{/b}' + html[hit.end()+len(endtag):]
    while iutag in html:
        findIU = '(?<=%s)' %iutag
        findIU += '(.*?)'
        findIU += '(?=%s)' %endtag
        iuRegex = re.compile(findIU)
        hit = re.search(iuRegex, html)
        matches = hit.group(0)
        html = html[:hit.start()-len(iutag)] + '{i}{u}' + matches + '{/u}{/i}' + html[hit.end()+len(endtag):]
    while bitag in html:
        findBI = '(?<=%s)' %bitag
        findBI += '(.*?)'
        findBI += '(?=%s)' %endtag
        biRegex = re.compile(findBI)
        hit = re.search(biRegex, html)
        matches = hit.group(0)
        html = html[:hit.start()-len(bitag)] + '{b}{i}' + matches + '{/i}{/b}' + html[hit.end()+len(endtag):]
    while butag in html:
        findBU = '(?<=%s)' %butag
        findBU += '(.*?)'
        findBU += '(?=%s)' %endtag
        buRegex = re.compile(findBU)
        hit = re.search(buRegex, html)
        matches = hit.group(0)
        html = html[:hit.start()-len(butag)] + '{b}{u}' + matches + '{/u}{/b}' + html[hit.end()+len(endtag):]
    return html   
    
def smallCapsConverter(newContent):
    """handles small caps for the literal field on lex cards, 
    applies formatting when user types in abbreviations
    newContent = contents of Lit field sans formatting
    newText = text to put into view"""
    abbNode = dataIndex.root.find('Abbreviations')
    newText = newContent
    abbrList = []
    termList = []
    for abbreviation in abbNode.iter('Abbr'):
        gloss = abbreviation.attrib.get('Abv')
        term = abbreviation.attrib.get('Term')
        if "." in gloss:
            glossList = gloss.split(".")
            for abbr in glossList:
                if abbr not in abbrList:
                    abbrList.append(abbr)
        else:
            if not gloss in abbrList:
                abbrList.append(gloss)
        termList.append([term, gloss])
    sortedTermList = sorted(termList, key=lambda x:len(x[0]), reverse=True)
    for term, gloss in sortedTermList:
        """convert long forms to small caps abbreviations"""
        regexTerm = re.compile('(?<=\W)%s(?=\W)'%term)
        if regexTerm.search(newContent):
            newGloss = "<small>" + gloss.upper() + "</small>"
            newContent = regexTerm.sub(gloss, newContent)
            newText = regexTerm.sub(newGloss, newText)
    for gloss in abbrList:    
        """format abbreviations in small caps"""
        newGloss = "<small>" + gloss.upper() + "</small>"
        regexAbbr = re.compile('(?<!\w)%s(?!\w)'%gloss) #handles abbreviations not yet in caps
        regexAbbrCaps = re.compile('(?<!\w)%s(?!\w)'%gloss.upper()) #handles abbreviations already in caps
        if regexAbbrCaps.search(newContent): #this condition is needed because the field holds caps versions of the abbreviations
            newContent = regexAbbrCaps.sub(gloss, newContent)
            newText = regexAbbrCaps.sub(newGloss, newText)
        elif regexAbbr.search(newContent):
            newContent = regexAbbr.sub(gloss, newContent)
            newText = regexAbbr.sub(newGloss, newText)
    return newContent, newText
    
def XMLtoRTF(string):
    string = string.replace('{i}', '<i>')
    string = string.replace('{/i}', '</i>')
    string = string.replace('{b}', '<b>')
    string = string.replace('{/b}', '</b>')
    string = string.replace('{u}', '<u>')
    string = string.replace('{/u}', '</u>')
    string = string.replace('\n', '<br/>')
    return string
    
def XMLtoPlainText(string):
    string = string.replace('{i}', '')
    string = string.replace('{/i}', '')
    string = string.replace('{b}', '')
    string = string.replace('{/b}', '')
    string = string.replace('{u}', '')
    string = string.replace('{/u}', '')
    return string
    
def RTFtoXML(string):
    string = string.replace('<i>', '{i}')
    string = string.replace('</i>', '{/i}')
    string = string.replace('<b>', '{b}')
    string = string.replace('</b>', '{/b}')
    string = string.replace('<u>', '{u}')
    string = string.replace('</u>', '{/u}')
    return string

def HighASCIItoHTML(string):
    string = string.replace('á', '&aacute;')
    string = string.replace('é', '&eacute;')
    string = string.replace('í', '&iacute;')
    string = string.replace('ó', '&oacute;')
    string = string.replace('ú', '&uacute;')
#    string = string.replace('\t', '&#9;')
    return string
