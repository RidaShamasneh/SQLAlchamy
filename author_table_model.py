from generic_table_model import GenericTableModel
from gui.filter.filter_constants import FilterConstants
from sql_alchemy_classes import Author


class AuthorTableModel(GenericTableModel):
    __table_column_names = {}
    __table_column_names[1] = '_name'

    def __init__(self, table_name):
        super(AuthorTableModel, self).__init__(table_name)
        self.__column_filter_query_dict = {}
        self.__column_filter_query_dict[1] = "select distinct {} from author;".format(self.__table_column_names[1])
        self.nullable_list = []

    def _column_filter_query(self, index):
        if index in self.__column_filter_query_dict.keys():
            return self.__column_filter_query_dict[index]

    def _start_filter_query(self, filter_items_dict):  # todo: needs refactor
        query = "select * from author where "
        for key, vals in filter_items_dict.iteritems():
            blanks = False
            added = False
            for item in vals.values():
                if item == FilterConstants.BLANKS_STRING:
                    query += "{} is null ".format(self.__table_column_names[key])
                    blanks = True
                else:
                    if blanks:
                        query += " or "
                        blanks = False
                    if not added:
                        query += self.__table_column_names[key] + " in ('{}')".format(item)
                        added = True
                    else:
                        query = query[:-1]
                        query += " ,'{}')".format(item)

            query += " and "
        query = query[:-len('  and')]
        return query

    def get_object(self):
        tmp_object = Author()
        return tmp_object
