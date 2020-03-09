from generic_table_model import GenericTableModel
from gui.filter.filter_constants import FilterConstants
from sql_alchemy_classes import Book


class BookTableModel(GenericTableModel):
    __table_column_names = {}
    __table_column_names[1] = '_isbn'
    __table_column_names[2] = '_title'
    __table_column_names[3] = '_price'

    def __init__(self, table_name):
        super(BookTableModel, self).__init__(table_name)
        self.nullable_list = []
        self.__column_filter_query_dict = {}
        self.__column_filter_query_dict[1] = "select distinct {} from book;".format(self.__table_column_names[1])
        self.__column_filter_query_dict[2] = "select distinct {} from book;".format(self.__table_column_names[2])
        self.__column_filter_query_dict[3] = "select distinct {} from book;".format(self.__table_column_names[3])

    @property
    def hyper_link_attributes_list(self):
        return ['_title']

    def _column_filter_query(self, index):
        if index in self.__column_filter_query_dict.keys():
            return self.__column_filter_query_dict[index]

    def _start_filter_query(self, filter_items_dict):  # todo: needs refactor
        query = "select * from book where "
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

    @property
    def fk_attributes_list(self):
        return ['author_marking']

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
