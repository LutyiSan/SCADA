from loguru import logger
import datetime
from database.driver import DBDriver
from modbus.modbus_poll import ModbusPoll
from functions.convertor import Convertor
from functions.grouper import Grouper


class Runner:
    def __init__(self, device_id):
        self.data_for_db = None
        # logger.add("logs/run.log", format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}", rotation="2MB")
        self.signals = None
        self.device_settings = None
        self.signals_dict = dict()
        self.db = DBDriver()
        self.device_id = device_id

    def create_device_polling(self):
        if self.db.connect():
            self.device_settings = self.db.db_get(f"SELECT*FROM `devices` WHERE `device_id` = {self.device_id}")
            if type(self.device_settings) is not tuple or type(self.device_settings) is None:
                if self.device_settings[0]['protocol'] == 'modbus':
                    signals_query = f"SELECT*FROM modbus WHERE `device_id`  = {self.device_id} ORDER BY" \
                                    f" `registers_type`, `register_address`, `bit_number`"
                    self.signals = self.db.db_get(signals_query)
                    if self.signals != tuple():
                        len_signals = len(self.signals)
                        logger.info(f'{len_signals} signals into device-{self.device_id}')
                        gr = Grouper(self.signals)
                        self.signals_dict = gr.grouping()
                        logger.debug(f"start-addresses: {self.signals_dict['start_address']} |"
                                     f" read-quantity: {self.signals_dict['read_quantity']}")
                    else:
                        logger.debug(f"No signals in Data Base for device {self.device_settings['device_id']}")
            else:
                logger.debug(f"No DATA in Data Base for device {self.device_settings['device_id']}")
        else:
            logger.error(f"No connect to Data Base")

    def polling(self):
        self.poll_list = list()
        mbp = ModbusPoll(self.device_settings[0], self.signals_dict)
        if mbp.connect():
            self.poll_list = mbp.read_device()
            poll_len = len(self.poll_list)
            logger.debug(f'reading DATA length: {poll_len}')
            mbp.disconnect()
            return True
        else:
            return False

    def convert(self):
        cv = Convertor(self.signals_dict, self.poll_list)
        self.data_for_db = cv.convert()

    def put_to_db(self):
        if self.db.connect():
            count = len(self.data_for_db['uuid']) - 1
            i = -1
            while i < count:
                i += 1
                timestamp = datetime.datetime.now()
                query = f"UPDATE modbus SET present_value = '{self.data_for_db['present_value'][i]}', " \
                        f"time_read = '{timestamp}' WHERE signal_id = '{self.data_for_db['uuid'][i]}'"

                self.db.db_update(query)
            logger.info(f'Signals UPDATED in data base SUCCESS')
            self.db.disconnect()
