from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy_utils import database_exists, create_database

import declarative_base_class
from sql_alchemy_classes import Book, Author

from mysql_connection_constants import MysqlConnectionConstants


class MysqlConnectionManager(object):
    __instance = None
    tables_models = {'book': Book,
                     'author': Author}

    ''''
    This class is implemented as a singleton. One instance should be used in the application to manage sql related 
    connection
    '''

    @staticmethod
    def getInstance():
        if MysqlConnectionManager.__instance is None:
            MysqlConnectionManager()
        return MysqlConnectionManager.__instance

    def __init__(self):
        if MysqlConnectionManager.__instance is None:
            MysqlConnectionManager.__instance = self
            self.__db_name = None
            self.__db_user = None
            self.__user_password = None
            self.__host = None
            self.__port = None
            self.__db_engine = None
            self.__connection = None
            self.__meta_data = sqlalchemy.MetaData()
            self.__session_maker = sessionmaker()
            self.__setup()
        else:
            raise Exception("One instance is allowed from class {}".format(__name__))

    def __setup(self):
        self.__db_name = 'testing_db'
        self.__db_user = 'root'
        self.__user_password = 'root'
        self.__host = "localhost"
        self.__port = '3306'

    def initialize_connection(self):
        self.__engine = sqlalchemy.create_engine(
            MysqlConnectionConstants.CONNECTION_STRING.format(MysqlConnectionConstants.DIALECT,
                                                              MysqlConnectionConstants.DRIVER,
                                                              self.__db_user,
                                                              self.__user_password,
                                                              self.__host,
                                                              self.__port,
                                                              self.__db_name), encoding='utf8', echo=False, pool_size=0)
        if not database_exists(self.__engine.url):
            create_database(self.__engine.url)

        self.__connection = self.__engine.connect()
        self.__session_maker.configure(bind=self.__engine)

        # create tables if does not exist in database
        declarative_base_class.base.metadata.create_all(self.__engine,
                                                        checkfirst=True)  # don't issue CREATEs for tables already exists
        self.__meta_data.reflect(bind=self.__engine)
        declarative_base_class.base.metadata = self.__meta_data

    def __del__(self):
        self.close_connection()

    def close_connection(self):
        self.__connection.close()

    def get_table(self, table_name):
        table = None
        try:  # TODO: propagate exception instead of catching it
            table = self.tables_models[table_name]
        except Exception as e:  # TODO: catch less general exception
            print "Fetch table failed"
        return table

    def read_all(self, table):
        session = self.__session_maker()
        rows = session.query(self.tables_models[table]).all()
        session.close()
        return rows

    def execute_query(self, query):
        result = []
        try:
            result = self.__connection.execute(query)
        except Exception as e:  # TODO: catch less general exception
            print "Executing query {} failed. Error \n".format(query, e)
        return result

    def execute_query_no_raise(self, query):
        result = self.__connection.execute(query)
        return result

    def insert_and_commit(self, data_list):
        session = self.__session_maker()
        try:
            session.bulk_save_objects(data_list)
            session.commit()
        except Exception as e:  # TODO: catch less general exception
            raise Exception(e.message)
        finally:
            session.close()

    @property
    def session(self):
        return self.__session_maker()
