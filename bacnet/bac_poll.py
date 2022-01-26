from bacnet.driver import BACnet
from loguru import logger
from database.driver import DBDriver


class BACPoll:
    def __init__(self, device):
        self.device = device
        self.db = DBDriver()
        self.bac_client = BACnet(host_ip=device['ip_address'], listen_port=device['tcp_port'])

    def get_signals(self):
        if self.db.connect():
            signals_query = f"SELECT*FROM modbus WHERE `device_id`  = {self.device['device_id']} ORDER BY" \
                            f" `object_type`, `object_id`"
            self.signals = self.db.db_get(signals_query)
            if self.signals != tuple():
                len_signals = len(self.signals)
                logger.info(f"{len_signals} signals into device-{self.device['device_id']}")
                return True
            else:
                logger.error(f"No signals into DB of device {self.device['device_id']}")
                return False
        else:
            logger.error("Can't connecting to DB")
            return False

    def read(self):
        if self.bac_client.create_client():
            if self.device['read_multiple'] != 'MULTI_MULTI':
                for signal in self.signals:
                    if self.device['read_multiple'] == 'SINGLE':
                        result_rss = self.bac_client.read_single_single(self.device['ip_address'],
                                                                    signal['object_type'], signal['object_id'])
                    elif self.device['read_multiple'] == 'MULTI':
                        result_rms = self.bac_client.read_multiple_single(self.device['ip_address'],
                                                                    signal['object_type'], signal['object_id'])
            elif self.device['read_multiple'] == 'MULTI_MULTI':
                    result_rmm = self.bac_client.read_multiple_multiple(self.device['ip_address'], self.signals)

