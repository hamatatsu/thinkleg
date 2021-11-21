import csv
import datetime
import json
import os
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


def make_dataobjs(record):
  date = start + datetime.timedelta(milliseconds=int(record[0]))
  return {"date": date.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], "leg": record[1]}


with Arduino() as arduino:
  time.sleep(1)  # 起動待ち
  arduino.start()
  with open(f"log/{startstr}.csv", 'a') as f:
    try:
      writer = csv.writer(f, lineterminator="\n")
      while True:
        records = arduino.read()
        # print(records[:10])
        if not records: break
        dataobjs = list(map(make_dataobjs, records))
        writer.writerows(records)
        client.publish(f"legdata/{os.uname()[1]}", json.dumps(dataobjs))
        # client.publish(f"legdata/test", json.dumps(dataobjs))
        time.sleep(2)
    except KeyboardInterrupt:
      exit()