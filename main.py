import datetime
from database.driver import DBDriver
from config.config import POLLING_DEVICE
from modbus.modbus_poll import ModbusPoll


def grouping(signals_dict):
    r_type = str
    count = len(signals_dict)
    new_list = list()
    start = signals_dict[0]['register_address']
    quantity = 1
    reg = -1
    while reg < count - 2:
        reg += 1
        r_type = signals_dict[reg]['registers_type']
        if signals_dict[reg]['register_address'] + signals_dict[reg]['quantity'] == signals_dict[reg + 1][
            'register_address'] and signals_dict[reg]['registers_type'] == signals_dict[reg + 1]['registers_type']:
            quantity += signals_dict[reg]['quantity']
        else:
            if quantity == 1:
                quantity = signals_dict[reg]['quantity']
            new_list.append([start, quantity, r_type])
            start = signals_dict[reg + 1]['register_address']
            quantity = 1
    new_list.append([start, quantity, r_type])
    print(new_list)
    return new_list


def run():
    while True:
        for i in POLLING_DEVICE:
            db.connect()
            device_query = f"SELECT*FROM `devices` WHERE `device_id` = {i}"
            device_settings = db.db_get(device_query)
            if device_settings is not tuple:
                if device_settings[0]['protocol'] == 'modbus':
                    signals_query = f"SELECT*FROM modbus WHERE `device_id`  = {i} ORDER BY `registers_type`, `register_address`"
                    signals = db.db_get(signals_query)
                    if signals != tuple():
                        signals = grouping(signals)
                        mbp = ModbusPoll(device_settings[0], signals)
                        connect_state = mbp.connect()
                        if connect_state:
                            poll_dict = mbp.read_device()
                            print(poll_dict)
                            mbp.disconnect()
                        # Здесь должна быть функция парсера и преобразования данных

                        # for signal in poll_dict:
                        #   timestamp = datetime.datetime.now()
                        #   query = f"UPDATE modbus SET `present_value` = '{(signal['present_value'])}', " \
                        #         f"`time_read` = '{timestamp}' WHERE `signal_id` = '{(signal['signal_id'])}' "
                        #  db.db_update(query)
                        else:
                            mbp.disconnect()

            db.disconnect()


if __name__ == "__main__":
    run()
