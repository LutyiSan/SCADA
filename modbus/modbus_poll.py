from modbus.driver import Modbus
from loguru import logger
from time import time


def to_16_bit(value):
    bin_value = bin(value)[2:]
    if len(bin_value) != 16:
        zero_array = ""
        count = 16 - len(bin_value)
        i = 0
        while i < count:
            i += 1
            zero_array += '0'
        zero_array += bin_value
        return zero_array
    else:
        return bin_value


def to_bool(value, bit_number=None):
    if bit_number is None:
        if value != 0:
            return 'true'
        else:
            return 'false'
    elif 16 > bit_number >= 0:
        bin_value = to_16_bit(value)[bit_number]
        if bin_value == '0':
            return 'false'
        else:
            return 'true'


def to_uint(value):
    if value >= 0:
        return value
    else:
        bin_value = to_16_bit(value)
        bin_value = '0b0' + bin_value
        uint_value = int(bin_value, 2)
        return uint_value


def converter(value, value_type, bit_number):
    if value_type == 'int' or value_type == "float":
        return value
    elif value_type == 'bool':
        result = to_bool(value, bit_number)
        return result
    elif value_type == 'uint':
        result = to_uint(value)
        return result
    else:
        return 'fault type'


class ModbusPoll:
    def __init__(self, device, signals):
     #   logger.add("logs/modbus.log", format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}", rotation="2MB")
        self.result_value = list()
        self.device = device
        self.signals = signals
        self.client = Modbus(self.device['ip_address'], self.device['tcp_port'])
        self.res_list = list()

    def connect(self):
        connect_state = False
        con_start = time()
        try:
            connect_state = self.client.connect()
        except:
            logger.exception('Connection TIMEOUT')

        con_stop = time()
        time_con = con_stop - con_start
        logger.info(f"TIME Connecting to {self.device['ip_address']} | {time_con}")
        return connect_state

    def read_hr(self, register_address, quantity):
        if quantity in range(1, 125):
            return_value = self.client.reader('hr', register_address, quantity)
            for i in return_value:
                self.result_value.append(i)
        else:
            logger.warning(f"INCORRECT parameter 'quantity' in {self.device['ip_address']} | {register_address}")
        return self.result_value

    def read_ir(self, register_address, quantity):
        if quantity in range(1, 125):
            return_value = self.client.reader('ir', register_address, quantity)
            for i in return_value:
                self.result_value.append(i)
        else:
            logger.warning(f"INCORRECT parameter 'quantity' in {self.device['ip_address']} | {register_address}")
        return self.result_value

    def read_coil(self, register_address, quantity):
        if quantity in range(1, 125):
            return_value = self.client.reader('coil', register_address, quantity)
            if type(return_value) == list and len(return_value) == quantity:
                self.result_value = return_value
            else:
                self.result_value = list()
                i = 0
                while i < quantity:
                    i += 1
                    self.result_value.append('fault')
                logger.debug(f"FAIL reading {self.device['ip_address']} | {register_address}")
        else:
            logger.warning(f"INCORRECT parameter 'quantity' in {self.device['ip_address']} | {register_address}")
        return self.result_value

    def read_di(self, register_address, quantity):
        if quantity in range(1, 125):
            return_value = self.client.reader('di', register_address, quantity)
            if type(return_value) == list and len(return_value) == quantity:
                self.result_value = return_value
            else:
                self.result_value = list()
                i = 0
                while i < quantity:
                    i += 1
                    self.result_value.append('fault')
                logger.debug(f"FAIL reading {self.device['ip_address']} | {register_address}")
        else:
            logger.warning(f"INCORRECT parameter 'quantity' in {self.device['ip_address']} | {register_address}")
        return self.result_value

    def read_device(self):
        start_read_device = time()
        start_address = self.signals['start_address']
        read_quantity = self.signals['read_quantity']
        reg_type = self.signals['reg_type']
        count = len(start_address) -1
        i = -1
        while i < count:
            i += 1
            if reg_type[i] == 'holding registers':
                self.result_value = self.read_hr(start_address[i], read_quantity[i])
            elif reg_type[i] == 'input registers':
                self.result_value = self.read_hr(start_address[i], read_quantity[i])
            elif reg_type[i] == 'coils':
                self.result_value = self.read_coil(start_address[i], read_quantity[i])
            elif reg_type[i]['registers_type'] == 'discrete inputs':
                self.result_value = self.read_di(start_address[i], read_quantity[i])
            for r in self.result_value:
                self.res_list.append(r)
        stop_reading_device = time()
        avg_time = stop_reading_device - start_read_device
        len_read = sum(read_quantity)
        logger.info(f"DEVICE {self.device['ip_address']}: READ TIME {avg_time} | reading {len_read} registers")
        return self.res_list

    def disconnect(self):
        self.client.disconnect()
