from generic_table_model import GenericTableModel
from sql_alchemy_classes import Author


class AuthorTableModel(GenericTableModel):
    def __init__(self, table_name):
        super(AuthorTableModel, self).__init__(table_name)
        self.nullable_list = []

    def get_object(self):
        tmp_object = Author()
        return tmp_object