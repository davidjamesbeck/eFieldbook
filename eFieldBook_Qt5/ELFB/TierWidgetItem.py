from PyQt6 import QtWidgets, QtCore
from ELFB import dataIndex


class TierWidgetItem(QtWidgets.QTableWidgetItem):

    def __init__(self, parent):
        super(TierWidgetItem, self).__init__(parent)
        self.installEventFilter(FocusOutFilter)


class FocusOutFilter(QtCore.QObject):
    def __init__(self, parent):
        super(FocusOutFilter, self).__init__(parent)
        self.lastContents = None

    def eventFilter(self, sender, event):
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
            if dataIndex.unsavedEdit == 1:
                self.parent().updateTable()
        return False
