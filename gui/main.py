import sys

from app_constants import AppConstants
from gui_constans import GUIConstants

'''
Please do not remove this namespace because it is needed in other places
'''
import gui.resources.gui_resources
import time

from main_window import MainWindow

from PyQt4.QtGui import QApplication, QSplashScreen, QPixmap
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt


def main(args):
    app = QApplication(sys.argv)
    main_window = MainWindow()
    app_icon = QtGui.QIcon()
    app_icon.addFile(GUIConstants.APP_ICON, QtCore.QSize(48, 48))
    app.setWindowIcon(app_icon)

    # splash screen
    splash = QSplashScreen(QPixmap(":/images/logo_splash.png"), Qt.WindowStaysOnTopHint)
    splash.setStyleSheet("font-size: 20px")
    splash.showMessage("{} v{}".format(AppConstants.APP_NAME, "0.0.1"),
                       Qt.AlignBottom | Qt.AlignCenter, Qt.black)
    splash.show()
    time.sleep(GUIConstants.SPLASH_SCREEN_TIMEOUT)
    splash.finish(main_window)
    main_window.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv[1:])
