from generic_table_model import GenericTableModel
from sql_alchemy_classes import Book


class BookTableModel(GenericTableModel):
    def __init__(self, table_name):
        super(BookTableModel, self).__init__(table_name)
        self.nullable_list = []

    def get_object(self):
        tmp_object = Book()
        return tmp_object

    def update_fkeys(self):
        errors_list = []
        d = []
        for item in self._array_data:
            try:
                item.set_fkeys()
            except Exception as e:
                d.append(item)
                errors_list.append("Failed to validate row in table {}. Error: {}".format(self._table_name, e.message))
        for item in d:
            self._array_data.remove(item)
        return errors_list