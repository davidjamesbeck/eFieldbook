from PyQt6 import QtWidgets, QtGui, QtCore
from ui.mainwindow import MainWindow

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pixmap = QtGui.QPixmap(':Splashbook.png')
    splash = QtWidgets.QSplashScreen(pixmap, QtCore.Qt.WindowType.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()
    ui = MainWindow()
    ui.show()
    splash.finish(ui)
    sys.exit(app.exec())
