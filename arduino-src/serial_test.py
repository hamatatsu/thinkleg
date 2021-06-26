import serial
import time

_serial = serial.Serial()
_serial.port = '/dev/ttyACM0'
_serial.baudrate = 9600
_serial.timeout = 0.01

with _serial as ser:
  print(ser.name)
  ser.flush()
  data = 0
  while(True):
    # data = time.time()
    data += 1
    ser.write((str(data)).encode())
    print(data)
    time.sleep(0.1)