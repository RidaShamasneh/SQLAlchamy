from collections import OrderedDict

from author_table_model import AuthorTableModel
from book_table_model import BookTableModel


class TableModelFactory(object):
    switcher = OrderedDict()

    @staticmethod
    def init_models():
        # order matters
        TableModelFactory.switcher['book'] = BookTableModel('book')
        TableModelFactory.switcher['author'] = AuthorTableModel('author')

    @staticmethod
    def get_table_model(table_name):
        return TableModelFactory.switcher.get(table_name, None)
