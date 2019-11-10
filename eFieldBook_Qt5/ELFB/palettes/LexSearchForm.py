
"""
Module implementing lexicon search form.
"""

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot
from ELFB import dataIndex, searchClasses

from .Ui_LexSearchForm import Ui_LexSearchForm

class LexSearchForm(QtWidgets.QWidget, Ui_LexSearchForm):
    """
    Class documentation goes here.
    """

    def __init__(self, parent):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(LexSearchForm, self).__init__(parent)
        self.setupUi(self)
        dataIndex.updateEnabled = 'off'
        dataIndex.activeSearch = 1
        self.sDoneBtn.setCheckState(1)
    
        controlBar = ':ControlPanel.png'
        self.lSearchControlBar.setStyleSheet("QPushButton {border: 0px solid black;"
    "     border-radius: 4px;"
    "     min-width: 70px;"
    "     min-height: 24px;"
    "     max-width: 70px;"
    "     max-height: 24px;"
    "     background: #6698FF;"
    "     color: white;}"
    "QPushButton:pressed {background: #1E90FF; border: 2px outset #1E90FF;}"
    "QFrame {border: 1px solid gray; "
            "border: 0px solid black;"
            "border-radius: 8px;"
            "padding: 0px;"
            "background-image: url('%s');}" %controlBar)

        self.instruction.setText('Enter text to find in the fields where you wish to search. '
                                            'Entering terms in more than one field will search for entries that '
                                            'meet all search criteria.\n\n'
                                            'Enter "&" between AND search terms in the same field, place "¬" before terms '
                                            'for NOT searches. \n\nFor edge-sensitive searches, place "#" on the edge you '
                                            'wish the search to key on (e.g., "#an" will find all words beginning '
                                            'with the string "an").\n\n'
                                            'Combine AND/NOT and "#" in the order "¬#". \n\n'
                                            'Use the checkboxes on the left to parameterize searches.')
                                            
    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return: 
            self.callSearchEngine()
        else:
            super().keyPressEvent(qKeyEvent)   
            
    def callSearchEngine(self):
        fldbk = dataIndex.fldbk
        engine = searchClasses.LexSearchEngine(fldbk)
        parameters = self.setParameters()
        engine.parameters = parameters
        fieldList = self.listFields()
        engine.fieldList = fieldList
        engine.doSearch()
        self.setVisible(0)
    
    def listFields(self):
        '''returns a list of search fields with context''' 
        fldList = []
        childList = self.findChildren(QtWidgets.QLineEdit)
        for child in childList:
            '''this condition seems to be needed because there is a "ghost" LineEdit with no name'''
            if len(child.objectName()) == 0:
                 continue
            elif child.objectName()[0] == 'l' and len(child.text()) != 0:
                fldList.append(child)
        return fldList
    
    def setParameters(self):
        '''parameters = [accent,diacrit,case,append,recOnly,wholeWord,secondLanguage]'''
        parameters = []
        if self.accentBtn.isChecked():
            parameters.append(1)
        else:
            parameters.append(0)
        if self.diacritBtn.isChecked():
            parameters.append(1)
        else:
            parameters.append(0)
        if self.caseBtn.isChecked():
            parameters.append(1)
        else:
            parameters.append(0)    
        if self.appendBtn.isChecked():
            parameters.append(1)
        else:
            parameters.append(0)    
        parameters.append(0) #this is a dummy list item to stand in for "recOnly" 
        if self.wholeWordBtn.isChecked():
            parameters.append(1)
        else:
            parameters.append(0)
        if self.setLangBtn.isChecked():
            parameters.append(1)
        else:
            parameters.append(0) 
        return parameters
    
    def clearAll(self):
        fldList = self.listFormFields()  
        for fld in fldList:
            fld.clear()
    
    def listFormFields(self):
        fldList = []
        childList = self.findChildren(QtWidgets.QLineEdit)
        for child in childList:
            try:
                if child.objectName()[0] == 'l':
                    fldList.append(child)
            except IndexError:
                pass
        return fldList
        
    def restoreLexCard(self):
        dataIndex.updateEnabled = 'on'
        dataIndex.activeSearch = None
        self.setVisible(0)
        dataIndex.fldbk.lexicon.setVisible(1)
    
    @pyqtSlot()
    def on_doSearch_released(self):
        """
        Slot documentation goes here.
        """
        self.callSearchEngine()
    
    @pyqtSlot()
    def on_clearForm_released(self):
        """
        Clear all field on form
        """
        self.clearAll()
    
    @pyqtSlot()
    def on_lCancelSearch_released(self):
        """
        Close form, return to last lexicon card
        """
        self.restoreLexCard()
