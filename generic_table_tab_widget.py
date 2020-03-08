from cb_message_boxes import CBMessageBoxes
from generic_tab_widget import GenericTabWidget
from PyQt4.QtGui import QToolButton, QIcon, QLabel, QMovie
from PyQt4.QtCore import Qt, QSize

from table_view_factory import TableViewFactory


class GenericTableTabWidget(GenericTabWidget):
    def __init__(self, model, main_window=None):
        super(GenericTableTabWidget, self).__init__(main_window)
        self.__model = model
        # Append Empty Row
        self.__add_row_toolbutton = QToolButton(self)
        self.__add_row_toolbutton.setText("Add Row")
        self.__add_row_toolbutton.setIcon(QIcon(":images/add.png"))
        self.__add_row_toolbutton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self._toolbar.addWidget(self.__add_row_toolbutton)

        # Save Changes to DB button
        self.__save_changes_toolbutton = QToolButton(self)
        self.__save_changes_toolbutton.setText("Save to DB")
        self.__save_changes_toolbutton.setIcon(QIcon(":images/save.ico"))
        self.__save_changes_toolbutton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self._toolbar.addWidget(self.__save_changes_toolbutton)
        self._toolbar.addSeparator()

        self.__table_view = TableViewFactory.get_table_view(model=model, tab_widget=self)
        self._main_layout.addWidget(self.__table_view)
        self.__connect_signals()

    def __connect_signals(self):
        self.__save_changes_toolbutton.clicked.connect(lambda: self.save_data(display_warning=True))
        self.__add_row_toolbutton.clicked.connect(self.__add_row_handler)
        # self.__refresh_data_toolbutton.clicked.connect(self.__refresh_data_handler)


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
