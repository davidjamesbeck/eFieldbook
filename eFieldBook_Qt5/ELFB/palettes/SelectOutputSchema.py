from PyQt6.QtWidgets import QDialog,  QListWidgetItem
from PyQt6 import QtCore, QtWidgets
from ELFB.palettes.Ui_SelectOutputSchema import Ui_SelectOutput
#from .Ui_SelectOutputSchema import Ui_Outputs



class SelectOutputSchema(QDialog, Ui_SelectOutput):
    """
    Selects output format for text output of database results into a file
    """

    def __init__(self, parent):
        print("Building output schema selector")
        super(SelectOutputSchema, self).__init__(parent)
        self.setupUi(self)
        formatList = ['DictLatexSpan', 'DeneDict']
        self.schema = None
        if len(formatList) != 0:
            for format in formatList:
                item = QtWidgets.QListWidgetItem()
                item.setText(format)
                self.schemaList.addItem(item)

    def exec_(self):
        super(SelectOutputSchema, self).exec_()
        return self.schema
        
    def setSchema(self, schema):
        print("window says",  schema)
        self.schema = schema
        self.accept()

    @QtCore.pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        outputs search results to file.
        """
        self.accept()
    
    @QtCore.pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Cancel.
        """
        self.reject()

    @QtCore.pyqtSlot(QListWidgetItem)
    def on_schemaList_itemDoubleClicked(self, item):
        """
        Slot documentation goes here.

        @param item DESCRIPTION
        @type QListWidgetItem
        """
        self.setSchema(item.text())
        
    @QtCore.pyqtSlot(QListWidgetItem)
    def on_schemaList_itemClicked(self, item):
        """
        Slot documentation goes here.

        @param item DESCRIPTION
        @type QListWidgetItem
        """
        self.schema = item.text()
