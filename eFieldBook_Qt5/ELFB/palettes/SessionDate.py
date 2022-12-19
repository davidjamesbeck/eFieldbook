# -*- coding: utf-8 -*-

"""
Module implementing SessionManagers.
These set defaults for date, researcher, and speaker
to avoid having to enter them over and over in a session.
"""

from PyQt6.QtCore import pyqtSlot, QSize, Qt
from PyQt6.QtWidgets import QDialog, QComboBox, QPlainTextEdit
from PyQt6.QtGui import QFont
from ELFB import dataIndex
from datetime import date

from .Ui_SessionDate import Ui_SessionDateManager


def dateFinder():
    tDate = date.isoformat(date.today())
    return tDate


class SessionManager(QDialog, Ui_SessionDateManager):
    """
    Class documentation goes here.
    """

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        self.accept()

    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        self.reject()


class SessionDateManager(SessionManager, Ui_SessionDateManager):

    def __init__(self, parent=None):
        super(SessionDateManager, self).__init__(parent)
        self.setupUi(self)
        self.sessionDateEdit = QPlainTextEdit()
        self.sessionDateEdit.setMinimumSize(QSize(150, 24))
        self.sessionDateEdit.setMaximumSize(QSize(150, 24))
        today = dateFinder()
        self.sessionDateEdit.setPlainText(today)
        font = QFont()
        font.setPointSize(13)
        self.sessionDateEdit.setFont(font)
        self.sessionDateEdit.setObjectName("sessionDateEdit")
        self.verticalLayout.insertWidget(0, self.sessionDateEdit)

    def getSessionDate(self):
        tDate = self.sessionDateEdit.toPlainText()
        return tDate


class SessionSpeakerManager(SessionManager, Ui_SessionDateManager):

    def __init__(self, parent=None):
        super(SessionSpeakerManager, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Session Speaker")
        self.setToolTip('Choose a speaker to fill in by default for the remainder of the session.')
        self.label.setText('Set a default a speaker\nfor the work session.')
        self.speakerCode = QComboBox()
        self.speakerCode.setMinimumSize(QSize(164, 32))
        self.speakerCode.setMaximumSize(QSize(164, 32))
        codeList = sorted(dataIndex.speakerDict.keys())
        for index, item in enumerate(codeList):
            try:
                fullName = dataIndex.speakerDict.get(item).findtext('Name')
                if fullName == 'Unattributed':
                    fullName = 'unattr.'
                item += ' (' + fullName + ')'
            except TypeError:
                item += ' (unattr.)'
            codeList[index] = item
        self.speakerCode.insertItems(0, codeList)
        self.verticalLayout.insertWidget(0, self.speakerCode)
        if dataIndex.lastSpeaker is not None:
            i = self.speakerCode.findText(dataIndex.lastSpeaker, Qt.MatchFlag.MatchStartsWith)
            self.speakerCode.setCurrentIndex(i)

    def getSessionSpeaker(self):
        speaker = self.speakerCode.currentText().split(None, 1)[0]
        return speaker


class SessionResearcherManager(SessionManager, Ui_SessionDateManager):

    def __init__(self, parent=None):
        super(SessionResearcherManager, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Session Researcher")
        self.setToolTip('Choose a researcher to fill in by default for the remainder of the session.')
        self.label.setText('Set a default a researcher\nfor the work session.')
        self.rschrCode = QComboBox()
        self.rschrCode.setMinimumSize(QSize(164, 32))
        self.rschrCode.setMaximumSize(QSize(164, 32))
        codeList = sorted(dataIndex.rschrDict.keys())
        self.rschrCode.insertItems(0, codeList)
        self.verticalLayout.insertWidget(0, self.rschrCode)
        if dataIndex.lastRschr is not None:
            i = self.rschrCode.findText(dataIndex.lastRschr, Qt.MatchFlag.MatchExactly)
            self.rschrCode.setCurrentIndex(i)

    def getSessionResearcher(self):
        researcher = self.rschrCode.currentText().split(None, 1)[0]
        return researcher
