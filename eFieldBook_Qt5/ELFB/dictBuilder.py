'''build additional dictionaries to index examples and recordings'''

from ELFB import dataIndex

def exDictBuilder(fldbk):
    dataIndex.exDict.clear()
    for node in dataIndex.root.iter('Ex'):
      ExID = node.attrib.get('ExID')
      dataIndex.exDict[ExID] = node
      
def mediaDictBuilder(fldbk):  
    dataIndex.mediaDict.clear()  
    for node in dataIndex.root.iter('Media'):
      MedID = node.attrib.get('MedID')
      dataIndex.mediaDict[MedID] = node

def speakerDictBuilder(fldbk):    
    dataIndex.speakerDict.clear()  
    for node in dataIndex.root.iter('Speaker'):
      spkrID = node.attrib.get('SCode')
      dataIndex.speakerDict[spkrID] = node

def rschrDictBuilder(fldbk):    
    dataIndex.rschrDict.clear()  
    for node in dataIndex.root.iter('Rschr'):
      rschr = node.attrib.get('RCode')
      dataIndex.rschrDict[rschr] = node
