from cb_message_boxes import CBMessageBoxes
from generic_table_view import GenericTableView
from PyQt4.QtGui import QAction, QCursor, QStyle
from functools import partial


class AuthorTableView(GenericTableView):
    __filterable_csv_headers_list = [1]

    def __init__(self, model, parent):
        super(AuthorTableView, self).__init__(model, parent, self.__filterable_csv_headers_list)
        self._model = model
