import csv
import datetime
import json
import sys
import time
from logging.config import fileConfig

import paho.mqtt.client as mqtt

from .arduino import Arduino

start = datetime.datetime.now()
startstr = start.strftime("%y%m%d%H%M%S")
fileConfig("client/logging.conf", defaults={"date": startstr}, disable_existing_loggers=False)

client = mqtt.Client()
client.username_pw_set("ham", "thinkleg")
client.connect(sys.argv[1], 1883, 60)
client.loop_start()

with Arduino() as arduino:
  time.sleep(1)  # 起動待ち
  arduino.start()
  with open(f"log/{startstr}.csv", 'a') as f:
    try:
      while True:
        arduino.read()
        records = arduino.get_record()
        writer = csv.writer(f, lineterminator="\n")
        while not records.empty():
          record = records.get()
          writer.writerow(record)
          date = start + datetime.timedelta(milliseconds=int(record[0]))
          dataobj = {"date": date.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], "leg": record[1]}
          client.publish("test", json.dumps(dataobj))
    except KeyboardInterrupt:
      exit()
