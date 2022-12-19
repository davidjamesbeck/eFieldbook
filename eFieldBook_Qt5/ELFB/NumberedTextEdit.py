from PyQt6 import QtGui, QtWidgets, QtCore
from ELFB import dataIndex


class LineTextWidget(QtWidgets.QFrame):
    class NumberBar(QtWidgets.QWidget):

        def __init__(self, *args):
            QtWidgets.QWidget.__init__(self, *args)
            self.edit = None
            # This is used to update the width of the control.
            # It is the highest line that is currently visible.
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
                    painter.drawText(self.width() - font_metrics.width(str(line_count)) - 5,
                                     round(position.y() + 3) - contents_y + font_metrics.ascent(), str(line_count))
                    line_count += 1
                    if line_count > self.edit.document().blockCount():
                        break
                block = block.next()

            self.highest_line = line_count
            painter.end()
            QtWidgets.QWidget.paintEvent(self, event)

    def __init__(self, *args):
        QtWidgets.QFrame.__init__(self, *args)

        self.setFrameStyle(QtWidgets.QFrame.Shape.StyledPanel | QtWidgets.QFrame.Shadow.Sunken)

        self.edit = dataIndex.fldbk.portal
        self.edit.setFrameStyle(QtWidgets.QFrame.Shape.NoFrame)
        self.edit.setAcceptRichText(False)

        self.number_bar = self.NumberBar()
        self.number_bar.setTextEdit(self.edit)

        hbox = QtWidgets.QHBoxLayout(self)
        hbox.setSpacing(0)
        #        hbox.setMargin(0)
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

    def eventFilter(self, sender, event):
        # Update the line numbers for scroll events on the text edit and the viewport.
        # and where editing affects the number of lines in the text edit
        try:
            if sender in (self.edit, self.edit.viewport()):
                fldbk = dataIndex.fldbk
                if event.type() == 6:
                    if event.key() == QtCore.Qt.Key.Key_Backspace and fldbk.portal.textCursor().atBlockStart():
                        self.number_bar.update()
                    elif event.key() == QtCore.Qt.Key.Key_Return:
                        self.number_bar.update()
                    return False
                elif event.type() == 31:
                    self.number_bar.update()
                    return False
            return QtWidgets.QFrame.eventFilter(sender, event)
        except AttributeError:
            return False
        except TypeError:
            return False

    def getTextEdit(self):
        return self.edit
