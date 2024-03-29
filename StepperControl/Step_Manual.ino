int stepPin = 3;
int initial = 1000;
int last = 310;
int increment = 5;
int runLoop = 20; 
static int broken = 0;
int dirPin = 2;
int inMill=0;

void accelerationStepper(int initial, int last, int increment, int stepPin);
void constantStepper(int inMill, int period, int stepPin);
long int MillToStep(int Mill);


void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  if (Serial.available() > 0) {
    inMill = Serial.parseInt();
    if (inMill > 3 && inMill < 101) {
      if (inMill != NULL) {
        digitalWrite(dirPin, HIGH);
        accelerationStepper(initial, last, increment, stepPin);
        constantStepper(inMill, last, stepPin); 
        Serial.println("exit");
      }
    }
  }
}

/*accelerates parastaltic pump to desired speed*/
void accelerationStepper(int initial, int last, int increment, int stepPin)
{
  /*combine runLoop and increment for acceleration smoothness*/
  /* how many loops is one acceleration step*/
  int LoopCount = 0;

  for(int period = initial; period>=last; period = period - increment)
  {
    for(int x = 0; x < runLoop; x++)
    {
      if(broken == 0)
      {
        digitalWrite(stepPin,HIGH);
        delayMicroseconds(period);
        digitalWrite(stepPin,LOW);
        delayMicroseconds(period);
        LoopCount++;
      }
    }
    Serial.println(period);
  }
  return LoopCount; /*returns loosp done by acceleration*/
}

/*runs parastaltic pump to desired speed*/
void constantStepper(int inMill, int period, int stepPin)
{
  /*int reading = digitalRead(butPin);*/
  

  for(long int z = 0; z<MillToStep(inMill); z++)
  {
    if(broken == 0)
    {
      digitalWrite(stepPin,HIGH);
      delayMicroseconds(period);
      digitalWrite(stepPin,LOW);
      delayMicroseconds(period);
    }
    /*if(reading != LOW)
    {
        exit;
    }*/
  }
  //Serial.println("I am here");
}

long int MillToStep(int Mill)
{
  return 350*Mill - 2760; //350 is roughly 1ml in steps ~ acceleration is exactly 1440 steps
}
