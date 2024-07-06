from ELFB import dataIndex
import xml.etree.ElementTree as etree


def cleanExElement(node):
    print('entering cleanExElement')
    line = node.findtext('Line')
    lineNode = node.find('Line')
    if '\n' in line:
        lineNode = removeExtraneousReturns(lineNode, line)
        
    L1Gloss = node.findtext('L1Gloss')
    L1GlossNode = node.find('L1Gloss')
    if '\n' in L1Gloss:
        L1GlossNode = removeExtraneousReturns(L1GlossNode, L1Gloss)

    if node.find('L2Gloss') != None:
        L2Gloss = node.findtext('L2Gloss')
        L2GlossNode = node.find('L2Gloss')
        if '\n' in L2Gloss:
            L2GlossNode = removeExtraneousReturns(L2GlossNode, L2Gloss)

    Mrph = node.findtext('Mrph')
    MrphNode = node.find('Mrph')
    if '\n' in Mrph:
        MrphNode = removeExtraneousReturns(MrphNode, Mrph)

    ILEG = node.findtext('ILEG')
    ILEGNode = node.find('ILEG')
    if '\n' in ILEG:
        ILEGNode = removeExtraneousReturns(ILEGNode, ILEG)

    return node
    
def cleanLexElement(node):
    print('entering cleanLexElement')
    for child in node.iter('Def'):
        L1Def = child.findtext('L1')
        L1DefNode = child.find('L1')
        if '\n' in L1Def:
            child = removeExtraneousReturns(L1DefNode, L1Def)

        if child.find('L2') != None:
            L2Def = child.findtext('L2')
            L2DefNode = child.find('L2')
            if '\n' in L2Def:
                child = removeExtraneousReturns(L2DefNode, L2Def)

    return node
    
def cleanOrthoElement(node):
    print('entering cleanOrthoElement')
    text = node.text
    if '\n' in text:
        node = removeExtraneousReturns(node, text)
    return node
    
def cleanSortElement(node):
    print('entering cleanSortElement')
    text = node.text
    if '\n' in text:
        node = removeExtraneousReturns(node, text)
    return node
    
def removeExtraneousReturns(node, text):
    print('entering removeExtraneousReturns')
    text = text.replace('\n',  ' ')
    node.text = removeExtraneousSpaces(text)
    print(etree.tostring(node,  encoding='unicode'))
    dataIndex.unsavedEdit = 1
    return node
    
def removeExtraneousSpaces(text):
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text
