from datetime import datetime
import threading
import time

import serial

_serial = serial.Serial()
_serial.port = '/dev/ttyACM0'
_serial.baudrate = 115200
_serial.timeout = 0.01

RATE = 50
INTETRVAL = 1 / RATE

def send_data(ser):
  data = f"{datetime.now()},{200}\n"
  ser.write(data.encode())

def schedule(interval_sec, ser):
  base_timing = time.time()
  while True:
    t = threading.Thread(target=send_data, args = [ser])
    t.start()

    current_timing = time.time()
    sleep_sec = interval_sec - ((current_timing - base_timing) % interval_sec)
    time.sleep(max(sleep_sec, 0))

with _serial as ser:
  schedule(INTETRVAL, ser)

