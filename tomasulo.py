from Architecture import *
import Config as cfg
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from main_window import Ui_MainWindow

if __name__ == '__main__':
    tomasulo = Architecture()
    results = tomasulo.start()
    cfg.results = results
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, results)
    MainWindow.show()
    sys.exit(app.exec_())