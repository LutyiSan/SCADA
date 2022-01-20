import pymysql
import pymysql.cursors
from loguru import logger
from config.config import DB


class DBDriver:
    def __init__(self):
     #   logger.add("logs/db.log", format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}", rotation="2MB")
        self.cursor = None
        self.connector = None

    def connect(self):
        connect_state = bool
        try:
            self.connector = pymysql.connect(host=DB['HOST'], port=DB['PORT'], user=DB['USERNAME'],
                                             password=DB['PASSWD'], database=DB['DB_NAME'],
                                             cursorclass=pymysql.cursors.DictCursor, autocommit=True)
            self.cursor = self.connector.cursor()
            connect_state = True
            logger.info('READY Connect to data base')
        except Exception as e:
            connect_state = False
            logger.exception('FAIL Connect to data base', e)
        return connect_state

    def db_get(self, query):
        result = None
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
        except Exception as e:
            logger.exception(f'FAIL SELECT QUERY: {query}', e)
        return result

    def db_update(self, query):
        result = None
        try:
            self.cursor.execute(query)
            # result = self.cursor.fetchall()
        except Exception as e:
            logger.exception(f'FAIL UPDATE QUERY: {query}', e)
        # return result

    def disconnect(self):
        try:
            self.cursor.close()
            logger.info('Connection to DB closed')
        except Exception as e:
            logger.exception('FAIL close connection to DB', e)



