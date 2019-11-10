from PyQt5 import QtGui, QtCore
from ELFB import searchClasses

def dAdvancedSearch(fldbk):
    """
    Search datasets.
    """
    engine = searchClasses.DSetSearchEngine(fldbk)
    engine.doSearch()

def removeHiliting(fldbk):
    text = fldbk.dData.document()
    block = text.begin()
    cursor = QtGui.QTextCursor(block)
    cursor.select(QtGui.QTextCursor.Document)
    format = QtGui.QTextCharFormat()
    format.setBackground(QtCore.Qt.white)
    cursor.setCharFormat(format)
