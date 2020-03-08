import sys
from PyQt4.QtGui import QMainWindow, QAction, QIcon

from app_constants import AppConstants
from db_connection import DbConnection
from generic_table_tab_widget import GenericTableTabWidget
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
        self.__connect_signals()

    def __connect_signals(self):
        # self.__back_up_db_action.triggered.connect(DBBackup.export_database)
        # self.__save_all_tabs.triggered.connect(self.__save_all_tabs_handler)
        self.__refresh_all_tabs.triggered.connect(self.__refresh_all_tabs_handler)
        # self.__xml_report_action.triggered.connect(self.__xml_report_handler)

    def __refresh_all_tabs_handler(self):
        # if CBMessageBoxes.prompt_user(icon=CBMessageBoxes.WARNING,
        #                               title="Refresh Data in all tables",
        #                               text="Unsaved data will be cleared in all tabs, are you sure you want to continue?") \
        #         == CBMessageBoxes.NO:
        #     return
        self.__ui_main_widget.refresh_all_tabs()

    def refresh_all_tabs(self):
        warnings_list = []
        self.__window_enabled(False)
        for tab in self.__get_specific_type_widgets(GenericTableTabWidget):
            warnings_list.append(tab.refresh_data(display_warning=False))

        warnings_list = '\n'.join(filter(None, warnings_list))
        # if warnings_list:
        #     CBMessageBoxes.popup_message(icon=CBMessageBoxes.WARNING,
        #                                  title="Failure while refreshing all tabs",
        #                                  text="An error occurred while refreshing database. Please try again later",
        #                                  detailed_text=warnings_list)
        self.__window_enabled(True)

    def __setup_ui(self):
        self.__ui_main_widget = UIMainWidget(main_window=self)
        self.setCentralWidget(self.__ui_main_widget)
        self.resize(GUIConstants.MAIN_WINDOW_FRAME_WIDTH, GUIConstants.MAIN_WINDOW_FRAME_HEIGHT)
        self.__application_title = "{} - {} v{}".format(AppConstants.WESTERN_DIGITAL_STRING,
                                                        AppConstants.APP_NAME,
                                                        "0.0.1")
        self.setWindowTitle(self.__application_title)
        self.__db_actions_menu = self.menuBar().addMenu('Database')
        self.__save_all_tabs = QAction(QIcon(":images/save_all.ico"), 'Save All Tabs', self)
        self.__db_actions_menu.addAction(self.__save_all_tabs)
        self.__refresh_all_tabs = QAction(QIcon(":images/refresh.png"), 'Refresh All Tabs', self)
        self.__db_actions_menu.addAction(self.__refresh_all_tabs)
