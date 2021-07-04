import signal
import threading
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
    signal.signal(signal.SIGALRM, self.handler)
    while True:
      read = threading.Thread(target=self.read_data)
      read.start()
      time.sleep(0.01)

  def write_data(self):
    t = int((time.time() - self.basetime) * 1000)
    data = f"{t},{200}\n"
    self.ser.write(data.encode())

  def read_data(self):
    data = self.ser.read()
    if data == b'0':
      self.ser.write("ready\n".encode())
    elif data == b'1':
      self.start()
    elif data == b'2':
      self.stop()

  def handler(self, num, frame):
    write = threading.Thread(target=self.write_data)
    write.start()

  def start(self):
    self.basetime = time.time()
    signal.setitimer(signal.ITIMER_REAL, 0.001, self.interval)

  def stop(self):
    signal.setitimer(signal.ITIMER_REAL, 0, self.interval)


with _serial as ser:
  Emulator(RATE, ser)
