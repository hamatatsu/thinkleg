from logging import getLogger

import serial


class Arduino():
  def __init__(self, port='/dev/ttyACM0', baudrate=9600, timeout=1):
    self.logger = getLogger(__name__)
    self.ser = serial.Serial()
    self.port = port
    self.baudrate = baudrate
    self.timeout = timeout
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
    self.ser.close()
    self.logger.debug("Arduino closed")

  def get(self):
    pass
