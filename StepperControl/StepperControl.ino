/*
runTime for stepper motors should be calculated based on the maximum flowrate of steppers.
This program will ensure the same volume as maximum flow rate by accounting for acceleration time.
Because of this you may notice a difference between the runtime you send and the actuall runtime of the steppers but volume will always be the same as if run at max speed.
*/

/*defines pump numbers*/
#define STEPPERNUM 4
#define SOLENOIDNUM 4
#define PUMPNUM 12

/*defines the first pins to be assigned*/
#define STEPSTART 4
#define SOLENOIDSTART 12

/*defines speed of parastaltics*/
#define PERIOD 170

/*function pre-declaration*/
void InitStepperPins(int stepperArray[STEPPERNUM][2]);
int acceleration(int initial, int last, int increment, int stepPin);
void constant(long int runtime, int period, int stepPin);
void ArrayToZero(int *list, int len);
String GetSerialString();
void SerialInterperate(String serialIn, int *pumpTimeS);
long int pumpTimeToRunLoop(int pumpTime, int period);
void startup(int period, int runTime, int stepper);

const int butPin = 2; /*button interupt, safety function*/
int stepperArray[STEPPERNUM][2]; /*array of stepper motors pumps, each index is stepPin|directionPin*/
static int broken = 0;

void setup()
{
  InitStepperPins(stepperArray); /*sets all parastaltic pins*/
  pinMode(butPin,CHANGE);
  attachInterrupt(0, InterruptFunction, CHANGE);
  Serial.begin(9600);
}

void loop()
{
  String serialIn = "000000000000000000000000";
  int pumpTimeS[PUMPNUM];
  for(int stepper=0;stepper<STEPPERNUM;stepper++)
  {
    digitalWrite(stepperArray[stepper][1], HIGH); /*sets parastaltics direction*/
  }
  ArrayToZero(pumpTimeS, PUMPNUM); /*sets all run times to zero for safety*/
  serialIn = GetSerialString(); /*gets instructions from serial*/

  SerialInterperate(serialIn, pumpTimeS); /*interperates instructions from serial*/

  /*runs parastaltics according to instructions*/
  for (int ii=0;ii<STEPPERNUM;ii++)
  {
    startup(PERIOD, pumpTimeS[ii], ii);
    Serial.println(pumpTimeS[ii]);
  }
  Serial.println("exit");
 }

/*inititialises all stepper motor pins*/
void InitStepperPins(int stepperArray[STEPPERNUM][2])
{
  int pinNumber = STEPSTART;

  /*assigns pins to motor*/
  for(int stepper=0;stepper<STEPPERNUM;stepper++)
  {
    for(int pin=0;pin<2;pin++)
    {
      stepperArray[stepper][pin] = pinNumber;
      pinNumber++;
    }
  }

  /*sets pins as OUTPUT*/
  for(int stepper=0;stepper<STEPPERNUM;stepper++)
  {
    pinMode(stepperArray[stepper][0],OUTPUT); /*step pin*/
    pinMode(stepperArray[stepper][1],OUTPUT); /*direction pin*/
  }
}

/*starts and runs stepper motors for correct time*/
void startup(int period, int pumpTime, int stepper)
{
  int stage = 0; /*0=accellerating,!0=running*/
  static int accelIncrement = 25;
  static int initialPeriod = 1000; /*start point of accelleration, should be larger than endpoint*/
  long int runLoop = pumpTimeToRunLoop(pumpTime, period); /*amount of turns required by stepper motor*/
  Serial.println(runLoop);
  if(stage==0)
  {
    runLoop = runLoop - acceleration(initialPeriod, period, accelIncrement, stepperArray[stepper][0]); /*accounts for loops used by acceleration stage*/
    stage++;
  }
  Serial.println(runLoop);
  constant(runLoop, period, stepperArray[stepper][0]);
}

/*accelerates stepper motor to desired speed*/
int acceleration(int initial, int last, int increment, int stepPin)
{
  /*combine runLoop and increment for acceleration smoothness*/
  int runLoop = 100; /* how many loops is one acceleration step*/
  int LoopCount = 0;
  int reading = digitalRead(butPin);

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
      /*if(reading != LOW)
      {
        exit;
      }*/
    }
  }
  return LoopCount; /*returns loosp done by acceleration*/
}

/*runs stepper motor to desired speed*/
void constant(long int runLoop, int period, int stepPin)
{
  /*int reading = digitalRead(butPin);*/

  for(long int z = 0; z<runLoop; z++)
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

/*converts serial input into an array of pump times*/
void SerialInterperate(String serialIn, int *pumpTimeS)
{
  int CharSIndex = 0;
  char SerialCharS[PUMPNUM*2];

  serialIn.toCharArray(SerialCharS, PUMPNUM*2);
  for (int ii=0;ii<PUMPNUM;ii++)
  {
    for (int digit=0;digit<2;digit++)
    {
      if (digit==0)
      {
        pumpTimeS[ii] = ((int)SerialCharS[CharSIndex] - 48) * 10;
      }
      else if (digit==1)
      {
        pumpTimeS[ii] += ((int)SerialCharS[CharSIndex] - 48);
      }
      CharSIndex++;
    }
  }
}

/*sets all values in an array to zero*/
void ArrayToZero(int *list, int len)
{
  for(int ii=0;ii<len;ii++)
  {
    list[ii] = 0;
  }
}

/*gets a serial input in string form, handles wait times and error checking*/
String GetSerialString()
{
  String serialIn;
  serialIn = "0";

  if(serialIn != NULL)
  {
    while(Serial.available()==0);
    {
      serialIn = Serial.readString();
      delay(100);
    }
  }

  return serialIn;
}

/*converts pumpTime in seconds to number of loop turns from stepper motor*/
long int pumpTimeToRunLoop(int pumpTime, int period)
{
  float temp = (1000/(2*(float)period));
  Serial.println(temp);
  long int runTime;
  long int runLoop;
  runTime = 1000*pumpTime;
  runLoop = (float)runTime*temp;
  return runLoop;
}

void InterruptFunction() {
  Serial.println("motor shutting down");
  broken = 1;
}
