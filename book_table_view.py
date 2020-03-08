from generic_table_view import GenericTableView


class BookTableView(GenericTableView):
    def __init__(self, model, parent):
        super(BookTableView, self).__init__(model, parent)
