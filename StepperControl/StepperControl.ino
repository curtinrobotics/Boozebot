#define EN 6
#define STEP 5
#define DIR 4

void setup(){

  pinMode(EN, OUTPUT);
  pinMode(STEP, OUTPUT);
  pinMode(DIR, OUTPUT);
  
  
  digitalWrite(EN, LOW);

}

int main()
{

  digitalWrite(DIR, HIGH);
  
  for(int x = 0; x < 200; x++) // Loop 200 times
  {
    digitalWrite(STEP,HIGH);
    delayMicroseconds(10);
    digitalWrite(STEP,LOW);
    delayMicroseconds(10);
  }
  delay(1000);

  return(0);
}
