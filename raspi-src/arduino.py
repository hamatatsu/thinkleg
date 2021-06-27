from logging import getLogger

import serial

logger = getLogger(__name__)


class Arduino():
  def __init__(self, port='/dev/ttyGS0', baudrate=9600, timeout=1):
    logger.info("Arduino initialized")
    self.ser = serial.Serial()
    self.port = port
    self.baudrate = baudrate
    self.timeout = timeout

  def __enter__(self):
    logger.info("Arduino enter")
    self.open()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    logger.info("Arduino exit")
    self.close()

  def open(self):
    logger.info("Arduino open")
    self.ser.port = self.port
    self.ser.baudrate = self.baudrate
    self.ser.timeout = self.timeout
    self.ser.open()

  def close(self):
    logger.info("Arduino close")
    self.ser.close()

  def get(self):
    logger.info("Arduino get")
    pass


def main():
  with Arduino() as arduino:
    arduino.get()
    while(True):
      pass

  logger.info("end")


if __name__ == "__main__":
  # execute only if run as a script
  main()
