from PyQt4.QtGui import QTableView, QAbstractItemView, QHeaderView


class GenericTableView(QTableView):
    def __init__(self, model, parent):
        super(GenericTableView, self).__init__(None)
        self._model = model
        self.setModel(self._model)
        self.__view_name = self._model._table_name
        # Hide id column
        self.setColumnHidden(0, True)
        # select one item a time
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        # select rows per click
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # resize headers labels to fit content
        self.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)

    @property
    def view_name(self):
        return self.__view_name
