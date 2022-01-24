import BAC0
from loguru import logger


class BACnet:
    def __init__(self, host_ip="10.21.103.245", netmask='24', listen_port=47808):
        self.my_interface = host_ip
        self.netmask = netmask
        self.listen_port = listen_port

    def create_client(self):
        try:
            self.bacnet_client = BAC0.lite(ip=f'{self.my_interface}/{self.netmask}', port=self.listen_port)
            logger.debug("BACNet Client READY")
            return True
        except Exception as e:
            logger.exception("Can't create BACNet Client", e)
        return False

    def read_single_single(self, device_ip, object_type, object_id):
        object_types = {"0": 'analogInput', '1': 'analogOutput', '2': 'analogValue', '3': 'binaryInput',
                        '4': 'binaryOutput', '5': 'binaryValue', '13': 'multistateInput', '14': 'multistateOutput',
                        '19': 'multistateValue'}
        obj_type = object_types[str(object_type)]
        result = list()
        try:
            present_value = self.bacnet_client.read(f'{device_ip}/{self.netmask} {obj_type} {object_id} presentValue')
            result.append(present_value)
            status_flags = self.bacnet_client.read(f'{device_ip}/{self.netmask} {obj_type} {object_id} statusFlags')
            result.append(status_flags)
            reliability = self.bacnet_client.read(f'{device_ip}/{self.netmask} {obj_type} {object_id} reliability')
            result.append(reliability)
            priority_array = self.bacnet_client.read(f'{device_ip}/{self.netmask} {obj_type} {object_id} priorityArray')
            result.append(priority_array)
            return result
        except Exception as e:
            logger.exception(f"Can't read property {device_ip} {obj_type} {object_id}", e)
        return False

    def read_multiple_single(self, device_ip, object_type, object_id):
        object_types = {"0": 'analogInput', '1': 'analogOutput', '2': 'analogValue', '3': 'binaryInput',
                        '4': 'binaryOutput', '5': 'binaryValue', '13': 'multistateInput', '14': 'multistateOutput',
                        '19': 'multistateValue'}
        obj_type = object_types[str(object_type)]
        try:
            properties = self.bacnet_client.readMultiple(f'{device_ip}/{self.netmask} {obj_type} {object_id}'
                                                         f' presentValue statusFlags reliability priorityArray')
            return properties
        except Exception as e:
            logger.exception(f"Can't read property {device_ip} {obj_type} {object_id}", e)
        return False

    def read_multiple_multiple(self, device_ip, objects_dict):
        objects = dict()
        _rpm = {'address': device_ip}
        for i in objects_dict:
            key_0 = i['object_type']
            key_1 = i['object_id']
            properties = ['presentValue', 'statusFlags', 'priorityArray', 'reliability']
            objects.update({f"{key_0}:{key_1}": properties})
        _rpm['objects'] = objects
        try:
            read_result = self.bacnet_client.readMultiple('303:9', request_dict=_rpm)
            return read_result
        except Exception as e:
            logger.exception("Can't read Property", e)
        return False

    def write_single(self, device_ip, object_type, object_id, value, priority):
        try:
            self.bacnet_client.write(f'{device_ip} {object_type} {object_id} presentValue {value} - {priority}')
        except Exception as e:
            logger.exception("Can't write set-point", e)

    def who_is(self):
        try:
            i_am_list = self.bacnet_client.whois()
            if len(i_am_list) > 0:
                for i in i_am_list:
                    name_vendor = self.bacnet_client.readMultiple(
                        f'{i[0]}/{self.netmask} device {i[1]} objectName vendorName')
                    if len(name_vendor) == 2:
                        logger.info(
                            f'IP-address: {i[0]} | Device-ID: {i[1]} | Device-Name: {name_vendor[0]} | Vendor: {name_vendor[1]}')
                    else:
                        logger.debug(f"Can't get DeviceName and VendorName of device{i[1]}")
            else:
                logger.error("No response I-AM")

        except Exception as e:
            logger.exception("Can't send WHO-IS", e)

    def get_object_list(self, device_ip, device_id):
        try:
            object_list = self.bacnet_client.read(f'{device_ip}/{self.netmask} device {device_id} objectList')
            objects_len = len(object_list)
            if objects_len > 0:
                for i in object_list:
                    name_desc = self.bacnet_client.read(f'{device_ip}/{self.netmask} {i[0]} {i[1]} objectName')
                    logger.info(f'{i} | {name_desc}')
        except Exception as e:
            logger.exception("Can't get object-list", e)

    def disconnect(self):
        try:
            self.bacnet_client.disconnect()
            logger.debug("BACnet client DISCONNECTED")
        except Exception as e:
            logger.exception(e)
