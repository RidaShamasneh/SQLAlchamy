from generic_table_model import GenericTableModel
from sql_alchemy_classes import Book


class BookTableModel(GenericTableModel):
    def __init__(self, table_name):
        super(BookTableModel, self).__init__(table_name)

    def get_object(self):
        tmp_object = Book()
        return tmp_object
