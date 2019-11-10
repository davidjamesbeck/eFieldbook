###### codes for getting stuff out of the database #####

from ELFB import dataIndex

def outputLexiconToCSV(fldbk):
    if fldbk.tabWidget.currentIndex() == 1: #Lexicon tab
        navModel = fldbk.lLexNav.model()
        LexList = []
        for i in range(0, navModel.rowCount()):
            LexID = navModel.index(i,0).data(32)
            LexList.append(LexID)
        forms = ''
        for ID in LexList:
            node = dataIndex.lexDict[ID]
            entry = node.findtext("Orth")
            entry += ", " + node.findtext("Def/L1")
            entry += ", " + node.attrib.get('Update') + '\n'
            forms += entry
        saveFile = open('/Users/David/Desktop/CSVOutput.txt', "w", encoding = "UTF-8")
        saveFile.write(forms)
        saveFile.close() 
