import serial

_serial = serial.Serial()
_serial.port = '/dev/ttyACM0'
_serial.baudrate = 9600
_serial.timeout = 0.01

with _serial as ser:
  print(ser.name)
  ser.flush()
  while(True):
    data = ser.readlines()
    if len(data) != 0:
      for d in data:
        print(d.decode())