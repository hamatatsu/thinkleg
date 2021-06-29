import unittest
from logging import DEBUG, getLogger

from arduino import Arduino


class TestArduino(unittest.TestCase):
  def setUp(self):
    self.logger = getLogger()

  def test_initialize(self):
    with self.assertLogs(logger=self.logger, level=DEBUG) as cm:
      Arduino()
    self.assertTrue("DEBUG:arduino:Arduino initialized" in cm.output)

  def test_connect(self):
    with self.assertLogs(logger=self.logger, level=DEBUG) as cm, Arduino(port='dev/ttyACM1'):
      pass
    self.assertTrue("ERROR:arduino:Serial port not found" in cm.output)
    with self.assertLogs(logger=self.logger, level=DEBUG) as cm, Arduino():
      pass
    self.assertTrue("DEBUG:arduino:Arduino opened" in cm.output)


if __name__ == '__main__':
  unittest.main()
