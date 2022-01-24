import time
from loguru import logger
from modbus_run import Runner
from database.driver import DBDriver
from config import config


if __name__ == "__main__":
    while True:
        db = DBDriver()
        if db.connect():
            for device in config.POLLING_DEVICE:
                device_settings = db.db_get(f"SELECT*FROM `devices` WHERE `device_id` = {device}")
                if device_settings[0]['protocol'] == 'modbus':
                    start = time.time()
                    run = Runner(device)
                    run.create_device_polling()
                    cs = run.polling()
                    if cs:
                        run.convert()
                        run.put_to_db()
                    stop = time.time()
                    logger.info(f'TIME POLLING device {device}: {stop - start}')
                    time.sleep(0.3)
                else:
                    print("BACnet mode")
        db.disconnect()
