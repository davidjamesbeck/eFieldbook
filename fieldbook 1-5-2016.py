# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import os
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow
from .Ui_fieldbook import Ui_Fieldbook
from ELFB import dataIndex, cardLoader, Alphabetizer, cardStack, menus, navLists, dictBuilder, contextMenus, NumberedLineEdit, metaDataTableFillers, formattingHandlers
from ELFB.focusOutFilter import focusOutFilter, dialectFilter, borrowFilter
from ELFB.GrmField import GrmField
from ELFB.DefTable import DefTable
from ELFB.EgTable import EgTable
from ELFB.HTMLDelegate import HTMLDelegate
from ELFB import navBtns, soundBtns, lexOnlyBtns, textOnlyBtns, egOnlyBtns, metaDataBtns, indexOnlyBtns, lexSearchBtns, newTextBtns, searchOnlyBtns, dsetOnlyBtns, Orthographies
from ELFB.palettes import RecordBrowser
from ELFB import MyElementTree
from os import path

class MainWindow(QMainWindow, Ui_Fieldbook):
    """
    Class documentation goes here.
    """
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(MainWindow, self).__init__(parent)
        QtWidgets.QApplication.setActiveWindow(self)
        QtWidgets.QApplication.setKeyboardInputInterval(600)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setWeight(50)
        QtWidgets.QApplication.setFont(font)
        self.ui = Ui_Fieldbook
        self.settings = QtCore.QSettings()
        self.Alphabetizer = Alphabetizer
        self.setupUi(self)
        dataIndex.fldbk = self
        dataIndex.homePath = path.expanduser("~")
        self.setStyleSheet("QMessageBox QPushButton {border: 0px solid black;font-size: 10pts;padding: 0 5 0 5;"
                                                    "border-radius: 4px;min-width: 50px;min-height: 23px;"
                                                    "max-width: 180px;max-height: 23px;background: #6698FF;color: white;}")

        '''Load XML'''
        '''determine the file to be opened on startup'''
        fname = None
        if self.settings.value('LastFile') and QtCore.QFile.exists(self.settings.value('LastFile')):
            '''check to see if an existing file has been opened previously'''
            fname = self.settings.value('LastFile')
            dataIndex.sourceFile = fname
        else:
            '''if there is no such file, ask for a file to open'''
            openFileDialog = QtWidgets.QFileDialog(self)
            filePath = openFileDialog.directory().currentPath()
            openFileDialog.setDirectory(filePath)
            fname = openFileDialog.getOpenFileName(self, "Open...","","XML (*.xml)")
            if fname:
                fname = fname[0]
                dataIndex.sourceFile = fname
                if fname in dataIndex.recentFile:
                    del dataIndex.recentFile[dataIndex.recentFile.index(fname)]
                dataIndex.recentFile.insert(0, fname)
                dataIndex.unsavedEdit = 1
        try:
            dataIndex.xmltree = MyElementTree.parse(fname)
        except (TypeError, PermissionError, FileNotFoundError):
            '''error arises if fname has not been set'''
            blankDbFile = QtCore.QFile(dataIndex.rootPath + '/ELFB/newFileTemplate.xml')
            blankDbFile.open(QtCore.QIODevice.OpenModeFlag.ReadOnly | QtCore.QIODevice.OpenModeFlag.Text)
            dataIndex.xmltree = MyElementTree.parse(blankDbFile)
            dataIndex.sourceFile = 'blank database'
        self.giveWindowTitle()
        dataIndex.root = dataIndex.xmltree.getroot()
        dataIndex.lastText = dataIndex.root.attrib.get('LastText')
        dataIndex.lastLex = dataIndex.root.attrib.get('LastLex')
        dataIndex.lastEG = dataIndex.root.attrib.get('LastEG')
        dataIndex.lastDset = dataIndex.root.attrib.get('LastDset')
        navLists.navListBuilderLex(self)
        navLists.navListBuilderText(self)
        navLists.navListBuilderData(self)
        dictBuilder.dictionaryBuilder(self)
        
        '''SET UP MENUS'''
        self.actionFind.setEnabled(0)
        self.actionFind_Again.setEnabled(0)
        self.actionFuzzy_Find.setEnabled(0)
        self.actionFuzzy_Find_Again.setEnabled(0)
        self.actionNewCard.setEnabled(0)
        self.actionDelCard.setEnabled(0)
        self.actionQuit.setShortcut(QtCore.Qt.Key_Control + QtCore.Qt.Key_Q)
        
        '''BUILD ICONS AND RESOURCES'''
        controlBar = dataIndex.rootPath + '/ELFB/ui/rsrc/ControlPanel.png'
        self.lControlBar.setStyleSheet('QToolButton {background: transparent;'
                'min-width: 32px;'
                'min-height: 32px;'
                'max-width: 32px;'
                'max-height: 32px;'
                'padding: 0px;}'
            'QFrame {border: 1px solid gray; '
                'border: 0px solid black;'
                'border-radius: 8px;'
                'padding: 0px;'
                'background-image: url("%s");}' %controlBar)
        self.eControlBar.setStyleSheet('QToolButton {background: transparent;'
                'min-width: 32px;'
                'min-height: 32px;'
                'max-width: 32px;'
                'max-height: 32px;'
                'padding: 0px;}'
            'QFrame {border: 1px solid gray; '
                'border: 0px solid black;'
                'border-radius: 8px;'
                'padding: 0px;'
                'background-image: url("%s");}' %controlBar)
        self.tControlBar.setStyleSheet('QToolButton {min-width: 32px;'
                'min-height: 32px;'
                'max-width: 32px;'
                'max-height: 32px;'
                'padding: 0px;}'
            'QFrame {border: 1px solid gray; '
                'border: 0px solid black;'
                'border-radius: 8px;'
                'padding: 0px;'
                'background-image: url("%s");}' %controlBar)
        self.dControlBar.setStyleSheet('QToolButton {background: transparent;'
                'min-width: 32px;'
                'min-height: 32px;'
                'max-width: 32px;'
                'max-height: 32px;'
                'padding: 0px;}'
            'QFrame {border: 1px solid gray; '
                'border: 0px solid black;'
                'border-radius: 8px;'
                'padding: 0px;'
                'background-image: url("%s");}' %controlBar)
        self.cResultsControlsBox.setStyleSheet('QPushButton {min-height: 25px;'
                'min-width: 60px;'
                'background: #6698FF;'
                'color: white;'   
                'border: 0px solid black;'
                'border-radius: 4px;'
                'padding: 0 0 0 0;'
                'margin: 0 0 0 0;}'
            'QPushButton:pressed {background: #1E90FF; border: 2px outset #1E90FF;}'
            'QToolButton {background: transparent;'
                'min-width: 32px;'
                'min-height: 32px;'
                'max-width: 32px;'
                'max-height: 32px;'
                'padding: 0px;}'
            'QGroupBox {border: 1px solid gray; '
                'border: 0px solid black;'
                'border-radius: 8px;'
                'padding: 0px;'
                'background-image: url("%s");}' %controlBar)
        navIconSize = QtCore.QSize(32, 32)
        rtnIcon = QtGui.QIcon(dataIndex.rootPath + '/ELFB/ui/rsrc/RtnBtn.png')
        self.lRtnBtn.setIcon(rtnIcon)
        self.lRtnBtn.setIconSize(navIconSize)
        self.eRtnBtn.setIcon(rtnIcon)
        self.eRtnBtn.setIconSize(navIconSize)
        self.tRtnBtn.setIcon(rtnIcon)
        self.tRtnBtn.setIconSize(navIconSize)
        self.dRtnBtn.setIcon(rtnIcon)
        self.dRtnBtn.setIconSize(navIconSize)
        prevIcon = QtGui.QIcon(dataIndex.rootPath + '/ELFB/ui/rsrc/PrevBtn.png')
        self.lPrevBtn.setIcon(prevIcon)
        self.lPrevBtn.setIconSize(navIconSize)
        self.ePrevBtn.setIcon(prevIcon)
        self.ePrevBtn.setIconSize(navIconSize)
        self.tPrevBtn.setIcon(prevIcon)
        self.tPrevBtn.setIconSize(navIconSize)
        self.dPrevBtn.setIcon(prevIcon)
        self.dPrevBtn.setIconSize(navIconSize)
        beginIcon = QtGui.QIcon(dataIndex.rootPath + '/ELFB/ui/rsrc/BeginBtn2.png')
        self.lBeginBtn.setIcon(beginIcon)
        self.lBeginBtn.setIconSize(navIconSize)
        self.eBeginBtn.setIcon(beginIcon)
        self.eBeginBtn.setIconSize(navIconSize)
        self.tBeginBtn.setIcon(beginIcon)
        self.tBeginBtn.setIconSize(navIconSize)
        self.dBeginBtn.setIcon(beginIcon)
        self.dBeginBtn.setIconSize(navIconSize)
        fwdIcon = QtGui.QIcon(dataIndex.rootPath + '/ELFB/ui/rsrc/FwdBtn.png')
        self.lFwdBtn.setIcon(fwdIcon)
        self.lFwdBtn.setIconSize(navIconSize)
        self.eFwdBtn.setIcon(fwdIcon)
        self.eFwdBtn.setIconSize(navIconSize)
        self.tFwdBtn.setIcon(fwdIcon)
        self.tFwdBtn.setIconSize(navIconSize)
        self.dFwdBtn.setIcon(fwdIcon)
        self.dFwdBtn.setIconSize(navIconSize)
        nextIcon = QtGui.QIcon(dataIndex.rootPath + '/ELFB/ui/rsrc/NextBtn.png')
        self.lNextBtn.setIcon(nextIcon)
        self.lNextBtn.setIconSize(navIconSize)
        self.eNextBtn.setIcon(nextIcon)
        self.eNextBtn.setIconSize(navIconSize)
        self.tNextBtn.setIcon(nextIcon)
        self.tNextBtn.setIconSize(navIconSize)
        self.dNextBtn.setIcon(nextIcon)
        self.dNextBtn.setIconSize(navIconSize)
        endIcon = QtGui.QIcon(dataIndex.rootPath + '/ELFB/ui/rsrc/EndBtn.png')
        self.lEndBtn.setIcon(endIcon)
        self.lEndBtn.setIconSize(navIconSize)
        self.eEndBtn.setIcon(endIcon)
        self.eEndBtn.setIconSize(navIconSize)
        self.tEndBtn.setIcon(endIcon)
        self.tEndBtn.setIconSize(navIconSize)
        self.dEndBtn.setIcon(endIcon)
        self.dEndBtn.setIconSize(navIconSize)
        soundIconSize = QtCore.QSize(23, 23)
        soundIcon = QtGui.QIcon(dataIndex.rootPath + '/ELFB/ui/rsrc/SpeakerBtn.png')
        self.lPlaySoundBtn.setStyleSheet('background: transparent; padding: 0px; min-width: 23px; min-height: 23px;')
        self.lPlaySoundBtn.setIcon(soundIcon)
        self.lPlaySoundBtn.setIconSize(soundIconSize)
        self.ePlaySoundBtn.setStyleSheet('background: transparent; padding: 0px; min-width: 23px; min-height: 23px;')
        self.ePlaySoundBtn.setIcon(soundIcon)
        self.ePlaySoundBtn.setIconSize(soundIconSize)   
        self.tPlaySoundBtn.setStyleSheet('background: transparent; padding: 0px; min-width: 23px; min-height: 23px;')
        self.tPlaySoundBtn.setIcon(soundIcon)
        self.tPlaySoundBtn.setIconSize(soundIconSize)    
        self.dPlaySoundBtn.setStyleSheet('background: transparent; padding: 0px; min-width: 23px; min-height: 23px;')
        self.dPlaySoundBtn.setIcon(soundIcon)
        self.dPlaySoundBtn.setIconSize(soundIconSize)
        self.mPlaySoundBtn.setStyleSheet('border: 0px; background: transparent; padding: 0px; min-width: 23px; min-height: 23px;')
        self.mPlaySoundBtn.setIcon(soundIcon)
        self.mPlaySoundBtn.setIconSize(soundIconSize)
        infoIconSize = QtCore.QSize(18, 18)
        infoIcon = QtGui.QIcon(dataIndex.rootPath + '/ELFB/ui/rsrc/InfoBtn.png')
        self.lSoundMetaBtn.setStyleSheet('background: transparent; padding: 0px; min-width: 18px; min-height: 18px;')
        self.lSoundMetaBtn.setIcon(infoIcon)
        self.lSoundMetaBtn.setIconSize(infoIconSize)       
        self.eSoundMetaBtn.setStyleSheet('background: transparent; padding: 0px; min-width: 18px; min-height: 18px;')
        self.eSoundMetaBtn.setIcon(infoIcon)
        self.eSoundMetaBtn.setIconSize(infoIconSize)         
        self.tSoundMetaBtn.setStyleSheet('background: transparent; padding: 0px; min-width: 18px; min-height: 18px;')
        self.tSoundMetaBtn.setIcon(infoIcon)
        self.tSoundMetaBtn.setIconSize(infoIconSize)   
        self.dSoundMetaBtn.setStyleSheet('background: transparent; padding: 0px; min-width: 18px; min-height: 18px;')
        self.dSoundMetaBtn.setIcon(infoIcon)
        self.dSoundMetaBtn.setIconSize(infoIconSize) 
        newCardIconSize = QtCore.QSize(40, 40)
        newCardIcon = QtGui.QIcon(dataIndex.rootPath + '/ELFB/ui/rsrc/New.png')
        self.lNewBtn.setStyleSheet('QToolButton {border: 0px; background: transparent;'
            ' padding: 0px; min-width: 40px; min-height: 40px;}'
            'QToolButton:pressed {border: 3px outset transparent;}')
        self.lNewBtn.setIcon(newCardIcon)
        self.lNewBtn.setIconSize(newCardIconSize) 
        self.tNewTextBtn.setStyleSheet('QToolButton {border: 0px; background: transparent;'
            ' padding: 0px; min-width: 40px; min-height: 40px;}'
            'QToolButton:pressed {border: 3px outset transparent;}')
        self.tNewTextBtn.setIcon(newCardIcon)
        self.tNewTextBtn.setIconSize(newCardIconSize)  
        self.eNewEgBtn.setStyleSheet('QToolButton {border: 0px; background: transparent;'
            ' padding: 0px; min-width: 40px; min-height: 40px;}'
            'QToolButton:pressed {border: 3px outset transparent;}')
        self.eNewEgBtn.setIcon(newCardIcon)
        self.eNewEgBtn.setIconSize(newCardIconSize)    
        self.dNewDsetBtn.setStyleSheet('QToolButton {border: 0px; background: transparent;'
            ' padding: 0px; min-width: 40px; min-height: 40px;}'
            'QToolButton:pressed {border: 3px outset transparent;}')
        self.dNewDsetBtn.setIcon(newCardIcon)
        self.dNewDsetBtn.setIconSize(newCardIconSize)  
        clipIcon =  QtGui.QIcon(dataIndex.rootPath + '/ELFB/ui/rsrc/Clip.png')
        self.lClipBtn.setStyleSheet('QToolButton {border: 0px; background: transparent;'
            'padding: 0px; min-width: 40px; min-height: 40px;}'
            'QToolButton:pressed {border: 3px outset transparent;}')
        self.lClipBtn.setIcon(clipIcon)        
        self.lClipBtn.setIconSize(newCardIconSize) 
        self.tClipBtn.setStyleSheet('QToolButton {border: 0px; background: transparent;'
            ' padding: 0px; min-width: 40px; min-height: 40px;}'
            'QToolButton:pressed {border: 3px outset transparent;}')
        self.tClipBtn.setIcon(clipIcon)        
        self.tClipBtn.setIconSize(newCardIconSize)  
        self.eCopyLineBtn.setStyleSheet('QToolButton {border: 0px; background: transparent;'
            ' padding: 0px; min-width: 40px; min-height: 40px;}'
            'QToolButton:pressed {border: 3px outset transparent;}')
        self.eCopyLineBtn.setIcon(clipIcon)        
        self.eCopyLineBtn.setIconSize(newCardIconSize) 
        duplicateIcon =  QtGui.QIcon(dataIndex.rootPath + '/ELFB/ui/rsrc/duplicate.png')
        self.eDuplicateBtn.setStyleSheet('QToolButton {border: 0px; background: transparent;'
            ' padding: 0px; min-width: 40px; min-height: 40px;}'
            'QToolButton:pressed {border: 3px outset transparent;}')
        self.eDuplicateBtn.setIcon(duplicateIcon)        
        self.eDuplicateBtn.setIconSize(newCardIconSize) 
        
        '''SET UP TABS AND SUB-CLASSED WIDGETS'''
        
        '''TextEdits'''
        
        '''Home tab'''
        dbTitle = dataIndex.root.attrib.get('Dbase')
        dbTitle = formattingHandlers.XMLtoRTF(dbTitle)
        self.hTitle.setText(dbTitle)
        self.hTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.filter = focusOutFilter(self.hTitle)
        self.hTitle.installEventFilter(self.filter)
        self.hTitle.textChanged.connect(self.flagUnsavedEdits)
    
        lang = dataIndex.root.attrib.get('Language')
        self.hLanguage.setPlainText(lang)
        self.filter = focusOutFilter(self.hLanguage)
        self.hLanguage.installEventFilter(self.filter)
        self.hLanguage.textChanged.connect(self.flagUnsavedEdits)
    
        family = dataIndex.root.attrib.get('Family')
        self.hFamily.setPlainText(family)
        self.filter = focusOutFilter(self.hFamily)
        self.hFamily.installEventFilter(self.filter)
        self.hFamily.textChanged.connect(self.flagUnsavedEdits)
        
        population = dataIndex.root.attrib.get('Population')
        self.hPopulation.setPlainText(population)
        self.filter = focusOutFilter(self.hPopulation)
        self.hPopulation.installEventFilter(self.filter)
        self.hPopulation.textChanged.connect(self.flagUnsavedEdits)
        
        location = dataIndex.root.attrib.get('Location')
        self.hLocation.setPlainText(location)
        self.filter = focusOutFilter(self.hLocation)
        self.hLocation.installEventFilter(self.filter)
        self.hLocation.textChanged.connect(self.flagUnsavedEdits)
        
        iso = dataIndex.root.attrib.get('ISO')
        self.hISO.setPlainText(iso)
        self.filter = focusOutFilter(self.hISO)
        self.hISO.installEventFilter(self.filter)
        self.hISO.textChanged.connect(self.flagUnsavedEdits)
        
        '''Lexicon tab'''
        
        #Lexicographic info
    
        self.filter = focusOutFilter(self.lOrthography)
        self.lOrthography.installEventFilter(self.filter)
        self.lOrthography.textChanged.connect(self.flagUnsavedEdits)
    
        self.filter = focusOutFilter(self.lPOS)
        self.lPOS.installEventFilter(self.filter)
        self.lPOS.textChanged.connect(self.flagUnsavedEdits)
    
        self.filter = focusOutFilter(self.lRegister)
        self.lRegister.installEventFilter(self.filter)
        self.lRegister.textChanged.connect(self.flagUnsavedEdits)
    
        self.filter = focusOutFilter(self.lIPA)
        self.lIPA.installEventFilter(self.filter)
        self.lIPA.textChanged.connect(self.flagUnsavedEdits)
    
        self.filter = dialectFilter(self.lDialect)
        self.lDialect.installEventFilter(self.filter)
        self.lDialect.textChanged.connect(self.flagUnsavedEdits)
        self.filter = borrowFilter(self.lBrrw)
        self.lBrrw.installEventFilter(self.filter)
        self.lBrrw.textChanged.connect(self.flagUnsavedEdits)
    
        def dialectMenu(position):
          field = 'lDialect'
          contextMenus.openContextMenu(self, field, position)
          
        self.lDialect.customContextMenuRequested.connect(dialectMenu)
    
        self.filter = focusOutFilter(self.lLiteral)
        self.lLiteral.installEventFilter(self.filter)
        self.lLiteral.textChanged.connect(self.flagUnsavedEdits)
    
        #Metadata
    
        self.filter = focusOutFilter(self.lSource)
        self.lSource.installEventFilter(self.filter)
        self.lSource.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.lResearcher)
        self.lResearcher.installEventFilter(self.filter)
        self.lResearcher.textChanged.connect(self.flagUnsavedEdits)
    
        self.filter = focusOutFilter(self.lDate)
        self.lDate.installEventFilter(self.filter)
        self.lDate.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.lUpdated)
        self.lUpdated.installEventFilter(self.filter)
        self.lUpdated.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.lConfirmed)
        self.lConfirmed.installEventFilter(self.filter)
        self.lConfirmed.textChanged.connect(self.flagUnsavedEdits)
    
        #Grammar
        self.lGrammar = GrmField(self.lGrammarBox)
        self.lGrammar.setGeometry(6, 22, 182, 87)
        self.lGrammar.setToolTip(QtWidgets.QApplication.translate("Fieldbook", "Grammatical information, comparisons, and cross-refs.\n"
        "Doubleclick to edit.", None))
        
        def grammarMenu(position):
          field = 'lGrammar'
          contextMenus.openContextMenu(self, field, position)
    
        self.lGrammar.customContextMenuRequested.connect(grammarMenu)
    
        #Notes
        
        self.filter = focusOutFilter(self.lNotes)
        self.lNotes.installEventFilter(self.filter)
        self.lNotes.textChanged.connect(self.flagUnsavedEdits)
    
        #Indices
        
        self.filter = focusOutFilter(self.lPrimaryIndex)
        self.lPrimaryIndex.installEventFilter(self.filter)
        self.lPrimaryIndex.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.lSecondaryIndex)
        self.lSecondaryIndex.installEventFilter(self.filter)
        self.lSecondaryIndex.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.lKeywordIndex)
        self.lKeywordIndex.installEventFilter(self.filter)
        self.lKeywordIndex.textChanged.connect(self.flagUnsavedEdits)
        
        '''definitions tables'''
        
        self.lL1Definition = DefTable(self.lL1Box)
        self.lL2Definition = DefTable(self.lL2Box)
        self.lL1Definition.setToolTip(QtWidgets.QApplication.translate("Fieldbook", "Definitions in primary working language.\n"
        "Doubleclick definition to edit, click example\nto go to analysis.", None))
        self.lL2Definition.setToolTip(QtWidgets.QApplication.translate("Fieldbook", "Definitions in secondary working language. \n"
        "Doubleclick definition to edit, click example\nto go to analysis.", None))
    
        def L1Menu(position):
          field = 'lL1Definition'
          contextMenus.openContextMenu(self, field, position)
    
        self.lL1Definition.customContextMenuRequested.connect(L1Menu)
        
        def L2Menu(position):
          field = 'lL2Definition'
          contextMenus.openContextMenu(self,  field, position)
        
        self.lL2Definition.customContextMenuRequested.connect(L2Menu)
        
        '''text fields'''
        '''Texts tab'''
        self.tNewTitle.setVisible(0)
        self.tNewTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tPortalBox.setVisible(0)
        self.tNewMetadataBox.setVisible(0)
        self.tNewTextComments.setVisible(0)
        self.tNewTextBox.setVisible(0)        
        self.filter = focusOutFilter(self.tSource)
        self.tSource.installEventFilter(self.filter)
        self.tSource.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.tResearcher)
        self.tResearcher.installEventFilter(self.filter)
        self.tResearcher.textChanged.connect(self.flagUnsavedEdits)
    
        self.filter = focusOutFilter(self.tDate)
        self.tDate.installEventFilter(self.filter)
        self.tDate.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.tUpdated)
        self.tUpdated.installEventFilter(self.filter)
        self.tUpdated.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.tTranscriber)
        self.tTranscriber.installEventFilter(self.filter)
        self.tTranscriber.textChanged.connect(self.flagUnsavedEdits)
       
        self.filter = focusOutFilter(self.tNotes)
        self.tNotes.installEventFilter(self.filter)
        self.tNotes.textChanged.connect(self.flagUnsavedEdits)
    
        self.filter = focusOutFilter(self.tTitle)
        self.tTitle.installEventFilter(self.filter)
        self.tTitle.textChanged.connect(self.flagUnsavedEdits)
        self.tTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        '''Examples tab'''
        self.filter = focusOutFilter(self.eLine)
        self.eLine.installEventFilter(self.filter)
        self.eLine.textChanged.connect(self.flagUnsavedEdits)
     
        self.filter = focusOutFilter(self.eL1Gloss)
        self.eL1Gloss.installEventFilter(self.filter)
        self.eL1Gloss.textChanged.connect(self.flagUnsavedEdits)
     
        self.filter = focusOutFilter(self.eL2Gloss)
        self.eL2Gloss.installEventFilter(self.filter)
        self.eL2Gloss.textChanged.connect(self.flagUnsavedEdits)
     
        self.filter = focusOutFilter(self.eNotes)
        self.eNotes.installEventFilter(self.filter)
        self.eNotes.textChanged.connect(self.flagUnsavedEdits)
     
        self.filter = focusOutFilter(self.eKeywords)
        self.eKeywords.installEventFilter(self.filter)
        self.eKeywords.textChanged.connect(self.flagUnsavedEdits)
     
        self.filter = focusOutFilter(self.eSource)
        self.eSource.installEventFilter(self.filter)
        self.eSource.textChanged.connect(self.flagUnsavedEdits)
     
        self.filter = focusOutFilter(self.eResearcher)
        self.eResearcher.installEventFilter(self.filter)
        self.eResearcher.textChanged.connect(self.flagUnsavedEdits)
     
        self.filter = focusOutFilter(self.eDate)
        self.eDate.installEventFilter(self.filter)
        self.eDate.textChanged.connect(self.flagUnsavedEdits)
     
        self.filter = focusOutFilter(self.eUpdated)
        self.eUpdated.installEventFilter(self.filter)
        self.eUpdated.textChanged.connect(self.flagUnsavedEdits)
     
        self.filter = focusOutFilter(self.eSourceText)
        self.eSourceText.installEventFilter(self.filter)
        self.eSourceText.textChanged.connect(self.flagUnsavedEdits)
     
        self.filter = focusOutFilter(self.eTimeCode)
        self.eTimeCode.installEventFilter(self.filter)
        self.eTimeCode.textChanged.connect(self.flagUnsavedEdits)
        
        '''create table for analyses'''
        self.eAnalysis = EgTable(self.eExScrollArea)
        self.eAnalysis.setGeometry(0,54,1900,215)
        
        '''Datasets tab'''
        self.filter = focusOutFilter(self.dSource)
        self.dSource.installEventFilter(self.filter)
        self.dSource.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.dResearcher)
        self.dResearcher.installEventFilter(self.filter)
        self.dResearcher.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.dDate)
        self.dDate.installEventFilter(self.filter)
        self.dDate.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.dKeywords)
        self.dKeywords.installEventFilter(self.filter)
        self.dKeywords.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.dNotes)
        self.dNotes.installEventFilter(self.filter)
        self.dNotes.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.dData)
        self.dData.installEventFilter(self.filter)
        self.dData.textChanged.connect(self.flagUnsavedEdits)
        self.dNumberBox = NumberedLineEdit.LineTextWidget(self.datasets)
        self.dNumberBox.setGeometry(12, 72, 896, 480)
        
        self.filter = focusOutFilter(self.dTitle)
        self.dTitle.installEventFilter(self.filter)
        self.dTitle.textChanged.connect(self.flagUnsavedEdits)
        
        '''metadata tab'''
        self.filter = focusOutFilter(self.oOrder)
        self.oOrder.installEventFilter(self.filter)
        self.oOrder.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.oDiacriticsField)
        self.oDiacriticsField.installEventFilter(self.filter)
        self.oDiacriticsField.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.sOrder)
        self.sOrder.installEventFilter(self.filter)
        self.sOrder.textChanged.connect(self.flagUnsavedEdits)
        
        self.filter = focusOutFilter(self.sExclusions)
        self.sExclusions.installEventFilter(self.filter)
        self.sExclusions.textChanged.connect(self.flagUnsavedEdits)
        
        '''buttons, list widgets and comboboxes'''
        
        '''HOME Tab'''        
        
        def goToLxCard():
            pointer = self.hLexNav.currentIndex()
            data = self.hLexNav.currentIndex().data(32)
            dataIndex.currentCard = data
            targetCard = dataIndex.lexDict[data]
            cardLoader.loadLexCard(self, targetCard)
            self.lLexNav.setCurrentIndex(pointer)
            self.lLexNav.scrollTo(pointer, QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
            dataIndex.unsavedEdit = 0
            dataIndex.currentCard = data
            self.tabWidget.setCurrentIndex(1)
    
        self.hLexNav.clicked.connect(goToLxCard)
        
        def goToTxtCard():
          pointer = self.hTextNav.currentIndex()
          data = self.hTextNav.currentIndex().data(32)
          dataIndex.currentCard = data
          targetCard = dataIndex.textDict[data]
          self.tabWidget.setCurrentIndex(2)
          cardLoader.loadTextCard(self, targetCard)
          self.tTextNav.setCurrentIndex(pointer)
          self.tTextNav.scrollTo(pointer, QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
          dataIndex.unsavedEdit = 0
    
        self.hTextNav.clicked.connect(goToTxtCard)
        
        def goToDataCard():
          data = self.hDataNav.currentIndex().data(32)
          dataIndex.currentCard = data
          targetCard = dataIndex.dataDict[data]
          cardLoader.loadDataCard(self, targetCard)
          i = self.hDataNav.currentIndex()
          self.dDataNav.setCurrentIndex(i)
          self.dDataNav.scrollTo(i, QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
          self.tabWidget.setCurrentIndex(4)
          dataIndex.unsavedEdit = 0
    
        self.hDataNav.clicked.connect(goToDataCard)
 
        '''Lexicon card'''
        
        def goToLxCard2():
          data = self.lLexNav.currentIndex().data(32)
          dataIndex.currentCard = data
          targetCard = dataIndex.lexDict[data]
          cardLoader.loadLexCard(self, targetCard)
          dataIndex.unsavedEdit = 0
    
        self.lLexNav.clicked.connect(goToLxCard2)
    
        def goToDerivation():
            data = self.lDerivatives.currentItem().data(32)
            targetCard = dataIndex.lexDict[data]
            cardLoader.loadLexCard(self, targetCard)
            dataIndex.unsavedEdit = 0
            for i in range(0,self.lLexNav.model().rowCount()):
                if self.lLexNav.model().index(i, 0).data(32) == data:
                    theItem = i
                    break                    
            self.lLexNav.setCurrentIndex(self.lLexNav.model().index(theItem,0))
            self.lLexNav.scrollTo(self.lLexNav.currentIndex(), QtWidgets.QAbstractItemView.ScrollHint.PositionAtCenter)
          
        self.lDerivatives.clicked.connect(goToDerivation)
        
        def goToBase():
            data = self.lBase.currentItem().data(32)
            targetCard = dataIndex.lexDict[data]
            cardLoader.loadLexCard(self, targetCard)
            dataIndex.unsavedEdit = 0
            for i in range(0,self.lLexNav.model().rowCount()):
                if self.lLexNav.model().index(i, 0).data(32) == data:
                    theItem = i
                    break                    
            self.lLexNav.setCurrentIndex(self.lLexNav.model().index(theItem,0))
            self.lLexNav.scrollTo(self.lLexNav.currentIndex(), QtWidgets.QAbstractItemView.ScrollHint.PositionAtCenter)
           
        self.lBase.clicked.connect(goToBase)
        
        try:
            if dataIndex.root.attrib.get('lAuto') == 'on':
                self.lAutoBtn.setChecked(1)
        except AttributeError:
            pass

        '''TextCard'''
        
        self.tText.setVisible(1)
        self.textLayout = QtWidgets.QGridLayout(self.tText)
        
        def goToTxtCard2():
          data = self.tTextNav.currentIndex().data(32)
          dataIndex.currentCard = data
          targetCard = dataIndex.textDict[data]
          cardLoader.loadTextCard(self, targetCard)
          dataIndex.unsavedEdit = 0
    
        self.tTextNav.clicked.connect(goToTxtCard2)
        comboBox = self.tOrthography
        Orthographies.fillOrthPickers(comboBox)  
        
        '''Example card'''
    
        self.eAbbreviations = QtWidgets.QTableWidget(self.eAbbrBox)
        self.eAbbreviations.setGeometry(12,29,234,420)
        self.eAbbreviations.setObjectName('Abbreviations')
        delegate = HTMLDelegate()
        self.eAbbreviations.setItemDelegate(delegate)
        self.eAbbreviations.horizontalHeader().setEnabled(0)
        self.eAbbreviations.verticalHeader().setEnabled(0)
        self.eAbbreviations.verticalHeader().hide()
        self.eAbbreviations.horizontalHeader().hide()
        self.eAbbreviations.setShowGrid(0)
        self.eAbbreviations.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.eAbbreviations.setStyleSheet("selection-background-color: #E6E6E6;")
        self.eAbbreviations.setColumnCount(1)
        self.eAbbreviations.setRowCount(0)
        for child in dataIndex.root.iter('Abbr'):
            abbrev = child.attrib.get('Abv').swapcase()
            itemText = '<small>' + abbrev + '</small>&emsp;‘' + child.attrib.get('Term') + '’'
            try:
                form = child.attrib.get('Form')
                itemText += ' (' + form + ')'
            except AttributeError:
                pass
            except TypeError:
                pass
            newItem = QtWidgets.QTableWidgetItem(1001)
            newItem.setData(35,child.attrib.get('ACode'))
            newItem.setData(36,child)
            newItem.setText(itemText)
            newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
            nextRow = self.eAbbreviations.rowCount()
            self.eAbbreviations.setRowCount(nextRow+1)
            self.eAbbreviations.setItem(nextRow,0,newItem)
            self.eAbbreviations.setRowHeight(nextRow,20)
        self.eAbbreviations.resizeColumnToContents(0)
        self.eAbbreviations.sortItems(0,QtCore.Qt.SortOrder.AscendingOrder)
        
        if dataIndex.root.attrib.get('eParse') == 'on':
            self.eAutoParsingBtn.setChecked(1)
        else:
            self.eAutoParsingBtn.setChecked(0)

        comboBox = self.eOrthography
        Orthographies.fillOrthPickers(comboBox)   
        
        '''Datasets'''

        '''ListWidgets'''
        def goToDataCard2():
            data = self.dDataNav.currentIndex().data(32)
            dataIndex.currentCard = data
            targetCard = dataIndex.dataDict[data]
            cardLoader.loadDataCard(self, targetCard)
            self.tabWidget.setCurrentIndex(4)
            dataIndex.unsavedEdit = 0
    
        self.dDataNav.clicked.connect(goToDataCard2)
        
        '''Searches card'''
        
        def setSignal(targets):
            for checkBox in targets:
                try:
                    checkBox.setChecked(0)
                    checkBox.stateChanged.connect(searchOnlyBtns.checkBoxToggled)
                except AttributeError:
                    pass
        
        def setExSignal(targets):
            for checkBox in targets:
                try:
                    checkBox.setChecked(0)
                    checkBox.stateChanged.connect(searchOnlyBtns.ExCheckBoxToggled)
                except AttributeError:
                    pass  
        
        setSignal(self.cLexiconFocusBox.children())
        setSignal(self.cTextsFocusBox.children())
        setExSignal(self.cExamplesFocusBox.children())
        
        
        '''METADATA Tab'''
    
        '''Consultants sub-tab'''
    
        def fillSpForm():
            self.mSpTable.selectRow(self.mSpTable.currentRow())
            u = self.mSpTable.currentRow()
            self.mSCode.clear()
            self.mSpeaker.clear()
            self.mBirthday.clear()
            self.mBirthplace.clear()
            self.mInfo.clear()
            self.mSCode.setHtml(self.mSpTable.item(u,0).text())
            self.mSpeaker.setHtml(self.mSpTable.item(u,1).text())
            self.mBirthday.setHtml(self.mSpTable.item(u,2).text())
            self.mBirthplace.setHtml(self.mSpTable.item(u,3).text())
            self.mInfo.setHtml(self.mSpTable.item(u,4).text())
            self.mSpAddBtn.setEnabled(0)
            self.mSpDelBtn.setEnabled(1)
            self.mSpUpdateBtn.setEnabled(1)
            self.mSCode.setReadOnly(1)
    
        self.mSpTable = QtWidgets.QTableWidget(self.mConsultantsTab)
        self.mSpTable.setGeometry(15,0,500,272)
        self.mSpTable.setItemDelegate(delegate)
        self.mSpTable.horizontalHeader().setEnabled(0)
        self.mSpTable.verticalHeader().setEnabled(0)
        self.mSpTable.verticalHeader().hide()
        self.mSpTable.horizontalHeader().hide()
        self.mSpTable.setShowGrid(0)
        self.mSpTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.mSpTable.setStyleSheet("selection-background-color: #E6E6E6;")
        self.mSpTable.setColumnCount(5)
        self.mSpTable.itemClicked.connect(fillSpForm)
    
        metaDataTableFillers.fillConsultantTable(self)
        self.mSpTable.sortItems(0,QtCore.Qt.SortOrder.AscendingOrder)
    
        '''researchers sub-tab'''
        
        levelList = ['Admin','Editor','Output','Read only','None']
        self.mPrivilegesBox.insertItems(-1,levelList)
        self.mPrivilegesBox.setCurrentIndex(-1)
        
        def fillRForm():
            self.mRTable.selectRow(self.mRTable.currentRow())
            u = self.mRTable.currentRow()
            self.mRCode.clear()
            self.mResearcher.clear()
            self.mAffiliation.clear()
            self.mRInfo.clear()
            self.mRCode.setHtml(self.mRTable.item(u,0).text())
            self.mResearcher.setHtml(self.mRTable.item(u,1).text())
            self.mAffiliation.setHtml(self.mRTable.item(u,3).text())
            self.mRInfo.setHtml(self.mRTable.item(u,4).text())
            self.mRAddBtn.setEnabled(0)
            self.mRDelBtn.setEnabled(1)
            self.mRCode.setReadOnly(1)
            self.mRUpdateBtn.setEnabled(1)
            y = self.mPrivilegesBox.findText(self.mRTable.item(u,0).data(40))
            if y != -1:
                self.mPrivilegesBox.setCurrentIndex(y)
            elif y == 'None':
                self.mPrivilegesBox.setCurrentIndex(-1)
            else:
                self.mPrivilegesBox.setCurrentIndex(-1)
    
        self.mRTable = QtWidgets.QTableWidget(self.mResearchersTab)
        self.mRTable.setGeometry(15,0,500,272)
        self.mRTable.setItemDelegate(delegate)
        self.mRTable.horizontalHeader().setEnabled(0)
        self.mRTable.verticalHeader().setEnabled(0)
        self.mRTable.verticalHeader().hide()
        self.mRTable.horizontalHeader().hide()
        self.mRTable.setShowGrid(0)
        self.mRTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.mRTable.setStyleSheet("selection-background-color: #E6E6E6;")
        self.mRTable.setColumnCount(5)
        self.mRTable.itemClicked.connect(fillRForm)
    
        metaDataTableFillers.fillRTable(self)
        self.mRTable.sortItems(0,QtCore.Qt.SortOrder.AscendingOrder)
    
        '''media sub-tab'''
        
        self.mSpDelBtn.setEnabled(0)
        self.mSpUpdateBtn.setEnabled(0)
        self.mRDelBtn.setEnabled(0)
        self.mRUpdateBtn.setEnabled(0)
    
        def selectMRow():
            if self.mMediaTable.currentColumn() == 3:
                caller = self.mMediaTable
                soundBtns.mediaInfo(caller)
            self.mMediaTable.selectRow(self.mMediaTable.currentRow())
        
        self.mMediaTable = QtWidgets.QTableWidget(self.mMediaBox)
        self.mMediaTable.setGeometry(15,33,328,576)
        self.mMediaTable.horizontalHeader().setEnabled(0)
        self.mMediaTable.verticalHeader().setEnabled(0)
        self.mMediaTable.verticalHeader().hide()
        self.mMediaTable.horizontalHeader().hide()
        self.mMediaTable.setShowGrid(0)
        self.mMediaTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.mMediaTable.setStyleSheet("selection-background-color: #E6E6E6;")
        self.mMediaTable.setColumnCount(4)
        self.mMediaTable.setAlternatingRowColors(1)
        self.mMediaTable.itemClicked.connect(selectMRow)
        metaDataTableFillers.fillMediaTable(self, infoIcon)
        if dataIndex.root.get("MediaFolder"):
            prefix = dataIndex.root.get("MediaFolder")
            self.mMediaPath.setText(prefix)
        self.mMediaTable.sortItems(0,QtCore.Qt.SortOrder.AscendingOrder)
        
        '''orthographies sub-tab'''
        
        self.oList.setColumnWidth(0,80)    
        self.oList.setColumnWidth(1,58)    
        self.oList.verticalHeader().hide()
        self.oList.setAlternatingRowColors(1)
        self.oList.setStyleSheet("selection-background-color: #E6E6E6;")
        metaDataTableFillers.fillOrth(self)
        self.oList.itemClicked.connect(metaDataBtns.selectORow)
        self.oTransformBox.insertItem(0, 'Orth ⇨ Phon')
        self.oTransformBox.insertItem(1, 'Phon ⇨ Orth')
        self.oTransformBox.setStyleSheet('selection-color: blue;')
        
        '''alphabetization sub-tab'''
        
        metaDataTableFillers.fillSort(self)
        self.sList.itemClicked.connect(metaDataBtns.selectSRow)

        '''index card'''
        
        self.iAbbreviations = QtWidgets.QTableWidget(self.iAbbrBox)
        self.iAbbreviations.setGeometry(15,30,230,454)
        self.iAbbreviations.setObjectName('Abbreviations')
        delegate = HTMLDelegate()
        self.iAbbreviations.setItemDelegate(delegate)
        self.iAbbreviations.horizontalHeader().setEnabled(0)
        self.iAbbreviations.verticalHeader().setEnabled(0)
        self.iAbbreviations.verticalHeader().hide()
        self.iAbbreviations.horizontalHeader().hide()
        self.iAbbreviations.setShowGrid(0)
        self.iAbbreviations.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.iAbbreviations.setStyleSheet("selection-background-color: #E6E6E6;")
        self.iAbbreviations.setColumnCount(1)
        self.iAbbreviations.setRowCount(0)        
        for child in dataIndex.root.iter('Abbr'):
            abbrev = child.attrib.get('Abv').swapcase()
            itemText = '<small>' + abbrev + '</small>&emsp;‘' + child.attrib.get('Term') + '’'
            try:
                form = child.attrib.get('Form')
                itemText += ' (' + form + ')'
            except AttributeError:
                pass
            except TypeError:
                pass
            newItem = QtWidgets.QTableWidgetItem(1001)
            newItem.setData(35,child.attrib.get('ACode'))
            newItem.setData(36,child)
            newItem.setText(itemText)
            newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)
            nextRow = self.iAbbreviations.rowCount()
            self.iAbbreviations.setRowCount(nextRow+1)
            self.iAbbreviations.setItem(nextRow,0,newItem)
            self.iAbbreviations.setRowHeight(nextRow,20)
        self.iAbbreviations.resizeColumnToContents(0)
        self.iAbbreviations.sortItems(0,QtCore.Qt.SortOrder.AscendingOrder)
        
        self.recoverRecentFiles()
        dataIndex.unsavedEdit = 0
        
    def flagUnsavedEdits(self):
        '''set flag when fields are edited'''
        dataIndex.unsavedEdit = 1
        return dataIndex.unsavedEdit
        
    @QtCore.pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        """
        Actions performed when tabWidget is clicked.
        """
        if dataIndex.sourceFile is None:
            return
        if self.tabWidget.currentIndex() == 0: #Home tab
            self.actionNewCard.setEnabled(False)
            self.actionDelCard.setEnabled(False)
            self.actionIPA.setEnabled(False)
            self.actionOrthographic.setEnabled(False) 
            self.actionCustom.setEnabled(False) 
            self.actionLoad_Schema.setEnabled(False)
            self.actionAssistant.setEnabled(False)
            self.menuOpen_Recent.setEnabled(True)
            self.actionClose.setEnabled(True)
            self.actionNew.setEnabled(True)
            self.actionOpen.setEnabled(True)
            self.actionFind.setEnabled(0)
            self.actionFind_Again.setEnabled(0)
            self.actionFuzzy_Find.setEnabled(0)
            self.actionFuzzy_Find_Again.setEnabled(0)
            cardStack.addToQueue(self,'Home')
            dataIndex.currentCard = 'Home'
            
        if self.tabWidget.currentIndex() == 1: #Lexicon tab
            if dataIndex.unsavedEdit == 1:
                pendingChange = 1
            else:
                pendingChange = 0
            if dataIndex.activeSearch:
                lastLex = dataIndex.lastLex
                if dataIndex.activeSearch != 'return':
                    lexSearchBtns.restoreLexCard(dataIndex.lexDict[lastLex])
                else:
                    dataIndex.activeSearch = 1
            else:
                lastLex = dataIndex.root.attrib.get('LastLex')
                if lastLex:
                    entry = dataIndex.lexDict[lastLex]
                else:
                    lastLex = self.lLexNav.model().index(0,0).data(32)     
                    entry = dataIndex.lexDict[lastLex]
                    dataIndex.lastLex = lastLex
                cardLoader.loadLexCard(self, entry)
            dataIndex.currentCard = lastLex
           ##this sets up the menus, etc
            self.actionNewCard.setEnabled(True)
            self.actionDelCard.setEnabled(True)
            self.actionIPA.setEnabled(True)
            self.actionOrthographic.setEnabled(True)
            self.actionCustom.setEnabled(True) 
            self.actionLoad_Schema.setEnabled(True)
            self.actionAssistant.setEnabled(True)
            self.actionFind.setEnabled(1)
            self.actionFind_Again.setEnabled(1)
            self.actionFuzzy_Find.setEnabled(1)
            self.actionFuzzy_Find_Again.setEnabled(1)
            for i in range(0,self.lLexNav.model().rowCount()):
                if self.lLexNav.model().index(i,0).data(32) == lastLex:
                    theItem = i
                    break                    
            self.lLexNav.setCurrentIndex(self.lLexNav.model().index(theItem,0))
            self.lLexNav.scrollTo(self.lLexNav.currentIndex(), QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
            if pendingChange:
                dataIndex.unsavedEdit = 1
            else:
                dataIndex.unsavedEdit = 0
            return theItem
        
        if self.tabWidget.currentIndex() == 2: #Texts tab
            if dataIndex.unsavedEdit == 1:
                pendingChange = 1
            else:
                pendingChange = 0
            lastText = dataIndex.root.attrib.get('LastText')
            if lastText:
                entry = dataIndex.textDict[lastText]
                for i in range(0,self.tTextNav.model().rowCount()):
                    if self.tTextNav.model().index(i,0).data(32) == lastText:
                        theItem = i
                        break                    
                self.tTextNav.setCurrentIndex(self.tTextNav.model().index(theItem,0))
                self.tTextNav.scrollTo(self.tTextNav.currentIndex(), QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
                dataIndex.currentCard = lastText
            entry = dataIndex.textDict[lastText]
            cardLoader.loadTextCard(self, entry)
            dataIndex.currentCard = lastText
            self.actionNewCard.setEnabled(True)
            self.actionDelCard.setEnabled(True)
            self.actionIPA.setEnabled(True)
            self.actionOrthographic.setEnabled(True)
            self.actionCustom.setEnabled(True) 
            self.actionLoad_Schema.setEnabled(True)
            self.actionAssistant.setEnabled(True)
            self.actionFind.setEnabled(0)
            self.actionFind_Again.setEnabled(0)
            self.actionFuzzy_Find.setEnabled(0)
            self.actionFuzzy_Find_Again.setEnabled(0)
            if pendingChange:
                dataIndex.unsavedEdit = 1
            else:
                dataIndex.unsavedEdit = 0
            try:
                noText = dataIndex.root.get("noText")
            except AttributeError:
                noText = None    
            if noText:
                newTextBtns.enterNewText(self)

        if self.tabWidget.currentIndex() == 3: #Examples tab
            if dataIndex.unsavedEdit == 1:
                pendingChange = 1
            else:
                pendingChange = 0

            lastEG = dataIndex.root.attrib.get('LastEG')
            if lastEG:
              entry = dataIndex.exDict[lastEG]
            else:
              entry = dataIndex.root.find('Ex')
            cardLoader.loadEgCard(self, entry)
            self.actionNewCard.setEnabled(True)
            self.actionDelCard.setEnabled(True)
            self.actionIPA.setEnabled(True)
            self.actionOrthographic.setEnabled(True)
            self.actionCustom.setEnabled(True) 
            self.actionLoad_Schema.setEnabled(True)
            self.actionAssistant.setEnabled(True)
            self.actionFind.setEnabled(1)
            self.actionFind_Again.setEnabled(1)
            self.actionFuzzy_Find.setEnabled(1)
            self.actionFuzzy_Find_Again.setEnabled(1)
            if pendingChange:
                dataIndex.unsavedEdit = 1
            else:
                dataIndex.unsavedEdit = 0
        if self.tabWidget.currentIndex() == 4: #Datasets tab
            if dataIndex.unsavedEdit == 1:
                pendingChange = 1
            else:
                pendingChange = 0
            lastDset = dataIndex.root.attrib.get('LastDset')
            if lastDset:
                entry = dataIndex.dataDict[lastDset]
                for i in range(0,self.dDataNav.model().rowCount()):
                    if self.dDataNav.model().index(i,0).data(32) == lastDset:
                        theItem = i
                        break                    
                self.dDataNav.setCurrentIndex(self.dDataNav.model().index(theItem,0))
                self.dDataNav.scrollTo(self.dDataNav.currentIndex(), QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
                dataIndex.currentCard = lastDset
            else:
                lastDset = dataIndex.root.find('Dset')         
            entry = dataIndex.dataDict[lastDset]
            cardLoader.loadDataCard(self, entry)
            dataIndex.currentCard = lastDset
            self.actionNewCard.setEnabled(True)
            self.actionDelCard.setEnabled(True)
            self.actionIPA.setEnabled(True)
            self.actionOrthographic.setEnabled(True)
            self.actionCustom.setEnabled(True) 
            self.actionLoad_Schema.setEnabled(True)
            self.actionAssistant.setEnabled(True)
            if pendingChange:
                dataIndex.unsavedEdit = 1
            else:
                dataIndex.unsavedEdit = 0
        if self.tabWidget.currentIndex() == 5: #Search tab
            self.actionNewCard.setEnabled(False)
            self.actionDelCard.setEnabled(False)
            self.actionIPA.setEnabled(False)
            self.actionOrthographic.setEnabled(False) 
            self.actionCustom.setEnabled(False) 
            self.actionLoad_Schema.setEnabled(False)
            self.actionAssistant.setEnabled(False)
            self.actionFind.setEnabled(0)
            self.actionFind_Again.setEnabled(0)
            self.actionFuzzy_Find.setEnabled(0)
            self.actionFuzzy_Find_Again.setEnabled(0)
            if self.cSearchResults.model():
                self.cNarrowBtn.setEnabled(1)
            else:
                self.cNarrowBtn.setDisabled(1)
            dataIndex.currentCard = 'concordances'
        if self.tabWidget.currentIndex() == 6: #Meta tab
            self.actionNewCard.setEnabled(False)
            self.actionDelCard.setEnabled(False)
            self.actionIPA.setEnabled(False)
            self.actionOrthographic.setEnabled(False) 
            self.actionCustom.setEnabled(False) 
            self.actionLoad_Schema.setEnabled(False)
            self.actionAssistant.setEnabled(False)
            self.actionFind.setEnabled(0)
            self.actionFind_Again.setEnabled(0)
            self.actionFuzzy_Find.setEnabled(0)
            self.actionFuzzy_Find_Again.setEnabled(0)
            dataIndex.currentCard = 'Meta'
        if self.tabWidget.currentIndex() == 7: #Index tab
            self.actionNewCard.setEnabled(False)
            self.actionDelCard.setEnabled(False)
            self.actionIPA.setEnabled(False)
            self.actionOrthographic.setEnabled(False) 
            self.actionCustom.setEnabled(False) 
            self.actionLoad_Schema.setEnabled(False)
            self.actionAssistant.setEnabled(False)
            self.actionFind.setEnabled(0)
            self.actionFind_Again.setEnabled(0)
            self.actionFuzzy_Find.setEnabled(0)
            self.actionFuzzy_Find_Again.setEnabled(0)
            dataIndex.currentCard = 'index'

    def recoverRecentFiles(self):
        '''get list of recently opened files from QSettings and store it in dataIndex'''
        if self.settings.value('RecentFile'):
            fname = self.settings.value('RecentFile')
            dataIndex.recentFile = []
            for i in range(0, len(fname)):
                try:
                    if QtCore.QFile.exists(fname[i]):
                        dataIndex.recentFile.append(fname[i])
                except TypeError:
                    pass

    def giveWindowTitle(self):
        if dataIndex.sourceFile != None:
            self.setWindowTitle("{0}[*]".format(os.path.basename(dataIndex.sourceFile)))
        else:
            self.setWindowTitle("Electronic Fieldbook")

    def closeEvent(self, event):
        if dataIndex.sourceFile != None and dataIndex.unsavedEdit == 1:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setText("Any unsaved changes will be lost.")
            msgbox.setInformativeText("Do you want to save changes?")
            msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Save | QtWidgets.QMessageBox.StandardButton.Discard | QtWidgets.QMessageBox.StandardButton.Cancel)
            msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Save)
            reply = msgbox.exec()
            if reply == QtWidgets.QMessageBox.StandardButton.Cancel:
              event.ignore()
              return
            elif reply == QtWidgets.QMessageBox.StandardButton.Save:
              QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.WaitCursor))
              dataIndex.xmltree.write(dataIndex.sourceFile, encoding="UTF-8")
              QtWidgets.QApplication.restoreOverrideCursor()
        self.settings.setValue('LastFile',dataIndex.sourceFile)
        self.settings.setValue('RecentFile',dataIndex.recentFile)

    @QtCore.pyqtSlot()
    def on_actionAbout_triggered(self):
        """
        triggers "about menu"
        """
        menus.showAbout(self)
    
    @QtCore.pyqtSlot()
    def on_actionNew_triggered(self):
        """
        start a clean database
        """
        menus.newDb(self)
    
    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        """
        open an existing database
        """
        menus.openDb(self)
    
    @QtCore.pyqtSlot()
    def on_menuFile_aboutToShow(self):
        """
        this will update the open recent file list whenever the File menu in the menu bar is selected
        """
        menus.updateRecentFile(self)
    
    @QtCore.pyqtSlot()
    def on_actionClose_triggered(self):
        """
        call close file menu
        """
        menus.closeDb(self)
     
    @QtCore.pyqtSlot()
    def on_actionQuit_triggered(self):
        """
        quit application.
        """
        menus.quitApplication(self)
        
    @QtCore.pyqtSlot()
    def on_actionSave_triggered(self):
        """
        save changes to database (calls "Save As" if database has no name yet)
        """
        menus.saveDb(self)
    
    @QtCore.pyqtSlot()
    def on_actionSaveAs_triggered(self):
        """
        save changes to unnamed database or rename database
        """
        menus.saveAsDb(self)
    
    @QtCore.pyqtSlot()
    def on_actionNewCard_triggered(self):
        """
        add new records to the database
        """
        menus.newCard(self)
    
    @QtCore.pyqtSlot()
    def on_actionDelCard_triggered(self):
        """
        delete records from database
        """
        menus.delCard(self)

    '''navigation buttons'''
    
    @QtCore.pyqtSlot()
    def on_lBeginBtn_released(self):
        """
        go to first Lexicon card
        """
        navBtns.firstLxCard(self)
    
    @QtCore.pyqtSlot()
    def on_lPrevBtn_released(self):
        """
        go to the previous Lexicon card in the list
        (as sorted in the nav bar)
        """
        navBtns.goPrevLx(self)
    
    @QtCore.pyqtSlot()
    def on_lRtnBtn_released(self):
        """
        goes back through the list of previous cards visited
        (iterable through sequence of previously visited cards)
        """
        navBtns.btnBack(self)
    
    @QtCore.pyqtSlot()
    def on_lFwdBtn_released(self):
        """
        goes forward through the list of cards visited
        (iterable through sequence of visited cards)
        """
        navBtns.btnForward(self)
        
    @QtCore.pyqtSlot()
    def on_lNextBtn_released(self):
        """
        go to the next Lexicon card in the list
        (as sorted in the nav bar)        
        """
        navBtns.goNextLx(self)
    
    @QtCore.pyqtSlot()
    def on_lEndBtn_released(self):
        """
        go to last Lexicon card.
        """
        navBtns.lastLxCard(self)
    
    @QtCore.pyqtSlot()
    def on_tBeginBtn_released(self):
        """
        go to first Text card
        """
        navBtns.firstTxtCard(self)
    
    @QtCore.pyqtSlot()
    def on_tPrevBtn_released(self):
        """
        go to the previous Text card in the list
        (as sorted in the nav bar)
        """
        navBtns.goPrevTxt(self)
    
    @QtCore.pyqtSlot()
    def on_tRtnBtn_released(self):
        """
        goes back through the list of previous cards visited
        (iterable through sequence of previously visited cards)
        """
        navBtns.btnBack(self)
    
    @QtCore.pyqtSlot()
    def on_tFwdBtn_released(self):
        """
        goes forward through the list of cards visited
        (iterable through sequence of visited cards)
        """
        navBtns.btnForward(self)
        
    @QtCore.pyqtSlot()
    def on_tNextBtn_released(self):
        """
        go to the next Text card in the list
        (as sorted in the nav bar)        
        """
        navBtns.goNextTxt(self)
    
    @QtCore.pyqtSlot()
    def on_tEndBtn_released(self):
        """
        go to last Text card.
        """
        navBtns.lastTxtCard(self)
        
    @QtCore.pyqtSlot()
    def on_eBeginBtn_released(self):
        """
        go to first Example card
        """
        navBtns.firstEgCard(self)
    
    @QtCore.pyqtSlot()
    def on_ePrevBtn_released(self):
        """
        go to the previous Example card in the list
        (as sorted in the nav bar)
        """
        navBtns.goPrevEg(self)
    
    @QtCore.pyqtSlot()
    def on_eRtnBtn_released(self):
        """
        goes back through the list of previous cards visited
        (iterable through sequence of previously visited cards)
        """
        navBtns.btnBack(self)
    
    @QtCore.pyqtSlot()
    def on_eFwdBtn_released(self):
        """
        goes forward through the list of cards visited
        (iterable through sequence of visited cards)
        """
        navBtns.btnForward(self)
        
    @QtCore.pyqtSlot()
    def on_eNextBtn_released(self):
        """
        go to the next Example card in the list
        """
        navBtns.goNextEg(self)
    
    @QtCore.pyqtSlot()
    def on_eEndBtn_released(self):
        """
        go to last Example card.
        """
        navBtns.lastEgCard(self)
        
    @QtCore.pyqtSlot()
    def on_dBeginBtn_released(self):
        """
        go to first Dataset card
        """
        navBtns.firstDsetCard(self)
    
    @QtCore.pyqtSlot()
    def on_dPrevBtn_released(self):
        """
        go to the previous Dataset card in the list
        (as sorted in the nav bar)
        """
        navBtns.goPrevDset(self)
    
    @QtCore.pyqtSlot()
    def on_dRtnBtn_released(self):
        """
        goes back through the list of previous cards visited
        (iterable through sequence of previously visited cards)
        """
        navBtns.btnBack(self)
    
    @QtCore.pyqtSlot()
    def on_dFwdBtn_released(self):
        """
        goes forward through the list of cards visited
        (iterable through sequence of visited cards)
        """
        navBtns.btnForward(self)
        
    @QtCore.pyqtSlot()
    def on_dNextBtn_released(self):
        """
        go to the next Dataset card in the list
        (as sorted in the nav bar)        
        """
        navBtns.goNextDset(self)
    
    @QtCore.pyqtSlot()
    def on_dEndBtn_released(self):
        """
        go to last Dataset card.
        """
        navBtns.lastDsetCard(self)
    
    @QtCore.pyqtSlot()
    def on_dNewDsetBtn_released(self):
        """
        create new dataset.
        """
        menus.newCard(self)
        
    @QtCore.pyqtSlot()
    def on_dAdvancedSearch_released(self):
        """
        Search examples.
        """
        dsetOnlyBtns.dAdvancedSearch(self)
        
    '''sound buttons (all cards)'''
    
    @QtCore.pyqtSlot()
    def on_dResetBtn_released(self):
        """
        Remove highlighting from search results.
        """
        dsetOnlyBtns.removeHiliting(self)
        
    @QtCore.pyqtSlot()
    def on_lPlaySoundBtn_released(self):
        """
        plays sound when speaker button is pressed
        """
        caller = self.lRecordings
        soundBtns.playSound(self, caller)
    
    @QtCore.pyqtSlot()
    def on_lSoundMetaBtn_released(self):
        """
        updates label with recording info
        """
        if self.lRecordings.count() != 0:
            caller = self.lRecordings
            metadataLabel = self.lSoundFileMeta
            soundBtns.mediaInfo(caller,metadataLabel)
        
    @QtCore.pyqtSlot()
    def on_lAddEgBtn_released(self):
        """
        adds media to card.
        """
        caller = self.lRecordings
        metadataLabel = self.lSoundFileMeta
        soundBtns.newMedia(self, caller,metadataLabel)
    
    @QtCore.pyqtSlot()
    def on_lDelEgBtn_released(self):
        """
        unlinks recording from card
        """
        if self.lRecordings.count() != 0:
            caller = self.lRecordings
            metadataLabel = self.lSoundFileMeta
            soundBtns.delMedia(self, caller,metadataLabel)
    
    @QtCore.pyqtSlot(str)
    def on_lRecordings_activated(self, p0):
        """
        plays the sound shown in the combobox list if selection is changed,
        and updates the metadata synopsis on the card
        calls the play sound button command
        """
        caller = self.lRecordings
        metadataLabel = self.lSoundFileMeta
        soundBtns.playSound(self, caller)
        for child in dataIndex.root.iter('Media'):
            if child.attrib.get('MedID') == caller.itemData(caller.currentIndex(),35):
                speaker = child.attrib.get('Spkr')
                date = child.attrib.get('Date')
                metadataLabel.setText(speaker + ' ' + date)
                break

    @QtCore.pyqtSlot()
    def on_tPlaySoundBtn_released(self):
        """
        plays recording when speaker button pressed.
        """
        caller = self.tRecordings
        soundBtns.playSound(self, caller)
    
    @QtCore.pyqtSlot()
    def on_tSoundMetaBtn_released(self):
        """
        updates label with recording info
        """
        if self.tRecordings.count() != 0:
            caller = self.tRecordings
            metadataLabel = self.tSoundFileMeta
            soundBtns.mediaInfo(caller,metadataLabel)
        
    @QtCore.pyqtSlot()
    def on_tAddEgBtn_released(self):
        """
        adds media to card.
        """
        caller = self.tRecordings
        metadataLabel = self.tSoundFileMeta
        soundBtns.newMedia(self, caller,metadataLabel)
    
    @QtCore.pyqtSlot()
    def on_tDelEgBtn_released(self):
        """
        unlinks recording from card
        """
        if self.tRecordings.count() != 0:
            caller = self.tRecordings
            metadataLabel = self.tSoundFileMeta
            soundBtns.delMedia(self, caller,metadataLabel)
    
    @QtCore.pyqtSlot(str)
    def on_tRecordings_activated(self, p0):
        """
        plays the sound shown in the combobox list if selection is changed,
        and updates the metadata synopsis on the card
        calls the play sound button command
        """
        caller = self.tRecordings
        metadataLabel = self.tSoundFileMeta
        soundBtns.playSound(self, caller)
        for child in dataIndex.root.iter('Media'):
            if child.attrib.get('MedID') == caller.itemData(caller.currentIndex(),35):
                speaker = child.attrib.get('Spkr')
                date = child.attrib.get('Date')
                metadataLabel.setText(speaker + ' ' + date)
                break

    @QtCore.pyqtSlot()
    def on_ePlaySoundBtn_released(self):
        """
        plays recording when speaker button pressed.
        """
        caller = self.eRecordings
        soundBtns.playSound(self, caller)
    
    @QtCore.pyqtSlot()
    def on_eSoundMetaBtn_released(self):
        """
        updates label with recording info
        """
        if self.eRecordings.count() != 0:
            caller = self.eRecordings
            metadataLabel = self.eSoundFileMeta
            soundBtns.mediaInfo(caller,metadataLabel)
        
    @QtCore.pyqtSlot()
    def on_eAddEgBtn_released(self):
        """
        adds media to card.
        """
        caller = self.eRecordings
        metadataLabel = self.eSoundFileMeta
        soundBtns.newMedia(self, caller,metadataLabel)
     
    @QtCore.pyqtSlot()
    def on_eDuplicateBtn_released(self):
        """
        Slot documentation goes here.
        """
        egOnlyBtns.eDuplicate(self)
        
    @QtCore.pyqtSlot()
    def on_eDelEgBtn_released(self):
        """
        unlinks recording from card
        """
        if self.eRecordings.count() != 0:
            caller = self.eRecordings
            metadataLabel = self.eSoundFileMeta
            soundBtns.delMedia(self, caller,metadataLabel)
    
    @QtCore.pyqtSlot(str)
    def on_eRecordings_activated(self, p0):
        """
        plays the sound shown in the combobox list if selection is changed,
        and updates the metadata synopsis on the card
        calls the play sound button command
        """
        caller = self.eRecordings
        metadataLabel = self.eSoundFileMeta
        soundBtns.playSound(self, caller)
        for child in dataIndex.root.iter('Media'):
            if child.attrib.get('MedID') == caller.itemData(caller.currentIndex(),35):
                speaker = child.attrib.get('Spkr')
                date = child.attrib.get('Date')
                metadataLabel.setText(speaker + ' ' + date)
                break
    
    @QtCore.pyqtSlot()
    def on_eAdvancedSearch_released(self):
        """
        Search examples.
        """
        egOnlyBtns.eAdvancedSearch(self)

    @QtCore.pyqtSlot()
    def on_dPlaySoundBtn_released(self):
        """
        plays sound when speaker button is pressed
        """
        caller = self.dRecordings
        soundBtns.playSound(self, caller)
    
    @QtCore.pyqtSlot()
    def on_dSoundMetaBtn_released(self):
        """
        updates label with recording info
        """
        if self.dRecordings.count() != 0:
            caller = self.dRecordings
            metadataLabel = self.dSoundFileMeta
            soundBtns.mediaInfo(caller,metadataLabel)
        
    @QtCore.pyqtSlot()
    def on_dAddEgBtn_released(self):
        """
        adds media to card.
        """
        caller = self.dRecordings
        metadataLabel = self.dSoundFileMeta
        soundBtns.newMedia(self, caller,metadataLabel)
    
    @QtCore.pyqtSlot()
    def on_dDelEgBtn_released(self):
        """
        unlinks recording from card
        """
        if self.dRecordings.count() != 0:
            caller = self.dRecordings
            metadataLabel = self.dSoundFileMeta
            soundBtns.delMedia(self, caller,metadataLabel)
    
    @QtCore.pyqtSlot(str)
    def on_dRecordings_activated(self, p0):
        """
        plays the sound shown in the combobox list if selection is changed,
        and updates the metadata synopsis on the card
        calls the play sound button command
        """
        caller = self.dRecordings
        metadataLabel = self.dSoundFileMeta
        soundBtns.playSound(self, caller)
        for child in dataIndex.root.iter('Media'):
            if child.attrib.get('MedID') == caller.itemData(caller.currentIndex(),35):
                speaker = child.attrib.get('Spkr')
                date = child.attrib.get('Date')
                metadataLabel.setText(speaker + ' ' + date)
                break

    @QtCore.pyqtSlot()
    def on_mPlaySoundBtn_released(self):
        """
        plays selected sound when speaker button is pressed.
        """
        caller = self.mMediaTable
        row = caller.currentRow()
        if row == -1:
            return
        node = caller.item(row,0).data(36)
        IDREF = node.attrib.get('MedID')       
        soundBtns.playSound(self, caller, IDREF)

    @QtCore.pyqtSlot()
    def on_mAddEgBtn_released(self):
        """
        adds media to database.
        """
        caller = self.mMediaTable
        soundBtns.newMedia(self, caller)

    @QtCore.pyqtSlot()
    def on_mDelEgBtn_released(self):
        """
        removes recording from database
        """
        if self.mMediaTable.currentRow() == -1:
            return
        msgbox = QtWidgets.QMessageBox()
        msgbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msgbox.setText("Remove recording.")
        msgbox.setInformativeText('This will remove all links to \n'
                                  'and information about this \n'
                                  'recording from the database. Proceed?')
        msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
        msgbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        msgbox.exec()
        if msgbox.result() == QtWidgets.QMessageBox.StandardButton.Ok:
            self.mMediaTable.removeRow(self.mMediaTable.currentRow())
            self.mMediaTable.setCurrentCell(-1,-1)
            print('purge')
            dataIndex.unsavedEdit = 1    
    
    @QtCore.pyqtSlot()
    def on_mMediaPath_editingFinished(self):
        """
        updates the MediaFolder attribute in the XML database, which sets
        the default directory for media files
        """
        newPath=self.mMediaPath.text()
        dataIndex.root.set("MediaFolder",newPath)
        dataIndex.unsavedEdit = 1

    '''lexicon card buttons'''
    
    @QtCore.pyqtSlot()
    def on_lAddDerBtn_released(self):
        """
        add link to derivatives to a lexicon card.
        """
        lexOnlyBtns.addDrvn(self)
    
    @QtCore.pyqtSlot()
    def on_lRemoveDerBtn_released(self):
        """
        break link to derivative on a lexicon card
        """
        lexOnlyBtns.delDrvn(self)
    
    @QtCore.pyqtSlot()
    def on_lRadicalBtn_released(self):
        """
        link card to morphological base.
        """
        lexOnlyBtns.addRoot(self)
    
    @QtCore.pyqtSlot()
    def on_lBreakLnkBtn_released(self):
        """
        Slot documentation goes here.
        """
        lexOnlyBtns.removeRoot(self)
    
    @QtCore.pyqtSlot(bool)
    def on_lAutoBtn_toggled(self, checked):
        """
        turns on autoparsing of Orthography to IPA
        """
        lexOnlyBtns.toggleAuto(self)
    
    @QtCore.pyqtSlot()
    def on_lOrthography_editingFinished(self):
        """
        Triggers autoconversion of text in Orthography fld.
        """
        if self.lAutoBtn.isChecked():
            string = self.lOrthography.text()
            IPA = Orthographies.toIPA(string)
            lexNode = dataIndex.lexDict[dataIndex.currentCard]
            try:
                lexNode.find('IPA').text = IPA
            except AttributeError:
                elemList = list(lexNode)
                elemList.reverse()
                for i,item in enumerate(elemList):
                    if item.tag == 'POS': 
                        break
                    elif item.tag == 'Orth': 
                        break
                i = len(elemList) - i
                lexNode.insert(i,MyElementTree.Element('IPA'))
                lexNode.find('IPA').text = IPA
            self.lIPA.setText(IPA)
        
    @QtCore.pyqtSlot(int)
    def on_lDoneBtn_stateChanged(self, p0):
        """
        check box for lexical entries considered more or less complete.
        """
        lexOnlyBtns.doneBtn(p0)
        
    @QtCore.pyqtSlot()
    def on_lClipBtn_released(self):
        """
        copies a digest of the lexical entry to the clipboard.
        """
        lexOnlyBtns.clipEG()
    
    @QtCore.pyqtSlot()
    def on_lAdvancedSearch_released(self):
        """
        Slot documentation goes here.
        """
        lexSearchBtns.lAdvancedSearch(self)

    '''text card only buttons'''
    
    @QtCore.pyqtSlot()
    def on_tAnalyzeBtn_released(self):
        """
        selects line of text for (re)analysis
        """
        textOnlyBtns.tAnalyzeLine(self)
    
    @QtCore.pyqtSlot()
    def on_tNewLineBtn_released(self):
        """
        inserts a new line into a text.
        """
        textOnlyBtns.tNewLine(self)
    
    @QtCore.pyqtSlot()
    def on_tRemoveLineBtn_released(self):
        """
        removes a line from a text.
        """
        textOnlyBtns.tRemoveLine(self)
    
    @QtCore.pyqtSlot()
    def on_lNewBtn_released(self):
        """
        add new lexical entry.
        """
        menus.newCard(self)
    
    @QtCore.pyqtSlot()
    def on_tLanguageBtn_released(self):
        """
        switches between languages for the full glosses of texts.
        """
        textOnlyBtns.switchLanguage(self)
    
    @QtCore.pyqtSlot()
    def on_tSplitLineBtn_released(self):
        """
        splits a line of text in two.
        """
        textOnlyBtns.tSplitLine(self)
    
    @QtCore.pyqtSlot()
    def on_tCopyLineBtn_released(self):
        """
        copies example to clipboard.
        """
        textOnlyBtns.tCopyLine()
    
    @QtCore.pyqtSlot()
    def on_tClipBtn_released(self):
        """
        Place text on clipboard.
        """
        textOnlyBtns.clipText()
        
    @QtCore.pyqtSlot()
    def on_tLoadNewTextBtn_released(self):
        """
        Slot documentation goes here.
        """
        newTextBtns.loadNewText(self)
    
    @QtCore.pyqtSlot()
    def on_tNewTextBtn_released(self):
        """
        button to add a new text.
        """
        newTextBtns.enterNewText(self)

    @QtCore.pyqtSlot()
    def on_tFormatNewTextBtn_released(self):
        """
        Formats new text to ensure clean XML.
        """
        newTextBtns.validateNewText(self)

    @QtCore.pyqtSlot()
    def on_tClearNewTextBtn_released(self):
        """
        Slot documentation goes here.
        """
        newTextBtns.clearNewText(self)
    
    @QtCore.pyqtSlot()
    def on_tCancelNewTextBtn_released(self):
        """
        Slot documentation goes here.
        """
        newTextBtns.restoreTextCard(self)
    
    @QtCore.pyqtSlot()
    def on_tOkayNewTextBtn_released(self):
        """
        Slot documentation goes here.
        """
        newTextBtns.okayNewText(self)
        
    @QtCore.pyqtSlot()
    def on_tAdvancedSearch_released(self):
        """
        Search examples.
        """
        textOnlyBtns.tAdvancedSearch(self)
    
    '''example card only buttons'''
    
    @QtCore.pyqtSlot()
    def on_eAddAbbrBtn_released(self):
        """
        adds new abbreviation to abbreviations list.
        """
        egOnlyBtns.addAbbr(self)
    
    @QtCore.pyqtSlot()
    def on_eDelAbbrBtn_released(self):
        """
        removes abbreviation from abbreviations list.
        """
        egOnlyBtns.delAbbr(self)

    @QtCore.pyqtSlot()
    def on_eEditAbbrBtn_released(self):
        """
        edits abbreviations list.
        """
        egOnlyBtns.editAbbr(self)
    
    @QtCore.pyqtSlot()
    def on_eLocateBtn_released(self):
        """
        take uses to context where example was found (if any).
        """
        egOnlyBtns.eLocateEg(self)
    
    @QtCore.pyqtSlot()
    def on_eUpdateBtn_released(self):
        """
        updates view of text or dataset after example is edited.
        """
        egOnlyBtns.eUpdateText(self)
        
    @QtCore.pyqtSlot()
    def on_eDeleteBtn_released(self):
        """
        Slot documentation goes here.
        """
        egOnlyBtns.eRemoveColumn(self)
        
    @QtCore.pyqtSlot()
    def on_eAddAnnotationBtn_released(self):
        """
        add column to analysis table
        """
        egOnlyBtns.eAddTier(self)    

    @QtCore.pyqtSlot()
    def on_eRemoveTier_released(self):
        """
        used to split one example into two parts.
        """
        egOnlyBtns.eDelTier(self)     
        
    @QtCore.pyqtSlot()
    def on_eAddMorphBtn_released(self):
        """
        add column to analysis table
        """
        egOnlyBtns.eAddColumn(self)    

    @QtCore.pyqtSlot()
    def on_eSplitBtn_released(self):
        """
        used to split one example into two parts.
        """
        egOnlyBtns.eSplitEg(self)
    
    @QtCore.pyqtSlot()
    def on_eAddExampleBtn_released(self):
        """
        Links example to lexicon.
        """
        egOnlyBtns.eAdd2Lex(self)

    @QtCore.pyqtSlot()
    def on_eBreakLinkBtn_released(self):
        """
        breaks link to lexicon cards.
        """
        egOnlyBtns.eBreakLink(self)   

    @QtCore.pyqtSlot()
    def on_eCopyLineBtn_released(self):
        """
        copies example to clipboard.
        """
        egOnlyBtns.copyLine()

    @QtCore.pyqtSlot()
    def on_eNewEgBtn_released(self):
        """
        add new example card
        """
        menus.newCard(self)
    
    @QtCore.pyqtSlot()
    def on_eMakeIndexBtn_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: make Index not implemented yet
        raise NotImplementedError
    
    @QtCore.pyqtSlot(bool)
    def on_eAutoParsingBtn_toggled(self, checked):
        """
        Slot documentation goes here.
        """
        egOnlyBtns.toggleParse(self)
    
    @QtCore.pyqtSlot(int)
    def on_eLinksList_activated(self, index):
        """
        comboBox takes user to lex cards that are linked to examples.
        """
        lexRoot = dataIndex.lexDict[self.eLinksList.itemText(index)]
        cardLoader.loadLexCard(self, lexRoot)
        self.tabWidget.setCurrentIndex(1)

    '''metadata card buttons'''
    
    @QtCore.pyqtSlot()
    def on_oTestBtn_released(self):
        """
        test transformations on a string
        """
        metaDataBtns.oTest(self)
    
    @QtCore.pyqtSlot()
    def on_oClearTestBtn_released(self):
        """
        clear test fields
        """
        metaDataBtns.oClearTest(self)
    
    @QtCore.pyqtSlot()
    def on_oRandomBtn_released(self):
        """
        test alphabetizationon a random set of n lexical entries
        """
        metaDataBtns.oRandom(self)
    
    @QtCore.pyqtSlot(str)
    def on_oNumberBox_valueChanged(self, p0):
        """
        set the number of random lexical entries for orthography test.
        """
        metaDataBtns.oNumber(self)
    
    @QtCore.pyqtSlot()
    def on_oClearTransformBtn_released(self):
        """
        clear transform field.
        """
        metaDataBtns.oClearTransform(self)
    
    @QtCore.pyqtSlot()
    def on_oDeleteBtn_released(self):
        """
        delete orthography from orthpgraphies list.
        """
        metaDataBtns.oDelete(self)
    
    @QtCore.pyqtSlot()
    def on_oNewBtn_released(self):
        """
        define new orthography.
        """
        metaDataBtns.oNew(self)
    
    @QtCore.pyqtSlot()
    def on_oUpdateBtn_released(self):
        """
        update changes to orthography.
        """
        metaDataBtns.oUpdate(self)
    
    @QtCore.pyqtSlot()
    def on_oSetBtn_released(self):
        """
        selects orthography as the primary orthography.
        """
        metaDataBtns.oSet(self)
    
    @QtCore.pyqtSlot()
    def on_oApplyBtn_released(self):
        """
        applies the orthography to all lexical entries.
        """
        metaDataBtns.oApply(self)
        
    @QtCore.pyqtSlot()
    def on_mSpUpdateBtn_released(self):
        """
        update speaker metadata.
        """
        metaDataBtns.mSpUpdate(self)
    
    @QtCore.pyqtSlot()
    def on_mSpClearBtn_released(self):
        """
        clears speaker metadata.
        """
        metaDataBtns.mSpClear(self)
   
    @QtCore.pyqtSlot()
    def on_sSaveAsBtn_released(self):
        """
        Create new sort order file.
        """
        metaDataBtns.sSaveOrder(self)
        
    @QtCore.pyqtSlot()
    def on_sDeleteBtn_released(self):
        """
        remove an existing order
        """
        metaDataBtns.sDeleteOrder(self)
    
    @QtCore.pyqtSlot()
    def on_sTestBtn_released(self):
        """
        Test new order.
        """
        metaDataBtns.sTestOrder(self)
    
    @QtCore.pyqtSlot()
    def on_sUpdateBtn_released(self):
        """
        update order.
        """
        metaDataBtns.sUpdateOrder(self)
      
    @QtCore.pyqtSlot()
    def on_sNewBtn_released(self):
        """
        Creates new sortKey.
        """
        metaDataBtns.sNew(self)
        
    @QtCore.pyqtSlot()
    def on_sDoSort_released(self):
        """
        Slot documentation goes here.
        """
        metaDataBtns.sSort(self)
    
    @QtCore.pyqtSlot()
    def on_sMoveDownBtn_released(self):
        """
        Move selected order down in list.
        """
        metaDataBtns.sMoveDown(self)
    
    @QtCore.pyqtSlot()
    def on_sClearBtn_released(self):
        """
        Clear the Sorting Order and Exclusions fields.
        """
        metaDataBtns.sClear(self)

    @QtCore.pyqtSlot()
    def on_sMoveUpBtn_released(self):
        """
        Move selected order up in list.
        """
        metaDataBtns.sMoveUp(self)

    @QtCore.pyqtSlot()
    def on_mSpAddBtn_released(self):
        """
        add new speaker metadata.
        """
        metaDataBtns.mSpAdd(self)

    @QtCore.pyqtSlot()
    def on_mSpDelBtn_released(self):
        """
        delete speaker metadata.
        """
        metaDataBtns.mSpDel(self)
    
    @QtCore.pyqtSlot()
    def on_mRUpdateBtn_released(self):
        """
        update researcher metadata.
        """
        metaDataBtns.mRUpdate(self)
    
    @QtCore.pyqtSlot()
    def on_mRClearBtn_released(self):
        """
        clear researcher metadata entry fields.
        """
        metaDataBtns.mRClear(self)
    
    @QtCore.pyqtSlot()
    def on_mRAddBtn_released(self):
        """
        add new researcher metadata.
        """
        metaDataBtns.mRAdd(self)
    
    @QtCore.pyqtSlot()
    def on_mRDelBtn_released(self):
        """
        delete researcher metadata.
        """
        metaDataBtns.mRDel(self)
    
    @QtCore.pyqtSlot()
    def on_iEditAbbrBtn_released(self):
        """
        edits abbreviations field on index card.
        """
        indexOnlyBtns.iEditAbbr(self)
    
    '''index card buttons'''
    
    @QtCore.pyqtSlot()
    def on_iAddAbbrBtn_released(self):
        """
        adds abbreviation to list.
        """
        indexOnlyBtns.iAddAbbr(self)
    
    @QtCore.pyqtSlot()
    def on_iDelAbbrBtn_released(self):
        """
        deletes abbreviations from list.
        """
        indexOnlyBtns.iDelAbbr(self)
    
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_cSearchResults_clicked(self, index):
        """
        responds to user click on search results view on Search card
        """
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.KeyboardModifier.AltModifier:
            self.cSearchResults.model().removeRow(index.row())
            hitNumber = self.cSearchResults.model().rowCount()
            self.cNumberOfHits.setText('Hits: %s' %str(hitNumber))
            return
        if modifiers == QtCore.Qt.KeyboardModifier.MetaModifier:
            row = index.row()
            datum = self.cSearchResults.model().item(row, 0).text()
            datum = datum.replace("</p><p>", "\n")
            datum = datum.replace("</p>", "")
            datum = datum.replace("<p>", "")
            clipboard = QtWidgets.QApplication.clipboard()
            clipping = QtCore.QMimeData()
            clipping.setText(datum)
            clipboard.setMimeData(clipping)
            return
        tCard = self.cSearchResults.currentIndex().data(35)
        dataIndex.currentCard = tCard
        if tCard[0] == "L":
            targetCard = dataIndex.lexDict[tCard]
            cardLoader.loadLexCard(self, targetCard)
            self.tabWidget.setCurrentIndex(1)
        elif tCard[0] == "E":
            targetCard = dataIndex.exDict[tCard]
            cardLoader.loadEgCard(self, targetCard)
            self.tabWidget.setCurrentIndex(3)
        elif tCard[0] == "D":
            targetCard = dataIndex.dataDict[tCard]
            cardLoader.loadDataCard(self, targetCard)
            self.tabWidget.setCurrentIndex(4) 
        elif tCard[0] == "T":
            targetCard = dataIndex.textDict[tCard]
            lineList = targetCard.findall('Ln')
            for i in range(0,len(lineList)):
                if lineList[i].attrib.get('LnRef') == self.cSearchResults.currentIndex().data(36 ):
                    lineNo =i + 1
                    break
            cardLoader.loadTextCard(self, targetCard)
            self.tabWidget.setCurrentIndex(2)
            textWidget = self.textLayout.itemAtPosition(lineNo-1, 0)
            textTable = textWidget.widget()
            dataIndex.currentTextTable = textTable
            textTable.setStyleSheet("QTableWidget QHeaderView::section {border-bottom: 0px;"
                                                                    "border-left: 0px; border-top: 0px; border-right: 0px;"
                                                                    "padding: 5px; outline: 0px; background: #E6E6E6;}")    
            scroll = 0
            for i in range(0, self.textLayout.rowCount()):
                scroll += self.textLayout.itemAtPosition(i, 0).widget().height() + 9
                if i == lineNo - 1:
                    break
            self.tFullText.verticalScrollBar().setValue(scroll)        
        try:
            if self.recordBrowser:
                hitList = self.recordBrowser.hitList
                self.recordBrowser.listIndex = hitList.index(tCard)
                self.recordBrowser.progressBar.setValue(self.recordBrowser.listIndex)
        except AttributeError:
            pass    
    
    @QtCore.pyqtSlot()
    def on_cBrowseBtn_released(self):
        """
        Call search results browser.
        """
        if self.cSearchResults.model() != None:
            self.recordBrowser = RecordBrowser.RecordBrowser(self)
            self.recordBrowser.setObjectName('recordBrowser')
            self.recordBrowser.setModal(0)
            self.recordBrowser.setWindowFlags(QtCore.Qt.WindowType.Dialog | QtCore.Qt.WindowType.WindowStaysOnTopHint)
            self.recordBrowser.show()
            self.recordBrowser.raise_()
    
    @QtCore.pyqtSlot()
    def on_actionFind_by_ID_triggered(self):
        """
        Allows user to search for a record by unique ID
        """
        menus.findByID(self)
    
    @QtCore.pyqtSlot()
    def on_lineErrorPrev_released(self):
        """
        step back through line errors in the new text field.
        """
        newTextBtns.lineErrorPrev(self)
    
    @QtCore.pyqtSlot()
    def on_lineErrorNext_released(self):
        """
        step forward through line errors in the new text field.
        """
        newTextBtns.lineErrorNext(self)
    
    @QtCore.pyqtSlot()
    def on_wordErrorNext_released(self):
        """
        step forward through word errors in the new text field.
        """
        newTextBtns.wordErrorNext(self)
    
    @QtCore.pyqtSlot()
    def on_morphErrorNext_released(self):
        """
        step forward through morph errors in the new text field.
        """
        newTextBtns.morphErrorNext(self)
    
    @QtCore.pyqtSlot()
    def on_wordErrorPrev_released(self):
        """
        step back through word errors in the new text field.
        """
        newTextBtns.wordErrorPrev(self)
    
    @QtCore.pyqtSlot()
    def on_morphErrorPrev_released(self):
        """
        step back through morph errors in the new text field.
        """
        newTextBtns.morphErrorPrev(self)
    
    @QtCore.pyqtSlot()
    def on_tSpliceBtn_released(self):
        """
        Splices lines in interlinear. analyses that have been split to 
        fit a page width.
        """
        newTextBtns.lineSplicer(self)
    
    @QtCore.pyqtSlot()
    def on_portal_textChanged(self):
        """
        tracks edits in new text field.
        """
        newTextBtns.editTracker(self)
    
    
    @QtCore.pyqtSlot()
    def on_cTarget_returnPressed(self):
        """
        intitiates search for text in lineEdit.
        """
        searchOnlyBtns.searchFor(self)
    
    @QtCore.pyqtSlot()
    def on_cSaveResultsBtn_released(self):
        """
        write search results to file
        """
        searchOnlyBtns.saveResults(self)
    
    @QtCore.pyqtSlot(bool)
    def on_cFindAllBtn_toggled(self, checked):
        """
        resets switches in search focus box.
        
        @param checked DESCRIPTION
        @type bool
        """
        searchOnlyBtns.toggleFocus(self, checked)
        
    @QtCore.pyqtSlot()
    def on_cArchiveBtn_released(self):
        """
        archive search results for future reference
        """
        searchOnlyBtns.archive(self)
    
    @QtCore.pyqtSlot()
    def on_cLoadPrevBtn_released(self):
        """
        load archived search results.
        """
        searchOnlyBtns.load(self)
    
    @QtCore.pyqtSlot()
    def on_cClearResultsBtn_released(self):
        """
        clear search results field of search card
        """
        searchOnlyBtns.clearResults(self)
    
    @QtCore.pyqtSlot()
    def on_cReturnBtn_released(self):
        """
        Return to search form on lexicon card or to tab that initiated search.
        """
        searchOnlyBtns.returnToSearch(self)
    
    @QtCore.pyqtSlot()
    def on_actionFind_triggered(self):
        """
        find text anywhere on cards of current type
        """
        menus.findMenu(self)
    
    @QtCore.pyqtSlot()
    def on_actionFind_Again_triggered(self):
        """
        find text anywhere on cards of current type
        """
        menus.findAgain()
    
    @QtCore.pyqtSlot()
    def on_actionFuzzy_Find_triggered(self):
        """
        find ignoring caps, accents, diacrits
        """
        menus.fuzzyFind(self)
    
    @QtCore.pyqtSlot()
    def on_actionFuzzy_Find_Again_triggered(self):
        """
        repeat find ignoring caps, accents, diacrits
        """
        menus.fuzzyAgain()
    
    @QtCore.pyqtSlot(int)
    def on_eOrthography_activated(self, index):
        """
        changes display orthography for examples.
        """
        Orthographies.changeDisplayOrthography(self, index, 'Ex')
    
    @QtCore.pyqtSlot(int)
    def on_tOrthography_activated(self, index):
        """
        changes display orthography for texts.
        """
        Orthographies.changeDisplayOrthography(self, index, 'Txt')
    
    @QtCore.pyqtSlot()
    def on_actionItalic_triggered(self):
        """
        toggle italic typeface in textEdits.
        """
        field = QtGui.QGuiApplication.focusObject()
        if field.metaObject().className() == 'QTextEdit':
            state = field.fontItalic()
            field.setFontItalic(not state)
    
    @QtCore.pyqtSlot()
    def on_actionBold_triggered(self):
        """
        toggle boldface in textEdits.
        """
        field = QtGui.QGuiApplication.focusObject()
        if field.metaObject().className() == 'QTextEdit':
            if field.fontWeight() == QtGui.QFont.Bold:
                field.setFontWeight(QtGui.QFont.Normal)
            else:
                field.setFontWeight(QtGui.QFont.Bold)
    
    @QtCore.pyqtSlot()
    def on_actionUnderline_triggered(self):
        """
        toggle underline in textEdits.
        """
        field = QtGui.QGuiApplication.focusObject()
        if field.metaObject().className() == 'QTextEdit':
            state = field.fontUnderline()
            field.setFontUnderline(not state)
    
    @QtCore.pyqtSlot()
    def on_actionNormal_triggered(self):
        """
        removes font formatting.
        """
        field = QtGui.QGuiApplication.focusObject()
        if field.metaObject().className() == 'QTextEdit':
            field.setFontUnderline(0)
            field.setFontItalic(0)
            field.setFontWeight(QtGui.QFont.Normal)
