import serial
import time
import datetime
from collections import deque
import csv

_serial = serial.Serial()
_serial.port = '/dev/ttyACM0'
_serial.baudrate = 9600
_serial.timeout = 0.01

FILENAME = datetime.datetime.now().strftime("log/%y%m%d%H%M%S.csv")
RECORD = deque()

with _serial as ser:
  print(ser.name)
  ser.flush()
  while(True):
    data = ser.readlines()
    time.sleep(1)
    if len(data) != 0:
      # RECORD.extend(data)
      decoded = map(lambda d: [d.decode().rstrip("\n")], data)
      with open(FILENAME, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(decoded)
      print(data)
      # for d in data:
      #   print(d)