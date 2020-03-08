from generic_tab_widget import GenericTabWidget
from table_view_factory import TableViewFactory


class GenericTableTabWidget(GenericTabWidget):
    def __init__(self, model, main_window=None):
        super(GenericTableTabWidget, self).__init__(main_window)
        self.__model = model
        self.__table_view = TableViewFactory.get_table_view(model=model, tab_widget=self)
        self._main_layout.addWidget(self.__table_view)

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
                # CBMessageBoxes.popup_message(icon=CBMessageBoxes.WARNING,
                #                              title="Failure while refreshing data to Database",
                #                              text="An error occurred while refreshing database. Please try again later",
                #                              detailed_text=e)
        finally:
            self.setEnabled(True)
            # self.__inprogress_indicator_label.hide()
        if not display_warning:
            return e

    @property
    def table_view(self):
        return self.__table_view
