from loguru import logger
import datetime
from database.driver import DBDriver
from modbus.modbus_poll import ModbusPoll
from convertor import Convertor


def grouping_signals(signals_dict):
    count = len(signals_dict)
    #print("Start LEN ", count)
    new_dict = {'start_address': [], 'read_quantity': [], 'reg_type': [], 'reg_address': [],
                'signal_quantity': [], 'value_type': [], 'bit_number': [], 'uuid': [], 'present_value': []}
    start = signals_dict[0]['register_address']
    start_count = signals_dict[0]['quantity']
    quantity = 0
    reg = -1
    while reg < count - 1:
        reg += 1
        if reg != count - 1:
            if signals_dict[reg]['register_address'] + signals_dict[reg]['quantity'] == \
                    signals_dict[reg + 1]['register_address'] and \
                    signals_dict[reg]['registers_type'] == signals_dict[reg + 1]['registers_type']:
                quantity += signals_dict[reg + 1]['quantity']
                new_dict['reg_address'].append(signals_dict[reg]['register_address'])
                new_dict['signal_quantity'].append(signals_dict[reg]['quantity'])
                new_dict['value_type'].append(signals_dict[reg]['value_type'])
                if signals_dict[reg]['bit_number'] is not None:
                    new_dict['bit_number'].append(signals_dict[reg]['bit_number'])
                else:
                    new_dict['bit_number'].append('none')
                new_dict['uuid'].append(signals_dict[reg]['signal_id'])
            elif signals_dict[reg]['register_address'] == signals_dict[reg + 1]['register_address']:
                new_dict['reg_address'].append(signals_dict[reg]['register_address'])
                new_dict['signal_quantity'].append(signals_dict[reg]['quantity'])
                new_dict['value_type'].append(signals_dict[reg]['value_type'])
                if signals_dict[reg]['bit_number'] is not None:
                    new_dict['bit_number'].append(signals_dict[reg]['bit_number'])
                else:
                    new_dict['bit_number'].append('none')
                new_dict['uuid'].append(signals_dict[reg]['signal_id'])
            elif len(new_dict['reg_address']) > 0 and signals_dict[reg]['register_address'] == signals_dict[reg - 1][
                'register_address']:
                pass
            else:
                if quantity == 1:
                    quantity = signals_dict[reg]['quantity']
                quantity += start_count
                new_dict['reg_address'].append(signals_dict[reg]['register_address'])
                new_dict['signal_quantity'].append(signals_dict[reg]['quantity'])
                new_dict['value_type'].append(signals_dict[reg]['value_type'])
                if signals_dict[reg]['bit_number'] is not None:
                    new_dict['bit_number'].append(signals_dict[reg]['bit_number'])
                else:
                    new_dict['bit_number'].append('none')
                new_dict['uuid'].append(signals_dict[reg]['signal_id'])
                new_dict['start_address'].append(start)
                new_dict['read_quantity'].append(quantity)
                new_dict['reg_type'].append(signals_dict[reg]['registers_type'])
                start = signals_dict[reg + 1]['register_address']
                start_count = signals_dict[reg + 1]['quantity']
                quantity = 0
        else:
            new_dict['reg_address'].append(signals_dict[reg]['register_address'])
            new_dict['signal_quantity'].append(signals_dict[reg]['quantity'])
            new_dict['value_type'].append(signals_dict[reg]['value_type'])
            if signals_dict[reg]['bit_number'] is not None:
                new_dict['bit_number'].append(signals_dict[reg]['bit_number'])
            else:
                new_dict['bit_number'].append('none')
                new_dict['uuid'].append(signals_dict[reg]['signal_id'])

    new_dict['start_address'].append(start)
    new_dict['read_quantity'].append(quantity + signals_dict[reg]['quantity'])
    new_dict['reg_type'].append(signals_dict[reg]['registers_type'])
    count2 = len(new_dict['uuid'])
   # print("After GROUPING LEN ", count2)
    #print(new_dict)
    return new_dict


class Runner:
    def __init__(self, device_id):
        self.data_for_db = None
        logger.add("logs/run.log", format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}", rotation="2MB")
        self.signals = None
        self.device_settings = None
        self.signals_dict = dict()
        self.db = DBDriver()
        self.device_id = device_id

    def create_device_polling(self):
        connect_state = self.db.connect()
        if connect_state:
            self.device_settings = self.db.db_get(f"SELECT*FROM `devices` WHERE `device_id` = {self.device_id}")
            if self.device_settings is not tuple:
                if self.device_settings[0]['protocol'] == 'modbus':
                    signals_query = f"SELECT*FROM modbus WHERE `device_id`  = {self.device_id} ORDER BY" \
                                    f" `registers_type`, `register_address`, `bit_number`"
                    self.signals = self.db.db_get(signals_query)
                    if self.signals != tuple():
                        self.signals_dict = grouping_signals(self.signals)
                    else:
                        logger.debug(f"No signals in Data Base for device {self.device_settings[0]['device_id']}")
            else:
                logger.debug(f"No DATA in Data Base for device {self.device_settings[0]['device_id']}")
        else:
            logger.error(f"No connect to Data Base")
        #self.db.disconnect()

    def polling(self):
        self.poll_list = list()
        mbp = ModbusPoll(self.device_settings[0], self.signals_dict)
        connect_state = mbp.connect()
        if connect_state:
            self.poll_list = mbp.read_device()
            mbp.disconnect()
        else:
            pass
        return connect_state

    def convert(self):
        cv = Convertor(self.signals_dict, self.poll_list)
        self.data_for_db = cv.convert()
        count = len(self.data_for_db['present_value'])
        #print(self.data_for_db)
       # print(count)

    def put_to_db(self):
        connect_state = self.db.connect()
        if connect_state:
            count = len(self.data_for_db['uuid']) -1
            i = -1
            while i < count:
                i += 1
                timestamp = datetime.datetime.now()
                query = f"UPDATE modbus SET present_value = '{self.data_for_db['present_value'][i]}', " \
                                        f"time_read = '{timestamp}' WHERE signal_id = '{self.data_for_db['uuid'][i]}'"

                self.db.db_update(query)
            self.db.disconnect()



#run = Runner(100)
#run.create_device_polling()
#cs = run.polling()
#if cs:
 #   run.convert()
#run.put_to_db()
