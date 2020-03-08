from PyQt4.QtCore import QAbstractTableModel, QVariant, Qt
from PyQt4.QtGui import QBrush, QColor, QFont, QSortFilterProxyModel, QIcon

from cb_table import CBTable


class GenericTableModel(QAbstractTableModel):
    def __init__(self, table_name):
        super(GenericTableModel, self).__init__()
        self._table_name = table_name
        self._crystal_ball_table = CBTable(table_name=self._table_name)
        self._headers = map(lambda x: x.title().replace("_", " "), self._crystal_ball_table.headers)
        self.__set_array_data()

    def __set_array_data(self):
        self._array_data = self._crystal_ball_table.rows

    def flags(self, QModelIndex):
        # TODO: needs refactoring; move this block to derived classes
        column = self._crystal_ball_table.headers[QModelIndex.column()]
        # TODO: determine which column is readonly and which is not?
        return QAbstractTableModel.flags(self, QModelIndex)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._array_data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._headers)

    def headerData(self, p_int, Qt_Orientation, role=None):
        if role == Qt.DisplayRole and Qt_Orientation == Qt.Horizontal:
            return self._headers[p_int]

    def refresh_data(self):
        self.__set_array_data()
        # self._cached_data = self._crystal_ball_table.rows
        self.reset()

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
        # if role == Qt.BackgroundRole and not self.__compare_row_item(index=QModelIndex.row()):
        #     return self.__yellow_brush
        # # handle hyperlink fields
        # if role == Qt.TextColorRole and column in self.hyper_link_attributes_list:
        #     return self.__blue_brush
        # if role == Qt.FontRole and column in self.hyper_link_attributes_list:
        #     return self.__hyperlink_font

        return QVariant()
