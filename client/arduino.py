import csv
import queue
from logging import getLogger

import serial


class Arduino():
  def __init__(self, port='/dev/ttyACM0', baudrate=115200, timeout=0.01):
    self.logger = getLogger(__name__)
    self.ser = serial.Serial()
    self.port = port
    self.baudrate = baudrate
    self.timeout = timeout
    self.record = queue.Queue()
    self.logger.debug("Arduino initialized")

  def __enter__(self):
    self.open()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.close()

  def open(self):
    self.ser.port = self.port
    self.ser.baudrate = self.baudrate
    self.ser.timeout = self.timeout
    try:
      self.ser.open()
    except serial.serialutil.SerialException:
      self.logger.error("Serial port not found")
      return
    self.logger.debug("Arduino opened")

  def close(self):
    self.ser.write(b'2')
    self.ser.close()
    self.logger.debug("Arduino closed")
  
  def start(self):
    self.ser.write(b'1')

  def read(self):
    data = self.ser.readlines()
    if data:
      for d in data:
        self.record.put(d.decode().strip().split(','))
      # self.logger.debug("Arduino read")
    return data

  def get_record(self):
    pass

  def save_csv(self, filename):
    with open(filename, 'a') as f:
      writer = csv.writer(f)
      while not self.record.empty():
        writer.writerow(self.record.get())
    # self.logger.debug("Arduino saved")