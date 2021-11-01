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
    self.records = queue.Queue()
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
      exit(1)
    self.logger.debug("Arduino opened")

  def close(self):
    self.ser.write(b'2')
    self.ser.close()
    self.logger.debug("Arduino closed")

  def start(self):
    self.ser.write(b'1')
    self.logger.debug("Arduino started")

  def get_port(self):
    ports = list_ports.comports()
    print([info.description for info in ports])
    # .descriptionでデバイスの名前を取得出来る
    device = [info for info in ports if "Arduino" in info.description]
    if not len(device) == 0:
      return device[0].device
    else:
      self.logger.error('Arduino not connected')
      return '/dev/ttyACM0'

  def read(self):
    data = self.ser.readlines()
    if data:
      for d in data:
        self.records.put(d.decode().strip().split(','))
      # self.logger.debug("Arduino read")
    return data

  def records_is_empty(self):
    return self.records.empty()

  def get_record(self):
    return self.records
