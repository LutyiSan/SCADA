import BAC0
from colorama import Fore


class BACnet:
    def __init__(self, host_ip="10.21.103.245", netmask='24', listen_port=47808):
        self.bacnet_client = None
        self.single_point_list = None
        self.object_dict = {"DEVICE_IP": [], 'DEVICE_ID': [], 'OBJECT_TYPE': [], 'OBJECT_ID': [], 'OBJECT_NAME': [],
                            'DESCRIPTION': []}
        self.i_am_dict = {'DEVICE_IP': [], 'DEVICE_ID': [], "DEVICE_NAME": [], 'VENDOR': []}
        self.my_interface = host_ip
        self.netmask = netmask
        self.listen_port = listen_port

    def create_client(self):
        connect_state = False
        try:
            self.bacnet_client = BAC0.lite(ip=f'{self.my_interface}/{self.netmask}', port=self.listen_port)
            print(Fore.LIGHTGREEN_EX + "BACNet Client READY")
            connect_state = True
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Can't create BACNet Client", e)
        return connect_state

    def who_is(self):
        try:
            i_am_list = self.bacnet_client.whois()
            for i in i_am_list:
                name_vendor = self.bacnet_client.readMultiple(
                    f'{i[0]}/{self.netmask} device {i[1]} objectName vendorName')

                print(Fore.LIGHTGREEN_EX + f'IP-address: {i[0]}  Device-ID: {i[1]}  '
                                           f'Device-Name: {name_vendor[0]}  Vendor: {name_vendor[1]}')
                self.i_am_dict['DEVICE_IP'].append(i[0])
                self.i_am_dict['DEVICE_ID'].append(i[1])
                self.i_am_dict['DEVICE_NAME'].append(name_vendor[0])
                self.i_am_dict['VENDOR'].append(name_vendor[1])
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Can't send who-is", e)
        self.bacnet_client.disconnect()
        return self.i_am_dict

    def read_single(self, device_ip, object_type, object_id):
        object_types = {"0": 'analogInput', '1': 'analogOutput', '2': 'analogValue', '3': 'binaryInput',
                        '4': 'binaryOutput', '5': 'binaryValue', '13': 'multistateInput', '14': 'multistateOutput',
                        '19': 'multistateValue'}
        obj_type = object_types[f'{object_type}']
        try:
            self.single_point_list = self.bacnet_client.readMultiple(
                f'{device_ip}/{self.netmask} {obj_type} {object_id}'
                f' presentValue statusFlags reliability')
            print(Fore.LIGHTGREEN_EX + f'object_type: {obj_type}  object_id:{object_id}\npresent_value:'
                                       f' {self.single_point_list[0]}\n'f'status_flags: {self.single_point_list[1]}\n'
                                       f'reliability: {self.single_point_list[2]}')
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Can't read property", e)
        self.bacnet_client.disconnect()

    def get_object_list(self, device_ip, device_id):
        try:
            object_list = self.bacnet_client.read(
                f'{device_ip}/{self.netmask} device {device_id} objectList')
            objects_len = len(object_list)

            for i in object_list:
                name_desc = self.bacnet_client.read(
                    f'{device_ip}/{self.netmask} {i[0]} {i[1]} objectName')
                self.object_dict['DEVICE_IP'].append(device_ip)
                self.object_dict['DEVICE_ID'].append(device_id)
                self.object_dict['OBJECT_TYPE'].append(i[0])
                self.object_dict['OBJECT_ID'].append(i[1])
                if type(name_desc) is dict:
                    name = list(name_desc.values())[0]
                    self.object_dict['OBJECT_NAME'].append(name)
                else:
                    self.object_dict['OBJECT_NAME'].append(name_desc)
                self.object_dict['DESCRIPTION'].append('unknown')
                print(Fore.LIGHTGREEN_EX + f'OBJECT_TYPE: {i[0]}  OBJECT_ID: {i[1]}  NAME: {name_desc}'
                                           f' DESCRIPTION: unknown')
            print(f"{objects_len}  objects in device")
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Can't get object-list", e)

        self.bacnet_client.disconnect()
        return self.object_dict

    def disconnect(self):
        self.bacnet_client.disconnect()
        pass