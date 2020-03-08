from mysql_connection_manager import MysqlConnectionManager


class CBTable(object):
    def __init__(self, table_name):
        self.__manager = MysqlConnectionManager.getInstance()
        self.__table_name = table_name
        self._headers = []
        self.__rows = []
        self.__table_model = self.__manager.get_table(table_name)  # needs refactor
        if self.__table_model is not None:
            self._headers = map(lambda x: str(x), self.__table_model.__table__.columns.keys())
            # if table_name == 'test_result':  # todo: needs refactoring
            #     self._headers = [item if item != 'test_type_id' else 'test_type_name' for item in self._headers]
            #     self._headers = [item if item != 'storage_id' else 'storage_marking' for item in self._headers]
            # elif table_name == 'storage':
            #     self._headers = [item if item != 'controller_id' else 'controller_marking' for item in
            #                      self._headers]
            #     self._headers = [item if item != 'memory_id' else 'memory_marking' for item in self._headers]
            self.__rows = self.__manager.read_all(table_name)  # needs refactor

    def insert_and_commit(self, data):
        self.__manager.insert_and_commit(data)

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, val):
        self._headers = val

    @property
    def rows(self):
        return self.__manager.read_all(self.__table_name)

    @rows.setter
    def rows(self, val):
        self.__rows = val

    def exec_query(self, query):
        return self.__manager.execute_query(query)
