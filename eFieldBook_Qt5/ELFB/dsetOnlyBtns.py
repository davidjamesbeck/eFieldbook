from PyQt6 import QtGui, QtCore
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
    cursor.select(QtGui.QTextCursor.SelectionType.Document)
    charformat = QtGui.QTextCharFormat()
    charformat.setBackground(QtCore.Qt.GlobalColor.white)
    cursor.setCharFormat(charformat)
