from PyQt5 import QtWidgets, QtCore
from ELFB import dataIndex
from .Ui_SearchResultsToFile import Ui_OutPutFormatDialog


class SearchResultsToFile(QtWidgets.QDialog, Ui_OutPutFormatDialog):
    """
    Selects output format for saving search results into a file
    """
    def __init__(self, parent):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(SearchResultsToFile, self).__init__(parent)
        self.setupUi(self)
        self.formatBox.setDisabled(1)
        
    def compileResults(self):
        hitsModel = dataIndex.fldbk.cSearchResults.model()
        if self.HtmlBox.isChecked():
            output = '<HTML><HEAD><meta charset="utf-8"></HEAD><BODY>'
            for i in range(0, hitsModel.rowCount()):
                output += '<P>' + hitsModel.item(i).text() + '</P>'   
            output += '</BODY></HTML>'
        elif self.TxtBox.isChecked():
            output = ''
            for i in range(0, hitsModel.rowCount()):
                string = hitsModel.item(i).text().replace('</p><p>', '\n')
                output += string + '\n' +'\n'
            output = output.replace('<b>', '')
            output = output.replace('</b>', '')
            output = output.replace('<i>', '')
            output = output.replace('</i>', '')
            output = output.replace('</p>', '')
            output = output.replace('<p>', '')
        else:
            output = False
        return output
    
    @QtCore.pyqtSlot(bool)
    def on_HtmlBox_toggled(self, checked):
        """
        sets the output to HTML
        
        @param checked DESCRIPTION
        @type bool
        """
        if checked == 1:
            self.formatBox.setDisabled(1)
            self.TxtBox.setChecked(0)
            self.customBox.setChecked(0)
    
    @QtCore.pyqtSlot(bool)
    def on_TxtBox_toggled(self, checked):
        """
        sets the output to .txt
        
        @param checked DESCRIPTION
        @type bool
        """
        if checked == 1:
            self.formatBox.setDisabled(1)
            self.HtmlBox.setChecked(0)
            self.customBox.setChecked(0)
    
    @QtCore.pyqtSlot(str)
    def on_comboBox_activated(self, p0):
        """
        select custom file formats.
        
        @param p0 DESCRIPTION
        @type str
        """
        # TODO: custom search outputs not implemented yet
        print('custom output')
    
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
    
    @QtCore.pyqtSlot(bool)
    def on_customBox_toggled(self, checked):
        """
        Enable/disable custom format box.
        
        @param checked DESCRIPTION
        @type bool
        """
        if checked == 1:
            self.formatBox.setEnabled(1)
            self.HtmlBox.setChecked(0)
            self.TxtBox.setChecked(0)
        else:
            self.formatBox.setDisabled(1)
