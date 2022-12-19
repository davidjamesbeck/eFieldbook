from PyQt6 import QtWidgets, QtCore
from ELFB import dataIndex, update, autoparsing


class FocusOutFilter(QtCore.QObject):
    def __init__(self, parent):
        super(FocusOutFilter, self).__init__(parent)
        self.lastContents = None

    def eventFilter(self, sender, event):
        fldbk = dataIndex.fldbk
        if event.type() == QtCore.QEvent.Type.FocusIn:
            try:
                sender.clearSelection()
            except AttributeError:
                pass

        if event.type() == QtCore.QEvent.Type.FocusOut:
            try:
                sender.clearSelection()
            except AttributeError:
                pass
            #                if dataIndex.unsavedEdit == 1:
            fieldname = QtCore.QObject.objectName(sender)
            if len(fieldname) != 0:
                update.setContents(fldbk, fieldname)
        return False


class DialectFilter(QtCore.QObject):
    def __init__(self, parent):
        super(DialectFilter, self).__init__(parent)
        self.lastContents = None

    def eventFilter(self, sender, event):
        fldbk = dataIndex.fldbk
        if event.type() == QtCore.QEvent.Type.FocusIn:
            try:
                sender.clearSelection()
            except AttributeError:
                pass
        if event.type() == QtCore.QEvent.Type.FocusOut:
            try:
                sender.clearSelection()
            except AttributeError:
                pass
            try:
                if self.parent().dialectMenu.hasFocus():
                    return False
            except AttributeError:
                pass
            if dataIndex.unsavedEdit == 1:
                fieldname = QtCore.QObject.objectName(sender)
                wordCount = fldbk.lDialect.toPlainText().split()
                if len(wordCount) == 2:
                    fldbk.dialectBox = QtWidgets.QMessageBox()
                    fldbk.dialectBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    fldbk.dialectBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                    fldbk.dialectBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    fldbk.dialectBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    fldbk.dialectBox.setText('Formatting error.')
                    fldbk.dialectBox.setInformativeText('Format dialect information as'
                                                        '<blockquote><big>Cdn. (US. soda; UK fizzy drink)</big></blockquote>'
                                                        'For expressions known for only one dialect, simply<br /> '
                                                        'give the dialect name without an alternative.<br />')
                    fldbk.dialectBox.exec()
                    return False
                update.setContents(fldbk, fieldname)
        return False


class BorrowFilter(QtCore.QObject):
    def __init__(self, parent):
        super(BorrowFilter, self).__init__(parent)
        self.lastContents = None

    def eventFilter(self, sender, event):
        fldbk = QtCore.QObject.parent(sender).parent()
        while QtCore.QObject.objectName(fldbk) != 'Fieldbook':
            fldbk = QtCore.QObject.parent(fldbk)
        if event.type() == QtCore.QEvent.Type.FocusOut:
            if dataIndex.unsavedEdit == 1:
                fieldname = QtCore.QObject.objectName(sender)
                if len(fldbk.lBrrw.toPlainText().split(None, 1)) == 1:
                    fldbk.brrwBox = QtWidgets.QMessageBox()
                    fldbk.brrwBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    fldbk.brrwBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                    fldbk.brrwBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    fldbk.brrwBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                    fldbk.brrwBox.setText('Formatting error.')
                    fldbk.brrwBox.setInformativeText('The borrowings field must have both<br />'
                                                     'the abbreviated variant name and the <br />'
                                                     'alternative form, as in:'
                                                     '<blockquote><big>Sp. “nena”</big></blockquote>')
                    fldbk.brrwBox.exec()
                    return False
                update.setContents(fldbk, fieldname)
        return False


class ExLineFilter(QtCore.QObject):
    def __init__(self, parent):
        super(ExLineFilter, self).__init__(parent)
        self.lastContents = None
        self.fldbk = dataIndex.fldbk

    def eventFilter(self, sender, event):
        fldbk = self.fldbk

        if event.type() == QtCore.QEvent.Type.FocusOut:
            fieldname = QtCore.QObject.objectName(sender)
            update.setContents(fldbk, fieldname)

        if event.type() == QtCore.QEvent.Type.KeyPress:
            if event.key() == QtCore.Qt.Key.Key_Return:
                if not fldbk.eAutoParsingBtn.isChecked():
                    return True
                autoparsing.doParse()
                return True
        return False
