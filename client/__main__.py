from .arduino import Arduino
from logging.config import fileConfig
import datetime
import time

date = datetime.datetime.now().strftime("%y%m%d%H%M%S")
fileConfig("client/logging.conf", defaults={"date":date}, disable_existing_loggers=False)

with Arduino() as arduino:
  time.sleep(1)
  arduino.start()
  try:
    while True:
      arduino.read()
      arduino.save_csv(f"log/{date}.csv")
  except KeyboardInterrupt:
    exit()
