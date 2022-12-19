# -*- coding: utf-8 -*-

"""
Module implementing navigation bar for data cards.
"""

from PyQt6 import QtWidgets, QtCore, QtGui
from ELFB import dataIndex, cardLoader
# from xml.etree import ElementTree as etree
# import re
from .Ui_NavBar import Ui_NavBar


class NavBar(QtWidgets.QWidget, Ui_NavBar):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):

        super(NavBar, self).__init__(parent)
        self.setupUi(self)
        self.stack = []
        self.index = 0
        controlBar = ':ControlPanel.png'
        self.ControlBar.setStyleSheet('QToolButton {background: transparent;'
                                      'min-width: 32px;'
                                      'min-height: 32px;'
                                      'max-width: 32px;'
                                      'max-height: 32px;'
                                      'padding: 0px;}'
                                      'QFrame {border: 1px solid gray; '
                                      'border: 0px solid black;'
                                      'border-radius: 8px;'
                                      'padding: 0px;'
                                      'background-image: url("%s");}' % controlBar)
        navIconSize = QtCore.QSize(32, 32)
        rtnIcon = QtGui.QIcon(':RtnBtn.png')
        self.RtnBtn.setIcon(rtnIcon)
        self.RtnBtn.setIconSize(navIconSize)
        prevIcon = QtGui.QIcon(':PrevBtn.png')
        self.PrevBtn.setIcon(prevIcon)
        self.PrevBtn.setIconSize(navIconSize)
        beginIcon = QtGui.QIcon(':BeginBtn2.png')
        self.BeginBtn.setIcon(beginIcon)
        self.BeginBtn.setIconSize(navIconSize)
        fwdIcon = QtGui.QIcon(':FwdBtn.png')
        self.FwdBtn.setIcon(fwdIcon)
        self.FwdBtn.setIconSize(navIconSize)
        nextIcon = QtGui.QIcon(':NextBtn.png')
        self.NextBtn.setIcon(nextIcon)
        self.NextBtn.setIconSize(navIconSize)
        endIcon = QtGui.QIcon(':EndBtn.png')
        self.EndBtn.setIcon(endIcon)
        self.EndBtn.setIconSize(navIconSize)

    def goPrev(self):
        navBar = self.navIndex
        try:
            if navBar.currentIndex().row() == 0:
                current = navBar.model().rowCount() - 1
            else:
                current = navBar.currentIndex().row() - 1
            navBar.setCurrentIndex(navBar.model().index(current, 0))
            navBar.scrollTo(navBar.currentIndex(), QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
            data = navBar.currentIndex().data(32)
            targetCard = self.dict[data]
            self.loader(targetCard)
        except AttributeError:
            pass

    def goNext(self):
        navBar = self.navIndex
        if navBar.currentIndex().row() == navBar.model().rowCount() - 1:
            current = 0
        else:
            current = navBar.currentIndex().row() + 1
        navBar.setCurrentIndex(navBar.model().index(current, 0))
        navBar.scrollTo(navBar.currentIndex(), QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
        data = navBar.currentIndex().data(32)
        targetCard = self.dict[data]
        self.loader(targetCard)

    def goFirstCard(self):
        navBar = self.navIndex
        data = navBar.model().index(0, 0).data(32)
        targetCard = self.dict[data]
        navBar.setCurrentIndex(navBar.model().index(0, 0))
        navBar.scrollTo(navBar.currentIndex(), QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
        self.loader(targetCard)

    def goLastCard(self):
        navBar = self.navIndex
        lastItem = navBar.model().rowCount() - 1
        data = navBar.model().index(lastItem, 0).data(32)
        targetCard = self.dict[data]
        navBar.setCurrentIndex(navBar.model().index(lastItem, 0))
        navBar.scrollTo(navBar.currentIndex(), QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
        self.loader(targetCard)

    def goBackwards(self):
        """NavBtn prevents this operation changing the stack"""
        if len(self.stack) <= 1:
            return
        if self.index == 0:
            return
        self.index = self.index - 1
        try:
            data = self.stack[self.index]
        except IndexError:
            data = self.index
        if data == dataIndex.currentCard:
            self.index = self.index - 1
            data = self.stack[self.index]
        targetCard = self.dict[data]
        navBtn = True
        self.loader(targetCard, navBtn)

    def goForward(self):
        """NavBtn prevents this operation changing the stack"""
        if len(self.stack) <= 1:
            return
        if self.index == len(self.stack) - 1:
            return
        self.index = self.index + 1
        try:
            data = self.stack[self.index]
        except IndexError:
            return
        targetCard = self.dict[data]
        navBtn = True
        self.loader(targetCard, navBtn)

    @QtCore.pyqtSlot()
    def on_RtnBtn_released(self):
        """
        go back in the queue of recent cards
        """
        self.goBackwards()

    @QtCore.pyqtSlot()
    def on_PrevBtn_released(self):
        """
        go to the previous data card in the list
        (as sorted in the nav bar)
        """
        self.goPrev()

    @QtCore.pyqtSlot()
    def on_BeginBtn_released(self):
        """
        go to the first data card in the list
        (as sorted in the nav bar)
        """
        self.goFirstCard()

    @QtCore.pyqtSlot()
    def on_FwdBtn_released(self):
        """
        go to the next data card in the queue of recent cards
        """
        self.goForward()

    @QtCore.pyqtSlot()
    def on_NextBtn_released(self):
        """
        go to the next data card in the list
        (as sorted in the nav bar)
        """
        self.goNext()

    @QtCore.pyqtSlot()
    def on_EndBtn_released(self):
        """
        go to the last data card in the list
        (as sorted in the nav bar)
        """
        self.goLastCard()


class ExampleNavBar(NavBar, Ui_NavBar):

    def goPrev(self):
        currentID = dataIndex.currentCard
        i = 1
        for child in dataIndex.root.iter('Ex'):
            if child.attrib.get('ExID') != currentID:
                prevID = child.attrib.get('ExID')
                i += 1
            else:
                if i != 1:
                    break
                else:
                    prevID = currentID
        targetCard = dataIndex.exDict[prevID]
        cardLoader.loadExCard(targetCard)

    def goNext(self):
        currentID = dataIndex.currentCard
        getNextCard = 0
        for child in dataIndex.root.iter('Ex'):
            if child.attrib.get('ExID') == currentID:
                getNextCard = 1
            else:
                if getNextCard == 1:
                    nextID = child.attrib.get('ExID')
                    break
        try:
            targetCard = dataIndex.exDict[nextID]
        except UnboundLocalError:
            nextID = dataIndex.root.find('Ex').attrib.get('ExID')
            targetCard = dataIndex.exDict[nextID]
        cardLoader.loadExCard(targetCard)

    def goFirstCard(self):
        egList = list(dataIndex.exDict.keys())
        targetCard = dataIndex.exDict[egList[0]]
        cardLoader.loadExCard(targetCard)

    def goLastCard(self):
        egList = list(dataIndex.exDict.keys())
        targetCard = dataIndex.exDict[egList[len(dataIndex.exDict) - 1]]
        cardLoader.loadExCard(targetCard)
