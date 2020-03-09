from cb_message_boxes import CBMessageBoxes
from generic_tab_widget import GenericTabWidget
from PyQt4.QtGui import QToolButton, QIcon, QLabel, QMovie
from PyQt4.QtCore import Qt, QSize

from table_view_factory import TableViewFactory


class GenericTableTabWidget(GenericTabWidget):
    __filterable_tables = ["book"]

    def __init__(self, model, main_window=None):
        super(GenericTableTabWidget, self).__init__(main_window)
        self.__model = model
        # Append Empty Row
        self.__add_row_toolbutton = QToolButton(self)
        self.__add_row_toolbutton.setText("Add Row")
        self.__add_row_toolbutton.setIcon(QIcon(":images/add.png"))
        self.__add_row_toolbutton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self._toolbar.addWidget(self.__add_row_toolbutton)
        self._toolbar.addSeparator()

        # Save Changes to DB button
        self.__save_changes_toolbutton = QToolButton(self)
        self.__save_changes_toolbutton.setText("Save to DB")
        self.__save_changes_toolbutton.setIcon(QIcon(":images/save.ico"))
        self.__save_changes_toolbutton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self._toolbar.addWidget(self.__save_changes_toolbutton)
        self._toolbar.addSeparator()

        # Refresh Data
        self.__refresh_data_toolbutton = QToolButton(self)
        self.__refresh_data_toolbutton.setText("Refresh Data")
        self.__refresh_data_toolbutton.setIcon(QIcon(":images/refresh.png"))
        self.__refresh_data_toolbutton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self._toolbar.addWidget(self.__refresh_data_toolbutton)

        # Filter Button; for tables that supports filtration
        if model._table_name in self.__filterable_tables:
            self.__filter_toolbutton = QToolButton(self)
            self.__filter_toolbutton.setText("Apply Filter")
            self.__filter_toolbutton.setIcon(QIcon(":/images/filter.ico"))
            self.__filter_toolbutton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            self.__filter_toolbutton.setCheckable(True)
            self._toolbar.addWidget(self.__filter_toolbutton)
            self.__filter_toolbutton.clicked.connect(self.__filter_toolbutton_toggled_handler)

        self.__table_view = TableViewFactory.get_table_view(model=model, tab_widget=self)
        self._main_layout.addWidget(self.__table_view)
        self.__connect_signals()

    def __filter_toolbutton_toggled_handler(self, checked):
        if not checked:
            self.__filter_toolbutton.setText("Apply Filter")
            self.__filter_toolbutton.setIcon(QIcon(":/images/filter.ico"))
            self.__table_view.disable_horizontal_headers_signals()
            # enable save, refresh, add row features
            self.__save_changes_toolbutton.setEnabled(True)
            self.__refresh_data_toolbutton.setEnabled(True)
            self.__add_row_toolbutton.setEnabled(True)
            return
        self.__filter_toolbutton.setText("Clear Filter")
        self.__filter_toolbutton.setIcon(QIcon(":/images/clear_filter.png"))
        self.__table_view.enable_horizontal_headers_signal()
        # disable save, refresh, add row features
        self.__save_changes_toolbutton.setEnabled(False)
        self.__refresh_data_toolbutton.setEnabled(False)
        self.__add_row_toolbutton.setEnabled(False)

    def __connect_signals(self):
        self.__save_changes_toolbutton.clicked.connect(lambda: self.save_data(display_warning=True))
        self.__add_row_toolbutton.clicked.connect(self.__add_row_handler)
        self.__refresh_data_toolbutton.clicked.connect(self.__refresh_data_handler)

    def __refresh_data_handler(self):
        if CBMessageBoxes.prompt_user(icon=CBMessageBoxes.WARNING,
                                      title="Refresh Data Table",
                                      text="Unsaved data will be cleared, are you sure you want to continue?") \
                == CBMessageBoxes.NO:
            return
        self.refresh_data()

    def refresh_data(self, display_warning=True):
        # if self.__model.table_name in self.__filterable_tables:
        #     # disable the feature in case filter is enabled
        #     if self.__filter_toolbutton.isChecked():
        #         return
        e = None
        self.setEnabled(False)
        # self.__inprogress_indicator_label.show()
        try:
            self.table_view.model().refresh_data()
        except Exception as e:
            e = e.message
            if display_warning:
                self.setEnabled(True)
                CBMessageBoxes.popup_message(icon=CBMessageBoxes.WARNING,
                                             title="Failure while refreshing data to Database",
                                             text="An error occurred while refreshing database. Please try again later",
                                             detailed_text=e)
        finally:
            self.setEnabled(True)
            # self.__inprogress_indicator_label.hide()
        if not display_warning:
            return e

    def save_data(self, display_warning=True):
        # if self.__model.table_name in self.__filterable_tables:
        #     # disable the feature in case filter is enabled
        #     if self.__filter_toolbutton.isChecked():
        #         return
        self.setEnabled(False)
        # self.__inprogress_indicator_label.show()
        error = self.table_view.model().save_data()
        self.setEnabled(True)
        # self.__inprogress_indicator_label.hide()

        if display_warning and error:
            CBMessageBoxes.popup_message(icon=CBMessageBoxes.WARNING,
                                         title="Failure while inserting data into Database",
                                         text="An error occurred while inserting into database.",
                                         detailed_text=error)
        if not display_warning:
            return error

    def __add_row_handler(self):
        self.table_view.model().add_empty_row()

    @property
    def table_view(self):
        return self.__table_view

    def search_token(self, search_col_index, search_token):
        result_index = self.table_view.model().search_row(search_col_index, search_token)
        if result_index is not None:
            self.table_view.selectRow(result_index.row())
        return result_index

    def froward_search_request_to_main_window(self, table, column_search_index, search_token):
        self._main_window.forward_search_request(table, column_search_index, search_token)
