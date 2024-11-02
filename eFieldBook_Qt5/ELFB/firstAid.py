'''scripts for repairing the database'''

from ELFB import dataIndex
import xml.etree.ElementTree as etree

def run_Command():
    print("entering run_command")
    fix_spkr()
    
def fix_spkr():
    print('entering fix_spkr')
    lexDict = dataIndex.lexDict
    entryList = lexDict.keys()
#    print(entryList)
    for key in entryList:
        entry = lexDict[key]
        oldSpkr = entry.attrib.get('Spkr')
#        print(oldSpkr)
        if len(oldSpkr) > 2:
            newSpkr = oldSpkr.split(',')[0]
            entry.set('Confirmed', oldSpkr)
            entry.set('Spkr', newSpkr)
            print(etree.tostring(entry, encoding='unicode'))
    
