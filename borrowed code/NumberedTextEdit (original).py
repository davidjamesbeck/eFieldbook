from PyQt4 import QtGui
from viewClasses import dataIndex
 
class LineTextWidget(QtGui.QFrame):
 
    class NumberBar(QtGui.QWidget):
 
        def __init__(self, *args):
            QtGui.QWidget.__init__(self, *args)
            self.edit = None
            # This is used to update the width of the control.
            # It is the highest line that is currently visibile.
            self.highest_line = 0
 
        def setTextEdit(self, edit):
            self.edit = edit
 
        def update(self, *args):
            '''
            Updates the number bar to display the current set of numbers.
            Also, adjusts the width of the number bar if necessary.
            '''
            width = self.fontMetrics().width(str(self.highest_line)) + 14
            if self.width() != width:
                self.setFixedWidth(width)
            QtGui.QWidget.update(self, *args)
 
        def paintEvent(self, event):
            contents_y = self.edit.verticalScrollBar().value()
            page_bottom = contents_y + self.edit.viewport().height()
            font_metrics = self.fontMetrics()
 
            painter = QtGui.QPainter(self)
 
            line_count = 1
            # Iterate over all text blocks in the document.
            block = self.edit.document().begin()
            while block.isValid():
 
                # The top left position of the block in the document
                position = self.edit.document().documentLayout().blockBoundingRect(block).topLeft()
 
                # Check if the position of the block is outside of the visible area.
                if position.y() > page_bottom:
                    break
 
                # Draw the line number right justified at the y position of the line. 
                # 3 is a magic padding number. drawText(x, y, text).
                painter.setPen(QtGui.QColor('#5882FA'))
                if len(block.previous().text()) <= 1:
                    painter.drawText(self.width() - font_metrics.width(str(line_count)) - 5, round(position.y()+3) - contents_y + font_metrics.ascent(), str(line_count))
                    line_count +=1
                    if line_count > self.edit.document().blockCount():
                        break
                block = block.next()
               
            self.highest_line = line_count
            painter.end()
 
            QtGui.QWidget.paintEvent(self, event)
 
 
    def __init__(self, *args):
        QtGui.QFrame.__init__(self, *args)
 
        self.setFrameStyle(QtGui.QFrame.Shape.StyledPanel | QtGui.QFrame.Shadow.Sunken)
 
        self.edit = dataIndex.fldbk.portal
        self.edit.setFrameStyle(QtGui.QFrame.NoFrame)
        self.edit.setAcceptRichText(False)
 
        self.number_bar = self.NumberBar()
        self.number_bar.setTextEdit(self.edit)
 
        hbox = QtGui.QHBoxLayout(self)
        hbox.setSpacing(0)
        hbox.setMargin(0)
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self.edit)
 
        self.edit.installEventFilter(self)
        self.edit.viewport().installEventFilter(self)
        
        self.lineErrors = []
        self.lineErrorIndex = None
        self.wordErrors = []
        self.wordErrorIndex = None
        self.morphErrors = []
        self.morphErrorIndex = None
        
        self.editorBlockCount = 0
 
    def eventFilter(self, object, event):
        # Update the line numbers for all events on the text edit and the viewport.
        if object in (self.edit, self.edit.viewport()):
            self.number_bar.update()
            return False
        return QtGui.QFrame.eventFilter(object, event)
 
    def getTextEdit(self):
        return self.edit
