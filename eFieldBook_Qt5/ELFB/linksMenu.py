from PyQt6 import QtWidgets
from ELFB import cardLoader,  dataIndex


class linksMenu(QtWidgets.QMenu):
    def __init__(self, parent):
        super(linksMenu, self).__init__(parent)

    def linkSelected(self):
        sender = self.sender()
        link = sender.data()
        fldbk = dataIndex.fldbk
        if 'M' in link:
            i = fldbk.lSound.Recordings.findData(link, 35)
            fldbk.lSound.Recordings.setCurrentIndex(i)
            fldbk.lSound.playSound()
        else:
            lexRoot = dataIndex.lexDict[link]
            cardLoader.loadLexCard(lexRoot)
