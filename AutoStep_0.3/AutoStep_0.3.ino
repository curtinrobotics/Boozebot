/*
* This program is the current working version of AutoStep that uses the pPump library
* Programmers: CJD
* Editor: 
* Iteration: 0.3
* Last edited: 02/09/2021
* Created: 18/03/2021
* 
* Dependencies: pPump.h, pPump.cpp
*
* (Soon to be replaced by BBSequence)
*
* Main code for the sequencing of BoozeBot
* Sequences pPump funtions according to customer order
*/

#include "pPump.h"

String inString;
int inMill;
String order[9];
pPump pump[] = {
    pPump(3, 2, 8, 400)}; //(step pin, direction pin, button pin, period)
    //fill in more when have more pumps

void setup() {
  Serial.begin(9600);
}

void loop() {
  /* initiates priming and draining funtion */
  pump[0].primedrain();
  if (Serial.available() > 0) {
    inString = Serial.readString();

    /* splits the 20 character serial input 
      into ten 2 character strings in the order[] array */
    for (int i = 0; i < 10; i++) {
      int from = 2 * i;
      order[i] = inString.substring(from, from + 2);
      Serial.println(order[i]);
    }

    /* cycles through all orders and pumps (currently only 1), 
      pumping the amount the order designates */
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
  }
}
