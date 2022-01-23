class Grouper:
    def __init__(self, signals_dict):
        self.return_dict = {'start_address': [], 'read_quantity': [], 'reg_type': [], 'reg_address': [],
                            'signal_quantity': [], 'value_type': [], 'bit_number': [], 'uuid': [], 'present_value': [],
                            'scale': []}
        self.signals = signals_dict
        self.len_signals = len(self.signals) - 1
        self.reg_address = list()
       # self.signal_quantity = list()
        self.query_quantity = list()
        self.reg_type = list()
        self.value_type = list()
        self.bit_number = list()
        self.id = list()
        self.scale = list()
        for i in self.signals:
            self.reg_address.append(i['register_address'])
          #  self.signal_quantity.append(i['quantity'])
            self.query_quantity.append(i['quantity'])
            self.reg_type.append(i['registers_type'])
            self.value_type.append(i['value_type'])
            self.bit_number.append(i['bit_number'])
            self.id.append(i['signal_id'])
            self.return_dict['scale'].append(i['scale'])
        self.start_register = self.reg_address[0]
        self.read_quantity = None

    def append_data(self, *args):
        self.return_dict['reg_address'].append(args[0])
        self.return_dict['signal_quantity'].append(args[1])
        self.return_dict['value_type'].append(args[2])
        if args[3] is not None:
            self.return_dict['bit_number'].append(args[3])
        else:
            self.return_dict['bit_number'].append('none')
        self.return_dict['uuid'].append(args[4])

    def grouping(self):
        self.read_quantity = self.query_quantity[0]
        idx = -1
        while idx < self.len_signals:
            idx += 1
            if idx != self.len_signals:
                # Если адрес регистра + длина запроса равны по значению следующему адресу и тип регистра одинаковый
                if (self.reg_address[idx] + self.query_quantity[idx] == self.reg_address[idx + 1]) and \
                        (self.reg_type[idx] == self.reg_type[idx + 1]):
                    self.read_quantity += self.query_quantity[idx + 1]
                    self.append_data(self.reg_address[idx], self.query_quantity[idx],
                                     self.value_type[idx], self.bit_number[idx], self.id[idx])
                # Если адрес регистра такой же как и у следующего и у них одинаковый тип регистра
                elif (self.reg_address[idx] == self.reg_address[idx + 1]) and \
                        (self.reg_type[idx] == self.reg_type[idx + 1]):
                    self.append_data(self.reg_address[idx], self.query_quantity[idx],
                                     self.value_type[idx], self.bit_number[idx], self.id[idx])
                # Если адрес регистра такой же как у предыдущего и не такой, как у следующего
                elif (self.reg_address[idx] == self.reg_address[idx - 1]) and (self.reg_address[idx] != self.reg_address[idx + 1]):

                    self.return_dict['start_address'].append(self.start_register)
                    self.return_dict['read_quantity'].append(self.read_quantity)
                    self.return_dict['reg_type'].append(self.reg_type[idx])
                    self.start_register = self.reg_address[idx + 1]
                    self.read_quantity = self.query_quantity[idx + 1]
                # Любая иная ситуация
                else:
                    if (self.reg_address[idx] - self.query_quantity[idx - 1] == self.reg_address[idx - 1]) and \
                            (self.reg_type[idx] == self.reg_type[idx - 1]):
                        self.append_data(self.reg_address[idx], self.query_quantity[idx],
                                         self.value_type[idx], self.bit_number[idx], self.id[idx])
                        self.return_dict['start_address'].append(self.start_register)
                        self.return_dict['read_quantity'].append(self.read_quantity)
                        self.return_dict['reg_type'].append(self.reg_type[idx])
                        self.start_register = self.reg_address[idx + 1]
                        self.read_quantity = self.query_quantity[idx + 1]
                    else:
                        self.return_dict['start_address'].append(self.start_register)
                        self.return_dict['read_quantity'].append(self.query_quantity[idx])
                        self.return_dict['reg_type'].append(self.reg_type[idx])
                        self.start_register = self.reg_address[idx + 1]
                        self.read_quantity = self.query_quantity[idx + 1]

            else:
                if self.reg_address[idx] - self.query_quantity[idx - 1] == self.reg_address[idx - 1] and \
                        self.reg_type[idx] == self.reg_type[idx - 1]:
                    self.append_data(self.reg_address[idx], self.query_quantity[idx],
                                     self.value_type[idx], self.bit_number[idx], self.id[idx])
                else:
                    self.append_data(self.reg_address[idx], self.query_quantity[idx],
                                     self.value_type[idx], self.bit_number[idx], self.id[idx])
                    self.read_quantity = self.query_quantity[idx]
        self.return_dict['start_address'].append(self.start_register)
        self.return_dict['read_quantity'].append(self.read_quantity)
        self.return_dict['reg_type'].append(self.reg_type[idx])
        return self.return_dict
