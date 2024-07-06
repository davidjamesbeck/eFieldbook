# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import os
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow
from .Ui_fieldbook import Ui_Fieldbook
from ELFB import dataIndex, cardLoader, Alphabetizer, menus, navLists, dictBuilder, contextMenus
from ELFB import lexOnlyBtns, textOnlyBtns, egOnlyBtns, metaDataBtns, tabConstructors
from ELFB import indexOnlyBtns, searchOnlyBtns, dsetOnlyBtns, Orthographies, exports
from ELFB import NumberedLineEdit, metaDataTableFillers, formattingHandlers, update
from ELFB.FocusOutFilter import FocusOutFilter, DialectFilter, BorrowFilter, ExLineFilter
from ELFB.palettes import LexSearchForm
from xml.etree import ElementTree as etree
from ELFB.ui.rsrc import images_rc


# from os import path

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
#        font = QtGui.QFont()
#        font.setFamily(font.defaultFamily())
        font = QtGui.QFont("Times New Roman")
        font.setWeight(QtGui.QFont.Weight.Light)
        QtWidgets.QApplication.setFont(font)
        self.ui = Ui_Fieldbook
        # self.settings = QtCore.QSettings('UNTProject', 'eFieldbook')
        self.settings = QtCore.QSettings(QtCore.QSettings.Format.NativeFormat, QtCore.QSettings.Scope.UserScope,
                                         'UNTProject', 'eFieldbook')
        self.Alphabetizer = Alphabetizer
        self.setupUi(self)
        dataIndex.fldbk = self
        homePath = QtCore.QDir.homePath()
        dirList = homePath.split('/')
        dataIndex.homePath = "/" + dirList[1] + '/' + dirList[2]
        self.setStyleSheet("QMessageBox QPushButton {border: 0px solid black;font-size: 10pts;padding: 0 5 0 5;"
                           "border-radius: 4px;min-width: 50px;min-height: 23px;"
                           "max-width: 180px;max-height: 23px;background: #6698FF;color: white;}")

        tabConstructors.grammarTableBuilder(self)
        tabConstructors.defTableBuilder(self)
        tabConstructors.egTableBuilder(self)
        tabConstructors.speakerTableBuilder(self)
        tabConstructors.researcherTableBuilder(self)
        tabConstructors.mediaTableBuilder(self)
        tabConstructors.egAbbreviationsBuilder(self)
        tabConstructors.indexAbbreviationsBuilder(self)
        tabConstructors.soundPanelBuilder(self)
        tabConstructors.navBarBuilder(self)

        """Load XML"""
        """determine the file to be opened on startup"""
        fname = None
        if self.settings.value('LastFile'):
            longName = dataIndex.homePath + self.settings.value('LastFile')
            if QtCore.QFile.exists(longName):
                """previously open file in QSettings exists, fname is set"""
                dataIndex.sourceFile = self.settings.value('LastFile')
                fname = longName
            try:
                xmltree = etree.parse(fname)
                dataIndex.root = xmltree.getroot()
            except (TypeError, PermissionError, FileNotFoundError) as err:
                """error arises if xml file can't be parsed by ElementTree"""
                print(err)
                xmlFile = QtCore.QFile(fname)
                if xmlFile.open(QtCore.QIODevice.OpenModeFlag.ReadOnly | QtCore.QIODevice.OpenModeFlag.Text):
                    """tries to open file using QFile"""
                    xmlStream = QtCore.QTextStream(xmlFile)
                    xmlString = xmlStream.readAll()
                    dataIndex.root = etree.XML(xmlString)
                    xmlFile.close()
                else:
                    """QFile.open() fails, fname reset to None"""
                    fname = None
        if fname is None:
            """if there is no file specified, ask for a file to open"""
            openFileDialog = QtWidgets.QFileDialog(self)
            filePath = openFileDialog.directory().currentPath()
            openFileDialog.setDirectory(filePath)
            fname = openFileDialog.getOpenFileName(self, "Open...", "")#, "XML (*.xml)")
            if len(fname[0]) != 0:
                """user selects file in FileDialog"""
                fname = fname[0]
                dataIndex.sourceFile = fname[len(dataIndex.homePath):]
                xmltree = etree.parse(fname)
                dataIndex.root = xmltree.getroot()
            else:
                """user presses 'Cancel' on the FileDialog"""
                blankDbFile = QtCore.QFile(dataIndex.rootPath + '/ELFB/newFileTemplate.xml')
                blankDbFile.open(QtCore.QIODevice.OpenModeFlag.ReadOnly | QtCore.QIODevice.OpenModeFlag.Text)
                blankDbString = blankDbFile.readAll()
                blankDbFile.close()
                dataIndex.root = etree.XML(blankDbString)
                del blankDbString
                dataIndex.sourceFile = 'blank database'
                menus.saveAsDb(self, 'newDb')

        self.giveWindowTitle()
        navLists.navListBuilderLex(self)
        navLists.navListBuilderText(self)
        navLists.navListBuilderData(self)
        dictBuilder.exDictBuilder()
        dictBuilder.mediaDictBuilder()
        dictBuilder.speakerDictBuilder()
        dictBuilder.rschrDictBuilder()

        """SET UP MENUS"""
        self.actionFind.setEnabled(0)
        self.actionFind_Again.setEnabled(0)
        self.actionFuzzy_Find.setEnabled(0)
        self.actionFuzzy_Find_Again.setEnabled(0)
        self.actionNewCard.setEnabled(0)
        self.actionCopyCard.setEnabled(0)
        self.actionDelCard.setEnabled(0)
        self.actionQuit.setShortcut(QtGui.QKeySequence("Ctrl+Q"))

        """BUILD ICONS AND RESOURCES"""
        AdvSearchIconSize = QtCore.QSize(50, 50)
        AdvSearchIcon = QtGui.QIcon(':AdvSearch.png')
        self.lAdvancedSearchBtn.setStyleSheet(
            'background: transparent; padding: 0px; min-width: 23px; min-height: 23px;')
        self.lAdvancedSearchBtn.setIcon(AdvSearchIcon)
        self.lAdvancedSearchBtn.setIconSize(AdvSearchIconSize)
        self.tAdvancedSearchBtn.setStyleSheet(
            'background: transparent; padding: 0px; min-width: 23px; min-height: 23px;')
        self.tAdvancedSearchBtn.setIcon(AdvSearchIcon)
        self.tAdvancedSearchBtn.setIconSize(AdvSearchIconSize)
        self.eAdvancedSearchBtn.setStyleSheet(
            'background: transparent; padding: 0px; min-width: 23px; min-height: 23px;')
        self.eAdvancedSearchBtn.setIcon(AdvSearchIcon)
        self.eAdvancedSearchBtn.setIconSize(AdvSearchIconSize)
        self.dAdvancedSearchBtn.setStyleSheet(
            'background: transparent; padding: 0px; min-width: 23px; min-height: 23px;')
        self.dAdvancedSearchBtn.setIcon(AdvSearchIcon)
        self.dAdvancedSearchBtn.setIconSize(AdvSearchIconSize)
        controlBar = ':ControlPanel.png'
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
                                               'background-image: url("%s");}' % controlBar)
        soundIconSize = QtCore.QSize(23, 23)
        soundIcon = QtGui.QIcon(':SpeakerBtn.png')
        self.mPlaySoundBtn.setStyleSheet(
            'border: 0px; background: transparent; padding: 0px; min-width: 23px; min-height: 23px;')
        self.mPlaySoundBtn.setIcon(soundIcon)
        self.mPlaySoundBtn.setIconSize(soundIconSize)
        infoIcon = QtGui.QIcon(':infoBtn.png')
        newCardIconSize = QtCore.QSize(40, 40)
        newCardIcon = QtGui.QIcon(':New.png')
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
        clipIcon = QtGui.QIcon(':Clip.png')
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
        duplicateIcon = QtGui.QIcon(':duplicate.png')
        self.eDuplicateBtn.setStyleSheet('QToolButton {border: 0px; background: transparent;'
                                         ' padding: 0px; min-width: 40px; min-height: 40px;}'
                                         'QToolButton:pressed {border: 3px outset transparent;}')
        self.eDuplicateBtn.setIcon(duplicateIcon)
        self.eDuplicateBtn.setIconSize(newCardIconSize)
        addMultiIcon = QtGui.QIcon(':addMulti.png')
        self.eAddMultiBtn.setStyleSheet('QToolButton {border: 0px; background: transparent;'
                                        ' padding: 0px; min-width: 40px; min-height: 40px;}'
                                        'QToolButton:pressed {border: 3px outset transparent;}')
        self.eAddMultiBtn.setIcon(addMultiIcon)
        self.eAddMultiBtn.setIconSize(newCardIconSize)
        indexIcon = QtGui.QIcon(':Index3.png')
        self.eMakeIndexBtn.setStyleSheet('QToolButton {border: 0px; background: transparent;'
                                         ' padding: 0px; min-width: 40px; min-height: 40px;}'
                                         'QToolButton:pressed {border: 3px outset transparent;}')
        self.eMakeIndexBtn.setIcon(indexIcon)
        self.eMakeIndexBtn.setIconSize(newCardIconSize)
        findUnparsedIcon = QtGui.QIcon(':Search.png')
        self.eFindUnparsedBtn.setStyleSheet('QToolButton {border: 0px; background: transparent;'
                                            ' padding: 0px; min-width: 40px; min-height: 40px;}'
                                            'QToolButton:pressed {border: 3px outset transparent;}')
        self.eFindUnparsedBtn.setIcon(findUnparsedIcon)
        self.eFindUnparsedBtn.setIconSize(newCardIconSize)

        """SET UP TABS AND SUB-CLASSED WIDGETS"""

        """TextEdits"""

        """Home tab"""
        dbTitle = dataIndex.root.attrib.get('Dbase')
        dbTitle = formattingHandlers.XMLtoRTF(dbTitle)
        self.hTitle.setText(dbTitle)
        self.hTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.filter = FocusOutFilter(self.hTitle)
        self.hTitle.installEventFilter(self.filter)
        self.hTitle.textChanged.connect(self.flagUnsavedEdits)

        lang = dataIndex.root.attrib.get('Language')
        self.hLanguage.setPlainText(lang)
        self.filter = FocusOutFilter(self.hLanguage)
        self.hLanguage.installEventFilter(self.filter)
        self.hLanguage.textChanged.connect(self.flagUnsavedEdits)

        family = dataIndex.root.attrib.get('Family')
        self.hFamily.setPlainText(family)
        self.filter = FocusOutFilter(self.hFamily)
        self.hFamily.installEventFilter(self.filter)
        self.hFamily.textChanged.connect(self.flagUnsavedEdits)

        population = dataIndex.root.attrib.get('Population')
        self.hPopulation.setPlainText(population)
        self.filter = FocusOutFilter(self.hPopulation)
        self.hPopulation.installEventFilter(self.filter)
        self.hPopulation.textChanged.connect(self.flagUnsavedEdits)

        location = dataIndex.root.attrib.get('Location')
        self.hLocation.setPlainText(location)
        self.filter = FocusOutFilter(self.hLocation)
        self.hLocation.installEventFilter(self.filter)
        self.hLocation.textChanged.connect(self.flagUnsavedEdits)

        iso = dataIndex.root.attrib.get('ISO')
        self.hISO.setPlainText(iso)
        self.filter = FocusOutFilter(self.hISO)
        self.hISO.installEventFilter(self.filter)
        self.hISO.textChanged.connect(self.flagUnsavedEdits)

        """Lexicon tab"""

        # Lexicographic info

        self.filter = FocusOutFilter(self.lOrthography)
        self.lOrthography.installEventFilter(self.filter)
        self.lOrthography.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.lPOS)
        self.lPOS.installEventFilter(self.filter)
        self.lPOS.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.lRegister)
        self.lRegister.installEventFilter(self.filter)
        self.lRegister.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.lIPA)
        self.lIPA.installEventFilter(self.filter)
        self.lIPA.textChanged.connect(self.flagUnsavedEdits)

        self.filter = DialectFilter(self.lDialect)
        self.lDialect.installEventFilter(self.filter)
        self.lDialect.textChanged.connect(self.flagUnsavedEdits)
        self.filter = BorrowFilter(self.lBrrw)
        self.lBrrw.installEventFilter(self.filter)
        self.lBrrw.textChanged.connect(self.flagUnsavedEdits)

        def grammarMenu(position):
            field = 'lGrammar'
            contextMenus.openContextMenu(self, field, position)

        self.lGrammar.customContextMenuRequested.connect(grammarMenu)

        def dialectMenu(position):
            field = 'lDialect'
            contextMenus.openContextMenu(self, field, position)

        self.lDialect.customContextMenuRequested.connect(dialectMenu)

        def L1Menu(position):
            field = 'lL1Definition'
            contextMenus.openContextMenu(self, field, position)

        self.lL1Definition.customContextMenuRequested.connect(L1Menu)

        def L2Menu(position):
            field = 'lL2Definition'
            contextMenus.openContextMenu(self, field, position)

        self.lL2Definition.customContextMenuRequested.connect(L2Menu)

        self.filter = FocusOutFilter(self.lLiteral)
        self.lLiteral.installEventFilter(self.filter)
        self.lLiteral.textChanged.connect(self.flagUnsavedEdits)

        # Metadata

        self.filter = FocusOutFilter(self.lSource)
        self.lSource.installEventFilter(self.filter)
        self.lSource.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.lResearcher)
        self.lResearcher.installEventFilter(self.filter)
        self.lResearcher.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.lDate)
        self.lDate.installEventFilter(self.filter)
        self.lDate.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.lUpdated)
        self.lUpdated.installEventFilter(self.filter)
        self.lUpdated.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.lConfirmed)
        self.lConfirmed.installEventFilter(self.filter)
        self.lConfirmed.textChanged.connect(self.flagUnsavedEdits)

        # Notes

        self.filter = FocusOutFilter(self.lNotes)
        self.lNotes.installEventFilter(self.filter)
        self.lNotes.textChanged.connect(self.flagUnsavedEdits)

        # Indices

        self.filter = FocusOutFilter(self.lPrimaryIndex)
        self.lPrimaryIndex.installEventFilter(self.filter)
        self.lPrimaryIndex.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.lSecondaryIndex)
        self.lSecondaryIndex.installEventFilter(self.filter)
        self.lSecondaryIndex.textChanged.connect(self.flagUnsavedEdits)

        self.filter = ExLineFilter(self.lKeywordIndex)
        self.lKeywordIndex.installEventFilter(self.filter)
        self.lKeywordIndex.textChanged.connect(self.flagUnsavedEdits)

        """text fields"""
        """Texts tab"""

        self.filter = FocusOutFilter(self.tSource)
        self.tSource.installEventFilter(self.filter)
        self.tSource.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.tResearcher)
        self.tResearcher.installEventFilter(self.filter)
        self.tResearcher.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.tDate)
        self.tDate.installEventFilter(self.filter)
        self.tDate.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.tUpdated)
        self.tUpdated.installEventFilter(self.filter)
        self.tUpdated.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.tTranscriber)
        self.tTranscriber.installEventFilter(self.filter)
        self.tTranscriber.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.tNotes)
        self.tNotes.installEventFilter(self.filter)
        self.tNotes.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.tTitle)
        self.tTitle.installEventFilter(self.filter)
        self.tTitle.textChanged.connect(self.flagUnsavedEdits)
        self.tTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        """Examples tab"""
        self.filter = ExLineFilter(self.eLine)
        self.eLine.installEventFilter(self.filter)
        self.eLine.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.eL1Gloss)
        self.eL1Gloss.installEventFilter(self.filter)
        self.eL1Gloss.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.eL2Gloss)
        self.eL2Gloss.installEventFilter(self.filter)
        self.eL2Gloss.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.eNotes)
        self.eNotes.installEventFilter(self.filter)
        self.eNotes.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.eKeywords)
        self.eKeywords.installEventFilter(self.filter)
        self.eKeywords.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.eSource)
        self.eSource.installEventFilter(self.filter)
        self.eSource.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.eResearcher)
        self.eResearcher.installEventFilter(self.filter)
        self.eResearcher.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.eDate)
        self.eDate.installEventFilter(self.filter)
        self.eDate.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.eUpdated)
        self.eUpdated.installEventFilter(self.filter)
        self.eUpdated.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.eSourceText)
        self.eSourceText.installEventFilter(self.filter)
        self.eSourceText.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.eTimeCode)
        self.eTimeCode.installEventFilter(self.filter)
        self.eTimeCode.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.eTimeCode)
        self.eSpokenBy.installEventFilter(self.filter)
        self.eSpokenBy.textChanged.connect(self.flagUnsavedEdits)

        """Datasets tab"""
        self.filter = FocusOutFilter(self.dSource)
        self.dSource.installEventFilter(self.filter)
        self.dSource.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.dResearcher)
        self.dResearcher.installEventFilter(self.filter)
        self.dResearcher.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.dDate)
        self.dDate.installEventFilter(self.filter)
        self.dDate.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.dKeywords)
        self.dKeywords.installEventFilter(self.filter)
        self.dKeywords.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.dNotes)
        self.dNotes.installEventFilter(self.filter)
        self.dNotes.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.dData)
        self.dData.installEventFilter(self.filter)
        self.dData.textChanged.connect(self.flagUnsavedEdits)
        self.dNumberBox = NumberedLineEdit.DataNumberWidget(self.datasets)
        self.dNumberBox.setGeometry(12, 72, 896, 480)

        self.filter = FocusOutFilter(self.dTitle)
        self.dTitle.installEventFilter(self.filter)
        self.dTitle.textChanged.connect(self.flagUnsavedEdits)

        """metadata tab"""
        self.filter = FocusOutFilter(self.oOrder)
        self.oOrder.installEventFilter(self.filter)
        self.oOrder.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.oDiacriticsField)
        self.oDiacriticsField.installEventFilter(self.filter)
        self.oDiacriticsField.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.sOrder)
        self.sOrder.installEventFilter(self.filter)
        self.sOrder.textChanged.connect(self.flagUnsavedEdits)

        self.filter = FocusOutFilter(self.sExclusions)
        self.sExclusions.installEventFilter(self.filter)
        self.sExclusions.textChanged.connect(self.flagUnsavedEdits)

        """buttons, list widgets and comboboxes"""

        """HOME Tab"""

        def goToLxCard():
            data = self.hLexNav.currentIndex().data(32)
            dataIndex.currentCard = data
            targetCard = dataIndex.lexDict[data]
            cardLoader.loadLexCard(targetCard)
            dataIndex.unsavedEdit = 0
            dataIndex.currentCard = data
            self.tabWidget.setCurrentIndex(1)

        self.hLexNav.clicked.connect(goToLxCard)

        def goToTxtCard():
            data = self.hTextNav.currentIndex().data(32)
            dataIndex.currentCard = data
            targetCard = dataIndex.textDict[data]
            self.tabWidget.setCurrentIndex(2)
            cardLoader.loadTextCard(targetCard)
            dataIndex.unsavedEdit = 0

        self.hTextNav.clicked.connect(goToTxtCard)

        def goToDataCard():
            data = self.hDataNav.currentIndex().data(32)
            dataIndex.currentCard = data
            targetCard = dataIndex.dataDict[data]
            cardLoader.loadDataCard(targetCard)
            self.tabWidget.setCurrentIndex(4)
            dataIndex.unsavedEdit = 0

        self.hDataNav.clicked.connect(goToDataCard)

        """Lexicon card"""

        def goToLxCard2():
            data = self.lLexNav.currentIndex().data(32)
            dataIndex.currentCard = data
            targetCard = dataIndex.lexDict[data]
            cardLoader.loadLexCard(targetCard)
            dataIndex.unsavedEdit = 0

        self.lLexNav.clicked.connect(goToLxCard2)

        def goToDerivation():
            data = self.lDerivatives.currentItem().data(32)
            targetCard = dataIndex.lexDict[data]
            cardLoader.loadLexCard(targetCard)
            dataIndex.unsavedEdit = 0
            for i in range(0, self.lLexNav.model().rowCount()):
                if self.lLexNav.model().index(i, 0).data(32) == data:
                    theItem = i
                    break
            self.lLexNav.setCurrentIndex(self.lLexNav.model().index(theItem, 0))
            self.lLexNav.scrollTo(self.lLexNav.currentIndex(), QtWidgets.QAbstractItemView.ScrollHint.PositionAtCenter)

        self.lDerivatives.doubleClicked.connect(goToDerivation)

        def goToBase():
            data = self.lBase.currentItem().data(32)
            targetCard = dataIndex.lexDict[data]
            cardLoader.loadLexCard(targetCard)
            dataIndex.unsavedEdit = 0
            for i in range(0, self.lLexNav.model().rowCount()):
                if self.lLexNav.model().index(i, 0).data(32) == data:
                    theItem = i
                    break
            self.lLexNav.setCurrentIndex(self.lLexNav.model().index(theItem, 0))
            self.lLexNav.scrollTo(self.lLexNav.currentIndex(), QtWidgets.QAbstractItemView.ScrollHint.PositionAtCenter)

        self.lBase.clicked.connect(goToBase)

        try:
            if dataIndex.root.attrib.get('lAuto') == 'on':
                self.lAutoBtn.setChecked(1)
        except AttributeError:
            pass

        """TextCard"""

        self.tText.setVisible(1)
        self.textLayout = QtWidgets.QVBoxLayout(self.tText)
        self.textLayout.setSpacing(8)
        self.textLayout.setStretch(0, 0)

        def goToTxtCard2():
            data = self.tTextNav.currentIndex().data(32)
            dataIndex.currentCard = data
            targetCard = dataIndex.textDict[data]
            cardLoader.loadTextCard(targetCard)
            dataIndex.unsavedEdit = 0

        self.tTextNav.clicked.connect(goToTxtCard2)
        comboBox = self.tOrthography
        Orthographies.fillOrthPickers(comboBox)

        """Example card"""

        metaDataTableFillers.fillAbbrevTables(self)

        comboBox = self.eOrthography
        Orthographies.fillOrthPickers(comboBox)

        """Datasets"""

        """ListWidgets"""

        def goToDataCard2():
            data = self.dDataNav.currentIndex().data(32)
            dataIndex.currentCard = data
            targetCard = dataIndex.dataDict[data]
            cardLoader.loadDataCard(targetCard)
            self.tabWidget.setCurrentIndex(4)
            dataIndex.unsavedEdit = 0

        self.dDataNav.clicked.connect(goToDataCard2)

        """Searches card"""

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

        """METADATA Tab"""

        """Consultants sub-tab"""

        metaDataTableFillers.fillConsultantTable(self)
        self.mSpTable.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.mSpSetDefaultBtn.setEnabled(0)

        """researchers sub-tab"""

        levelList = ['Admin', 'Editor', 'Output', 'Read only', 'None']
        self.mPrivilegesBox.insertItems(-1, levelList)
        self.mPrivilegesBox.setCurrentIndex(-1)
        metaDataTableFillers.fillRTable(self)
        self.mRTable.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.mRSetDefaultBtn.setEnabled(0)

        """media sub-tab"""

        self.mSpDelBtn.setEnabled(0)
        self.mSpUpdateBtn.setEnabled(0)
        self.mRDelBtn.setEnabled(0)
        self.mRUpdateBtn.setEnabled(0)

        metaDataTableFillers.fillMediaTable(self, infoIcon)
        if dataIndex.root.get("MediaFolder"):
            prefix = dataIndex.root.get("MediaFolder")
            self.mMediaPath.setText(prefix)
        self.mMediaTable.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)

        """orthographies sub-tab"""

        self.oList.setColumnWidth(0, 118)
        self.oList.setColumnWidth(1, 78)
        self.oList.verticalHeader().hide()
        self.oList.setAlternatingRowColors(1)
        self.oList.setStyleSheet("selection-background-color: #E6E6E6;")
        metaDataTableFillers.fillOrth(self)
        self.oList.itemClicked.connect(metaDataBtns.selectORow)
        self.oTransformBox.insertItem(0, 'Orth ⇨ Phon')
        self.oTransformBox.insertItem(1, 'Phon ⇨ Orth')
        self.oTransformBox.setStyleSheet('selection-color: blue;')
        newCardIconSize = QtCore.QSize(40, 40)
        newCardIcon = QtGui.QIcon(':HelpBtn.png')
        self.oHelpBtn.setIcon(newCardIcon)
        self.oHelpBtn.setIconSize(newCardIconSize)

        """alphabetization sub-tab"""

        metaDataTableFillers.fillSort(self)
        self.sList.itemClicked.connect(metaDataBtns.selectSRow)

        """index card"""

        self.iSortingBox.clear()
        self.iSortingBox.insertItem(0, 'Wordforms')
        self.iSortingBox.insertItem(1, 'Morphs')
        self.iSortingBox.insertItem(2, 'Analysis')

        self.iIndex.setTabStopDistance(150)

        """final setup"""

        dataIndex.lastText = dataIndex.root.attrib.get('LastText')
        dataIndex.lastLex = dataIndex.root.attrib.get('LastLex')
        dataIndex.lastEx = dataIndex.root.attrib.get('LastEx')
        dataIndex.lastDset = dataIndex.root.attrib.get('LastDset')
        keyList = list(dataIndex.root.keys())
        # if there are default researchers and speakers set, 
        # use these to set lastRschr and lastSpeaker, otherwise
        # use saved values for lastRschr and lastSpeaker
        if 'DefaultRschr' in keyList:
            dataIndex.lastRschr = dataIndex.root.attrib.get('DefaultRschr')
        elif 'LastRschr' in keyList:
            dataIndex.lastRschr = dataIndex.root.attrib.get('LastRschr')
        if 'DefaultSpeaker' in keyList:
            dataIndex.lastSpeaker = dataIndex.root.attrib.get('DefaultSpeaker')
        elif 'LastSpeaker' in keyList:
            dataIndex.lastSpeaker = dataIndex.root.attrib.get('LastSpeaker')

        self.recoverRecentFiles()
        dataIndex.unsavedEdit = 0

    def flagUnsavedEdits(self):
        """set flag when fields are edited"""
        dataIndex.unsavedEdit = 1
        return dataIndex.unsavedEdit

    @QtCore.pyqtSlot(int)
    def on_tabWidget_tabBarClicked(self, index):
        if self.tabWidget.currentIndex() == 1:
            try:
                if self.lSearchForm.isVisible() == 1:
                    self.lSearchForm.setVisible(0)
                    self.lexicon.setVisible(1)
            except AttributeError:
                pass

    @QtCore.pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        """
        Actions performed when tabWidget is clicked.
        """
        if dataIndex.sourceFile is None:
            return
        if self.tabWidget.currentIndex() == 0:  # Home tab
            self.actionNewCard.setEnabled(False)
            self.actionCopyCard.setEnabled(False)
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
            dataIndex.currentCard = 'Home'

        if self.tabWidget.currentIndex() == 1:  # Lexicon tab
            if dataIndex.unsavedEdit == 1:
                pendingChange = 1
            else:
                pendingChange = 0
            lastLex = dataIndex.root.attrib.get('LastLex')
            if lastLex:
                entry = dataIndex.lexDict[lastLex]
            else:
                lastLex = self.lLexNav.model().index(0, 0).data(32)
                entry = dataIndex.lexDict[lastLex]
                dataIndex.lastLex = lastLex
            cardLoader.loadLexCard(entry)
            dataIndex.currentCard = lastLex
            """this sets up the menus, etc"""
            self.actionNewCard.setEnabled(True)
            self.actionCopyCard.setEnabled(True)
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
            for i in range(0, self.lLexNav.model().rowCount()):
                if self.lLexNav.model().index(i, 0).data(32) == lastLex:
                    theItem = i
                    break
            self.lLexNav.setCurrentIndex(self.lLexNav.model().index(theItem, 0))
            self.lLexNav.scrollTo(self.lLexNav.currentIndex(), QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
            if pendingChange:
                dataIndex.unsavedEdit = 1
            else:
                dataIndex.unsavedEdit = 0
            return theItem

        if self.tabWidget.currentIndex() == 2:  # Texts tab
            if dataIndex.unsavedEdit == 1:
                pendingChange = 1
            else:
                pendingChange = 0
            lastText = dataIndex.root.attrib.get('LastText')
            if lastText:
                entry = dataIndex.textDict[lastText]
                for i in range(0, self.tTextNav.model().rowCount()):
                    if self.tTextNav.model().index(i, 0).data(32) == lastText:
                        theItem = i
                        break
                self.tTextNav.setCurrentIndex(self.tTextNav.model().index(theItem, 0))
                self.tTextNav.scrollTo(self.tTextNav.currentIndex(),
                                       QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
                dataIndex.currentCard = lastText
            entry = dataIndex.textDict[lastText]
            cardLoader.loadTextCard(entry)
            dataIndex.currentCard = lastText
            self.actionNewCard.setEnabled(True)
            self.actionCopyCard.setEnabled(True)
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
                textOnlyBtns.enterNewText(self)

        if self.tabWidget.currentIndex() == 3:  # Examples tab
            if dataIndex.unsavedEdit == 1:
                pendingChange = 1
            else:
                pendingChange = 0

            lastEx = dataIndex.root.attrib.get('LastEx')
            if lastEx:
                entry = dataIndex.exDict[lastEx]
            else:
                entry = dataIndex.root.find('Ex')
            cardLoader.loadExCard(entry)
            self.actionNewCard.setEnabled(True)
            self.actionCopyCard.setEnabled(True)
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

        if self.tabWidget.currentIndex() == 4:  # Datasets tab
            if dataIndex.unsavedEdit == 1:
                pendingChange = 1
            else:
                pendingChange = 0
            lastDset = dataIndex.root.attrib.get('LastDset')
            if lastDset:
                entry = dataIndex.dataDict[lastDset]
                for i in range(0, self.dDataNav.model().rowCount()):
                    if self.dDataNav.model().index(i, 0).data(32) == lastDset:
                        theItem = i
                        break
                self.dDataNav.setCurrentIndex(self.dDataNav.model().index(theItem, 0))
                self.dDataNav.scrollTo(self.dDataNav.currentIndex(),
                                       QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
                dataIndex.currentCard = lastDset
            else:
                lastDset = dataIndex.root.find('Dset')
            entry = dataIndex.dataDict[lastDset]
            cardLoader.loadDataCard(entry)
            dataIndex.currentCard = lastDset
            self.actionNewCard.setEnabled(True)
            self.actionCopyCard.setEnabled(True)
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

        if self.tabWidget.currentIndex() == 5:  # Search tab
            self.actionNewCard.setEnabled(False)
            self.actionCopyCard.setEnabled(False)
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

        if self.tabWidget.currentIndex() == 6:  # Meta tab
            self.actionNewCard.setEnabled(False)
            self.actionCopyCard.setEnabled(False)
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

        if self.tabWidget.currentIndex() == 7:  # Index tab
            self.actionNewCard.setEnabled(False)
            self.actionCopyCard.setEnabled(False)
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

        try:
            if self.lSearchForm.isVisible() == 1:
                self.lSearchForm.setVisible(0)
                self.lexicon.setVisible(1)
        except AttributeError:
            pass

    def recoverRecentFiles(self):
        """get list of recently opened files from QSettings and store it in dataIndex"""
        try:
            if len(self.settings.value('RecentFile')) != 0:
                fnames = self.settings.value('RecentFile')
                dataIndex.recentFile = []
                for i in range(0, len(fnames)):
                    if fnames[i] == dataIndex.sourceFile:
                        continue
                    if QtCore.QFile.exists(dataIndex.homePath + fnames[i]):
                        dataIndex.recentFile.append(fnames[i])
        except TypeError:
            pass

    def giveWindowTitle(self):
        if dataIndex.sourceFile is not None:
            self.setWindowTitle("{0}[*]".format(os.path.basename(dataIndex.sourceFile)))
        else:
            self.setWindowTitle("Electronic Fieldbook")

    def closeEvent(self, event):
        menus.closeDb(self)

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
    def on_actionCopyCard_triggered(self):
        """
        copy current card.
        """
        menus.copyCard(self)

    @QtCore.pyqtSlot()
    def on_actionDelCard_triggered(self):
        """
        delete records from database
        """
        menus.delCard(self)

    @QtCore.pyqtSlot(bool)
    def on_tNewAutoparseBtn_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        textOnlyBtns.toggleParse(self)

    @QtCore.pyqtSlot()
    def on_eFindUnparsedBtn_released(self):
        """
        Load next unparsed example.
        """
        egOnlyBtns.findUnparsed(self)

    @QtCore.pyqtSlot()
    def on_dNewDsetBtn_released(self):
        """
        create new dataset.
        """
        menus.newCard(self)

    @QtCore.pyqtSlot()
    def on_dAdvancedSearchBtn_released(self):
        """
        Search examples.
        """
        dsetOnlyBtns.dAdvancedSearch(self)

    """sound buttons (all cards)"""

    @QtCore.pyqtSlot()
    def on_dResetBtn_released(self):
        """
        Remove highlighting from search results.
        """
        dsetOnlyBtns.removeHiliting(self)

    @QtCore.pyqtSlot()
    def on_eDuplicateBtn_released(self):
        """
        Slot documentation goes here.
        """
        egOnlyBtns.eDuplicate(self)

    @QtCore.pyqtSlot()
    def on_eAdvancedSearchBtn_released(self):
        """
        Search examples.
        """
        egOnlyBtns.eAdvancedSearch(self)

    @QtCore.pyqtSlot()
    def on_mPlaySoundBtn_released(self):
        """
        plays selected sound in MediaTable when speaker button is pressed.
        """
        metaDataBtns.playSound(self)

    @QtCore.pyqtSlot()
    def on_mAddMediaBtn_released(self):
        """
        adds media to database.
        """
        metaDataBtns.newMedia(self)

    @QtCore.pyqtSlot()
    def on_mDelMediaBtn_released(self):
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
            mediaElement = self.mMediaTable.currentItem().data(36)
            mediaID = mediaElement.attrib.get('MedID')
            del dataIndex.mediaDict[mediaID]
            dataIndex.root.remove(mediaElement)
            self.mMediaTable.removeRow(self.mMediaTable.currentRow())
            self.mMediaTable.setCurrentCell(-1, -1)
            update.cleanUpIDs(mediaID)
            dataIndex.unsavedEdit = 1

    @QtCore.pyqtSlot()
    def on_mMediaPath_editingFinished(self):
        """
        updates the MediaFolder attribute in the XML database, which sets
        the default directory for media files
        """
        newPath = self.mMediaPath.text()
        dataIndex.root.set("MediaFolder", newPath)
        dataIndex.unsavedEdit = 1

    """lexicon card buttons"""

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
                for i, item in enumerate(elemList):
                    if item.tag == 'POS':
                        break
                    elif item.tag == 'Orth':
                        break
                i = len(elemList) - i
                lexNode.insert(i, etree.Element('IPA'))
                lexNode.find('IPA').text = IPA
            self.lIPA.setText(IPA)
            dataIndex.unsavedEdits = 1

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
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.KeyboardModifier.AltModifier:
            outputLanguage = 'L2'
        else:
            outputLanguage = 'L1'
        lexOnlyBtns.clipEG(outputLanguage)

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem)
    def on_iErrorBox_itemClicked(self, item):
        """
        Slot documentation goes here.
        
        @param item DESCRIPTION
        @type QListWidgetItem
        """
        cardID = item.text()
        tEntry = dataIndex.exDict[cardID]
        cardLoader.loadExCard(tEntry)
        self.tabWidget.setCurrentIndex(3)

    @QtCore.pyqtSlot()
    def on_iFindInIndex_returnPressed(self):
        """
        Find text in Index
        """
        indexOnlyBtns.findFirst(self)

    @QtCore.pyqtSlot()
    def on_iFindNextBtn_released(self):
        """
        Find text in Index
        """
        indexOnlyBtns.findFirst(self)

    @QtCore.pyqtSlot()
    def on_lAdvancedSearchBtn_released(self):
        """
        Slot documentation goes here.
        """
        try:
            self.lSearchForm.setVisible(1)
            self.lSearchForm.clearAll()
        except AttributeError:
            self.lSearchForm = LexSearchForm.LexSearchForm(self)
            self.lSearchForm.setGeometry(10, 40, 1126, 686)
            self.lSearchForm.setVisible(1)
        self.lexicon.setVisible(0)

    """text card only buttons"""

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
        calls egOnlyBtns
        """
        try:
            currentTable = dataIndex.currentTextTable
            node = currentTable.verticalHeaderItem(0).data(35)
        except AttributeError:
            return
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.KeyboardModifier.AltModifier:
            outputLanguage = 'L2'
        else:
            outputLanguage = 'L1'
        egOnlyBtns.copyLine(node, outputLanguage)

    @QtCore.pyqtSlot()
    def on_tClipBtn_released(self):
        """
        Place text on clipboard.
        """
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.KeyboardModifier.AltModifier:
            outputLanguage = 'L2'
        else:
            outputLanguage = 'L1'
        textOnlyBtns.clipText(self, outputLanguage)

    @QtCore.pyqtSlot()
    def on_tNewTextBtn_released(self):
        """
        button to add a new text.
        """
        textOnlyBtns.enterNewText(self)

    @QtCore.pyqtSlot()
    def on_tAdvancedSearchBtn_released(self):
        """
        Search examples.
        """
        textOnlyBtns.tAdvancedSearch(self)

    """example card only buttons"""

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
        egOnlyBtns.editAbbr(self, 'eg')

    @QtCore.pyqtSlot()
    def on_eLocateBtn_released(self):
        """
        take uses to context where example was found (if any).
        """
        egOnlyBtns.eLocateEg(self)

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
    def on_eDelColumnBtn_released(self):
        """
        delete a column in an example table.
        """
        egOnlyBtns.delColumn(self)

    @QtCore.pyqtSlot()
    def on_eGoToLinkBtn_released(self):
        """
        go to selected card in links menu.
        """
        egOnlyBtns.goToLink(self)

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
    def on_eSplitColumnBtn_released(self):
        """
        Split a column into two.
        """
        egOnlyBtns.eSplitColumn(self)

    @QtCore.pyqtSlot()
    def on_eAddExampleBtn_released(self):
        """
        Links example to lexicon.
        """
        egOnlyBtns.eAdd2Lex(self)

    @QtCore.pyqtSlot()
    def on_eBreakLnkBtn_released(self):
        """
        breaks link to lexicon cards.
        """
        egOnlyBtns.eBreakLink(self)

    @QtCore.pyqtSlot()
    def on_eCopyLineBtn_released(self):
        """
        copies example to clipboard.
        """
        node = dataIndex.exDict[dataIndex.currentCard]
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.KeyboardModifier.AltModifier:
            outputLanguage = 'L2'
        else:
            outputLanguage = 'L1'
        egOnlyBtns.copyLine(node, outputLanguage)

    @QtCore.pyqtSlot()
    def on_eNewEgBtn_released(self):
        """
        add new example card
        """
        menus.newCard(self)

    @QtCore.pyqtSlot()
    def on_eMakeIndexBtn_released(self):
        """
        Build a morphological index.
        Calls "indexOnlyBtns.py", not "egOnlyBtns.py".
        """
        indexOnlyBtns.buildIndex()

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
        cardLoader.loadLexCard(lexRoot)
        self.tabWidget.setCurrentIndex(1)

    """metadata card buttons"""

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
    def on_iUpdateExampleBtn_released(self):
        """
        Make corrections to all instances of a wordform.
        """
        indexOnlyBtns.updateWordForms(self)

    @QtCore.pyqtSlot()
    def on_iEditAbbrBtn_released(self):
        """
        edits abbreviations field on index card.
        Calls to egOnlyBtns
        """
        egOnlyBtns.editAbbr(self, 'index')

    """index card buttons"""

    @QtCore.pyqtSlot()
    def on_iSortNowBtn_released(self):
        """
        Initiate sort of index field.
        """
        indexOnlyBtns.sortNow(self)

    @QtCore.pyqtSlot()
    def on_iDuplicateBtn_released(self):
        """
        Highlight potential duplicates in index field
        based on sorting paramaters in combobox
        """
        indexOnlyBtns.showDuplicates(self)

    @QtCore.pyqtSlot(int)
    def on_iSortingBox_currentIndexChanged(self, index):
        """
        Sort index field.
        
        @param index DESCRIPTION
        @type int
        """
        indexOnlyBtns.sortIndex(self, index)

    @QtCore.pyqtSlot()
    def on_iAddAbbrBtn_released(self):
        """
        adds abbreviation to list.
        Calls egOnlyBtns.py
        """
        egOnlyBtns.addAbbr(self)

    @QtCore.pyqtSlot()
    def on_iDelAbbrBtn_released(self):
        """
        deletes abbreviations from list.
        """
        indexOnlyBtns.iDelAbbr(self)

    @QtCore.pyqtSlot()
    def on_iBrowseBtn_released(self):
        """
        Call index browser.
        """
        indexOnlyBtns.indexBrowser(self)

    @QtCore.pyqtSlot()
    def on_iLocateBtn_released(self):
        """
        Find selected form.
        """
        indexOnlyBtns.findForm(self)

    @QtCore.pyqtSlot()
    def on_iConcordanceBtn_released(self):
        """
        Gather examples on search card.
        """
        indexOnlyBtns.makeSet(self)

    @QtCore.pyqtSlot()
    def on_iBuildIndexBtn_released(self):
        """
        Build morphological index.
        """
        indexOnlyBtns.buildIndex()

    @QtCore.pyqtSlot()
    def on_iTabSlider_sliderReleased(self):
        """
        Slot documentation goes here.
        """
        value = self.iTabSlider.value()
        self.iIndex.setTabStopDistance(value * 10)

    @QtCore.pyqtSlot()
    def on_iClearHiliteBtn_released(self):
        """
        Reset hilited text in Index field.
        """
        indexOnlyBtns.clearHighlighting(self)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_cSearchResults_clicked(self, index):
        """
        responds to user click on search results view on Search card
        """
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.KeyboardModifier.AltModifier:
            self.cSearchResults.model().removeRow(index.row())
            hitNumber = self.cSearchResults.model().rowCount()
            self.cNumberOfHits.setText('Hits: %s' % str(hitNumber))
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
            cardLoader.loadLexCard(targetCard)
            self.tabWidget.setCurrentIndex(1)
        elif tCard[0] == "E":
            targetCard = dataIndex.exDict[tCard]
            cardLoader.loadExCard(targetCard)
            self.tabWidget.setCurrentIndex(3)
        elif tCard[0] == "D":
            targetCard = dataIndex.dataDict[tCard]
            cardLoader.loadDataCard(targetCard)
            self.tabWidget.setCurrentIndex(4)
        elif tCard[0] == "T":
            targetCard = dataIndex.textDict[tCard]
            lineList = targetCard.findall('Ln')
            for i in range(0, len(lineList)):
                if lineList[i].attrib.get('LnRef') == self.cSearchResults.currentIndex().data(36):
                    lineNo = i + 1
                    break
            cardLoader.loadTextCard(targetCard)
            self.tabWidget.setCurrentIndex(2)
            textWidget = self.textLayout.itemAtPosition(lineNo - 1, 0)
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
        searchOnlyBtns.searchBrowser(self)

    @QtCore.pyqtSlot()
    def on_actionFind_by_ID_triggered(self):
        """
        Allows user to search for a record by unique ID
        """
        menus.findByID(self)

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
        menus.findAgain(self)

    @QtCore.pyqtSlot()
    def on_actionFuzzy_Find_triggered(self):
        """
        find ignoring caps, accents, diacrits
        """
        menus.fuzzyFind(self)

    @QtCore.pyqtSlot()
    def on_actionLook_Up_triggered(self):
        """
        find lexical entry by name or ID number
        """
        menus.lookUp(self)

    @QtCore.pyqtSlot(bool)
    def on_actionSession_Date_triggered(self):
        """
        toggle session date on/off
        """
        p0 = self.actionSession_Date.isChecked()
        if p0 is True:
            dataIndex.sessionDate = None
        else:
            dataIndex.sessionDate = 'today'
        menus.setSessionDate()

    @QtCore.pyqtSlot()
    def on_actionSession_Speaker_triggered(self):
        """
        Set default speaker for session.
        """
        p0 = self.actionSession_Speaker.isChecked()
        menus.setSessionSpeaker(p0)

    @QtCore.pyqtSlot()
    def on_actionSession_Researcher_triggered(self):
        """
        Set default researcher for session.
        """
        p0 = self.actionSession_Researcher.isChecked()
        menus.setSessionResearcher(p0)

    @QtCore.pyqtSlot()
    def on_actionFuzzy_Find_Again_triggered(self):
        """
        repeat find ignoring caps, accents, diacrits
        """
        menus.fuzzyAgain(self)

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
            if field.fontWeight() == QtGui.QFont.Weight.Bold:
                field.setFontWeight(QtGui.QFont.Weight.Normal)
            else:
                field.setFontWeight(QtGui.QFont.Weight.Bold)

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
            field.setFontWeight(QtGui.QFont.Weight.Normal)

    @QtCore.pyqtSlot(bool)
    def on_mSpSetDefaultBtn_toggled(self, checked):
        """
        Sets a default speaker to be filled in on new cards.
        
        @param checked DESCRIPTION
        @type bool
        """
        if checked is True:
            speaker = self.mSCode.toPlainText()
            dataIndex.sessionSpeaker = speaker
            dataIndex.lastSpeaker = speaker
        else:
            dataIndex.sessionSpeaker = None

    @QtCore.pyqtSlot(bool)
    def on_mRSetDefaultBtn_toggled(self, checked):
        """
        sets a default researcher to be filled in on new cards.
        
        @param checked DESCRIPTION
        @type bool
        """
        if checked is True:
            researcher = self.mRCode.toPlainText()
            dataIndex.sessionRschr = researcher
            dataIndex.lastRschr = researcher
        else:
            dataIndex.sessionRschr = None

    @QtCore.pyqtSlot()
    def on_iClearFieldBtn_released(self):
        """
        clear index field.
        """
        self.iIndex.clear()

    @QtCore.pyqtSlot()
    def on_eClearAnalysisBtn_released(self):
        """
        clear analysis from EgTable
        """
        egOnlyBtns.clearAnalysis(self)

    @QtCore.pyqtSlot()
    def on_oHelpBtn_released(self):
        """
        helpf for using orthographies.
        """
        metaDataBtns.oHelp(self)

    @QtCore.pyqtSlot()
    def on_eAddMultiBtn_released(self):
        """
        load multiple examples into the database.
        """
        egOnlyBtns.addMulti(self)

    @QtCore.pyqtSlot()
    def on_actionLoad_Schema_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: this is just a temporary fix
        print("entering on_actionLoad_Schema_triggered")
        exports.outputLexiconToCSV(self)
        exports.sayHello()
