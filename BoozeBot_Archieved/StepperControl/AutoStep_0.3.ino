#include "pPump.h"

String inString;
int inMill;
String order[9];
pPump pump[] = {
  pPump(3,2,8,310)}; //(step pin, direction pin, button pin, period)
//fill in more when have more pumps

void setup() {
  Serial.begin(9600);
}

void loop() {
  pump[0].primedrain();
  if (Serial.available() > 0) {
    inString = Serial.readString();

    //splits the 20 character serial input into ten 2 character strings in the order[] array
    for (int i = 0; i < 10 ; i++) { //1 is supposed to be 10 in final run
      int from = 2 * i;
      order[i] = inString.substring(from,from + 2);
      Serial.println(order[i]);
    }

    for (int i = 0; i < 1; i++) {
      if (order[i] == "00") {
        Serial.println("break");
        break;
      } else {
        inMill = order[i].toDouble();
        //function for moving the linear rail will go here
        pump[i].pour(inMill);
        Serial.println(inMill);
      }
    }
    
    
    /*inMill = inString.toInt();
        if (inMill > 3 && inMill < 101) {
            if (inMill != NULL && inMill) {
                pump0.pour(inMill);
                Serial.println("exit");
            }
        }
    } */
  }
}
