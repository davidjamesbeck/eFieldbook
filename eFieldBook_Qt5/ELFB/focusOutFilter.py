from PyQt5 import QtWidgets, QtCore
from ELFB import dataIndex, update, autoparsing

class focusOutFilter(QtCore.QObject):
        def __init__(self, parent):
            super(focusOutFilter, self).__init__(parent)
            self.lastContents = None
            
        def eventFilter(self, object, event):
            fldbk = dataIndex.fldbk
            if event.type() == QtCore.QEvent.FocusIn:
                try:
                    object.clearSelection()
                except AttributeError:
                    pass
                   
            if event.type() == QtCore.QEvent.FocusOut:
                try:
                    object.clearSelection()
                except AttributeError:
                    pass
#                if dataIndex.unsavedEdit == 1:
                fieldname = QtCore.QObject.objectName(object)
                if len(fieldname) != 0:
                    update.setContents(fldbk, fieldname)
            return False

class dialectFilter(QtCore.QObject):
    def __init__(self, parent):
        super(dialectFilter, self).__init__(parent)
        self.lastContents = None
        
    def eventFilter(self,  object,  event):
        fldbk = dataIndex.fldbk
        if event.type() == QtCore.QEvent.FocusIn:
            try:
                object.clearSelection()
            except AttributeError:
                pass
        if event.type() == QtCore.QEvent.FocusOut:
            try:
                object.clearSelection()
            except AttributeError:
                pass
            try:
                if self.parentWidget().dialectMenu.hasFocus():
                    return False
            except AttributeError:
                pass
            if dataIndex.unsavedEdit == 1:
                fieldname = QtCore.QObject.objectName(object)
                wordCount = fldbk.lDialect.toPlainText().split()
                if len(wordCount) == 2:
                    fldbk.dialectBox = QtWidgets.QMessageBox()
                    fldbk.dialectBox.setIcon(QtWidgets.QMessageBox.Warning)
                    fldbk.dialectBox.setStandardButtons(QtWidgets.QMessageBox.Cancel)
                    fldbk.dialectBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    fldbk.dialectBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                    fldbk.dialectBox.setText('Formatting error.')
                    fldbk.dialectBox.setInformativeText('Format dialect information as'
                                                       '<blockquote><big>Cdn. (US. soda; UK fizzy drink)</big></blockquote>'
                                                       'For expressions known for only one dialect, simply<br /> '
                                                       'give the dialect name without an alternative.<br />')
                    fldbk.dialectBox.exec_()
                    return False
                update.setContents(fldbk, fieldname)
        return False

class borrowFilter(QtCore.QObject):
    def __init__(self, parent):
        super(borrowFilter, self).__init__(parent)
        self.lastContents = None
        
    def eventFilter(self,  object,  event):
        fldbk = QtCore.QObject.parent(object).parentWidget()
        while QtCore.QObject.objectName(fldbk) != 'Fieldbook':
            fldbk = QtCore.QObject.parent(fldbk)
        if event.type() == QtCore.QEvent.FocusOut:
            if dataIndex.unsavedEdit ==1:
                fieldname = QtCore.QObject.objectName(object)
                if len(fldbk.lBrrw.toPlainText().split(None,1)) == 1:
                    fldbk.brrwBox = QtWidgets.QMessageBox()
                    fldbk.brrwBox.setIcon(QtWidgets.QMessageBox.Warning)
                    fldbk.brrwBox.setStandardButtons(QtWidgets.QMessageBox.Cancel)
                    fldbk.brrwBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    fldbk.brrwBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                    fldbk.brrwBox.setText('Formatting error.')
                    fldbk.brrwBox.setInformativeText('The borrowings field must have both<br />'
                                                    'the abbreviated variant name and the <br />'
                                                    'alternative form, as in:'
                                                    '<blockquote><big>Sp. “nena”</big></blockquote>')
                    fldbk.brrwBox.exec_()
                    return False
                update.setContents(fldbk, fieldname)
        return False

class exLineFilter(QtCore.QObject):
    def __init__(self, parent):
        super(exLineFilter, self).__init__(parent)
        self.lastContents = None
        self.fldbk = dataIndex.fldbk
        
    def eventFilter(self, object, event):
        fldbk = self.fldbk
               
        if event.type() == QtCore.QEvent.FocusOut:
#            if dataIndex.unsavedEdit == 1:
            fieldname = QtCore.QObject.objectName(object)
            update.setContents(fldbk, fieldname)
        
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return:
                if not fldbk.eAutoParsingBtn.isChecked():
                    return True
                autoparsing.doParse()
                return True
        return False
