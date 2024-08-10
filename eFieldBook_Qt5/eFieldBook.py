from PyQt6 import QtWidgets, QtCore, QtGui
from ELFB.ui.fieldbook import MainWindow
from ELFB.qtLibPathFacade.qtLibPathFacade import QtLibPathFacade
from ELFB import dataIndex

if __name__ == "__main__":
    import sys
    
#    if getattr(sys, 'frozen', False):
#        import pyi_splash
    QtLibPathFacade.addBundledPluginsPath()
    app = QtWidgets.QApplication(sys.argv)
    dataIndex.rootPath = QtCore.QFileInfo(__file__).absolutePath()
    print('image lives in: %s' % dataIndex.rootPath)
    piximage = dataIndex.rootPath + '/Splashbook.png' 
    print('image file is: %s' % piximage)
    pixmap = QtGui.QPixmap(piximage)
    print('image is %d pixels wide.' % pixmap.width())
    splash = QtWidgets.QSplashScreen(pixmap, QtCore.Qt.WindowType.WindowStaysOnTopHint)
    print('QPixmap = %s' % splash.pixmap())
    print('QPixmap is null: %s' % pixmap.isNull())
    splash.show()
    print('splash is visible: %s' % splash.isVisible())
    print('splash WindowState is: %s' % splash.windowState())
    app.processEvents()
    ui = MainWindow()
#    if getattr(sys, 'frozen', False):
#        pyi_splash.close()
    QtWidgets.QApplication.setOrganizationName("UNTProject")
    QtWidgets.QApplication.setApplicationName("eFieldbook")
    QtWidgets.QApplication.setOrganizationDomain("http://www.artsrn.ualberta.ca/totonaco/")
    ui.statusBar.hide()
    ui.show()
    splash.finish(ui)
    del splash
    sys.exit(app.exec())
