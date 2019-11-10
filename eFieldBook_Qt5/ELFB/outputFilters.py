from ELFB import dataIndex

'''converts XML to various formats for output or between
formats for different views in the database'''

def lexToText(nodeID):
    node = dataIndex.lexDict[nodeID]
    entryWord = node.find('Orth').text
    pos = node.find('POS').text
    dfn = node.find('Def/L1').text
    newText = entryWord + " (" + pos + ") " + dfn + " [" + nodeID + "]"
    return newText
    
def egToText(nodeID):
    print(nodeID)
