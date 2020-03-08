import sys
from PyQt4.QtGui import QMainWindow

from app_constants import AppConstants
from db_connection import DbConnection
from gui_constans import GUIConstants
from ui_main_widget import UIMainWidget


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # Initialize DB Connection
        self.__db_connection = DbConnection()
        try:
            self.__db_connection.initialize_connection()
        except Exception as e:
            # CBMessageBoxes.popup_message(icon=CBMessageBoxes.CRITICAL,
            #                              title='Database Connection Error',
            #                              text='Failure in connecting to configured database. \n App will exit',
            #                              detailed_text=e.message)
            sys.exit(0)

        self.__setup_ui()

    def __setup_ui(self):
        self.__ui_main_widget = UIMainWidget(main_window=self)
        self.setCentralWidget(self.__ui_main_widget)
        self.resize(GUIConstants.MAIN_WINDOW_FRAME_WIDTH, GUIConstants.MAIN_WINDOW_FRAME_HEIGHT)
        self.__application_title = "{} - {} v{}".format(AppConstants.WESTERN_DIGITAL_STRING,
                                                        AppConstants.APP_NAME,
                                                        "0.0.1")
        self.setWindowTitle(self.__application_title)
