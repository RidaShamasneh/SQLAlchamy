from generic_tab_widget import GenericTabWidget
from table_view_factory import TableViewFactory


class GenericTableTabWidget(GenericTabWidget):
    def __init__(self, model, main_window=None):
        super(GenericTableTabWidget, self).__init__(main_window)
        self.__model = model
        self.__table_view = TableViewFactory.get_table_view(model=model, tab_widget=self)
        self._main_layout.addWidget(self.__table_view)

    @property
    def table_view(self):
        return self.__table_view
