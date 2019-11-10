from PyQt5 import QtWidgets,  QtCore
from ELFB import dataIndex

class TierWidgetItem(QtWidgets.QTableWidgetItem):

    def __init__(self, parent):
        super(TierWidgetItem, self).__init__(parent)
        self.installEventFilter(focusOutFilter)
        
class focusOutFilter(QtCore.QObject):
        def __init__(self, parent):
            super(focusOutFilter, self).__init__(parent)
            self.lastContents = None     
            
        def eventFilter(self, object, event):
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
                if dataIndex.unsavedEdit == 1:
                    self.parent().updateTable()
            return False
