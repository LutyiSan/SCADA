class Grouper:
    def __init__(self, signals_dict):
        self.return_dict = {'start_address': [], 'read_quantity': [], 'reg_type': [], 'reg_address': [],
                            'signal_quantity': [], 'value_type': [], 'bit_number': [], 'uuid': [], 'present_value': []}
        self.signals = signals_dict
        self.len_signals = len(self.signals) - 1
        self.reg_address = list()
        self.signal_quantity = list()
        self.query_quanty = list()
        self.reg_type = list()
        self.value_type = list()
        self.bit_number = list()
        self.id = list()
        for i in self.signals:
            self.reg_address.append(i['register_address'])
            self.signal_quantity.append(i['quantity'])
            self.query_quanty.append(i['quantity'])
            self.reg_type.append(i['registers_type'])
            self.value_type.append(i['value_type'])
            self.bit_number.append(i['bit_number'])
            self.id.append(i['signal_id'])
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
        self.read_quantity = self.signal_quantity[0]
        idx = -1
        while idx < self.len_signals:
            idx += 1
            if idx != self.len_signals:
                if self.reg_address[idx] + self.query_quanty[idx] == self.reg_address[idx + 1] and \
                        self.reg_type[idx] == self.reg_type[idx + 1]:
                    self.read_quantity += self.query_quanty[idx + 1]
                    self.append_data(self.reg_address[idx], self.signal_quantity[idx],
                                     self.value_type[idx], self.bit_number[idx], self.id[idx])

                elif self.reg_address[idx] == self.reg_address[idx + 1] and \
                        self.reg_type[idx] == self.reg_type[idx + 1]:
                    self.append_data(self.reg_address[idx], self.signal_quantity[idx],
                                     self.value_type[idx], self.bit_number[idx], self.id[idx])

                elif len(self.return_dict['reg_address']) > 0 and self.reg_address[idx] == \
                        self.reg_address[idx - 1] and \
                        self.reg_type[idx] == self.reg_type[idx + 1]:
                    self.append_data(self.reg_address[idx], self.signal_quantity[idx],
                                     self.value_type[idx], self.bit_number[idx], self.id[idx])

                else:
                    if self.reg_address[idx] - self.query_quanty[idx - 1] == self.reg_address[idx - 1] and \
                            self.reg_type[idx] == self.reg_type[idx - 1]:
                        self.append_data(self.reg_address[idx], self.signal_quantity[idx],
                                         self.value_type[idx], self.bit_number[idx], self.id[idx])
                        self.return_dict['start_address'].append(self.start_register)
                        self.return_dict['read_quantity'].append(self.read_quantity)
                        self.return_dict['reg_type'].append(self.reg_type[idx])
                        self.start_register = self.reg_address[idx + 1]
                        self.read_quantity = self.query_quanty[idx + 1]
                    else:
                        self.append_data(self.reg_address[idx], self.signal_quantity[idx],
                                         self.value_type[idx], self.bit_number[idx], self.id[idx])
                        self.return_dict['start_address'].append(self.start_register)
                        self.return_dict['read_quantity'].append(self.query_quanty[idx])
                        self.return_dict['reg_type'].append(self.reg_type[idx])
                        self.start_register = self.reg_address[idx + 1]
                        self.read_quantity = self.query_quanty[idx + 1]

            else:
                if self.reg_address[idx] - self.query_quanty[idx - 1] == self.reg_address[idx - 1] and \
                            self.reg_type[idx] == self.reg_type[idx - 1]:
                    self.append_data(self.reg_address[idx], self.signal_quantity[idx],
                                     self.value_type[idx], self.bit_number[idx], self.id[idx])
                else:
                    self.append_data(self.reg_address[idx], self.signal_quantity[idx],
                                     self.value_type[idx], self.bit_number[idx], self.id[idx])
                    self.read_quantity = self.signal_quantity[idx]
        self.return_dict['start_address'].append(self.start_register)
        self.return_dict['read_quantity'].append(self.read_quantity)
        self.return_dict['reg_type'].append(self.reg_type[idx])
        return self.return_dict
