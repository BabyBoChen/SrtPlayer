import srt_player_v4
import sys
import widgets
from PyQt5 import QtCore, QtWidgets

app = QtWidgets.QApplication(sys.argv)
MainWindow = widgets.MainWindow()
MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
MainWindow.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
ui = srt_player_v4.Ui_MainWindow(MainWindow,app)
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
