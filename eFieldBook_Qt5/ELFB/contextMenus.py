from PyQt6 import QtGui
from ELFB import dataIndex, linksMenu

def __init__(self, parent=dataIndex.fldbk):
    self.fldbk = dataIndex.fldbk

def clearContextMenu(fldbk, field):
    try:
      if field == 'lDialect':
          del(fldbk.lDialect.dialectMenu)
      if field == 'lL1Definition':
          del(fldbk.L1Definition.L1DefinitionMenu)
      if field == 'lL2Definition':
          del(fldbk.L2Definition.L2DefinitionMenu)
      if field == 'lGrammar':
          del(fldbk.lGrammar.crossrefMenu)
    except AttributeError:
        pass

def updateContextMenu(fldbk, field, linksList, altList=None):
      if field == 'lDialect':
          try:
              fldbk.lDialect.dialectMenu.clear()
          except AttributeError:
              fldbk.lDialect.dialectMenu = linksMenu.linksMenu(fldbk)
          actionHeader = 'Find...'
          fldbk.lDialect.dialectMenu.addAction(actionHeader)
          for i in range(0, len(linksList)):
              actionLink = 'action' + linksList[i]
              alternate = "   " + altList[i]
              setattr(fldbk, actionLink, QtGui.QAction(alternate, fldbk.lDialect.dialectMenu))
              action = getattr(fldbk, actionLink)
              fldbk.lDialect.dialectMenu.addAction(action)
              action.setData(linksList[i])
              action.triggered.connect(fldbk.lDialect.dialectMenu.linkSelected)
              
      if field == 'lL1Definition':
          try:
              fldbk.lL1Definition.L1DefinitionMenu.clear()
          except AttributeError:
              fldbk.lL1Definition.L1DefinitionMenu = linksMenu.linksMenu(fldbk)
          actionHeader = 'Find...'
          fldbk.lL1Definition.L1DefinitionMenu.addAction(actionHeader)
          for i in range(0, len(linksList)):
              actionLink = 'action' + linksList[i]
              alternate = "   " + altList[i]
              setattr(fldbk, actionLink, QtGui.QAction(alternate, fldbk.lL1Definition.L1DefinitionMenu))
              action = getattr(fldbk, actionLink)
              fldbk.lL1Definition.L1DefinitionMenu.addAction(action)
              action.setData(linksList[i])
              action.triggered.connect(fldbk.lL1Definition.L1DefinitionMenu.linkSelected)
          
          try:
              fldbk.lL2Definition.L2DefinitionMenu.clear()
          except AttributeError:
              fldbk.lL2Definition.L2DefinitionMenu = linksMenu.linksMenu(fldbk)
          actionHeader = 'Find...'
          fldbk.lL2Definition.L2DefinitionMenu.addAction(actionHeader)
          for i in range(0, len(linksList)):
              actionLink = 'action' + linksList[i]
              alternate = "   " + altList[i]
              setattr(fldbk, actionLink, QtGui.QAction(alternate, fldbk.lL2Definition.L2DefinitionMenu))
              action = getattr(fldbk, actionLink)
              fldbk.lL2Definition.L2DefinitionMenu.addAction(action)
              action.setData(linksList[i])
              action.triggered.connect(fldbk.lL2Definition.L2DefinitionMenu.linkSelected)
    
      if field == 'lGrammar':
          try:
              fldbk.lGrammar.crossrefMenu.clear()
          except AttributeError:
              fldbk.lGrammar.crossrefMenu = linksMenu.linksMenu(fldbk)
          soundsList = []
          soundName = []
          refList = []
          refName = []
          for i in range(0, len(linksList)):             
              if 'M' in linksList[i]:
                  soundsList.append(linksList[i])
                  soundName.append(altList[i])
              else:
                  refList.append(linksList[i])
                  refName.append(altList[i])
          if len(soundsList) != 0:
              actionHeader = 'Play...'
              fldbk.lGrammar.crossrefMenu.addAction(actionHeader)
              for j in range(0, len(soundsList)):
                  if soundsList[j]:
                      actionLink = 'action' + soundsList[j]
                      alternative = "   " + soundName[j]
                      setattr(fldbk, actionLink, QtGui.QAction(alternative, fldbk.lGrammar.crossrefMenu))
                      action = getattr(fldbk, actionLink)
                      fldbk.lGrammar.crossrefMenu.addAction(action)
                      action.setData(soundsList[j])
                      action.triggered.connect(fldbk.lGrammar.crossrefMenu.linkSelected)
          if len(refList) != 0:
              actionHeader = 'Find...'
              fldbk.lGrammar.crossrefMenu.addAction(actionHeader)
              for k in range(0, len(refList)):
                  if refList[k]:
                      actionLink = 'action' + refList[k]
                      alternative = "   " + refName[k]
                      setattr(fldbk, actionLink, QtGui.QAction(alternative, fldbk.lGrammar.crossrefMenu))
                      action = getattr(fldbk, actionLink)
                      fldbk.lGrammar.crossrefMenu.addAction(action)
                      action.setData(refList[k])
                      action.triggered.connect(fldbk.lGrammar.crossrefMenu.linkSelected)              
          
def buildContextMenu(fldbk, field, linksList, altList=None):
        if field == 'lDialect':
            try:
                del(fldbk.lDialect.dialectMenu)
            except AttributeError:
                pass
            fldbk.lDialect.dialectMenu = linksMenu.linksMenu(fldbk)
        if field == 'lL1Definition' or field == 'L2Definition':
            try:
                del(fldbk.lL1Definition.L1DefinitionMenu)
            except AttributeError:
                pass
            fldbk.lL1Definition.L1DefinitionMenu = linksMenu.linksMenu(fldbk)

            try:
                del(fldbk.lL2Definition.L2DefinitionMenu)
            except AttributeError:
                pass
            fldbk.lL2Definition.L2DefinitionMenu = linksMenu.linksMenu(fldbk)

        if field == 'lGrammar':
            try:
                del(fldbk.lGrammar.crossrefMenu)
            except AttributeError:
                pass
            fldbk.lGrammar.crossrefMenu = linksMenu.linksMenu(fldbk)

        updateContextMenu(fldbk, field, linksList, altList)

def openContextMenu(fldbk, field, position):
        try:
            if field == 'lDialect':
                fldbk.lDialect.dialectMenu.exec(fldbk.lDialect.mapToGlobal(position))
            if field == 'lL1Definition':
                fldbk.lL1Definition.L1DefinitionMenu.exec(fldbk.lL1Definition.mapToGlobal(position))
            if field == 'lL2Definition':
                fldbk.lL2Definition.L2DefinitionMenu.exec(fldbk.lL2Definition.mapToGlobal(position))
            if field == 'lGrammar':
                fldbk.lGrammar.crossrefMenu.exec(fldbk.lGrammar.mapToGlobal(position))
        except AttributeError:
            pass
