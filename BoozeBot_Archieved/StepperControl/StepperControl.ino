/*
runTime for parastaltic pumps should be calculated based on the maximum flowrate of parastaltics.
This program will ensure the same volume as maximum flow rate by accounting for acceleration time.
Because of this you may notice a difference between the runtime you send and the actuall runtime of the parastaltics but volume will always be the same as if run at max speed.
*/

/*defines pump numbers*/
#define PARASTALTICNUM 4
#define SOLENOIDNUM 4
#define PUMPNUM 12

/*defines the first pins to be assigned*/
#define PARASTART 7
#define SOLENOIDSTART (PARASTART + (2*PARASTALTICNUM))

/*defines speed of parastaltics*/
#define PERIOD 170
#define CIRCUMFRENCE 100

/*function pre-declaration*/
void InitParastalticPins(int ParastalticArray[PARASTALTICNUM][2]);
void InitSolenoidPins(int solenoidArray[SOLENOIDNUM]);
int accelerationStepper(int initial, int last, int increment, int stepPin);
void constantStepper(long int runtime, int period, int stepPin);
void ArrayToZero(int *list, int len);
String GetSerialString();
void SerialInterperate(String serialIn, int *pumpTimeS);
long int pumpTimeToRunLoop(int pumpTime, int period);
long int distanceToRunLoop(int distance);
void startupLinearRail(int period, int distance, int dir, int *LinearRail);
void startupParastaltic(int period, int runTime, int parastaltic);
void runSolenoid(int pumpTime, int solenoid);

const int butPin = 2; /*button interupt, safety function*/
const int endStop1 = 3;
const int endStop2 = 4;
const int linearRail[2] = {5, 6};
int parastalticArray[PARASTALTICNUM][2]; /*array of parastaltic motors pumps, each index is stepPin|directionPin*/
int solenoidArray[SOLENOIDNUM];
static int broken = 0;

void setup()
{
  InitParastalticPins(parastalticArray); /*sets all parastaltic pins*/
  InitSolenoidPins(solenoidArray); /*sets all solenoid pins*/
  /*sets linearRail pins*/
  pinMode(linearRail[0],OUTPUT); /*step pin*/
  pinMode(linearRail,OUTPUT); /*direction pin*/
  pinMode(butPin,CHANGE);
  attachInterrupt(0, InterruptFunction, CHANGE);
  pinMode(endStop1,CHANGE);
  attachInterrupt(0, InterruptFunction, CHANGE);
  pinMode(endStop2,CHANGE);
  attachInterrupt(0, InterruptFunction, CHANGE);
  Serial.begin(9600);
}

void loop()
{
  String serialIn = "000000000000000000000000";
  int pumpTimeS[PUMPNUM];
  for(int parastaltic=0;parastaltic<PARASTALTICNUM;parastaltic++)
  {
    digitalWrite(parastalticArray[parastaltic][1], HIGH); /*sets parastaltics direction*/
  }
  ArrayToZero(pumpTimeS, PUMPNUM); /*sets all run times to zero for safety*/
  serialIn = GetSerialString(); /*gets instructions from serial*/

  SerialInterperate(serialIn, pumpTimeS); /*interperates instructions from serial*/

  /*runs parastaltics according to instructions*/
  startupLinearRail(PERIOD, 1000, HIGH, linearRail);
  for (int ii=0;ii<PARASTALTICNUM;ii++)
  {
    startupParastaltic(PERIOD, pumpTimeS[ii], ii);
    Serial.println(pumpTimeS[ii]);
  }
  startupLinearRail(PERIOD, 500, LOW, linearRail);
  for (int ii=0;ii<SOLENOIDNUM;ii++)
  {
    runSolenoid(pumpTimeS[PARASTALTICNUM + ii], solenoidArray[ii]);
    Serial.println(pumpTimeS[PARASTALTICNUM + ii]);
  }
  startupLinearRail(PERIOD, 500, LOW, linearRail);
  Serial.println("Done Order");
 }

/*inititialises all parastaltic pump pins*/
void InitSolenoidPins(int solenoidArray[SOLENOIDNUM])
{
  int pinNumber = SOLENOIDSTART;

  /*assigns pins to motor*/
  for(int solenoid=0;solenoid<SOLENOIDNUM;solenoid++)
  {
    solenoidArray[solenoid] = pinNumber;
    pinNumber++;
  }

  /*sets pins as OUTPUT*/
  for(int solenoid=0;solenoid<SOLENOIDNUM;solenoid++)
  {
    pinMode(solenoidArray[solenoid],OUTPUT); /*step pin*/
  }
}

/*inititialises all parastaltic pump pins*/
void InitParastalticPins(int parastalticArray[PARASTALTICNUM][2])
{
  int pinNumber = PARASTART;

  /*assigns pins to motor*/
  for(int parastaltic=0;parastaltic<PARASTALTICNUM;parastaltic++)
  {
    for(int pin=0;pin<2;pin++)
    {
      parastalticArray[parastaltic][pin] = pinNumber;
      pinNumber++;
    }
  }

  /*sets pins as OUTPUT*/
  for(int parastaltic=0;parastaltic<PARASTALTICNUM;parastaltic++)
  {
    pinMode(parastalticArray[parastaltic][0],OUTPUT); /*step pin*/
    pinMode(parastalticArray[parastaltic][1],OUTPUT); /*direction pin*/
  }
}

/*starts and runs parastaltic pumps for correct time*/
void startupParastaltic(int period, int pumpTime, int parastaltic)
{
  int stage = 0; /*0=accellerating,!0=running*/
  static int accelIncrement = 25;
  static int initialPeriod = 1000; /*start point of accelleration, should be larger than endpoint*/
  long int runLoop = pumpTimeToRunLoop(pumpTime, period); /*amount of turns required by parastaltic pump*/
  Serial.println(runLoop);
  if(stage==0)
  {
    runLoop = runLoop - accelerationStepper(initialPeriod, period, accelIncrement, parastalticArray[parastaltic][0]); /*accounts for loops used by acceleration stage*/
    stage++;
  }
  Serial.println(runLoop);
  constantStepper(runLoop, period, parastalticArray[parastaltic][0]);
}

/*starts and runs parastaltic pumps for correct time*/
void runSolenoid(int pumpTime, int solenoid)
{
  if(broken == 0)
  {
    digitalWrite(solenoid, HIGH);
    delay(pumpTime*1000);
    digitalWrite(solenoid, LOW);
  }
  /*if(reading != LOW)
  {
    exit;
  }*/
}

/*starts and runs Linear Rail for correct distance in mm*/
void startupLinearRail(int period, int distance, int dir, int *stepper)
{
  int stage = 0; /*0=accellerating,!0=running*/
  static int accelIncrement = 25;
  static int initialPeriod = 1000; /*start point of accelleration, should be larger than endpoint*/
  int stepPin = stepper[0];
  int dirPin = stepper[1];
  long int runLoop = distanceToRunLoop(distance); /*amount of turns required by parastaltic pump*/
  Serial.println(runLoop);
  digitalWrite(dirPin,dir);
  if(stage==0)
  {
    runLoop = runLoop - accelerationStepper(initialPeriod, period, accelIncrement, stepPin); /*accounts for loops used by acceleration stage*/
    stage++;
  }
  Serial.println(runLoop);
  constantStepper(runLoop, period, stepPin);
}

/*accelerates parastaltic pump to desired speed*/
int accelerationStepper(int initial, int last, int increment, int stepPin)
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

/*runs parastaltic pump to desired speed*/
void constantStepper(long int runLoop, int period, int stepPin)
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

/*converts pumpTime in seconds to number of loop turns from parastaltic pump*/
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

/*converts pumpTime in seconds to number of loop turns from parastaltic pump*/
long int distanceToRunLoop(int distance)
{
  float turns = distance/CIRCUMFRENCE;
  Serial.println(turns);
  long int runLoop;
  runLoop = (float)4*turns;
  return runLoop;
}

void InterruptFunction() {
  Serial.println("motor shutting down");
  broken = 1;
}
