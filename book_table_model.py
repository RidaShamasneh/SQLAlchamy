from sqlalchemy import or_, and_

from generic_table_model import GenericTableModel
from gui.filter.filter_constants import FilterConstants
from sql_alchemy_classes import Book


class BookTableModel(GenericTableModel):
    __table_column_names = {}
    __table_column_names[1] = '_isbn'
    __table_column_names[2] = '_title'
    __table_column_names[3] = '_price'
    __table_column_names[4] = 'author_id'

    def __init__(self, table_name):
        super(BookTableModel, self).__init__(table_name)
        self.nullable_list = []
        # TODO-Rida: replace these by ORM calls
        self.__column_filter_query_dict = {}
        self.__column_filter_query_dict[1] = "select distinct {} from book;".format(self.__table_column_names[1])
        self.__column_filter_query_dict[2] = "select distinct {} from book;".format(self.__table_column_names[2])
        self.__column_filter_query_dict[3] = "select distinct {} from book;".format(self.__table_column_names[3])
        self.__column_filter_query_dict[
            4] = "select distinct _name from author inner join book where (author.id = book.author_id)"

    @property
    def hyper_link_attributes_list(self):
        return ['_title']

    def _column_filter_query(self, index):
        if index in self.__column_filter_query_dict.keys():
            return self.__column_filter_query_dict[index]

    def __convert(self, item):
        for obj in self._array_data:
            if obj.author_marking == item:
                return obj.author_id

    def _start_filter_query(self, filter_items_dict):  # todo: needs refactor
        global_binary_expression = None
        for key, vals in filter_items_dict.iteritems():
            column_name = self.__table_column_names[key]
            instrumented_attribute = getattr(self._crystal_ball_table.table_model, column_name)
            list_of_items_to_be_filtered_per_column = []
            is_null_expression = None
            for item in vals.values():
                if item == FilterConstants.BLANKS_STRING:
                    is_null_expression = instrumented_attribute.is_(None)
                elif key == 4:
                    list_of_items_to_be_filtered_per_column.append(self.__convert(item))
                else:
                    list_of_items_to_be_filtered_per_column.append(str(item))
            # construct the local binary expression using in_(..) operator
            local_binary_expression = instrumented_attribute.in_(list_of_items_to_be_filtered_per_column)
            # If blank value is part of the filter, we add it here as an or_ portion to local binary expression
            if is_null_expression is not None:
                local_binary_expression = or_(local_binary_expression, is_null_expression)
            '''
            Accumulate all BinaryExpressions in global expression operator
            '''
            # Special case: for 1st iteration
            if global_binary_expression is None:
                global_binary_expression = local_binary_expression
            # For later iterations, we and_ local binary expression with global one
            else:
                global_binary_expression = and_(global_binary_expression, local_binary_expression)
        # finally, executing it ... :)
        result = self._crystal_ball_table.filter_query(global_binary_expression)
        return result

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

    def _fetch_unique_column_vals(self, index):
        result = []
        append_none = False
        query = self._column_filter_query(index)
        try:
            result = self._crystal_ball_table.exec_query(query).fetchall()
            #TODO-POC: find a way to all ORM API instead?
            if index == 4:
                r = self._crystal_ball_table.exec_query(
                    "select count(*) from book where author_id is null").fetchall()
                if [str(value) for (value,) in r][0] != 0:
                    append_none = True
        except Exception as e:
            # todo: report error for user
            print "An error occurred in fetching filter unique results"
            print e.message
        finally:
            result = [str(value) for (value,) in result]
            if append_none:
                result.append('None')
            return result
