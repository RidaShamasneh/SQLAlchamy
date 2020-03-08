from generic_table_model import GenericTableModel


class BookTableModel(GenericTableModel):
    def __init__(self, table_name):
        super(BookTableModel, self).__init__(table_name)
