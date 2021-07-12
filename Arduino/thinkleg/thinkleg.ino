unsigned long current_time, base_time, next_time;
int val;
bool writeFlag = false;
int rate = 50;
unsigned long interval = 1000 / rate;
int pinNum = 5;

void writeData() {
  val = analogRead(pinNum);
  Serial.print(current_time - base_time);
  Serial.write(",");
  Serial.print(val);
  Serial.println();
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  current_time = millis();
  if (writeFlag && current_time >= next_time) {
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
      next_time = base_time;
      break;
    case 50: // 2
      writeFlag = false;
      break;
  }
}
