from PyQt5 import QtWidgets, QtCore
from ELFB import dataIndex

from .Ui_AddEgDialog import Ui_AddEg


class AddEgDialog(QtWidgets.QDialog, Ui_AddEg):
    
    def __init__(self, parent):
        super(AddEgDialog,self).__init__(parent)
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.IDREF = ''
    
    def validateID(self):
        if self.IDREF in dataIndex.exDict: 
            return self.IDREF
        else:
            return False
    
    @QtCore.pyqtSlot()
    def on_IDRef_editingFinished(self):
        """
        captures IDRef in line Edit
        """
        self.IDREF = self.IDRef.text()
    
    @QtCore.pyqtSlot(bool)
    def on_checkBox_toggled(self, checked):
        """
        If user checks this box, IDREF is set
        to id number of current example.
        
        @param checked DESCRIPTION
        @type bool
        """
        if checked == 1 and dataIndex.lastEx:
            if not dataIndex.lastEx in dataIndex.exDict:
                #making sure that the current value of lastEx is valid
                dataIndex.lastEx = list(dataIndex.exDict.keys())[0]
            self.IDRef.setText(dataIndex.lastEx)
            self.IDREF = dataIndex.lastEx
        else:
            self.IDRef.setText('')
            self.IDREF = ''
    
    @QtCore.pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Accept, validate, return values.
        """
        self.accept()
    
    @QtCore.pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Close and cancel process.
        """
        self.reject()
