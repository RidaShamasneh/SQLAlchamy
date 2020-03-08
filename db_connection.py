from mysql_connection_manager import MysqlConnectionManager


class DbConnection(object):
    def __init__(self):
        self.__manager = MysqlConnectionManager.getInstance()

    def initialize_connection(self):
        self.__manager.initialize_connection()

    def close_connectiion(self):
        self.__manager.close_connection()
