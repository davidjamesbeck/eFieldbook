from PyQt6 import QtGui, QtWidgets, QtCore


class HTMLDelegate(QtWidgets.QStyledItemDelegate):
        
    def paint(self, painter, option, index):
        options = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        style = QtWidgets.QApplication.style() if options.widget is None else options.widget.style()
        doc = QtGui.QTextDocument()
        doc.setHtml(options.text)
        options.text = ""
        style.drawControl(QtWidgets.QStyle.ControlElement.CE_ItemViewItem, options, painter)
        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()
        textRect = style.subElementRect(QtWidgets.QStyle.SubElement.SE_ItemViewItemText, options)
        painter.save()
        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter, ctx)
        painter.restore()

    def sizeHint(self, option, index):
        options = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        doc = QtGui.QTextDocument()
        doc.setHtml(options.text)
        return QtCore.QSize(doc.idealWidth(), doc.size().height())


class SearchDelegate(QtWidgets.QStyledItemDelegate):
        
    def paint(self, painter, option, index):
        options = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options, index)

        style = QtWidgets.QApplication.style() if options.widget is None else options.widget.style()
        doc = QtGui.QTextDocument()
        tOption = self.setOption()
        doc.setDefaultTextOption(tOption)
        tStyle = self.setStyle()
        doc.setDefaultStyleSheet(tStyle)
        doc.setHtml(options.text)
        options.text = ""
        style.drawControl(QtWidgets.QStyle.ControlElement.CE_ItemViewItem, options, painter)
        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()
        textRect = style.subElementRect(QtWidgets.QStyle.SubElement.SE_ItemViewItemText, options)
        painter.save()
        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter, ctx)
        painter.restore()

    def sizeHint(self, option, index):
        options = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        doc = QtGui.QTextDocument()
        tOption = self.setOption()
        doc.setDefaultTextOption(tOption)
        tStyle = self.setStyle()
        doc.setDefaultStyleSheet(tStyle)
        doc.setHtml(options.text)
        return QtCore.QSize(doc.idealWidth(), doc.size().height())
        
    def setOption(self):
        tOption = QtGui.QTextOption()
        tOption.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
        return tOption

    def setStyle(self):
        tStyle = 'p {padding: 0px, 0px, 0px, 0px; margin: 0px, 0px, 0px, 0px; line-height: 16px;}'
        return tStyle
