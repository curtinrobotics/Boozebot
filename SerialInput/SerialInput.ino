  char New = 'O';

  // sets pump output pins
  int pump1 = 2;
  int pump2 = 3;
  int pump3 = 4;
  int pump4 = 5;
  int pump5 = 6;
  int pump6 = 7;
  int pump7 = 8;
  int pump8 = 9;
  int pump9 = 10;
  int pump10 = 11;
  int pump11 = 12;
  int pump12 = 13;

  //initializes pump runtimes
  int pump1Run = -1;
  int pump2Run = -1;
  int pump3Run = -1;
  int pump4Run = -1;
  int pump5Run = -1;
  int pump6Run = -1;
  int pump7Run = -1;
  int pump8Run = -1;
  int pump9Run = -1;
  int pump10Run = -1;
  int pump11Run = -1;
  int pump12Run = -1;


void setup() {
  //initializes pump pins
  pinMode(pump1, OUTPUT);
  digitalWrite(pump1, LOW);
  pinMode(pump2, OUTPUT);
  digitalWrite(pump2, LOW);
  pinMode(pump3, OUTPUT);
  digitalWrite(pump3, LOW);
  pinMode(pump4, OUTPUT);
  digitalWrite(pump4, LOW);
  pinMode(pump5, OUTPUT);
  digitalWrite(pump5, LOW);
  pinMode(pump6, OUTPUT);
  digitalWrite(pump6, LOW);
  pinMode(pump7, OUTPUT);
  digitalWrite(pump7, LOW);
  pinMode(pump8, OUTPUT);
  digitalWrite(pump8, LOW);
  pinMode(pump9, OUTPUT);
  digitalWrite(pump9, LOW);
  pinMode(pump10, OUTPUT);
  digitalWrite(pump10, LOW);
  pinMode(pump11, OUTPUT);
  digitalWrite(pump11, LOW);
  pinMode(pump12, OUTPUT);
  digitalWrite(pump12, LOW);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    //Gets input from serial
    while (New != 'N') {
      New = Serial.read();
    }
    while (pump1Run == -1) {
      pump1Run = atof(Serial.read());
    }
    while (pump2Run == -1) {
      pump2Run = atof(Serial.read());
    }
    while (pump3Run == -1) {
      pump3Run = atof(Serial.read());
    }
    while (pump4Run == -1) {
      pump4Run = atof(Serial.read());
    }
    while (pump5Run == -1) {
      pump5Run = atof(Serial.read());
    }
    while (pump6Run == -1) {
      pump6Run = atof(Serial.read());
    }
    while (pump7Run == -1) {
      pump7Run = atof(Serial.read());
    }
    while (pump8Run == -1) {
      pump8Run = atof(Serial.read());
    }
    while (pump9Run == -1) {
      pump9Run = atof(Serial.read());
    }
    while (pump10Run == -1) {
      pump10Run = atof(Serial.read());
    }
    while (pump11Run == -1) {
      pump11Run = atof(Serial.read());
    }
    while (pump12Run == -1) {
      pump12Run = atof(Serial.read());
    }
    //runs pumps for runtime
    if (pump1Run != 0) {
      digitalWrite(pump1, HIGH);
      delay(1000*pump1Run);
      digitalWrite(pump1, LOW);
    }
    else {
      digitalWrite(pump1, LOW);
    }
    if (pump2Run != 0) {
      digitalWrite(pump2, HIGH);
      delay(1000*pump2Run);
      digitalWrite(pump3, LOW);
    }
    else {
      digitalWrite(pump2, LOW);
    }
    if (pump3Run != 0) {
      digitalWrite(pump3, HIGH);
      delay(1000*pump3Run);
      digitalWrite(pump3, LOW);
    }
    else {
      digitalWrite(pump3, LOW);
    }
    if (pump4Run != 0) {
      digitalWrite(pump4, HIGH);
      delay(1000*pump4Run);
      digitalWrite(pump4, LOW);
    }
    else {
      digitalWrite(pump4, LOW);
    }
    if (pump5Run != 0) {
      digitalWrite(pump5, HIGH);
      delay(1000*pump5Run);
      digitalWrite(pump5, LOW);
    }
    else {
      digitalWrite(pump5, LOW);
    }
    if (pump6Run != 0) {
      digitalWrite(pump6, HIGH);
      delay(1000*pump6Run);
      digitalWrite(pump6, LOW);
    }
    else {
      digitalWrite(pump6, LOW);
    }
    if (pump7Run != 0) {
      digitalWrite(pump7, HIGH);
      delay(1000*pump7Run);
      digitalWrite(pump7, LOW);
    }
    else {
      digitalWrite(pump7, LOW);
    }
    if (pump8Run != 0) {
      digitalWrite(pump8, HIGH);
      delay(1000*pump8Run);
      digitalWrite(pump8, LOW);
    }
    else {
      digitalWrite(pump8, LOW);
    }
    if (pump9Run != 0) {
      digitalWrite(pump9, HIGH);
      delay(1000*pump9Run);
      digitalWrite(pump9, LOW);
    }
    else {
      digitalWrite(pump9, LOW);
    }
    if (pump10Run != 0) {
      digitalWrite(pump10, HIGH);
      delay(1000*pump10Run);
      digitalWrite(pump10, LOW);
    }
    else {
      digitalWrite(pump10, LOW);
    }
    if (pump11Run != 0) {
      digitalWrite(pump11, HIGH);
      delay(1000*pump11Run);
      digitalWrite(pump11, LOW);
    }
    else {
      digitalWrite(pump11, LOW);
    }
    if (pump12Run != 0) {
      digitalWrite(pump12, HIGH);
      delay(1000*pump12Run);
      digitalWrite(pump12, LOW);
    }
    else {
      digitalWrite(pump12, LOW);
    }

    //resets pump runtimes
    New = 'O';
    pump1Run = -1;
    pump2Run = -1;
    pump3Run = -1;
    pump4Run = -1;
    pump5Run = -1;
    pump6Run = -1;
    pump7Run = -1;
    pump8Run = -1;
    pump9Run = -1;
    pump10Run = -1;
    pump11Run = -1;
    pump12Run = -1;
  }
  else {
    }
}
