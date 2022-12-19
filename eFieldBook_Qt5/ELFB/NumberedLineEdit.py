from PyQt6 import QtGui, QtWidgets, QtCore
from ELFB import dataIndex
 

class LineTextWidget(QtWidgets.QFrame):
 
    class NumberBar(QtWidgets.QWidget):
        def __init__(self, *args):
            QtWidgets.QWidget.__init__(self, *args)
            self.edit = None
            # This is used to update the width of the control.
            # It is the highest line that is currently visibile.
            self.highest_line = 0
 
        def setTextEdit(self, edit):
            self.edit = edit
 
        def update(self, *args):
            """
            Updates the number bar to display the current set of numbers.
            Also, adjusts the width of the number bar if necessary.
            """
            width = self.fontMetrics().width(str(self.highest_line)) + 14
            if self.width() != width:
                self.setFixedWidth(width)
            QtWidgets.QWidget.update(self, *args)
 
        def paintEvent(self, event):
            contents_y = self.edit.verticalScrollBar().value()
            page_bottom = contents_y + self.edit.viewport().height()
            font_metrics = self.fontMetrics() 
            painter = QtGui.QPainter(self) 
            line_count = 0
            # Iterate over all text blocks in the document.
            block = self.edit.document().begin()
            while block.isValid():
                line_count += 1
                # The top left position of the block in the document
                position = self.edit.document().documentLayout().blockBoundingRect(block).topLeft() 
                # Check if the position of the block is outside of the visible area.
                if position.y() > page_bottom:
                    break 
                # Draw the line number right justified at the y position of the line. 
                # 3 is a magic padding number. drawText(x, y, text).
                painter.setPen(QtGui.QColor('#5882FA'))
                painter.drawText(self.width() - font_metrics.width(str(line_count)) - 5, round(position.y()+4) - contents_y + font_metrics.ascent(), str(line_count)) 
                block = block.next() 
            self.highest_line = line_count
            painter.end() 
            QtWidgets.QWidget.paintEvent(self, event)
 
    def __init__(self, *args):
        QtWidgets.QFrame.__init__(self, *args)
        self.setFrameStyle(QtWidgets.QFrame.Shape.StyledPanel | QtWidgets.QFrame.Shadow.Sunken)

    def sliderMoved(self):
        """
        makes sure the number box scrolls in synch with the editing field
        (self.edit) and adjusts the width when necessary
        """
        vPosition = self.edit.verticalScrollBar().value()
        self.number_bar.scroll(0, vPosition)
        width = self.number_bar.fontMetrics().width(str(self.number_bar.highest_line)) + 14
        if self.number_bar.width() != width:
            self.number_bar.setFixedWidth(width)
 
    def eventFilter(self, sender, event):
        # Update the line numbers for all KeyPress events.
        if sender in (self.edit, self.edit.viewport()):
            if event.type() == QtCore.QEvent.Type.KeyPress:
                self.number_bar.update()
            return False
        try:
            return QtWidgets.QFrame.eventFilter(sender, event)
        except TypeError:
            return False
        return False
 
    def getTextEdit(self):
        return self.edit
        

class DataNumberWidget(LineTextWidget):
    def __init__(self, parent, *args):
        super(DataNumberWidget, self).__init__(parent)
        self.edit = dataIndex.fldbk.dData
        self.number_bar = self.NumberBar()
        self.number_bar.setTextEdit(self.edit)
        self.edit.verticalScrollBar().valueChanged.connect(self.sliderMoved)
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.setSpacing(0)
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self.edit) 
        self.edit.installEventFilter(self)
        self.edit.viewport().installEventFilter(self)


class TextNumberWidget(LineTextWidget):
    def __init__(self, parent, portal):
        super(TextNumberWidget, self).__init__(parent)
        self.edit = portal
        self.number_bar = self.NumberBar()
        self.number_bar.setTextEdit(self.edit)
        self.edit.verticalScrollBar().valueChanged.connect(self.sliderMoved)
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.setSpacing(0)
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
