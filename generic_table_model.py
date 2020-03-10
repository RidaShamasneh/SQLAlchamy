from PyQt4.QtCore import QAbstractTableModel, QVariant, Qt
from PyQt4.QtGui import QBrush, QColor, QFont, QSortFilterProxyModel, QIcon

from cb_message_boxes import CBMessageBoxes
from cb_table import CBTable


class GenericTableModel(QAbstractTableModel):
    def __init__(self, table_name):
        super(GenericTableModel, self).__init__()
        self._table_name = table_name
        self.__filterable_csv_headers_list = []
        self.__filterable_csv_headers_icons_dict = {}
        self.__unique_vals_dict = {}
        self.__filter_is_enabled = (False, None, None)
        self._crystal_ball_table = CBTable(table_name=self._table_name)
        self._headers = map(lambda x: x.title().replace("_", " "), self._crystal_ball_table.headers)
        self.__set_array_data()
        self._cached_data = self._crystal_ball_table.rows
        self.__empty_rows_count = 1
        self.__hyperlink_font = QFont()
        self.__hyperlink_font.setUnderline(True)
        self.__blue_brush = QBrush(QColor(Qt.blue))
        self.__yellow_brush = QBrush(QColor('#ffff99'))

    def init_filter_data_list(self):
        self._filter_data_list = self._array_data

    def __is_filter_enabled(self):
        return self.__filter_is_enabled[0]

    def __set_array_data(self):
        self._array_data = self._crystal_ball_table.rows
        self.__fill_unique_vals_dict()

    def __fill_unique_vals_dict(self):
        for index in self.__filterable_csv_headers_list:
            self.__unique_vals_dict[index] = []
            self.__unique_vals_dict[index] = self._fetch_unique_column_vals(index)

    def _column_filter_query(self, index):
        return None

    def _fetch_unique_column_vals(self, index):
        result = []
        query = self._column_filter_query(index)
        try:
            result = self._crystal_ball_table.exec_query(query).fetchall()
        except Exception as e:
            # todo: report error for user
            print "An error occurred in fetching filter unique results"
            print e.message
        finally:
            return [str(value) for (value,) in result]

    def flags(self, QModelIndex):
        # TODO: needs refactoring; move this block to derived classes
        column = self._crystal_ball_table.headers[QModelIndex.column()]
        if self.__is_filter_enabled():
            return QAbstractTableModel.flags(self, QModelIndex)
        if column not in self.read_only_list:
            return QAbstractTableModel.flags(self, QModelIndex) | Qt.ItemIsEditable
        return QAbstractTableModel.flags(self, QModelIndex)

    def add_empty_row(self):
        self.__empty_rows_count += 1
        self.reset()

    def rowCount(self, parent=None, *args, **kwargs):
        if self.__is_filter_enabled():
            return len(self._filter_data_list)
        return len(self._array_data) + self.__empty_rows_count

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._headers)

    @property
    def array_data_len(self):
        return len(self._array_data)

    def start_filter(self, filter_items_dict):
        if not filter_items_dict:
            self._filter_data_list = []
        else:
            self._filter_data_list = []
            query = self._start_filter_query(filter_items_dict)
            try:
                # self._filter_data_list = self._crystal_ball_table.exec_query(query)
                # if self._filter_data_list:
                #     self._filter_data_list = self._filter_data_list.fetchall()
                  if query:
                    self._filter_data_list = query.all()
            except Exception as e:
                print "An error occurred in starting filter"
                print e.message
            # Todo: add finally section
        self.reset()

    def setData(self, QModelIndex, QVariant, role=None):
        column = self._crystal_ball_table.headers[QModelIndex.column()]
        row_index = QModelIndex.row()
        set_obj = False
        if row_index >= self.array_data_len:
            row_object = self.get_object()
            set_obj = True
        else:
            row_object = self._array_data[row_index]
        val = str(QVariant.toString()).strip()
        try:
            if val != "":
                setattr(row_object, column, val)
            else:
                setattr(row_object, column, None)
            if set_obj:
                self._array_data.append(row_object)
        except Exception as e:
            CBMessageBoxes.popup_message(icon=CBMessageBoxes.WARNING,
                                         title="{}: Cannot Set Value".format(self._table_name),
                                         text="Failed to set value \"{}\" for field \"{}\"".format(val, column),
                                         detailed_text=e.message)

        self.reset()  # needed to resize columns horizontal headers
        return True

    def headerData(self, p_int, Qt_Orientation, role=None):
        if role == Qt.DisplayRole and Qt_Orientation == Qt.Horizontal:
            return self._headers[p_int]
        elif role == Qt.DecorationRole and self.__filter_is_enabled[0] and \
                Qt_Orientation == Qt.Horizontal and \
                p_int in self.__filterable_csv_headers_list:
            if self.__filter_is_enabled[2] is None:
                self.__filterable_csv_headers_icons_dict[p_int] = self.__filter_is_enabled[1]
                return QIcon(self.__filter_is_enabled[1])
            else:
                return QIcon(self.__filterable_csv_headers_icons_dict[p_int])

    def update_fkeys(self):
        return []

    def __validate_nullable(self):
        errors_list = []
        d = []
        for item in self._array_data:
            for field in self.nullable_list:
                if not getattr(item, field):
                    d.append(item)
                    errors_list.append(
                        "Field \"{}\" in table \"{}\" not allowed to be none, row removed from insertion".format(field,
                                                                                                                 self._table_name))
        for item in d:
            self._array_data.remove(item)
        return errors_list

    def validate_before_insert(self):
        return self.__validate_nullable() + self.update_fkeys()

    def save_data(self):
        error_list = self.validate_before_insert()
        try:
            self._crystal_ball_table.insert_and_commit(self._array_data)
            self.__empty_rows_count = 1
            self._array_data = []
            self._cached_data = []
            self.__unique_vals_dict = {}
            self.__set_array_data()
            self._cached_data = self._crystal_ball_table.rows
            self.reset()
        except Exception as e:
            error_list.append("Failure in inserting data into table {}. Error: {}".format(self._table_name, e.message))
        return ''.join(error_list)

    def refresh_data(self):
        self.__set_array_data()
        self._cached_data = self._crystal_ball_table.rows
        self.reset()

    def __compare_row_item(self, index):
        if index <= (len(self._cached_data) - 1):
            if not self._array_data[index] == self._cached_data[index]:
                return False
        else:
            return False
        return True

    def compare_all_data_rows(self):
        if len(self._cached_data) != len(self._array_data):
            return False
        for index, item in enumerate(self._array_data):
            if index <= (self.array_data_len - 1):
                if item.id == self._cached_data[index].id:
                    if not item == self._cached_data[index]:
                        return False
            else:
                return False
        return True

    @property
    def hyper_link_attributes_list(self):
        return []

    @property
    def fk_attributes_list(self):
        return []

    def get_cell_value(self, QModelIndex):
        row_index = QModelIndex.row()
        if row_index >= self.array_data_len:
            return
        row = self._array_data[row_index]
        column = self._crystal_ball_table.headers[QModelIndex.column()]
        return getattr(row, column)

    def column_name(self, QModelIndex):
        return self._crystal_ball_table.headers[QModelIndex.column()]

    @property
    def filter_is_enabled(self):
        return self.__filter_is_enabled

    @filter_is_enabled.setter
    def filter_is_enabled(self, val):
        self.__filter_is_enabled = val
        if self.__filter_is_enabled[2] is not None:
            self.__filterable_csv_headers_icons_dict[self.__filter_is_enabled[2]] = self.__filter_is_enabled[1]
        self.reset()

    def data(self, QModelIndex, role=None):  # provides data each time the view requests it
        if self.__is_filter_enabled():
            data_source_list = self._filter_data_list
        else:
            data_source_list = self._array_data

        if QModelIndex.row() >= len(data_source_list):
            return QVariant()

        row = data_source_list[QModelIndex.row()]
        column = self._crystal_ball_table.headers[QModelIndex.column()]

        if role == Qt.DisplayRole:
            try:
                return str(QVariant(getattr(row, column)).toString())
            except Exception as e:
                return ''
        if role == Qt.EditRole and not self.__is_filter_enabled():
            return str(QVariant(getattr(row, column)).toString())
        # Indicate unsaved row
        if role == Qt.BackgroundRole and not self.__compare_row_item(index=QModelIndex.row()):
            return self.__yellow_brush
        # handle hyperlink fields
        if role == Qt.TextColorRole and column in self.hyper_link_attributes_list:
            return self.__blue_brush
        if role == Qt.FontRole and column in self.hyper_link_attributes_list:
            return self.__hyperlink_font

        return QVariant()

    def search_row(self, search_column_index, search_token):
        proxy = QSortFilterProxyModel()
        proxy.setSourceModel(self)
        # TODO: needs refactoring
        # 1 hard coded value is used based on the assumption that we will use this function to
        # search for the table_marking column only to server the feature: go from FK to PK
        search_column_index = 1
        proxy.setFilterKeyColumn(search_column_index)
        proxy.setFilterFixedString(search_token)
        matching_index = proxy.mapToSource(proxy.index(0, 0))
        if matching_index.isValid():
            return matching_index
        return None

    @property
    def read_only_list(self):
        return []

    @property
    def filterable_csv_headers_list(self):
        return self.__filterable_csv_headers_list

    @filterable_csv_headers_list.setter
    def filterable_csv_headers_list(self, val):
        self.__filterable_csv_headers_list = val
        self.__fill_unique_vals_dict()

    def get_unique_column_values(self, column_index):
        if column_index in self.__unique_vals_dict.keys():
            return self.__unique_vals_dict[column_index]

    @property
    def unique_vals_dict(self):
        return self.__unique_vals_dict

    @unique_vals_dict.setter
    def unique_vals_dict(self, val):
        self.__unique_vals_dict = val

    def _start_filter_query(self, filter_items_dict):
        raise NotImplementedError
