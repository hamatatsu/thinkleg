import datetime
import json
import sys
import time
from logging.config import fileConfig
import paho.mqtt.client as mqtt

from .arduino import Arduino

date = datetime.datetime.now().strftime("%y%m%d%H%M%S")
fileConfig("client/logging.conf", defaults={"date":date}, disable_existing_loggers=False)

client = mqtt.Client()
client.username_pw_set("ham", "thinkleg")
client.connect(sys.argv[1], 1883, 60)
client.loop_start()

with Arduino() as arduino:
  time.sleep(1)
  arduino.start()
  try:
    while True:
      data = arduino.read()
      arduino.save_csv(f"log/{date}.csv")
      if data:
        for d in data:
          (date, leg) = d.decode().strip().split(',')
          client.publish("test", json.dumps({"date":date, "leg":leg}))
  except KeyboardInterrupt:
    exit()
