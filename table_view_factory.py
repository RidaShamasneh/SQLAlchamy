from book_table_model import BookTableModel
from book_table_view import BookTableView


class TableViewFactory(object):
    @staticmethod
    def get_table_view(model, tab_widget):
        if type(model) == BookTableModel:
            return BookTableView(model, tab_widget)
        else:
            raise Exception("Model Type \"{}\" is not supported yet!".format(type(model)))
