from cb_message_boxes import CBMessageBoxes
from generic_table_view import GenericTableView
from PyQt4.QtGui import QAction, QCursor, QStyle
from functools import partial


class BookTableView(GenericTableView):
    __filterable_csv_headers_list = [1, 2, 3]

    def __init__(self, model, parent):
        super(BookTableView, self).__init__(model, parent, self.__filterable_csv_headers_list)
        self._model = model

    def custom_ctx_menu_handler(self, pos):
        self._context_menu.clear()
        index = self.sender().indexAt(pos)
        column = self._model.column_name(index)

        if column in self._model.hyper_link_attributes_list:
            title = self._model.get_cell_value(index)
            if not title:
                return
            temp_action = QAction("Search '%s' on internet" % title, self)
            # temp_action.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_FileDialogContentsView')))
            temp_action.triggered.connect(partial(self._search_for_files, title))

            self._context_menu.addAction(temp_action)
            self._context_menu.popup(QCursor.pos())

        if column in self._model.fk_attributes_list:
            marking_value = self._model.get_cell_value(index)
            if not marking_value:
                return
            temp_action = QAction("Go to \"{}\" in \"{}\" tab".format(marking_value, column.split("_")[0].capitalize()),
                                  self)
            temp_action.triggered.connect(
                partial(self._search_in_table, column.split("_")[0], index.column(), marking_value))
            self._context_menu.addAction(temp_action)
            self._context_menu.popup(QCursor.pos())

    def _search_for_files(self, title):
        CBMessageBoxes.popup_message(icon=CBMessageBoxes.INFO,
                                     title="An error occurred",
                                     text="Searching for file \n \"{}\"".format(title),
                                     detailed_text="!!!")
