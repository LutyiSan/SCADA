from easymodbus import modbusClient
from easymodbus.modbusClient import convert_float_to_two_registers, convert_registers_to_float
from loguru import logger
from func_timeout import func_set_timeout


class Modbus:
    # TODO timeout settings
    timeout = 0.2

    def __init__(self, ip_address, tcp_port):
        self.connect_state = None
        self.retry = None
        #  logger.add("logs/modbus.log", format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}", rotation="2MB")
        self.ip_address = ip_address
        self.client = modbusClient.ModbusClient(ip_address, tcp_port)

    @func_set_timeout(3)
    def connect(self, retry=2):
        self.retry = retry
        attempt = 0
        while attempt < self.retry and not self.connect_state:
            attempt += 1
            try:
                self.client.connect()
                self.connect_state = True
                logger.info(f" READY connection to {self.ip_address}")
            except Exception as e:
                self.connect_state = False
                logger.exception(f"FAIL connect to {self.ip_address}\n{e}")
        return self.connect_state

    def reader(self, type, register_address, quantity):
        result = list()
        if type == 'hr':
            try:
                result = self.read_hr(register_address, quantity)
            except:
                i = -1
                while i < quantity:
                    i += 1
                    result.append('none')
                logger.error('timeout')

        elif type == 'ir':
            try:
                result = self.read_ir(register_address, quantity)
            except:
                i = -1
                while i < quantity:
                    i += 1
                    result.append('none')
                logger.error('timeout')

        elif type == 'coil':
            try:
                result = self.read_coil(register_address, quantity)
            except:
                i = -1
                while i < quantity:
                    i += 1
                    result.append('none')
                logger.error('timeout')

        elif type == 'di':
            try:
                result = self.read_di(register_address, quantity)
            except:
                i = -1
                while i < quantity:
                    i += 1
                    result.append('none')
                logger.error('timeout')
        return result

    @func_set_timeout(timeout)
    def read_hr(self, reg_address, quantity):
        return_result = list()
        try:
            result = self.client.read_holdingregisters(reg_address, quantity)
            if type(result) == list and len(result) == quantity:
                return_result = result
            else:
                i = -1
                while i < quantity:
                    i += 1
                    return_result.append('none')
        except Exception as e:
            i = -1
            while i < quantity:
                i += 1
                return_result.append('none')
            logger.exception(f"FAIL read registers: {reg_address}\n{e}")
        return return_result

    @func_set_timeout(timeout)
    def read_ir(self, reg_address, quantity):
        return_result = list()
        try:
            result = self.client.read_inputregisters(reg_address, quantity)
            if type(result) == list and len(result) == quantity:
                return_result = result
            else:
                i = -1
                while i < quantity:
                    i += 1
                    return_result.append('none')
        except Exception as e:
            i = -1
            while i < quantity:
                i += 1
                return_result.append('none')
            logger.exception(f"FAIL read registers: {reg_address}\n{e}")
        return return_result

    @func_set_timeout(timeout)
    def read_coil(self, reg_address, quantity):
        result = ['None']
        try:
            # logger.info(f"TRY to read registers")
            result = self.client.read_coils(reg_address, quantity)
        except Exception as e:
            logger.exception(f"FAIL read registers: {reg_address}\n{e}")
        return result

    @func_set_timeout(timeout)
    def read_di(self, reg_address, quantity):
        result = ['None']
        try:
            # logger.info(f"TRY to read registers")
            result = self.client.read_discreteinputs(reg_address, quantity)
        except Exception as e:
            logger.exception(f"FAIL read registers: {reg_address}\n{e}")
        return result

    def write_hr(self, reg_address, value):
        write_status = False
        try:
            logger.info(f"TRY write value in registers")
            self.client.write_single_register(reg_address, value)
            write_status = True
        except Exception as e:
            logger.exception(f"FAIL write value in registers\n{e}")
        return write_status

    def write_float_hr(self, reg_address, value):
        write_status = False
        try:
            logger.info(f"TRY write value in registers")
            self.client.write_multiple_registers(reg_address, convert_float_to_two_registers(value))
            write_status = True
        except Exception as e:
            logger.exception(f"FAIL write value in registers\n{e}")
        return write_status

    def write_coil(self, reg_address, value):
        write_status = False
        try:
            logger.info(f"TRY write value in registers")
            self.client.write_single_coil(reg_address, value)
            write_status = True
        except Exception as e:
            logger.exception(f"FAIL write value in registers\n{e}")
        return write_status

    def disconnect(self):
        try:
            self.client.close()
            logger.debug('CLOSE connection')
        except Exception as e:
            logger.exception(e)
