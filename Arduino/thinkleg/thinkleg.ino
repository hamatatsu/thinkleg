unsigned long current_time, base_time, next_time;
int val0;
bool writeFlag = false;
int rate = 50;
unsigned long interval = 1000 / rate;

void writeData() {
  current_time = millis();
  val0 = analogRead(0);
  Serial.print(current_time - base_time);
  Serial.write(",");
  Serial.print(val0);
  Serial.println();
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  current_time = millis();
  if (writeFlag && current_time > next_time) {
    writeData();
    next_time += interval;
  }
  if (Serial.available() > 0) {
    serialEvent();
  }
}

void serialEvent() {
  int incomingByte = Serial.read();
  switch (incomingByte) {
    case 48: // 0
      Serial.println("ready");
      break;
    case 49: // 1
      writeFlag = true;
      base_time = millis();
      break;
    case 50: // 2
      writeFlag = false;
      break;
  }
}
