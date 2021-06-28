import unittest
from logging import DEBUG, getLogger

from arduino import Arduino


class TestArduino(unittest.TestCase):
  def test_initialize(self):
    logger = getLogger()
    with self.assertLogs(logger=logger, level=DEBUG) as cm:
      Arduino()
    self.assertEqual(cm.output, ['DEBUG:arduino:Arduino initialized'])


if __name__ == '__main__':
  unittest.main()
