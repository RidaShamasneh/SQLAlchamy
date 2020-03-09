from collections import OrderedDict

from PyQt4.QtGui import QWidget, QStatusBar, QLabel, QVBoxLayout, QTabWidget, QMovie, QTabBar
from PyQt4.QtCore import QSize

from cb_message_boxes import CBMessageBoxes
from generic_table_tab_widget import GenericTableTabWidget
from gui_constans import GUIConstants
from table_model_factory import TableModelFactory


class UIMainWidget(QWidget):
    def __init__(self, main_window):
        QWidget.__init__(self)
        self.__main_window = main_window
        self.__setup_ui()

    def __setup_ui(self):
        # Initialize MainWindow Geometry
        self.resize(GUIConstants.MAIN_WINDOW_FRAME_WIDTH, GUIConstants.MAIN_WINDOW_FRAME_HEIGHT)
        self.__window_layout = QVBoxLayout()
        self.setLayout(self.__window_layout)
        self.__status_bar = QStatusBar()
        self.__status_bar.setSizeGripEnabled(False)
        self.__status_bar_label = QLabel("Welcome")
        self.__status_bar.addPermanentWidget(self.__status_bar_label)
        self.__status_bar.setContentsMargins(0, 0, 10, 0)
        # loading gif spinner gif
        self.__loading_indicator_label = QLabel()
        self.__search_indicator_movie = QMovie(":/images/loading_spinner.gif")
        self.__search_indicator_movie.setScaledSize(QSize(24, 24))
        self.__loading_indicator_label.setMovie(self.__search_indicator_movie)
        self.__loading_indicator_label.hide()
        self.__status_bar.addPermanentWidget(self.__loading_indicator_label)
        self.__search_indicator_movie.start()

        # Tab Widget
        # Add tab widget to view
        self.__tab_widget = QTabWidget()
        self.__tab_widget.setMovable(True)
        self.__tab_widget.setTabsClosable(True)
        self.__window_layout.addWidget(self.__tab_widget)

        # Enable File D&D
        self.setAcceptDrops(True)

        # init table models
        TableModelFactory.init_models()
        # Add widgets statically
        self.__setup_tabs()

    def __setup_tabs(self):
        # TODO: report error occurred in fetching tables
        for table_name, model in TableModelFactory.switcher.items():
            self.__add_new_table_tab(table_name)
        self.__tab_widget.setCurrentIndex(0)

    def __add_new_table_tab(self, table_name):
        model = TableModelFactory.switcher[table_name]
        widget = GenericTableTabWidget(model=model, main_window=self)
        # append tab
        self.__tab_widget.addTab(widget, widget.table_view.view_name.title().replace("_", " "))
        self.__tab_widget.setTabToolTip(self.__tab_widget.count() - 1, "'{}' {}".format(widget.table_view.view_name,
                                                                                        "Table"))
        self.__tab_widget.setFocus()
        self.__tab_widget.setCurrentWidget(widget)
        # Disable close button for tab
        self.__tab_widget.tabBar().setTabButton(self.__tab_widget.count() - 1, QTabBar.RightSide, None)

    def __window_enabled(self, is_enabled):
        self.__tab_widget.setEnabled(is_enabled)
        self.__main_window.menuBar().setEnabled(is_enabled)
        self.__loading_indicator_label.setHidden(is_enabled)

    def save_all_tabs(self):
        warnings_list = []
        '''
        We need to insert data into DB tables by order; in order to maintain the FK relationships between tables
        '''
        tabs_to_save = OrderedDict({})
        tabs_to_save['book'] = None
        tabs_to_save['author'] = None
        for tab in self.__get_specific_type_widgets(GenericTableTabWidget):
            tabs_to_save[tab.table_view.view_name] = tab
        self.__window_enabled(False)
        for tab_name, tab in tabs_to_save.items():
            if tab is not None:
                warnings_list.append(tab.save_data(display_warning=False))
        warnings_list = '\n'.join(filter(None, warnings_list))
        if warnings_list:
            CBMessageBoxes.popup_message(icon=CBMessageBoxes.WARNING,
                                         title="Failure while saving all tabs",
                                         text="An error occurred while saving all tables.",
                                         detailed_text=warnings_list)
        self.__window_enabled(True)

    def __get_specific_type_widgets(self, widget_type):
        tabs_count = self.__tab_widget.count()
        for tab_index in range(tabs_count):
            widget = self.__tab_widget.widget(tab_index)
            if isinstance(widget, widget_type):
                yield widget

    def refresh_all_tabs(self):
        warnings_list = []
        self.__window_enabled(False)
        for tab in self.__get_specific_type_widgets(GenericTableTabWidget):
            warnings_list.append(tab.refresh_data(display_warning=False))

        warnings_list = '\n'.join(filter(None, warnings_list))
        if warnings_list:
            CBMessageBoxes.popup_message(icon=CBMessageBoxes.WARNING,
                                         title="Failure while refreshing all tabs",
                                         text="An error occurred while refreshing database. Please try again later",
                                         detailed_text=warnings_list)
        self.__window_enabled(True)

    def forward_search_request(self, table, column_search_index, search_token):
        self.__window_enabled(False)
        for index, widget in enumerate(self.__get_specific_type_widgets(GenericTableTabWidget)):
            if widget.table_view.view_name == table:
                val = widget.search_token(column_search_index, search_token)
                if val is not None:
                    self.__tab_widget.setCurrentIndex(index)
                else:
                    CBMessageBoxes.popup_message(icon=CBMessageBoxes.WARNING,
                                                 title="Could not locate item in opened tabs",
                                                 text="Value is not found in corresponding tab")
                break  # No need to continue; one instance per table exists
        self.__window_enabled(True)
