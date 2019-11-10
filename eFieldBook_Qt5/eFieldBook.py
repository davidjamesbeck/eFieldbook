from PyQt5 import QtWidgets, QtCore, QtGui
from ELFB.ui.fieldbook import MainWindow
from ELFB.qtLibPathFacade.qtLibPathFacade import QtLibPathFacade
from ELFB import dataIndex

if __name__ == "__main__":
    import sys
    
    QtLibPathFacade.addBundledPluginsPath()
    app = QtWidgets.QApplication(sys.argv)
    dataIndex.rootPath = QtCore.QFileInfo(__file__).absolutePath()
    pixmap = QtGui.QPixmap(':Splash(book).png')
    splash = QtWidgets.QSplashScreen(pixmap, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()
    ui = MainWindow()
    QtWidgets.QApplication.setOrganizationName("UNTProject")
    QtWidgets.QApplication.setApplicationName("eFieldbook")
    QtWidgets.QApplication.setOrganizationDomain("http://www.artsrn.ualberta.ca/totonaco/")
    ui.statusBar.hide()
    ui.show()
    splash.finish(ui)
    del splash
    sys.exit(app.exec_())
