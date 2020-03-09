from PyQt4.QtGui import QTableView, QAbstractItemView, QHeaderView, QMenu
from PyQt4.QtCore import Qt, QPoint


class GenericTableView(QTableView):
    def __init__(self, model, parent):
        super(GenericTableView, self).__init__(None)
        self._model = model
        self.setModel(self._model)
        self.__parent = parent
        self.__view_name = self._model._table_name
        # Hide id column
        self.setColumnHidden(0, True)
        # select one item a time
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        # select rows per click
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # resize headers labels to fit content
        self.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        self._context_menu = QMenu()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.custom_ctx_menu_handler)

    @property
    def view_name(self):
        return self.__view_name

    def _search_in_table(self, table, column, search_token):
        self.__parent.froward_search_request_to_main_window(table, column, search_token)

    def custom_ctx_menu_handler(self, pos):
        return
