import os
import subprocess
import datetime
from threading import Timer

from cb_message_boxes import CBMessageBoxes
from mysql_connection_constants import MysqlConnectionConstants


class DBBackup(object):

    @staticmethod
    def export_database():
        file_name = 'cb_db_{}{}'.format(datetime.datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S"), MysqlConnectionConstants.SQL_EXTENSION)

        db_name = 'testing_db'
        db_user = 'root'
        user_password = 'root'
        host = "localhost"
        port = '3306'

        back_up_folder = "db_backups"
        if not os.path.exists(back_up_folder):
            os.mkdir(back_up_folder)
        file_name = os.path.join(back_up_folder, file_name)
        cmd = MysqlConnectionConstants.BACKUP_DB_CMD.format(
            host,
            port,
            db_user,
            user_password,
            db_name,
            file_name)
        error, rc = DBBackup.__execute_cmd(cmd)
        if rc:
            CBMessageBoxes.popup_message(icon=CBMessageBoxes.CRITICAL,
                                         title="Database Export Error",
                                         text="Failed to export database \n{}".format(file_name),
                                         detailed_text=error[0])
            return
        CBMessageBoxes.popup_message(icon=CBMessageBoxes.INFO,
                                     title="Database Export Success",
                                     text="File generated; path \n{}".format(file_name))

    @staticmethod
    def __execute_cmd(cmd):
        process = subprocess.Popen(cmd, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        timer = Timer(MysqlConnectionConstants.DB_BACKUP_PROCESS_TIMEOUT_SEC, process.kill, [process])
        timer.start()
        output = process.communicate()
        timer.cancel()
        return output, process.returncode
