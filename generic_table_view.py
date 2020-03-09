from PyQt4.QtGui import QTableView, QAbstractItemView, QHeaderView, QMenu
from PyQt4.QtCore import Qt, QPoint
from functools import partial

from gui.filter.csv_filter import CSVFilter


class GenericTableView(QTableView):
    def __init__(self, model, parent, csv_filterable_headers_list):
        super(GenericTableView, self).__init__(None)
        self.__filterable_csv_headers_list = csv_filterable_headers_list
        self.__csv_filter = CSVFilter()
        self._model = model
        self._model.filterable_csv_headers_list = self.__filterable_csv_headers_list
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
        # Filter meny preparation
        self.__csv_filter.filter_unique_items = self._model.unique_vals_dict
        self.__csv_filter.construct_filter_menus()
        # connect ok | cancel signals per qmenu
        for csv_column_index, filter_qmenu in self.__csv_filter.filter_menus.iteritems():
            filter_qmenu.ok_cancel_dialog_button_rejected.connect(
                partial(self.__cancel_filters_selection_handler, csv_column_index))
            filter_qmenu.ok_cancel_dialog_button_accepted.connect(
                partial(self.__start_data_filter_handler, csv_column_index))
            filter_qmenu.ok_cancel_dialog_button_accepted.connect(
                partial(self.__change_header_icon_handler, csv_column_index))

    def __change_header_icon_handler(self, column_index):
        if self.__csv_filter.filter_menus[column_index].get_select_all_state():
            self._model.filter_is_enabled = True, ":/images/filter_grey.png", column_index
        else:
            self._model.filter_is_enabled = True, ":/images/filter.ico", column_index

    def __start_data_filter_handler(self, column_index):
        self.__csv_filter.filter_menus[column_index].hide()
        # Case 1: check if current requested filter is the same as the previous filter, so no need to run filtration
        if self.__csv_filter.is_state_changed():
            return
        # Case 2: at least one filter is disabled
        elif self.__csv_filter.is_at_least_one_filter_menu_items_all_unchecked():
            self.__csv_filter.update_cached_states()
            self._model.start_filter({})
        # case 3: all filters are enables, i.e: filter_data == array_Data
        elif self.__csv_filter.is_all_filter_menus_checked():
            self._model.init_filter_data_list()
            self.__csv_filter.update_cached_states()
            self._model.reset()
        else:
            filter_items_list = self.__csv_filter.get_enabled_checkboxes_dict()
            self.__csv_filter.update_cached_states()
            self._model.start_filter(filter_items_list)

    def __cancel_filters_selection_handler(self, column_index):
        # close menu
        self.__csv_filter.filter_menus[column_index].close()
        # reset menu from cached_values to reverse user changes on menu_checkboxes
        self.__csv_filter.reset_filter_menu_at_index_from_cached_state(column_index)

    @property
    def view_name(self):
        return self.__view_name

    def _search_in_table(self, table, column, search_token):
        self.__parent.froward_search_request_to_main_window(table, column, search_token)

    def custom_ctx_menu_handler(self, pos):
        return

    def __column_header_sectionclicked_handler(self, column_index):
        # skip column that are not subjective for filtration
        if not column_index in self.__filterable_csv_headers_list:
            return
        filter_qmenu = self.__csv_filter.filter_menus[column_index]
        # get position of header to display the menu
        header_xy_pos = self.mapToGlobal(self.horizontalHeader().pos())
        x_pos = header_xy_pos.x() + self.horizontalHeader().sectionViewportPosition(column_index)
        y_pos = header_xy_pos.y() + self.horizontalHeader().height()
        # Show menu at x,y pos
        filter_qmenu.exec_(QPoint(x_pos, y_pos))

    def enable_horizontal_headers_signal(self):
        if self.__filterable_csv_headers_list:
            # Enable section signal: single left click header to add filters
            self.horizontalHeader().sectionClicked.connect(self.__column_header_sectionclicked_handler)
            # notify model that filters is enabled to display columns icons
            self._model.init_filter_data_list()
            self._model.filter_is_enabled = True, ":/images/filter_grey.png", None

    def disable_horizontal_headers_signals(self):
        if self.__filterable_csv_headers_list:
            # notify model that filter is disabled to remove columns icons
            self._model.filter_is_enabled = False, None, None
            # disconnect header section signal
            self.horizontalHeader().sectionClicked.disconnect(self.__column_header_sectionclicked_handler)
            # reset filter menu items to initial_state
            self.__csv_filter.reset_filter_menus(is_checked=True)
