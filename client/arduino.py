import csv
import queue
from logging import getLogger

import serial
from serial.tools import list_ports


class Arduino():
  def __init__(self, baudrate=115200, timeout=0.01):
    self.logger = getLogger(__name__)
    self.ser = serial.Serial()
    self.port = self.get_port()
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
      raise serial.serialutil.SerialException
    self.logger.debug("Arduino opened")

  def close(self):
    self.ser.write(b'2')
    self.ser.close()
    self.logger.debug("Arduino closed")
  
  def start(self):
    self.ser.write(b'1')
    self.logger.debug("Arduino started")

  def get_port(self):
    ports=list_ports.comports()
    device=[info for info in ports if "Arduino" in info.description] #.descriptionでデバイスの名前を取得出来る
    if not len(device) == 0:
      return device[0].device
    else:
      self.logger.error('Ardunoは接続されていません')
      exit(0)

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
      writer = csv.writer(f, lineterminator="\n")
      while not self.record.empty():
        writer.writerow(self.record.get())
    # self.logger.debug("Arduino saved")