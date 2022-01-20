import time

from run import Runner
from config import config
import datetime

if __name__ == "__main__":
    while True:

        for device in config.POLLING_DEVICE:
            start = datetime.datetime.now()
            run = Runner(device)
            run.create_device_polling()
            cs = run.polling()
            if cs:
                run.convert()
                run.put_to_db()
            stop = datetime.datetime.now()
            print(f'Circle TIME: {stop - start}')
            time.sleep(3)
