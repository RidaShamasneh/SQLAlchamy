class MysqlConnectionConstants(object):
    DIALECT = 'mysql'
    DRIVER = 'mysqlconnector'
    CONNECTION_STRING = '{}+{}://{}:{}@{}:{}/{}'  # todo: support charset
    BACKUP_DB_CMD = 'mysqldump --default-character-set=utf8 ' \
                    '--add-drop-table --add-locks --dump-date --lock-tables -h ' \
                    '{} -P {} -u {} -p{} {} > {}'
    SQL_EXTENSION = '.sql'
    DB_BACKUP_PROCESS_TIMEOUT_SEC = 500
