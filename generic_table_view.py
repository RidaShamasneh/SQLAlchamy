from PyQt4.QtGui import QTableView


class GenericTableView(QTableView):
    def __init__(self, model, parent):
        super(GenericTableView, self).__init__(None)
        self._model = model
        self.setModel(self._model)
        self.__view_name = self._model._table_name

    @property
    def view_name(self):
        return self.__view_name
