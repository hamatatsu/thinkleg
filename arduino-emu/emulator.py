import math
import time

import serial

_serial = serial.Serial()
_serial.port = '/dev/ttyACM0'
_serial.baudrate = 115200
_serial.timeout = 0.01

RATE = 50


class Emulator():
  def __init__(self, rate, ser):
    self.rate = rate
    self.interval = 1 / self.rate
    self.ser = ser
    self.basetime = 0
    self.nexttime = 0
    self.writeFlag = False
    while True:
      currenttime = time.time()
      if self.writeFlag and currenttime >= self.nexttime:
        self.write_data()
        self.nexttime += self.interval
      if self.ser.in_waiting > 0:
        self.read_data()

  def write_data(self):
    t = int((time.time() - self.basetime) * 1000)
    num = math.floor(math.sin(t*math.pi/1000.0) * 256 + 256)
    data = f"{t},{num}\n"
    self.ser.write(data.encode())

  def read_data(self):
    data = self.ser.read()
    if data == b'0':
      self.ser.write("ready".encode())
    elif data == b'1':
      self.writeFlag = True
      self.basetime = time.time()
      self.nexttime = self.basetime
    elif data == b'2':
      self.writeFlag = False


with _serial as ser:
  print("Emulator started")
  Emulator(RATE, ser)
