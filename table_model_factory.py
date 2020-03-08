from collections import OrderedDict
from book_table_model import BookTableModel


class TableModelFactory(object):
    switcher = OrderedDict()

    @staticmethod
    def init_models():
        # order matters
        TableModelFactory.switcher['book'] = BookTableModel('book')
        TableModelFactory.switcher['author'] = BookTableModel('author')

    @staticmethod
    def get_table_model(table_name):
        return TableModelFactory.switcher.get(table_name, None)
