int dirPin = 4;
int stepPin = 3;
int dist;
int period = 700;

void setup() {
  Serial.begin(9600);
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

int Acc(int finP, int stepPin);
int Dcc(int initP, int stepPin);

void loop() {
  digitalWrite(dirPin, HIGH);
  Serial.println(Acc(period, stepPin));
  for (int i = 0; i < 2000; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(700);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(700);
   }
   Serial.println(Dcc(period, stepPin));

   digitalWrite(dirPin, LOW);
   Serial.println(Acc(period, stepPin));
   for (int i = 0; i < 2000; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(700);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(700);
   }
   Serial.println(Dcc(period, stepPin));  
   if (Serial.available() > 1) {
    char input[10];
    byte size = Serial.readBytes(input, 10);
    input[size] = 0;

    char* command;
    command = strtok(input, " ");

    if ((strcmp(command, "a") == 0) || (strcmp(command, "A") == 0)) {
      digitalWrite(dirPin, HIGH);
    } else if ((strcmp(command, "d") == 0) || (strcmp(command, "D") == 0)) {
      digitalWrite(dirPin, LOW);
    } else {
      Serial.println("You are sussy baka");
      return;
    }
    
    command = strtok(NULL, " ");
    dist = atoi(command) * 5;

    if (dist > 156) {
      Serial.println(Acc(period, stepPin));
      for (int i = 0; i < dist - 156; i++) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(700);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(700);
      }
      Serial.println(Dcc(period, stepPin));
    } else {
      for (int i = 0; i < dist; i++) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(2500);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(2500);
      }
    }
  }
}

int Acc(int finP, int stepPin) {
  int inc = 100;
  int initP = 5000;
  int steps = 0;
  for (int period = initP; period >= finP; period = period - inc) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(period);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(period);
    if (inc > 2) {
      inc = inc - 1;
    }
    steps++;
  }
  return steps;
}

int Dcc(int initP, int stepPin) {
  int inc = 1;
  int finP = 5000;
  int steps = 0;
  for (int period = initP; period <= finP; period = period + inc) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(period);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(period);
    if (inc < 100) {
      inc = inc + 1;
    }
    steps++;
  }
  return steps;
}
