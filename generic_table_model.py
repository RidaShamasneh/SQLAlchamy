from PyQt4.QtCore import QAbstractTableModel, QVariant, Qt
from PyQt4.QtGui import QBrush, QColor, QFont, QSortFilterProxyModel, QIcon

from cb_message_boxes import CBMessageBoxes
from cb_table import CBTable


class GenericTableModel(QAbstractTableModel):
    def __init__(self, table_name):
        super(GenericTableModel, self).__init__()
        self._table_name = table_name
        self._crystal_ball_table = CBTable(table_name=self._table_name)
        self._headers = map(lambda x: x.title().replace("_", " "), self._crystal_ball_table.headers)
        self.__set_array_data()
        self._cached_data = self._crystal_ball_table.rows
        self.__empty_rows_count = 1
        self.__hyperlink_font = QFont()
        self.__hyperlink_font.setUnderline(True)
        self.__blue_brush = QBrush(QColor(Qt.blue))
        self.__yellow_brush = QBrush(QColor('#ffff99'))

    def __set_array_data(self):
        self._array_data = self._crystal_ball_table.rows

    def flags(self, QModelIndex):
        # TODO: needs refactoring; move this block to derived classes
        column = self._crystal_ball_table.headers[QModelIndex.column()]
        # TODO: determine which column is readonly and which is not?
        return QAbstractTableModel.flags(self, QModelIndex) | Qt.ItemIsEditable

    def add_empty_row(self):
        self.__empty_rows_count += 1
        self.reset()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._array_data) + self.__empty_rows_count

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._headers)

    @property
    def array_data_len(self):
        return len(self._array_data)

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
            # self.__unique_vals_dict = {}
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

    def data(self, QModelIndex, role=None):  # provides data each time the view requests it
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
        # if role == Qt.EditRole and not self.__is_filter_enabled():
        #     return str(QVariant(getattr(row, column)).toString())
        # Indicate unsaved row
        if role == Qt.BackgroundRole and not self.__compare_row_item(index=QModelIndex.row()):
            return self.__yellow_brush
        # handle hyperlink fields
        if role == Qt.TextColorRole and column in self.hyper_link_attributes_list:
            return self.__blue_brush
        if role == Qt.FontRole and column in self.hyper_link_attributes_list:
            return self.__hyperlink_font

        return QVariant()
