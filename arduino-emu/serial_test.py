import serial
import time

_serial = serial.Serial()
_serial.port = '/dev/ttyACM0'
_serial.baudrate = 9600
_serial.timeout = 0.01

RATE = 10
INTETRVAL = 1 / RATE

with _serial as ser:
  print(ser.name)
  ser.flush()
  data = 0
  while(True):
    # data = time.time()
    data += 1
    ser.write((str(data)+"\n").encode())
    print(data)
    time.sleep(INTETRVAL)