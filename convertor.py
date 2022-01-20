from easymodbus.modbusClient import convert_registers_to_float


class Convertor:
    def __init__(self, signals, data_values):
        self.signals = signals
        self.data_values = data_values
        self.reg_address = signals['reg_address']
        self.bit_number = signals['bit_number']
        self.value_type = signals['value_type']
        self.present_value = signals['present_value']
        self.uuid = signals['uuid']

    def __to_bool(self, value, bit_number=99):
        if bit_number == 99:
            if value != 0:
                return 'true'
            else:
                return 'false'
        elif 16 > bit_number >= 0:
            bin_value = self.__to_16bit(value)[bit_number]
            if bin_value == '0':
                return 'false'
            else:
                return 'true'

    def __to_uint(self, value):
        if value >= 0:
            return value
        else:
            bin_value = self.__to_16bit(value)
            bin_value = '0b0' + bin_value
            uint_value = int(bin_value, 2)
            return uint_value

    def __to_16bit(self, value):
        bin_value = bin(value[0])[2:]
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

    def convert(self):
        count = len(self.uuid)
        print(count)
        i = 0
        index_data_value = 0
        while i < count:
            if self.bit_number[i] == 'none' or self.bit_number[i] != 'none' and self.value_type[i] != 'bool':
                # Запись значения типа INT
                if self.value_type[i] == 'int':
                    coef = 1
                    pv = self.data_values[index_data_value:index_data_value + 1]
                    self.present_value.append(pv[0])
                    i += coef
                    index_data_value += coef
                # Запись значения типа UINT
                elif self.value_type[i] == 'uint':
                    coef = 1
                    if self.data_values[index_data_value:index_data_value + 1][0] != 'fault':
                        pv = self.__to_uint(self.data_values[index_data_value:index_data_value + 1])
                        self.present_value.append(pv)
                    else:
                        pv = self.data_values[index_data_value:index_data_value + 1]
                        self.present_value.append(pv[0])
                    index_data_value += coef
                    i += 1
                elif self.value_type[i] == 'bool':
                    coef = 1
                    if self.data_values[index_data_value:index_data_value + 1][0] != 'fault':
                        pv = self.__to_bool(self.data_values[index_data_value:index_data_value + 1])
                        self.present_value.append(pv)
                    else:
                        pv = self.data_values[index_data_value:index_data_value + 1]
                        self.present_value.append(pv[0])
                    index_data_value += coef
                    i += 1
                elif self.value_type[i] == 'float':
                    coef = 2
                    big = self.data_values[index_data_value:index_data_value + 1]
                    little = self.data_values[index_data_value + 1:index_data_value + 2]
                    if big[0] != 'fault' or little[0] != 'fault':
                        print(big[0], little[0])
                        pv = convert_registers_to_float([big[0], little[0]])
                        self.present_value.append(pv[0])
                    else:
                        pv = self.data_values[index_data_value:index_data_value + 1]
                        self.present_value.append('fault')
                    index_data_value += coef
                    i += 1
            elif self.value_type[i] == 'bool' and self.bit_number[i] != 'none':
                coef = 1
                while self.reg_address[i] == self.reg_address[i + 1] or self.reg_address[i] == self.reg_address[i - 1]:
                    if self.data_values[index_data_value:index_data_value + 1][0] != 'fault':
                        print(self.data_values[index_data_value:index_data_value + 1])
                        pv = self.__to_bool(self.data_values[index_data_value:index_data_value + 1], self.bit_number[i])
                        self.present_value.append(pv)
                    else:
                        self.present_value.append('fault')
                    i += 1
                index_data_value += coef
        return self.signals
