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
    self.nexttime = 0
    self.writeFlag = False
    signal.signal(signal.SIGALRM, self.handler)
    while True:
      read = threading.Thread(target=self.read_data)
      read.start()
      currenttime = time.time()
      if(self.writeFlag and currenttime >= self.nexttime) {
        write_data()
        nexttime += interval;
      }

  def write_data(self):
    t = int((time.time() - self.basetime) * 1000)
    data = f"{t},{200}\n"
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
